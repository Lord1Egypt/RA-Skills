#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import ssl
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlparse, urlsplit, urlunsplit
from urllib.request import Request, urlopen


LYRICS_CREATE_URL = "https://api.senseaudio.cn/v1/music/lyrics/create"
CREATE_URL = "https://api.senseaudio.cn/v1/music/song/create"
PENDING_URL_TEMPLATE = "https://api.senseaudio.cn/v1/music/song/pending/{task_id}"
DEFAULT_MUSIC_MODEL = "senseaudio-music-1.0-260319"
ALLOWED_GENERATION_MODES = {"instrumental", "vocal_female", "vocal_male"}
NETWORK_RETRY_LIMIT = 4


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate music with SenseAudio official music APIs.")
    parser.add_argument("--text-file", default="")
    parser.add_argument("--transcript-json", default="")
    parser.add_argument("--env-file", default="")
    parser.add_argument("--output-dir", default="")
    parser.add_argument("--title", default="")
    parser.add_argument("--model", default="")
    parser.add_argument("--style-preset", default="")
    parser.add_argument("--generation-mode", default="instrumental")
    parser.add_argument("--prompt-extra", default="")
    parser.add_argument("--timeout-seconds", type=int, default=480)
    parser.add_argument("--poll-interval", type=int, default=8)
    return parser.parse_args()


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        raw = line.strip()
        if not raw or raw.startswith("#") or "=" not in raw:
            continue
        key, value = raw.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def resolve_api_key() -> str:
    for key_name in ["SENSEAUDIO_API_KEY", "AUDIOCLAW_ASR_API_KEY"]:
        value = os.environ.get(key_name, "").strip()
        if value:
            return value
    raise SystemExit("Missing SenseAudio API key. Expected SENSEAUDIO_API_KEY or AUDIOCLAW_ASR_API_KEY.")


def resolve_music_model(explicit: str) -> str:
    if explicit.strip():
        return explicit.strip()
    for key_name in ["SENSEAUDIO_MUSIC_MODEL", "SENSEAUDIO_SONG_MODEL"]:
        value = os.environ.get(key_name, "").strip()
        if value:
            return value
    return DEFAULT_MUSIC_MODEL


def normalize_generation_mode(raw: str) -> str:
    value = (raw or "").strip().lower()
    return value if value in ALLOWED_GENERATION_MODES else "instrumental"


def read_source_text(text_file: str, transcript_json: str) -> tuple[str, str, Path]:
    if text_file.strip():
        path = Path(text_file).expanduser().resolve()
        text = path.read_text(encoding="utf-8").strip()
        if not text:
            raise SystemExit("Text file is empty.")
        return text, path.stem, path

    if transcript_json.strip():
        path = Path(transcript_json).expanduser().resolve()
        payload = json.loads(path.read_text(encoding="utf-8"))
        text = str(payload.get("transcript_text") or "").strip()
        if not text and isinstance(payload.get("segments"), list):
            text = " ".join(str(item.get("text") or "").strip() for item in payload["segments"]).strip()
        if not text:
            raise SystemExit("Transcript is empty.")
        return text, path.parent.name, path

    raise SystemExit("Either --text-file or --transcript-json is required.")


def infer_output_dir(explicit: str, source_path: Path) -> Path:
    if explicit.strip():
        return Path(explicit).expanduser().resolve()
    if source_path.name == "senseaudio_asr.json":
        return source_path.parent / "music_generation"
    return source_path.parent / f"{source_path.stem}_music"


def shorten(text: str, limit: int) -> str:
    compact = " ".join(text.split())
    if len(compact) <= limit:
        return compact
    return compact[:limit].rstrip() + "..."


def derive_title(explicit: str, fallback: str) -> str:
    if explicit.strip():
        return explicit.strip()[:40]
    compact = "".join(ch for ch in fallback if ch not in "\\/:*?\"<>|").strip()
    compact = compact[:18] if compact else "AudioClaw"
    return f"{compact}配乐"


def style_instruction(style_preset: str) -> str:
    styles = {
        "cinematic": "风格偏电影感与情绪推进，适合总结、纪录片和旁白背景。",
        "ambient": "风格偏氛围与治愈，层次轻柔、空间感明显，适合安静内容。",
        "electronic": "风格偏现代轻电子与律动，节奏清晰但不要过于吵闹。",
        "piano": "风格偏钢琴叙事与温柔铺陈，旋律清楚，适合讲述和回顾内容。",
        "uplifting": "风格偏积极明亮与轻鼓点，适合产品展示、vlog 和轻快内容。",
    }
    return styles.get(style_preset.strip(), styles["cinematic"])


def build_prompt(source_text: str, *, style_preset: str, prompt_extra: str) -> str:
    snippet = shorten(source_text, 420)
    prompt = (
        "[intro-medium] ; "
        f"[verse] 这段纯音乐围绕以下内容展开：{snippet}。整体气质要求温暖、自然、具备旋律记忆点。{style_instruction(style_preset)} ; "
        "[chorus] 旋律进一步打开，情绪更明亮、更治愈，适合作为视频总结或内容回顾的主旋律段落。 ; "
        "[bridge] 保持空间感与层次，减少拥挤感，允许短暂情绪抬升后自然回落。 ; "
        "[outro-medium]"
    )
    if prompt_extra.strip():
        prompt = prompt[:-len("[outro-medium]")] + f"补充要求：{prompt_extra.strip()} ; [outro-medium]"
    return prompt


def build_lyrics_prompt(source_text: str, *, style_preset: str, prompt_extra: str) -> str:
    snippet = shorten(source_text, 520)
    prompt = (
        "请根据下面内容创作一首适合视频总结或内容表达的中文歌曲歌词。"
        "要求：结构完整，包含前奏/主歌/副歌/桥段/尾奏等合理段落；"
        "语言自然，有记忆点，情绪清楚，适合后续自动作曲。"
        f"{style_instruction(style_preset)}"
        f"参考内容：{snippet}"
    )
    if prompt_extra.strip():
        prompt += f" 补充要求：{prompt_extra.strip()}"
    return prompt


def request_json(url: str, *, method: str = "GET", api_key: str, payload: dict | None = None) -> dict:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "User-Agent": "AudioClaw-RealtimeInterpreter/1.0",
    }
    data = None
    if payload is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = Request(url, data=data, headers=headers, method=method)
    last_error: str | None = None
    for attempt in range(1, NETWORK_RETRY_LIMIT + 1):
        try:
            with urlopen(req, timeout=60) as resp:
                raw = resp.read().decode("utf-8", "ignore")
            break
        except HTTPError as exc:
            body = exc.read().decode("utf-8", "ignore")
            raise SystemExit(body or f"SenseAudio API returned HTTP {exc.code}")
        except (URLError, ssl.SSLError, OSError) as exc:
            reason = getattr(exc, "reason", None) or str(exc)
            last_error = str(reason)
            if attempt >= NETWORK_RETRY_LIMIT:
                raise SystemExit(f"SenseAudio request failed: {last_error}")
            time.sleep(min(8, attempt * 2))
    else:
        raise SystemExit(f"SenseAudio request failed: {last_error or 'unknown network error'}")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        raise SystemExit(f"SenseAudio returned non-JSON response: {raw[:300]}")


def walk_values(payload: object):
    if isinstance(payload, dict):
        for key, value in payload.items():
            yield key, value
            yield from walk_values(value)
    elif isinstance(payload, list):
        for item in payload:
            yield from walk_values(item)


def find_first_string(payload: dict, candidate_keys: list[str]) -> str:
    for key, value in walk_values(payload):
        if key in candidate_keys and isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def find_status(payload: dict) -> str:
    for key in ["status", "task_status", "state"]:
        value = find_first_string(payload, [key])
        if value:
            return value
    return ""


def first_data_item(payload: dict) -> dict:
    response = payload.get("response")
    if isinstance(response, dict):
        data = response.get("data")
        if isinstance(data, list) and data and isinstance(data[0], dict):
            return data[0]
    data = payload.get("data")
    if isinstance(data, list) and data and isinstance(data[0], dict):
        return data[0]
    return {}


def music_style_value(style_preset: str) -> tuple[str, float]:
    mapping = {
        "cinematic": ("cinematic", 0.78),
        "ambient": ("ambient", 0.72),
        "electronic": ("electronic", 0.76),
        "piano": ("piano", 0.74),
        "uplifting": ("pop", 0.7),
    }
    return mapping.get(style_preset.strip(), ("cinematic", 0.78))


def negative_tags_for_mode(generation_mode: str) -> str:
    base = "低质噪音,杂乱失真,对白,口播,电流声"
    if generation_mode == "instrumental":
        return base + ",有人声,说唱"
    return base


def create_lyrics(api_key: str, provider: str, prompt: str) -> dict:
    payload = {
        "prompt": prompt,
        "provider": provider,
    }
    response = request_json(LYRICS_CREATE_URL, method="POST", api_key=api_key, payload=payload)
    item = first_data_item(response)
    if not item.get("text"):
        raise SystemExit("SenseAudio lyrics_create did not return lyrics text.")
    return {"request": payload, "response": response, "item": item}


def submit_music_task(
    api_key: str,
    *,
    model: str,
    title: str,
    lyrics_or_prompt: str,
    style_preset: str,
    generation_mode: str,
) -> tuple[str, dict]:
    style, style_weight = music_style_value(style_preset)
    payload: dict[str, object] = {
        "model": model,
        "title": title,
        "lyrics": lyrics_or_prompt,
        "style": style,
        "style_weight": style_weight,
        "negative_tags": negative_tags_for_mode(generation_mode),
    }
    if generation_mode == "instrumental":
        payload["instrumental"] = True
    else:
        payload["instrumental"] = False
        payload["vocal_gender"] = "f" if generation_mode == "vocal_female" else "m"
    response = request_json(CREATE_URL, method="POST", api_key=api_key, payload=payload)
    task_id = find_first_string(response, ["task_id", "id"])
    if task_id:
        return task_id, {"request": payload, "response": response}
    raise SystemExit("Could not create music task. " + json.dumps(response, ensure_ascii=False))


def wait_for_music(api_key: str, task_id: str, timeout_seconds: int, poll_interval: int) -> dict:
    deadline = time.time() + timeout_seconds
    last_response: dict = {}
    while time.time() < deadline:
        payload = request_json(PENDING_URL_TEMPLATE.format(task_id=task_id), api_key=api_key)
        last_response = payload
        audio_url = str(first_data_item(payload).get("audio_url") or "").strip() or find_first_string(payload, ["audio_url", "url", "music_url"])
        if audio_url:
            return payload
        status = find_status(payload).lower()
        if status in {"failed", "error", "canceled", "cancelled"}:
            raise SystemExit(json.dumps(payload, ensure_ascii=False))
        time.sleep(max(2, poll_interval))
    raise SystemExit("Timed out waiting for SenseAudio music generation. Last response: " + json.dumps(last_response, ensure_ascii=False))


def infer_suffix_from_url(url: str) -> str:
    parsed = urlparse(url)
    suffix = Path(parsed.path).suffix.lower()
    return suffix if suffix else ".mp3"


def infer_suffix_from_audio_bytes(data: bytes, fallback: str) -> str:
    if data.startswith(b"RIFF") and data[8:12] == b"WAVE":
        return ".wav"
    if data.startswith(b"ID3") or data[:2] in (b"\xff\xfb", b"\xff\xf3", b"\xff\xf2"):
        return ".mp3"
    if data.startswith(b"OggS"):
        return ".ogg"
    if data[4:8] == b"ftyp":
        return ".m4a"
    return fallback


def normalize_download_url(url: str) -> str:
    split = urlsplit(url)
    normalized_path = quote(split.path, safe="/%")
    normalized_query = quote(split.query, safe="=&%")
    return urlunsplit((split.scheme, split.netloc, normalized_path, normalized_query, split.fragment))


def download_file(url: str, destination: Path) -> Path:
    req = Request(normalize_download_url(url), headers={"User-Agent": "AudioClaw-RealtimeInterpreter/1.0"})
    last_error: str | None = None
    for attempt in range(1, NETWORK_RETRY_LIMIT + 1):
        try:
            with urlopen(req, timeout=120) as resp:
                data = resp.read()
            resolved_suffix = infer_suffix_from_audio_bytes(data, destination.suffix.lower())
            resolved_destination = destination.with_suffix(resolved_suffix)
            resolved_destination.write_bytes(data)
            if resolved_destination != destination and destination.exists():
                destination.unlink()
            return resolved_destination
        except (URLError, ssl.SSLError, OSError) as exc:
            reason = getattr(exc, "reason", None) or str(exc)
            last_error = str(reason)
            if attempt >= NETWORK_RETRY_LIMIT:
                raise SystemExit(f"Failed to download generated audio: {last_error}")
            time.sleep(min(8, attempt * 2))
    raise SystemExit(f"Failed to download generated audio: {last_error or 'unknown network error'}")


def main() -> int:
    args = parse_args()
    if args.env_file.strip():
        load_dotenv(Path(args.env_file).expanduser().resolve())
    else:
        load_dotenv(Path(__file__).resolve().parents[2] / ".env")
    api_key = resolve_api_key()
    model = resolve_music_model(args.model)

    source_text, fallback_title, source_path = read_source_text(args.text_file, args.transcript_json)
    output_dir = infer_output_dir(args.output_dir, source_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    title = derive_title(args.title, fallback_title)
    generation_mode = normalize_generation_mode(args.generation_mode)
    prompt = build_prompt(
        source_text,
        style_preset=args.style_preset,
        prompt_extra=args.prompt_extra,
    )
    prompt_path = output_dir / "music_prompt.txt"
    prompt_path.write_text(prompt + "\n", encoding="utf-8")
    lyrics_bundle: dict | None = None
    lyrics_or_prompt = prompt
    lyrics_prompt_path: Path | None = None
    lyrics_text_path: Path | None = None
    if generation_mode != "instrumental":
        lyrics_prompt = build_lyrics_prompt(
            source_text,
            style_preset=args.style_preset,
            prompt_extra=args.prompt_extra,
        )
        lyrics_prompt_path = output_dir / "lyrics_prompt.txt"
        lyrics_prompt_path.write_text(lyrics_prompt + "\n", encoding="utf-8")
        lyrics_bundle = create_lyrics(api_key, model, lyrics_prompt)
        lyrics_item = lyrics_bundle["item"]
        lyrics_or_prompt = str(lyrics_item.get("text") or "").strip()
        lyrics_text_path = output_dir / "generated_lyrics.txt"
        lyrics_text_path.write_text(lyrics_or_prompt + "\n", encoding="utf-8")
        title = derive_title(str(lyrics_item.get("title") or "").strip() or args.title, fallback_title)

    task_id, create_bundle = submit_music_task(
        api_key,
        model=model,
        title=title,
        lyrics_or_prompt=lyrics_or_prompt,
        style_preset=args.style_preset,
        generation_mode=generation_mode,
    )
    status_payload = wait_for_music(api_key, task_id, args.timeout_seconds, args.poll_interval)
    result_item = first_data_item(status_payload)
    audio_url = str(result_item.get("audio_url") or "").strip() or find_first_string(status_payload, ["audio_url", "url", "music_url"])
    if not audio_url:
        raise SystemExit("SenseAudio did not return an audio_url.")

    suffix = infer_suffix_from_url(audio_url)
    audio_path = output_dir / f"generated_music_{task_id}{suffix}"
    audio_path = download_file(audio_url, audio_path)

    manifest = {
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "task_id": task_id,
        "model": model,
        "title": title,
        "generation_mode": generation_mode,
        "style_preset": args.style_preset.strip() or "cinematic",
        "prompt_extra": args.prompt_extra.strip(),
        "source_path": str(source_path),
        "prompt_file": str(prompt_path),
        "lyrics_prompt_file": str(lyrics_prompt_path) if lyrics_prompt_path else "",
        "lyrics_file": str(lyrics_text_path) if lyrics_text_path else "",
        "output_audio": str(audio_path),
        "audio_url": audio_url,
        "cover_url": str(result_item.get("cover_url") or ""),
        "duration": result_item.get("duration"),
        "lyrics": str(result_item.get("lyrics") or lyrics_or_prompt),
        "song_id": str(result_item.get("id") or ""),
        "lyrics_request": lyrics_bundle["request"] if lyrics_bundle else None,
        "lyrics_response": lyrics_bundle["response"] if lyrics_bundle else None,
        "create_request": create_bundle["request"],
        "create_response": create_bundle["response"],
        "status_response": status_payload,
    }
    (output_dir / "generated_music.meta.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
