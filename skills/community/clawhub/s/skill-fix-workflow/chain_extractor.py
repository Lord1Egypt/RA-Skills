# -*- coding: utf-8 -*-
"""
执行链提取器 - V3.0

从对话历史中提取 Skill/Tool/Function 调用序列
"""

import re
from typing import List, Dict, Any, Optional
from datetime import datetime


class ChainExtractor:
    """执行链提取器"""
    
    def __init__(self):
        # 识别 Skill/Tool 调用的正则模式
        self.call_patterns = [
            # skill_xxx() 或 tool_xxx()
            r'(skill_\w+)\s*\(([^)]*)\)',
            r'(tool_\w+)\s*\(([^)]*)\)',
            # function_xxx()
            r'(function_\w+)\s*\(([^)]*)\)',
            # 通用函数调用
            r'(\w+_search)\s*\(([^)]*)\)',
            r'(\w+_fetch)\s*\(([^)]*)\)',
            r'(\w+_save)\s*\(([^)]*)\)',
            r'(\w+_post)\s*\(([^)]*)\)',
            r'(\w+_publish)\s*\(([^)]*)\)',
        ]
        
        # 识别用户输入值的模式
        self.input_patterns = [
            # key=value
            r'(\w+)\s*=\s*["\']?([^"\',\)]+)["\']?',
            # "xxx" 或 'xxx'
            r'["\']([^"\']+)["\']',
            # 数字
            r'\b(\d+)\b',
        ]
    
    def extract_chain(self, conversation: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """
        从对话中提取执行链
        
        Args:
            conversation: 对话历史 [{"role": "user/assistant", "content": "..."}]
            
        Returns:
            执行链 [{"step": 1, "type": "skill/tool/function", "name": "...", "params": {...}}]
        """
        chain = []
        step = 0
        
        for msg in conversation:
            role = msg.get("role", "")
            content = msg.get("content", "")
            
            if role == "assistant":
                # 从助手消息中提取 Skill/Tool 调用
                calls = self._extract_calls(content)
                for call in calls:
                    step += 1
                    call["step"] = step
                    call["source"] = content
                    chain.append(call)
        
        return chain
    
    def _extract_calls(self, content: str) -> List[Dict[str, Any]]:
        """从内容中提取函数调用"""
        calls = []
        
        for pattern in self.call_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                func_name = match[0]
                params_str = match[1] if len(match) > 1 else ""
                
                # 解析参数
                params = self._parse_params(params_str)
                
                calls.append({
                    "type": self._get_call_type(func_name),
                    "name": func_name,
                    "params": params,
                    "raw": f"{func_name}({params_str})"
                })
        
        return calls
    
    def _get_call_type(self, func_name: str) -> str:
        """判断调用类型"""
        if func_name.startswith("skill_"):
            return "skill"
        elif func_name.startswith("tool_"):
            return "tool"
        elif func_name.startswith("function_"):
            return "function"
        else:
            return "call"
    
    def _parse_params(self, params_str: str) -> Dict[str, Any]:
        """解析函数字符串中的参数"""
        params = {}
        
        if not params_str.strip():
            return params
        
        # 解析 key=value 格式
        kv_pattern = r'(\w+)\s*=\s*["\']?([^"\',\)]+)["\']?'
        matches = re.findall(kv_pattern, params_str)
        
        for key, value in matches:
            # 尝试转换类型
            params[key] = self._convert_value(value.strip())
        
        # 如果没有 key=value，尝试提取位置参数
        if not params:
            # 提取字符串值
            str_matches = re.findall(r'["\']([^"\']+)["\']', params_str)
            for i, val in enumerate(str_matches):
                params[f"arg{i}"] = val
            
            # 提取数字值
            num_matches = re.findall(r'\b(\d+)\b', params_str)
            for i, val in enumerate(num_matches):
                params[f"num{i}"] = int(val)
        
        return params
    
    def _convert_value(self, value: str) -> Any:
        """转换参数值类型"""
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
        
        # 默认字符串
        return value


def extract_execution_chain(conversation: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """便捷函数：提取执行链"""
    extractor = ChainExtractor()
    return extractor.extract_chain(conversation)


# 测试
if __name__ == "__main__":
    test_conversation = [
        {"role": "user", "content": "帮我搜索 AI 相关新闻，limit=10"},
        {"role": "assistant", "content": "已调用 skill_search(keyword='AI', limit=10)"},
        {"role": "user", "content": "保存到 result.csv"},
        {"role": "assistant", "content": "已调用 tool_file_save(data, path='result.csv')"}
    ]
    
    chain = extract_execution_chain(test_conversation)
    print("提取的执行链:")
    for step in chain:
        print(f"  步骤{step['step']}: {step['type']}.{step['name']}({step['params']})")
