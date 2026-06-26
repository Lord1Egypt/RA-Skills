#!/usr/bin/env python3
"""
微信公众号文章分析器
自动提取关键信息并生成结构化报告
"""

import requests
import re
import json
import yaml
from html import unescape
from datetime import datetime
import argparse
import sys


def read_wechat_article(url):
    """读取微信公众号文章内容"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code != 200:
            return None, f"请求失败: {response.status_code}"
        
        html = response.text
        
        # 提取标题
        title_match = re.search(r'<h1[^>]*class="rich_media_title[^"]*"[^>]*>(.*?)</h1>', html, re.DOTALL)
        title = re.sub(r'<[^>]+>', '', title_match.group(1)) if title_match else "未找到标题"
        title = unescape(title).strip()
        
        # 提取正文
        content_match = re.search(r'<div[^>]*id="js_content"[^>]*>(.*?)</div>\s*<script', html, re.DOTALL)
        if content_match:
            content_html = content_match.group(1)
            content = re.sub(r'<p[^>]*>', '\n', content_html)
            content = re.sub(r'<br[^>]*>', '\n', content)
            content = re.sub(r'<[^>]+>', '', content)
            content = unescape(content)
            content = re.sub(r'\n{3,}', '\n\n', content).strip()
        else:
            content = "未找到正文"
        
        return {"title": title, "content": content, "url": url}, None
        
    except Exception as e:
        return None, str(e)


def extract_timeline(content):
    """提取时间线"""
    timeline = []
    
    # 日期模式匹配
    date_patterns = [
        (r'(\d{4})年(\d{1,2})月(\d{1,2})日', 'date'),
        (r'(\d{4})-(\d{2})-(\d{2})', 'date'),
        (r'(\d{1,2})月(\d{1,2})日', 'date_partial'),
    ]
    
    # 关键词匹配
    event_keywords = {
        '封杀': 'ban',
        '禁止': 'prohibition',
        '宣布': 'announcement',
        '加入': 'join',
        '跳槽': 'job_change',
        '邮件': 'email',
        '通知': 'notification',
        '更新': 'update',
        '推出': 'launch',
    }
    
    # 简单提取包含日期的句子
    lines = content.split('\n')
    seen_events = set()
    
    for line in lines:
        line = line.strip()
        if len(line) < 10 or len(line) > 200:
            continue
            
        for pattern, ptype in date_patterns:
            match = re.search(pattern, line)
            if match:
                event_key = line[:50]
                if event_key in seen_events:
                    break
                seen_events.add(event_key)
                
                event_type = 'general'
                for keyword, etype in event_keywords.items():
                    if keyword in line:
                        event_type = etype
                        break
                
                timeline.append({
                    'date_text': match.group(0),
                    'event': line,
                    'type': event_type
                })
                break
    
    return timeline[:15]


def extract_stakeholders(content):
    """提取关键人物/公司"""
    stakeholders = []
    seen_names = set()
    
    # 公司/组织
    companies = [
        ('Anthropic', 'AI Company'),
        ('OpenAI', 'AI Company'),
        ('OpenClaw', 'Third-party Tool'),
        ('Claude', 'AI Product'),
        ('新智元', 'Media'),
        ('Hacker News', 'Community'),
        ('Semafor', 'Media'),
        ('The Verge', 'Media'),
    ]
    
    # 人名
    people = [
        ('Peter Steinberger', 'OpenClaw Founder'),
        ('Boris Cherny', 'Claude Code Lead'),
        ('Dave Morin', 'OpenClaw Board'),
        ('Matthew Berman', 'AI Blogger'),
        ('Paul Smith', 'Anthropic CBO'),
    ]
    
    for name, role in companies:
        if name in content and name not in seen_names:
            seen_names.add(name)
            sentences = re.findall(r'[^。！？]*' + re.escape(name) + r'[^。！？]*[。！？]', content)
            stakeholders.append({
                'name': name,
                'type': 'company',
                'role': role,
                'mentions': len(sentences),
                'context': sentences[:2] if sentences else []
            })
    
    for name, role in people:
        if name in content and name not in seen_names:
            seen_names.add(name)
            sentences = re.findall(r'[^。！？]*' + re.escape(name) + r'[^。！？]*[。！？]', content)
            stakeholders.append({
                'name': name,
                'type': 'person',
                'role': role,
                'mentions': len(sentences),
                'context': sentences[:2] if sentences else []
            })
    
    return stakeholders


def extract_facts(content):
    """提取核心事实"""
    facts = []
    
    # 金额
    money_pattern = r'\$?\d+[\d,]*(?:\.\d+)?\s*(?:美元|USD|\$|dollar|元)'
    money_matches = list(set(re.findall(money_pattern, content, re.IGNORECASE)))
    if money_matches:
        facts.append({'type': 'money', 'values': money_matches[:5]})
    
    # 百分比
    percent_pattern = r'\d+(?:\.\d+)?%'
    percent_matches = list(set(re.findall(percent_pattern, content)))
    if percent_matches:
        facts.append({'type': 'percentage', 'values': percent_matches[:5]})
    
    # CVE/漏洞编号
    cve_pattern = r'CVE-\d{4}-\d+'
    cve_matches = re.findall(cve_pattern, content)
    if cve_matches:
        facts.append({'type': 'vulnerability', 'values': cve_matches})
    
    # CVSS 分数
    cvss_pattern = r'CVSS\s+(\d+\.?\d*)'
    cvss_matches = re.findall(cvss_pattern, content)
    if cvss_matches:
        facts.append({'type': 'cvss_score', 'values': cvss_matches})
    
    # 数字统计
    number_pattern = r'(\d{1,3}(?:,\d{3})+|\d+)\s*(?:个|次|天|小时|分钟|秒|万|千|百)'
    number_matches = list(set(re.findall(number_pattern, content)))
    if number_matches:
        facts.append({'type': 'statistics', 'values': number_matches[:5]})
    
    return facts


def extract_themes(content):
    """提取主题"""
    themes = []
    
    theme_keywords = {
        '平台锁定': ['平台锁定', '垂直整合', '生态锁定'],
        '开源与闭源': ['开源', '闭源', '开放', '封闭'],
        '商业竞争': ['竞争', '商业', '利益', '成本'],
        '开发者权益': ['开发者', '社区', '信任', '权益'],
        'AI伦理': ['伦理', '道德', '责任', '安全'],
    }
    
    for theme_name, keywords in theme_keywords.items():
        for keyword in keywords:
            if keyword in content:
                themes.append(theme_name)
                break
    
    return list(set(themes))


def extract_quotes(content):
    """提取引语"""
    quotes = []
    
    # 匹配引号内容
    quote_patterns = [
        r'["""]([^"""]+)["""]',
        r'["]([^"]+)["]',
        r'[『]([^』]+)[』]',
        r'[「]([^」]+)[」]',
    ]
    
    for pattern in quote_patterns:
        matches = re.findall(pattern, content)
        for match in matches:
            if len(match) > 10 and len(match) < 200:
                # 查找说话人
                context = content[max(0, content.find(match) - 100):content.find(match)]
                speaker_match = re.search(r'([^，。：:]+)[：:]', context)
                speaker = speaker_match.group(1).strip()[-20:] if speaker_match else "Unknown"
                
                quotes.append({
                    'text': match,
                    'speaker': speaker,
                    'length': len(match)
                })
    
    # 去重并排序
    seen = set()
    unique_quotes = []
    for q in quotes:
        if q['text'] not in seen:
            seen.add(q['text'])
            unique_quotes.append(q)
    
    return sorted(unique_quotes, key=lambda x: x['length'], reverse=True)[:10]


def generate_opencli_adapter(article, timeline, stakeholders, facts, themes, quotes):
    """生成 OpenCLI 适配器"""
    adapter = {
        'name': 'wechat-article-analysis',
        'version': '1.0.0',
        'description': f"Analysis of: {article['title']}",
        'source': {
            'title': article['title'],
            'url': article['url'],
        },
        'generated_at': datetime.now().isoformat(),
        'analysis': {
            'timeline': timeline,
            'stakeholders': stakeholders,
            'facts': facts,
            'themes': themes,
            'quotes': quotes,
        },
        'commands': {
            'summary': {'description': 'Get article summary'},
            'timeline': {'description': 'Show event timeline'},
            'stakeholders': {'description': 'List key players'},
            'facts': {'description': 'Show key facts'},
            'themes': {'description': 'Show analysis themes'},
            'quotes': {'description': 'Show notable quotes'},
        }
    }
    return adapter


def generate_markdown_report(article, timeline, stakeholders, facts, themes, quotes):
    """生成 Markdown 报告"""
    report = f"""# 📰 {article['title']}

**🔗 来源:** {article['url']}
**📅 分析时间:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 📅 事件时间线

"""
    
    for i, event in enumerate(timeline[:10], 1):
        emoji = {
            'ban': '🚫', 'prohibition': '⛔', 'announcement': '📢',
            'join': '👋', 'job_change': '💼', 'email': '✉️',
            'notification': '📨', 'update': '📝', 'launch': '🚀',
        }.get(event['type'], '📌')
        
        report += f"{emoji} **{event['date_text']}** - {event['event'][:80]}\n\n"
    
    report += "\n## 👥 关键人物/组织\n\n"
    for s in stakeholders[:10]:
        icon = '🏢' if s['type'] == 'company' else '👤'
        report += f"{icon} **{s['name']}** ({s['role']}) - 提及 {s['mentions']} 次\n"
        if s['context']:
            report += f"   > {s['context'][0][:80]}...\n"
        report += "\n"
    
    report += "\n## 📊 核心事实\n\n"
    for fact in facts:
        emoji = {
            'money': '💰', 'percentage': '📈', 'vulnerability': '🔒',
            'cvss_score': '⚠️', 'statistics': '📉',
        }.get(fact['type'], '📌')
        report += f"{emoji} **{fact['type']}:** {', '.join(fact['values'][:3])}\n"
    
    report += "\n## 🎯 主题分析\n\n"
    for theme in themes:
        report += f"- {theme}\n"
    
    report += "\n## 💬 重要引语\n\n"
    for i, quote in enumerate(quotes[:5], 1):
        report += f'{i}. **{quote["speaker"]}:** "{quote["text"][:100]}..."\n\n'
    
    return report


def generate_json_report(article, timeline, stakeholders, facts, themes, quotes):
    """生成 JSON 报告"""
    return {
        'article': article,
        'analysis': {
            'timeline': timeline,
            'stakeholders': stakeholders,
            'facts': facts,
            'themes': themes,
            'quotes': quotes,
        },
        'generated_at': datetime.now().isoformat(),
    }


def main():
    parser = argparse.ArgumentParser(
        description='微信公众号文章分析器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s https://mp.weixin.qq.com/s/xxx
  %(prog)s https://mp.weixin.qq.com/s/xxx --format markdown --output report.md
  %(prog)s https://mp.weixin.qq.com/s/xxx --format opencli --output adapter.yaml
  %(prog)s https://mp.weixin.qq.com/s/xxx --format json --output data.json
        """
    )
    parser.add_argument('url', help='微信公众号文章链接')
    parser.add_argument('--format', '-f', choices=['markdown', 'opencli', 'json', 'all'],
                        default='markdown', help='输出格式 (默认: markdown)')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--verbose', '-v', action='store_true', help='显示详细过程')
    
    args = parser.parse_args()
    
    if args.verbose:
        print(f"🔍 正在读取文章: {args.url}")
    
    # 读取文章
    article, error = read_wechat_article(args.url)
    if error:
        print(f"❌ 错误: {error}", file=sys.stderr)
        sys.exit(1)
    
    if args.verbose:
        print(f"✅ 读取成功: {article['title']}")
        print(f"📝 内容长度: {len(article['content'])} 字符")
    
    # 提取信息
    if args.verbose:
        print("🔍 正在提取时间线...")
    timeline = extract_timeline(article['content'])
    
    if args.verbose:
        print(f"🔍 发现 {len(timeline)} 个时间事件")
        print("🔍 正在提取关键人物...")
    stakeholders = extract_stakeholders(article['content'])
    
    if args.verbose:
        print(f"🔍 发现 {len(stakeholders)} 个关键人物/组织")
        print("🔍 正在提取核心事实...")
    facts = extract_facts(article['content'])
    
    if args.verbose:
        print(f"🔍 发现 {len(facts)} 类事实数据")
        print("🔍 正在提取主题...")
    themes = extract_themes(article['content'])
    
    if args.verbose:
        print(f"🔍 发现 {len(themes)} 个主题")
        print("🔍 正在提取引语...")
    quotes = extract_quotes(article['content'])
    
    if args.verbose:
        print(f"🔍 发现 {len(quotes)} 条引语")
    
    # 生成输出
    if args.format == 'markdown' or args.format == 'all':
        output = generate_markdown_report(article, timeline, stakeholders, facts, themes, quotes)
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"✅ Markdown 报告已保存: {args.output}")
        else:
            print(output)
    
    if args.format == 'opencli' or args.format == 'all':
        adapter = generate_opencli_adapter(article, timeline, stakeholders, facts, themes, quotes)
        output_file = args.output or 'adapter.yaml'
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(adapter, f, allow_unicode=True)
        print(f"✅ OpenCLI 适配器已保存: {output_file}")
    
    if args.format == 'json' or args.format == 'all':
        report = generate_json_report(article, timeline, stakeholders, facts, themes, quotes)
        output_file = args.output or 'report.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"✅ JSON 报告已保存: {output_file}")
    
    if args.verbose:
        print("\n✅ 分析完成!")


if __name__ == '__main__':
    main()