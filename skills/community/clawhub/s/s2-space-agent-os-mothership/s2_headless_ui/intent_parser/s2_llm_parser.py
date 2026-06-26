#!/usr/bin/env python3
import json
import logging
import requests

# =====================================================================
# 🧠 S2-SP-OS: Semantic Intent Parser (V2.0 Real LLM Edition)
# 真实大模型引擎：彻底移除硬编码，100% 依赖本地大模型实时推理
# =====================================================================
# 🔌 [极客连接指引]
# 1. 本代码默认连接本地 Ollama 引擎。请先在主机安装 Ollama (https://ollama.com/)
# 2. 在终端运行 `ollama run llama3:8b` 下载并启动模型。
# 3. 如果你想使用你之前的 LM Studio (对应 http://localhost:1234/v1)，
#    只需将下方的 ollama_url 替换，并调整请求 JSON 结构为 OpenAI 格式即可。
# =====================================================================

class S2RealIntentParser:
    def __init__(self, ollama_url="http://localhost:11434/api/generate", model="llama3:8b"):
        self.logger = logging.getLogger("S2_LLM_Parser")
        self.ollama_url = ollama_url
        self.model = model

    def parse_to_syscall(self, voice_text: str, current_memzero_context: dict) -> dict:
        """【真实调用】请求本地大模型进行意图解析，并强制输出 JSON"""
        
        # 构造给 LLM 的 System Prompt (系统提示词)
        prompt = f"""
        你是一个空间操作系统 (S2-SP-OS) 的底层逻辑解析器。
        当前空间多模态传感器状态: {json.dumps(current_memzero_context, ensure_ascii=False)}
        人类语音指令: "{voice_text}"
        
        你必须严格输出 JSON 格式，不要包含任何 markdown 标记或额外解释。
        JSON 结构示例: 
        {{
            "is_valid": true,
            "action_intent": "Set_Temperature",
            "target_skills": [{{"skill": "s2-hvac-perception", "intent": "Set_Temperature", "params": {{"target_temp": 24}}}}],
            "verbal_feedback": "已为您调低温度。"
        }}
        """
        
        try:
            self.logger.info(f"🚀 正向本地模型 [{self.model}] 发起推理请求...")
            response = requests.post(self.ollama_url, json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "format": "json" # 强制模型结构化输出
            }, timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                return json.loads(result["response"])
            else:
                self.logger.error(f"❌ LLM API 返回异常状态码: {response.status_code}")
                return {"is_valid": False, "error": "LLM 推理异常"}
                
        except requests.exceptions.RequestException as e:
            self.logger.critical(f"🛑 大模型引擎宕机或连接失败: {str(e)}")
            return {"is_valid": False, "error": "LLM 引擎离线"}