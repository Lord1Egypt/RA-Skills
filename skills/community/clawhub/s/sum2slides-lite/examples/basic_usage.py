#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sum2Slides Lite 使用示例
"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

try:
    from sum2slides import sum2slides
    
    print("🚀 Sum2Slides Lite 示例")
    print("=" * 50)
    
    # 示例对话
    conversation = """
会议讨论：
1. 决定开发Sum2Slides功能
2. 需要支持多种PPT软件
3. 关键决策：采用模块化架构
4. 行动项：本周完成测试
"""
    
    print("对话内容:")
    print(conversation)
    print()
    
    # 生成PPT
    print("生成PPT...")
    result = sum2slides(
        conversation_text=conversation,
        title="会议总结",
        software="powerpoint",
        template="business"
    )
    
    if result.get("success"):
        print("✅ PPT生成成功!")
        print("   文件:", result["ppt_info"]["file_path"])
        print("   幻灯片:", result["ppt_info"]["slide_count"], "页")
    else:
        print("❌ 生成失败:", result.get("error"))
        
except ImportError as e:
    print("❌ 导入失败:", e)
    print("请确保已正确安装")
