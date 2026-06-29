from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def review_code(
    code: str,
    style: Optional[str] = None,
    commitMessage: Optional[str] = None
) -> Dict[str, Any]:
    """
    构建用于代码整体审查与打分的 LLM 提示词（不直接调用 LLM）
    
    Args:
        code: 待审查的代码文本
        style: 审查风格，可选
        commitMessage: 可选的提交信息
    
    Returns:
        
    """
    arguments = {
        "code": code,
        "style": style,
        "commitMessage": commitMessage
    }
    
    return call_api("1777316659306499", "review_code", arguments)

def review_diff(
    diff: str,
    style: Optional[str] = None,
    commitMessage: Optional[str] = None
) -> Dict[str, Any]:
    """
    构建用于 Git diff 变更审查与打分的 LLM 提示词（不直接调用 LLM）
    
    Args:
        diff: git diff 内容
        style: 审查风格，可选
        commitMessage: 可选的提交信息
    
    Returns:
        
    """
    arguments = {
        "diff": diff,
        "style": style,
        "commitMessage": commitMessage
    }
    
    return call_api("1777316659306499", "review_diff", arguments)

def review_file(
    filePath: str,
    content: str,
    style: Optional[str] = None,
    commitMessage: Optional[str] = None
) -> Dict[str, Any]:
    """
    构建用于单文件审查与打分的 LLM 提示词（不直接调用 LLM）
    
    Args:
        filePath: 文件路径
        content: 文件内容
        style: 审查风格，可选
        commitMessage: 可选的提交信息
    
    Returns:
        
    """
    arguments = {
        "filePath": filePath,
        "content": content,
        "style": style,
        "commitMessage": commitMessage
    }
    
    return call_api("1777316659306499", "review_file", arguments)

def parse_review_score(
    reviewText: str
) -> Dict[str, Any]:
    """
    从审查文本中解析评分（提取 '总分:XX分' 格式）
    
    Args:
        reviewText: 审查文本，应包含 '总分:XX分' 格式的评分
    
    Returns:
        
    """
    arguments = {
        "reviewText": reviewText
    }
    
    return call_api("1777316659306499", "parse_review_score", arguments)

