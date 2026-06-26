#!/usr/bin/env python3
"""
Voice Chat Bridge 完整流程入口：
1. 转写音频 → 文字
2. 调用 LLM 生成回复（使用当前会话的模型和上下文）
3. TTS 合成语音
4. 输出结果供 OpenClaw 发送

关键：通过 OPENCLAW_SESSION_ID 环境变量传递当前会话 ID，让 openclaw agent 命令复用当前会话的 LLM。
"""
from __future__ import annotations

import json
import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from transcribe_audio import transcribe, TranscriptionError
from reply_with_tts import synthesize_to_feishu_voice, TTSGenerationError

# 日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# 配置
OPENCLAW_GATEWAY_URL = os.environ.get('OPENCLAW_GATEWAY_URL', 'http://127.0.0.1:18789')
OPENCLAW_API_KEY = os.environ.get('OPENCLAW_API_KEY', '')
PYTHON_CMD = sys.executable


def call_openclaw_llm(user_text: str, system_prompt: str = "你是一个智能助手，根据用户的语音内容，给出简洁、有帮助的回复。") -> str:
    """
    调用 OpenClaw Agent 的 LLM 能力生成回复。
    
    关键：通过 --session-id 参数指定当前会话，让 Agent 复用该会话的模型和上下文。
    """
    session_id = os.environ.get('OPENCLAW_SESSION_ID')
    
    if not session_id:
        logger.warning("未设置 OPENCLAW_SESSION_ID，无法调用当前会话的 LLM，降级为简单回复")
        return f"收到：{user_text}。"
    
    try:
        cmd = [
            "openclaw", "agent",
            "--session-id", session_id,
            "--message", f"{system_prompt}\n\n用户语音内容：{user_text}\n\n请给出简洁、有帮助的回复。"
        ]
        
        logger.info(f"调用当前会话 LLM (session: {session_id})...")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=90
        )
        
        if result.returncode == 0:
            reply = result.stdout.strip()
            if reply:
                logger.info(f"LLM 回复成功：{reply[:100]}...")
                return reply
            else:
                logger.warning("LLM 返回空回复")
        else:
            stderr = result.stderr.strip() or "未知错误"
            logger.error(f"LLM 调用失败 (code {result.returncode}): {stderr[:200]}")
            
    except subprocess.TimeoutExpired:
        logger.error("LLM 调用超时（90 秒）")
    except Exception as e:
        logger.error(f"LLM 调用异常：{e}")
    
    # 降级
    return f"收到：{user_text}。"


def process_voice_message(
    audio_path: str,
    system_prompt: Optional[str] = None
) -> dict:
    """
    处理语音消息的完整流程。
    """
    audio_path = Path(audio_path).resolve()
    
    if not audio_path.exists():
        return {"status": "error", "error": f"音频文件不存在：{audio_path}"}
    
    try:
        # 步骤 1: 转写
        logger.info(f"开始转写：{audio_path}")
        transcript = transcribe(str(audio_path))
        if not transcript:
            return {"status": "error", "error": "转写结果为空"}
        logger.info(f"转写结果：{transcript}")
        
        # 步骤 2: LLM 生成回复
        logger.info("调用 LLM 生成回复...")
        reply = call_openclaw_llm(transcript, system_prompt)
        logger.info(f"LLM 回复：{reply}")
        
        # 步骤 3: TTS 合成
        logger.info("开始 TTS 合成...")
        voice_path = synthesize_to_feishu_voice(reply)
        logger.info(f"语音文件：{voice_path}")
        
        return {
            "status": "ok",
            "transcript": transcript,
            "reply": reply,
            "voice_path": str(voice_path)
        }
        
    except TranscriptionError as e:
        logger.error(f"转写失败：{e}")
        return {"status": "error", "error": f"转写失败：{e}"}
    except TTSGenerationError as e:
        logger.error(f"TTS 失败：{e}")
        return {"status": "error", "error": f"TTS 失败：{e}"}
    except Exception as e:
        logger.exception(f"未预期错误：{e}")
        return {"status": "error", "error": f"未预期错误：{e}"}


def main():
    """命令行入口点"""
    if len(sys.argv) < 2:
        print("Usage: run_voice_chat.py <audio_file_path> [system_prompt]", file=sys.stderr)
        sys.exit(1)
    
    audio_file = sys.argv[1]
    system_prompt = sys.argv[2] if len(sys.argv) > 2 else None
    
    result = process_voice_message(audio_file, system_prompt)
    
    # 输出 JSON
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    if result["status"] == "error":
        sys.exit(1)


if __name__ == "__main__":
    main()
