#!/usr/bin/env python3
"""
mlx-qwen3-asr OpenAI 兼容 STT API 服务器
端点: POST /v1/audio/transcriptions
"""

import os
import tempfile
import time
import subprocess
import logging
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import uvicorn

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s")
logger = logging.getLogger("mlx-asr")

# ====== 启动时预加载模型 ======
DEFAULT_MODEL = os.environ.get("MLX_ASR_MODEL", "Qwen/Qwen3-ASR-0.6B")
logger.info(f"🔄 Loading model: {DEFAULT_MODEL} ...")
from mlx_qwen3_asr import transcribe
# 可选：预热（首次加载模型权重）
# transcribe("warmup.wav", model=DEFAULT_MODEL)
logger.info("✅ Model loaded!")

CONVERT_EXTS = {".silk", ".slk", ".amr", ".ogg", ".opus",
                ".webm", ".m4a", ".mp4", ".aac"}

app = FastAPI(title="MLX Qwen3-ASR Server", version="1.0.0")


def convert_to_wav(src: str) -> str | None:
    wav = src + ".wav"
    try:
        r = subprocess.run(
            ["ffmpeg", "-y", "-i", src, "-ar", "16000", "-ac", "1", "-f", "wav", wav],
            capture_output=True, timeout=60)
        if r.returncode == 0 and os.path.exists(wav):
            return wav
    except Exception:
        pass
    return None


@app.get("/")
async def health():
    return {"status": "ok", "model": DEFAULT_MODEL}


@app.get("/v1/models")
async def models():
    return {"object": "list", "data": [
        {"id": "qwen3-asr", "object": "model",
         "created": int(time.time()), "owned_by": "local"}]}


@app.post("/v1/audio/transcriptions")
async def transcribe_audio(
    file: UploadFile = File(...),
    model: str = Form(default="qwen3-asr"),
    language: str = Form(default=None),
    response_format: str = Form(default="json"),
):
    suffix = Path(file.filename).suffix.lower() if file.filename else ".wav"
    if not suffix:
        suffix = ".wav"

    # 保存临时文件
    try:
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        logger.info(f"📥 {file.filename} → {tmp_path} ({len(content)} bytes)")
    except Exception as e:
        raise HTTPException(500, detail=str(e))

    # 格式转换
    converted = None
    if suffix in CONVERT_EXTS:
        converted = convert_to_wav(tmp_path)
        if converted:
            logger.info(f"🔄 Converted {suffix} → WAV")
            tmp_path = converted

    # 转录
    try:
        t0 = time.time()
        result = transcribe(tmp_path, model=DEFAULT_MODEL)
        text = result.get("text", "").strip() if isinstance(result, dict) else str(result).strip()
        logger.info(f"✅ {time.time()-t0:.2f}s → \"{text[:80]}\"")
    except Exception as e:
        logger.error(f"❌ Transcription failed: {e}")
        raise HTTPException(500, detail=str(e))
    finally:
        for p in filter(None, [tmp_path, converted]):
            try:
                os.unlink(p)
            except OSError:
                pass

    if response_format == "text":
        return text
    return JSONResponse({"text": text})


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8787)
    p.add_argument("--model", default=None)
    a = p.parse_args()
    if a.model:
        DEFAULT_MODEL = a.model
    logger.info(f"🚀 http://{a.host}:{a.port}  model={DEFAULT_MODEL}")
    uvicorn.run(app, host=a.host, port=a.port)
