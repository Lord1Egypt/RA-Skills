#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import queue
import signal
import subprocess
import threading
import time
import tkinter as tk
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = SCRIPT_DIR.parents[1]
DEFAULT_CONFIG_PATH = SCRIPT_DIR / "config.example.json"
DEFAULT_ENV_PATH = WORKSPACE_ROOT / ".env"
LOG_PATH = WORKSPACE_ROOT / "state" / "realtime_interpreter" / "session.log"
OVERLAY_STATE_PATH = WORKSPACE_ROOT / "state" / "realtime_interpreter" / "overlay_state.json"
RUNNER_PATH = SCRIPT_DIR / "runner.py"
VENV_PYTHON = SCRIPT_DIR / ".venv" / "bin" / "python"


class RunnerController:
    def __init__(
        self,
        *,
        config_path: Path,
        env_path: Path,
        log_path: Path,
        event_queue: queue.Queue[tuple[str, Any]],
    ) -> None:
        self.config_path = config_path
        self.env_path = env_path
        self.log_path = log_path
        self.event_queue = event_queue
        self.process: subprocess.Popen[str] | None = None
        self.stdout_thread: threading.Thread | None = None
        self.wait_thread: threading.Thread | None = None
        self.log_offset = 0
        self.running = False
        self.translation_enabled = True

    def start(self, *, translation_enabled: bool) -> None:
        if self.running:
            return
        self.translation_enabled = translation_enabled
        self.log_offset = self.log_path.stat().st_size if self.log_path.exists() else 0
        command = [
            str(VENV_PYTHON if VENV_PYTHON.exists() else "python3"),
            "-u",
            str(RUNNER_PATH),
            "--config",
            str(self.config_path),
            "--env-file",
            str(self.env_path),
        ]
        if not translation_enabled:
            command.append("--no-translation")
        env = os.environ.copy()
        env.setdefault("PYTHONUNBUFFERED", "1")
        self.process = subprocess.Popen(
            command,
            cwd=str(WORKSPACE_ROOT.parent),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            env=env,
        )
        self.running = True
        self.event_queue.put(("runner_state", {"running": True, "status": "正在连接 SenseAudio"}))

        self.stdout_thread = threading.Thread(target=self._read_stdout, daemon=True)
        self.stdout_thread.start()

        self.wait_thread = threading.Thread(target=self._wait_for_exit, daemon=True)
        self.wait_thread.start()

    def stop(self) -> None:
        if not self.process or self.process.poll() is not None:
            self.running = False
            return
        self.event_queue.put(("runner_state", {"running": True, "status": "正在停止识别"}))
        with contextlib_suppress():
            self.process.send_signal(signal.SIGINT)

    def poll_log(self) -> None:
        if not self.log_path.exists():
            return
        current_size = self.log_path.stat().st_size
        if current_size < self.log_offset:
            self.log_offset = 0
        if current_size == self.log_offset:
            return

        with self.log_path.open("r", encoding="utf-8") as handle:
            handle.seek(self.log_offset)
            for raw_line in handle:
                line = raw_line.strip()
                if not line:
                    continue
                try:
                    payload = json.loads(line)
                except json.JSONDecodeError:
                    continue
                self.event_queue.put(("subtitle", payload))
            self.log_offset = handle.tell()

    def _read_stdout(self) -> None:
        assert self.process is not None
        assert self.process.stdout is not None
        for raw_line in self.process.stdout:
            line = raw_line.strip()
            if not line:
                continue
            if "[translation] disabled after startup failure:" in line:
                self.event_queue.put(
                    (
                        "runner_state",
                        {
                            "running": True,
                            "status": "双语流启动失败，已自动降级为原文字幕",
                        },
                    )
                )
            elif "connected_success" in line:
                self.event_queue.put(("runner_state", {"running": True, "status": "已连接，正在监听系统音频"}))
            elif "task_started" in line:
                self.event_queue.put(("runner_state", {"running": True, "status": "识别中"}))
            elif "task_failed" in line:
                self.event_queue.put(("runner_error", line))
            elif "[segment" in line:
                self.event_queue.put(("runner_state", {"running": True, "status": "收到新字幕"}))

    def _wait_for_exit(self) -> None:
        assert self.process is not None
        return_code = self.process.wait()
        self.running = False
        if return_code == 0:
            self.event_queue.put(("runner_state", {"running": False, "status": "已停止"}))
        else:
            self.event_queue.put(("runner_error", f"识别进程已退出，返回码 {return_code}"))


class contextlib_suppress:
    def __init__(self, *exceptions: type[BaseException]) -> None:
        self.exceptions = exceptions or (Exception,)

    def __enter__(self) -> None:
        return None

    def __exit__(self, exc_type, exc, tb) -> bool:
        return exc_type is not None and issubclass(exc_type, self.exceptions)


class OverlayApp:
    def __init__(self) -> None:
        self.event_queue: queue.Queue[tuple[str, Any]] = queue.Queue()
        self.controller = RunnerController(
            config_path=DEFAULT_CONFIG_PATH,
            env_path=DEFAULT_ENV_PATH,
            log_path=LOG_PATH,
            event_queue=self.event_queue,
        )

        self.root = tk.Tk()
        self.root.title("AudioClaw Subtitles")
        self.root.configure(bg="#06070a")
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-alpha", 0.94)

        self.translation_var = tk.BooleanVar(value=True)
        self.status_var = tk.StringVar(value="准备就绪")
        self.original_var = tk.StringVar(value="系统字幕浮层已就绪")
        self.translation_text_var = tk.StringVar(value="点击 Start 开始监听系统音频")
        self.meta_var = tk.StringVar(value="模式: 双语 | 输入: 系统输出 (BlackHole)")

        self.drag_start_x = 0
        self.drag_start_y = 0

        self._build_ui()
        self._restore_window_state()
        self.root.after(250, self._poll)
        self.root.protocol("WM_DELETE_WINDOW", self.shutdown)

    def _build_ui(self) -> None:
        self.root.geometry("960x180+180+72")

        outer = tk.Frame(self.root, bg="#06070a", highlightbackground="#303647", highlightthickness=1, bd=0)
        outer.pack(fill="both", expand=True)

        header = tk.Frame(outer, bg="#101521", height=42)
        header.pack(fill="x")
        header.bind("<ButtonPress-1>", self._start_drag)
        header.bind("<B1-Motion>", self._on_drag)

        pill = tk.Label(
            header,
            text="AUDIOCLAW LIVE",
            bg="#b7f55e",
            fg="#08110a",
            font=("SF Pro Display", 11, "bold"),
            padx=10,
            pady=4,
        )
        pill.pack(side="left", padx=(14, 10), pady=8)
        pill.bind("<ButtonPress-1>", self._start_drag)
        pill.bind("<B1-Motion>", self._on_drag)

        status = tk.Label(
            header,
            textvariable=self.status_var,
            bg="#101521",
            fg="#d7deea",
            font=("SF Pro Text", 12),
        )
        status.pack(side="left", pady=8)
        status.bind("<ButtonPress-1>", self._start_drag)
        status.bind("<B1-Motion>", self._on_drag)

        self.mode_button = tk.Button(
            header,
            text="双语 ON",
            command=self.toggle_translation_mode,
            bg="#1c2537",
            fg="#f3f7ff",
            activebackground="#263149",
            activeforeground="#ffffff",
            relief="flat",
            padx=12,
            pady=6,
            highlightthickness=0,
            bd=0,
        )
        self.mode_button.pack(side="right", padx=(0, 10), pady=8)

        self.close_button = tk.Button(
            header,
            text="Close",
            command=self.shutdown,
            bg="#7a1d2a",
            fg="#fff7f7",
            activebackground="#932236",
            activeforeground="#ffffff",
            relief="flat",
            padx=12,
            pady=6,
            highlightthickness=0,
            bd=0,
        )
        self.close_button.pack(side="right", padx=(0, 8), pady=8)

        self.start_button = tk.Button(
            header,
            text="Start",
            command=self.toggle_runner,
            bg="#0d8a68",
            fg="#f6fffd",
            activebackground="#0fa279",
            activeforeground="#ffffff",
            relief="flat",
            padx=14,
            pady=6,
            highlightthickness=0,
            bd=0,
        )
        self.start_button.pack(side="right", padx=(0, 8), pady=8)

        body = tk.Frame(outer, bg="#06070a", padx=24, pady=18)
        body.pack(fill="both", expand=True)

        self.original_label = tk.Label(
            body,
            textvariable=self.original_var,
            bg="#06070a",
            fg="#f7fafc",
            justify="left",
            anchor="w",
            wraplength=900,
            font=("SF Pro Display", 26, "bold"),
        )
        self.original_label.pack(fill="x", anchor="w")

        self.translation_label = tk.Label(
            body,
            textvariable=self.translation_text_var,
            bg="#06070a",
            fg="#a7bfd7",
            justify="left",
            anchor="w",
            wraplength=900,
            font=("SF Pro Text", 18),
            pady=8,
        )
        self.translation_label.pack(fill="x", anchor="w")

        meta = tk.Label(
            body,
            textvariable=self.meta_var,
            bg="#06070a",
            fg="#7f8aa3",
            justify="left",
            anchor="w",
            wraplength=900,
            font=("SF Pro Text", 12),
        )
        meta.pack(fill="x", anchor="w", pady=(6, 0))

    def toggle_runner(self) -> None:
        if self.controller.running:
            self.controller.stop()
            return
        self.original_var.set("正在接入系统音频")
        self.translation_text_var.set("请播放浏览器、播放器或会议应用中的音频")
        self.meta_var.set(
            f"模式: {'双语' if self.translation_var.get() else '原文'} | 输入: 系统输出 (BlackHole)"
        )
        self.controller.start(translation_enabled=self.translation_var.get())
        self.start_button.configure(text="Stop", bg="#934d13", activebackground="#aa5b1b")

    def toggle_translation_mode(self) -> None:
        next_value = not self.translation_var.get()
        self.translation_var.set(next_value)
        self.mode_button.configure(text="双语 ON" if next_value else "双语 OFF")
        self.meta_var.set(f"模式: {'双语' if next_value else '原文'} | 输入: 系统输出 (BlackHole)")
        if self.controller.running:
            self.status_var.set("正在切换模式")
            self.controller.stop()
            self.root.after(1200, lambda: self.controller.start(translation_enabled=self.translation_var.get()))
            self.start_button.configure(text="Stop", bg="#934d13", activebackground="#aa5b1b")

    def _poll(self) -> None:
        self.controller.poll_log()
        while True:
            try:
                event_name, payload = self.event_queue.get_nowait()
            except queue.Empty:
                break
            if event_name == "subtitle":
                self._apply_subtitle(payload)
            elif event_name == "runner_state":
                self._apply_runner_state(payload)
            elif event_name == "runner_error":
                self.status_var.set(str(payload))
                self.start_button.configure(text="Start", bg="#0d8a68", activebackground="#0fa279")
        self.root.after(250, self._poll)

    def _apply_subtitle(self, payload: dict[str, Any]) -> None:
        original = str(payload.get("original") or "").strip()
        translation = str(payload.get("translation") or "").strip()
        if original:
            self.original_var.set(original)
        else:
            self.original_var.set("已捕获音频，但本句未识别出文本")
        if translation:
            self.translation_text_var.set(translation)
            self.translation_label.configure(fg="#ffe8a3")
        else:
            if self.translation_var.get():
                self.translation_text_var.set("翻译结果暂未返回，正在继续监听")
            else:
                self.translation_text_var.set("原文字幕模式")
            self.translation_label.configure(fg="#a7bfd7")
        stamp = payload.get("emitted_at") or time.strftime("%Y-%m-%dT%H:%M:%S")
        self.meta_var.set(
            f"模式: {'双语' if self.translation_var.get() else '原文'} | 最近更新时间: {stamp} | 输入: 系统输出"
        )
        self.status_var.set("字幕已更新")

    def _apply_runner_state(self, payload: dict[str, Any]) -> None:
        status = str(payload.get("status") or "").strip()
        running = bool(payload.get("running"))
        if status:
            self.status_var.set(status)
        if running:
            self.start_button.configure(text="Stop", bg="#934d13", activebackground="#aa5b1b")
        else:
            self.start_button.configure(text="Start", bg="#0d8a68", activebackground="#0fa279")

    def _start_drag(self, event: tk.Event[Any]) -> None:
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def _on_drag(self, event: tk.Event[Any]) -> None:
        x = self.root.winfo_x() + event.x - self.drag_start_x
        y = self.root.winfo_y() + event.y - self.drag_start_y
        self.root.geometry(f"+{x}+{y}")
        self._save_window_state()

    def _restore_window_state(self) -> None:
        if not OVERLAY_STATE_PATH.exists():
            return
        try:
            payload = json.loads(OVERLAY_STATE_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return
        width = int(payload.get("width") or 960)
        height = int(payload.get("height") or 180)
        x = int(payload.get("x") or 180)
        y = int(payload.get("y") or 72)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _save_window_state(self) -> None:
        OVERLAY_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "x": self.root.winfo_x(),
            "y": self.root.winfo_y(),
            "width": self.root.winfo_width(),
            "height": self.root.winfo_height(),
        }
        OVERLAY_STATE_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def shutdown(self) -> None:
        self._save_window_state()
        self.controller.stop()
        self.root.after(600, self.root.destroy)

    def run(self) -> None:
        self.toggle_runner()
        self.root.mainloop()


def main() -> int:
    app = OverlayApp()
    app.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
