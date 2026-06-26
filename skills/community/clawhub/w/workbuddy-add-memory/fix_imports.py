#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复模块导入问题
作者: zcg007
日期: 2026-03-15
"""

import os
import re

def fix_imports_in_file(file_path, replacements):
    """修复文件中的导入语句"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    for old_import, new_import in replacements.items():
        # 修复相对导入
        pattern1 = f'from {re.escape(old_import)} import'
        replacement1 = f'from {new_import} import'
        content = re.sub(pattern1, replacement1, content)
        
        pattern2 = f'import {re.escape(old_import)}'
        replacement2 = f'import {new_import}'
        content = re.sub(pattern2, replacement2, content)
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 修复了 {file_path}")
        return True
    else:
        print(f"⚠️  无需修复 {file_path}")
        return False

def main():
    """主函数"""
    skill_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 需要修复的文件列表
    files_to_fix = [
        "task_detector.py",
        "memory_retriever.py", 
        "conversation_hook.py",
        "work_preparation.py",
    ]
    
    # 导入替换规则
    import_replacements = {
        ".config_loader": "config_loader",
        ".task_detector": "task_detector",
        ".memory_retriever": "memory_retriever",
        ".conversation_hook": "conversation_hook",
        ".work_preparation": "work_preparation",
    }
    
    print("🔧 开始修复模块导入问题...")
    print(f"技能目录: {skill_dir}")
    print()
    
    fixed_count = 0
    for file_name in files_to_fix:
        file_path = os.path.join(skill_dir, file_name)
        if os.path.exists(file_path):
            if fix_imports_in_file(file_path, import_replacements):
                fixed_count += 1
    
    print()
    print("=" * 60)
    print(f"修复完成: 处理了 {len(files_to_fix)} 个文件，修复了 {fixed_count} 个文件")
    print()
    
    # 测试修复结果
    print("🔍 测试修复结果...")
    test_script = """
import sys
import os

# 添加当前目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    # 测试导入所有模块
    from config_loader import config_loader
    print("✅ config_loader 导入成功")
    
    from task_detector import task_detector
    print("✅ task_detector 导入成功")
    
    from memory_retriever import memory_retriever
    print("✅ memory_retriever 导入成功")
    
    from conversation_hook import conversation_hook
    print("✅ conversation_hook 导入成功")
    
    from work_preparation import WorkPreparation
    print("✅ work_preparation 导入成功")
    
    print()
    print("🎉 所有模块导入修复成功！")
    
except Exception as e:
    print(f"❌ 导入测试失败: {{e}}")
    import traceback
    traceback.print_exc()
"""
    
    test_file = os.path.join(skill_dir, "test_fix_result.py")
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_script)
    
    os.system(f"cd {skill_dir} && python3 test_fix_result.py")
    
    # 清理测试文件
    if os.path.exists(test_file):
        os.remove(test_file)
    
    print()
    print("💡 提示:")
    print("如果仍有导入问题，可能需要检查:")
    print("1. 依赖包是否安装完整 (requirements.txt)")
    print("2. Python路径是否正确设置")
    print("3. 模块文件是否存在")
    print()
    print("📦 安装依赖:")
    print("pip3 install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt")

if __name__ == "__main__":
    main()