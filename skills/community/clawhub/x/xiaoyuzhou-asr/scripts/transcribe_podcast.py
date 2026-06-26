#!/usr/bin/env python3
"""
小宇宙播客转录工具
从 小宇宙 FM 获取播客音频，使用 Qwen3-ASR 本地转录为文字。

用法:
  python3 transcribe_podcast.py --token TOKEN --keyword "关键词"
  python3 transcribe_podcast.py --token TOKEN --eid EPISODE_ID
  python3 transcribe_podcast.py --token TOKEN --url https://www.xiaoyuzhoufm.com/episode/EPISODE_ID
  python3 transcribe_podcast.py --check-env --token TOKEN
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Optional
from urllib.parse import parse_qs, unquote, urlparse

BASE_URL = os.environ.get("XYZ_BASE_URL", "http://localhost:23020")
AUDIO_DIR = Path(tempfile.gettempdir()) / "xiaoyuzhou-audio"
MAX_SEGMENT_SEC = 180  # 3 min — Metal GPU hangs on longer segments
HTTP_TIMEOUT_SEC = float(os.environ.get("XYZ_HTTP_TIMEOUT", "15"))
DOWNLOAD_TIMEOUT_SEC = float(os.environ.get("XYZ_DOWNLOAD_TIMEOUT", "120"))
USER_AGENT = "xiaoyuzhou-asr/2.0"
VERSION = "2.0.0"


def _is_local_host(hostname: Optional[str]) -> bool:
    """Return True when a hostname points at the local machine."""
    if not hostname:
        return False
    host = hostname.strip("[]").lower()
    return host in {"localhost", "127.0.0.1", "::1", "0.0.0.0"} or host.endswith(".localhost")


def _ensure_local_proxy_bypass(base_url: str) -> None:
    """Make urllib skip HTTP(S)_PROXY for a local xyz API endpoint."""
    parsed = urlparse(base_url)
    if not _is_local_host(parsed.hostname):
        return

    existing: list[str] = []
    for key in ("NO_PROXY", "no_proxy"):
        existing.extend(p.strip() for p in os.environ.get(key, "").split(",") if p.strip())
    if "*" in existing:
        return

    seen = {p.lower() for p in existing}
    for host in ("localhost", "127.0.0.1", "::1", "0.0.0.0"):
        if host.lower() not in seen:
            existing.append(host)
            seen.add(host.lower())

    value = ",".join(existing)
    os.environ["NO_PROXY"] = value
    os.environ["no_proxy"] = value


_ensure_local_proxy_bypass(BASE_URL)


# --- Auto-detect paths ---

def _detect_model_dir() -> str:
    """Detect Qwen3-ASR model directory."""
    env = os.environ.get("QWEN3_ASR_MODEL_DIR")
    if env and Path(env).exists():
        return env
    candidates = [
        Path.home() / "qwen3-asr-models" / "0.6B",
        Path.home() / "models" / "0.6B",
        Path("/opt/qwen3-asr-models/0.6B"),
    ]
    for c in candidates:
        if c.exists():
            return str(c)
    return str(candidates[0])  # return default even if missing (for --check-env)


def _detect_asr_bin() -> str:
    """Detect qwen3-asr-rs local_transcribe binary."""
    env = os.environ.get("QWEN3_ASR_BIN")
    if env and Path(env).exists():
        return env
    # Check PATH
    found = shutil.which("local_transcribe")
    if found:
        return found
    candidates = [
        Path.home() / "qwen3-asr-rs" / "target" / "release" / "examples" / "local_transcribe",
        Path.home() / "src" / "qwen3-asr-rs" / "target" / "release" / "examples" / "local_transcribe",
    ]
    for c in candidates:
        if c.exists():
            return str(c)
    return str(candidates[0])


# --- Custom exceptions ---

class TranscriptionError(Exception):
    """Base exception for transcription errors."""


class ApiError(TranscriptionError):
    """xyz API call failed."""

    def __init__(self, message: str, status_code: int = 0):
        super().__init__(message)
        self.status_code = status_code


class TokenExpiredError(ApiError):
    """Access token has expired and refresh failed."""


class DependencyError(TranscriptionError):
    """Required dependency is missing or misconfigured."""


class AudioError(TranscriptionError):
    """Audio processing error."""


def sanitize_filename(title: str, max_len: int = 50) -> str:
    """Create a safe cross-platform filename from a title."""
    # Replace common separators with hyphens
    name = re.sub(r"[/\\|:]", "-", title)
    # Remove characters unsafe on any platform
    name = re.sub(r'[<>"*?\x00-\x1f]', "", name)
    # Collapse whitespace and hyphens
    name = re.sub(r"[\s_]+", " ", name).strip()
    # Truncate to max_len (keeping valid unicode chars)
    if len(name) > max_len:
        name = name[:max_len].rsplit(" ", 1)[0].rstrip("- ")
    return name or "untitled"


def episode_file_stem(episode: dict, fallback: str = "episode") -> str:
    """Create a stable filename stem that avoids collisions across same-title episodes."""
    title = str(episode.get("title") or fallback)
    eid = str(episode.get("eid") or fallback)
    pub_date = (episode.get("pubDate") or "")[:10]

    date_part = sanitize_filename(pub_date, max_len=10) if pub_date else ""
    eid_part = sanitize_filename(eid, max_len=32) if eid and eid not in title else ""
    fixed_len = len(date_part) + len(eid_part)
    separator_len = 3 * len([p for p in (date_part, eid_part) if p])
    title_budget = max(20, 90 - fixed_len - separator_len)
    title_part = sanitize_filename(title, max_len=title_budget)

    return " - ".join(p for p in (date_part, title_part, eid_part) if p)


def output_extension(fmt: str) -> str:
    """Return the conventional output extension for a formatter name."""
    return {
        "markdown": "md",
        "srt": "srt",
        "txt": "txt",
        "json": "json",
    }.get(fmt, "txt")


def extract_episode_id_from_url(value: str) -> str:
    """Extract a Xiaoyuzhou episode id from a supported episode URL."""
    parsed = urlparse(value.strip())
    if not parsed.scheme or not parsed.netloc:
        raise TranscriptionError(f"不是有效 URL: {value}")

    host = parsed.netloc.lower()
    if host != "xiaoyuzhoufm.com" and not host.endswith(".xiaoyuzhoufm.com"):
        raise TranscriptionError(f"暂不支持的小宇宙链接域名: {parsed.netloc}")

    query = parse_qs(parsed.query)
    for key in ("eid", "episode_id", "episodeId"):
        candidate = query.get(key, [""])[0].strip()
        if candidate:
            return candidate

    segments = [s for s in parsed.path.split("/") if s]
    for i, segment in enumerate(segments):
        if segment in {"episode", "episodes"} and i + 1 < len(segments):
            return unquote(segments[i + 1])

    raise TranscriptionError(
        "无法从链接中提取单集 ID；请使用形如 "
        "https://www.xiaoyuzhoufm.com/episode/EPISODE_ID 的链接，或直接传 --eid"
    )


def validate_asr_environment(model_dir: str, asr_bin: str) -> None:
    """Fail fast before downloading audio if local ASR dependencies are missing."""
    if not asr_bin:
        raise DependencyError("ASR 二进制路径为空，请设置 --asr-bin 或 QWEN3_ASR_BIN")

    if not Path(asr_bin).exists() and not shutil.which(asr_bin):
        raise DependencyError(
            f"ASR 二进制不存在: {asr_bin}\n"
            "请先编译: cd qwen3-asr-rs && cargo build --release --example local_transcribe"
        )

    model_path = Path(model_dir)
    if not model_path.exists():
        raise DependencyError(f"模型目录不存在: {model_dir}")

    required = ["config.json", "vocab.json", "merges.txt"]
    if not (model_path / "tokenizer.json").exists():
        required.append("tokenizer_config.json")
    missing = [name for name in required if not (model_path / name).exists()]
    if missing:
        raise DependencyError(f"模型目录不完整，缺少: {', '.join(missing)} ({model_dir})")

    if not any(model_path.glob("*.safetensors")):
        raise DependencyError(f"模型目录不完整，缺少 *.safetensors 权重文件 ({model_dir})")


CONFIG_PATH = Path.home() / ".xiaoyuzhou-asr.json"


def load_config() -> dict:
    """Load config from ~/.xiaoyuzhou-asr.json."""
    if CONFIG_PATH.exists():
        try:
            return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))  # type: ignore[no-any-return]
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def save_config(config: dict) -> None:
    """Save config to ~/.xiaoyuzhou-asr.json."""
    CONFIG_PATH.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")
    try:
        os.chmod(CONFIG_PATH, 0o600)
    except (OSError, TypeError, ValueError):
        pass
    print(f"配置已保存到 {CONFIG_PATH}")


def read_json_response(resp, context: str) -> dict:
    """Read and validate a JSON object response from urllib."""
    status = getattr(resp, "status", 0) or getattr(resp, "code", 0) or 0
    body = resp.read()
    if not body or not body.strip():
        raise ApiError(f"{context} 响应为空 (HTTP {status})", status_code=status)
    try:
        parsed = json.loads(body)
    except json.JSONDecodeError:
        preview = body[:200].decode("utf-8", errors="replace")
        raise ApiError(f"{context} 返回非 JSON 响应 (HTTP {status}): {preview}", status_code=status)
    if not isinstance(parsed, dict):
        raise ApiError(f"{context} JSON 响应不是对象 (HTTP {status})", status_code=status)
    return parsed


def resolve_setting(cli_value: Optional[str], env_key: str, config_key: str) -> Optional[str]:
    """Resolve a setting from CLI arg > env var > config file."""
    if cli_value:
        return cli_value
    env_val = os.environ.get(env_key)
    if env_val:
        return env_val
    return load_config().get(config_key)


def do_login(base_url: str) -> None:
    """Interactive login flow: send code → verify → save tokens."""
    import urllib.request
    import urllib.error

    phone = input("手机号 (含区号，如 13111111111): ").strip()
    if not phone:
        print("手机号不能为空")
        return

    area_code = "+86"
    # Send verification code
    req = urllib.request.Request(
        f"{base_url}/sendCode",
        data=json.dumps({"mobilePhoneNumber": phone, "areaCode": area_code}).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT_SEC) as resp:
            result = read_json_response(resp, "发送验证码")
        print("验证码已发送，请查看手机短信")
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"发送验证码失败: {e.code} {body[:200]}")
        return
    except urllib.error.URLError as e:
        print(f"无法连接 {base_url}，请确认 xyz 服务已启动")
        return
    except ApiError as e:
        print(f"发送验证码失败: {e}")
        return

    code = input("验证码: ").strip()
    if not code:
        print("验证码不能为空")
        return

    # Login
    req = urllib.request.Request(
        f"{base_url}/login",
        data=json.dumps({"mobilePhoneNumber": phone, "areaCode": area_code, "verifyCode": code}).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT_SEC) as resp:
            result = read_json_response(resp, "登录")
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"登录失败: {e.code} {body[:200]}")
        return
    except ApiError as e:
        print(f"登录失败: {e}")
        return

    data = result.get("data", {})
    access_token = data.get("x-jike-access-token") or data.get("token", "")
    refresh_token = data.get("x-jike-refresh-token") or data.get("refreshToken", "")

    if not access_token:
        print(f"登录响应异常: {json.dumps(result, ensure_ascii=False)[:200]}")
        return

    config = load_config()
    config["token"] = access_token
    if refresh_token:
        config["refresh_token"] = refresh_token
    save_config(config)
    print("登录成功!")


# --- API ---

def api(endpoint: str, token: str, payload: dict, _retry: bool = True) -> dict:
    """Call xyz API endpoint with auto token refresh on 401."""
    import urllib.request
    import urllib.error
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"{BASE_URL}{endpoint}",
        data=data,
        headers={
            "Content-Type": "application/json",
            "x-jike-access-token": token,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT_SEC) as resp:
            return read_json_response(resp, f"API {endpoint}")
    except urllib.error.HTTPError as e:
        if e.code == 401 and _retry:
            refresh_token = os.environ.get("XYZ_REFRESH_TOKEN") or load_config().get("refresh_token")
            if refresh_token:
                print("  Token 过期，自动刷新...")
                try:
                    refresh_req = urllib.request.Request(
                        f"{BASE_URL}/refresh_token",
                        data=json.dumps({
                            "x-jike-access-token": token,
                            "x-jike-refresh-token": refresh_token,
                        }).encode(),
                        headers={"Content-Type": "application/json"},
                        method="POST",
                    )
                    with urllib.request.urlopen(refresh_req, timeout=HTTP_TIMEOUT_SEC) as resp:
                        result = read_json_response(resp, "刷新 token")
                    new_token = (result.get("data", {}).get("x-jike-access-token")
                                 or result.get("data", {}).get("token", ""))
                    if new_token:
                        os.environ["XYZ_ACCESS_TOKEN"] = new_token
                        config = load_config()
                        config["token"] = new_token
                        new_refresh = result.get("data", {}).get("x-jike-refresh-token")
                        if new_refresh:
                            config["refresh_token"] = new_refresh
                            os.environ["XYZ_REFRESH_TOKEN"] = new_refresh
                        save_config(config)
                        return api(endpoint, new_token, payload, _retry=False)
                except Exception:
                    pass
            raise TokenExpiredError(
                f"Token 过期且刷新失败，请重新登录 (POST {BASE_URL}/login)",
                status_code=401,
            )
        raise ApiError(f"API 错误 {e.code}: {endpoint}", status_code=e.code)
    except urllib.error.URLError as e:
        raise ApiError(
            f"无法连接 xyz API ({BASE_URL})，请确认服务已启动: {e.reason}",
        )


# --- Search and Episode ---

def search_episodes(token: str, keyword: str, limit: int = 5, loadMoreKey: Optional[dict] = None) -> tuple:
    """Search episodes by keyword. Returns (episodes, next_loadMoreKey)."""
    payload: dict = {"keyword": keyword, "type": "EPISODE"}
    if loadMoreKey:
        payload["loadMoreKey"] = loadMoreKey
    result = api("/search", token, payload)
    episodes = []
    for item in result.get("data", {}).get("data", []):
        if item.get("type") == "EPISODE":
            episodes.append(item)
    next_key = result.get("data", {}).get("loadMoreKey")
    return episodes[:limit], next_key


def search_all_episodes(token: str, keyword: str, max_pages: int = 10) -> list:
    """Search episodes with pagination. Returns all episodes up to max_pages."""
    all_episodes = []
    next_key = None
    for page in range(max_pages):
        episodes, next_key = search_episodes(token, keyword, limit=20, loadMoreKey=next_key)
        all_episodes.extend(episodes)
        if not next_key or not episodes:
            break
    return all_episodes


def get_episode_detail(token: str, eid: str) -> dict:
    """Get episode detail by eid."""
    result = api("/episode_detail", token, {"eid": eid})
    return result.get("data", {}).get("data", {})  # type: ignore[no-any-return]


def get_episode_list(token: str, pid: str, count: int = 5, loadMoreKey: Optional[dict] = None) -> tuple:
    """Get recent episodes of a podcast. Returns (episodes, next_loadMoreKey)."""
    payload: dict = {"pid": pid, "order": "desc"}
    if loadMoreKey:
        payload["loadMoreKey"] = loadMoreKey
    result = api("/episode_list", token, payload)
    episodes = result.get("data", {}).get("data", [])  # type: ignore[assignment]
    next_key = result.get("data", {}).get("loadMoreKey")
    return episodes[:count], next_key  # type: ignore[no-any-return]


def get_all_episodes(token: str, pid: str, max_pages: int = 50) -> list:
    """Get all episodes of a podcast with pagination."""
    all_episodes = []
    next_key = None
    for page in range(max_pages):
        episodes, next_key = get_episode_list(token, pid, count=50, loadMoreKey=next_key)
        all_episodes.extend(episodes)
        if not next_key or not episodes:
            break
        print(f"  分页 {page+1}: 已获取 {len(all_episodes)} 集...")
    return all_episodes


def search_podcasts(token: str, keyword: str, limit: int = 5, loadMoreKey: Optional[dict] = None) -> tuple:
    """Search podcasts by keyword. Returns (podcasts, next_loadMoreKey)."""
    payload: dict = {"keyword": keyword, "type": "PODCAST"}
    if loadMoreKey:
        payload["loadMoreKey"] = loadMoreKey
    result = api("/search", token, payload)
    podcasts = []
    for item in result.get("data", {}).get("data", []):
        if item.get("type") == "PODCAST":
            podcasts.append(item)
    next_key = result.get("data", {}).get("loadMoreKey")
    return podcasts[:limit], next_key


def search_all_podcasts(token: str, keyword: str, max_pages: int = 5) -> list:
    """Search podcasts with pagination. Returns all podcasts up to max_pages."""
    all_podcasts = []
    next_key = None
    for page in range(max_pages):
        podcasts, next_key = search_podcasts(token, keyword, limit=20, loadMoreKey=next_key)
        all_podcasts.extend(podcasts)
        if not next_key or not podcasts:
            break
    return all_podcasts


def get_podcast_detail(token: str, pid: str) -> dict:
    """Get podcast detail."""
    result = api("/podcast_detail", token, {"pid": pid})
    return result.get("data", {}).get("data", {})  # type: ignore[no-any-return]


def show_podcast_info(token: str, keyword: str) -> None:
    """Search and display podcast info for finding PIDs."""
    podcasts, _ = search_podcasts(token, keyword)
    if not podcasts:
        print(f"未找到与 '{keyword}' 相关的播客")
        return

    print(f"\n找到 {len(podcasts)} 个播客:\n")
    for i, p in enumerate(podcasts):
        pid = p.get("pid", "?")
        title = p.get("title", "未知")
        sub_count = p.get("subscriptionCount", 0)
        ep_count = p.get("episodeCount", 0)
        author = p.get("author", "")
        print(f"  {i+1}. {title}")
        if author:
            print(f"     作者: {author}")
        print(f"     PID: {pid}")
        print(f"     订阅: {sub_count:,} | 集数: {ep_count}")
        print()


def list_episodes(token: str, pid: str, count: int = 10) -> None:
    """List recent episodes of a podcast."""
    episodes, _ = get_episode_list(token, pid, count)
    if not episodes:
        print(f"播客 {pid} 没有单集")
        return

    print(f"\n播客 {pid} 最近 {len(episodes)} 集:\n")
    for i, ep in enumerate(episodes):
        eid = ep.get("eid", "?")
        title = ep.get("title", "未知")
        pub_date = ep.get("pubDate", "")[:10]
        duration = ep.get("duration", 0)
        mins, secs = divmod(duration, 60)
        play_count = ep.get("playCount", 0)
        print(f"  {i+1}. {title}")
        print(f"     EID: {eid} | 日期: {pub_date} | 时长: {int(mins)}:{int(secs):02d}")
        if play_count:
            print(f"     播放: {play_count:,}")
        print()


# --- Audio Processing ---

def download_audio(url: str, output_path: Path, max_retries: int = 3) -> Path:
    """Download audio file with retry."""
    import urllib.error
    import urllib.request

    output_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"  下载音频: {url[:80]}...")
    for attempt in range(1, max_retries + 1):
        try:
            tmp_path = output_path.with_suffix(output_path.suffix + ".part")
            request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(request, timeout=DOWNLOAD_TIMEOUT_SEC) as resp:
                with open(tmp_path, "wb") as f:
                    shutil.copyfileobj(resp, f)
            tmp_path.replace(output_path)
            size_mb = output_path.stat().st_size / 1024 / 1024
            print(f"  已下载: {size_mb:.1f} MB")
            return output_path
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            if output_path.exists():
                output_path.unlink()
            part_path = output_path.with_suffix(output_path.suffix + ".part")
            if part_path.exists():
                part_path.unlink()
            if attempt < max_retries:
                print(f"  下载失败 (尝试 {attempt}/{max_retries}): {e}，重试...")
            else:
                raise AudioError(f"下载音频失败 ({max_retries} 次尝试): {e}")
    raise AudioError(f"下载音频失败: 未预期流程")


def convert_to_wav(input_path: Path, output_path: Path) -> Path:
    """Convert audio to WAV 16kHz mono using ffmpeg."""
    if not shutil.which("ffmpeg"):
        raise DependencyError("ffmpeg 未安装，请运行: brew install ffmpeg")
    print("  转换为 WAV 16kHz...")
    cmd = [
        "ffmpeg", "-y", "-i", str(input_path),
        "-ar", "16000", "-ac", "1", "-f", "wav", str(output_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise AudioError(f"ffmpeg 错误: {result.stderr[:200]}")
    return output_path


def get_duration_sec(wav_path: Path) -> float:
    """Get WAV duration in seconds using ffmpeg."""
    result = subprocess.run(
        ["ffmpeg", "-i", str(wav_path)],
        capture_output=True, text=True,
    )
    for line in result.stderr.splitlines():
        if "Duration:" in line:
            # Duration: 01:30:45.12, ...
            part = line.split("Duration:")[1].split(",")[0].strip()
            h, m, s = part.split(":")
            return float(h) * 3600 + float(m) * 60 + float(s)
    raise AudioError(f"无法获取音频时长: {wav_path}")


def split_audio(wav_path: Path, output_dir: Path) -> list[Path]:
    """Split audio at silence boundaries if > MAX_SEGMENT_SEC."""
    duration = get_duration_sec(wav_path)
    if duration <= MAX_SEGMENT_SEC:
        print(f"  音频时长: {duration:.0f}s ({duration/60:.1f}min), 无需分割")
        return [wav_path]

    print(f"  音频时长: {duration:.0f}s ({duration/60:.1f}min), 需要分割")

    # Detect silence points
    result = subprocess.run(
        ["ffmpeg", "-i", str(wav_path),
         "-af", "silencedetect=noise=-30dB:d=2",
         "-f", "null", "-"],
        capture_output=True, text=True,
    )

    ends = re.findall(r"silence_end:\s*([\d.]+)", result.stderr)
    MIN_SEGMENT_SEC = 60
    split_times: list[float] = []
    for t in ends:
        sec = float(t)
        if sec < MIN_SEGMENT_SEC or sec >= duration - 1:
            continue
        if not split_times or sec - split_times[-1] >= MAX_SEGMENT_SEC * 0.8:
            split_times.append(sec)

    # Always fill gaps with evenly-spaced splits
    t = MAX_SEGMENT_SEC
    while t < duration:
        if not any(abs(t - s) < 60 for s in split_times):
            split_times.append(t)
        t += MAX_SEGMENT_SEC

    split_times.sort()

    print(f"  分割点: {[f'{t:.0f}s' for t in split_times]}")

    output_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-y", "-i", str(wav_path),
        "-f", "segment",
        "-segment_times", ",".join(f"{t:.3f}" for t in split_times),
        "-ar", "16000", "-ac", "1",
        str(output_dir / "seg_%03d.wav"),
    ]
    subprocess.run(cmd, capture_output=True, text=True, check=True)

    segments = sorted(output_dir.glob("seg_*.wav"))
    print(f"  分割为 {len(segments)} 个片段")
    return segments


# --- Tokenizer ---

def ensure_tokenizer(model_dir: str) -> None:
    """Build tokenizer.json from vocab.json + merges.txt if missing."""
    tok_path = Path(model_dir) / "tokenizer.json"
    if tok_path.exists():
        return
    print("  生成 tokenizer.json...")
    vocab_path = Path(model_dir) / "vocab.json"
    merges_path = Path(model_dir) / "merges.txt"
    config_path = Path(model_dir) / "tokenizer_config.json"
    if not all(p.exists() for p in [vocab_path, merges_path, config_path]):
        raise DependencyError(
            f"模型目录不完整，缺少 vocab.json / merges.txt / tokenizer_config.json: {model_dir}"
        )

    with open(vocab_path) as f:
        vocab_val = json.load(f)
    with open(merges_path) as f:
        merges_vec = [l for l in f.read().splitlines() if l and not l.startswith("#")]
    with open(config_path) as f:
        tok_cfg = json.load(f)

    added_tokens = []
    if "added_tokens_decoder" in tok_cfg:
        entries = sorted(
            [(int(k), v) for k, v in tok_cfg["added_tokens_decoder"].items()],
            key=lambda x: x[0],
        )
        for id_, v in entries:
            added_tokens.append({
                "id": id_, "content": v["content"],
                "single_word": False, "lstrip": False, "rstrip": False,
                "normalized": False, "special": v.get("special", False),
            })

    tokenizer_json = {
        "version": "1.0", "truncation": None, "padding": None,
        "added_tokens": added_tokens,
        "normalizer": {"type": "NFC"},
        "pre_tokenizer": {"type": "Sequence", "pretokenizers": [
            {"type": "Split", "pattern": {"Regex": "(?i:'s|'t|'re|'ve|'m|'ll|'d)|[^\\r\\n\\p{L}\\p{N}]?\\p{L}+|\\p{N}| ?[^\\s\\p{L}\\p{N}]+[\\r\\n]*|\\s*[\\r\\n]+|\\s+(?!\\S)|\\s+"}, "behavior": "Isolated", "invert": False},
            {"type": "ByteLevel", "add_prefix_space": False, "trim_offsets": False, "use_regex": False},
        ]},
        "post_processor": {"type": "ByteLevel", "add_prefix_space": False, "trim_offsets": False, "use_regex": False},
        "decoder": {"type": "ByteLevel", "add_prefix_space": False, "trim_offsets": False, "use_regex": False},
        "model": {"type": "BPE", "dropout": None, "unk_token": None,
                  "continuing_subword_prefix": "", "end_of_word_suffix": "",
                  "fuse_unk": False, "byte_fallback": False, "ignore_merges": False,
                  "vocab": vocab_val, "merges": merges_vec},
    }
    with open(tok_path, "w") as f:
        json.dump(tokenizer_json, f)
    print("  tokenizer.json 已生成")


# --- Transcription ---

_SENTENCE_END = frozenset("。！？.!?")

def stitch_segments(texts: list[str]) -> str:
    """Join segment texts, merging cut sentences at boundaries."""
    if len(texts) <= 1:
        return texts[0] if texts else ""
    result = [texts[0]]
    for text in texts[1:]:
        prev = result[-1]
        # If previous segment doesn't end with sentence punctuation, merge
        if prev and prev[-1] not in _SENTENCE_END:
            result[-1] = prev + text
        else:
            result.append(text)
    return "\n\n".join(result)


def transcribe_segment(wav_path: Path, model_dir: str, asr_bin: str) -> str:
    """Transcribe a single WAV segment using qwen3-asr-rs."""
    cmd = [asr_bin, model_dir, str(wav_path)]
    print(f"  转录: {wav_path.name}...")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
    except subprocess.TimeoutExpired:
        raise TranscriptionError(f"转录超时 (900s): {wav_path.name}")
    if result.returncode != 0:
        raise TranscriptionError(f"转录错误: {result.stderr[:200]}")
    lines = result.stdout.strip().splitlines()
    for line in lines:
        if line.startswith("Text     :"):
            return line[len("Text     :"):].strip()
    return result.stdout.strip()


def transcribe_segments(segments: list[Path], model_dir: str, asr_bin: str) -> tuple[str, list[tuple[str, float, float]]]:
    """Transcribe multiple segments. Returns (combined_text, segment_timings)."""
    texts = []
    timings = []
    total = len(segments)
    offset = 0.0
    for i, seg in enumerate(segments):
        pct = (i + 1) / total * 100
        print(f"  [{i+1}/{total}] ({pct:.0f}%)", end=" ")
        text = transcribe_segment(seg, model_dir, asr_bin)
        seg_dur = get_duration_sec(seg)
        if text:
            texts.append(text)
            timings.append((text, offset, offset + seg_dur))
        offset += seg_dur
    return stitch_segments(texts), timings


# --- Output ---

def format_output(episode: dict, transcript: str, _segment_timings: Optional[list] = None) -> str:
    """Format transcript as markdown."""
    title = episode.get("title", "未知标题")
    podcast = episode.get("podcast", {})
    podcast_title = podcast.get("title", "未知节目")
    pub_date = episode.get("pubDate") or ""
    duration = episode.get("duration") or 0
    mins, secs = divmod(duration, 60)
    play_count = episode.get("playCount") or 0

    lines = [
        f"# {title}",
        "",
        f"**节目**: {podcast_title}",
        f"**日期**: {pub_date[:10] if pub_date else '未知'}",
        f"**时长**: {int(mins)}分{int(secs)}秒",
    ]
    if play_count:
        lines.append(f"**播放量**: {play_count:,}")

    lines += [
        "",
        "---",
        "",
        "## 转录文本",
        "",
        transcript,
    ]
    return "\n".join(lines)


def _srt_time(sec: float) -> str:
    """Format seconds as SRT timestamp HH:MM:SS,mmm."""
    h, remainder = divmod(int(sec), 3600)
    m, s = divmod(remainder, 60)
    ms = int((sec % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def format_srt(episode: dict, transcript: str, segment_timings: Optional[list] = None) -> str:
    """Format transcript as SRT subtitles with segment-aware timestamps."""
    duration = episode.get("duration", 0)

    if segment_timings:
        # Use actual segment boundaries for accurate timestamps
        lines = []
        idx = 1
        for seg_text, seg_start, seg_end in segment_timings:
            sentences = re.split(r"(?<=[。！？\.\!])\s*", seg_text)
            sentences = [s.strip() for s in sentences if s.strip()]
            if not sentences:
                continue
            seg_dur = seg_end - seg_start
            total_chars = sum(len(s) for s in sentences)
            if total_chars == 0:
                continue
            char_offset = 0.0
            for sentence in sentences:
                char_frac = len(sentence) / total_chars
                s_start = seg_start + char_offset * seg_dur
                s_end = seg_start + (char_offset + char_frac) * seg_dur
                lines.append(f"{idx}\n{_srt_time(s_start)} --> {_srt_time(s_end)}\n{sentence}")
                idx += 1
                char_offset += char_frac
        return "\n\n".join(lines)

    # Fallback: estimate by evenly distributing across duration
    sentences = re.split(r"(?<=[。！？\.\!])\s*", transcript)
    sentences = [s.strip() for s in sentences if s.strip()]

    if not sentences or duration == 0:
        return f"1\n00:00:00,000 --> {_srt_time(duration)}\n{transcript}\n"

    time_per_sentence = duration / len(sentences)
    lines = []
    for i, sentence in enumerate(sentences):
        start_sec = i * time_per_sentence
        end_sec = (i + 1) * time_per_sentence
        lines.append(f"{i+1}\n{_srt_time(start_sec)} --> {_srt_time(end_sec)}\n{sentence}")
    return "\n\n".join(lines)


def format_txt(episode: dict, transcript: str, _segment_timings: Optional[list] = None) -> str:
    """Format transcript as plain text."""
    title = episode.get("title", "未知标题")
    podcast = episode.get("podcast", {})
    podcast_title = podcast.get("title", "未知节目")
    pub_date = episode.get("pubDate") or ""

    header = f"{title}"
    if podcast_title:
        header += f" | {podcast_title}"
    if pub_date:
        header += f" | {pub_date[:10]}"
    return f"{header}\n\n{transcript}"


def format_json(episode: dict, transcript: str, _segment_timings: Optional[list] = None) -> str:
    """Format transcript as JSON."""
    return json.dumps({
        "title": episode.get("title") or "",
        "podcast": (episode.get("podcast") or {}).get("title") or "",
        "date": (episode.get("pubDate") or "")[:10],
        "duration": episode.get("duration") or 0,
        "play_count": episode.get("playCount") or 0,
        "transcript": transcript,
    }, ensure_ascii=False, indent=2)


FORMATTERS = {
    "markdown": format_output,
    "srt": format_srt,
    "txt": format_txt,
    "json": format_json,
}


# --- Environment Check ---

def check_env(token: Optional[str] = None) -> bool:
    """Check all dependencies and report status. Returns True if all pass."""
    checks = []
    all_ok = True

    # 1. ffmpeg
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        checks.append(("ffmpeg", True, ffmpeg_path))
    else:
        checks.append(("ffmpeg", False, "未安装"))
        all_ok = False

    # 2. xyz API
    import urllib.request
    import urllib.error
    try:
        req = urllib.request.Request(
            f"{BASE_URL}/", method="GET",
        )
        with urllib.request.urlopen(req, timeout=3) as resp:
            checks.append(("xyz API", True, f"{BASE_URL} (响应 HTTP {resp.status})"))
    except urllib.error.HTTPError as e:
        checks.append(("xyz API", True, f"{BASE_URL} (响应 HTTP {e.code})"))
    except Exception:
        checks.append(("xyz API", False, f"{BASE_URL} (未响应)"))
        all_ok = False

    # 3. Access token
    actual_token = token or os.environ.get("XYZ_ACCESS_TOKEN")
    if actual_token:
        # Try to validate by searching
        try:
            api("/search", actual_token, {"keyword": "test", "type": "EPISODE"})
            checks.append(("Access Token", True, "有效"))
        except TokenExpiredError:
            checks.append(("Access Token", False, "已过期，需重新登录"))
            all_ok = False
        except ApiError:
            checks.append(("Access Token", False, "验证失败"))
            all_ok = False
    else:
        checks.append(("Access Token", False, "未设置 (XYZ_ACCESS_TOKEN 环境变量或 --token)"))
        all_ok = False

    # 4. Refresh token
    refresh = os.environ.get("XYZ_REFRESH_TOKEN") or load_config().get("refresh_token")
    if refresh:
        checks.append(("Refresh Token", True, "已设置"))
    else:
        checks.append(("Refresh Token", False, "未设置 (可选，用于自动续期)"))

    # 5. ASR binary
    asr_bin = _detect_asr_bin()
    if Path(asr_bin).exists() or shutil.which(asr_bin):
        checks.append(("qwen3-asr-rs", True, asr_bin))
    else:
        checks.append(("qwen3-asr-rs", False, f"未找到: {asr_bin}"))
        all_ok = False

    # 6. Model directory
    model_dir = _detect_model_dir()
    model_path = Path(model_dir)
    if model_path.exists():
        required_files = ["config.json", "vocab.json", "merges.txt"]
        if not (model_path / "tokenizer.json").exists():
            required_files.append("tokenizer_config.json")
        missing = [f for f in required_files if not (model_path / f).exists()]
        if not any(model_path.glob("*.safetensors")):
            missing.append("*.safetensors")
        if missing:
            checks.append(("ASR Model", False, f"模型不完整，缺少: {', '.join(missing)}"))
            all_ok = False
        else:
            tokenizer_ok = (model_path / "tokenizer.json").exists()
            note = "" if tokenizer_ok else " (tokenizer.json 将在首次运行时自动生成)"
            checks.append(("ASR Model", True, f"{model_dir}{note}"))
    else:
        checks.append(("ASR Model", False, f"目录不存在: {model_dir}"))
        all_ok = False

    # Print results
    print("\n=== 环境检查 ===\n")
    for name, ok, detail in checks:
        icon = "✓" if ok else "✗"
        print(f"  [{icon}] {name}: {detail}")

    print()
    if all_ok:
        print("所有检查通过，可以开始转录。")
    else:
        print("部分检查未通过，请根据上述提示修复。")

    return all_ok


# --- Cleanup ---

def cleanup_audio(m4a_path: Path, wav_path: Path, seg_dir: Path) -> None:
    """Clean up temporary audio files."""
    for p in [m4a_path, wav_path]:
        p.unlink(missing_ok=True)
    if seg_dir.exists():
        for f in seg_dir.iterdir():
            if f.is_file():
                f.unlink()
        try:
            seg_dir.rmdir()
        except OSError:
            pass  # not empty, leave it


# --- Main ---

def transcribe_episode(token: str, eid: str, model_dir: str, asr_bin: str, keep_audio: bool = False) -> tuple[dict, str, list]:
    """Transcribe a single episode. Returns (episode_meta, transcript_text, segment_timings)."""
    validate_asr_environment(model_dir, asr_bin)

    episode = get_episode_detail(token, eid)
    title = episode.get("title", "未知")
    print(f"\n单集: {title}")

    media = episode.get("media", {})
    audio_url = media.get("source", {}).get("url") or episode.get("enclosure", {}).get("url")
    if not audio_url:
        raise TranscriptionError("未找到音频链接")

    size_mb = media.get("size", 0) / 1024 / 1024
    print(f"音频: {size_mb:.1f} MB, {media.get('mimeType', 'unknown')}")

    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    safe_stem = episode_file_stem(episode, fallback=eid)
    m4a_path = AUDIO_DIR / f"{safe_stem}.m4a"
    wav_path = AUDIO_DIR / f"{safe_stem}.wav"
    seg_dir = AUDIO_DIR / f"{safe_stem}_segments"

    try:
        download_audio(audio_url, m4a_path)
        convert_to_wav(m4a_path, wav_path)
        segments = split_audio(wav_path, seg_dir)

        ensure_tokenizer(model_dir)
        print("\n开始转录...")
        transcript, timings = transcribe_segments(segments, model_dir, asr_bin)
        return episode, transcript, timings
    finally:
        if not keep_audio:
            cleanup_audio(m4a_path, wav_path, seg_dir)


def run_transcription(args: argparse.Namespace) -> str:
    """Core transcription logic. Returns formatted output. Raises on error."""
    token = resolve_setting(args.token, "XYZ_ACCESS_TOKEN", "token") or ""
    if not token:
        raise ApiError("需要 access token (--login 登录, 或设置 --token / XYZ_ACCESS_TOKEN)")

    model_dir = resolve_setting(args.model_dir, "QWEN3_ASR_MODEL_DIR", "model_dir") or _detect_model_dir()
    asr_bin = resolve_setting(args.asr_bin, "QWEN3_ASR_BIN", "asr_bin") or _detect_asr_bin()
    fmt = args.format or "markdown"
    formatter = FORMATTERS.get(fmt)
    if not formatter:
        raise TranscriptionError(f"不支持的格式: {fmt}，可选: {', '.join(FORMATTERS.keys())}")

    # Batch mode: --pid + --count
    if args.pid:
        count = args.count or 3
        print(f"批量转录播客 {args.pid} 最近 {count} 集...")
        episodes_meta, _ = get_episode_list(token, args.pid, count)
        if not episodes_meta:
            raise TranscriptionError(f"播客 {args.pid} 没有可转录的单集")

        # Checkpoint: skip already-transcribed episodes
        out_dir = Path(args.output) if args.output else None
        skipped = 0
        if out_dir and (out_dir.is_dir() or not out_dir.suffix):
            ext = output_extension(fmt)
            remaining = []
            for ep in episodes_meta:
                safe = episode_file_stem(ep, fallback=ep.get("eid", "ep-unknown"))
                ep_path = out_dir / f"{safe}.{ext}"
                if ep_path.exists() and ep_path.stat().st_size > 0:
                    print(f"  跳过 (已存在): {ep.get('title', '?')}")
                    skipped += 1
                else:
                    remaining.append(ep)
            episodes_meta = remaining
            if skipped:
                print(f"  断点续传: 跳过 {skipped} 个已完成，剩余 {len(episodes_meta)} 个")

        if not episodes_meta:
            print("所有单集已完成转录。")
            return ""

        results = []
        for i, ep in enumerate(episodes_meta):
            eid = ep.get("eid")
            if not eid:
                print(f"  跳过 (缺少 EID): {ep.get('title', '?')}")
                continue
            print(f"\n{'='*40}")
            print(f"批量进度: [{i+1+skipped}/{count}]")
            print(f"{'='*40}")
            episode, transcript, timings = transcribe_episode(
                token, eid, model_dir, asr_bin, args.keep_audio,
            )
            output = formatter(episode, transcript, timings)
            results.append((episode, output))

            if out_dir:
                if out_dir.is_dir() or not out_dir.suffix:
                    out_dir.mkdir(parents=True, exist_ok=True)
                    safe = episode_file_stem(episode, fallback=str(eid) or f"ep{i}")
                    ext = output_extension(fmt)
                    ep_path = out_dir / f"{safe}.{ext}"
                    ep_path.write_text(output, encoding="utf-8")
                    print(f"  已保存: {ep_path}")

        return "\n\n---\n\n".join(r[1] for r in results)

    # Single episode mode
    if args.eid:
        eid = args.eid
    elif getattr(args, "url", None):
        eid = extract_episode_id_from_url(args.url)
    elif args.keyword:
        print(f"搜索: {args.keyword}")
        episodes, _ = search_episodes(token, args.keyword)
        if not episodes:
            raise TranscriptionError(f"未找到与 '{args.keyword}' 相关的单集")
        print(f"找到 {len(episodes)} 个单集，选择第一个:")
        print(f"  {episodes[0].get('title', '?')}")
        eid = episodes[0]["eid"]
    else:
        raise TranscriptionError("需要 --eid、--url、--keyword 或 --pid")

    episode, transcript, timings = transcribe_episode(
        token, eid, model_dir, asr_bin, args.keep_audio,
    )
    return formatter(episode, transcript, timings)


def main():
    parser = argparse.ArgumentParser(description="小宇宙播客转录工具")
    parser.add_argument("--token", help="x-jike-access-token (或设置 XYZ_ACCESS_TOKEN)")
    parser.add_argument("--keyword", help="搜索关键词")
    parser.add_argument("--eid", help="单集 ID (可替代关键词搜索)")
    parser.add_argument("--url", help="小宇宙单集链接 (可替代 --eid)")
    parser.add_argument("--pid", help="播客 ID (批量模式，配合 --count)")
    parser.add_argument("--podcast-info", action="store_true", help="搜索播客并显示 PID 等信息")
    parser.add_argument("--list-episodes", action="store_true", help="列出播客最近单集 (配合 --pid)")
    parser.add_argument("--count", type=int, default=3, help="批量转录集数 (默认 3)")
    parser.add_argument("--model-dir", help="Qwen3-ASR 模型目录 (或设置 QWEN3_ASR_MODEL_DIR)")
    parser.add_argument("--asr-bin", help="qwen3-asr-rs local_transcribe 路径 (或设置 QWEN3_ASR_BIN)")
    parser.add_argument("--format", choices=["markdown", "srt", "txt", "json"], default="markdown",
                        help="输出格式 (默认 markdown)")
    parser.add_argument("--output", "-o", help="输出文件/目录路径 (默认 stdout)")
    parser.add_argument("--keep-audio", action="store_true", help="保留下载的音频文件")
    parser.add_argument("--check-env", action="store_true", help="检查所有依赖是否就绪")
    parser.add_argument("--login", action="store_true", help="交互式登录并保存 token")
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    args = parser.parse_args()

    try:
        if args.check_env:
            token = resolve_setting(args.token, "XYZ_ACCESS_TOKEN", "token")
            ok = check_env(token)
            sys.exit(0 if ok else 1)

        if args.login:
            do_login(BASE_URL)
            return

        if args.podcast_info:
            if not args.keyword:
                parser.error("--podcast-info 需要配合 --keyword 指定搜索关键词")
            token = resolve_setting(args.token, "XYZ_ACCESS_TOKEN", "token") or ""
            if not token:
                raise ApiError("需要 access token (--token 或 XYZ_ACCESS_TOKEN 环境变量)")
            show_podcast_info(token, args.keyword)
            return

        if args.list_episodes:
            if not args.pid:
                parser.error("--list-episodes 需要配合 --pid 指定播客 ID")
            token = resolve_setting(args.token, "XYZ_ACCESS_TOKEN", "token") or ""
            if not token:
                raise ApiError("需要 access token (--token 或 XYZ_ACCESS_TOKEN 环境变量)")
            list_episodes(token, args.pid, args.count or 10)
            return

        if not args.eid and not args.url and not args.keyword and not args.pid:
            parser.error("需要 --eid、--url、--keyword 或 --pid (或使用 --check-env / --podcast-info)")

        output = run_transcription(args)

        if args.output:
            out_path = Path(args.output)
            # Batch mode already handles per-file saving
            if not (args.pid and (out_path.is_dir() or not out_path.suffix)):
                Path(args.output).write_text(output, encoding="utf-8")
                print(f"\n已保存到: {args.output}")
        else:
            print("\n" + output)

        print("\n完成!")
    except TranscriptionError as e:
        print(f"\n错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
