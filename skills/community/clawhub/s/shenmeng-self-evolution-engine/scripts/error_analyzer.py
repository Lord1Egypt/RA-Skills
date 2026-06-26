#!/usr/bin/env python3
"""
错误分析器 - 分析Skill执行错误，找出根本原因

用法:
    # 分析最近7天的错误
    python error_analyzer.py --skill my-skill --analyze
    
    # 生成修复建议
    python error_analyzer.py --skill my-skill --fix-suggestions
"""

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from collections import defaultdict


class ErrorAnalyzer:
    """错误分析器"""
    
    def __init__(self, skill_name: str, data_dir: str = "logs"):
        self.skill_name = skill_name
        self.data_dir = Path(data_dir)
        
        # 错误模式库
        self.error_patterns = {
            "FileNotFoundError": {
                "pattern": r"FileNotFoundError.*No such file or directory: '([^']+)'",
                "category": "文件错误",
                "suggestion": "检查文件路径是否存在，或添加路径创建逻辑"
            },
            "PermissionError": {
                "pattern": r"PermissionError.*Permission denied",
                "category": "权限错误",
                "suggestion": "检查文件/目录权限，或调整操作用户"
            },
            "ConnectionError": {
                "pattern": r"ConnectionError|Max retries exceeded|Connection refused",
                "category": "网络错误",
                "suggestion": "检查网络连接，添加重试机制和超时设置"
            },
            "TimeoutError": {
                "pattern": r"TimeoutError|timed out",
                "category": "超时错误",
                "suggestion": "增加超时时间，或优化请求处理速度"
            },
            "JSONDecodeError": {
                "pattern": r"JSONDecodeError|Expecting.*delimiter",
                "category": "数据解析错误",
                "suggestion": "检查返回数据格式，添加异常处理"
            },
            "KeyError": {
                "pattern": r"KeyError: '([^']+)'",
                "category": "键错误",
                "suggestion": "检查字典键是否存在，使用.get()方法"
            },
            "IndexError": {
                "pattern": r"IndexError:.*index out of range",
                "category": "索引错误",
                "suggestion": "检查列表长度，避免越界访问"
            },
            "AttributeError": {
                "pattern": r"AttributeError: '([^']+)' object has no attribute '([^']+)'",
                "category": "属性错误",
                "suggestion": "检查对象类型，或添加属性存在性检查"
            },
            "TypeError": {
                "pattern": r"TypeError:.*takes \d+ positional argument",
                "category": "类型错误",
                "suggestion": "检查函数参数数量和类型"
            },
            "ImportError": {
                "pattern": r"ImportError|ModuleNotFoundError",
                "category": "导入错误",
                "suggestion": "检查依赖是否安装，或添加requirements.txt"
            }
        }
    
    def load_errors(self, days: int = 7) -> List[Dict]:
        """加载错误日志"""
        errors = []
        
        from datetime import datetime, timedelta
        for i in range(days):
            date_str = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            log_file = self.data_dir / f"{self.skill_name}_{date_str}.jsonl"
            
            if log_file.exists():
                with open(log_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        try:
                            data = json.loads(line.strip())
                            if not data.get('success') and data.get('error_type'):
                                errors.append(data)
                        except:
                            continue
        
        return errors
    
    def categorize_error(self, error_message: str) -> Tuple[str, str, str]:
        """
        分类错误
        返回: (错误类型, 类别, 建议)
        """
        for error_type, info in self.error_patterns.items():
            match = re.search(info['pattern'], error_message, re.IGNORECASE)
            if match:
                return error_type, info['category'], info['suggestion']
        
        return "UnknownError", "未知错误", "查看详细错误日志，联系开发者"
    
    def analyze(self, days: int = 7) -> Dict:
        """分析错误"""
        errors = self.load_errors(days)
        
        if not errors:
            return {"status": "ok", "message": "最近无错误记录"}
        
        # 分类统计
        categories = defaultdict(list)
        for error in errors:
            error_type, category, suggestion = self.categorize_error(
                error.get('error_type', '')
            )
            categories[category].append({
                "timestamp": error.get('timestamp'),
                "function": error.get('function_name'),
                "error_type": error_type,
                "suggestion": suggestion
            })
        
        # 生成报告
        report = {
            "total_errors": len(errors),
            "period_days": days,
            "categories": dict(categories),
            "top_issues": self._identify_top_issues(categories),
            "hotspots": self._find_error_hotspots(errors)
        }
        
        return report
    
    def _identify_top_issues(self, categories: Dict) -> List[Dict]:
        """识别首要问题"""
        issues = []
        for category, errors in categories.items():
            if len(errors) >= 3:  # 出现3次以上的问题
                issues.append({
                    "category": category,
                    "count": len(errors),
                    "priority": "high" if len(errors) >= 5 else "medium"
                })
        
        return sorted(issues, key=lambda x: x['count'], reverse=True)
    
    def _find_error_hotspots(self, errors: List[Dict]) -> List[Dict]:
        """找出错误热点（哪个函数最容易出错）"""
        function_errors = defaultdict(int)
        for error in errors:
            func = error.get('function_name', 'unknown')
            function_errors[func] += 1
        
        hotspots = [
            {"function": func, "error_count": count}
            for func, count in function_errors.items()
        ]
        
        return sorted(hotspots, key=lambda x: x['error_count'], reverse=True)[:5]
    
    def generate_fix_suggestions(self, days: int = 7) -> List[Dict]:
        """生成修复建议"""
        report = self.analyze(days)
        
        if report.get('status') == 'ok':
            return []
        
        suggestions = []
        
        for category, errors in report.get('categories', {}).items():
            if len(errors) >= 3:
                suggestion = {
                    "issue": category,
                    "frequency": len(errors),
                    "affected_functions": list(set(e['function'] for e in errors)),
                    "suggested_fix": errors[0]['suggestion'],
                    "code_example": self._generate_code_example(category)
                }
                suggestions.append(suggestion)
        
        return suggestions
    
    def _generate_code_example(self, category: str) -> str:
        """生成代码修复示例"""
        examples = {
            "文件错误": """
# 添加路径检查
def ensure_dir(path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)

# 使用示例
file_path = "data/output.json"
ensure_dir(file_path)
with open(file_path, 'w') as f:
    json.dump(data, f)
""",
            "网络错误": """
# 添加重试机制
import time
from functools import wraps

def retry(max_attempts=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except ConnectionError:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(delay * (attempt + 1))
        return wrapper
    return decorator

# 使用示例
@retry(max_attempts=3)
def fetch_data(url):
    return requests.get(url, timeout=10)
""",
            "键错误": """
# 使用安全的字典访问
value = data.get('key', default_value)

# 或检查键是否存在
if 'key' in data:
    value = data['key']
else:
    value = default_value
""",
            "索引错误": """
# 检查列表长度
if len(items) > index:
    value = items[index]
else:
    value = None
"""
        }
        
        return examples.get(category, "# 查看具体错误日志，针对性修复")


def main():
    parser = argparse.ArgumentParser(description='错误分析器')
    parser.add_argument('--skill', type=str, required=True, help='Skill名称')
    parser.add_argument('--analyze', action='store_true', help='分析错误')
    parser.add_argument('--fix-suggestions', action='store_true', help='生成修复建议')
    parser.add_argument('--days', type=int, default=7, help='分析天数')
    
    args = parser.parse_args()
    
    analyzer = ErrorAnalyzer(args.skill)
    
    if args.analyze:
        report = analyzer.analyze(args.days)
        print(json.dumps(report, indent=2, ensure_ascii=False))
    
    elif args.fix_suggestions:
        suggestions = analyzer.generate_fix_suggestions(args.days)
        print(json.dumps(suggestions, indent=2, ensure_ascii=False))
    
    else:
        print(f"[*] 错误分析器已初始化: {args.skill}")
        print("[*] 使用 --analyze 分析错误")
        print("[*] 使用 --fix-suggestions 生成修复建议")


if __name__ == '__main__':
    main()
