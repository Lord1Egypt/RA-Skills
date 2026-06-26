"""
Voice Bridge Light - 简化版 HTTP API 服务
提供 STT (语音识别) 和 TTS (语音合成) 的 OpenAI 兼容接口
支持引擎：
- TTS: Piper (本地), Edge TTS (在线)
- STT: Whisper (本地)
"""

import os
import json
import logging
import asyncio
from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import numpy as np
import soundfile as sf
import io

# TTS 引擎
try:
    from piper import PiperVoice
    PIPER_AVAILABLE = True
except ImportError:
    PIPER_AVAILABLE = False

try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False

# STT 引擎
try:
    from faster_whisper import WhisperModel
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False

app = Flask(__name__)
CORS(app)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

HOST = os.getenv('VOICE_BRIDGE_HOST', '0.0.0.0')
PORT = int(os.getenv('VOICE_BRIDGE_PORT', 18790))
TTS_ENGINE = os.getenv('TTS_ENGINE', 'edge').lower()
PIPER_MODEL = os.getenv('PIPER_MODEL', 'models/piper/zh_CN-huayan-medium.onnx')
EDGE_VOICE = os.getenv('EDGE_VOICE', 'zh-CN-XiaoxiaoNeural')
STT_MODEL = os.getenv('STT_MODEL', 'base')

tts_engine = None
stt_engine = None

def get_piper():
    global tts_engine
    if tts_engine is None and PIPER_AVAILABLE:
        try:
            tts_engine = PiperVoice(PIPER_MODEL)
            logger.info(f"Piper TTS 加载成功: {PIPER_MODEL}")
        except Exception as e:
            logger.error(f"Piper 加载失败: {e}")
    return tts_engine

def get_edge_tts():
    return EDGE_TTS_AVAILABLE

def synthesize_piper(text, voice=None):
    engine = get_piper()
    if engine is None:
        raise RuntimeError("Piper TTS 不可用")
    audio, sample_rate = engine.synthesize(text, speaker_id=0)
    return audio, sample_rate

def synthesize_edge(text, voice=None):
    if not EDGE_TTS_AVAILABLE:
        raise RuntimeError("Edge TTS 不可用")
    voice = voice or EDGE_VOICE
    
    async def _synth():
        communicate = edge_tts.Communicate(text, voice)
        audio_chunks = []
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_chunks.append(chunk["data"])
        return b''.join(audio_chunks)
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        audio_mp3 = loop.run_until_complete(_synth())
    finally:
        loop.close()
    return audio_mp3

def get_stt():
    global stt_engine
    if stt_engine is None and WHISPER_AVAILABLE:
        try:
            stt_engine = WhisperModel(STT_MODEL, device="cpu", compute_type="int8")
            logger.info(f"Whisper STT 加载成功: {STT_MODEL}")
        except Exception as e:
            logger.error(f"Whisper 加载失败: {e}")
    return stt_engine

@app.route('/health', methods=['GET'])
def health():
    piper_ready = get_piper() is not None
    edge_ready = EDGE_TTS_AVAILABLE
    stt_ready = get_stt() is not None
    tts_ready = piper_ready if TTS_ENGINE == 'piper' else edge_ready
    return jsonify({
        "status": "healthy",
        "tts_ready": tts_ready,
        "stt_ready": stt_ready,
        "engines": {"piper": piper_ready, "edge": edge_ready, "whisper": stt_ready}
    })

@app.route('/audio/speech', methods=['POST'])
def tts():
    try:
        data = request.get_json(force=True)
        text = data.get('input', '').strip()
        fmt = data.get('response_format', 'wav')
        voice = data.get('voice')
        if not text:
            return jsonify({"error": "empty input"}), 400

        if TTS_ENGINE == 'piper' and PIPER_AVAILABLE:
            audio, sample_rate = synthesize_piper(text, voice)
            buffer = io.BytesIO()
            sf.write(buffer, audio, sample_rate, format='wav')
            audio_bytes = buffer.getvalue()
        else:
            if not EDGE_TTS_AVAILABLE:
                return jsonify({"error": "TTS 引擎不可用"}), 503
            audio_bytes = synthesize_edge(text, voice)
            if fmt == 'wav':
                try:
                    from pydub import AudioSegment
                    mp3 = AudioSegment.from_file(io.BytesIO(audio_bytes), format="mp3")
                    wav_io = io.BytesIO()
                    mp3.export(wav_io, format="wav")
                    audio_bytes = wav_io.getvalue()
                except Exception as e:
                    logger.error(f"MP3 转 WAV 失败: {e}")
                    fmt = 'mp3'

        if fmt == 'pcm':
            import wave
            with io.BytesIO(audio_bytes) as bio:
                with wave.open(bio, 'rb') as wav:
                    pcm_data = wav.readframes(wav.getnframes())
            return Response(pcm_data, mimetype='audio/pcm')
        elif fmt == 'mp3':
            return Response(audio_bytes, mimetype='audio/mpeg')
        else:
            return Response(audio_bytes, mimetype='audio/wav')
    except Exception as e:
        logger.error(f"TTS 错误: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/audio/transcriptions', methods=['POST'])
def stt():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "no file provided"}), 400
        file = request.files['file']
        audio_data = file.read()
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            f.write(audio_data)
            temp_path = f.name
        engine = get_stt()
        if engine is None:
            return jsonify({"error": "STT 不可用"}), 503
        segments, info = engine.transcribe(temp_path, language="zh")
        text = "".join([seg.text for seg in segments])
        os.unlink(temp_path)
        return jsonify({
            "text": text.strip(),
            "task": "transcribe",
            "language": info.language,
            "duration": info.duration
        })
    except Exception as e:
        logger.error(f"STT 错误: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    logger.info(f"Voice Bridge Light 启动: http://{HOST}:{PORT}")
    logger.info(f"TTS 引擎: {TTS_ENGINE} (Piper可用: {PIPER_AVAILABLE}, Edge可用: {EDGE_TTS_AVAILABLE})")
    app.run(host=HOST, port=PORT, debug=False, threaded=True, use_reloader=False)