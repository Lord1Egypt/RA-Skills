#!/usr/bin/env python3
"""Offline newspaper checkpoints and portable exports. Never calls a model."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import uuid
import zipfile

VERSION = "1.0.0"
PAPERS = {"A3": (297, 420), "A4": (210, 297), "A5": (148, 210)}


def now():
    return datetime.now(timezone.utc).isoformat()


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_json(file):
    return json.loads(Path(file).read_text(encoding="utf-8-sig"))


def stable_id(value):
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,95}", value):
        raise ValueError("IDs must use 1-96 ASCII letters, numbers, underscores or hyphens")
    return value


def safe_path(root, relative):
    if not isinstance(relative, str) or "\\" in relative or ":" in relative:
        raise ValueError("Asset path must be a portable relative path")
    item = PurePosixPath(relative)
    if item.is_absolute() or ".." in item.parts or not item.parts:
        raise ValueError("Unsafe asset path")
    root = Path(root).resolve()
    target = root.joinpath(*item.parts)
    if not target.resolve().is_relative_to(root) or target.is_symlink():
        raise ValueError("Asset escapes project or is a symbolic link")
    return target


def load(root):
    project = read_json(Path(root) / "project.json")
    if project.get("schemaVersion") != 1:
        raise ValueError("Unsupported newspaper project schema")
    return project


def save(root, project):
    project["updatedAt"] = now()
    temporary = Path(root) / (".project-" + uuid.uuid4().hex + ".tmp")
    temporary.write_text(json.dumps(project, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(temporary, Path(root) / "project.json")


@contextmanager
def locked(root):
    """Fail clearly instead of overwriting concurrent agent writes."""
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    lock = root / ".project.lock"
    try:
        descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        raise ValueError("Project is locked. Check the owner/process before manually removing a stale .project.lock")
    try:
        os.write(descriptor, str(os.getpid()).encode("ascii"))
        os.close(descriptor)
        yield
    finally:
        lock.unlink(missing_ok=True)


def image_info(file):
    from PIL import Image
    with Image.open(file) as image:
        width, height = image.size
        image.verify()
    return {"width": width, "height": height}


def check_asset(root, asset):
    file = safe_path(root, asset["path"])
    if not file.is_file() or digest(file.read_bytes()) != asset["sha256"]:
        raise ValueError("Missing or changed asset: " + asset["path"])
    return file


def copy_asset(root, project, asset_id, file, role, origin, label=""):
    stable_id(asset_id)
    file = Path(file)
    data = file.read_bytes()
    pixels = image_info(file)
    checksum = digest(data)
    extension = file.suffix.lower()
    if extension not in (".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff"):
        raise ValueError("Supported images: PNG, JPEG, WebP and TIFF")
    relative = "assets/" + checksum + extension
    target = safe_path(root, relative)
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and digest(target.read_bytes()) != checksum:
        raise ValueError("Existing content-addressed asset is corrupt; preserve it for diagnosis")
    if not target.exists():
        temporary = target.with_name(target.name + "." + uuid.uuid4().hex + ".tmp")
        temporary.write_bytes(data)
        os.replace(temporary, target)
    asset = {"id": asset_id, "path": relative, "sha256": checksum, "role": role,
             "origin": origin, "label": label, "pixels": pixels}
    existing = project["assets"].get(asset_id)
    if existing and (existing["sha256"] != checksum or existing["role"] != role):
        raise ValueError("Asset ID already refers to different content or role; use a new ID")
    project["assets"][asset_id] = asset
    return asset


def init(root, title, paper="A4", orientation="portrait", sides="single", pages=2,
         width_mm=None, height_mm=None, delegated_approval=None):
    if (Path(root) / "project.json").exists():
        raise ValueError("Project already exists")
    if not 1 <= pages <= 64:
        raise ValueError("Choose 1-64 pages")
    if paper == "custom":
        if width_mm is None or height_mm is None or min(width_mm, height_mm) <= 0:
            raise ValueError("Custom paper needs positive --width-mm and --height-mm")
        width, height = sorted((width_mm, height_mm))
    else:
        width, height = PAPERS[paper]
    if orientation == "landscape":
        width, height = height, width
    project = {"schemaVersion": 1, "skillVersion": VERSION, "id": uuid.uuid4().hex,
        "title": title, "createdAt": now(), "paper": {"name": paper, "widthMm": width,
        "heightMm": height, "orientation": orientation, "sides": sides},
        "delegatedApproval": delegated_approval, "assets": {}, "tasks": {}, "activeIntents": {}, "pages": {},
        "approvals": {}, "approvalHistory": [], "plan": {"title": title, "style": "",
        "pages": [{"id": f"page-{i + 1:02}", "title": "", "role": "front" if i == 0 else "feature",
                   "summary": "", "visualBrief": "", "articles": []} for i in range(pages)]}}
    save(root, project)
    return {"project": str(Path(root) / "project.json"), "id": project["id"]}


def visual_fields(value):
    # These are display annotations only. Printed copy belongs in articles/instruction.
    return {key: val for key, val in value.items() if key not in ("caption", "rationale")}


def invalidate(project, page_ids):
    for page_id in page_ids:
        if page_id in project["pages"]:
            project["pages"][page_id]["needsRender"] = True
    project["approvals"].pop("issue", None)
    front_id = project["plan"]["pages"][0]["id"]
    if front_id in page_ids:
        project["approvals"].pop("front", None)


def set_plan(root, plan):
    project = load(root)
    pages = plan.get("pages", [])
    if not 1 <= len(pages) <= 64:
        raise ValueError("Plan needs 1-64 pages")
    ids = [stable_id(page["id"]) for page in pages]
    if len(set(ids)) != len(ids):
        raise ValueError("Page IDs must be unique")
    old = project["plan"]
    old_pages = {page["id"]: page for page in old["pages"]}
    shared_old = visual_fields({k: v for k, v in old.items() if k != "pages"})
    shared_new = visual_fields({k: v for k, v in plan.items() if k != "pages"})
    changed = ids if shared_old != shared_new else [page["id"] for page in pages
        if visual_fields(page) != visual_fields(old_pages.get(page["id"], {}))]
    order_changed = [page["id"] for page in old["pages"]] != ids
    project["plan"] = plan
    project["title"] = plan.get("title", project["title"])
    if changed or order_changed:
        project["approvals"].pop("plan", None)
        invalidate(project, changed or ids)
    save(root, project)
    return {"invalidatedPages": changed, "planApprovalRequired": "plan" not in project["approvals"]}


def ready_page(root, project, page_id):
    page = project["pages"].get(page_id, {})
    if not page.get("assetId") or page.get("needsRender"):
        raise ValueError("Page is not ready: " + page_id)
    check_asset(root, project["assets"][page["assetId"]])
    return page


def approve(root, stage, by, note):
    project = load(root)
    if not note.strip():
        raise ValueError("Approval needs a note identifying the actual decision")
    if by == "delegated" and not project.get("delegatedApproval"):
        raise ValueError("Delegated approval requires explicit authorization recorded at init")
    if stage in ("front", "issue"):
        if "plan" not in project["approvals"]:
            raise ValueError("Plan approval is required")
        ready_page(root, project, project["plan"]["pages"][0]["id"])
    if stage == "issue":
        if "front" not in project["approvals"]:
            raise ValueError("Front-page approval is required")
        for page in project["plan"]["pages"]:
            ready_page(root, project, page["id"])
    record = {"stage": stage, "by": by, "note": note, "at": now()}
    project["approvals"][stage] = record
    project["approvalHistory"].append(record)
    save(root, project)
    return record


def task_spec(root, project, spec):
    if spec.get("stage") not in ("extraction", "variant", "page"):
        raise ValueError("Stage must be extraction, variant or page")
    if not spec.get("model") or not spec.get("promptVersion") or not spec.get("instruction"):
        raise ValueError("Task requires model, promptVersion and instruction")
    effective = visual_fields(spec)
    inputs = spec.get("inputs", [])
    if not isinstance(inputs, list) or not all(isinstance(item, str) for item in inputs):
        raise ValueError("inputs must be a list of registered asset IDs")
    effective["inputHashes"] = []
    for asset_id in inputs:
        asset = project["assets"][asset_id]
        check_asset(root, asset)
        effective["inputHashes"].append({"id": asset_id, "sha256": asset["sha256"], "role": asset["role"]})
    if spec["stage"] == "page":
        if "plan" not in project["approvals"]:
            raise ValueError("Approve the plan before page generation")
        page_id = spec.get("pageId")
        page_plan = next((p for p in project["plan"]["pages"] if p["id"] == page_id), None)
        if page_plan is None:
            raise ValueError("Unknown pageId")
        effective["pagePlan"] = visual_fields(page_plan)
        effective["issuePlan"] = visual_fields({k: v for k, v in project["plan"].items() if k != "pages"})
        effective["paper"] = project["paper"]
        if page_id != project["plan"]["pages"][0]["id"]:
            if "front" not in project["approvals"]:
                raise ValueError("Approve the actual front page before inner pages")
            front = ready_page(root, project, project["plan"]["pages"][0]["id"])
            effective["approvedFrontHash"] = project["assets"][front["assetId"]]["sha256"]
    return effective


def begin(root, spec, new_intent=False, retry_manual=False):
    project = load(root)
    effective = task_spec(root, project, spec)
    base_key = digest(canonical({k: v for k, v in effective.items() if k != "generationKey"}))[:32]
    active_intents = project.setdefault("activeIntents", {})
    if new_intent:
        if spec.get("stage") != "page":
            raise ValueError("New intent is for explicit whole-page regeneration")
        spec = {**spec, "generationKey": uuid.uuid4().hex}
        effective = task_spec(root, project, spec)
    elif spec["stage"] == "page" and "generationKey" not in spec and base_key in active_intents:
        # The original page spec resumes its latest explicit intent, not an old
        # successful base page. Persisted mapping survives process restarts.
        previous = project["tasks"].get(active_intents[base_key])
        if previous:
            spec = previous["spec"]
            effective = task_spec(root, project, spec)
    task_id = digest(canonical(effective))[:32]
    if spec["stage"] == "page":
        active_intents[base_key] = task_id
    task = project["tasks"].get(task_id)
    if task and task["status"] == "completed":
        try:
            check_asset(root, project["assets"][task["assetId"]])
        except (ValueError, KeyError) as error:
            return {"action": "blocked", "taskId": task_id, "reason": str(error), "requiresManualRecovery": True}
        task["cacheHits"] += 1
        if task["spec"]["stage"] == "page":
            apply_page(project, task)
        save(root, project)
        return {"action": "cached", "taskId": task_id, "asset": project["assets"][task["assetId"]]}
    if task and task["status"] in ("started", "failed"):
        failure = task.get("failure", {})
        automatic = (task["status"] == "failed" and failure.get("state") == "not-started"
                     and failure.get("transient") is True and len(task["attempts"]) == 1
                     and not re.search(r"timeout|timed out|abort|超时", failure.get("message", ""), re.I))
        if not automatic and not retry_manual:
            return {"action": "blocked", "taskId": task_id,
                    "reason": "Outcome is unknown or automatic retry is exhausted. Recover output first; manual retry must be explicit."}
        if task["status"] == "started" and retry_manual:
            task["attempts"][-1]["status"] = "unknown"
    else:
        task = {"id": task_id, "spec": spec, "effective": effective, "status": "started", "attempts": [], "cacheHits": 0}
        project["tasks"][task_id] = task
    task["status"] = "started"
    task.pop("failure", None)
    task["attempts"].append({"number": len(task["attempts"]) + 1, "startedAt": now(), "status": "started",
        "durationMs": None, "tokens": None, "providerRequests": None, "retryMode": "manual" if retry_manual else "automatic" if len(task["attempts"]) else None})
    if spec["stage"] == "page":
        invalidate(project, [spec["pageId"]])
    save(root, project)
    return {"action": "run", "taskId": task_id, "attempt": len(task["attempts"]), "spec": task["spec"]}


def apply_page(project, task):
    page_id = task["spec"]["pageId"]
    page = project["pages"].setdefault(page_id, {"history": []})
    if page.get("assetId") == task["assetId"] and not page.get("needsRender"):
        return
    if page.get("assetId"):
        page["history"].append({"assetId": page["assetId"], "taskId": page.get("taskId"), "savedAt": now()})
    page.update({"assetId": task["assetId"], "taskId": task["id"], "needsRender": False})
    invalidate(project, [page_id])
    page["needsRender"] = False
    # A local front-page edit does not imply a new issue-wide visual direction.
    # Shared style changes invalidate all pages through set_plan; otherwise the
    # existing inner pages are assessed at issue review without forced generation.


def complete(root, task_id, file, duration_ms=None, tokens=None, provider_requests=None):
    project = load(root)
    task = project["tasks"][task_id]
    if task["status"] not in ("started", "failed"):
        raise ValueError("Task already completed; use its existing output")
    for value in (duration_ms, tokens, provider_requests):
        if value is not None and value < 0:
            raise ValueError("Measurements must be non-negative or omitted")
    stage = task["spec"]["stage"]
    asset_id = "result-" + task_id
    asset = copy_asset(root, project, asset_id, file, "page" if stage == "page" else "derived", "generated")
    task["status"] = "completed"
    task["assetId"] = asset_id
    task.pop("failure", None)
    task["attempts"][-1].update({"status": "completed", "finishedAt": now(), "durationMs": duration_ms,
                               "tokens": tokens, "providerRequests": provider_requests})
    applied = False
    if stage == "page":
        try:
            current = task_spec(root, project, task["spec"])
        except (ValueError, KeyError):
            current = None
        base_key = digest(canonical({k: v for k, v in task["effective"].items() if k != "generationKey"}))[:32]
        current_intent = project.get("activeIntents", {}).get(base_key)
        if current == task["effective"] and current_intent in (None, task_id):
            apply_page(project, task)
            applied = True
    save(root, project)
    return {"taskId": task_id, "asset": asset, "status": "completed", "appliedToPage": applied}


def restore_page(root, page_id, task_id):
    project = load(root)
    if page_id not in [item["id"] for item in project["plan"]["pages"]]:
        raise ValueError("Unknown page ID")
    task = project["tasks"][task_id]
    if task["status"] != "completed" or task["spec"].get("pageId") != page_id:
        raise ValueError("Choose a completed task belonging to this page")
    check_asset(root, project["assets"][task["assetId"]])
    base_key = digest(canonical({k: v for k, v in task["effective"].items() if k != "generationKey"}))[:32]
    project.setdefault("activeIntents", {})[base_key] = task_id
    apply_page(project, task)
    save(root, project)
    return {"pageId": page_id, "taskId": task_id, "approvalRequired": True}


def fail(root, task_id, state, transient, message):
    project = load(root)
    task = project["tasks"][task_id]
    if task["status"] != "started":
        raise ValueError("Only a started task can fail")
    task["status"] = "failed"
    task["failure"] = {"state": state, "transient": transient, "message": message}
    task["attempts"][-1].update({"status": "failed", "finishedAt": now()})
    save(root, project)
    return {"taskId": task_id, "status": "failed"}


def status(root):
    project = load(root)
    attempts = [attempt for task in project["tasks"].values() for attempt in task["attempts"]]
    measured = [item["tokens"] for item in attempts if item["tokens"] is not None]
    durations = [item["durationMs"] for item in attempts if item["durationMs"] is not None]
    return {"title": project["title"], "paper": project["paper"], "approvals": project["approvals"],
        "plannedPages": len(project["plan"]["pages"]), "completedPages": sum(bool(project["pages"].get(p["id"], {}).get("assetId"))
        and not project["pages"].get(p["id"], {}).get("needsRender") for p in project["plan"]["pages"]),
        "taskAttempts": len(attempts), "cacheHits": sum(task["cacheHits"] for task in project["tasks"].values()),
        "recordedTokens": sum(measured) if measured else None, "tokenMeasuredAttempts": len(measured),
        "recordedDurationMs": sum(durations) if durations else None,
        "scope": "Recorded task attempts, not all provider subrequests; durations may overlap; tokens are not a bill",
        "tasks": [{"id": task["id"], "stage": task["spec"]["stage"], "status": task["status"]} for task in project["tasks"].values()]}


def export_pdf(root, output):
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader
    project = load(root)
    if "issue" not in project["approvals"]:
        raise ValueError("Approve the completed issue before final export")
    width, height = (project["paper"][key] / 25.4 * 72 for key in ("widthMm", "heightMm"))
    output = Path(output)
    if output.exists():
        raise ValueError("Output already exists; use a new filename to preserve the previous export")
    output.parent.mkdir(parents=True, exist_ok=True)
    document = canvas.Canvas(str(output), pagesize=(width, height), pageCompression=1)
    document.setTitle(project["title"])
    measurements = []
    for item in project["plan"]["pages"]:
        page = ready_page(root, project, item["id"])
        asset = project["assets"][page["assetId"]]
        file = check_asset(root, asset)
        pixels = image_info(file)
        scale = min(width / pixels["width"], height / pixels["height"])
        drawn_width, drawn_height = pixels["width"] * scale, pixels["height"] * scale
        document.drawImage(ImageReader(str(file)), (width - drawn_width) / 2, (height - drawn_height) / 2,
                           width=drawn_width, height=drawn_height, mask="auto")
        document.showPage()
        measurements.append({"pageId": item["id"], "nativePixels": pixels,
                             "effectiveDpi": round(72 / scale, 2)})
    document.save()
    return {"pdf": str(output), "pages": measurements, "containsProject": False,
            "printSides": project["paper"]["sides"], "note": "Pages are in reading order. Select duplex/flip edge in the printer; no imposition or raster upsampling is applied."}


def archive(root, output):
    project = load(root)
    output = Path(output)
    if output.exists():
        raise ValueError("Archive already exists; choose a new filename")
    if not str(output).endswith(".newspaper.zip"):
        raise ValueError("Use the .newspaper.zip suffix (not the website .shiguang.json format)")
    files = {asset["path"]: check_asset(root, asset) for asset in project["assets"].values()}
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as package:
        package.writestr("project.json", json.dumps(project, ensure_ascii=False, indent=2))
        for relative, file in files.items():
            package.write(file, relative)
    return {"archive": str(output), "uniqueAssetFiles": len(files), "format": "newspaper-project-v1"}


def restore(archive_file, root):
    root = Path(root)
    if root.exists() and any(root.iterdir()):
        raise ValueError("Restore destination must be empty or new")
    with zipfile.ZipFile(archive_file) as package:
        entries = package.infolist()
        if len(entries) > 10000 or sum(item.file_size for item in entries) > 2 * 1024 ** 3:
            raise ValueError("Archive exceeds the 2 GiB / 10,000 file restore limit")
        names = set()
        for item in entries:
            safe_path(root, item.filename)
            normalized = item.filename.casefold()
            if normalized in names or item.is_dir() or stat.S_ISLNK(item.external_attr >> 16):
                raise ValueError("Duplicate, directory or symbolic-link ZIP entry")
            if item.filename != "project.json" and not re.fullmatch(r"assets/[0-9a-f]{64}\.(png|jpg|jpeg|webp|tif|tiff)", item.filename):
                raise ValueError("Unexpected archive entry: " + item.filename)
            if item.file_size > 512 * 1024 ** 2:
                raise ValueError("Single archive entry exceeds 512 MiB")
            names.add(normalized)
        project = json.loads(package.read("project.json").decode("utf-8"))
        if project.get("schemaVersion") != 1:
            raise ValueError("Unsupported newspaper archive schema")
        expected = {"project.json"} | {a["path"] for a in project["assets"].values()}
        if expected != {item.filename for item in entries}:
            raise ValueError("Archive contents do not match the asset manifest")
        for asset in project["assets"].values():
            if digest(package.read(asset["path"])) != asset["sha256"]:
                raise ValueError("Archive asset hash mismatch")
        root.mkdir(parents=True, exist_ok=True)
        for item in entries:
            target = safe_path(root, item.filename)
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("xb") as file:
                file.write(package.read(item.filename))
    return {"project": str(root / "project.json"), "assets": len(project["assets"])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("init", "register", "plan", "approve", "begin", "complete", "fail", "status", "export", "archive", "restore", "restore-page"):
        sub = commands.add_parser(name)
        sub.add_argument("--project", required=True)
        if name == "init":
            sub.add_argument("--title", required=True)
            sub.add_argument("--paper", choices=[*PAPERS, "custom"], default="A4")
            sub.add_argument("--orientation", choices=["portrait", "landscape"], default="portrait")
            sub.add_argument("--sides", choices=["single", "double"], default="single")
            sub.add_argument("--pages", type=int, default=2)
            sub.add_argument("--width-mm", type=float)
            sub.add_argument("--height-mm", type=float)
            sub.add_argument("--delegated-approval")
        if name == "register":
            sub.add_argument("--id", required=True)
            sub.add_argument("--file", required=True)
            sub.add_argument("--role", choices=["content", "reference"], required=True)
            sub.add_argument("--origin", choices=["synthetic", "user", "web"], required=True)
            sub.add_argument("--label", default="")
        if name == "plan":
            sub.add_argument("--file", required=True)
        if name == "approve":
            sub.add_argument("--stage", choices=["plan", "front", "issue"], required=True)
            sub.add_argument("--by", choices=["user", "delegated"], required=True)
            sub.add_argument("--note", required=True)
        if name == "begin":
            sub.add_argument("--spec", required=True)
            sub.add_argument("--new-intent", action="store_true")
            sub.add_argument("--retry-manual", action="store_true")
        if name in ("complete", "fail", "restore-page"):
            sub.add_argument("--task", required=True)
        if name == "restore-page":
            sub.add_argument("--page", required=True)
        if name == "complete":
            sub.add_argument("--file", required=True)
            sub.add_argument("--duration-ms", type=int)
            sub.add_argument("--tokens", type=int)
            sub.add_argument("--provider-requests", type=int)
        if name == "fail":
            sub.add_argument("--state", choices=["not-started", "unknown"], required=True)
            sub.add_argument("--transient", action="store_true")
            sub.add_argument("--message", required=True)
        if name in ("export", "archive"):
            sub.add_argument("--output", required=True)
        if name == "restore":
            sub.add_argument("--archive", required=True)
    args = parser.parse_args()
    root = Path(args.project)
    if args.command == "restore":
        result = restore(args.archive, root)
    else:
        with locked(root):
            command = args.command
            if command == "init":
                result = init(root, args.title, args.paper, args.orientation, args.sides, args.pages,
                              args.width_mm, args.height_mm, args.delegated_approval)
            elif command == "register":
                project = load(root)
                result = copy_asset(root, project, args.id, args.file, args.role, args.origin, args.label)
                save(root, project)
            elif command == "plan":
                result = set_plan(root, read_json(args.file))
            elif command == "approve":
                result = approve(root, args.stage, args.by, args.note)
            elif command == "begin":
                result = begin(root, read_json(args.spec), args.new_intent, args.retry_manual)
            elif command == "complete":
                result = complete(root, args.task, args.file, args.duration_ms, args.tokens, args.provider_requests)
            elif command == "fail":
                result = fail(root, args.task, args.state, args.transient, args.message)
            elif command == "restore-page":
                result = restore_page(root, args.page, args.task)
            elif command == "status":
                result = status(root)
            elif command == "export":
                result = export_pdf(root, args.output)
            elif command == "archive":
                result = archive(root, args.output)
    print(json.dumps(result, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError, ImportError, zipfile.BadZipFile) as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=True), file=sys.stderr)
        sys.exit(1)
