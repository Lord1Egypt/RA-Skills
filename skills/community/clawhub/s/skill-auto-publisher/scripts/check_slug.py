#!/usr/bin/env python3
"""技能名称占用检测脚本"""

import subprocess
import sys
import re

def check_slug_available(slug):
    """检查技能名称是否可用"""
    try:
        result = subprocess.run(
            ["skillhub", "search", slug],
            capture_output=True,
            text=True,
            timeout=30
        )
        output = result.stdout + result.stderr
        
        # 检查是否找到完全匹配的技能
        # 格式通常是 "skill-name  Title" 或 "skill-name:"
        pattern = rf'^{re.escape(slug)}\s'
        if re.search(pattern, output, re.MULTILINE):
            return False, output
        
        # 也检查是否在输出中出现（有些格式可能不同）
        if f' {slug} ' in output or f'/{slug}' in output:
            return False, output
            
        return True, None
        
    except subprocess.TimeoutExpired:
        return None, "检测超时"
    except Exception as e:
        return None, str(e)

def suggest_alternatives(slug):
    """建议替代名称"""
    alternatives = [
        f"xiao-duo-{slug}",
        f"{slug}-cn",
        f"{slug}-auto",
        f"my-{slug}",
    ]
    
    # 如果名称包含连字符，尝试修改
    parts = slug.split('-')
    if len(parts) > 1:
        alternatives.append(f"{parts[0]}-{''.join(parts[1:])}")
    
    return alternatives

def main():
    if len(sys.argv) < 2:
        print("用法: python3 check_slug.py <skill-name>")
        sys.exit(1)
    
    slug = sys.argv[1]
    
    print(f"🔍 检测技能名称: {slug}")
    print()
    
    available, info = check_slug_available(slug)
    
    if available is None:
        print(f"⚠️ 检测失败: {info}")
        sys.exit(2)
    
    if available:
        print(f"✅ 名称可用: {slug}")
        sys.exit(0)
    else:
        print(f"❌ 名称已被占用: {slug}")
        print()
        
        # 尝试从输出中提取占用者信息
        if info:
            lines = info.split('\n')
            for line in lines[:5]:
                if slug in line:
                    print(f"   {line.strip()}")
        
        print()
        print("💡 建议替代名称:")
        alternatives = suggest_alternatives(slug)
        for i, alt in enumerate(alternatives, 1):
            print(f"   {i}. {alt}")
        
        sys.exit(1)

if __name__ == "__main__":
    main()
