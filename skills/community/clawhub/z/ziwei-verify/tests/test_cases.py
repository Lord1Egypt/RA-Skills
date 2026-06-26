"""
tests/test_cases.py - 测试案例加载器
"""

import json
import os
from typing import Dict, List, Optional
from pathlib import Path

_test_cases_cache: Optional[List[Dict]] = None


def load_test_case(case_id: str) -> Optional[Dict]:
    """
    加载单个测试案例
    
    参数：
    - case_id: 案例ID（如 "TC001"）
    
    返回：测试案例字典，未找到返回 None
    """
    all_cases = load_all_test_cases()
    for case in all_cases:
        if case.get("case_id") == case_id:
            return case
    return None


def list_test_cases() -> List[str]:
    """
    列出所有测试案例ID
    
    返回：案例ID列表
    """
    all_cases = load_all_test_cases()
    return [case.get("case_id") for case in all_cases if case.get("case_id")]


def load_all_test_cases() -> List[Dict]:
    """
    加载所有测试案例（带缓存）
    
    返回：测试案例列表
    """
    global _test_cases_cache
    if _test_cases_cache is not None:
        return _test_cases_cache
    
    # 读取 JSON 文件
    test_file = Path(__file__).parent / "test_cases.json"
    try:
        with open(test_file, "r", encoding="utf-8") as f:
            content = f.read()
            # 支持多 JSON 对象（每行一个或直接数组）
            content = content.strip()
            if content.startswith("["):
                _test_cases_cache = json.loads(content)
            else:
                # 每行一个 JSON 对象
                cases = []
                for line in content.splitlines():
                    line = line.strip()
                    if line and not line.startswith("#"):
                        cases.append(json.loads(line))
                _test_cases_cache = cases
    except FileNotFoundError:
        logger.error(f"测试案例文件不存在: {test_file}")
        _test_cases_cache = []
    except json.JSONDecodeError as e:
        logger.error(f"测试案例 JSON 解析失败: {e}")
        _test_cases_cache = []
    
    return _test_cases_cache


def clear_test_cache():
    """清除测试案例缓存（用于测试）"""
    global _test_cases_cache
    _test_cases_cache = None


# 设置 logger
import logging
logger = logging.getLogger(__name__)
