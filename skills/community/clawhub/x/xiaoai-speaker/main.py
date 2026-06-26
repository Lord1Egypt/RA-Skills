#!/usr/bin/env python3
"""
OpenClaw xiaoai-speaker Skill 主入口
提供简化的命令行接口
"""

import sys
import os

# 添加脚本路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from xiaoai_cli import main as cli_main

def main():
    """OpenClaw 调用的主函数"""
    # 如果第一个参数是 'xiaoai'，去掉它（因为 OpenClaw 会传入）
    if len(sys.argv) > 1 and sys.argv[1] == 'xiaoai':
        sys.argv.pop(1)
    
    return cli_main()

if __name__ == '__main__':
    sys.exit(main())
