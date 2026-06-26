#!/usr/bin/env python3
"""
voice_speak.py — 中枢语音输出（豆包TTS版）

修复版 v2：长文本分段 + 顺序播放 + PID锁防重叠

每次调用：
  python3 voice_speak.py "要说的内容"
"""

import sys
import json
import urllib.request
import subprocess
import uuid
import tempfile
import os
import base64
import signal

# ============== 豆包TTS 配置 ==============
APPID = "8982709936"
ACCESS_TOKEN = "gSlkMz98nDVwnHUwiuDefPjwVFtFNrbw"
CLUSTER = "volcano_tts"

# 默认音色
DEFAULT_VOICE = "zh_female_xiaohe_uranus_bigtts"
DEFAULT_EMOTION = "neutral"
DEFAULT_SPEED = 1.0
DEFAULT_PITCH = 1.0
DEFAULT_ENCODING = "mp3"

# 分段配置
MAX_CHARS_PER_SEGMENT = 200      # 每段最大字符数（减小以防超时）
AFPLAY_TIMEOUT = 30              # 播放超时（秒）
LOCK_FILE = "/tmp/voice_speaking.lock"


# ============== PID 锁 ==============
def acquire_lock():
    """获取锁，成功返回 True；锁存在且进程存活则返回 False"""
    if os.path.exists(LOCK_FILE):
        try:
            old_pid = int(open(LOCK_FILE).read().strip())
            os.kill(old_pid, 0)  # 信号0只检测存活
            return False  # 进程还活着，真的在播放
        except (ProcessLookupError, ValueError, OSError):
            pass  # 进程已死，锁文件残留，删掉继续
    try:
        with open(LOCK_FILE, 'w') as f:
            f.write(str(os.getpid()))
        return True
    except Exception:
        return False


def release_lock():
    """释放锁"""
    if os.path.exists(LOCK_FILE):
        try:
            os.unlink(LOCK_FILE)
        except Exception:
            pass


# ============== 文本分段 ==============
def split_text(text: str) -> list:
    """按中文句号/问号/感叹号分句，每段不超过 MAX_CHARS_PER_SEGMENT"""
    if not text:
        return []

    # 按句子分隔符分
    import re
    # 先按可断句的标点分
    sentences = re.split(r'([。！？\n]+)', text)
    
    segments = []
    current = ""

    for i in range(0, len(sentences), 2):
        s = sentences[i]
        # 接上标点（如果有）
        if i + 1 < len(sentences):
            s += sentences[i + 1]

        if len(current) + len(s) <= MAX_CHARS_PER_SEGMENT:
            current += s
        else:
            # current 已满，先保存
            if current.strip():
                segments.append(current.strip())
            # 新的段落从 s 开始
            current = s

    # 剩余内容
    if current.strip():
        segments.append(current.strip())

    # 如果单个句子超长，强制按 MAX_CHARS_PER_SEGMENT 截断
    final_segments = []
    for seg in segments:
        while len(seg) > MAX_CHARS_PER_SEGMENT:
            final_segments.append(seg[:MAX_CHARS_PER_SEGMENT])
            seg = seg[MAX_CHARS_PER_SEGMENT:]
        if seg.strip():
            final_segments.append(seg.strip())

    return final_segments


# ============== 豆包TTS ==============
def tts_synthesize(
    text: str,
    voice_type: str = DEFAULT_VOICE,
    emotion: str = DEFAULT_EMOTION,
    speed_ratio: float = DEFAULT_SPEED,
    pitch_ratio: float = DEFAULT_PITCH,
    encoding: str = DEFAULT_ENCODING,
) -> bytes:
    """调用豆包TTS 2.0 API，返回音频数据（bytes，MP3格式）"""
    url = "https://openspeech.bytedance.com/api/v1/tts"
    reqid = str(uuid.uuid4())

    payload = {
        "app": {
            "appid": APPID,
            "token": ACCESS_TOKEN,
            "cluster": CLUSTER,
        },
        "user": {"uid": "zhongshu_tts"},
        "audio": {
            "voice_type": voice_type,
            "encoding": encoding,
            "speed_ratio": speed_ratio,
            "volume_ratio": 1.0,
            "pitch_ratio": pitch_ratio,
            "emotion": emotion,
        },
        "request": {
            "reqid": reqid,
            "text": text,
            "text_type": "plain",
            "operation": "query",
        },
    }

    headers = {
        "Authorization": f"Bearer; {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read())

    if result.get("code") != 3000:
        raise Exception(f"TTS API error: code={result.get('code')}, msg={result.get('message')}")

    audio_base64 = result.get("data", "")
    if not audio_base64:
        raise Exception("No audio data in response")

    return base64.b64decode(audio_base64)


# ============== 单段合成 + 播放 ==============
def speak_segment(
    text: str,
    voice_type: str,
    emotion: str,
    speed_ratio: float,
    pitch_ratio: float,
) -> bool:
    """合成并播放单段文字，成功返回 True"""
    tmp = tempfile.gettempdir()
    tmp_file = os.path.join(tmp, f"voice_{uuid.uuid4().hex}.mp3")

    try:
        audio_data = tts_synthesize(text, voice_type, emotion, speed_ratio, pitch_ratio)
        print(f"[DoubaoTTS] generated {len(audio_data)} bytes: '{text[:30]}...'", file=sys.stderr)

        with open(tmp_file, "wb") as f:
            f.write(audio_data)

        # 阻塞等待播放完成，带超时保护
        result = subprocess.run(
            ["afplay", "-q", "1", tmp_file],  # -q 1 = 高质量，阻塞
            capture_output=True,
            timeout=AFPLAY_TIMEOUT,
        )

        if result.returncode == 0:
            print(f"[DoubaoTTS] played: '{text[:30]}...'", file=sys.stderr)
            return True
        else:
            print(f"[DoubaoTTS] play failed: {result.stderr.decode()[:100]}", file=sys.stderr)
            return False

    except subprocess.TimeoutExpired:
        print(f"[DoubaoTTS] play timeout ({AFPLAY_TIMEOUT}s), skipping", file=sys.stderr)
        return False
    except Exception as e:
        print(f"[DoubaoTTS ERROR] {e}", file=sys.stderr)
        return False
    finally:
        if os.path.exists(tmp_file):
            try:
                os.unlink(tmp_file)
            except Exception:
                pass


# ============== 主函数 ==============
def speak(
    text: str,
    voice_type: str = DEFAULT_VOICE,
    emotion: str = DEFAULT_EMOTION,
    speed_ratio: float = DEFAULT_SPEED,
    pitch_ratio: float = DEFAULT_PITCH,
) -> bool:
    """文字转语音并播放（分段顺序播放），成功返回 True"""
    if not text or not text.strip():
        return False

    # 获取锁
    if not acquire_lock():
        print(f"[DoubaoTTS] Another instance is playing, skipping.", file=sys.stderr)
        return False

    try:
        # 分段
        segments = split_text(text)
        print(f"[DoubaoTTS] Split into {len(segments)} segments", file=sys.stderr)

        if not segments:
            return False

        success_count = 0
        fail_count = 0

        for i, seg in enumerate(segments):
            print(f"[DoubaoTTS] Playing segment {i+1}/{len(segments)}", file=sys.stderr)
            if speak_segment(seg, voice_type, emotion, speed_ratio, pitch_ratio):
                success_count += 1
            else:
                fail_count += 1

        print(f"[DoubaoTTS] Done: {success_count} ok, {fail_count} failed", file=sys.stderr)
        return success_count > 0

    finally:
        release_lock()


# ============== main ==============
def main():
    # 注册信号处理，确保退出时释放锁
    def cleanup(signum, frame):
        release_lock()
        sys.exit(0)
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print("用法: voice_speak.py \"要说的内容\" [voice_type] [emotion] [speed] [pitch]")
        print("示例: voice_speak.py \"你好，我是中枢\" zh_female_xiaohe_uranus_bigtts happy 1.0 1.0")
        print(f"\n默认音色: {DEFAULT_VOICE}")
        print(f"默认情绪: {DEFAULT_EMOTION}")
        print(f"默认语速: {DEFAULT_SPEED}")
        print(f"每段上限: {MAX_CHARS_PER_SEGMENT} 字符")
        print(f"播放超时: {AFPLAY_TIMEOUT} 秒")
        sys.exit(0)

    text = sys.argv[1]
    voice_type = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_VOICE
    emotion = sys.argv[3] if len(sys.argv) > 3 else DEFAULT_EMOTION
    speed = float(sys.argv[4]) if len(sys.argv) > 4 else DEFAULT_SPEED
    pitch = float(sys.argv[5]) if len(sys.argv) > 5 else DEFAULT_PITCH

    ok = speak(text, voice_type, emotion, speed, pitch)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
