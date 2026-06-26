#!/usr/bin/env python3
"""
Local STT API Server
将 qwen-asr 封装为 OpenAI 兼容格式
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI(title="Local STT", version="1.0.0")

# qwen-asr 脚本路径
QWEN_ASR_SCRIPT = "/Users/reks/.openclaw/skills/qwen-asr/scripts/main.py"


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/v1/audio/transcriptions")
async def transcribe(
    file: UploadFile = File(...),
    model: str = Form("qwen-asr")
):
    """OpenAI 兼容的转录端点"""
    
    # 检查文件类型
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # 创建临时文件
    suffix = Path(file.filename).suffix or ".wav"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp_path = tmp.name
        # 写入上传的文件内容
        content = await file.read()
        tmp.write(content)
    
    try:
        # 调用 qwen-asr
        result = subprocess.run(
            [
                sys.executable,  # 使用当前 Python 解释器
                "-m", "uv", "run",
                QWEN_ASR_SCRIPT,
                "-f", tmp_path
            ],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(Path(QWEN_ASR_SCRIPT).parent.parent)
        )
        
        if result.returncode != 0:
            raise HTTPException(
                status_code=500, 
                detail=f"STT failed: {result.stderr}"
            )
        
        text = result.stdout.strip()
        if not text:
            text = ""
            
        # OpenAI 格式返回
        return JSONResponse({
            "text": text
        })
        
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="STT timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # 清理临时文件
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


if __name__ == "__main__":
    print("Starting Local STT server on http://localhost:8787")
    uvicorn.run(app, host="0.0.0.0", port=8787)
