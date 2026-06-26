"""
Real-time speech transcription using SenseVoice via FunASR.
Captures system audio (BlackHole) or microphone audio, transcribes in discrete windows.

Usage:
    python3 realtime_asr.py --source blackhole   # capture system audio
    python3 realtime_asr.py --source mic         # capture microphone audio
    python3 realtime_asr.py --list-devices       # list available audio devices
    Ctrl+C to stop
"""

import argparse
import contextlib
import datetime
import io
import os
import queue
import signal
import subprocess
import sys
import threading
import time
import numpy as np

# All dependencies required by this skill
REQUIRED_DEPS = {
    'sounddevice': 'PyAudio binding for microphone/system audio capture',
    'librosa':     'Audio resampling and preprocessing',
    'funasr':      'SenseVoice ASR model framework',
    'torch':       'PyTorch deep learning runtime',
    'numpy':       'Numerical array processing',
}

OPTIONAL_DEPS = {
    'pyyaml': 'YAML parsing (for skill.yaml validation)',
}


def check_deps():
    """Check all required dependencies and report status."""
    missing = []
    for pkg in REQUIRED_DEPS:
        try:
            __import__(pkg.replace('-', '_'))
        except ImportError:
            missing.append(pkg)
    return missing


def install_deps(packages=None):
    """Install missing dependencies one by one with progress output."""
    if packages is None:
        packages = check_deps()

    if not packages:
        print("  ✅ 所有依赖已安装，无需更新。\n")
        return

    total = len(packages)
    for i, pkg in enumerate(packages, 1):
        desc = REQUIRED_DEPS.get(pkg, '')
        print(f"  [{i}/{total}] 安装 {pkg}... {desc}")
        print(f"  ⏳ pip3 install {pkg} ", end="", flush=True)
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'install', '--quiet', pkg],
                capture_output=True, text=True, timeout=300
            )
            if result.returncode == 0:
                print(f"✅ 安装成功")
            else:
                print(f"❌ 安装失败")
                if result.stderr:
                    # Show last few lines of error
                    lines = result.stderr.strip().split('\n')
                    for line in lines[-3:]:
                        print(f"     {line}")
        except subprocess.TimeoutExpired:
            print("❌ 超时（300秒）")
        except Exception as e:
            print(f"❌ {e}")

    # Final check
    remaining = check_deps()
    if remaining:
        print(f"\n  ⚠️  仍有依赖未安装: {', '.join(remaining)}")
        print(f"  请手动运行: pip3 install {' '.join(remaining)}")
        return False
    print(f"\n  ✅ 所有依赖安装完成，可以开始使用转录技能。\n")
    return True


def import_deps():
    """Import all required dependencies after they've been installed."""
    import sounddevice as sd
    import librosa
    import torch
    with contextlib.redirect_stdout(io.StringIO()):
        from funasr import AutoModel
        from funasr.utils.postprocess_utils import rich_transcription_postprocess
    return sd, librosa, torch, AutoModel, rich_transcription_postprocess

TARGET_RATE = 16000          # SenseVoice expects 16kHz
DEVICE_RATE = 48000          # BlackHole native rate
CHANNELS = 2
CHUNK_SAMPLES = int(DEVICE_RATE * 1)  # 1-second chunks at device rate
TRANSCRIBE_INTERVAL = 3      # seconds between transcriptions
IDLE_TIMEOUT = 60            # seconds of silence before stopping (0 to disable)
AMPLITUDE_THRESHOLD = 0.01   # minimum amplitude to count as "sound"
EXIT_CODE_IDLE = 42          # exit code for idle timeout


def _strip_overlap(new_text: str, prev_text: str) -> str:
    """
    Remove text from new_text that was already output in prev_text.

    Uses LCS (Longest Common Subsequence) to detect if new_text is mostly
    a superset of prev_text (ASR recognizing the same audio with slight
    differences). If >80% of prev_text is in new_text, outputs only the
    genuinely new part.
    """
    if not prev_text or not new_text:
        return new_text

    m, n = len(prev_text), len(new_text)

    # Compute LCS length table
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if prev_text[i-1] == new_text[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    lcs_len = dp[m][n]
    overlap_ratio = lcs_len / m  # how much of prev is contained in new

    # If >80% of prev is in new, it's likely a superset/re-recognition
    if overlap_ratio > 0.8:
        # Backtrack to find LCS characters
        lcs_chars = []
        i, j = m, n
        while i > 0 and j > 0:
            if prev_text[i-1] == new_text[j-1]:
                lcs_chars.append(prev_text[i-1])
                i -= 1
                j -= 1
            elif dp[i-1][j] > dp[i][j-1]:
                i -= 1
            else:
                j -= 1
        lcs_chars.reverse()

        # Find last matched LCS character position in new_text
        last_pos = -1
        search_from = 0
        for c in lcs_chars:
            idx = new_text.find(c, search_from)
            if idx >= 0:
                last_pos = idx
                search_from = idx + 1

        if last_pos >= 0 and last_pos < len(new_text) - 1:
            return new_text[last_pos + 1:]
        elif last_pos == len(new_text) - 1:
            return ""

    return new_text


class StreamingTranscriber:
    def __init__(self, model_path: str, stream_kwargs: dict | None = None,
                 output_file: str = None, idle_timeout: int = IDLE_TIMEOUT):
        self.audio_queue: queue.Queue[np.ndarray] = queue.Queue()
        self.amplitude_queue: queue.Queue[float] = queue.Queue()
        self.buffer: list[np.ndarray] = []  # fresh audio chunks since last transcription
        self.stop_event = threading.Event()
        self.stream_kwargs = stream_kwargs or {}
        self.output_file = output_file
        self.output_lock = threading.Lock()
        self.idle_timeout = idle_timeout
        self._idle_timeout = False  # set True when idle timeout triggers
        self.prev_text = ""  # last transcription output, for overlap stripping

        # Clear output file on start
        if self.output_file:
            os.makedirs(os.path.dirname(self.output_file) or ".", exist_ok=True)
            with open(self.output_file, "w") as f:
                pass  # truncate

        print("Loading SenseVoice model ...", flush=True)
        with contextlib.redirect_stdout(io.StringIO()):
            self.asr_model = AutoModel(
                model=model_path,
                trust_remote_code=True,
                device="cpu",
                disable_update=True,
            )
        print("Model loaded. Listening ...\n", flush=True)

    def audio_callback(self, indata, frames, time_info, status):
        if status:
            print(f"\n⚠️  {status}", flush=True)
        # Mix stereo to mono
        mono = indata.mean(axis=1).astype(np.float32)
        # Track amplitude for idle detection
        self.amplitude_queue.put(float(np.abs(mono).max()))
        # Resample from device rate (48kHz) to target rate (16kHz)
        mono = librosa.resample(mono, orig_sr=DEVICE_RATE, target_sr=TARGET_RATE)
        self.audio_queue.put(mono.copy())

    def transcribe_buffer(self) -> str:
        """Transcribe accumulated buffer and clear it."""
        if not self.buffer:
            return ""
        audio = np.concatenate(self.buffer, axis=0)
        # Clear buffer immediately so new audio starts accumulating fresh
        self.buffer = []

        try:
            result = self.asr_model.generate(
                input=audio,
                cache={},
                language="auto",
                use_itn=True,
            )
            if result and "text" in result[0]:
                return rich_transcription_postprocess(result[0]["text"]).strip()
        except Exception as e:
            print(f"\n⚠️  Transcription error: {e}", flush=True)
        return ""

    def run(self):
        # Start audio capture at device native rate (48kHz)
        stream = sd.InputStream(
            samplerate=DEVICE_RATE,
            channels=CHANNELS,
            callback=self.audio_callback,
            dtype=np.float32,
            blocksize=CHUNK_SAMPLES,
            **self.stream_kwargs,
        )
        stream.start()

        try:
            accumulated = 0
            last_sound_time = time.time()

            while not self.stop_event.is_set():
                try:
                    chunk = self.audio_queue.get(timeout=0.2)
                except queue.Empty:
                    continue

                # Drain amplitude queue and update last sound time
                while True:
                    try:
                        amp = self.amplitude_queue.get_nowait()
                        if amp > AMPLITUDE_THRESHOLD:
                            last_sound_time = time.time()
                    except queue.Empty:
                        break

                # Check idle timeout
                if self.idle_timeout > 0 and (time.time() - last_sound_time) > self.idle_timeout:
                    print(f"\n⏸️  已 {self.idle_timeout} 秒没有检测到声音，自动停止。", flush=True)
                    self.stop_event.set()
                    self._idle_timeout = True
                    break

                self.buffer.append(chunk)
                accumulated += 1

                # Transcribe every TRANSCRIBE_INTERVAL seconds
                if accumulated >= TRANSCRIBE_INTERVAL:
                    accumulated = 0
                    text = self.transcribe_buffer()
                    if text:
                        # Strip overlap with previous result
                        new_text = _strip_overlap(text, self.prev_text)
                        self.prev_text = text

                        if new_text:
                            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
                            line = f"[{timestamp}] {new_text}"
                            print(f"  → {new_text}", flush=True)
                            # Append to output file
                            if self.output_file:
                                with self.output_lock:
                                    with open(self.output_file, "a", encoding="utf-8") as f:
                                        f.write(line + "\n")

        except KeyboardInterrupt:
            pass
        finally:
            self.stop_event.set()
            stream.stop()
            stream.close()

        print("\nStopped.")


def main():
    parser = argparse.ArgumentParser(description="Real-time SenseVoice transcription")
    parser.add_argument("--source", default="blackhole", choices=["blackhole", "mic"],
                        help="Audio input source: blackhole (system audio) or mic (microphone)")
    parser.add_argument("--device", default=None, type=int,
                        help="Audio input device ID (overrides auto-detection)")
    parser.add_argument("--output", default=".tmp/transcript.txt",
                        help="Transcript output file path (default: .tmp/transcript.txt)")
    parser.add_argument("--state", default=".tmp/asr.pid",
                        help="Process PID file path (default: .tmp/asr.pid)")
    parser.add_argument("--model", default="./model/SenseVoiceSmall",
                        help="Path to SenseVoice model directory")
    parser.add_argument("--check-deps", action="store_true",
                        help="Check dependencies and exit")
    parser.add_argument("--install-deps", action="store_true",
                        help="Install missing dependencies with progress output")
    parser.add_argument("--list-devices", action="store_true",
                        help="List available audio input devices")
    parser.add_argument("--idle-timeout", default=IDLE_TIMEOUT, type=int,
                        help=f"Stop after N seconds of silence (0 to disable, default: {IDLE_TIMEOUT})")
    args = parser.parse_args()

    # --- Dependency management ---
    missing = check_deps()

    if args.install_deps:
        print("📦 检查并安装转录技能依赖...\n")
        print(f"  需要安装的依赖: {', '.join(REQUIRED_DEPS.keys())}\n")
        # List status
        for pkg, desc in REQUIRED_DEPS.items():
            status = "✅ 已安装" if pkg not in missing else "❌ 未安装"
            print(f"  {status}  {pkg} — {desc}")
        print()
        if missing:
            print(f"  需要安装: {', '.join(missing)}\n")
            if install_deps(missing):
                sys.exit(0)
            else:
                sys.exit(1)
        else:
            print("  ✅ 所有依赖已安装，无需更新。")
            sys.exit(0)

    if args.check_deps:
        if not missing:
            print("✅ 所有依赖已安装。")
            for pkg, desc in REQUIRED_DEPS.items():
                print(f"   {pkg} — {desc}")
            sys.exit(0)
        else:
            print("❌ 缺少依赖:\n")
            for pkg, desc in REQUIRED_DEPS.items():
                status = "✅" if pkg not in missing else "❌"
                print(f"  {status} {pkg} — {desc}")
            print(f"\n请运行以下命令安装:")
            print(f"  pip3 install {' '.join(missing)}")
            print(f"\n或者运行:")
            print(f"  python3 realtime_asr.py --install-deps")
            sys.exit(1)

    # If missing deps at startup, refuse to run
    if missing:
        print("❌ 转录技能无法启动，缺少以下依赖:\n")
        for pkg in missing:
            desc = REQUIRED_DEPS.get(pkg, '')
            print(f"  ❌ {pkg} — {desc}")
        print(f"\n请先安装依赖:")
        print(f"  pip3 install {' '.join(missing)}")
        print(f"\n或者运行:")
        print(f"  python3 realtime_asr.py --install-deps")
        sys.exit(1)

    # All deps satisfied — import the rest
    sd, librosa, torch, AutoModel, rich_transcription_postprocess = import_deps()

    if args.list_devices:
        print(sd.query_devices())
        return

    # Auto-detect device based on source
    device_kw = {}
    if args.device is not None:
        device_kw["device"] = args.device
    else:
        dev_info = sd.query_devices()
        if args.source == "blackhole":
            for i, d in enumerate(dev_info):
                if d["max_input_channels"] > 0 and "blackhole" in d["name"].lower():
                    device_kw["device"] = i
                    break
            else:
                # Fallback: try Loopback
                for i, d in enumerate(dev_info):
                    if d["max_input_channels"] > 0 and "loopback" in d["name"].lower():
                        device_kw["device"] = i
                        break
                else:
                    print("[ERROR] No BlackHole/Loopback device found. Install BlackHole or use --source mic.", file=sys.stderr)
                    sys.exit(1)
        else:  # mic
            for i, d in enumerate(dev_info):
                if d["max_input_channels"] > 0 and "mic" in d["name"].lower():
                    device_kw["device"] = i
                    break
            else:
                # Default to first input device
                for i, d in enumerate(dev_info):
                    if d["max_input_channels"] > 0:
                        device_kw["device"] = i
                        break

    # Create output directory if needed
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    os.makedirs(os.path.dirname(args.state) or ".", exist_ok=True)

    # Write PID file
    with open(args.state, "w") as f:
        f.write(str(os.getpid()))

    source_label = "系统音频" if args.source == "blackhole" else "麦克风"
    print(f"=" * 50)
    print(f"  Real-time Speech Transcription (SenseVoice)")
    print(f"  Source: {source_label}")
    print(f"  Output: {args.output}")
    print(f"  Press Ctrl+C to stop")
    print(f"=" * 50)
    print()

    # Register SIGTERM handler so `kill <pid>` also cleans up the PID file
    def _sigterm_handler(signum, frame):
        raise SystemExit(0)
    signal.signal(signal.SIGTERM, _sigterm_handler)

    transcriber = StreamingTranscriber(
        model_path=args.model,
        stream_kwargs=device_kw,
        output_file=args.output,
        idle_timeout=args.idle_timeout,
    )
    try:
        transcriber.run()
    finally:
        # Clean up PID file
        if os.path.exists(args.state):
            os.remove(args.state)
        # Exit with special code if idle timeout triggered
        if getattr(transcriber, '_idle_timeout', False):
            sys.exit(EXIT_CODE_IDLE)


if __name__ == "__main__":
    main()
