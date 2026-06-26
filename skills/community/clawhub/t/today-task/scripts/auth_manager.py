#!/usr/bin/env python3
"""
授权码管理器 - OpenClaw配置系统版本
检测授权码并提示用户使用OpenClaw配置命令设置
"""

import re
import os
import logging
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

class AuthCodeManager:
    """授权码管理器 - 用于OpenClaw配置系统"""
    
    def __init__(self, config_path: str = None):
        """初始化授权码管理器"""
        # config_path参数保留但不使用，用于兼容性
        logger.info("授权码管理器初始化（OpenClaw配置系统版本）")
        
    def _get_openclaw_config_command(self, auth_code: str) -> str:
        """获取OpenClaw配置命令"""
        return f"openclaw config set skills.entries.today-task.config.authCode {auth_code}"
    
    def _is_likely_auth_code(self, text: str) -> bool:
        """判断文本是否可能是授权码"""
        if not text or not isinstance(text, str):
            return False
        
        # 授权码通常是字母数字组合，长度10-20
        text = text.strip()
        
        # 检查长度
        if len(text) < 10 or len(text) > 30:
            return False
        
        # 检查字符组成（主要是字母和数字）
        if not re.match(r'^[A-Za-z0-9_-]+$', text):
            return False
        
        return True
    
    def detect_auth_code(self, text: str) -> Optional[str]:
        """
        从文本中检测授权码
        
        授权码特征：
        1. 通常是一串字母数字组合
        2. 长度通常在10-20个字符
        3. 可能包含大小写字母和数字
        4. 用户可能会说"授权码是xxx"或"使用授权码xxx"
        """
        if not text or not isinstance(text, str):
            return None
        
        # 清理文本
        text = text.strip()
        
        # 模式1：直接匹配授权码格式（字母数字组合，长度10-30）
        auth_code_patterns = [
            r'授权码[：:]\s*([A-Za-z0-9_-]{10,30})',
            r'auth[：:]\s*([A-Za-z0-9_-]{10,30})',
            r'使用授权码\s*([A-Za-z0-9_-]{10,30})',
            r'我的授权码是\s*([A-Za-z0-9_-]{10,30})',
            r'授权码为\s*([A-Za-z0-9_-]{10,30})',
        ]
        
        for pattern in auth_code_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                auth_code = match.group(1)
                if self._is_likely_auth_code(auth_code):
                    return auth_code
        
        # 模式2：直接提取可能是授权码的字符串
        # 查找连续的字母数字组合，长度10-30
        direct_match = re.search(r'\b([A-Za-z0-9_-]{10,30})\b', text)
        if direct_match:
            candidate = direct_match.group(1)
            if self._is_likely_auth_code(candidate):
                # 检查上下文，确保不是其他内容
                context = text.lower()
                auth_keywords = ['授权码', 'auth', '码', 'code']
                if any(keyword in context for keyword in auth_keywords):
                    return candidate
        
        return None
    
    def update_auth_code(self, auth_code: str) -> Tuple[bool, str]:
        """
        检测到授权码，提示用户使用OpenClaw配置命令
        
        返回: (成功与否, 消息)
        """
        if not auth_code or not self._is_likely_auth_code(auth_code):
            return False, "授权码格式无效"
        
        try:
            # 生成OpenClaw配置命令
            config_command = self._get_openclaw_config_command(auth_code)
            
            message = f"检测到授权码: {auth_code[:4]}***\n\n"
            message += "请使用以下OpenClaw命令设置授权码:\n"
            message += f"{config_command}\n\n"
            message += "设置完成后，技能将使用新的授权码进行推送。"
            
            logger.info(f"检测到授权码，已生成OpenClaw配置命令")
            return True, message
            
        except Exception as e:
            error_msg = f"处理授权码时出错: {str(e)}"
            logger.error(error_msg)
            return False, error_msg

# 测试代码
if __name__ == "__main__":
    # 设置日志
    logging.basicConfig(level=logging.INFO)
    
    # 测试授权码管理器
    manager = AuthCodeManager()
    
    test_cases = [
        "我的授权码是 aqvIVhhWz7ir",
        "使用授权码 FrF2e6Pwqvpz",
        "授权码: NWrU7qbN8vvx",
        "auth: HO4hza2l9MYy",
        "这不是授权码",
        "请使用授权码abc123def456",
    ]
    
    print("测试授权码检测:")
    print("=" * 60)
    
    for text in test_cases:
        auth_code = manager.detect_auth_code(text)
        if auth_code:
            print(f"[SUCCESS] 检测到授权码: {text[:30]}...")
            print(f"   提取的授权码: {auth_code[:4]}***")
            
            # 测试更新
            success, message = manager.update_auth_code(auth_code)
            print(f"   更新结果: {'成功' if success else '失败'}")
            print(f"   消息: {message[:80]}...")
        else:
            print(f"[ERROR] 未检测到授权码: {text[:30]}...")
        
        print()