#!/usr/bin/env python3
"""
bulk_cleanup.py - 批量清理现有卡片

用新标准（v3.0）重新评估所有现有卡片：
- 体育分析 → 删除
- 具体市场预测 → 删除
- 临时新闻 → 删除
- 内容污染 → 删除
- 架构/避坑/配置 → 保留
"""

import json
import shutil
from pathlib import Path
from datetime import datetime

TOPICS_DIR = Path("/home/aqukin/.openclaw/workspace/memory/topics")
ARCHIVE_DIR = Path("/home/aqukin/.openclaw/workspace/memory/archive")
REPORT_DIR = Path("/home/aqukin/.openclaw/workspace/memory/reports")

def ensure_dirs():
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

def should_delete(card_name, content):
    """根据新标准判断是否删除"""
    name_lower = card_name.lower()
    content_lower = content.lower()
    reasons = []
    
    # 规则 1: 体育分析
    sports_keywords = ['sports', 'thunder', 'knicks', 'maple_leafs', 'devils', 
                       'heroic', 'passion', 'trail_blazers', 'grizzlies', 
                       'vs_', 'win_rate', '胜率', 'odds', '赔率']
    if any(k in name_lower or k in content_lower for k in sports_keywords):
        if 'polymarket' in name_lower and any(s in content_lower for s in ['vs', '胜率', 'odds']):
            reasons.append('体育比赛分析（短期时效）')
    
    # 规则 2: 具体市场分析（带日期的预测）
    if 'polymarket' in name_lower and any(x in name_lower for x in [
        '_march', '_april', '_may', '_2024', '_2025', '_2026',
        'cyprus', 'iran', 'gulf', 'market_analysis'
    ]):
        # 检查是否包含具体胜率预测
        if any(x in content_lower for x in ['胜率', '%', 'probability', 'price', 'yes', 'no']):
            reasons.append('具体市场预测（短期时效）')
    
    # 规则 3: 临时新闻
    news_keywords = ['_scan_', '_breaking_', '_news_', ' jerusalem post', 
                     'al jazeera', '突发', 'news_']
    if any(k in name_lower or k in content_lower for k in news_keywords):
        reasons.append('临时新闻解读')
    
    # 规则 4: 内容污染（处理报告混入）
    pollution_markers = [
        '记忆蒸馏任务已全部完成',
        '最终成果报告',
        '处理统计',
        '我看到您正在测试',
        '让我查看几个',
    ]
    if any(m in content for m in pollution_markers):
        reasons.append('内容污染（处理报告混入）')
    
    # 规则 5: 纯测试/寒暄
    if any(x in name_lower for x in ['test_', 'hello_', 'hi_', 'greeting_']):
        reasons.append('测试/寒暄内容')
    
    # 规则 6: 过短的无效内容
    if len(content.strip()) < 100:
        reasons.append('内容过短无效')
    
    return len(reasons) > 0, reasons

def classify_keep_reason(card_name, content):
    """判断保留的原因（分类）"""
    name_lower = card_name.lower()
    content_lower = content.lower()
    
    # 架构设计
    if any(x in name_lower for x in ['architecture', 'cluster', 'bridge', 'queue', 'system_design']):
        return '架构设计'
    
    # 避坑指南
    if any(x in name_lower for x in ['fix', 'bug', 'error', 'solution', 'resolved', 'workaround']):
        return '避坑指南'
    
    # 配置沉淀
    if any(x in name_lower for x in ['config', 'setup', 'install', 'env', 'conda', 'docker']):
        return '配置沉淀'
    
    # 流程 SOP
    if any(x in name_lower for x in ['sop', 'workflow', 'process', 'how_to', 'guide']):
        return '流程SOP'
    
    # 代码/策略（非具体市场）
    if 'trader' in name_lower or 'bot' in name_lower:
        if 'analysis' not in name_lower and 'scan' not in name_lower:
            return '代码策略'
    
    return '其他'

def main():
    print("🧹 批量清理现有卡片")
    print("=" * 60)
    
    ensure_dirs()
    
    cards = list(TOPICS_DIR.glob('*.md'))
    print(f"发现 {len(cards)} 张卡片")
    print()
    
    to_delete = []
    to_keep = []
    
    for card_path in cards:
        content = card_path.read_text(encoding='utf-8')
        should_del, reasons = should_delete(card_path.name, content)
        
        if should_del:
            to_delete.append({
                'name': card_path.name,
                'reasons': reasons,
                'size': len(content)
            })
        else:
            category = classify_keep_reason(card_path.name, content)
            to_keep.append({
                'name': card_path.name,
                'category': category,
                'size': len(content)
            })
    
    # 显示删除列表
    print(f"🗑️  建议删除: {len(to_delete)} 张")
    for item in to_delete[:20]:  # 只显示前20个
        print(f"   - {item['name']}")
        for r in item['reasons']:
            print(f"     └─ {r}")
    if len(to_delete) > 20:
        print(f"   ... 还有 {len(to_delete) - 20} 个")
    print()
    
    # 显示保留列表
    print(f"✅ 建议保留: {len(to_keep)} 张")
    categories = {}
    for item in to_keep:
        cat = item['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        print(f"   - {cat}: {count} 张")
    print()
    
    # 保存报告
    report = {
        'timestamp': datetime.now().isoformat(),
        'total': len(cards),
        'to_delete': to_delete,
        'to_keep': to_keep,
        'delete_count': len(to_delete),
        'keep_count': len(to_keep)
    }
    
    report_path = REPORT_DIR / f'cleanup_report_{datetime.now().strftime("%Y%m%d")}.json'
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"📄 详细报告: {report_path}")
    
    # 询问是否执行删除
    print()
    print("=" * 60)
    print("⚠️  准备执行清理:")
    print(f"   将删除: {len(to_delete)} 张卡片（移动到 archive/）")
    print(f"   将保留: {len(to_keep)} 张卡片")
    print()
    print("运行以下命令执行删除:")
    print(f"  python3 {__file__} --exec")

def execute_cleanup():
    """执行实际的清理操作"""
    print("🧹 执行批量清理...")
    
    cards = list(TOPICS_DIR.glob('*.md'))
    deleted = 0
    
    for card_path in cards:
        content = card_path.read_text(encoding='utf-8')
        should_del, reasons = should_delete(card_path.name, content)
        
        if should_del:
            # 移动到 archive
            shutil.move(str(card_path), str(ARCHIVE_DIR / card_path.name))
            print(f"   🗑️  已归档: {card_path.name}")
            deleted += 1
    
    print(f"\n✅ 清理完成，已归档 {deleted} 张卡片")

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--exec':
        execute_cleanup()
    else:
        main()