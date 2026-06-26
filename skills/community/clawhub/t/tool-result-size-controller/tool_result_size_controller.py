# -*- coding: utf-8 -*-
"""
Tool结果大小控制器
基于Claude Code maxResultSizeChars机制实现

核心设计：
- 大结果自动落盘，保护上下文窗口
- 智能阈值判断（默认10000字符）
- 文件路径回显而非完整内容
- 自动清理过期文件
"""

import json
import gzip
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Union, Any
from dataclasses import dataclass

# 配置
RESULTS_DIR = Path.home() / ".openclaw" / "workspace" / "tmp" / "tool-results"
DEFAULT_THRESHOLD = 10000  # 字符阈值
MAX_AGE_DAYS = 7  # 文件保留7天

def ensure_results_dir():
    """确保结果目录存在"""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    return RESULTS_DIR

def get_result_path(tool_name: str, content_hash: str) -> Path:
    """生成结果文件路径"""
    date_str = datetime.now().strftime("%Y%m%d")
    return RESULTS_DIR / f"{tool_name}-{date_str}-{content_hash[:8]}.json.gz"

def should_spill_to_disk(content: Union[str, dict, list], threshold: int = DEFAULT_THRESHOLD) -> bool:
    """
    判断是否应该落盘
    
    参考Claude Code的maxResultSizeChars机制
    """
    if isinstance(content, str):
        return len(content) > threshold
    elif isinstance(content, (dict, list)):
        # 估算JSON序列化后的字符数
        return len(json.dumps(content, ensure_ascii=False)) > threshold
    return False

def spill_to_disk(tool_name: str, content: Union[str, dict, list], compress: bool = True) -> dict:
    """
    将大结果写入磁盘
    
    Returns:
        {
            "spilled": True,
            "file_path": "path/to/file.json.gz",
            "size_chars": 15000,
            "size_bytes": 4500,
            "content_hash": "a1b2c3d4",
            "preview": "前500字符预览..."
        }
    """
    ensure_results_dir()
    
    # 序列化内容
    if isinstance(content, str):
        content_str = content
    else:
        content_str = json.dumps(content, ensure_ascii=False, indent=2)
    
    # 计算hash和路径
    content_hash = hashlib.md5(content_str.encode()).hexdigest()
    result_path = get_result_path(tool_name, content_hash)
    
    # 写入文件
    if compress:
        with gzip.open(result_path, 'wt', encoding='utf-8') as f:
            f.write(content_str)
    else:
        result_path = result_path.with_suffix('.json')
        with open(result_path, 'w', encoding='utf-8') as f:
            f.write(content_str)
    
    # 获取文件大小
    size_bytes = result_path.stat().st_size
    
    return {
        "spilled": True,
        "file_path": str(result_path),
        "size_chars": len(content_str),
        "size_bytes": size_bytes,
        "content_hash": content_hash[:8],
        "preview": content_str[:500] + ("..." if len(content_str) > 500 else "")
    }

def load_spilled_result(file_path: str) -> Union[str, dict, list]:
    """从磁盘加载结果"""
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"Result file not found: {file_path}")
    
    if path.suffix == '.gz':
        with gzip.open(path, 'rt', encoding='utf-8') as f:
            content = f.read()
    else:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    
    # 尝试解析JSON
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return content

def cleanup_old_results(max_age_days: int = MAX_AGE_DAYS) -> int:
    """清理过期结果文件"""
    if not RESULTS_DIR.exists():
        return 0
    
    cutoff = datetime.now() - timedelta(days=max_age_days)
    deleted_count = 0
    
    for file_path in RESULTS_DIR.glob("*"):
        if file_path.is_file():
            mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
            if mtime < cutoff:
                file_path.unlink()
                deleted_count += 1
    
    return deleted_count

class ToolResultWrapper:
    """
    Tool结果包装器
    
    参考Claude Code Tool返回值的maxResultSizeChars处理
    """
    
    def __init__(self, tool_name: str, threshold: int = DEFAULT_THRESHOLD):
        self.tool_name = tool_name
        self.threshold = threshold
    
    def wrap(self, result: Any) -> Union[Any, dict]:
        """
        包装结果，大结果自动落盘
        """
        if should_spill_to_disk(result, self.threshold):
            return spill_to_disk(self.tool_name, result)
        return result
    
    def __call__(self, func):
        """
        装饰器用法
        
        @ToolResultWrapper("my_tool", threshold=5000)
        def my_tool_func(*args, **kwargs):
            return large_result
        """
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return self.wrap(result)
        return wrapper

# 便捷函数
def maybe_spill(result: Any, tool_name: str = "unknown", threshold: int = DEFAULT_THRESHOLD) -> Union[Any, dict]:
    """
    便捷函数：可能需要落盘
    
    使用示例：
        result = maybe_spill(large_data, "search_results")
        if isinstance(result, dict) and result.get("spilled"):
            print(f"结果已落盘：{result['file_path']}")
        else:
            print(f"结果：{result}")
    """
    wrapper = ToolResultWrapper(tool_name, threshold)
    return wrapper.wrap(result)

if __name__ == "__main__":
    # 测试
    print("Tool Result Size Controller")
    print(f"Results dir: {ensure_results_dir()}")
    
    # 测试小结果不落盘
    small_result = {"key": "value"}
    wrapped = maybe_spill(small_result, "test_tool")
    print(f"Small result: {wrapped}")
    
    # 测试大结果落盘
    large_result = "x" * 15000
    wrapped = maybe_spill(large_result, "test_tool")
    print(f"Large result: {wrapped.get('file_path', 'not spilled')}")
    print(f"Size chars: {wrapped.get('size_chars', len(str(wrapped)))}")
