# -*- coding: utf-8 -*-
"""
参数识别器 - V3.0

从对话中自动识别用户输入的值，变成可配置参数
"""

import re
from typing import Dict, Any, List, Optional
from datetime import datetime


class ParamRecognizer:
    """参数识别器"""
    
    def __init__(self):
        # 常见参数名模式
        self.param_name_patterns = [
            r'关键词 [=:]\s*["\']?([^"\'\n,]+)["\']?',
            r'keyword[=:]\s*["\']?([^"\'\n,]+)["\']?',
            r'城市 [=:]\s*["\']?([^"\'\n,]+)["\']?',
            r'city[=:]\s*["\']?([^"\'\n,]+)["\']?',
            r'数量 [=:]\s*(\d+)',
            r'limit[=:]\s*(\d+)',
            r'频率 [=:]\s*["\']?([^"\'\n,]+)["\']?',
            r'frequency[=:]\s*["\']?([^"\'\n,]+)["\']?',
            r'路径 [=:]\s*["\']?([^"\'\n,]+)["\']?',
            r'path[=:]\s*["\']?([^"\'\n,]+)["\']?',
            r'保存 [到至]\s*["\']?([^"\'\n,]+)["\']?',
            r'输出 [到至]\s*["\']?([^"\'\n,]+)["\']?',
        ]
    
    def recognize_params(self, conversation: List[Dict[str, str]], 
                         execution_chain: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        从对话中识别参数
        
        Args:
            conversation: 对话历史
            execution_chain: 执行链（用于提取函数参数）
            
        Returns:
            参数字典
        """
        params = {}
        
        # 1. 从用户消息中提取显式参数
        for msg in conversation:
            if msg.get("role") == "user":
                content = msg.get("content", "")
                extracted = self._extract_from_text(content)
                params.update(extracted)
        
        # 2. 从执行链中提取函数参数
        for step in execution_chain:
            func_params = step.get("params", {})
            for key, value in func_params.items():
                if key not in params:  # 用户显式输入优先
                    params[key] = value
        
        # 3. 添加元参数
        params["_generated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        params["_step_count"] = len(execution_chain)
        
        return params
    
    def _extract_from_text(self, text: str) -> Dict[str, Any]:
        """从文本中提取参数"""
        params = {}
        
        for pattern in self.param_name_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                # 根据模式推断参数名
                param_name = self._infer_param_name(pattern, match)
                if param_name:
                    params[param_name] = self._convert_value(match)
        
        # 提取通用的 key=value 格式
        kv_pattern = r'(\w+)\s*=\s*["\']?([^"\'\n,]+)["\']?'
        matches = re.findall(kv_pattern, text)
        for key, value in matches:
            if key not in params:
                params[key] = self._convert_value(value)
        
        return params
    
    def _infer_param_name(self, pattern: str, value: str) -> Optional[str]:
        """根据模式推断参数名"""
        if "关键词" in pattern or "keyword" in pattern:
            return "keyword"
        elif "城市" in pattern or "city" in pattern:
            return "city"
        elif "数量" in pattern or "limit" in pattern:
            return "limit"
        elif "频率" in pattern or "frequency" in pattern:
            return "frequency"
        elif "路径" in pattern or "path" in pattern:
            return "path"
        elif "保存" in pattern or "输出" in pattern:
            return "output_file"
        return None
    
    def _convert_value(self, value: str) -> Any:
        """转换参数值类型"""
        value = value.strip()
        
        # 尝试整数
        try:
            return int(value)
        except ValueError:
            pass
        
        # 尝试浮点数
        try:
            return float(value)
        except ValueError:
            pass
        
        # 布尔值
        if value.lower() == "true":
            return True
        elif value.lower() == "false":
            return False
        
        # 去除引号
        if (value.startswith('"') and value.endswith('"')) or \
           (value.startswith("'") and value.endswith("'")):
            value = value[1:-1]
        
        return value


def recognize_params(conversation: List[Dict[str, str]], 
                     execution_chain: List[Dict[str, Any]]) -> Dict[str, Any]:
    """便捷函数：识别参数"""
    recognizer = ParamRecognizer()
    return recognizer.recognize_params(conversation, execution_chain)


# 测试
if __name__ == "__main__":
    test_conversation = [
        {"role": "user", "content": "帮我搜索 AI 相关新闻，keyword=AI, limit=10"},
        {"role": "assistant", "content": "已调用 skill_search(keyword='AI', limit=10)"},
        {"role": "user", "content": "保存到 result.csv"},
        {"role": "assistant", "content": "已调用 tool_file_save(data, path='result.csv')"}
    ]
    
    chain = [
        {"name": "skill_search", "params": {"keyword": "AI", "limit": 10}},
        {"name": "tool_file_save", "params": {"path": "result.csv"}}
    ]
    
    params = recognize_params(test_conversation, chain)
    print("识别的参数:")
    for key, value in params.items():
        if not key.startswith("_"):
            print(f"  {key}: {value}")
