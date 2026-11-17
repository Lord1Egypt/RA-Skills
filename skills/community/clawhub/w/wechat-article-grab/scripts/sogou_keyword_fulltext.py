#!/usr/bin/env python3
"""
sogou_keyword_fulltext.py - 一键式关键词搜 + 拿全文

工作流：
1. 关键词 → mptext compare 拿爆款文章（自动尝试关键词变体）
2. 提取 (标题, 公众号) 配对
3. 对每个公众号 → mptext full 路径拿全文
4. 输出 Markdown / JSON 报告

用法：
  # 一键搞定
  python3 sogou_keyword_fulltext.py "Qwen3.8 测评"
  
  # 跳过 mptext，用 sogou.md
  python3 sogou_keyword_fulltext.py "关键词" --sogou-md sogou.md
"""

import sys
import os
import re
import json
import argparse
import subprocess
from typing import List, Dict, Optional

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from mptext_api import get_client as get_mptext_client


def normalize_title(title: str) -> str:
    """标准化标题用于去重"""
    return ''.join(c for c in title if '\u4e00' <= c <= '\u9fff' or c.isalnum()).lower()


def fetch_via_compare(keyword: str, max_articles: int = 10) -> List[Dict]:
    """
    通过 mptext compare 拿关键词爆款文章
    自动尝试关键词变体（去空格、单字）
    """
    keyword_variants = [keyword]
    if ' ' in keyword:
        keyword_variants.append(keyword.replace(' ', ''))
    # 也加单字尝试（适用于组合词）
    for kw in [keyword, keyword.split(' ')[0] if ' ' in keyword else keyword]:
        if kw not in keyword_variants:
            keyword_variants.append(kw)
    
    for kw in keyword_variants:
        try:
            result = subprocess.run(
                ['python3', os.path.join(SCRIPT_DIR, 'gzh_article.py'), 'compare', kw],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode != 0:
                continue
            if '共 0 条' in result.stdout or '总数据量: 0' in result.stdout:
                continue
            
            articles = _parse_compare_output(result.stdout)
            if articles:
                if kw != keyword:
                    print(f"  💡 关键词 '{kw}' 命中（去空格）")
                return articles[:max_articles]
        except Exception as e:
            print(f"  [compare error]: {e}", file=sys.stderr)
    
    return []


def _parse_compare_output(output: str) -> List[Dict]:
    """解析 gzh_article.py compare 的输出"""
    articles = []
    current = {}
    for line in output.split('\n'):
        title_match = re.match(r'📄\s*\d+\.\s*(.+)', line)
        if title_match:
            if current.get('title'):
                articles.append(current)
            current = {'title': title_match.group(1).strip()}
            continue

        url_match = re.search(r'🔗\s*(https?://\S+)', line)
        if url_match:
            current['url'] = url_match.group(1).strip()
            continue

        account_match = re.search(r'👤\s*([^|]+)', line)
        if account_match:
            current['account'] = account_match.group(1).strip()
            continue

        time_match = re.search(r'📅\s*([\d\-: ]+)', line)
        if time_match:
            current['time'] = time_match.group(1).strip()
            continue

        read_match = re.search(r'阅读:\s*([\d,]+)', line)
        if read_match:
            current['reads'] = read_match.group(1).strip()
            continue

        if '📝 正文:' in line:
            current['summary'] = line.split('📝 正文:', 1)[1].strip()[:200]
            continue

    if current.get('title'):
        articles.append(current)
    return articles


def fetch_sogou_from_md(md_path: str) -> List[Dict]:
    """从 sogou markdown 文件解析"""
    with open(md_path, 'r', encoding='utf-8') as f:
        md = f.read()
    
    articles = []
    blocks = md.split('### [')
    
    for block in blocks[1:]:
        first_line_end = block.find('\n')
        if first_line_end == -1:
            continue
        title_part = block[:first_line_end]
        
        title_end = title_part.find('](')
        if title_end == -1:
            continue
        title = title_part[:title_end].strip()
        
        rest = block[first_line_end + 1:]
        lines = [l.strip() for l in rest.split('\n') if l.strip()]
        
        account = None
        summary = None
        for line in lines:
            clean_line = line.lstrip('* ').strip()
            if clean_line.startswith('!') or 'sogoucdn' in clean_line or 'qpic.cn' in clean_line:
                continue
            if clean_line.startswith('/link') or clean_line.startswith('http'):
                continue
            if summary is None and clean_line.startswith(('导语', '摘要', '正文', '【')):
                summary = clean_line
                continue
            if account is None:
                if (4 <= len(clean_line) <= 30 and
                    not any(c in clean_line for c in '/?&=[]().，:：；！。、*#@') and
                    not clean_line.startswith(('http', '导语', '摘要', '搜索', '请', '联系'))):
                    chinese_chars = sum(1 for c in clean_line if '一' <= c <= '鿿')
                    if chinese_chars >= 2:
                        account = clean_line
                        break
        
        articles.append({
            'title': title,
            'account': account,
            'summary': summary or '',
            'sogou_url': 'https://weixin.sogou.com/link?url=...'
        })
    
    return articles


def fetch_with_gzh(url: str) -> Optional[str]:
    """
    拿完整正文，优先级：
    1. gzh_article.py mpdownload（拿 1000-4000+ 字）
    2. gzh_article.py fetch（fallback）
    3. mptext download_article（最后 fallback）
    """
    # 1. mpdownload（直接调 mptext 公共 API，最完整）
    try:
        result = subprocess.run(
            ['python3', os.path.join(SCRIPT_DIR, 'gzh_article.py'), 'mpdownload', url],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0 and len(result.stdout) > 100:
            # mpdownload 返回的格式: 标题\n公众号\n...正文...
            lines = result.stdout.split('\n')
            # 跳过前 4-5 行（标题/公众号/分隔）
            content_lines = []
            skip_first_n = 0
            for i, line in enumerate(lines):
                if skip_first_n < 4 and (not line.strip() or '原创' in line or '来源' in line or '在小说阅读器' in line or '点下方' in line):
                    skip_first_n += 1
                    continue
                content_lines.append(line)
            content = '\n'.join(content_lines).strip()
            if len(content) > 50:
                return content
    except Exception:
        pass

    # 2. fetch
    if 'chksm=' not in url:
        test_url = url + ('&chksm=placeholder' if '?' in url else '?chksm=placeholder')
    else:
        test_url = url

    try:
        result = subprocess.run(
            ['python3', os.path.join(SCRIPT_DIR, 'gzh_article.py'), 'fetch', test_url],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            content_lines = []
            started = False
            for line in lines:
                if line.startswith('📄 '):
                    started = True
                    continue
                if started and line.strip():
                    if '共 ' in line and '字' in line:
                        break
                    content_lines.append(line)
            content = '\n'.join(content_lines).strip()
            if len(content) > 50:
                return content
    except Exception:
        pass

    # 3. mptext download_article
    client = get_mptext_client()
    try:
        return client.download_article(url, format='text')
    except Exception:
        return None


def fetch_full_text_via_full(account_name: str, target_title: str, max_count: int = 20) -> Optional[Dict]:
    """通过 mptext full 路径 + 标题匹配拿完整 URL"""
    client = get_mptext_client()
    try:
        accounts = client.search_account(account_name, size=3)
        if not accounts:
            return None

        matched_acc = None
        for acc in accounts:
            if acc.nickname == account_name:
                matched_acc = acc
                break
        if not matched_acc:
            matched_acc = accounts[0]

        articles = client.get_articles(matched_acc.fakeid, size=max_count)

        for art in articles:
            title_norm = normalize_title(art.title)
            target_norm = normalize_title(target_title)
            # 1. 精确包含
            if target_norm in title_norm or title_norm in target_norm:
                content = fetch_with_gzh(art.link)
                if content:
                    return {
                        'url': art.link,
                        'account': matched_acc.nickname,
                        'title': art.title,
                        'full_text': content,
                        'full_text_length': len(content)
                    }
            # 2. 多关键词必须都命中（去除通用词后剩的关键词）
            stop_words = {'这份', '这个', '那篇', '一篇', '一文', '看看', '如何', '怎么', '怎样', '详解', '全网', '汇总', '简介'}
            target_words = [w for w in set(target_norm) if len(w) >= 3 and w not in stop_words]
            if target_words:
                hit_count = sum(1 for w in target_words if w in title_norm)
                # 要求 80% 以上的关键词命中
                if hit_count >= len(target_words) * 0.8:
                    content = fetch_with_gzh(art.link)
                    if content:
                        return {
                            'url': art.link,
                            'account': matched_acc.nickname,
                            'title': art.title,
                            'full_text': content,
                            'full_text_length': len(content)
                        }
    except Exception as e:
        print(f"    [full match error]: {e}", file=sys.stderr)
    return None


def process_articles(articles: List[Dict], max_results: int = 10, 
                     fetch_content: bool = True) -> List[Dict]:
    """对每篇文章尝试拿全文"""
    results = []
    for i, art in enumerate(articles[:max_results], 1):
        title = art.get('title', '')
        account = art.get('account', '')
        
        print(f"\n[{i}/{min(len(articles), max_results)}] {title[:55]}...")
        
        full_data = None
        if fetch_content and account:
            print(f"  📥 搜 '{account}' 匹配...", end='')
            result = fetch_full_text_via_full(account, title)
            if result:
                full_data = result
                full_data['summary'] = art.get('summary', '')
                full_data['reads'] = art.get('reads', '')
                full_data['fetch_method'] = 'account_match'
                print(f" ✅ {result['full_text_length']} 字")
            else:
                print(f" ⚠️")
        
        if not full_data:
            full_data = {
                'title': title,
                'url': art.get('url', ''),
                'account': account,
                'summary': art.get('summary', ''),
                'reads': art.get('reads', ''),
                'full_text': None,
                'full_text_length': 0,
                'fetch_method': 'failed'
            }
            if fetch_content:
                print(f"  ⚠️ 未能拿到全文")
        
        results.append(full_data)
    return results


def deduplicate(articles: List[Dict]) -> List[Dict]:
    """去重（按标准化标题）"""
    seen = set()
    result = []
    for art in articles:
        norm = normalize_title(art.get('title', ''))
        if norm and norm not in seen:
            seen.add(norm)
            result.append(art)
    return result


def print_report(keyword: str, results: List[Dict], source: str):
    """详细模式报告"""
    print(f"\n{'='*70}")
    print(f"🔍 关键词搜: {keyword}")
    print(f"📊 数据源: {source}")
    print(f"📊 处理: {len(results)} 篇")
    print('='*70)
    
    total_full = sum(1 for r in results if r.get('full_text'))
    
    for i, r in enumerate(results, 1):
        if r.get('full_text'):
            status = f"✅ {r['full_text_length']} 字"
        else:
            status = "⚠️ 仅元数据"
        print(f"\n{i}. {r['title']}")
        print(f"   公众号: {r.get('account', 'unknown')}")
        if r.get('reads'):
            print(f"   阅读: {r['reads']}")
        if r.get('summary'):
            print(f"   摘要: {r['summary'][:80]}...")
        url_short = r.get('url', '')[:80]
        print(f"   URL: {url_short}{'...' if len(r.get('url', '')) > 80 else ''}")
        print(f"   {status}")
        if r.get('full_text'):
            print(f"   全文: {r['full_text'][:150].replace(chr(10), ' ')}...")
    
    print(f"\n{'='*70}")
    print(f"📊 拿完整正文: {total_full}/{len(results)} 篇")
    print('='*70)


def print_summary(keyword: str, results: List[Dict], source: str):
    """汇总模式报告"""
    print(f"\n{'='*70}")
    print(f"🔍 {keyword} - 汇总")
    print('='*70)
    
    total_full = sum(1 for r in results if r.get('full_text'))
    print(f"\n📊 数据源: {source} | {len(results)} 篇 | 拿全文 {total_full} 篇")
    
    by_account = {}
    for r in results:
        acc = r.get('account') or '(未知)'
        by_account.setdefault(acc, []).append(r)
    
    for acc, arts in by_account.items():
        full_in = sum(1 for a in arts if a.get('full_text'))
        print(f"\n  【{acc}】({full_in}/{len(arts)} 完整)")
        for art in arts:
            title_short = art['title'][:50]
            if art.get('full_text'):
                print(f"    ✅ 《{title_short}》 {art['full_text_length']} 字")
            else:
                print(f"    ⚠️ 《{title_short}》")
    
    print(f"\n{'='*70}")


def main():
    parser = argparse.ArgumentParser(
        description='一键式关键词搜 + 拿全文',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
完整流程（一步搞定）：
  python3 sogou_keyword_fulltext.py "Qwen3.8 测评"
  
或用 sogou.md（如果有现成的）：
  python3 sogou_keyword_fulltext.py "关键词" --sogou-md sogou.md
        """
    )
    parser.add_argument('keyword', help='搜索关键词')
    parser.add_argument('--sogou-md', help='可选：sogou markdown 文件路径')
    parser.add_argument('--max', type=int, default=10, help='最多处理几篇')
    parser.add_argument('--no-full', action='store_true', help='不抓全文')
    parser.add_argument('--format', choices=['detailed', 'summary', 'both'], default='detailed')
    parser.add_argument('--output', choices=['json', 'markdown'], default='markdown')
    parser.add_argument('--save-json', help='保存结果到 JSON')
    args = parser.parse_args()
    
    # Step 1: 拿文章列表
    if args.sogou_md:
        print(f"📊 从 {args.sogou_md} 提取...")
        articles = fetch_sogou_from_md(args.sogou_md)
        source = f"sogou.md ({len(articles)} 篇)"
    else:
        print(f"📊 mptext compare 搜 '{args.keyword}'...")
        articles = fetch_via_compare(args.keyword, max_articles=args.max)
        source = f"mptext compare ({len(articles)} 篇)"
    
    print(f"📊 搜到: {len(articles)} 篇")
    
    # Step 2: 去重
    articles = deduplicate(articles)
    print(f"🔀 去重后: {len(articles)} 篇")
    
    # Step 3: 拿全文
    results = process_articles(articles, args.max, fetch_content=not args.no_full)
    
    # 输出
    if args.output == 'json':
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        if args.format in ('detailed', 'both'):
            print_report(args.keyword, results, source)
        if args.format in ('summary', 'both'):
            print_summary(args.keyword, results, source)
    
    if args.save_json:
        with open(args.save_json, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n💾 保存到: {args.save_json}")


if __name__ == '__main__':
    main()