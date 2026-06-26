from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
import uuid
from pathlib import Path


def load_env_file():
    """
    在 server/app.py 直接运行时，自动回填项目根目录 .env 中的配置。
    """
    repo_root = Path(__file__).resolve().parent.parent
    env_path = Path(os.getenv("TTS_CONFIG_FILE", str(repo_root / ".env")))
    if not env_path.exists():
        return

    with env_path.open("r", encoding="utf-8") as f:
        for line in f:
            raw = line.strip()
            if not raw or raw.startswith("#") or "=" not in raw:
                continue
            key, value = raw.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


def env_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except Exception:
        return default


load_env_file()

# 全局环境变数锁定：在导入任何大模型之前注入这个限制
os.environ["HF_HOME"] = os.path.expanduser("~/.openclaw/models/voice-clone")
os.environ["MODELSCOPE_CACHE"] = os.path.expanduser("~/.openclaw/models/voice-clone")

import core_tts

app = FastAPI(title="OpenClaw Voice Clone Backend")

# 在独立后端的根目录下建立专门缓冲生成音频的桶
OUTPUT_DIR = os.path.join(os.getcwd(), "generated_audio")
os.makedirs(OUTPUT_DIR, exist_ok=True)

class CloneRequest(BaseModel):
    text: str
    ref_audio_path: Optional[str] = None
    speed: float = 1.0
    output_dir: Optional[str] = None

@app.on_event("startup")
def load_heavy_models():
    """
    当这台服务器启动时，立即进行巨无霸语音模型的重量级加载，
    并且从 ~/.openclaw/models/voice-clone 读取预加载的 Checkpoints。
    """
    print("=== 开始加载大型权重至内存与 GPU，请勿关闭本控制台 ===")
    core_tts.initialize_models()
    print("=== 加载完毕！模型就位完毕，可以开始服务 ===")

@app.post("/clone")
def clone_voice(req: CloneRequest):
    """
    生成音频的核心路由：
    - 读取前端抛出的文字
    - 调用 core_tts 完成大模型音频生成
    - 确保它转码成最友好的 ogg 返给调用方
    """
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text is empty.")
    
    # 决定输出路径
    target_dir = OUTPUT_DIR
    if req.output_dir:
        os.makedirs(req.output_dir, exist_ok=True)
        target_dir = req.output_dir
        
    # 获取唯一的生成 ID
    request_id = uuid.uuid4().hex[:8]
    output_filename = os.path.abspath(os.path.join(target_dir, f"reply_{request_id}.ogg"))
    
    try:
        # 下发至核心逻辑层
        success = core_tts.generate_voice(
            text=req.text,
            ref_audio=req.ref_audio_path,
            output_path=output_filename,
            speed=req.speed
        )
        
        if success and os.path.exists(output_filename):
            print(f"[/clone] 成功组装出用户声音的回答包：{output_filename}")
            return {"status": "success", "output_audio_path": output_filename}
        else:
            raise HTTPException(status_code=500, detail="Engine failed to output local audio file.")
            
    except Exception as e:
        print(f"[/clone] 崩溃：由于计算或音频包出错，异常内容为: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("TTS_SERVER_HOST", "127.0.0.1")
    port = env_int("TTS_SERVER_PORT", 8000)
    print(f"[app] 启动地址: http://{host}:{port}")
    uvicorn.run(app, host=host, port=port)
