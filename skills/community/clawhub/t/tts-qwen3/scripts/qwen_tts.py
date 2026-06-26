#!/usr/bin/env python3
"""
Qwen3-TTS 单角色语音合成脚本
通过 ComfyUI API 调用 Qwen3-TTS 生成语音。
失败时自动回退到 Edge TTS。

用法:
  python3 qwen_tts.py --text "你好" --voice qiqi_clone --output /tmp/out.wav
  python3 qwen_tts.py --text "旁白内容" --voice narrator_teacher --output /tmp/out.wav --srt /tmp/out.srt
"""

import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.error

# ComfyUI API
COMFYUI_URL = os.environ.get("COMFYUI_URL", "http://127.0.0.1:8188")

# 音色库配置
VOICE_PRESETS = {
    "qiqi_clone": {
        "label": "琪琪（克隆）",
        "type": "voice_clone",
        "ref_audio": os.path.expanduser("~/.openclaw/workspace/skills/tts-qwen3/presets/qiqi_voice_v3.wav"),
        "ref_text": "春天来了花园里的花朵都开放了小兔子琪琪蹦蹦跳跳的跑过来说好漂亮啊我们一起玩吧朋友们开心的笑着在阳光下奔跑",
        "model": "1.7B",
    },
    "narrator_teacher": {
        "label": "旁白-幼儿园老师",
        "type": "voice_design",
        "instruct": "A warm and gentle female voice, like a kindergarten teacher telling stories to children, speaking slowly and clearly with affection",
        "seed": 100,
        "model": "1.7B",
    },
    "boy_child": {
        "label": "男孩",
        "type": "voice_design",
        "instruct": "A cheerful young boy's voice, energetic and curious, around 8 years old, speaking with enthusiasm",
        "seed": 200,
        "model": "1.7B",
    },
    "girl_child": {
        "label": "女孩",
        "type": "voice_design",
        "instruct": "A sweet young girl's voice, bright and lively, around 7 years old, speaking with innocence and joy",
        "seed": 300,
        "model": "1.7B",
    },
    "adult_male": {
        "label": "大人男",
        "type": "voice_design",
        "instruct": "A mature and steady male voice, deep and warm, speaking with confidence and calmness",
        "seed": 400,
        "model": "1.7B",
    },
    "adult_female": {
        "label": "大人女",
        "type": "voice_design",
        "instruct": "An elegant and gentle female voice, warm and reassuring, speaking with grace and kindness",
        "seed": 500,
        "model": "1.7B",
    },
}

# Edge TTS 回退音色映射
EDGE_TTS_FALLBACK = {
    "qiqi_clone": "zh-CN-XiaoyiNeural",
    "narrator_teacher": "zh-CN-XiaoxiaoNeural",
    "boy_child": "zh-CN-YunxiNeural",
    "girl_child": "zh-CN-XiaoyiNeural",
    "adult_male": "zh-CN-YunjianNeural",
    "adult_female": "zh-CN-XiaoxiaoNeural",
}


def build_voice_design_workflow(text, voice_name, language="Chinese", model="1.7B", attention="sdpa"):
    """构建 VoiceDesign 工作流（用于旁白、男孩、女孩等设计音色）"""
    preset = VOICE_PRESETS[voice_name]
    seed = preset.get("seed", 100)
    instruct = preset.get("instruct", "")

    workflow = {
        "1": {
            "class_type": "FB_Qwen3TTSVoiceDesign",
            "inputs": {
                "text": text,
                "instruct": instruct,
                "model_choice": model,
                "device": "auto",
                "precision": "bf16",
                "language": language,
                "seed": seed,
                "attention": attention,
                "unload_model_after_generate": False,
            }
        },
        "2": {
            "class_type": "SaveAudio",
            "inputs": {
                "audio": ["1", 0],
                "filename_prefix": f"qwen_tts/{voice_name}",
            }
        }
    }
    return workflow


def build_voice_clone_workflow(text, voice_name, language="Chinese", model="1.7B", attention="sdpa"):
    """构建 VoiceClone 工作流（用于琪琪克隆音色）"""
    preset = VOICE_PRESETS[voice_name]
    ref_audio = preset.get("ref_audio", "")
    ref_text = preset.get("ref_text", "")

    if not os.path.exists(ref_audio):
        print(f"⚠️ 参考音频不存在: {ref_audio}，回退到 Edge TTS")
        return None

    # ComfyUI 需要相对路径（相对于 ComfyUI/input/ 目录）
    # 或者直接用文件名（前提是文件在 ComfyUI/input/ 下）
    comfyui_input_dir = os.path.expanduser("~/ComfyUI/input")
    ref_audio_filename = os.path.basename(ref_audio)
    # 确保参考音频在 ComfyUI/input 目录下
    if not os.path.exists(os.path.join(comfyui_input_dir, ref_audio_filename)):
        import shutil
        shutil.copy2(ref_audio, os.path.join(comfyui_input_dir, ref_audio_filename))

    workflow = {
        "1": {
            "class_type": "LoadAudio",
            "inputs": {
                "audio": ref_audio_filename,
                "channel": "stereo",
            }
        },
        "2": {
            "class_type": "FB_Qwen3TTSVoiceClonePrompt",
            "inputs": {
                "ref_audio": ["1", 0],
                "ref_text": ref_text,
                "model_choice": model,
                "device": "auto",
                "precision": "bf16",
                "attention": attention,
                "x_vector_only": True,
                "unload_model_after_generate": False,
            }
        },
        "3": {
            "class_type": "FB_Qwen3TTSVoiceClone",
            "inputs": {
                "target_text": text,
                "model_choice": model,
                "device": "auto",
                "precision": "bf16",
                "language": language,
                "voice_clone_prompt": ["2", 0],
                "attention": attention,
                "unload_model_after_generate": False,
            }
        },
        "4": {
            "class_type": "SaveAudio",
            "inputs": {
                "audio": ["3", 0],
                "filename_prefix": f"qwen_tts/{voice_name}",
            }
        }
    }
    return workflow


def queue_prompt(workflow):
    """提交工作流到 ComfyUI API"""
    data = json.dumps({"prompt": workflow}).encode("utf-8")
    req = urllib.request.Request(
        f"{COMFYUI_URL}/prompt",
        data=data,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
            return result.get("prompt_id")
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        print(f"❌ ComfyUI API 错误: {e}")
        return None


def wait_for_completion(prompt_id, timeout=300):
    """等待 ComfyUI 生成完成"""
    start = time.time()
    while time.time() - start < timeout:
        try:
            url = f"{COMFYUI_URL}/history/{prompt_id}"
            with urllib.request.urlopen(url, timeout=10) as resp:
                history = json.loads(resp.read())
                if prompt_id in history:
                    status = history[prompt_id].get("status", {})
                    if status.get("completed", False) or status.get("status_str") == "success":
                        outputs = history[prompt_id].get("outputs", {})
                        return True, outputs
                    elif status.get("status_str") == "error":
                        return False, f"生成失败: {status}"
        except Exception:
            pass
        time.sleep(2)
    return False, "超时"


def find_output_file(outputs, voice_name):
    """从 ComfyUI 输出中找到生成的音频文件"""
    for node_id, node_output in outputs.items():
        if "audio" in node_output:
            for audio_info in node_output["audio"]:
                filename = audio_info.get("filename", "")
                subfolder = audio_info.get("subfolder", "")
                output_dir = os.path.expanduser("~/ComfyUI/output")
                path = os.path.join(output_dir, subfolder, filename)
                if os.path.exists(path):
                    return path
    # 兜底：搜索最新文件
    output_dir = os.path.expanduser(f"~/ComfyUI/output/qwen_tts")
    if os.path.exists(output_dir):
        files = sorted(
            [f for f in os.listdir(output_dir) if voice_name in f and f.endswith(('.wav', '.flac'))],
            key=lambda f: os.path.getmtime(os.path.join(output_dir, f)),
            reverse=True,
        )
        if files:
            return os.path.join(output_dir, files[0])
    return None


def fallback_edge_tts(text, voice_name, output_path, srt_path=None):
    """回退到 Edge TTS"""
    edge_voice = EDGE_TTS_FALLBACK.get(voice_name, "zh-CN-XiaoxiaoNeural")
    print(f"🔄 回退到 Edge TTS，音色: {edge_voice}")

    edge_script = os.path.expanduser("~/.openclaw/workspace/skills/tts-cosyvoice/scripts/tts.py")
    cmd = [sys.executable, edge_script, "--text", text, "--voice", edge_voice, "--output", output_path]
    if srt_path:
        cmd.extend(["--srt", srt_path])

    import subprocess
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Edge TTS 也失败了: {result.stderr}")
        return False
    print(f"✅ Edge TTS 生成完成: {output_path}")
    return True


def convert_to_wav(src_path, dst_path):
    """用 ffmpeg 转换音频格式"""
    import subprocess
    cmd = ["ffmpeg", "-y", "-i", src_path, "-ar", "24000", "-ac", "1", dst_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(description="Qwen3-TTS 语音合成")
    parser.add_argument("--text", required=True, help="要合成的文本")
    parser.add_argument("--voice", default="narrator_teacher", help="音色名")
    parser.add_argument("--output", default="/tmp/qwen_tts_output.wav", help="输出文件")
    parser.add_argument("--srt", default=None, help="SRT 字幕输出路径")
    parser.add_argument("--language", default="Chinese", help="语言")
    parser.add_argument("--model", default="1.7B", choices=["0.6B", "1.7B"], help="模型大小")
    parser.add_argument("--attention", default="sdpa", help="注意力机制")
    parser.add_argument("--fallback-edge", default="true", help="失败时回退 Edge TTS")
    parser.add_argument("--file", default=None, help="从文件读取文本")
    args = parser.parse_args()

    # 从文件读取文本
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read().strip()
    else:
        text = args.text

    if not text:
        print("❌ 文本为空")
        sys.exit(1)

    # 验证音色
    if args.voice not in VOICE_PRESETS:
        print(f"❌ 未知音色: {args.voice}")
        print(f"可用音色: {', '.join(VOICE_PRESETS.keys())}")
        sys.exit(1)

    preset = VOICE_PRESETS[args.voice]
    print(f"🎤 音色: {preset['label']} | 方式: {preset['type']} | 文本长度: {len(text)}字")

    # 尝试 Qwen3-TTS
    success = False
    output_path = None

    try:
        # 构建工作流
        if preset["type"] == "voice_clone":
            workflow = build_voice_clone_workflow(text, args.voice, args.language, args.model, args.attention)
        else:
            workflow = build_voice_design_workflow(text, args.voice, args.language, args.model, args.attention)

        if workflow is None:
            raise RuntimeError("工作流构建失败")

        # 提交到 ComfyUI
        print(f"📤 提交到 ComfyUI...")
        prompt_id = queue_prompt(workflow)
        if not prompt_id:
            raise RuntimeError("ComfyUI 提交失败")

        print(f"⏳ 等待生成 (prompt_id={prompt_id})...")
        ok, result = wait_for_completion(prompt_id, timeout=300)
        if not ok:
            raise RuntimeError(f"生成失败: {result}")

        # 找到输出文件
        output_path = find_output_file(result, args.voice)
        if not output_path:
            raise RuntimeError("找不到输出文件")

        print(f"✅ Qwen3-TTS 生成完成: {output_path}")

        # 转换到目标格式
        if output_path != args.output:
            if convert_to_wav(output_path, args.output):
                print(f"✅ 转换完成: {args.output}")
                output_path = args.output
            else:
                print(f"⚠️ 格式转换失败，使用原始文件: {output_path}")

        success = True

    except Exception as e:
        print(f"❌ Qwen3-TTS 失败: {e}")

    # 回退 Edge TTS
    if not success and args.fallback_edge.lower() in ("true", "1", "yes"):
        if not fallback_edge_tts(text, args.voice, args.output, args.srt):
            sys.exit(1)
    elif not success:
        print("❌ Qwen3-TTS 失败且未启用 Edge TTS 回退")
        sys.exit(1)

    # SRT 生成（如果需要）
    if args.srt and success:
        # Qwen3-TTS 不直接支持 SRT，用 ASR 回听生成时间轴
        # 或者用 Edge TTS 单独生成 SRT
        print(f"ℹ️ SRT 生成需要单独处理，可使用 Edge TTS --srt 或 ASR 回听")


if __name__ == "__main__":
    main()
