# -*- coding: utf-8 -*-
"""
Report-gama — 依赖检查脚本
在启动主程序前检查所有必需的 Python 依赖是否已安装
"""

import sys

REQUIRED = [
    ("requests", "HTTP 请求库"),
    ("bs4", "BeautifulSoup HTML 解析"),
    ("lxml", "lxml XML/HTML 解析"),
]

OPTIONAL = [
    ("fake_useragent", "用户代理池（推荐）"),
    ("matplotlib", "图表生成"),
    ("reportlab", "PDF 导出"),
    ("PIL", "图片处理"),
    ("dateutil", "日期处理"),
]

def check():
    print("=" * 50)
    print("Report-gama 依赖检查")
    print("=" * 50)

    missing = []
    for module, desc in REQUIRED:
        try:
            __import__(module)
            print(f"  [OK]  {desc} ({module})")
        except ImportError:
            print(f"  [MISSING] {desc} ({module}) — 必需")
            missing.append(module)

    print()
    print("可选依赖:")
    for module, desc in OPTIONAL:
        try:
            __import__(module)
            print(f"  [OK]  {desc} ({module})")
        except ImportError:
            print(f"  [--]  {desc} ({module}) — 可选，未安装")

    print()
    if missing:
        print(f"缺少必需依赖！请运行：")
        print(f"  pip install {' '.join(missing)}")
        print()
        return False
    else:
        print("所有必需依赖已安装！")
        print()
        return True

if __name__ == "__main__":
    ok = check()
    sys.exit(0 if ok else 1)
