#!/usr/bin/env python3
"""
English Tutor · ASR 转写脚本
支持本地 sherpa-onnx（默认）和线上 ASR API（通过 ASR_PROVIDER 切换）

环境变量：
  ASR_PROVIDER=local|assemblyai|openai|xfyun
  ASR_API_KEY=your-key                    # AssemblyAI / OpenAI
  XFyun_ASR_APPID=xxx                    # 讯飞
  XFyun_ASR_APISECRET=xxx
  XFyun_ASR_APIKEY=xxx
  SENSE_VOICE_MODEL_DIR=~/.local/share/sense-voice-model   # 本地模型目录
  SHERPA_PYTHON_PATH=/path/to/site-packages               # sherpa-onnx 的 Python 路径

用法: python3 transcribe.py <audio_file> [sample_rate] [num_threads]
"""
import sys
import os
import tempfile

# ── 路径配置 ───────────────────────────────────────────────
def _get_model_dir():
    """从环境变量读取模型目录，默认 ~/.local/share/sense-voice-model"""
    return os.environ.get(
        'SENSE_VOICE_MODEL_DIR',
        os.path.join(os.path.expanduser('~'), '.local', 'share', 'sense-voice-model')
    )

def _setup_sherpa_path():
    """把 sherpa-onnx 的 Python 路径加入 sys.path"""
    p = os.environ.get('SHERPA_PYTHON_PATH', '')
    if p and p not in sys.path:
        sys.path.insert(0, p)

# ── 本地 ASR ───────────────────────────────────────────────
def local_asr(audio_path, sample_rate=16000, num_threads=2):
    _setup_sherpa_path()
    import subprocess, wave, numpy as np, sherpa_onnx

    model_dir = _get_model_dir()
    recognizer = sherpa_onnx.OfflineRecognizer.from_sense_voice(
        model=os.path.join(model_dir, 'model.onnx'),
        tokens=os.path.join(model_dir, 'tokens.txt'),
        provider='cpu',
        num_threads=num_threads,
        use_itn=True,
        sample_rate=sample_rate,
        debug=False
    )

    wav_path = os.path.join(tempfile.gettempdir(), 'sherpa_asr_temp.wav')
    r = subprocess.run(
        ['ffmpeg', '-y', '-i', audio_path,
         '-ar', str(sample_rate), '-ac', '1', '-acodec', 'pcm_s16le', wav_path],
        capture_output=True
    )
    if r.returncode != 0:
        raise RuntimeError('FFMPEG_ERROR: ' + r.stderr.decode()[-300:])

    with wave.open(wav_path, 'rb') as wf:
        samples = wf.readframes(wf.getnframes())

    stream = recognizer.create_stream()
    stream.accept_waveform(sample_rate, np.frombuffer(samples, dtype=np.int16))
    recognizer.decode_stream(stream)
    return stream.result.text

# ── AssemblyAI ─────────────────────────────────────────────
def assemblyai_asr(audio_path):
    import requests
    key = os.environ.get('ASR_API_KEY', '')
    if not key:
        raise RuntimeError('ASR_API_KEY not set (provider=assemblyai)')

    with open(audio_path, 'rb') as f:
        resp = requests.post(
            'https://api.assemblyai.com/v2/upload',
            headers={'Authorization': key},
            file={'file': (audio_path, f, 'audio/ogg')}
        )
    if resp.status_code != 200:
        raise RuntimeError(f'AssemblyAI upload failed: {resp.status_code}')

    transcript_id = resp.json()['upload_url']
    poll = requests.post(
        'https://api.assemblyai.com/v2/transcript',
        headers={'Authorization': key},
        json={'audio_url': transcript_id}
    )
    result = poll.json()
    import time
    while result.get('status') not in ('completed', 'error'):
        time.sleep(2)
        poll = requests.get(
            f"https://api.assemblyai.com/v2/transcript/{result['id']}",
            headers={'Authorization': key}
        )
        result = poll.json()

    if result['status'] == 'error':
        raise RuntimeError('AssemblyAI error: ' + result.get('error', ''))
    return result['text']

# ── OpenAI Whisper ─────────────────────────────────────────
def openai_whisper_asr(audio_path):
    import openai
    with open(audio_path, 'rb') as f:
        resp = openai.Audio.translate('whisper-1', f, filename=os.path.basename(audio_path))
    return resp['text']

# ── 讯飞 ASR ──────────────────────────────────────────────
def xfyun_asr(audio_path):
    raise NotImplementedError(
        '讯飞 ASR：请在 https://console.xfyun.cn 注册，'
        '设置 XFyun_ASR_APPID / XFyun_ASR_APISECRET / XFyun_ASR_APIKEY 环境变量，'
        '然后按官方文档实现签名认证'
    )

# ── 统一入口 ───────────────────────────────────────────────
def transcribe(audio_path, sample_rate=16000, num_threads=2):
    provider = os.environ.get('ASR_PROVIDER', 'local').lower()

    if provider == 'local':
        return local_asr(audio_path, sample_rate, num_threads)
    elif provider == 'assemblyai':
        return assemblyai_asr(audio_path)
    elif provider in ('xfyun', 'xunfei'):
        return xfyun_asr(audio_path)
    elif provider == 'openai':
        return openai_whisper_asr(audio_path)
    else:
        raise ValueError(f'Unknown ASR_PROVIDER: {provider}. Use: local | assemblyai | openai | xfyun')

# ── CLI ─────────────────────────────────────────────────────
if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
        print(__doc__)
        sys.exit(0)
    audio_path = sys.argv[1]
    if not os.path.exists(audio_path):
        print(f'ERROR: file not found: {audio_path}', file=sys.stderr)
        sys.exit(1)
    try:
        result = transcribe(audio_path)
        print(result)
    except Exception as e:
        print(f'ERROR: {e}', file=sys.stderr)
        sys.exit(1)
