"""FastAPI server compatible with OpenAI Whisper API format."""
import os
import tempfile
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from faster_whisper import WhisperModel

app = FastAPI()

# Preload model on startup
_model_name = os.getenv("WHISPER_MODEL", "base")
print(f"Loading Whisper model: {_model_name}...")
whisper_model = WhisperModel(_model_name, device="cpu", compute_type="int8")
print("Model loaded successfully!")

@app.post("/v1/audio/transcriptions")
async def transcribe(
    file: UploadFile = File(...),
    model: str = Form("whisper-1"),
    language: str = Form(None),
    response_format: str = Form("json")
):
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    
    try:
        segments, info = whisper_model.transcribe(tmp_path, language=language)
        
        segments_list = []
        full_text = []
        for seg in segments:
            segments_list.append({
                "id": seg.id,
                "start": seg.start,
                "end": seg.end,
                "text": seg.text
            })
            full_text.append(seg.text)
        
        text = " ".join(full_text)
        
        if response_format == "text":
            return text
        elif response_format == "verbose_json":
            return JSONResponse({
                "text": text,
                "segments": segments_list,
                "language": info.language
            })
        else:
            return JSONResponse({"text": text})
    finally:
        os.unlink(tmp_path)

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8765)
