#!/usr/bin/env python3
"""
记忆冲突检测 - 检测新旧记忆之间的矛盾
"""
import json
import re
from pathlib import Path
from datetime import datetime

WORKSPACE = Path.home() / '.openclaw/workspace'
MEMORY_DIR = WORKSPACE / 'memory'
CONFLICT_LOG = WORKSPACE / 'memory' / 'conflicts.jsonl'

def extract_rules(content):
    """从记忆内容中提取规则"""
    rules = []
    # 简单规则提取：寻找"应该"、"必须"、"禁止"等关键词
    patterns = [
        r'应该.*',
        r'必须.*',
        r'禁止.*',
        r'不要.*',
        r'使用.*代替',
    ]
    for pattern in patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        rules.extend(matches)
    return rules

def check_conflicts(new_memory):
    """检查新记忆是否与现有记忆冲突"""
    conflicts = []
    
    # 遍历现有记忆文件
    for md_file in MEMORY_DIR.glob("*.md"):
        with open(md_file, 'r', encoding='utf-8') as f:
            existing_content = f.read()
            
        # 提取规则
        existing_rules = extract_rules(existing_content)
        new_rules = extract_rules(new_memory)
        
        # 检查冲突
        for new_rule in new_rules:
            for existing_rule in existing_rules:
                # 简单冲突检测：规则关键词相同但内容相反
                if ('禁止' in new_rule and '禁止' not in existing_rule or
                    '必须' in new_rule and '不要' in existing_rule or
                    '使用' in new_rule and '不要使用' in existing_rule):
                    
                    conflicts.append({
                        'new': new_rule,
                        'old': existing_rule,
                        'file': md_file.name,
                        'timestamp': datetime.now().isoformat()
                    })
    
    return conflicts

def log_conflict(conflict):
    """记录冲突到日志"""
    with open(CONFLICT_LOG, 'a', encoding='utf-8') as f:
        f.write(json.dumps(conflict, ensure_ascii=False) + '\n')

def main():
    # 测试冲突检测
    new_memory = "应该使用双引号而不是单引号"
    
    conflicts = check_conflicts(new_memory)
    
    if conflicts:
        print("⚠️  发现记忆冲突:")
        for i, conflict in enumerate(conflicts, 1):
            print(f"\n冲突 {i}:")
            print(f"  新记忆: {conflict['new']}")
            print(f"  旧记忆: {conflict['old']}")
            print(f"  来源文件: {conflict['file']}")
            print(f"  检测时间: {conflict['timestamp']}")
            log_conflict(conflict)
    else:
        print("✅ 未发现记忆冲突")

if __name__ == '__main__':
    main()