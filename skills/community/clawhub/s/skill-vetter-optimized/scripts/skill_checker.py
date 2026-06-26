#!/usr/bin/env python3
"""
Skill Vetter Helper Script
辅助工具，用于快速检查技能的基本信息和安全风险
"""

import os
import sys
import json
import re
from pathlib import Path

def check_skill_directory(skill_path):
    """检查技能目录的基本信息"""
    skill_path = Path(skill_path)
    
    if not skill_path.exists():
        print(f"错误: 路径不存在: {skill_path}")
        return None
    
    print(f"检查技能目录: {skill_path}")
    print("=" * 60)
    
    # 检查SKILL.md文件
    skill_md = skill_path / "SKILL.md"
    if skill_md.exists():
        print(f"✅ 找到 SKILL.md")
        with open(skill_md, 'r', encoding='utf-8') as f:
            content = f.read(2000)  # 只读取前2000字符
            
            # 提取元数据
            if content.startswith('---'):
                meta_end = content.find('---', 3)
                if meta_end != -1:
                    meta_content = content[3:meta_end]
                    print("📋 技能元数据:")
                    for line in meta_content.strip().split('\n'):
                        if ':' in line:
                            key, value = line.split(':', 1)
                            print(f"   {key.strip()}: {value.strip()}")
    else:
        print(f"❌ 未找到 SKILL.md 文件")
    
    # 列出所有文件
    print("\n📁 目录结构:")
    file_count = 0
    script_files = []
    
    for root, dirs, files in os.walk(skill_path):
        level = root.replace(str(skill_path), '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        
        for file in files:
            file_count += 1
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, skill_path)
            
            # 检查脚本文件
            if file.endswith(('.py', '.sh', '.js', '.ts')):
                script_files.append(rel_path)
                print(f"{subindent}🔧 {file}")
            elif file.endswith('.md'):
                print(f"{subindent}📝 {file}")
            elif file.endswith('.json'):
                print(f"{subindent}📊 {file}")
            else:
                print(f"{subindent}{file}")
    
    print(f"\n📊 统计信息:")
    print(f"   总文件数: {file_count}")
    print(f"   脚本文件: {len(script_files)}")
    if script_files:
        print(f"   脚本列表: {', '.join(script_files)}")
    
    # 快速安全检查
    print("\n🔍 快速安全检查:")
    
    red_flags = []
    for script in script_files:
        script_path = skill_path / script
        try:
            with open(script_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                # 检查危险模式
                checks = [
                    ("curl.*\\|.*bash", "curl管道到bash"),
                    ("wget.*\\|.*sh", "wget管道到sh"),
                    ("eval\\s*\\(.*\\)", "eval函数调用"),
                    ("exec\\s*\\(.*\\)", "exec函数调用"),
                    ("base64.*decode", "base64解码"),
                    ("requests\\.(get|post)", "网络请求"),
                    ("subprocess\\.run", "子进程执行"),
                    ("os\\.system", "系统命令执行"),
                    ("chmod.*777", "危险权限设置"),
                    ("sudo", "sudo命令"),
                ]
                
                for pattern, desc in checks:
                    if re.search(pattern, content, re.IGNORECASE):
                        red_flags.append(f"{script}: {desc}")
                        
        except Exception as e:
            print(f"   无法读取 {script}: {e}")
    
    if red_flags:
        print("   ⚠️  发现潜在风险:")
        for flag in red_flags:
            print(f"      • {flag}")
    else:
        print("   ✅ 未发现明显的危险模式")
    
    print("\n" + "=" * 60)
    return {
        "path": str(skill_path),
        "has_skill_md": skill_md.exists(),
        "file_count": file_count,
        "script_count": len(script_files),
        "red_flags": red_flags
    }

def main():
    if len(sys.argv) < 2:
        print("用法: python3 skill_checker.py <技能目录路径>")
        print("示例: python3 skill_checker.py /path/to/skill")
        sys.exit(1)
    
    skill_path = sys.argv[1]
    result = check_skill_directory(skill_path)
    
    if result:
        print("\n🎯 检查完成!")
        print(f"技能路径: {result['path']}")
        print(f"SKILL.md: {'✅ 存在' if result['has_skill_md'] else '❌ 缺失'}")
        print(f"文件总数: {result['file_count']}")
        print(f"脚本文件: {result['script_count']}")
        print(f"风险标记: {len(result['red_flags'])} 个")
        
        if result['red_flags']:
            print("\n⚠️  建议进行详细的安全审查!")
        else:
            print("\n✅ 初步检查通过，但仍建议进行完整审查")

if __name__ == "__main__":
    main()