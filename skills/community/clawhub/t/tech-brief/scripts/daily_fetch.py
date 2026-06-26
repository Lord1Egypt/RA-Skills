#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
科技资讯每日汇总脚本
自动采集内存、AI、算力相关的新闻、政策、热点
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# 添加脚本目录到路径
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from fetch_news import fetch_all_news
from fetch_trends import fetch_trends


def parse_args():
    parser = argparse.ArgumentParser(description='科技资讯每日简报')
    parser.add_argument('--days', type=int, default=7, help='时间范围（天）')
    parser.add_argument('--output', type=str, default='output/brief.md', help='输出文件')
    parser.add_argument('--topics', type=str, default='memory,ai,compute', help='主题筛选')
    parser.add_argument('--quiet', action='store_true', help='静默模式')
    return parser.parse_args()


def load_policy_data(days):
    """加载政策数据（复用 AI Policy Brief 的结果）"""
    # 尝试读取已有的政策数据文件
    policy_file = SCRIPT_DIR.parent / 'ai-policy-brief' / 'output' / 'policy.json'
    
    if policy_file.exists():
        try:
            with open(policy_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    
    # 如果没有，尝试运行政策采集脚本
    policy_script = SCRIPT_DIR.parent / 'ai-policy-brief' / 'scripts' / 'fetch_policy.py'
    if policy_script.exists():
        import subprocess
        try:
            result = subprocess.run(
                [sys.executable, str(policy_script), '--days', str(days)],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            if result.stdout.strip():
                return json.loads(result.stdout)
        except:
            pass
    
    return {"results": [], "total": 0}


def generate_brief(news_data, policy_data, trends_data, args):
    """生成简报"""
    query_date = datetime.now().strftime('%Y-%m-%d')
    date_from = (datetime.now() - timedelta(days=args.days)).strftime('%Y-%m-%d')
    
    # 统计数量
    news_count = len(news_data.get('results', []))
    policy_count = len(policy_data.get('results', []))
    trends_count = len(trends_data.get('results', []))
    total = news_count + policy_count + trends_count
    
    # 构建 Markdown
    brief = f"""# 📡 科技资讯简报

**查询日期**: {query_date}
**时间范围**: 最近{args.days}天（{date_from} - {query_date}）

---

## 🔥 热点话题
"""
    
    # 热点话题
    trends = trends_data.get('results', [])
    if trends:
        for item in trends[:5]:
            brief += f"- {item.get('title', '无标题')} ({item.get('source', '未知来源')})\n"
    else:
        brief += "- 暂无热点话题\n"
    
    brief += "\n## 📰 行业新闻\n"
    
    # 行业新闻
    news = news_data.get('results', [])
    if news:
        for item in news[:8]:
            title = item.get('title', '无标题')
            source = item.get('source', '未知来源')
            url = item.get('url', '#')
            date = item.get('date', '')
            brief += f"- [{title}]({url}) - {source}"
            if date:
                brief += f" ({date})"
            brief += "\n"
    else:
        brief += "- 暂无行业新闻\n"
    
    brief += "\n## 📜 政策动态\n"
    
    # 政策动态
    policies = policy_data.get('results', [])
    if policies:
        for item in policies[:5]:
            title = item.get('title', '无标题')
            source = item.get('source', '未知来源')
            url = item.get('url', '#')
            brief += f"- [{title}]({url}) - {source}\n"
    else:
        brief += "- 暂无最新政策\n"
    
    brief += f"""
---

📊 **今日共收录 {total} 条资讯**（新闻 {news_count} + 政策 {policy_count} + 热点 {trends_count}）

*自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    return brief


def main():
    args = parse_args()
    
    if not args.quiet:
        print(f"📡 开始采集科技资讯（最近{args.days}天）...")
    
    # 并发采集（模拟，实际可并行）
    if not args.quiet:
        print("  📰 采集行业新闻...")
    news_data = fetch_all_news(args.days)
    
    if not args.quiet:
        print("  📜 采集政策动态...")
    policy_data = load_policy_data(args.days)
    
    if not args.quiet:
        print("  🔥 采集热点话题...")
    trends_data = fetch_trends(args.days)
    
    # 生成简报
    brief = generate_brief(news_data, policy_data, trends_data, args)
    
    # 保存输出
    output_path = SCRIPT_DIR / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(brief)
    
    if not args.quiet:
        total = len(news_data.get('results', [])) + len(policy_data.get('results', [])) + len(trends_data.get('results', []))
        print(f"✅ 简报已生成：{output_path}")
        print(f"   共收录 {total} 条资讯")
    
    # 输出 JSON 供 AI 读取
    result = {
        "query_date": datetime.now().strftime('%Y-%m-%d'),
        "date_range": {"days": args.days},
        "total": len(news_data.get('results', [])) + len(policy_data.get('results', [])) + len(trends_data.get('results', [])),
        "news_count": len(news_data.get('results', [])),
        "policy_count": len(policy_data.get('results', [])),
        "trends_count": len(trends_data.get('results', [])),
        "brief_path": str(output_path)
    }
    
    print("\n=== JSON_OUTPUT_START ===")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print("=== JSON_OUTPUT_END ===")
    
    return result


if __name__ == '__main__':
    main()