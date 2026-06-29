#!/usr/bin/env python3
"""Compile concise comic-page prompts and optionally run happy-img2-direct img2img."""
import argparse
import json
import os
import pathlib
import shlex
import subprocess
import sys
import time
from typing import Any, Dict, List

SKILL_DIR = pathlib.Path(__file__).resolve().parents[1]
WORKSPACE = SKILL_DIR.parents[1]
DIRECT_RUN = WORKSPACE / "skills/happy-img2-direct/scripts/run.py"
DEFAULT_OUTPUT_DIR = os.path.expanduser("~/.openclaw/generated-images/visual-prompt-compiler-img2")


def iso_now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S%z")


def slugify(text: str) -> str:
    import re
    text = re.sub(r"[^A-Za-z0-9._-]+", "-", text or "visual-prompt-compiler-img2").strip("-._")
    return text[:80] or "visual-prompt-compiler-img2"


def read_input(path: str) -> Dict[str, Any]:
    p = pathlib.Path(path)
    raw = p.read_text(encoding="utf-8")
    if p.suffix.lower() in {".yaml", ".yml"}:
        try:
            import yaml  # type: ignore
        except Exception as e:
            raise SystemExit(f"YAML input needs PyYAML installed, or use JSON. import error: {e}")
        data = yaml.safe_load(raw)
    else:
        data = json.loads(raw)
    if not isinstance(data, dict):
        raise SystemExit("input file must contain an object")
    data["_input_file"] = str(p)
    return data


def as_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(x).strip() for x in value if str(x).strip()]
    if isinstance(value, dict):
        return [f"{k}: {v}" for k, v in value.items()]
    return [x.strip() for x in str(value).split(",") if x.strip()]


def resolve_path(path: str) -> str:
    p = pathlib.Path(os.path.expanduser(path))
    if not p.is_absolute():
        p = WORKSPACE / p
    return str(p.resolve())


def choose_reference_images(data: Dict[str, Any], args: argparse.Namespace) -> List[str]:
    refs = []
    if args.reference_image:
        refs.extend(args.reference_image)
    else:
        refs.extend(as_list(data.get("reference_images")))
    if args.style_image:
        refs.append(args.style_image)

    # Validate forbidden images against the file name, not the full workspace path.
    # Example: a valid project directory may contain "openclaw", while a forbidden
    # input image like "P2" or "logo" should be rejected by basename/stem.
    forbidden_terms = [x.lower() for x in as_list(data.get("forbidden")) + as_list(args.forbidden)]
    forbidden_image_terms = [x for x in forbidden_terms if x]
    out = []
    seen = set()
    for ref in refs:
        full = resolve_path(ref)
        name_low = pathlib.Path(full).name.lower()
        stem_low = pathlib.Path(full).stem.lower()
        if any(term in name_low or term == stem_low for term in forbidden_image_terms):
            raise SystemExit(f"forbidden input image rejected: {ref}")
        if full not in seen:
            out.append(full)
            seen.add(full)
    if args.require_character_refs and not out:
        raise SystemExit("input_images must not be empty when --require-character-refs is set")
    if len(out) > args.max_input_images:
        raise SystemExit(f"too many input_images: {len(out)} > {args.max_input_images}")
    missing = [p for p in out if not pathlib.Path(p).exists()]
    if missing:
        raise SystemExit("missing input image(s): " + ", ".join(missing))
    return out


def normalize_dialogues(value: Any) -> List[str]:
    if isinstance(value, list):
        out = []
        for item in value:
            if isinstance(item, dict):
                speaker = item.get("speaker") or item.get("name") or item.get("character") or "角色"
                text = item.get("text") or item.get("line") or item.get("dialogue") or ""
                if text:
                    out.append(f"{speaker}：“{text}”")
            else:
                out.append(str(item))
        return out
    if isinstance(value, dict):
        return [f"{k}：“{v}”" for k, v in value.items()]
    return as_list(value)


def compile_prompt(data: Dict[str, Any], args: argparse.Namespace) -> str:
    page_id = args.page_id or data.get("page_id") or data.get("id") or "comic-page"
    title = args.title or data.get("title") or ""
    scene = args.scene or data.get("scene") or ""
    style = args.style_ref_text or data.get("style_ref_text") or "warm beige paper-texture, clean funny editorial comic, minimal Chinese text, large readable typography"
    reminder = args.reminder or data.get("reminder") or ""
    chars = data.get("characters") or {}
    char_text = "; ".join(as_list(chars)) if not isinstance(chars, dict) else "; ".join(f"{k}={v}" for k, v in chars.items())
    dialogues = normalize_dialogues(data.get("dialogues") or data.get("dialogue"))
    screen_text = as_list(data.get("screen_text"))
    forbidden = as_list(data.get("forbidden")) + as_list(args.forbidden)

    parts = [
        f"Square Chinese science comic {page_id}: {title}.",
        f"Scene: {scene}",
        f"Characters: {char_text}.",
    ]
    if dialogues:
        parts.append("Bubbles exactly: " + "；".join(dialogues) + ".")
    if screen_text:
        parts.append("Only card/screen text: " + "；".join(screen_text) + ".")
    if reminder:
        parts.append("Footer: " + reminder)
    parts.append("Style: " + style + ".")
    parts.append("Rules: minimal big readable Chinese; preserve cat/husky; AI only as normal chat screen; no extra captions.")
    # Keep the request compact. Long forbidden lists belong in review docs, not the
    # image prompt; still validate forbidden input-image basenames separately.
    visible_forbidden = [x for x in forbidden if x.lower() not in {"logo", "二维码", "p2"}]
    if visible_forbidden:
        parts.append("Forbidden: " + ", ".join(dict.fromkeys(visible_forbidden)) + ".")
    prompt = "\n".join(x.strip() for x in parts if x and x.strip())
    return prompt


def write_json(path: pathlib.Path, data: Dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Compile concise comic img2img prompts and optionally run happy-img2-direct.")
    ap.add_argument("input", nargs="?", help="JSON/YAML page spec")
    ap.add_argument("--page-id")
    ap.add_argument("--title")
    ap.add_argument("--scene")
    ap.add_argument("--reminder")
    ap.add_argument("--style-ref-text")
    ap.add_argument("--reference-image", action="append", default=[])
    ap.add_argument("--style-image", default="", help="Optional style reference image, e.g. P1. Not used by default.")
    ap.add_argument("--forbidden", action="append", default=[])
    ap.add_argument("--task-name", default="")
    ap.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    ap.add_argument("--size", default="1024x1024")
    ap.add_argument("--timeout-ms", type=int, default=600000)
    ap.add_argument("--max-attempts", type=int, default=1)
    ap.add_argument("--max-input-images", type=int, default=2)
    ap.add_argument("--provider", default="happy")
    ap.add_argument("--model", default="gpt-image-2")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--run", action="store_true", help="Actually call happy-img2-direct. If omitted, dry-run behavior is used.")
    ap.add_argument("--require-character-refs", action=argparse.BooleanOptionalAction, default=True)
    args = ap.parse_args()

    data: Dict[str, Any] = {}
    if args.input:
        data = read_input(args.input)
    if not data and not (args.page_id or args.title or args.scene):
        ap.error("provide an input JSON/YAML or CLI page fields")

    prompt = compile_prompt(data, args)
    input_images = choose_reference_images(data, args)
    task_name = args.task_name or f"{data.get('page_id') or args.page_id or 'comic'}-compiled"
    output_root = pathlib.Path(os.path.expanduser(args.output_dir))
    run_dir = output_root / "_compiler_runs" / f"{slugify(task_name)}-{time.strftime('%Y%m%d-%H%M%S')}"
    run_dir.mkdir(parents=True, exist_ok=True)

    (run_dir / "compiled_prompt.txt").write_text(prompt, encoding="utf-8")
    request = {
        "page_id": args.page_id or data.get("page_id") or data.get("id"),
        "title": args.title or data.get("title"),
        "input_file": data.get("_input_file"),
        "compiled_prompt_chars": len(prompt),
        "input_images": input_images,
        "provider": args.provider,
        "model": args.model,
        "size": args.size,
        "timeout_ms": args.timeout_ms,
        "max_attempts": args.max_attempts,
        "direct_skill": str(DIRECT_RUN),
        "expected_mode": "edit" if input_images else "generation",
    }
    write_json(run_dir / "request.json", request)

    cmd = [sys.executable, str(DIRECT_RUN), "--prompt", prompt, "--task-name", task_name, "--provider", args.provider, "--model", args.model, "--size", args.size, "--timeout-ms", str(args.timeout_ms), "--max-attempts", str(args.max_attempts), "--output-dir", str(output_root), "--no-send"]
    for img in input_images:
        cmd += ["--input-image", img]
    (run_dir / "run_command.md").write_text("```bash\n" + " \\\n  ".join(shlex.quote(x) for x in cmd) + "\n```\n", encoding="utf-8")

    should_run = args.run and not args.dry_run
    summary: Dict[str, Any] = {
        "ok": True,
        "stage": "dry_run" if not should_run else "prepared",
        "created_at": iso_now(),
        "run_dir": str(run_dir),
        "compiled_prompt": str(run_dir / "compiled_prompt.txt"),
        "compiled_prompt_chars": len(prompt),
        "input_images": input_images,
        "used_direct_endpoint_expected": "/images/edits" if input_images else "/images/generations",
        "direct_skill": str(DIRECT_RUN),
    }

    if should_run:
        started = time.time()
        proc = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=args.timeout_ms / 1000 + 45)
        elapsed = round(time.time() - started, 3)
        (run_dir / "stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
        (run_dir / "stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
        try:
            result = json.loads((proc.stdout or "").strip())
        except Exception:
            result = {"ok": False, "stage": "parse_stdout", "returncode": proc.returncode, "stdout_tail": (proc.stdout or "")[-2000:], "stderr_tail": (proc.stderr or "")[-2000:]}
        write_json(run_dir / "result.json", result)
        summary.update({
            "ok": bool(result.get("ok")) and proc.returncode == 0,
            "stage": "done" if result.get("ok") and proc.returncode == 0 else "failed",
            "elapsed_seconds": elapsed,
            "returncode": proc.returncode,
            "output": result.get("output", ""),
            "result_json": str(run_dir / "result.json"),
            "actual_mode": result.get("mode"),
            "used_direct_endpoint_actual": "/images/edits" if result.get("mode") == "edit" else ("/images/generations" if result.get("mode") == "generation" else "unknown"),
            "provider": result.get("provider"),
            "model": result.get("model"),
            "bytes": result.get("bytes"),
            "direct_run_dir": result.get("run_dir"),
        })
    else:
        (run_dir / "stdout.txt").write_text("", encoding="utf-8")
        (run_dir / "stderr.txt").write_text("", encoding="utf-8")
        write_json(run_dir / "result.json", {"ok": True, "stage": "dry_run", "mode": "edit" if input_images else "generation", "input_images": input_images})

    write_json(run_dir / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary.get("ok") else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.TimeoutExpired as e:
        print(json.dumps({"ok": False, "stage": "timeout", "error": str(e)}, ensure_ascii=False, indent=2))
        raise SystemExit(124)
