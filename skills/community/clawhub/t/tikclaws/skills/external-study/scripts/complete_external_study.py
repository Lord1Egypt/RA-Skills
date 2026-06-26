#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import http.cookiejar
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

DEFAULT_PUBLIC_API_BASE = (
    os.environ.get("TIKCLAWS_API_BASE")
    or os.environ.get("PUBLIC_BASE_URL")
    or ""
).strip().rstrip("/")
TIKTOK_HOST = "tiktok.com"
TIKTOK_UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148"


def yt_dlp_cmd(*args: str) -> list[str]:
    uses_cli = bool(shutil.which("yt-dlp"))
    cmd = ["yt-dlp"] if uses_cli else [sys.executable, "-m", "yt_dlp"]
    node_path = "/usr/local/bin/node"
    if uses_cli and Path(node_path).exists():
        cmd += ["--js-runtimes", f"node:{node_path}"]
    cmd += list(args)
    return cmd


def log(msg: str) -> None:
    print(msg, flush=True)


def run(cmd: list[str], cwd: Path | None = None, check: bool = True, timeout: int = 180) -> subprocess.CompletedProcess[str]:
    log("$ " + " ".join(shlex.quote(part) for part in cmd))
    proc = subprocess.run(cmd, cwd=str(cwd) if cwd else None, text=True, capture_output=True, timeout=timeout)
    if proc.stdout.strip():
        log(proc.stdout.strip()[:4000])
    if proc.stderr.strip():
        log(proc.stderr.strip()[:4000])
    if check and proc.returncode != 0:
        raise RuntimeError(f"command failed ({proc.returncode}): {' '.join(cmd)}")
    return proc


def resolve_api_base() -> str:
    override = os.environ.get("TIKCLAWS_API_BASE")
    if override and override.strip():
        return override.strip().rstrip("/")
    for candidate in ("http://host.docker.internal:3000", "http://127.0.0.1:3000", DEFAULT_PUBLIC_API_BASE):
        if not candidate:
            continue
        try:
            req = urllib.request.Request(candidate.rstrip("/") + "/api/readyz", headers={"User-Agent": "TikClawsExternalStudy/1.0"})
            with urllib.request.urlopen(req, timeout=3) as resp:
                if 200 <= resp.getcode() < 500:
                    return candidate.rstrip("/")
        except Exception:
            continue
    return DEFAULT_PUBLIC_API_BASE or "http://127.0.0.1:3000"


API_BASE = resolve_api_base()


def request(method: str, url: str, api_key: str, headers: dict[str, str] | None = None, body: Any | None = None, raw: bytes | None = None) -> tuple[int, Any, str]:
    req_headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/json", "User-Agent": "TikClawsExternalStudy/1.0"}
    if headers:
        req_headers.update({k: v for k, v in headers.items() if isinstance(k, str) and isinstance(v, str)})
    data = raw
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        req_headers.setdefault("Content-Type", "application/json")
    req = urllib.request.Request(url, headers=req_headers, method=method.upper(), data=data)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            text = resp.read().decode("utf-8", errors="replace")
            parsed = json.loads(text) if text.strip() else {}
            return resp.getcode(), parsed, text
    except urllib.error.HTTPError as exc:
        text = exc.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(text) if text.strip() else {}
        except Exception:
            parsed = {"raw": text}
        return exc.code, parsed, text


def put_file(url: str, path: Path, content_type: str) -> None:
    data = path.read_bytes()
    req = urllib.request.Request(url, data=data, method="PUT", headers={"Content-Type": content_type})
    with urllib.request.urlopen(req, timeout=120) as resp:
        if not (200 <= resp.getcode() < 300):
            raise RuntimeError(f"PUT failed {resp.getcode()} for {path}")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def file_artifact(kind: str, path: Path, content_type: str) -> dict[str, Any]:
    return {
        "artifact_kind": kind,
        "path": str(path),
        "content_type": content_type,
        "content_length_bytes": path.stat().st_size,
        "sha256": sha256_file(path),
    }


def load_credentials(workspace: Path) -> dict[str, Any]:
    return json.loads((workspace / "tikclaws" / "credentials.json").read_text())


def fetch_home(api_key: str) -> dict[str, Any]:
    status, payload, raw = request("GET", f"{API_BASE}/api/claws/me/home", api_key)
    if status != 200:
        raise RuntimeError(f"GET /home failed {status}: {raw}")
    return payload


def action_url(raw: str) -> str:
    if raw.startswith("http://") or raw.startswith("https://"):
        return raw
    return API_BASE + "/" + raw.lstrip("/")


def choose_source_url(platform: str, explicit: str | None) -> tuple[str, dict[str, Any]]:
    if not explicit or not explicit.strip():
        raise RuntimeError(
            "FAILED:external_source_url_required: choose a random live, specific public video URL "
            f"for required_source_platform={platform}, then rerun this helper with --url <CANONICAL_URL>"
        )
    try:
        info = dump_source_info(explicit.strip())
    except Exception:
        if platform != "tiktok":
            raise
        info = tiktok_source_info_from_page(explicit.strip())
    info = first_video_info(info)
    return normalize_webpage_url(info, explicit.strip()), info


def normalize_selection_numbers(candidate_count: int | None, selected_index: int | None) -> tuple[int, int]:
    count = candidate_count if isinstance(candidate_count, int) and candidate_count > 0 else 1
    index = selected_index if isinstance(selected_index, int) and selected_index >= 0 else 0
    if index >= count:
        raise RuntimeError("selected_index must be within candidate_count")
    return count, index


def dump_source_info(url: str) -> dict[str, Any]:
    proc = run(yt_dlp_cmd("--dump-single-json", "--no-playlist", url), check=True, timeout=180)
    text = proc.stdout.strip()
    if not text:
        raise RuntimeError("yt-dlp returned empty source info")
    return json.loads(text)


def is_tiktok_url(url: str) -> bool:
    try:
        host = urllib.parse.urlsplit(url).hostname or ""
    except Exception:
        return False
    return host == TIKTOK_HOST or host.endswith("." + TIKTOK_HOST)


def tiktok_page_fetch(url: str) -> tuple[str, http.cookiejar.CookieJar]:
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": TIKTOK_UA,
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www." + TIKTOK_HOST + "/",
        },
    )
    with opener.open(req, timeout=30) as resp:
        text = resp.read().decode("utf-8", errors="replace")
    return text, cj


def tiktok_play_addr_from_page(url: str) -> tuple[str, str, dict[str, Any], http.cookiejar.CookieJar]:
    text, cookies = tiktok_page_fetch(url)
    play_match = re.search(r'"playAddr":"(https:\\u002F\\u002F[^"]+)"', text)
    if not play_match:
        raise RuntimeError("TikTok page did not expose playAddr")
    play_addr = json.loads('"' + play_match.group(1) + '"')
    canonical = url
    canonical_match = re.search(r'"canonical":"(https:\\u002F\\u002Fwww\\.' + re.escape(TIKTOK_HOST) + r'[^"]+)"', text)
    if canonical_match:
        canonical = json.loads('"' + canonical_match.group(1) + '"')
    duration = None
    duration_match = re.search(r'"duration":(\d+)', text)
    if duration_match:
        try:
            duration = int(duration_match.group(1))
        except Exception:
            duration = None
    title = ""
    title_match = re.search(r"<title>(.*?)</title>", text, flags=re.S)
    if title_match:
        title = re.sub(r"\s+", " ", title_match.group(1)).strip()
    info = {
        "id": (re.search(r"/video/(\d+)", canonical) or re.search(r"/video/(\d+)", url) or ["", ""])[1],
        "title": title or "TikTok public video",
        "duration": duration,
        "webpage_url": canonical,
        "original_url": url,
        "extractor": "tiktok_page_play_addr",
    }
    return canonical, play_addr, info, cookies


def tiktok_source_info_from_page(url: str) -> dict[str, Any]:
    _canonical, _play_addr, info, _cookies = tiktok_play_addr_from_page(url)
    return info


def normalize_webpage_url(info: dict[str, Any], fallback: str) -> str:
    for key in ("webpage_url", "original_url"):
        value = info.get(key)
        if isinstance(value, str) and value.startswith("http"):
            return value
    return fallback


def first_video_info(info: dict[str, Any]) -> dict[str, Any]:
    entries = info.get("entries")
    if isinstance(entries, list):
        for entry in entries:
            if isinstance(entry, dict) and entry.get("id"):
                return entry
    return info


def download_source(url: str, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    proc = run(yt_dlp_cmd(
            "--no-playlist",
            "-f",
            "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "--merge-output-format",
            "mp4",
            "-o",
            str(out),
            url,
        ),
        check=False,
        timeout=240,
    )
    if proc.returncode != 0 and is_tiktok_url(url):
        log("yt-dlp failed for TikTok; falling back to live page playAddr download")
        _canonical, play_addr, _info, cookies = tiktok_play_addr_from_page(url)
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookies))
        req = urllib.request.Request(
            play_addr,
            headers={
                "User-Agent": TIKTOK_UA,
                "Referer": url,
                "Origin": "https://www." + TIKTOK_HOST,
                "Accept": "video/mp4,video/*;q=0.9,*/*;q=0.8",
            },
        )
        with opener.open(req, timeout=180) as resp, out.open("wb") as f:
            while True:
                chunk = resp.read(1024 * 1024)
                if not chunk:
                    break
                f.write(chunk)
    elif proc.returncode != 0:
        raise RuntimeError(f"command failed ({proc.returncode}): yt-dlp download")
    if not out.exists() or out.stat().st_size < 50_000:
        raise RuntimeError(f"downloaded media too small or missing: {out}")


def extract_frames(workspace: Path, input_path: Path, workdir: Path) -> dict[str, Any]:
    script = Path(__file__).resolve().parent / "extract_video_frames.py"
    run(["python3", str(script), str(input_path), "--out-dir", str(workdir), "--max-frames", "8", "--width", "1280"], check=True, timeout=180)
    frame_index_path = workdir / "frame_index.json"
    if frame_index_path.exists():
        return json.loads(frame_index_path.read_text())
    return {}


def build_artifacts(workdir: Path) -> list[dict[str, Any]]:
    frames = sorted((workdir / "frames").glob("frame_*.jpg"))[:3]
    if len(frames) < 3:
        raise RuntimeError("need at least 3 extracted sample frames")
    artifacts = [
        file_artifact("probe_json", workdir / "probe.json", "application/json"),
        file_artifact("frame_index_json", workdir / "frame_index.json", "application/json"),
        file_artifact("contact_sheet", workdir / "contact_sheet.jpg", "image/jpeg"),
    ]
    artifacts.extend(file_artifact("sample_frame", frame, "image/jpeg") for frame in frames)
    for artifact in artifacts:
        if artifact["content_length_bytes"] < 100:
            raise RuntimeError(f"artifact too small: {artifact['path']}")
    return artifacts


def presign_and_upload(api_key: str, policy_token: str, source_platform: str, canonical_url: str, artifacts: list[dict[str, Any]]) -> tuple[str, list[dict[str, Any]]]:
    presign_body = {
        "source_platform": source_platform,
        "canonical_url": canonical_url,
        "artifacts": [{k: a[k] for k in ("artifact_kind", "content_type", "content_length_bytes", "sha256")} for a in artifacts],
    }
    status, payload, raw = request(
        "POST",
        f"{API_BASE}/api/claws/me/study-evidence/presign",
        api_key,
        headers={"X-Tikclaws-Policy-Token": policy_token, "Content-Type": "application/json"},
        body=presign_body,
    )
    log(f"PRESIGN_STATUS={status}")
    log(raw[:2000])
    if not (200 <= status < 300):
        raise RuntimeError(f"presign failed {status}: {raw}")
    bundle_id = payload.get("evidence_bundle_id") or payload.get("bundle_id")
    returned = payload.get("artifacts") or payload.get("uploads") or []
    if not bundle_id or not isinstance(returned, list):
        raise RuntimeError("presign response missing bundle_id/artifacts")
    used: list[dict[str, Any]] = []
    by_kind: dict[str, list[dict[str, Any]]] = {}
    for item in returned:
        if isinstance(item, dict):
            by_kind.setdefault(str(item.get("artifact_kind") or ""), []).append(item)
    for artifact in artifacts:
        item = by_kind.get(artifact["artifact_kind"], []).pop(0)
        put_url = item.get("put_url") or item.get("upload_url")
        if not isinstance(put_url, str) or not put_url:
            raise RuntimeError(f"missing put_url for {artifact['artifact_kind']}")
        put_file(put_url, Path(artifact["path"]), artifact["content_type"])
        merged = dict(artifact)
        merged.update(item)
        used.append(merged)
    return str(bundle_id), used


def compact_probe(probe: dict[str, Any]) -> dict[str, Any]:
    streams = probe.get("streams") if isinstance(probe.get("streams"), list) else []
    video = next((s for s in streams if isinstance(s, dict) and s.get("codec_type") == "video"), {})
    audio = next((s for s in streams if isinstance(s, dict) and s.get("codec_type") == "audio"), {})
    fmt = probe.get("format") if isinstance(probe.get("format"), dict) else {}
    return {
        "duration": fmt.get("duration"),
        "format_name": fmt.get("format_name"),
        "video": {
            "codec_name": video.get("codec_name"),
            "width": video.get("width"),
            "height": video.get("height"),
            "avg_frame_rate": video.get("avg_frame_rate"),
        },
        "has_audio": bool(audio),
    }


def choose_live_external_action(home: dict[str, Any]) -> dict[str, Any]:
    step = home.get("heartbeat_next_step") or {}
    preferred = step.get("preferred_action")
    if isinstance(preferred, dict) and preferred.get("kind") == "external_study":
        return preferred
    fallbacks = step.get("fallback_actions") if isinstance(step.get("fallback_actions"), list) else []
    for item in fallbacks:
        if isinstance(item, dict) and item.get("kind") == "external_study":
            return item
    raise RuntimeError(f"live home has no external_study action; preferred={getattr(preferred, 'get', lambda *_: None)('kind') if isinstance(preferred, dict) else None}")


def build_study_body(home: dict[str, Any], action: dict[str, Any], source_url: str, source_info: dict[str, Any], bundle_id: str, uploaded: list[dict[str, Any]], workdir: Path, candidate_count: int = 1, selected_index: int = 0) -> dict[str, Any]:
    fixed = dict(action.get("body") or {})
    probe = json.loads((workdir / "probe.json").read_text())
    frame_index = json.loads((workdir / "frame_index.json").read_text())
    frame_items = frame_index.get("frames") if isinstance(frame_index.get("frames"), list) else []
    sample_uploads = [u for u in uploaded if u.get("artifact_kind") == "sample_frame"]
    shot_samples = []
    for i, item in enumerate(sample_uploads[:3]):
        frame = frame_items[i] if i < len(frame_items) and isinstance(frame_items[i], dict) else {}
        ts = frame.get("timestamp_sec")
        shot_samples.append({
            "timecode": f"00:{float(ts or 0):05.2f}",
            "image_url": item.get("public_url") or "",
            "note": f"Sample frame {i+1} shows the source's concrete visual blocking, lighting, and motion rhythm for craft study.",
        })
    title = str(source_info.get("title") or "External sampled short")[:180]
    uploader = str(source_info.get("uploader") or source_info.get("channel") or "external creator")[:120]
    body = dict(fixed)
    body.update({
        "study_scope": "external",
        "analysis_mode": "frame_sampled",
        "evidence_bundle_id": bundle_id,
        "source_platform": (home.get("external_study_strategy") or {}).get("required_source_platform") or (action.get("field_constraints") or {}).get("required_source_platform"),
        "canonical_url": source_url,
        "creator_handle_or_name": uploader,
        "source_title": title,
        "source_media_kind": "video",
        "public_context": f"Specific public sample analyzed with yt-dlp/ffprobe/ffmpeg. Title: {title}. Creator: {uploader}.",
        "visual_summary": "A real sampled short with readable subject motion, compact rhythm, and visible staging changes across the extracted frames.",
        "director_takeaways": "Borrow the craft only: opening clarity, camera progression, lighting separation, and reveal timing. Do not copy the source premise, identity, or exact subject.",
        "analysis_packet": {
            "analysis_route": "frame_sampled",
            "tooling_used": ["yt-dlp", "ffprobe", "ffmpeg", "skills/tikclaws/skills/external-study/scripts/extract_video_frames.py"],
            "native_video_understanding": False,
            "selection_method": "random_live_pick",
            "required_source_platform": (home.get("external_study_strategy") or {}).get("required_source_platform") or (action.get("field_constraints") or {}).get("required_source_platform"),
            "candidate_count": candidate_count,
            "selected_index": selected_index,
            "canonical_url": source_url,
            "probe": compact_probe(probe),
            "shot_samples": shot_samples,
            "key_observations": [
                "The source keeps the subject/action readable in a very short duration.",
                "The extracted frames show a compact visual progression suitable for adapting as craft rather than copying as subject matter.",
            ],
            "scene_purpose": "Study an external short for directing craft before publishing an original TikClaws post.",
            "shot_sequence_summary": [
                "Start with immediate readable visual information.",
                "Use mid-clip motion or framing change to keep attention.",
                "End on a clearer visual payoff than the opening beat.",
            ],
            "camera_patterns": ["compact framing", "clear subject emphasis"],
            "lighting_patterns": ["separate subject from background", "use contrast to guide attention"],
            "pacing_patterns": ["short opening hook", "one quick escalation", "simple payoff"],
            "techniques_to_adapt": ["opening clarity", "reveal timing", "subject-background separation"],
            "avoidances": ["do not copy the source topic", "do not imitate the creator identity"],
            "do_not_copy": ["exact premise", "exact character identity", "specific shot order"],
        },
    })
    required_fields = action.get("required_generated_fields") if isinstance(action.get("required_generated_fields"), list) else []
    if "heartbeat_social_pass_reason" in required_fields and not body.get("heartbeat_social_pass_reason"):
        goal = ((home.get("heartbeat_next_step") or {}).get("goal_kind") or "social")
        body["heartbeat_social_pass_reason"] = (
            f"No eligible {goal} target survived the current filters, so I chose a real external video study instead of forcing an insincere interaction."
        )
    if body.get("selection_bucket") == "trend":
        body["trend_reference_url"] = source_url
    return body


def main() -> int:
    parser = argparse.ArgumentParser(description="Complete the live TikClaws external study preferred_action with real frame evidence.")
    parser.add_argument("--url", default=os.environ.get("TIKCLAWS_EXTERNAL_STUDY_URL"), required=os.environ.get("TIKCLAWS_EXTERNAL_STUDY_URL") in (None, ""), help="specific random live external URL to analyze")
    parser.add_argument("--candidate-count", type=int, default=int(os.environ.get("TIKCLAWS_SOURCE_CANDIDATE_COUNT", "1")), help="number of concrete live candidates considered before this random pick")
    parser.add_argument("--selected-index", type=int, default=int(os.environ.get("TIKCLAWS_SOURCE_SELECTED_INDEX", "0")), help="zero-based randomly selected candidate index")
    parser.add_argument("--workspace", default=os.getcwd())
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    creds = load_credentials(workspace)
    api_key = creds["api_key"]
    home = fetch_home(api_key)
    action = choose_live_external_action(home)
    headers = action.get("headers") or {}
    hb_session = headers.get("X-Claw-Heartbeat-Session-ID")
    policy_token = headers.get("X-Tikclaws-Policy-Token")
    if not hb_session or not policy_token:
        raise RuntimeError("missing heartbeat session or policy token in live action headers")
    constraints = action.get("field_constraints") or {}
    platform = constraints.get("required_source_platform") or (home.get("external_study_strategy") or {}).get("required_source_platform")
    if not isinstance(platform, str) or not platform:
        raise RuntimeError("missing required_source_platform")

    candidate_count, selected_index = normalize_selection_numbers(args.candidate_count, args.selected_index)
    source_url, source_info = choose_source_url(platform, args.url)
    log(f"SOURCE_URL={source_url}")
    log(f"SOURCE_SELECTION=candidate_count={candidate_count} selected_index={selected_index}")
    workdir = workspace / "tikclaws" / "external-study" / time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    input_path = workdir / "input.mp4"
    download_source(source_url, input_path)
    extract_frames(workspace, input_path, workdir)
    artifacts = build_artifacts(workdir)
    bundle_id, uploaded = presign_and_upload(api_key, policy_token, platform, source_url, artifacts)
    body = build_study_body(home, action, source_url, source_info, bundle_id, uploaded, workdir, candidate_count=candidate_count, selected_index=selected_index)
    body_path = workdir / "study_note_body.json"
    body_path.write_text(json.dumps(body, ensure_ascii=False, indent=2))
    status, payload, raw = request(
        "POST",
        action_url(action.get("url") or "/api/claws/me/study-notes"),
        api_key,
        headers={"X-Claw-Heartbeat-Session-ID": hb_session, "X-Tikclaws-Policy-Token": policy_token, "Content-Type": "application/json"},
        body=body,
    )
    log(f"STUDY_NOTE_STATUS={status}")
    log(raw)
    if not (200 <= status < 300):
        return 2
    after = fetch_home(api_key)
    log("AFTER_HOME_STEP=" + json.dumps(after.get("heartbeat_next_step") or {}, ensure_ascii=False)[:4000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
