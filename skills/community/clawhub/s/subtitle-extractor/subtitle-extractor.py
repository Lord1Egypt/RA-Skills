#!/usr/bin/env python3
"""
subtitle-extractor.py — Subtitle Extractor
Extracts native subtitles or Whisper transcription from video platforms.
Outputs raw subtitle file path + basic metadata; agent handles naming/analysis (see SKILL.md).

Usage: python subtitle-extractor.py <url|file> [--lang <code>] [--transcribe] [--cookies <file>]
"""

import argparse
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Force UTF-8 for stdout and stderr on all platforms.
# On Windows the default is GBK/cp936, which cannot encode many Unicode characters.
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


# ANSI colors — auto-disabled when stderr is not a tty (e.g. captured by agent)
def _c(code):
    return f'\033[{code}m' if sys.stderr.isatty() else ''

RED    = _c('0;31'); GREEN  = _c('0;32'); YELLOW = _c('1;33')
BLUE   = _c('0;34'); CYAN   = _c('0;36'); NC     = _c('0')


def eprint(*args, **kwargs):
    """Print to stderr (status / error messages — not captured by agent)."""
    print(*args, file=sys.stderr, **kwargs)


# ---------------------------------------------------------------------------

def detect_platform(url):
    if re.search(r'youtube\.com|youtu\.be', url):         return 'youtube'
    if re.search(r'bilibili\.com|b23\.tv', url):          return 'bilibili'
    if re.search(r'xiaohongshu\.com|xhslink\.com', url):  return 'xiaohongshu'
    if re.search(r'douyin\.com', url):                    return 'douyin'
    if Path(url).is_file():                               return 'local'
    return 'unknown'


# ---------------------------------------------------------------------------

def find_bilibili_cookies(cookie_file):
    """
    If cookie_file is already a valid path, return it.
    Otherwise scan the skill directory for any .txt file whose name contains 'bilibili'.
    Returns absolute path string, or empty string if not found.
    """
    if cookie_file and Path(cookie_file).is_file():
        return str(Path(cookie_file).resolve())

    skill_dir = Path(__file__).parent.resolve()

    # Prefer exact name first, then scan all .txt files for 'bilibili' in the filename
    candidate = skill_dir / 'bilibili_cookies.txt'
    if candidate.is_file():
        eprint(f'{CYAN}找到 Bilibili Cookie: {candidate}{NC}')
        return str(candidate.resolve())

    for f in sorted(skill_dir.glob('*.txt')):
        if 'bilibili' in f.name.lower():
            eprint(f'{CYAN}找到 Bilibili Cookie: {f}{NC}')
            return str(f.resolve())

    return ''


# ---------------------------------------------------------------------------

def _check_faster_whisper():
    """Raise RuntimeError if faster-whisper is not importable."""
    try:
        import faster_whisper  # noqa: F401
    except ImportError:
        raise RuntimeError('faster-whisper 未安装。请运行: pip install faster-whisper')


def _fmt_srt_time(seconds):
    h  = int(seconds // 3600)
    m  = int((seconds % 3600) // 60)
    s  = int(seconds % 60)
    ms = int(round((seconds % 1) * 1000))
    return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'


def _segments_to_srt(segments):
    """Convert faster-whisper segment iterator to SRT format string."""
    lines = []
    for i, seg in enumerate(segments, 1):
        lines.append(str(i))
        lines.append(f'{_fmt_srt_time(seg.start)} --> {_fmt_srt_time(seg.end)}')
        lines.append(seg.text.strip())
        lines.append('')
    return '\n'.join(lines)


# ---------------------------------------------------------------------------

def get_metadata(url, cookie_file):
    """Fetch title and uploader via yt-dlp --print. Returns (title, author)."""
    cmd = ['yt-dlp']
    if cookie_file:
        cmd += ['--cookies', cookie_file]
    cmd += ['--print', '%(title)s', '--print', '%(uploader)s', '--skip-download', url]

    result = subprocess.run(cmd, capture_output=True, encoding='utf-8', errors='replace')
    lines = result.stdout.strip().splitlines()

    title  = lines[0].strip() if len(lines) > 0 else ''
    author = lines[1].strip() if len(lines) > 1 else ''

    return (title  if title  and title  != 'NA' else 'Unknown',
            author if author and author != 'NA' else 'Unknown')


# ---------------------------------------------------------------------------

def _find_sub_file(directory):
    """Return first subtitle file found in directory tree, or None."""
    for ext in ('*.srt', '*.vtt', '*.ass'):
        matches = list(Path(directory).rglob(ext))
        if matches:
            return matches[0]
    return None


def extract_bilibili_subtitles(url, lang, cookie_file):
    """
    Extract Bilibili subtitles with language fallback (zh-CN → ai-zh).
    Returns subtitle text, or empty string if not found.
    Raises RuntimeError on 412 (cookie expired).
    """
    base_cmd = ['yt-dlp']
    if cookie_file:
        base_cmd += ['--cookies', cookie_file]

    lang_priority = []
    if lang != 'auto':
        lang_priority.append(lang)
    lang_priority += ['zh-CN', 'ai-zh']

    for try_lang in lang_priority:
        eprint(f'{BLUE}尝试字幕语言: {try_lang}{NC}')

        with tempfile.TemporaryDirectory() as tmp_dir:
            result = subprocess.run(
                base_cmd + [
                    '--write-sub', '--write-auto-sub',
                    '--sub-lang', try_lang,
                    '--skip-download',
                    '-P', tmp_dir,
                    url,
                ],
                capture_output=True, encoding='utf-8', errors='replace'
            )

            if '412' in result.stderr or 'Precondition Failed' in result.stderr:
                raise RuntimeError(
                    'Bilibili 412 错误：Cookie 已过期。\n'
                    '请重新导出 → 命名为 bilibili_cookies.txt → 放于脚本目录或 ~/Downloads'
                )

            sub_file = _find_sub_file(tmp_dir)
            if sub_file:
                eprint(f'{GREEN}找到字幕: {try_lang}{NC}')
                return sub_file.read_text(encoding='utf-8', errors='replace')

    # List available subtitles for user reference
    eprint(f'{YELLOW}未找到中文字幕，可用字幕列表：{NC}')
    result = subprocess.run(
        base_cmd + ['--list-subs', '--skip-download', url],
        capture_output=True, encoding='utf-8', errors='replace'
    )
    for line in (result.stdout + result.stderr).splitlines():
        if not line.startswith('[debug]'):
            eprint(line)
    eprint(f'{YELLOW}请使用 --lang <语言代码> 指定字幕{NC}')
    return ''


def extract_subtitles(url, lang, cookie_file):
    """Generic subtitle extraction via yt-dlp (YouTube, etc.)."""
    cmd = ['yt-dlp']
    if cookie_file:
        cmd += ['--cookies', cookie_file]
    if lang != 'auto':
        cmd += ['--sub-lang', lang]

    eprint(f'{BLUE}正在提取字幕...{NC}')

    with tempfile.TemporaryDirectory() as tmp_dir:
        subprocess.run(
            cmd + ['--write-sub', '--write-auto-sub', '--skip-download', '-P', tmp_dir, url],
            capture_output=True, encoding='utf-8', errors='replace'
        )
        sub_file = _find_sub_file(tmp_dir)
        if sub_file:
            return sub_file.read_text(encoding='utf-8', errors='replace')

    eprint(f'{YELLOW}未找到字幕{NC}')
    return ''


# ---------------------------------------------------------------------------

def _resolve_model_path(model_size):
    """
    Resolve Whisper model path.
    Priority:
      1. VIDEO_SUMMARY_WHISPER_MODEL env var — if it points to an existing directory, use as local path
      2. {skill_dir}/models/whisper-{model_size}/ — local model placed next to the script
      3. Fall through to HuggingFace / mirror download
    Returns either an absolute path string (local) or the model_size string (for download).
    """
    env_val = os.environ.get('VIDEO_SUMMARY_WHISPER_MODEL', '')
    if env_val:
        p = Path(env_val)
        if p.is_dir() and (p / 'model.bin').is_file():
            eprint(f'{CYAN}使用本地模型（环境变量）: {p}{NC}')
            return str(p)
        if not p.is_dir():
            # treat as model size name, not a path
            return env_val

    skill_dir = Path(__file__).parent.resolve()
    local_model = skill_dir / 'models' / f'whisper-{model_size}'
    if local_model.is_dir() and (local_model / 'model.bin').is_file():
        eprint(f'{CYAN}使用本地模型: {local_model}{NC}')
        return str(local_model)

    return model_size  # fall back to download


def _download_via_modelscope(model_size, target_dir):
    """
    Try to download faster-whisper model from ModelScope (fastest in China).
    Returns True if model is ready at target_dir, False if modelscope is not installed.
    Raises RuntimeError on download failure.
    """
    try:
        from modelscope.hub.snapshot_download import snapshot_download  # noqa
    except ImportError:
        return False

    eprint(f'{BLUE}正在从 ModelScope 下载模型 faster-whisper-{model_size}（国内推荐，速度更快）...{NC}')
    target_dir.mkdir(parents=True, exist_ok=True)
    try:
        snapshot_download(
            f'pkufool/faster-whisper-{model_size}',
            local_dir=str(target_dir),
            ignore_file_pattern=['.gitattributes', 'README.md', '*.md'],
        )
        eprint(f'{GREEN}ModelScope 下载完成{NC}')
        return True
    except Exception as e:
        eprint(f'{YELLOW}ModelScope 下载失败: {e}，将尝试其他镜像...{NC}')
        return False


def _whisper_transcribe(audio_path, model_size):
    """Transcribe audio with faster-whisper. Returns SRT text."""
    from faster_whisper import WhisperModel

    model_path = _resolve_model_path(model_size)
    is_local = Path(model_path).is_dir()

    if is_local:
        eprint(f'{BLUE}正在加载本地 Whisper 模型: {model_path}（可能需要数秒）...{NC}')
        model = WhisperModel(model_path, device='cpu', compute_type='int8')
    else:
        skill_dir = Path(__file__).parent.resolve()
        local_model_dir = skill_dir / 'models' / f'whisper-{model_path}'

        # Force-enable HuggingFace Hub progress bars (disabled by default in non-tty)
        os.environ['HF_HUB_DISABLE_PROGRESS_BARS'] = '0'

        # Priority 1: ModelScope (most reliable in China, install: pip install modelscope)
        if _download_via_modelscope(model_path, local_model_dir):
            eprint(f'{BLUE}正在加载模型...{NC}')
            model = WhisperModel(str(local_model_dir), device='cpu', compute_type='int8')
        else:
            # Priority 2: HuggingFace mirrors
            mirrors = [
                'https://hf-mirror.com',
                'https://huggingface.co',
            ]
            model = None
            for mirror in mirrors:
                os.environ['HF_ENDPOINT'] = mirror
                try:
                    eprint(f'{BLUE}正在从 {mirror} 下载 Whisper 模型 ({model_path})，'
                           f'约 150MB，请耐心等待（如多次卡住建议 pip install modelscope）...{NC}')
                    model = WhisperModel(model_path, device='cpu', compute_type='int8')
                    eprint(f'{GREEN}模型加载完成{NC}')
                    break
                except Exception as e:
                    err_str = str(e)
                    if ('ConnectError' in err_str or 'LocalEntryNotFoundError' in type(e).__name__
                            or 'ConnectionError' in err_str or 'WinError 10054' in err_str
                            or 'RemoteDisconnected' in err_str):
                        eprint(f'{YELLOW}镜像 {mirror} 连接失败，尝试下一个...{NC}')
                        continue
                    raise  # non-network error, re-raise immediately

            if model is None:
                raise RuntimeError(
                    f'Whisper 模型下载失败（所有网络镜像均无法连接）。\n\n'
                    f'推荐方案（国内最快）：\n'
                    f'  pip install modelscope\n'
                    f'  然后重新运行脚本，将自动从 ModelScope 下载\n\n'
                    f'或手动下载后放置到：\n'
                    f'  {local_model_dir}\n\n'
                    f'手动下载步骤：\n'
                    f'  1. 用浏览器打开（国内可访问）：\n'
                    f'     https://modelscope.cn/models/pkufool/faster-whisper-{model_path}/files\n'
                    f'  2. 下载以下 5 个文件：\n'
                    f'     config.json  model.bin  tokenizer.json\n'
                    f'     vocabulary.json  preprocessor_config.json\n'
                    f'  3. 创建目录并放入：\n'
                    f'     {local_model_dir}\\\n'
                    f'  4. 重新运行脚本'
                )

    eprint(f'{BLUE}正在转写音频，CPU 模式下请耐心等待（base 模型 3 分钟视频约需 10~20 秒）...{NC}')
    segments, info = model.transcribe(audio_path)
    eprint(f'{BLUE}检测到语言: {info.language}，开始生成字幕...{NC}')
    srt = _segments_to_srt(segments)
    eprint(f'{GREEN}转写完成{NC}')
    return srt


def transcribe_video(url, cookie_file, model):
    """Download audio from URL and transcribe with faster-whisper."""
    cmd = ['yt-dlp']
    if cookie_file:
        cmd += ['--cookies', cookie_file]

    eprint(f'{BLUE}正在下载音频（yt-dlp），下载进度如下：{NC}')

    with tempfile.TemporaryDirectory() as tmp_dir:
        audio_template = str(Path(tmp_dir) / 'audio.%(ext)s')
        # Stream yt-dlp stderr so download progress is visible to the agent
        result = subprocess.run(
            cmd + ['-x', '--audio-format', 'mp3', '-o', audio_template, url],
            stdout=subprocess.PIPE,
            stderr=sys.stderr,
            encoding='utf-8', errors='replace'
        )
        if result.returncode != 0:
            raise RuntimeError('yt-dlp 音频下载失败（见上方错误输出）')

        audio_files = list(Path(tmp_dir).glob('audio.*'))
        if not audio_files:
            raise RuntimeError('yt-dlp 未生成音频文件')

        eprint(f'{GREEN}音频下载完成，开始 Whisper 转写（模型: {model}）...{NC}')
        return _whisper_transcribe(str(audio_files[0]), model)


def transcribe_local(file_path, model):
    """Transcribe a local video/audio file with faster-whisper."""
    eprint(f'{BLUE}正在转写本地文件（模型: {model}）...{NC}')
    return _whisper_transcribe(file_path, model)


# ---------------------------------------------------------------------------
# Step handlers
# ---------------------------------------------------------------------------

def run_download_audio(args, model):
    """
    --step download-audio
    Downloads audio from a URL to a persistent temp file.
    Stdout: {"audio_file": "...", "title": "...", "author": "...", "platform": "..."}
    """
    url      = args.input
    platform = detect_platform(url)
    eprint(f'{GREEN}Platform: {platform}{NC}')

    if platform == 'local':
        eprint(f'{RED}Error: --step download-audio 不支持本地文件，请直接使用 --step transcribe{NC}')
        sys.exit(1)

    # --- Cookie setup ---
    cookie_file = args.cookies
    if platform == 'bilibili':
        cookie_file = find_bilibili_cookies(cookie_file)
        if not cookie_file:
            eprint(f'{RED}Error: 未找到 Bilibili Cookie 文件{NC}')
            eprint(f'{YELLOW}请导出 Cookie 并命名为 bilibili_cookies.txt，放于脚本目录{NC}')
            sys.exit(1)

    # --- Metadata ---
    title, author = get_metadata(url, cookie_file)

    # --- Download audio to persistent temp file ---
    pid            = os.getpid()
    audio_template = str(Path(tempfile.gettempdir()) / f'video-summary-audio-{pid}.%(ext)s')

    cmd = ['yt-dlp']
    if cookie_file:
        cmd += ['--cookies', cookie_file]
    cmd += ['-x', '--audio-format', 'mp3', '-o', audio_template, url]

    eprint(f'{BLUE}正在下载音频（yt-dlp），下载进度如下：{NC}')
    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=sys.stderr,
        encoding='utf-8', errors='replace'
    )
    if result.returncode != 0:
        eprint(f'{RED}Error: yt-dlp 音频下载失败（见上方错误输出）{NC}')
        sys.exit(1)

    audio_files = list(Path(tempfile.gettempdir()).glob(f'video-summary-audio-{pid}.*'))
    if not audio_files:
        eprint(f'{RED}Error: yt-dlp 未生成音频文件{NC}')
        sys.exit(1)

    output = {
        'audio_file': str(audio_files[0]),
        'title':      title,
        'author':     author,
        'platform':   platform,
    }
    print(json.dumps(output, ensure_ascii=True))
    eprint(f'{GREEN}音频下载完成{NC}')


def run_transcribe(args, model):
    """
    --step transcribe
    Transcribes a local audio/video file with faster-whisper.
    Input: local file path (URL_OR_FILE positional arg).
    Stdout: {"subtitle_file": "..."}
    """
    audio_path = args.input

    if not Path(audio_path).is_file():
        eprint(f'{RED}Error: 文件不存在: {audio_path}{NC}')
        sys.exit(1)

    try:
        _check_faster_whisper()
        srt = _whisper_transcribe(audio_path, model)
    except RuntimeError as e:
        eprint(f'{RED}Error: {e}{NC}')
        sys.exit(1)

    sub_path = Path(tempfile.gettempdir()) / f'video-summary-{os.getpid()}.srt'
    sub_path.write_text(srt, encoding='utf-8')

    output = {'subtitle_file': str(sub_path)}
    print(json.dumps(output, ensure_ascii=True))
    eprint(f'{GREEN}转写完成{NC}')


def run_native_subtitle(args, model):
    """
    Default path (no --step): extract native subtitles via yt-dlp.
    Falls back to Whisper if no subtitles found.
    Stdout: {"title": "...", "author": "...", "platform": "...", "subtitle_file": "..."}
    """
    url      = args.input
    lang     = args.lang
    platform = detect_platform(url)
    eprint(f'{GREEN}Platform: {platform}{NC}')

    # --- Cookie setup ---
    cookie_file = args.cookies
    if platform == 'bilibili':
        cookie_file = find_bilibili_cookies(cookie_file)
        if not cookie_file:
            eprint(f'{RED}Error: 未找到 Bilibili Cookie 文件{NC}')
            eprint(f'{YELLOW}请导出 Cookie 并命名为 bilibili_cookies.txt，放于脚本目录{NC}')
            sys.exit(1)

    # --- Metadata ---
    if platform != 'local':
        title, author = get_metadata(url, cookie_file)
    else:
        title  = Path(url).name
        author = 'local'

    # --- Extract subtitles ---
    transcript = ''
    try:
        if platform in ('xiaohongshu', 'douyin', 'local'):
            _check_faster_whisper()
            if platform == 'local':
                transcript = transcribe_local(url, model)
            else:
                transcript = transcribe_video(url, cookie_file, model)

        elif platform == 'bilibili':
            transcript = extract_bilibili_subtitles(url, lang, cookie_file)
            if not transcript:
                eprint(f'{YELLOW}字幕提取失败，回退到 Whisper 转写...{NC}')
                _check_faster_whisper()
                transcript = transcribe_video(url, cookie_file, model)

        else:
            transcript = extract_subtitles(url, lang, cookie_file)
            if not transcript:
                eprint(f'{YELLOW}未找到字幕，回退到 Whisper 转写...{NC}')
                _check_faster_whisper()
                transcript = transcribe_video(url, cookie_file, model)

    except RuntimeError as e:
        eprint(f'{RED}Error: {e}{NC}')
        sys.exit(1)

    if not transcript:
        eprint(f'{RED}Error: 无法提取字幕{NC}')
        sys.exit(1)

    # --- Detect subtitle format ---
    first_line = transcript.splitlines()[0] if transcript.splitlines() else ''
    sub_ext = 'vtt' if first_line.startswith('WEBVTT') else 'srt'

    sub_path = Path(tempfile.gettempdir()) / f'video-summary-{os.getpid()}.{sub_ext}'
    sub_path.write_text(transcript, encoding='utf-8')

    output = {
        'title':         title,
        'author':        author,
        'platform':      platform,
        'subtitle_file': str(sub_path),
    }
    print(json.dumps(output, ensure_ascii=True))
    eprint(f'{GREEN}Done!{NC}')


# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        prog='subtitle-extractor',
        description='Subtitle extractor for Bilibili, YouTube, Xiaohongshu, Douyin, local files.'
    )
    parser.add_argument('input', metavar='URL_OR_FILE', help='Video URL or local file path')
    parser.add_argument('--step',    choices=['download-audio', 'transcribe'],
                        help='Run a single pipeline step (see SKILL.md)')
    parser.add_argument('--lang',    default='auto',
                        help='Subtitle language code, default path only (default: auto)')
    parser.add_argument('--cookies', default=os.environ.get('VIDEO_SUMMARY_COOKIES', ''),
                        help='Cookie file path (or set VIDEO_SUMMARY_COOKIES env var)')
    args = parser.parse_args()

    model = os.environ.get('VIDEO_SUMMARY_WHISPER_MODEL', 'base')

    if args.step == 'download-audio':
        run_download_audio(args, model)
    elif args.step == 'transcribe':
        run_transcribe(args, model)
    else:
        run_native_subtitle(args, model)


if __name__ == '__main__':
    main()
