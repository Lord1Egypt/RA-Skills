#!/usr/bin/env python3
"""
Report Writing Skill v1.02 - Main Entry Point
Real-time progress tracking and execution status feedback
"""

import sys
import os

# Add the scripts directory to Python path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

# Import the v1.02 workflow with progress tracking
from report_writing_workflow_v102 import main

if __name__ == "__main__":
    print("🦞 Report-Writing Skill v1.02 已加载")
    print("📊 自动化研究报告收集与分析系统")
    print("📁 默认保存位置: 桌面 (可自定义)")
    print("⏳ 实时进度反馈: 启用")
    print()
    
    # Run the main workflow
    main()