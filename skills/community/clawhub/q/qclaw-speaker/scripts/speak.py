#!/usr/bin/env python3
"""QClaw Speaker — 四引擎 TTS 语音播报系统

====================================================================
Engine              离线  模型  中文  速度    流式   安装
====================================================================
edge (Microsoft)    ❌   0MB  ⭐⭐⭐⭐⭐  <1s    ✅   pip edge-tts
sherpa (Piper ONNX) ✅  13MB  ⭐⭐⭐⭐   <0.2s  ✅   pip sherpa-onnx
win (SAPI)          ✅   0MB  ⭐⭐⭐    <0.1s  ✅   系统自带
====================================================================

Auto优先级: edge → sherpa → win (任一成功即停止)

Usage:
  python speak.py "你好世界"                          # auto
  python speak.py "播报" --voice xiaoxiao              # 晓晓女声(edge)
  python speak.py "播放" --engine sherpa --voice xiao_ya  # 小雅女声(本地)
  python speak.py "离线" --engine win                  # Windows原生
  python speak.py --list-voices
  python speak.py --auto-speak on              # 开启自动播报
"""

import os, sys, json, argparse, tempfile, asyncio, time, struct, shutil
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
CONFIG_FILE = SKILL_DIR / "config.json"
MODELS_DIR = SKILL_DIR / "models"

# ━━ Voice Registry ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VOICES = {
    # Edge TTS (online, premium neural) — DEFAULT
    "xiaoxiao":  {"engine":"edge","voice":"zh-CN-XiaoxiaoNeural",  "desc":"晓晓 微软神经女声 ⭐默认","size":0},
    "yunxi":     {"engine":"edge","voice":"zh-CN-YunxiNeural",     "desc":"云希 微软神经男声","size":0},
    "xiaoyi":    {"engine":"edge","voice":"zh-CN-XiaoyiNeural",    "desc":"晓依 温柔知性女声","size":0},
    "xiaochen":  {"engine":"edge","voice":"zh-CN-XiaochenNeural",  "desc":"晓辰 自然男声","size":0},
    "yunyang":   {"engine":"edge","voice":"zh-CN-YunyangNeural",   "desc":"云扬 新闻播报男声","size":0},
    "xiaohan":   {"engine":"edge","voice":"zh-CN-XiaohanNeural",   "desc":"晓涵 少女甜美女声","size":0},

    # Sherpa-onnx Piper VITS (offline, 13MB ONNX)
    "xiao_ya":   {"engine":"sherpa","voice":"vits-piper-zh_CN-xiao_ya-medium-int8",  "desc":"小雅 女声 (13MB离线)","size":13},
    "chaowen":   {"engine":"sherpa","voice":"vits-piper-zh_CN-chaowen-medium-int8",  "desc":"超稳 男声 (13MB离线)","size":13},
    "huayan":    {"engine":"sherpa","voice":"vits-piper-zh_CN-huayan-medium",        "desc":"花颜 女声 (64MB离线)","size":64},

    # Windows SAPI (offline, native)
    "huihui":    {"engine":"win",  "voice":"huihui",                "desc":"慧慧 Windows原生中文","size":0},
}

DEFAULT_VOICE = "xiaoxiao"


# ━━ Helpers ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def load_config():
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text(encoding='utf-8'))
    return {"voice": DEFAULT_VOICE, "speed": 1.0, "auto_speak": False}

def save_config(cfg):
    CONFIG_FILE.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding='utf-8')

def _ensure_ort_fix():
    """Override sherpa-onnx's bundled ORT DLL with system ORT if needed."""
    try:
        import sherpa_onnx
        sherpa_dir = Path(sherpa_onnx.__file__).parent
        # Check if ORT DLL in sherpa dir differs from system
        local_dll = sherpa_dir / "lib" / "onnxruntime.dll"
        if local_dll.exists():
            return  # Already overridden
        # Find system ORT DLL
        import onnxruntime as ort
        ort_dir = Path(ort.__file__).parent
        for candidate in [ort_dir / "capi" / "onnxruntime.dll",
                          ort_dir / "onnxruntime.dll"]:
            if candidate.exists():
                shutil.copy2(str(candidate), str(sherpa_dir / "lib" / "onnxruntime.dll"))
                shutil.copy2(str(candidate), str(sherpa_dir / "onnxruntime.dll"))
                return
    except ImportError:
        pass


# ━━ Engine: Edge TTS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def speak_edge(text, voice_name="xiaoxiao", speed=1.0, output=None):
    import edge_tts
    voice = VOICES.get(voice_name, {}).get("voice", "zh-CN-XiaoxiaoNeural")
    rate_str = f"{int((speed - 1) * 100):+d}%"
    if not output:
        output = str(Path(tempfile.gettempdir()) / f"qclaw_edge_{int(time.time()*1000)}.mp3")
    async def _run():
        communicate = edge_tts.Communicate(text, voice, rate=rate_str)
        await communicate.save(output)
    asyncio.run(_run())
    return output


# ━━ Engine: Sherpa-onnx (Piper VITS) ━━━━━━━━━━━━━━━━━━━━━━━
def speak_sherpa(text, voice_name="xiao_ya", speed=1.0, output=None):
    _ensure_ort_fix()
    import sherpa_onnx, soundfile as sf

    # Find model files
    voice_info = VOICES.get(voice_name, VOICES["xiao_ya"])
    model_name = voice_info.get("voice", "vits-piper-zh_CN-xiao_ya-medium-int8")
    model_dir = MODELS_DIR / model_name
    if not model_dir.exists():
        raise RuntimeError(f"Model not found: {model_dir}. Run 'python scripts/install.py --sherpa {voice_name}'")

    onnx_file = str(list(model_dir.glob("*.onnx"))[0])
    tokens_file = str(list(model_dir.glob("tokens.txt"))[0])
    lexicon_file = str(list(model_dir.glob("lexicon.txt"))[0]) if list(model_dir.glob("lexicon.txt")) else ""

    config = sherpa_onnx.OfflineTtsConfig(
        model=sherpa_onnx.OfflineTtsModelConfig(
            vits=sherpa_onnx.OfflineTtsVitsModelConfig(
                model=onnx_file,
                tokens=tokens_file,
                lexicon=lexicon_file,
                data_dir=str(model_dir),
            )),
        max_num_sentences=1)

    if not output:
        output = str(Path(tempfile.gettempdir()) / f"qclaw_sherpa_{int(time.time()*1000)}.wav")

    tts = sherpa_onnx.OfflineTts(config)
    audio = tts.generate(text, sid=0, speed=speed)
    if audio and audio.samples is not None:
        sf.write(output, audio.samples, audio.sample_rate)
        return output
    raise RuntimeError("sherpa-onnx: no audio generated")


# ━━ Engine: Windows SAPI ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def speak_win(text, voice_name="huihui", speed=1.0, output=None):
    import pyttsx3
    if not output:
        output = str(Path(tempfile.gettempdir()) / f"qclaw_win_{int(time.time()*1000)}.wav")
    engine = pyttsx3.init()
    engine.setProperty('rate', int(150 * speed))
    engine.setProperty('volume', 1.0)
    if voice_name == "huihui":
        voices = engine.getProperty('voices')
        zh = [v for v in voices if 'chinese' in v.name.lower()]
        if zh:
            engine.setProperty('voice', zh[0].id)
    engine.save_to_file(text, output)
    engine.runAndWait()
    engine.stop()
    return output


# ━━ Dispatcher ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SPEAKERS = {"edge": speak_edge, "sherpa": speak_sherpa, "win": speak_win}

def speak_text(text, voice_name=None, engine=None, speed=None, output=None):
    cfg = load_config()
    voice_name = voice_name or cfg.get("voice", DEFAULT_VOICE)
    speed = speed or cfg.get("speed", 1.0)
    voice_info = VOICES.get(voice_name)
    if not voice_info:
        raise ValueError(f"Unknown voice: {voice_name}. Run --list-voices")

    eng = engine or voice_info.get("engine", "edge")

    # Strict mode: use exactly the engine requested or implied by voice
    if engine:
        return SPEAKERS[engine](text, voice_name, speed, output)

    # Auto mode: try voice's native engine first, then fallback edg→shr→win
    engines_to_try = [eng] + [e for e in ["edge","sherpa","win"] if e != eng]
    for e in engines_to_try:
        try:
            return SPEAKERS[e](text, voice_name, speed, output)
        except Exception as ex:
            print(f"[WARN]  {e} engine failed: {ex}", file=sys.stderr)
            continue
    raise RuntimeError("All TTS engines failed.")


# ━━ CLI ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def show_voice_table():
    print("\n🎙️  QClaw Speaker — 四引擎音色库\n")
    col = "%-3s %-14s %-8s %-6s %-28s %s"
    print(col % ("", "Name", "Engine", "Size", "  Description", "Mode"))
    print("-" * 75)
    for name, info in VOICES.items():
        sz = f"{info['size']}MB" if info['size'] else "——"
        m = "★ " if name == DEFAULT_VOICE else "  "
        eng = info.get('engine','?')
        mode = "🟢在线" if eng == 'edge' else ("🔵本地" if eng in ('sherpa','win') else "?")
        print(col % (m, name, eng, sz, info['desc'], mode))
    print(f"\n  默认: {DEFAULT_VOICE}  |  auto: edge → sherpa → win\n")

def show_config():
    print(json.dumps(load_config(), ensure_ascii=False, indent=2))

def main():
    parser = argparse.ArgumentParser(description="QClaw Speaker — 四引擎 TTS")
    parser.add_argument("text", nargs="?", help="要朗读的文字")
    parser.add_argument("--voice", "-v", help="音色名称")
    parser.add_argument("--engine", "-e", choices=["auto","edge","sherpa","win"], default="auto")
    parser.add_argument("--speed", "-s", type=float, default=1.0)
    parser.add_argument("--output", "-o", help="输出音频文件路径")
    parser.add_argument("--list-voices", action="store_true")
    parser.add_argument("--set-voice", help="设置默认音色")
    parser.add_argument("--set-speed", type=float)
    parser.add_argument("--auto-speak", choices=["on","off"])
    parser.add_argument("--config", action="store_true", help="显示配置")
    parser.add_argument("--config-path", action="store_true")
    args = parser.parse_args()

    if args.list_voices:   return show_voice_table()
    if args.config_path:   return print(str(CONFIG_FILE))
    if args.config:        return show_config()
    if args.set_voice:
        if args.set_voice not in VOICES:
            print(f"[ERROR] Unknown voice: {args.set_voice}")
            return show_voice_table()
        c = load_config(); c["voice"] = args.set_voice; save_config(c)
        return print(f"[OK] 默认音色 → {args.set_voice} ({VOICES[args.set_voice]['desc']})")
    if args.set_speed:
        c = load_config(); c["speed"] = args.set_speed; save_config(c)
        return print(f"[OK] 语速 → {args.set_speed}x")
    if args.auto_speak:
        c = load_config()
        c["auto_speak"] = args.auto_speak == "on"
        save_config(c)
        return print(f"[OK] 自动播报: {'🟢 ON' if c['auto_speak'] else '⚫ OFF'}")
    if not args.text:
        parser.print_help()
        return

    try:
        out = speak_text(text=args.text, voice_name=args.voice,
                         engine=args.engine if args.engine != "auto" else None,
                         speed=args.speed, output=args.output)
        print(json.dumps({"status":"ok","file":out,"voice":args.voice or load_config().get('voice','xiaoxiao')}))
    except Exception as e:
        print(json.dumps({"status":"error","error":str(e)}), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()