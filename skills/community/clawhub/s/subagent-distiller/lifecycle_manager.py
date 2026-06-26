#!/usr/bin/env python3
"""
lifecycle_manager.py - 生命周期管理器 v3.0

功能：
- 自动清理过期内容（7天前的短期内容）
- 提醒 PENDING 事项（超过3天未解决）
- 归档 ABANDONED（仅保留避坑价值）
- 每日健康检查报告
"""

import json
import re
from pathlib import Path
from datetime import datetime, timedelta

WORKSPACE = Path("/home/aqukin/.openclaw/workspace")
SKILL_DIR = WORKSPACE / "skills/subagent-distiller"
TOPICS_DIR = WORKSPACE / "memory/topics"
ARCHIVE_DIR = WORKSPACE / "memory/archive"
REPORTS_DIR = WORKSPACE / "memory/reports"

def ensure_dirs():
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

def parse_card_frontmatter(card_path):
    """解析卡片 frontmatter"""
    with open(card_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    metadata = {}
    
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 2:
            frontmatter = parts[1].strip()
            for line in frontmatter.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    metadata[key] = value
    
    return metadata, content

def parse_date(date_str):
    """解析日期字符串"""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except:
        try:
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except:
            return None

def days_since(date_str):
    """计算距离今天的天数"""
    date = parse_date(date_str)
    if not date:
        return 0
    return (datetime.now() - date).days

def check_card_health(card_path):
    """检查卡片健康状态"""
    metadata, content = parse_card_frontmatter(card_path)
    
    status = metadata.get('status', 'UNKNOWN')
    created = metadata.get('created', '')
    updated = metadata.get('updated', created)
    
    issues = []
    actions = []
    
    # 检查 1：PENDING 超时提醒
    if status == 'PENDING':
        age = days_since(updated)
        if age > 7:
            issues.append(f'PENDING 超时（{age}天无更新）')
            actions.append('ALERT')  # 严重提醒
        elif age > 3:
            issues.append(f'PENDING 提醒（{age}天未解决）')
            actions.append('REMIND')  # 普通提醒
    
    # 检查 2：ABANDONED 标记审查
    if status == 'ABANDONED':
        issues.append('已放弃的方案（仅保留避坑价值）')
        # 不再自动归档，只标记
    
    # 检查 3：空内容
    if len(content.strip()) < 50:
        issues.append('内容过短或为空')
        actions.append('REVIEW')
    
    return {
        'name': card_path.name,
        'status': status,
        'created': created,
        'updated': updated,
        'age_days': days_since(created),
        'issues': issues,
        'actions': actions
    }

def generate_report(checks):
    """生成健康检查报告"""
    # 统计
    status_counts = {}
    action_counts = {}
    pending_list = []
    
    for check in checks:
        status = check['status']
        status_counts[status] = status_counts.get(status, 0) + 1
        
        for action in check['actions']:
            action_counts[action] = action_counts.get(action, 0) + 1
        
        if check['status'] == 'PENDING':
            pending_list.append(check)
    
    report_lines = [
        "# ⏰ 记忆系统待办提醒",
        f"",
        f"**检查时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**总卡片数**: {len(checks)}",
        f"**PENDING 待办**: {len(pending_list)} 项",
        f"",
    ]
    
    # PENDING 清单（核心功能）
    if pending_list:
        report_lines.append("## 🔴 待办事项清单（按紧急程度排序）")
        report_lines.append("")
        
        # 按超时天数排序
        for check in sorted(pending_list, key=lambda x: x['age_days'], reverse=True):
            urgency = '🔴' if check['age_days'] > 7 else '⏰' if check['age_days'] > 3 else '⏳'
            report_lines.append(f"### {urgency} {check['name']}")
            report_lines.append(f"- 状态: PENDING")
            report_lines.append(f"- 已 {check['age_days']} 天未更新")
            report_lines.append(f"- 问题: {', '.join(check['issues'])}")
            report_lines.append("")
    else:
        report_lines.append("✅ 没有 PENDING 待办事项，所有任务已完成！")
    
    # 状态统计
    report_lines.extend([
        "",
        "## 📊 状态分布",
        "",
    ])
    for status, count in sorted(status_counts.items()):
        report_lines.append(f"- {status}: {count}")
    
    return '\n'.join(report_lines)

def main():
    print("⏰ 生命周期管理器 v3.0 - 专注待办提醒")
    print("=" * 50)
    
    ensure_dirs()
    
    # 获取所有卡片
    cards = list(TOPICS_DIR.glob('*.md'))
    if not cards:
        print("没有找到知识卡片")
        return
    
    print(f"检查 {len(cards)} 个知识卡片...")
    print()
    
    checks = []
    alerted = []
    reminded = []
    
    for card_path in cards:
        check = check_card_health(card_path)
        checks.append(check)
        
        if check['actions']:
            print(f"📄 {check['name']}")
            for issue in check['issues']:
                print(f"   ⏰ {issue}")
            print()
            
            # 分类提醒
            for action in check['actions']:
                if action == 'ALERT':
                    alerted.append(check)
                elif action == 'REMIND':
                    reminded.append(check)
    
    # 生成报告
    report = generate_report(checks)
    report_path = REPORTS_DIR / f"pending_reminder_{datetime.now().strftime('%Y%m%d')}.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print()
    print("=" * 50)
    print("✅ 待办提醒检查完成")
    print(f"   总卡片: {len(cards)}")
    print(f"   紧急提醒: {len(alerted)} 个（PENDING >7天）")
    print(f"   普通提醒: {len(reminded)} 个（PENDING 3-7天）")
    print(f"   报告: {report_path}")
    
    # 发送警报（如果有）
    if alerted:
        print()
        print("🔴 紧急提醒（需立即处理）:")
        for check in alerted[:5]:
            print(f"   - {check['name']}: {check['age_days']}天未更新")

def list_pending():
    """列出所有 PENDING 事项"""
    cards = list(TOPICS_DIR.glob('*.md'))
    pending = []
    
    for card_path in cards:
        metadata, _ = parse_card_frontmatter(card_path)
        if metadata.get('status') == 'PENDING':
            age = days_since(metadata.get('updated', metadata.get('created', '')))
            pending.append({
                'name': card_path.name,
                'summary': metadata.get('summary', '无摘要'),
                'age_days': age
            })
    
    if not pending:
        print("✅ 没有 PENDING 待办事项")
        return
    
    print(f"⏰ PENDING 待办清单 ({len(pending)} 项):")
    print()
    for item in sorted(pending, key=lambda x: x['age_days'], reverse=True):
        urgency = '🔴' if item['age_days'] > 7 else '⏰' if item['age_days'] > 3 else '⏳'
        print(f"{urgency} [{item['name']}]")
        print(f"   摘要: {item['summary']}")
        print(f"   已 {item['age_days']} 天未更新")
        print()

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--list-pending':
        list_pending()
    else:
        main()