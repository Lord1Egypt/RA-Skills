#!/usr/bin/env python3
"""
VideoClaw Pro CLI 工具 - 支持 wiki 和 docx 链接的飞书文档读写功能
"""
import sys
import os
import re

# 添加当前目录到路径，确保可以导入模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from videoclaw_lib import feishu_doc_reader, feishu_doc_writer

def main():
    if len(sys.argv) < 2:
        print("VideoClaw Pro CLI")
        print("Usage:")
        print("  python videoclaw_cli.py read <doc_url>           - 读取飞书文档（支持 docx 和 wiki）")
        print("  python videoclaw_cli.py write <title> <content> - 创建并写入飞书文档")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "read":
        if len(sys.argv) < 3:
            print("Error: 请提供文档URL")
            sys.exit(1)
        doc_url = sys.argv[2]
        result = feishu_doc_reader(doc_url)
        print(result)
    
    elif command == "write":
        if len(sys.argv) < 4:
            print("Error: 请提供标题和内容")
            sys.exit(1)
        title = sys.argv[2]
        content = sys.argv[3]
        result = feishu_doc_writer(title, content)
        print(result)
    
    else:
        print(f"Unknown command: {command}")
        print("Use 'read' or 'write'")
        sys.exit(1)

if __name__ == "__main__":
    main()
