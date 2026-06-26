#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WorkBuddy智能记忆管理系统导入测试
作者: zcg007
日期: 2026-03-15
"""

import os
import sys

# 添加当前目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print("🔍 开始导入测试...")
print(f"Python路径: {sys.executable}")
print(f"工作目录: {current_dir}")
print()

# 测试导入所有模块
modules_to_test = [
    ("config_loader", "config_loader"),
    ("task_detector", "task_detector"),
    ("memory_retriever", "memory_retriever"),
    ("conversation_hook", "conversation_hook"),
    ("work_preparation", "WorkPreparation"),
]

all_success = True

for module_name, import_name in modules_to_test:
    try:
        if module_name == "config_loader":
            from config_loader import config_loader
            print(f"✅ {module_name} 导入成功")
            
            # 测试配置加载
            config = config_loader.load_config()
            print(f"   配置加载成功，记忆源: {len(config.get('memory_sources', []))}个")
            
        elif module_name == "task_detector":
            from task_detector import task_detector
            print(f"✅ {module_name} 导入成功")
            
            # 测试任务检测
            result = task_detector.detect_task("制作Excel预算表")
            print(f"   任务检测成功，类型: {result.get('primary_task')}, 置信度: {result.get('confidence'):.2f}")
            
        elif module_name == "memory_retriever":
            from memory_retriever import memory_retriever
            print(f"✅ {module_name} 导入成功")
            
            # 测试记忆检索器初始化
            print(f"   记忆检索器初始化成功")
            
        elif module_name == "conversation_hook":
            from conversation_hook import conversation_hook
            print(f"✅ {module_name} 导入成功")
            
            # 测试对话钩子
            print(f"   对话钩子初始化成功")
            
        elif module_name == "work_preparation":
            from work_preparation import WorkPreparation
            print(f"✅ {module_name} 导入成功")
            
            # 测试工作准备模块
            print(f"   工作准备模块导入成功")
            
    except Exception as e:
        print(f"❌ {module_name} 导入失败: {e}")
        all_success = False
        import traceback
        traceback.print_exc()

print()
print("=" * 60)
if all_success:
    print("🎉 所有模块导入测试通过！")
    print()
    print("新版本功能特性:")
    print("1. 增强配置加载器 (支持多层级配置)")
    print("2. 智能任务检测器 (多层级检测算法)")
    print("3. 增强记忆检索器 (TF-IDF + 语义相似度)")
    print("4. 增强对话钩子 (智能触发机制)")
    print("5. 工作准备模块 (自动准备环境和计划)")
    print("6. 改进的启动脚本 (交互式和命令行)")
else:
    print("⚠️  部分模块导入失败，请检查依赖和导入路径")
print("=" * 60)

# 测试启动脚本
print()
print("🔧 测试启动脚本...")
try:
    import subprocess
    result = subprocess.run(
        [sys.executable, "start_work.py", "--status"],
        cwd=current_dir,
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ 启动脚本测试通过")
        # 显示部分输出
        output_lines = result.stdout.split('\n')
        for line in output_lines[:10]:
            if line.strip():
                print(f"   {line}")
    else:
        print(f"❌ 启动脚本测试失败: {result.stderr}")
        
except Exception as e:
    print(f"❌ 启动脚本测试失败: {e}")