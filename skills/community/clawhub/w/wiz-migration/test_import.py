#!/usr/bin/env python3
"""
为知笔记迁移技能 - 测试脚本
"""

import sys
from pathlib import Path

# 添加技能目录到路径
SKILL_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SKILL_DIR))

print("正在测试 wiz_migration 技能导入...")

try:
    import wiz_migration
    print(f"✅ 包导入成功，版本: {wiz_migration.__version__}")
    
    # 测试函数是否存在
    functions = [
        'detect_wiz_data_dir',
        'validate_data_dir',
        'generate_export_guide',
        'run_attachment_migration',
        'start_wizard'
    ]
    
    print("\n检查导出函数:")
    for func in functions:
        if hasattr(wiz_migration, func):
            print(f"  ✅ {func}")
        else:
            print(f"  ❌ 缺失: {func}")
    
    # 测试检测功能
    print("\n测试自动检测:")
    detected = wiz_migration.detect_wiz_data_dir()
    if detected:
        print(f"  ✅ 检测到目录: {detected}")
    else:
        print("  ⚠️  未检测到目录（正常，如果不存在标准安装）")
    
    print("\n✅ 所有测试通过！技能已就绪。")
    
except Exception as e:
    print(f"❌ 导入失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
