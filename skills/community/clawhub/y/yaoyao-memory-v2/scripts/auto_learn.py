#!/usr/bin/env python3
"""自动学习器 - 根据错误自动学习改进
功能：
1. 错误模式识别
2. 自动记录到 ERRORS.md
3. 生成改进建议
4. 周期性自检
"""
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

ERRORS_FILE = Path.home() / ".openclaw" / "workspace" / ".learnings" / "ERRORS.md"
LEARNINGS_FILE = Path.home() / ".openclaw" / "workspace" / ".learnings" / "LEARNINGS.md"

class ErrorPattern:
    """错误模式"""
    
    PATTERNS = [
        (r"Permission denied", "权限问题", "检查文件权限设置"),
        (r"Connection timeout", "网络超时", "增加超时时间或重试"),
        (r"File not found", "文件缺失", "检查文件路径是否正确"),
        (r"JSON decode error", "JSON解析失败", "检查JSON格式是否正确"),
        (r"Module not found", "模块缺失", "检查依赖是否安装"),
        (r"SyntaxError", "语法错误", "检查代码语法"),
        (r"ImportError", "导入错误", "检查模块路径和导入语句"),
    ]
    
    @classmethod
    def match(cls, error_msg: str) -> Optional[Dict]:
        """匹配错误模式"""
        for pattern, error_type, suggestion in cls.PATTERNS:
            if re.search(pattern, error_msg, re.IGNORECASE):
                return {
                    "type": error_type,
                    "suggestion": suggestion
                }
        return None


class AutoLearner:
    """自动学习器"""
    
    def __init__(self):
        self.errors = []
        self.learnings = []
    
    def record_error(self, error_msg: str, context: str = ""):
        """记录错误"""
        pattern = ErrorPattern.match(error_msg)
        
        error_entry = {
            "timestamp": datetime.now().isoformat(),
            "error": error_msg[:100],
            "context": context,
            "pattern": pattern
        }
        
        self.errors.append(error_entry)
        
        # 如果匹配到模式，也记录到 ERRORS.md
        if pattern:
            self._update_errors_md(error_entry)
        
        return pattern
    
    def _update_errors_md(self, entry: Dict):
        """更新 ERRORS.md"""
        if not ERRORS_FILE.exists():
            ERRORS_FILE.parent.mkdir(parents=True, exist_ok=True)
            ERRORS_FILE.write_text("# ERRORS.md\n\n> 错误记录\n\n---\n\n")
        
        content = ERRORS_FILE.read_text()
        
        new_entry = f"""
### {entry['timestamp']}
- **错误**: {entry['error']}
- **类型**: {entry['pattern']['type']}
- **建议**: {entry['pattern']['suggestion']}
- **上下文**: {entry['context'] or 'N/A'}
"""
        
        # 插入到标记位置后
        if "## 错误记录" in content:
            content = content.replace(
                "## 错误记录\n",
                "## 错误记录\n" + new_entry
            )
        
        ERRORS_FILE.write_text(content)
    
    def generate_learnings(self) -> List[str]:
        """根据错误模式生成学习建议"""
        learnings = []
        
        # 统计错误类型
        error_types = {}
        for e in self.errors:
            if e["pattern"]:
                ptype = e["pattern"]["type"]
                error_types[ptype] = error_types.get(ptype, 0) + 1
        
        # 生成建议
        for etype, count in error_types.items():
            if count >= 3:
                learnings.append(f"频繁出现 {etype} ({count}次)，需要系统性改进")
        
        return learnings
    
    def auto_check(self) -> Dict:
        """自动检查"""
        results = {
            "timestamp": datetime.now().isoformat(),
            "errors_recorded": len(self.errors),
            "patterns_found": len([e for e in self.errors if e["pattern"]]),
            "learnings": self.generate_learnings()
        }
        
        return results


if __name__ == "__main__":
    learner = AutoLearner()
    
    # 测试错误识别
    test_errors = [
        "Permission denied: /path/to/file",
        "Connection timeout after 30s",
        "Module not found: numpy",
        "Unknown error occurred"
    ]
    
    print("=== 自动学习测试 ===\n")
    
    for err in test_errors:
        pattern = learner.record_error(err, "test context")
        if pattern:
            print(f"识别: {err[:40]}...")
            print(f"  类型: {pattern['type']}")
            print(f"  建议: {pattern['suggestion']}\n")
        else:
            print(f"未识别: {err}\n")
    
    # 自动检查
    results = learner.auto_check()
    print(f"\n自动检查结果:")
    print(f"  记录错误: {results['errors_recorded']}")
    print(f"  识别模式: {results['patterns_found']}")
    print(f"  学习建议: {len(results['learnings'])} 条")
