from __future__ import annotations

from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from copy import deepcopy
from dataclasses import asdict
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import shutil
import sys
import threading
import uuid
from urllib import error, request
from zipfile import ZipFile

import fitz
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from latex_convert.candidate_pipeline import (  # noqa: E402
    Candidate,
    _ssl_context,
    apply_docx_decisions,
    normalize_action,
    scan_docx_candidates,
)
from latex_convert.document_converter import convert_docx_to_pdf, ensure_docx  # noqa: E402
from latex_convert.preview import formula_to_latex  # noqa: E402


STORAGE = Path(os.environ.get("LATEX_WEB_STORAGE", ROOT / "storage")).resolve()
INDEX_PATH = STORAGE / "app.json"
ALLOWED_EXTENSIONS = {".doc", ".docx", ".wps"}
STATE_LOCK = threading.Lock()

app = FastAPI(title="Word LaTeX Formula Web API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class FolderCreate(BaseModel):
    name: str
    parent_id: str | None = None


class TaskCreate(BaseModel):
    name: str
    folder_id: str | None = None


class ScanOptions(BaseModel):
    engine: str = "auto"
    mode: str = "balanced"
    skip_bibliography: bool = True


class AiOptions(BaseModel):
    api_key: str | None = None
    base_url: str | None = None
    model: str | None = None
    timeout_seconds: int = 60
    retries: int = 1
    batch_size: int = 10
    max_workers: int = 5
    failure_fallback: str = "rule"


class AiConfig(BaseModel):
    api_key: str = ""
    base_url: str = "https://api.openai.com/v1"
    model: str = "gpt-4.1-mini"
    batch_size: int = 10
    max_workers: int = 5
    failure_fallback: str = "rule"


class ApplyRequest(BaseModel):
    selections: dict[str, str] = Field(default_factory=dict)
    label: str = "Web conversion"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def load_index() -> dict:
    STORAGE.mkdir(parents=True, exist_ok=True)
    if INDEX_PATH.exists():
        return json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    data = {"folders": [], "tasks": [], "versions": []}
    save_index(data)
    return data


def save_index(data: dict) -> None:
    STORAGE.mkdir(parents=True, exist_ok=True)
    tmp = INDEX_PATH.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(INDEX_PATH)


def task_dir(task_id: str) -> Path:
    return STORAGE / "tasks" / task_id


def task_paths(task_id: str) -> dict[str, Path]:
    base = task_dir(task_id)
    return {
        "base": base,
        "uploads": base / "uploads",
        "work": base / "work",
        "preview": base / "preview",
        "outputs": base / "outputs",
        "state": base / "state.json",
        "candidates": base / "candidates.json",
        "decisions": base / "decisions.json",
        "ai": base / "ai_decisions.json",
    }


def read_state(task_id: str) -> dict:
    path = task_paths(task_id)["state"]
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def write_state(task_id: str, state: dict) -> None:
    paths = task_paths(task_id)
    paths["base"].mkdir(parents=True, exist_ok=True)
    paths["state"].write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def mutate_state(task_id: str, mutator) -> dict:
    with STATE_LOCK:
        state = read_state(task_id)
        mutator(state)
        write_state(task_id, state)
        return state


def get_task_or_404(data: dict, task_id: str) -> dict:
    for task in data["tasks"]:
        if task["id"] == task_id and not task.get("is_deleted"):
            return task
    raise HTTPException(404, "Task not found")


def get_folder_or_404(data: dict, folder_id: str) -> dict:
    for folder in data["folders"]:
        if folder["id"] == folder_id and not folder.get("is_deleted"):
            return folder
    raise HTTPException(404, "Folder not found")


def create_quick_task(data: dict) -> dict:
    task = {
        "id": new_id("task"),
        "folder_id": None,
        "name": "快速公式转换",
        "status": "empty",
        "created_at": utc_now(),
        "updated_at": utc_now(),
        "is_deleted": False,
        "session_kind": "quick",
    }
    data["tasks"].append(task)
    write_state(task["id"], {"task_id": task["id"], "candidates": [], "selections": {}, "logs": []})
    return task


def latest_active_task(data: dict) -> dict | None:
    tasks = [task for task in data["tasks"] if not task.get("is_deleted")]
    if not tasks:
        return None
    return sorted(tasks, key=lambda item: item.get("updated_at") or item.get("created_at") or "", reverse=True)[0]


def session_payload(task: dict, data: dict | None = None) -> dict:
    data = data or load_index()
    state = read_state(task["id"])
    versions = [version for version in data["versions"] if version["task_id"] == task["id"]]
    return {"task": task, "state": state, "versions": versions}


@app.get("/api/health")
def health() -> dict:
    return {"ok": True, "storage": str(STORAGE)}


@app.get("/api/ai-config")
def get_ai_config() -> dict:
    return read_ai_config()


@app.post("/api/ai-config")
def save_ai_config(payload: AiConfig) -> dict:
    write_ai_config(payload)
    _load_dotenv(overwrite=True)
    return {"ok": True, "config": read_ai_config()}


@app.post("/api/ai-config/test")
def test_ai_config(payload: AiConfig) -> dict:
    try:
        reply = call_ai_handshake(payload.api_key, payload.base_url, payload.model)
        return {"ok": True, "reply": reply}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


@app.get("/api/session")
def get_session() -> dict:
    data = load_index()
    task = latest_active_task(data)
    if task is None:
        task = create_quick_task(data)
        save_index(data)
    return session_payload(task, data)


@app.post("/api/session/reset")
def reset_session() -> dict:
    tasks_dir = STORAGE / "tasks"
    if tasks_dir.exists():
        shutil.rmtree(tasks_dir)
    data = {"folders": [], "tasks": [], "versions": []}
    task = create_quick_task(data)
    save_index(data)
    return session_payload(task, data)


@app.get("/api/folders")
def list_folders() -> list[dict]:
    data = load_index()
    return [folder for folder in data["folders"] if not folder.get("is_deleted")]


@app.post("/api/folders")
def create_folder(payload: FolderCreate) -> dict:
    data = load_index()
    if payload.parent_id:
        get_folder_or_404(data, payload.parent_id)
    folder = {
        "id": new_id("folder"),
        "name": payload.name.strip() or "未命名目录",
        "parent_id": payload.parent_id,
        "created_at": utc_now(),
        "updated_at": utc_now(),
        "is_deleted": False,
    }
    data["folders"].append(folder)
    save_index(data)
    return folder


@app.delete("/api/folders/{folder_id}")
def delete_folder(folder_id: str) -> dict:
    data = load_index()
    folder = get_folder_or_404(data, folder_id)
    folder["is_deleted"] = True
    folder["updated_at"] = utc_now()
    save_index(data)
    return {"ok": True}


@app.get("/api/tasks")
def list_tasks(folder_id: str | None = None) -> list[dict]:
    data = load_index()
    tasks = [task for task in data["tasks"] if not task.get("is_deleted")]
    if folder_id:
        tasks = [task for task in tasks if task.get("folder_id") == folder_id]
    return tasks


@app.post("/api/tasks")
def create_task(payload: TaskCreate) -> dict:
    data = load_index()
    if payload.folder_id:
        get_folder_or_404(data, payload.folder_id)
    task = {
        "id": new_id("task"),
        "folder_id": payload.folder_id,
        "name": payload.name.strip() or "未命名任务",
        "status": "empty",
        "created_at": utc_now(),
        "updated_at": utc_now(),
        "is_deleted": False,
    }
    data["tasks"].append(task)
    save_index(data)
    write_state(task["id"], {"task_id": task["id"], "candidates": [], "selections": {}, "logs": []})
    return task


@app.get("/api/tasks/{task_id}")
def get_task(task_id: str) -> dict:
    data = load_index()
    task = get_task_or_404(data, task_id)
    state = read_state(task_id)
    versions = [version for version in data["versions"] if version["task_id"] == task_id]
    return {"task": task, "state": state, "versions": versions}


@app.post("/api/tasks/{task_id}/upload")
async def upload_and_scan(
    task_id: str,
    file: UploadFile = File(...),
    engine: str = "auto",
    mode: str = "balanced",
    skip_bibliography: bool = True,
) -> dict:
    data = load_index()
    task = get_task_or_404(data, task_id)
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, f"Unsupported file extension: {suffix}")
    paths = task_paths(task_id)
    for key in ["uploads", "work", "preview", "outputs"]:
        paths[key].mkdir(parents=True, exist_ok=True)
    source_path = paths["uploads"] / _safe_filename(file.filename or f"upload{suffix}")
    with source_path.open("wb") as out:
        shutil.copyfileobj(file.file, out)

    try:
        prepared_docx, engine_used = ensure_docx(source_path, paths["work"], engine)
        scan = scan_docx_candidates(
            prepared_docx,
            input_path=source_path,
            engine=engine_used,
            mode=mode,
            skip_bibliography=skip_bibliography,
        )
        pdf_path, preview_engine = render_docx_to_pdf(prepared_docx, paths["preview"], engine)
        page_texts = extract_pdf_page_texts(pdf_path)
        page_count = render_pdf_pages(pdf_path, paths["preview"])
        candidates = enrich_candidates(scan.candidates, page_texts)
        selections = {candidate["id"]: candidate["default_action"] for candidate in candidates}
        state = {
            "task_id": task_id,
            "source_name": file.filename,
            "source_path": str(source_path),
            "prepared_docx": str(prepared_docx),
            "engine": engine_used,
            "mode": mode,
            "skip_bibliography": skip_bibliography,
            "preview_pdf": str(pdf_path),
            "preview_engine": preview_engine,
            "page_count": page_count,
            "summary": scan.to_dict()["summary"],
            "candidates": candidates,
            "selections": selections,
            "ai_ready": False,
            "logs": [f"Scanned {len(candidates)} candidates with engine={engine_used}, preview={preview_engine}"],
        }
        write_state(task_id, state)
        paths["candidates"].write_text(json.dumps(scan.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
        task["status"] = "scanned"
        task["source_name"] = file.filename
        task["updated_at"] = utc_now()
        save_index(data)
        return task_payload(task, state)
    except Exception as exc:
        task["status"] = "failed"
        task["updated_at"] = utc_now()
        save_index(data)
        raise HTTPException(500, str(exc)) from exc


@app.post("/api/tasks/{task_id}/scan")
def rescan_task(task_id: str, options: ScanOptions) -> dict:
    state = read_state(task_id)
    source_path = Path(state.get("source_path", ""))
    if not source_path.exists():
        raise HTTPException(400, "No uploaded document for this task")
    # Reuse the upload pipeline with a small internal shim would require rebuilding
    # UploadFile; this explicit path keeps the Web endpoint clear.
    paths = task_paths(task_id)
    prepared_docx, engine_used = ensure_docx(source_path, paths["work"], options.engine)
    scan = scan_docx_candidates(
        prepared_docx,
        input_path=source_path,
        engine=engine_used,
        mode=options.mode,
        skip_bibliography=options.skip_bibliography,
    )
    pdf_path, preview_engine = render_docx_to_pdf(prepared_docx, paths["preview"], options.engine)
    page_count = render_pdf_pages(pdf_path, paths["preview"])
    candidates = enrich_candidates(scan.candidates, extract_pdf_page_texts(pdf_path))
    state.update(
        {
            "prepared_docx": str(prepared_docx),
            "engine": engine_used,
            "mode": options.mode,
            "skip_bibliography": options.skip_bibliography,
            "preview_pdf": str(pdf_path),
            "preview_engine": preview_engine,
            "page_count": page_count,
            "summary": scan.to_dict()["summary"],
            "candidates": candidates,
            "selections": {candidate["id"]: candidate["default_action"] for candidate in candidates},
            "ai_ready": False,
        }
    )
    write_state(task_id, state)
    paths["candidates"].write_text(json.dumps(scan.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    return {"state": state}


@app.post("/api/tasks/{task_id}/ai-review")
def ai_review(task_id: str, options: AiOptions) -> dict:
    state = read_state(task_id)
    candidates = state.get("candidates", [])
    if not candidates:
        raise HTTPException(400, "No candidates to review")
    api_key = options.api_key or env_first("OPENAI_API_KEY", "API_KEY")
    base_url = options.base_url or env_first("OPENAI_BASE_URL", "BASE_URL", default="https://api.openai.com/v1")
    model = options.model or env_first("OPENAI_MODEL", "MODEL", default="gpt-4.1-mini")
    if not api_key:
        raise HTTPException(400, "Missing API key")

    logs = state.setdefault("logs", [])
    ai_results = ai_review_candidates(candidates, api_key, base_url, model, options, logs)
    by_id = {item["id"]: item for item in ai_results}
    for candidate in candidates:
        result = by_id.get(candidate["id"])
        if not result:
            continue
        candidate["ai_action"] = normalize_action(result.get("action", "review"))
        candidate["ai_latex"] = result.get("latex") or candidate.get("local_latex") or candidate["text"]
        candidate["ai_reason"] = result.get("reason", "")
    state["ai_ready"] = True
    state["ai_model"] = model
    write_state(task_id, state)
    task_paths(task_id)["ai"].write_text(json.dumps(ai_results, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"state": state, "actions": dict(Counter(c.get("ai_action") for c in candidates))}


@app.post("/api/tasks/{task_id}/ai-review/start")
def start_ai_review(task_id: str, options: AiOptions) -> dict:
    state = read_state(task_id)
    candidates = state.get("candidates", [])
    if not candidates:
        raise HTTPException(400, "No candidates to review")
    api_key = options.api_key or env_first("OPENAI_API_KEY", "API_KEY")
    base_url = options.base_url or env_first("OPENAI_BASE_URL", "BASE_URL", default="https://api.openai.com/v1")
    model = options.model or env_first("OPENAI_MODEL", "MODEL", default="gpt-4.1-mini")
    if not api_key:
        raise HTTPException(400, "Missing API key")

    job_id = new_id("aijob")

    def reset_ai(next_state: dict) -> None:
        for candidate in next_state.get("candidates", []):
            candidate["ai_latex"] = None
            candidate["ai_action"] = None
            candidate["ai_reason"] = ""
            candidate["ai_status"] = "待转换"
        next_state["ai_ready"] = False
        next_state["ai_running"] = True
        next_state["ai_model"] = model
        next_state["ai_job_id"] = job_id
        next_state["ai_cancel_requested"] = False
        next_state["ai_failure_fallback"] = options.failure_fallback
        next_state["ai_summary"] = {"done": 0, "total": len(candidates), "failed": 0}
        next_state.setdefault("logs", []).append(f"AI review started {job_id}")

    state = mutate_state(task_id, reset_ai)
    thread = threading.Thread(
        target=run_ai_review_job,
        args=(task_id, api_key, base_url, model, options, job_id),
        daemon=True,
    )
    thread.start()
    return {"state": state, "job_id": job_id}


@app.get("/api/tasks/{task_id}/ai-review/status")
def ai_review_status(task_id: str) -> dict:
    state = read_state(task_id)
    candidates = state.get("candidates", [])
    return {
        "state": state,
        "running": bool(state.get("ai_running")),
        "actions": dict(Counter(c.get("ai_action") for c in candidates if c.get("ai_action"))),
        "summary": state.get("ai_summary", {}),
    }


@app.post("/api/tasks/{task_id}/ai-review/stop")
def stop_ai_review(task_id: str) -> dict:
    state = read_state(task_id)
    if not state:
        raise HTTPException(404, "Task state not found")
    strategy = state.get("ai_failure_fallback", "rule")

    def stop(next_state: dict) -> None:
        next_state["ai_cancel_requested"] = True
        next_state["ai_running"] = False
        next_state["ai_ready"] = True
        _fallback_unfinished_ai(next_state, strategy, "user-stopped")
        next_state.setdefault("logs", []).append("AI review stopped by user")

    state = mutate_state(task_id, stop)
    candidates = state.get("candidates", [])
    return {
        "state": state,
        "running": False,
        "actions": dict(Counter(c.get("ai_action") for c in candidates if c.get("ai_action"))),
        "summary": state.get("ai_summary", {}),
    }


@app.post("/api/tasks/{task_id}/selections")
def update_selections(task_id: str, selections: dict[str, str]) -> dict:
    state = read_state(task_id)
    normalized = {
        candidate_id: _selection_to_action(value)
        for candidate_id, value in selections.items()
    }
    state["selections"] = {**state.get("selections", {}), **normalized}
    write_state(task_id, state)
    return {"selections": state["selections"]}


@app.post("/api/tasks/{task_id}/apply")
def apply_task(task_id: str, payload: ApplyRequest) -> dict:
    data = load_index()
    task = get_task_or_404(data, task_id)
    state = read_state(task_id)
    prepared_docx = Path(state.get("prepared_docx", ""))
    if not prepared_docx.exists():
        raise HTTPException(400, "No prepared DOCX found")
    candidates = state.get("candidates", [])
    selections = {**state.get("selections", {}), **payload.selections}
    decisions = {
        candidate["id"]: _selection_to_action(selections.get(candidate["id"], candidate["default_action"]))
        for candidate in candidates
    }
    formula_overrides = {
        candidate["id"]: candidate["ai_latex"]
        for candidate in candidates
        if selections.get(candidate["id"]) == "ai" and candidate.get("ai_latex")
    }
    version_id = new_id("version")
    paths = task_paths(task_id)
    paths["outputs"].mkdir(parents=True, exist_ok=True)
    output_path = paths["outputs"] / f"{version_id}.docx"
    report_path = paths["outputs"] / f"{version_id}_report.json"
    stats = apply_docx_decisions(
        prepared_docx,
        output_path,
        decisions,
        mode=state.get("mode", "balanced"),
        skip_bibliography=state.get("skip_bibliography", True),
        formula_text_overrides=formula_overrides,
    )
    report = {
        "task_id": task_id,
        "version_id": version_id,
        "output": str(output_path),
        "formulas_converted": stats.formulas_converted,
        "formulas_kept": stats.formulas_kept,
        "failed": stats.failed,
        "created_at": utc_now(),
    }
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    decisions_path = paths["outputs"] / f"{version_id}_decisions.json"
    decisions_path.write_text(json.dumps(decisions, ensure_ascii=False, indent=2), encoding="utf-8")
    version = {
        "id": version_id,
        "task_id": task_id,
        "label": payload.label,
        "created_at": utc_now(),
        "output_docx": str(output_path),
        "report": str(report_path),
        "decisions": str(decisions_path),
        "converted": stats.formulas_converted,
        "kept": stats.formulas_kept,
        "failed": len(stats.failed),
    }
    data["versions"].append(version)
    task["status"] = "converted"
    task["latest_version_id"] = version_id
    task["updated_at"] = utc_now()
    state["selections"] = decisions
    state["latest_version_id"] = version_id
    write_state(task_id, state)
    save_index(data)
    return {"version": version, "report": report}


@app.get("/api/tasks/{task_id}/preview/pages/{page_number}")
def preview_page(task_id: str, page_number: int) -> FileResponse:
    page_path = task_paths(task_id)["preview"] / f"page-{page_number:03d}.png"
    if not page_path.exists():
        raise HTTPException(404, "Preview page not found")
    return FileResponse(page_path)


@app.get("/api/tasks/{task_id}/preview.pdf")
def preview_pdf(task_id: str) -> FileResponse:
    state = read_state(task_id)
    path = Path(state.get("preview_pdf", ""))
    if not path.exists():
        raise HTTPException(404, "Preview PDF not found")
    return FileResponse(path, media_type="application/pdf")


@app.get("/api/versions/{version_id}/download")
def download_version(version_id: str) -> FileResponse:
    data = load_index()
    for version in data["versions"]:
        if version["id"] == version_id:
            path = Path(version["output_docx"])
            if not path.exists():
                raise HTTPException(404, "Output not found")
            return FileResponse(
                path,
                media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                filename=f"{version_id}.docx",
            )
    raise HTTPException(404, "Version not found")


def task_payload(task: dict, state: dict) -> dict:
    return {"task": task, "state": state}


def enrich_candidates(candidates: list[Candidate], page_texts: list[str]) -> list[dict]:
    pages = estimate_candidate_pages(candidates, page_texts)
    enriched = []
    for candidate, page in zip(candidates, pages, strict=False):
        item = asdict(candidate)
        latex = formula_to_latex(candidate.text)
        item.update(
            {
                "page_number": page,
                "local_latex": latex,
                "local_action": candidate.default_action,
                "ai_latex": None,
                "ai_action": None,
                "ai_reason": None,
            }
        )
        enriched.append(item)
    return enriched


def render_docx_to_pdf(docx_path: Path, out_dir: Path, engine: str = "auto") -> tuple[Path, str]:
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = out_dir / f"{docx_path.stem}.pdf"
    preview_engine = engine if engine in {"auto", "word", "libreoffice"} else "auto"
    return convert_docx_to_pdf(docx_path, pdf_path, engine=preview_engine)


def extract_pdf_page_texts(pdf_path: Path) -> list[str]:
    doc = fitz.open(pdf_path)
    return [page.get_text() for page in doc]


def render_pdf_pages(pdf_path: Path, out_dir: Path) -> int:
    doc = fitz.open(pdf_path)
    for old in out_dir.glob("page-*.png"):
        old.unlink()
    for index, page in enumerate(doc, 1):
        pix = page.get_pixmap(matrix=fitz.Matrix(1.45, 1.45), alpha=False)
        pix.save(out_dir / f"page-{index:03d}.png")
    return doc.page_count


def estimate_candidate_pages(candidates: list[Candidate], page_texts: list[str]) -> list[int]:
    normalized_pages = [_normalize_search_text(text) for text in page_texts]
    pages: list[int] = []
    last_page = 1
    for candidate in candidates:
        probes = _candidate_search_probes(candidate)
        best_page = last_page
        best_score = -1
        for page_index, page_text in enumerate(normalized_pages, 1):
            score = 0
            for probe in probes:
                if not probe:
                    continue
                if probe in page_text:
                    score += min(len(probe), 90)
                else:
                    score += _token_overlap_score(probe, page_text)
            if page_index < last_page:
                score -= 5
            if score > best_score:
                best_score = score
                best_page = page_index
        last_page = max(last_page, best_page)
        pages.append(best_page)
    return pages


def _candidate_search_probes(candidate: Candidate) -> list[str]:
    text = candidate.text
    context = candidate.context or candidate.paragraph_text or ""
    probes = [_normalize_search_text(text)]
    location = context.find(text)
    if location >= 0:
        probes.append(_normalize_search_text(context[max(0, location - 35) : location + len(text) + 35]))
    probes.append(_normalize_search_text(context[:150]))
    probes.append(_normalize_search_text(candidate.paragraph_text[:220]))
    return [probe for probe in probes if len(probe) >= 2]


def _normalize_search_text(text: str) -> str:
    return re.sub(r"\s+", "", text).replace("−", "-").replace("—", "-").replace("–", "-")


def _token_overlap_score(probe: str, page_text: str) -> int:
    tokens = re.findall(r"[\u4e00-\u9fff]{2,}|[A-Za-zΑ-Ωα-ωϑϖ℘ℓℛ𝓡]+|[0-9]+", probe)
    return sum(min(len(token), 12) for token in tokens if token and token in page_text)


def ai_review_candidates(
    candidates: list[dict],
    api_key: str,
    base_url: str,
    model: str,
    options: AiOptions,
    logs: list[str],
) -> list[dict]:
    chunks = [candidates[start : start + options.batch_size] for start in range(0, len(candidates), options.batch_size)]
    results: list[dict] = []
    workers = max(1, min(options.max_workers, len(chunks)))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {
            pool.submit(_ai_review_chunk, chunk, api_key, base_url, model, options): (index, chunk)
            for index, chunk in enumerate(chunks, 1)
        }
        for future in as_completed(futures):
            index, chunk = futures[future]
            try:
                results.extend(future.result())
                logs.append(f"AI reviewed batch {index}/{len(chunks)}")
            except Exception as exc:
                logs.append(f"AI batch {index} failed, fallback-{options.failure_fallback}: {exc}")
                for candidate in chunk:
                    action = _fallback_action(candidate, options.failure_fallback)
                    results.append(
                        {
                            "id": candidate["id"],
                            "action": action,
                            "latex": candidate.get("local_latex") or candidate["text"],
                            "reason": f"fallback-{options.failure_fallback}",
                        }
                    )
    return results


def run_ai_review_job(
    task_id: str,
    api_key: str,
    base_url: str,
    model: str,
    options: AiOptions,
    job_id: str,
) -> None:
    state = read_state(task_id)
    candidates = state.get("candidates", [])
    chunks = [candidates[start : start + options.batch_size] for start in range(0, len(candidates), options.batch_size)]
    if not chunks:
        mutate_state(task_id, lambda s: s.update({"ai_running": False, "ai_ready": True}))
        return

    def set_status(candidate_ids: set[str], status: str) -> None:
        def update(next_state: dict) -> None:
            if next_state.get("ai_job_id") != job_id or next_state.get("ai_cancel_requested"):
                return
            for candidate in next_state.get("candidates", []):
                if candidate["id"] in candidate_ids:
                    candidate["ai_status"] = status

        mutate_state(task_id, update)

    def finish_chunk(chunk: list[dict], results: list[dict], failed: bool) -> None:
        by_id = {item["id"]: item for item in results}

        def update(next_state: dict) -> None:
            if next_state.get("ai_job_id") != job_id or next_state.get("ai_cancel_requested"):
                return
            done = 0
            failures = 0
            for candidate in next_state.get("candidates", []):
                result = by_id.get(candidate["id"])
                if not result:
                    continue
                candidate["ai_action"] = normalize_action(result.get("action", "review"))
                candidate["ai_latex"] = result.get("latex") or candidate.get("local_latex") or candidate["text"]
                candidate["ai_reason"] = result.get("reason", "")
                candidate["ai_status"] = "请求失败回退结果" if failed else "AI转换结果"
            for candidate in next_state.get("candidates", []):
                status = candidate.get("ai_status")
                if status in {"AI转换结果", "请求失败回退结果"}:
                    done += 1
                if status == "请求失败回退结果":
                    failures += 1
            next_state["ai_summary"] = {"done": done, "total": len(next_state.get("candidates", [])), "failed": failures}
            next_state.setdefault("logs", []).append(f"AI batch finished failed={failed} size={len(chunk)}")

        mutate_state(task_id, update)

    def worker(chunk: list[dict]) -> tuple[list[dict], bool]:
        ids = {candidate["id"] for candidate in chunk}
        set_status(ids, "转换中")
        current_state = read_state(task_id)
        if current_state.get("ai_job_id") != job_id or current_state.get("ai_cancel_requested"):
            return _fallback_results(chunk, options.failure_fallback, "user-stopped"), True
        try:
            return _ai_review_chunk(chunk, api_key, base_url, model, options), False
        except Exception as exc:
            return _fallback_results(chunk, options.failure_fallback, f"fallback-{options.failure_fallback}: {exc}"), True

    workers = max(1, min(options.max_workers, len(chunks)))
    all_results: list[dict] = []
    try:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = {pool.submit(worker, chunk): chunk for chunk in chunks}
            for future in as_completed(futures):
                chunk = futures[future]
                results, failed = future.result()
                all_results.extend(results)
                finish_chunk(chunk, results, failed)
    finally:
        def complete(next_state: dict) -> None:
            if next_state.get("ai_job_id") != job_id or next_state.get("ai_cancel_requested"):
                return
            next_state["ai_running"] = False
            next_state["ai_ready"] = True
            _fallback_unfinished_ai(next_state, options.failure_fallback, "fallback-unfinished")
            next_state.setdefault("logs", []).append(f"AI review completed {job_id}")

        mutate_state(task_id, complete)
        task_paths(task_id)["ai"].write_text(json.dumps(all_results, ensure_ascii=False, indent=2), encoding="utf-8")


def _ai_review_chunk(
    chunk: list[dict],
    api_key: str,
    base_url: str,
    model: str,
    options: AiOptions,
) -> list[dict]:
    compact = [
        {
            "id": item["id"],
            "text": item["text"],
            "context": item.get("context", ""),
            "local_latex": item.get("local_latex", ""),
            "default_action": item.get("default_action", "review"),
        }
        for item in chunk
    ]
    prompt = (
        "Review candidate formula fragments extracted from an academic Word document. "
        "Return strict JSON only, with no Markdown and no commentary. "
        "The JSON must be an array, in the same order as the input, with exactly one object per input item. "
        "Each object must contain id, action, latex, reason. Preserve the input id exactly. "
        "action must be one of convert, keep, review. "
        "Use convert only for real mathematical or scientific formulas. "
        "Use keep for DOI, URL, references, ordinary prose, headings, code-like feature names, or isolated text that should stay unchanged. "
        "Use review when ambiguous. "
        "For convert, latex must be compact editable LaTeX without surrounding dollar signs. "
        "Separate Greek commands from following Latin letters: write \\beta E_t, not \\betaE_t; write \\mu E_t, not \\muE_t. "
        "For keep, latex must be an empty string.\n\n"
        + json.dumps(compact, ensure_ascii=False)
    )
    body = json.dumps(
        {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are a precise formula reviewer and LaTeX normalizer."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0,
        },
        ensure_ascii=False,
    ).encode("utf-8")
    req = request.Request(
        base_url.rstrip("/") + "/chat/completions",
        data=body,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    last_exc: Exception | None = None
    for attempt in range(max(0, options.retries) + 1):
        try:
            with request.urlopen(req, timeout=options.timeout_seconds, context=_ssl_context()) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
            content = payload["choices"][0]["message"]["content"]
            parsed = json.loads(_extract_json(content))
            if isinstance(parsed, dict):
                parsed = parsed.get("items") or parsed.get("results") or parsed.get("data") or []
            if not isinstance(parsed, list):
                raise json.JSONDecodeError("AI response was not a JSON array", content, 0)
            return [_normalize_ai_item(item) for item in parsed]
        except (error.HTTPError, error.URLError, TimeoutError, json.JSONDecodeError, KeyError) as exc:
            last_exc = exc
            if attempt >= options.retries:
                break
    assert last_exc is not None
    raise last_exc


def _normalize_ai_item(item: dict) -> dict:
    return {
        "id": str(item.get("id", "")),
        "action": normalize_action(str(item.get("action", "review"))),
        "latex": str(item.get("latex", "")),
        "reason": str(item.get("reason", "")),
    }


def _extract_json(content: str) -> str:
    content = content.strip()
    if content.startswith("```"):
        content = re.sub(r"^```(?:json)?\s*", "", content)
        content = re.sub(r"\s*```$", "", content)
    if not content.startswith("["):
        start = content.find("[")
        end = content.rfind("]")
        if start >= 0 and end > start:
            return content[start : end + 1]
    return content


def _fallback_results(chunk: list[dict], strategy: str, reason: str) -> list[dict]:
    results = []
    for candidate in chunk:
        action = _fallback_action(candidate, strategy)
        results.append(
            {
                "id": candidate["id"],
                "action": action,
                "latex": candidate.get("local_latex") or candidate["text"],
                "reason": reason,
            }
        )
    return results


def _fallback_unfinished_ai(state: dict, strategy: str, reason: str) -> None:
    for candidate in state.get("candidates", []):
        if candidate.get("ai_status") in {None, "待转换", "转换中"}:
            candidate["ai_status"] = "请求失败回退结果"
            candidate["ai_action"] = normalize_action(_fallback_action(candidate, strategy))
            candidate["ai_latex"] = candidate.get("local_latex") or candidate["text"]
            candidate["ai_reason"] = reason
    done = sum(
        1
        for candidate in state.get("candidates", [])
        if candidate.get("ai_status") in {"AI转换结果", "请求失败回退结果"}
    )
    failed = sum(1 for candidate in state.get("candidates", []) if candidate.get("ai_status") == "请求失败回退结果")
    state["ai_summary"] = {"done": done, "total": len(state.get("candidates", [])), "failed": failed}


def _fallback_action(candidate: dict, strategy: str) -> str:
    strategy = strategy.lower()
    if strategy == "rule":
        return normalize_action(candidate.get("default_action", "review"))
    if strategy in {"keep", "review"}:
        return strategy
    return "review"


def _selection_to_action(value: str) -> str:
    value = (value or "").lower()
    if value in {"source", "original", "keep", "原文"}:
        return "keep"
    if value in {"local", "algorithm", "script", "convert", "算法"}:
        return "convert"
    if value == "ai":
        return "convert"
    return normalize_action(value)


def read_ai_config() -> dict:
    _load_dotenv(overwrite=True)
    return {
        "api_key": os.environ.get("OPENAI_API_KEY") or os.environ.get("API_KEY") or "",
        "base_url": os.environ.get("OPENAI_BASE_URL") or os.environ.get("BASE_URL") or "https://api.openai.com/v1",
        "model": os.environ.get("OPENAI_MODEL") or os.environ.get("MODEL") or "gpt-4.1-mini",
        "batch_size": _env_int("AI_BATCH_SIZE", 10),
        "max_workers": _env_int("AI_MAX_WORKERS", 5),
        "failure_fallback": os.environ.get("AI_FAILURE_FALLBACK") or "rule",
    }


def write_ai_config(config: AiConfig) -> None:
    env_path = ROOT / ".env"
    existing: dict[str, str] = {}
    if env_path.exists():
        for raw_line in env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            existing[key.strip()] = value.strip().strip('"').strip("'")
    existing.update(
        {
            "API_KEY": config.api_key.strip(),
            "BASE_URL": config.base_url.strip() or "https://api.openai.com/v1",
            "MODEL": config.model.strip() or "gpt-4.1-mini",
            "OPENAI_API_KEY": config.api_key.strip(),
            "OPENAI_BASE_URL": config.base_url.strip() or "https://api.openai.com/v1",
            "OPENAI_MODEL": config.model.strip() or "gpt-4.1-mini",
            "AI_BATCH_SIZE": str(max(1, min(config.batch_size, 50))),
            "AI_MAX_WORKERS": str(max(1, min(config.max_workers, 10))),
            "AI_FAILURE_FALLBACK": config.failure_fallback.strip() or "rule",
        }
    )
    lines = [f"{key}={_quote_env_value(value)}" for key, value in existing.items()]
    env_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    for key, value in existing.items():
        os.environ[key] = value


def call_ai_handshake(api_key: str, base_url: str, model: str) -> str:
    if not api_key.strip():
        raise RuntimeError("Missing API key")
    if not base_url.strip():
        raise RuntimeError("Missing base URL")
    if not model.strip():
        raise RuntimeError("Missing model")
    body = json.dumps(
        {
            "model": model.strip(),
            "messages": [
                {"role": "system", "content": "You are a concise connectivity test responder."},
                {"role": "user", "content": "Reply with exactly: formula-converter-ok"},
            ],
            "temperature": 0,
            "max_tokens": 32,
        },
        ensure_ascii=False,
    ).encode("utf-8")
    req = request.Request(
        base_url.rstrip("/") + "/chat/completions",
        data=body,
        headers={"Authorization": f"Bearer {api_key.strip()}", "Content-Type": "application/json"},
        method="POST",
    )
    with request.urlopen(req, timeout=20, context=_ssl_context()) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    return str(payload["choices"][0]["message"]["content"]).strip()


def _quote_env_value(value: str) -> str:
    if re.search(r"\s|#|=|\"", value):
        return json.dumps(value, ensure_ascii=False)
    return value


def env_first(*names: str, default: str | None = None) -> str | None:
    _load_dotenv()
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    return default


def _env_int(name: str, default: int) -> int:
    try:
        return int(os.environ.get(name, default))
    except (TypeError, ValueError):
        return default


def _load_dotenv(*, overwrite: bool = False) -> None:
    for path in [ROOT / ".env", Path.cwd() / ".env"]:
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            if overwrite or key not in os.environ:
                os.environ[key] = value.strip().strip('"').strip("'")


def _safe_filename(name: str) -> str:
    cleaned = re.sub(r"[^\w.\-一-龥（）()]+", "_", name, flags=re.UNICODE).strip("._")
    return cleaned or f"upload_{uuid.uuid4().hex[:8]}"
