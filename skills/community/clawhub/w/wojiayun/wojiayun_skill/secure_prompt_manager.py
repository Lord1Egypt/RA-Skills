"""
安全提示词管理器
系统提示词加密存储，防止用户查看和篡改
"""

import base64
import json
import os
from datetime import datetime

try:
    from .crypto_utils import encrypt_value, decrypt_value, get_crypto
except ImportError:
    from crypto_utils import encrypt_value, decrypt_value, get_crypto


class SecurePromptManager:
    """安全提示词管理器"""
    
    # 提示词存储文件
    PROMPT_FILE = "e:\\workbuddy\\wy\\.secure_prompts"
    
    def __init__(self):
        """初始化提示词管理器"""
        self._prompts = {}
        self._load_prompts()
    
    def _load_prompts(self):
        """从文件加载提示词"""
        if os.path.exists(self.PROMPT_FILE):
            try:
                with open(self.PROMPT_FILE, 'r', encoding='utf-8') as f:
                    self._prompts = json.load(f)
            except:
                self._prompts = {}
    
    def _save_prompts(self):
        """保存提示词到文件"""
        with open(self.PROMPT_FILE, 'w', encoding='utf-8') as f:
            json.dump(self._prompts, f, ensure_ascii=False, indent=2)
    
    def store_prompt(self, prompt_name: str, prompt_text: str, description: str = ""):
        """存储提示词（加密）"""
        encrypted = encrypt_value(prompt_text)
        
        self._prompts[prompt_name] = {
            "encrypted": encrypted,
            "description": description,
            "created_at": datetime.now().isoformat()
        }
        
        self._save_prompts()
    
    def get_prompt(self, prompt_name: str) -> str:
        """获取提示词（解密）"""
        if prompt_name not in self._prompts:
            return None
        
        try:
            encrypted = self._prompts[prompt_name]["encrypted"]
            return decrypt_value(encrypted)
        except Exception as e:
            return None
    
    def list_prompts(self) -> list:
        """列出所有提示词名称"""
        return list(self._prompts.keys())


# 全局实例
_prompt_manager = None


def get_prompt_manager() -> SecurePromptManager:
    """获取全局提示词管理器实例"""
    global _prompt_manager
    if _prompt_manager is None:
        _prompt_manager = SecurePromptManager()
    return _prompt_manager


class SecureAIWrapper:
    """安全 AI 包装器"""
    
    def __init__(self):
        self._pm = get_prompt_manager()
    
    def get_system_prompt(self) -> str:
        """获取系统提示词"""
        prompt = self._pm.get_prompt("system")
        if not prompt:
            # 默认提示词
            prompt = "你是一个专业的设备管理助手。"
        return prompt
