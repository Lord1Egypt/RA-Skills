"""
初始化标准模块脚本

用法：
    python init_module.py --type worker --name MyWorker
    python init_module.py --type util --name DateHelper
    python init_module.py --type app --name MyApp
"""

import os
import sys
import argparse
from datetime import datetime

# 模板定义
TEMPLATES = {
    "worker": '''"""
{module_name} - 数据处理工作器

Created: {date}
"""
import os
import traceback
from PySide6.QtCore import QObject, Signal


class {class_name}(QObject):
    """数据处理工作器"""
    
    # 信号定义
    progress = Signal(str)
    finished = Signal(str)
    failed = Signal(str)
    
    def __init__(self, config, source_path, output_dir):
        super().__init__()
        self.config = config
        self.source_path = source_path
        self.output_dir = output_dir
    
    def run(self):
        """执行任务"""
        try:
            self._run_impl()
        except Exception as e:
            msg = f"发生异常：{e}\\n\\n{traceback.format_exc()}"
            self.failed.emit(msg)
    
    def _run_impl(self):
        """实际执行逻辑"""
        self.progress.emit("开始处理...")
        
        # TODO: 实现具体逻辑
        
        self.finished.emit("处理完成")
''',

    "util": '''"""
{module_name} - 工具模块

Created: {date}
"""
import os
import re
from typing import Dict, List, Optional, Tuple


def col_letter_to_index(letter: str) -> int:
    """
    将Excel列字母（如 'G', 'AK'）转换为1-based索引
    """
    letter = letter.strip().upper()
    n = 0
    for ch in letter:
        if not ("A" <= ch <= "Z"):
            raise ValueError(f"无效的列字母: {{letter}}")
        n = n * 26 + (ord(ch) - ord("A") + 1)
    return n


def safe_str(v) -> str:
    """安全转换为字符串"""
    if v is None:
        return ""
    return str(v).strip()


def parse_float(v) -> float:
    """安全转换为浮点数，失败返回0.0"""
    s = safe_str(v)
    if not s:
        return 0.0
    try:
        return float(s)
    except ValueError:
        return 0.0
''',

    "app": '''"""
{module_name} - 应用程序主模块

Created: {date}
"""
import os
import sys
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import logging


class TextHandler(logging.Handler):
    """将日志输出到Tkinter文本框"""
    
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget
    
    def emit(self, record):
        def append():
            msg = self.format(record)
            if record.levelno >= logging.ERROR:
                self.text_widget.insert(tk.END, msg + '\\n', 'error')
            elif record.levelno >= logging.WARNING:
                self.text_widget.insert(tk.END, msg + '\\n', 'warning')
            else:
                self.text_widget.insert(tk.END, msg + '\\n')
            self.text_widget.see(tk.END)
        
        try:
            self.text_widget.after(0, append)
        except Exception:
            pass


class {class_name}:
    """主应用程序"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("{app_title}")
        
        # 跨平台字体
        self.font_main = ("Microsoft YaHei", 10) if sys.platform != "darwin" else ("Helvetica Neue", 10)
        
        # 设置浅色主题
        self.root.configure(bg="#f0f5f9")
        
        self.setup_ui()
        self.init_logger()
    
    def setup_ui(self):
        """设置UI"""
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # TODO: 添加UI组件
    
    def init_logger(self):
        """初始化日志"""
        self.logger = logging.getLogger('{app_name}')
        self.logger.setLevel(logging.DEBUG)
        
        text_handler = TextHandler(self.log_text)
        text_handler.setLevel(logging.DEBUG)
        self.logger.addHandler(text_handler)


def main():
    root = tk.Tk()
    app = {class_name}(root)
    root.mainloop()


if __name__ == "__main__":
    main()
''',

    "config": '''{{
    "schema_version": 1,
    "source": {{
        "default_paths": [],
        "sheet_index": 0
    }},
    "target": {{
        "workbook_relative_path": "数据模板.xlsx",
        "sheet_name": "Sheet1",
        "match_key_target_column": "A",
        "match_key_source_column": "A",
        "target_row_start": 1,
        "target_row_end": 100
    }},
    "output": {{
        "summary_filename": "结果.xlsx"
    }},
    "source_columns": {{}},
    "base_columns": {{}}
}}
''',

    "test": '''"""
{module_name} - 测试模块

Created: {date}
"""
import unittest
from {module_name_lower} import *


class Test{class_name}(unittest.TestCase):
    """测试用例"""
    
    def setUp(self):
        """测试前准备"""
        pass
    
    def test_col_letter_to_index(self):
        """测试列字母转换"""
        self.assertEqual(col_letter_to_index("A"), 1)
        self.assertEqual(col_letter_to_index("Z"), 26)
        self.assertEqual(col_letter_to_index("AA"), 27)
        self.assertEqual(col_letter_to_index("AK"), 37)
    
    def test_safe_str(self):
        """测试安全字符串转换"""
        self.assertEqual(safe_str(None), "")
        self.assertEqual(safe_str("  hello  "), "hello")
        self.assertEqual(safe_str(123), "123")
    
    def test_parse_float(self):
        """测试安全浮点数转换"""
        self.assertEqual(parse_float(None), 0.0)
        self.assertEqual(parse_float(""), 0.0)
        self.assertEqual(parse_float("123.45"), 123.45)
        self.assertEqual(parse_float("abc"), 0.0)


if __name__ == "__main__":
    unittest.main()
'''
}


def get_script_dir():
    """获取脚本目录"""
    return os.path.dirname(os.path.abspath(__file__))


def get_output_dir():
    """获取输出目录（上一级）"""
    return os.path.dirname(get_script_dir())


def to_class_name(name):
    """转换为PascalCase类名"""
    return ''.join(word.capitalize() for word in name.replace('-', '_').split('_'))


def to_module_name(name):
    """转换为snake_case模块名"""
    return name.replace('-', '_').lower()


def main():
    parser = argparse.ArgumentParser(description="初始化标准模块")
    parser.add_argument("--type", "-t", choices=["worker", "util", "app", "config", "test"],
                        default="util", help="模块类型")
    parser.add_argument("--name", "-n", required=True, help="模块名称")
    parser.add_argument("--output", "-o", default=None, help="输出目录")
    parser.add_argument("--app-title", default="应用程序", help="应用标题（仅app类型）")
    
    args = parser.parse_args()
    
    module_name = to_module_name(args.name)
    class_name = to_class_name(args.name)
    date = datetime.now().strftime("%Y-%m-%d")
    
    # 获取输出目录
    if args.output:
        output_dir = args.output
    else:
        output_dir = get_output_dir()
    
    if args.type == "config":
        # 配置模板单独处理
        output_path = os.path.join(output_dir, f"{module_name}.json")
        content = TEMPLATES["config"].format()
    elif args.type == "test":
        # 测试模板
        output_path = os.path.join(output_dir, f"test_{module_name}.py")
        # 获取主模块路径（去掉test_前缀）
        main_module = module_name.replace("test_", "")
        content = TEMPLATES["test"].format(
            module_name=f"test_{module_name}",
            module_name_lower=main_module,
            class_name=class_name,
            date=date
        )
    else:
        output_path = os.path.join(output_dir, f"{module_name}.py")
        content = TEMPLATES[args.type].format(
            module_name=module_name,
            class_name=class_name,
            date=date,
            app_name=module_name,
            app_title=args.app_title
        )
    
    # 检查文件是否已存在
    if os.path.exists(output_path):
        response = input(f"文件已存在: {output_path}\\n是否覆盖? (y/N): ")
        if response.lower() != 'y':
            print("已取消")
            return
    
    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ 已创建: {output_path}")


if __name__ == "__main__":
    main()
