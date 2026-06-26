#!/usr/bin/env python3
"""
LetPub 期刊查询（浏览器自动化）
查询完成后自动关闭浏览器
"""

import sys
import json

# 注意：这个脚本需要配合主程序和 browser 工具使用
# 实际的浏览器操作由主程序控制

def format_letpub_output(detail):
    """格式化 LetPub 输出"""
    lines = [f"📊 {detail.get('title', 'Unknown')}"]
    
    if detail.get('issn'):
        lines.append(f"ISSN: {detail['issn']}")
    
    lines.append("\n【影响因子】")
    if detail.get('impact_factor'):
        lines.append(f"  • 2024-2025: {detail['impact_factor']}")
    if detail.get('realtime_impact_factor'):
        lines.append(f"  • 实时：{detail['realtime_impact_factor']}")
    if detail.get('five_year_impact_factor'):
        lines.append(f"  • 5 年：{detail['five_year_impact_factor']}")
    
    if detail.get('self_citation_rate'):
        lines.append(f"  • 自引率：{detail['self_citation_rate']}%")
    
    lines.append("\n【其他指标】")
    if detail.get('jci'):
        lines.append(f"  • JCI: {detail['jci']}")
    if detail.get('h_index'):
        lines.append(f"  • h-index: {detail['h_index']}")
    if detail.get('citescore'):
        lines.append(f"  • CiteScore: {detail['citescore']}")
    
    lines.append("\n【审稿周期】")
    if detail.get('review_speed_official'):
        lines.append(f"  • 官网：{detail['review_speed_official']}")
    if detail.get('review_speed_user'):
        lines.append(f"  • 网友：{detail['review_speed_user']}")
    if not detail.get('review_speed_official') and not detail.get('review_speed_user'):
        lines.append("  • 暂无数据")
    
    return '\n'.join(lines)

def main():
    if len(sys.argv) < 2:
        print("用法：python query-letpub.py <期刊名>")
        print("注意：此脚本需要配合主程序和 browser 工具使用")
        sys.exit(1)
    
    journal_name = sys.argv[1]
    print(f"准备查询 LetPub: {journal_name}")
    print("浏览器将在查询完成后自动关闭")
    
    # 返回查询信息，由主程序调用 browser 工具
    result = {
        'status': 'need_browser',
        'journal': journal_name,
        'search_url': f"https://www.letpub.com.cn/index.php?page=journalapp&searchname={journal_name}",
        'action': 'open_and_parse',
        'close_browser_after': True  # 标记查询后关闭浏览器
    }
    
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    sys.exit(main())
