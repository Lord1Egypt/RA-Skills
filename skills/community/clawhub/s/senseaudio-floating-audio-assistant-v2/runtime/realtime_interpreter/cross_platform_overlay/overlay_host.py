#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import threading
import time
from datetime import datetime
from pathlib import Path

import webview

try:
    from AppKit import NSPasteboard, NSPasteboardTypeString
except Exception:  # pragma: no cover
    NSPasteboard = None
    NSPasteboardTypeString = None


ROOT = Path(__file__).resolve().parent
INTERPRETER_DIR = ROOT.parent
WORKSPACE_DIR = INTERPRETER_DIR.parent.parent
REPO_DIR = WORKSPACE_DIR.parent
DIST_DIR = ROOT / "dist"
INDEX_HTML = DIST_DIR / "index.html"
STATE_FILE = ROOT / ".overlay_window_state.json"
RUNS_DIR = WORKSPACE_DIR / "state" / "realtime_interpreter" / "runs"
CLIPBOARD_DIR = WORKSPACE_DIR / "state" / "realtime_interpreter" / "clipboard"
ENV_FILE = WORKSPACE_DIR / ".env"
SESSION_LOG = WORKSPACE_DIR / "state" / "realtime_interpreter" / "session.log"
RUNNER_CONFIG = INTERPRETER_DIR / "config.example.json"

VOICE_OPTIONS = [
    {"id": "female_0006_a", "label": "女声 A"},
    {"id": "male_0004_a", "label": "男声 A"},
    {"id": "male_0018_a", "label": "男声 B"},
]


def load_window_state():
    if not STATE_FILE.exists():
        return None
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return None


def save_window_state(window):
    try:
        STATE_FILE.write_text(
            json.dumps(
                {
                    "x": window.x,
                    "y": window.y,
                    "width": window.width,
                    "height": window.height,
                    "voice_id": getattr(window, "_audioclaw_voice_id", VOICE_OPTIONS[0]["id"]),
                },
                indent=2,
            ),
            encoding="utf-8",
        )
    except Exception:
        pass


def state_int(state: dict, key: str, default: int) -> int:
    value = state.get(key, default)
    try:
        if value is None:
            return default
        return int(value)
    except Exception:
        return default


def clamped_window_value(value: int, *, minimum: int, maximum: int) -> int:
    return max(minimum, min(maximum, value))


def build_parser():
    parser = argparse.ArgumentParser(description="Launch React overlay in a desktop host.")
    parser.add_argument("--debug", action="store_true")
    return parser


def current_clipboard_text() -> str:
    if NSPasteboard is None:
        return ""
    try:
        pb = NSPasteboard.generalPasteboard()
        return (pb.stringForType_(NSPasteboardTypeString) or "").strip()
    except Exception:
        return ""


def summarize_title(run_dir: Path) -> str:
    txt_file = run_dir / "senseaudio_asr.txt"
    if txt_file.exists():
        text = txt_file.read_text(encoding="utf-8", errors="ignore").strip()
        if text:
            first = text.splitlines()[0].strip()
            return first[:26]
    return run_dir.name


def format_time(value: float) -> str:
    return datetime.fromtimestamp(value).strftime("%H:%M")


def recent_projects(limit: int = 6):
    if not RUNS_DIR.exists():
        return []

    run_dirs = sorted(
        [path for path in RUNS_DIR.iterdir() if path.is_dir()],
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    projects = []
    for run_dir in run_dirs[:limit]:
        transcript_json = run_dir / "senseaudio_asr.json"
        if not transcript_json.exists():
            continue
        notes_md = run_dir / "organized_notes.md"
        music_dir = run_dir / "music"
        state = "music_ready" if music_dir.exists() else ("organized" if notes_md.exists() else "draft")
        projects.append(
            {
                "id": run_dir.name,
                "title": summarize_title(run_dir),
                "updatedAt": format_time(run_dir.stat().st_mtime),
                "state": state,
            }
        )
    return projects


def run_subprocess(arguments: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        arguments,
        cwd=REPO_DIR,
        text=True,
        capture_output=True,
        check=False,
    )


def write_clipboard_file(prefix: str, text: str) -> Path:
    CLIPBOARD_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    target = CLIPBOARD_DIR / f"{prefix}_{stamp}.txt"
    target.write_text(text, encoding="utf-8")
    return target


def open_path(path: Path):
    subprocess.Popen(["open", str(path)], cwd=REPO_DIR)


class OverlayBridge:
    def __init__(self):
        state = load_window_state() or {}
        self.voice_id = state.get("voice_id", VOICE_OPTIONS[0]["id"])
        self.window = None
        self.runner_process: subprocess.Popen[str] | None = None
        self.runner_log_offset = 0
        self.last_status = "待命中"
        self.shutdown = False
        self.current_line = "React + Python 宿主桌面浮窗已连接本地项目能力"
        self.previous_line = "SenseAudio 已确认上一句字幕"
        self.poll_thread: threading.Thread | None = None

    def getInitialState(self):
        projects = recent_projects()
        selected = projects[0]["id"] if projects else None
        return {
            "status": self.last_status,
            "hover": False,
            "projectPanelOpen": False,
            "selectedProjectId": selected,
            "voiceId": self.voice_id,
            "voices": VOICE_OPTIONS,
            "previousLine": self.previous_line,
            "currentLine": self.current_line,
            "projects": projects,
        }

    def attach_window(self, window):
        self.window = window
        self.start_polling()

    def emit_state(self, patch: dict):
        if self.window is None:
            return
        payload = json.dumps(patch, ensure_ascii=False)
        script = f"""
        window.dispatchEvent(new CustomEvent('audioclaw:overlay-state', {{ detail: {payload} }}));
        """
        try:
            self.window.evaluate_js(script)
        except Exception:
            pass

    def start_polling(self):
        if self.poll_thread is not None:
            return

        def loop():
            while not self.shutdown:
                self.poll_runner_output()
                time.sleep(0.35)

        self.poll_thread = threading.Thread(target=loop, daemon=True)
        self.poll_thread.start()

    def poll_runner_output(self):
        if not SESSION_LOG.exists():
            return
        try:
            with SESSION_LOG.open("r", encoding="utf-8") as fh:
                fh.seek(self.runner_log_offset)
                lines = fh.readlines()
                self.runner_log_offset = fh.tell()
        except Exception:
            return

        for line in lines:
            line = line.strip()
            if not line:
                continue
            try:
                payload = json.loads(line)
            except Exception:
                continue
            original = (payload.get("original") or "").strip()
            if not original:
                continue
            self.previous_line = self.current_line
            self.current_line = original
            self.last_status = (
                "SenseAudio 终稿已更新"
                if payload.get("source") == "senseaudio"
                else "本地快字幕更新"
            )
            self.emit_state(
                {
                    "previousLine": self.previous_line,
                    "currentLine": self.current_line,
                    "status": self.last_status,
                }
            )

    def start_runner(self):
        if self.runner_process and self.runner_process.poll() is None:
            return
        SESSION_LOG.parent.mkdir(parents=True, exist_ok=True)
        SESSION_LOG.write_text("", encoding="utf-8")
        self.runner_log_offset = 0
        args = [
            sys.executable,
            str(INTERPRETER_DIR / "runner.py"),
            "--config",
            str(RUNNER_CONFIG),
            "--env-file",
            str(ENV_FILE),
            "--no-translation",
        ]
        self.runner_process = subprocess.Popen(
            args,
            cwd=INTERPRETER_DIR,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            text=True,
        )
        self.last_status = "正在连接 SenseAudio"
        self.emit_state({"status": self.last_status})

    def stop_runner(self):
        if self.runner_process and self.runner_process.poll() is None:
            self.runner_process.terminate()
            self.runner_process = None
            self.last_status = "已停止实时 ASR"
            self.emit_state({"status": self.last_status})

    def triggerSatellite(self, action: str):
        if action == "recent_projects":
            return
        if action == "start_asr":
            self.start_runner()
            return

        clipboard = current_clipboard_text()
        if not clipboard:
            return

        if action == "clipboard_process":
            text_file = write_clipboard_file("clipboard", clipboard)
            result = run_subprocess(
                [
                    sys.executable,
                    str(INTERPRETER_DIR / "organize_clipboard_text.py"),
                    "--text-file",
                    str(text_file),
                ]
            )
            if result.returncode == 0:
                for line in result.stdout.splitlines():
                    if line.strip().endswith(".md") and Path(line.strip()).exists():
                        open_path(Path(line.strip()))
                        break
            return

        if action == "clipboard_read":
            text_file = write_clipboard_file("clipboard_speak", clipboard)
            output_audio = text_file.with_suffix(f".{self.voice_id}.mp3")
            result = run_subprocess(
                [
                    sys.executable,
                    str(INTERPRETER_DIR / "senseaudio_tts_clipboard.py"),
                    "--text-file",
                    str(text_file),
                    "--env-file",
                    str(ENV_FILE),
                    "--voice-id",
                    self.voice_id,
                    "--output-audio",
                    str(output_audio),
                ]
            )
            if result.returncode == 0 and output_audio.exists():
                open_path(output_audio)
            return

        if action == "clipboard_music":
            text_file = write_clipboard_file("clipboard_music", clipboard)
            output_dir = text_file.with_suffix("")
            run_subprocess(
                [
                    sys.executable,
                    str(INTERPRETER_DIR / "generate_senseaudio_music.py"),
                    "--text-file",
                    str(text_file),
                    "--env-file",
                    str(ENV_FILE),
                    "--output-dir",
                    str(output_dir),
                ]
            )

    def triggerProjectAction(self, project_id: str, action: str):
        run_dir = RUNS_DIR / project_id
        transcript_json = run_dir / "senseaudio_asr.json"
        if not transcript_json.exists():
            return

        if action == "transcript":
            txt = run_dir / "senseaudio_asr.txt"
            open_path(txt if txt.exists() else transcript_json)
            return

        if action == "music":
            output_dir = run_dir / "music"
            run_subprocess(
                [
                    sys.executable,
                    str(INTERPRETER_DIR / "generate_senseaudio_music.py"),
                    "--transcript-json",
                    str(transcript_json),
                    "--env-file",
                    str(ENV_FILE),
                    "--output-dir",
                    str(output_dir),
                ]
            )
            return

        mode = "summary" if action == "organize" else "keywords"
        result = run_subprocess(
            [
                sys.executable,
                str(INTERPRETER_DIR / "organize_senseaudio_transcript.py"),
                "--transcript-json",
                str(transcript_json),
                "--mode",
                mode,
            ]
        )
        if result.returncode == 0:
            target_name = "organized_notes.md" if mode == "summary" else "keywords_notes.md"
            target = run_dir / target_name
            if target.exists():
                open_path(target)

    def setVoice(self, voice_id: str):
        self.voice_id = voice_id
        self.emit_state({"voiceId": voice_id})


def main():
    args = build_parser().parse_args()
    if not INDEX_HTML.exists():
        raise SystemExit(
            f"Missing built frontend at {INDEX_HTML}. Run `npm run build` in cross_platform_overlay first."
        )

    state = load_window_state() or {"width": 438, "height": 310}
    bridge = OverlayBridge()
    width = clamped_window_value(state_int(state, "width", 438), minimum=390, maximum=470)
    height = clamped_window_value(state_int(state, "height", 310), minimum=260, maximum=360)
    window = webview.create_window(
        "AudioClaw Overlay",
        INDEX_HTML.as_uri(),
        js_api=bridge,
        width=width,
        height=height,
        x=state_int(state, "x", 220) if "x" in state and state.get("x") is not None else None,
        y=state_int(state, "y", 160) if "y" in state and state.get("y") is not None else None,
        frameless=True,
        easy_drag=True,
        on_top=True,
        transparent=True,
        background_color="#000000",
    )
    window._audioclaw_voice_id = bridge.voice_id
    bridge.attach_window(window)

    def on_closed():
        bridge.shutdown = True
        bridge.stop_runner()
        window._audioclaw_voice_id = bridge.voice_id
        save_window_state(window)

    window.events.closed += on_closed
    webview.start(debug=args.debug)


if __name__ == "__main__":
    main()
