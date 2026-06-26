#!/usr/bin/env python3
"""
Super RSS Agent CLI - 统一 RSS 订阅管理器
用法: super_rss_agent <command> [options]
"""

import argparse
import os
import sys
from datetime import datetime, timedelta, timezone

# 确保 scripts/ 在 import 路径中
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 确保 Windows 下 UTF-8 输出
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from storage import Storage, _CONFIG_DEFAULTS
from scanner import (
    fetch_url, parse_feed_xml, discover_feed_url,
    scan_blog, scan_all, strip_html, safe_parse_xml_file,
    scrape_articles_html,
    ScanResult, SSRFError, REQUEST_TIMEOUT,
)


# ---------------------------------------------------------------------------
# 输入清理
# ---------------------------------------------------------------------------

def _sanitize_text(text, max_length=500):
    """清理文本，确保存储和 XML 输出安全。
    移除控制字符并截断到 max_length。"""
    if not text:
        return text
    import re
    # 移除 XML 不安全的控制字符（保留 \n, \r, \t）
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    if len(text) > max_length:
        text = text[:max_length]
    return text.strip()


def _validate_url_format(url):
    """验证 URL 是否具有合法的协议和结构。"""
    from urllib.parse import urlparse
    parsed = urlparse(url)
    if parsed.scheme not in ('http', 'https'):
        return False
    if not parsed.netloc:
        return False
    return True


# ---------------------------------------------------------------------------
# Storage 辅助函数
# ---------------------------------------------------------------------------

_custom_db_path = None


def _get_storage():
    """获取 Storage 实例。"""
    return Storage(db_path=_custom_db_path) if _custom_db_path else Storage()


def _confirm(prompt):
    """请求用户 Y/N 确认。"""
    try:
        answer = input(f"{prompt} [y/N] ").strip().lower()
        return answer in ('y', 'yes')
    except (EOFError, KeyboardInterrupt):
        print()
        return False


# ---------------------------------------------------------------------------
# 命令
# ---------------------------------------------------------------------------

def cmd_list(args):
    """列出所有订阅"""
    with _get_storage() as store:
        blogs = store.list_blogs(category=args.category)

        if not blogs:
            print("📭 没有找到订阅")
            return

        # 按分类分组
        categories = {}
        for b in blogs:
            cat = b.get('category') or 'Uncategorized'
            categories.setdefault(cat, []).append(b)

        print(f"📚 共 {len(blogs)} 个订阅\n")

        for cat in sorted(categories):
            cat_blogs = categories[cat]
            print(f"\n【{cat}】({len(cat_blogs)})")
            print("-" * 40)
            for b in cat_blogs:
                name = b.get('name', 'Unknown')
                print(f"  • {name}")
                if args.verbose:
                    print(f"    Feed:  {b.get('feed_url', '')}")
                    if b.get('url'):
                        print(f"    URL:   {b['url']}")
                    if b.get('scrape_selector'):
                        print(f"    Selector: {b['scrape_selector']}")
                    if b.get('last_scanned'):
                        print(f"    上次扫描: {b['last_scanned']}")

        unread = store.unread_count()
        if unread > 0:
            print(f"\n📬 {unread} 篇未读文章（使用 'super_rss_agent articles' 查看）")


def cmd_add(args):
    """添加新订阅"""
    url = args.url
    feed_url = args.feed_url
    name = args.name

    # 验证 URL 格式和 SSRF 防护
    if not _validate_url_format(url):
        print(f"❌ 无效的 URL（仅支持 http/https）: {url}")
        return
    if feed_url and not _validate_url_format(feed_url):
        print(f"❌ 无效的 Feed URL（仅支持 http/https）: {feed_url}")
        return

    from scanner import _validate_url_safe, SSRFError as _SSRFError
    try:
        _validate_url_safe(url)
        if feed_url:
            _validate_url_safe(feed_url)
    except _SSRFError as e:
        print(f"❌ 已拦截: {e}")
        return

    # 清理文本输入
    name = _sanitize_text(name, max_length=200) if name else name

    with _get_storage() as store:
        # 检查是否已存在（按 feed_url）
        if feed_url:
            existing = store.get_blog(feed_url)
            if existing:
                print(f"⚠️  已存在: {existing['name']} ({feed_url})")
                return

        # 如果未指定 feed_url，尝试自动发现
        if not feed_url:
            print(f"🔍 正在为 {url} 发现 Feed URL...")
            try:
                feed_url = discover_feed_url(url)
            except SSRFError as e:
                print(f"❌ 已拦截: {e}")
                return
            if feed_url:
                print(f"✅ 已发现: {feed_url}")
                # 发现后检查重复
                existing = store.get_blog(feed_url)
                if existing:
                    print(f"⚠️  已存在: {existing['name']} ({feed_url})")
                    return
            else:
                # URL 本身可能就是 feed
                feed_url = url
                print(f"⚠️  无法自动发现 Feed，将直接使用 URL 作为 Feed: {feed_url}")

        # 如果未提供名称则自动推导
        if not name:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            name = parsed.netloc or "Unnamed"

        # 如果提供的 url 看起来就是 feed url 且没有单独的主页，则推导主页
        homepage = url
        if url == feed_url:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            homepage = f"{parsed.scheme}://{parsed.netloc}" if parsed.netloc else url

        try:
            blog_id = store.add_blog(
                name=name,
                url=homepage,
                feed_url=feed_url,
                category=args.category or "Uncategorized",
                scrape_selector=args.scrape_selector,
            )
            print(f"✅ 已添加: {name} (id={blog_id})")
            print(f"   分类: {args.category or 'Uncategorized'}")
            print(f"   Feed: {feed_url}")
        except Exception as e:
            if 'UNIQUE' in str(e):
                print(f"⚠️  Feed URL 已存在: {feed_url}")
            else:
                print(f"❌ 添加失败: {e}")


def cmd_remove(args):
    """删除订阅"""
    with _get_storage() as store:
        blog = store.get_blog(args.identifier)
        if not blog:
            print(f"❌ 未找到: {args.identifier}")
            return

        if not args.yes:
            if not _confirm(f"删除 '{blog['name']}' 及其所有文章?"):
                print("已取消")
                return

        removed = store.remove_blog(args.identifier)
        for b in removed:
            print(f"🗑️  已删除: {b.get('name')}")


def cmd_update(args):
    """更新订阅信息"""
    with _get_storage() as store:
        blog = store.get_blog(args.identifier)
        if not blog:
            print(f"❌ 未找到: {args.identifier}")
            return

        fields = {}
        if args.name:
            fields['name'] = _sanitize_text(args.name, max_length=200)
        if args.category:
            fields['category'] = _sanitize_text(args.category, max_length=100)
        if args.feed_url:
            if not _validate_url_format(args.feed_url):
                print(f"❌ 无效的 Feed URL: {args.feed_url}")
                return
            fields['feed_url'] = args.feed_url
        if args.url:
            if not _validate_url_format(args.url):
                print(f"❌ 无效的 URL: {args.url}")
                return
            fields['url'] = args.url
        if args.scrape_selector is not None:
            fields['scrape_selector'] = args.scrape_selector or None

        if not fields:
            print("⚠️  没有指定要更新的字段")
            print("   可用参数: -n/--name, -c/--category, --feed-url, --url, --scrape-selector")
            return

        # 显示变更对比
        print(f"📝 更新 '{blog['name']}':")
        for key, new_val in fields.items():
            old_val = blog.get(key, '')
            print(f"   {key}: {old_val} → {new_val}")

        store.update_blog(blog['id'], **fields)
        print(f"✅ 已更新")


def cmd_check(args):
    """检查订阅源健康状态（并发）"""
    with _get_storage() as store:
        blogs = store.list_blogs()

    if not blogs:
        print("📭 没有订阅")
        return

    print(f"🔍 正在检查 {len(blogs)} 个订阅源...\n")

    ok_count = 0
    fail_count = 0

    def check_single(blog):
        name = blog.get('name', 'Unknown')
        url = blog.get('feed_url', '')
        try:
            resp = fetch_url(url, timeout=REQUEST_TIMEOUT)
            if resp.status_code == 200:
                ct = resp.headers.get('Content-Type', '').lower()
                is_xml = 'xml' in ct or 'rss' in ct or 'atom' in ct
                if not is_xml:
                    is_xml = resp.text.strip().startswith('<?xml') or '<rss' in resp.text[:500]
                if is_xml:
                    return ('ok', name, None)
                return ('warn', name, '无效的 RSS/Atom')
            return ('fail', name, f'HTTP {resp.status_code}')
        except Exception as e:
            return ('fail', name, str(e)[:50])

    from concurrent.futures import ThreadPoolExecutor, as_completed
    max_workers = min(20, len(blogs))
    total_timeout = min(60 * len(blogs), 300)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(check_single, b): b for b in blogs}
        try:
            for future in as_completed(futures, timeout=total_timeout):
                try:
                    status, name, detail = future.result(timeout=5)
                except TimeoutError:
                    b = futures[future]
                    status, name, detail = 'fail', b.get('name', '?'), '检查超时'
                except Exception as e:
                    b = futures[future]
                    status, name, detail = 'fail', b.get('name', '?'), str(e)[:50]

                if status == 'ok':
                    print(f"✅ {name}")
                    ok_count += 1
                elif status == 'warn':
                    print(f"⚠️  {name} - {detail}")
                    fail_count += 1
                else:
                    print(f"❌ {name} - {detail}")
                    fail_count += 1
        except TimeoutError:
            # 总超时：将未完成的订阅源标记为超时
            for future, b in futures.items():
                if not future.done():
                    print(f"⏰ {b.get('name', '?')} - 检查超时")
                    fail_count += 1
                    future.cancel()

    print(f"\n📊 结果: {ok_count} 正常, {fail_count} 失败")


def cmd_fetch(args):
    """实时拉取订阅内容"""
    with _get_storage() as store:
        blog = store.get_blog(args.identifier)
        if not blog:
            print(f"❌ 未找到: {args.identifier}")
            return

    feed_url = blog.get('feed_url')
    name = blog.get('name')
    limit = args.limit
    full_content = args.full_content

    print(f"📡 正在拉取: {name}{' (全文)' if full_content else ''}\n")

    try:
        resp = fetch_url(feed_url)
        if resp.status_code != 200:
            print(f"❌ HTTP {resp.status_code}")
            return

        items = parse_feed_xml(resp.content, limit=limit, full_content=full_content)

        print(f"📰 最新 {len(items)} 条:\n")
        for i, item in enumerate(items, 1):
            print(f"{'=' * 50}")
            print(f"{i}. {item['title']}")
            if item.get('date_str'):
                print(f"   日期: {item['date_str']}")
            if args.verbose and item.get('link'):
                print(f"   链接: {item['link']}")

            if full_content and item.get('content'):
                content = item['content']
                if len(content) > 2000:
                    print(f"\n📄 全文:\n{content[:2000]}...")
                else:
                    print(f"\n📄 全文:\n{content}")
            elif not full_content:
                print(f"\n📝 摘要: {item.get('summary', '')}")
            else:
                print(f"\n⚠️  全文不可用")
            print()

    except Exception as e:
        print(f"❌ 失败: {e}")


def cmd_export(args):
    """导出为 OPML"""
    from xml.etree.ElementTree import Element, SubElement, tostring
    from xml.dom import minidom

    with _get_storage() as store:
        blogs = store.list_blogs()

    if not blogs:
        print("📭 没有可导出的订阅")
        return

    opml = Element('opml', version='2.0')
    head = SubElement(opml, 'head')
    title_elem = SubElement(head, 'title')
    title_elem.text = 'RSS Subscriptions'
    date_elem = SubElement(head, 'dateCreated')
    date_elem.text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')

    body = SubElement(opml, 'body')

    # 按分类分组
    categories = {}
    for b in blogs:
        cat = b.get('category') or 'Uncategorized'
        categories.setdefault(cat, []).append(b)

    for category in sorted(categories):
        cat_blogs = categories[category]
        safe_cat = _sanitize_text(category, max_length=100)
        cat_outline = SubElement(body, 'outline', text=safe_cat, title=safe_cat)
        parent = cat_outline

        for b in cat_blogs:
            # 清理所有属性值，确保 XML 输出安全
            safe_name = _sanitize_text(b.get('name', 'Unknown'), max_length=200)
            attrs = {
                'type': 'rss',
                'text': safe_name,
                'title': safe_name,
                'xmlUrl': b.get('feed_url', ''),
            }
            url = b.get('url', '')
            if url:
                attrs['htmlUrl'] = url
            SubElement(parent, 'outline', **attrs)

    xml_str = tostring(opml, encoding='utf-8')
    dom = minidom.parseString(xml_str)
    pretty_xml = dom.toprettyxml(indent='  ', encoding='utf-8')
    lines = [line for line in pretty_xml.decode('utf-8').split('\n') if line.strip()]
    pretty_xml = '\n'.join(lines)

    output_file = args.output or f'rss_export_{datetime.now().strftime("%Y%m%d")}.opml'

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(pretty_xml)

    print(f"✅ 已导出: {output_file}")
    print(f"📊 {len(blogs)} 个订阅源, {len(categories)} 个分类")


def cmd_import(args):
    """从 OPML 导入"""
    if not os.path.exists(args.file):
        print(f"❌ 文件未找到: {args.file}")
        return

    try:
        root = safe_parse_xml_file(args.file)
    except Exception as e:
        print(f"❌ 解析 OPML 失败: {e}")
        return

    new_feeds = []

    def walk(node, category=None):
        for outline in node.findall('outline'):
            text = outline.get('text')
            xml_url = outline.get('xmlUrl')
            html_url = outline.get('htmlUrl')

            if xml_url:
                # 验证 URL 格式（SSRF 防护）
                if not _validate_url_format(xml_url):
                    print(f"⚠️  跳过无效的 Feed URL: {xml_url}")
                    walk(outline, category=category)
                    continue
                if html_url and not _validate_url_format(html_url):
                    html_url = ""

                feed_entry = {
                    "name": _sanitize_text(text, max_length=200) or "Unnamed",
                    "feed_url": xml_url,
                    "url": html_url or "",
                    "category": _sanitize_text(category, max_length=100) or "Uncategorized",
                }
                new_feeds.append(feed_entry)

            walk(outline, category=text if not xml_url else category)

    body = root.find('body')
    if body is None:
        print("⚠️  无效的 OPML: 未找到 <body> 元素")
        return

    walk(body)

    if not new_feeds:
        print("⚠️  OPML 中未找到订阅源")
        return

    added = 0
    skipped = 0

    with _get_storage() as store:
        for feed in new_feeds:
            # 如果缺少主页则推导
            if not feed['url']:
                from urllib.parse import urlparse
                parsed = urlparse(feed['feed_url'])
                feed['url'] = f"{parsed.scheme}://{parsed.netloc}" if parsed.netloc else feed['feed_url']

            try:
                store.add_blog(
                    name=feed['name'],
                    url=feed['url'],
                    feed_url=feed['feed_url'],
                    category=feed['category'],
                )
                added += 1
            except Exception:
                skipped += 1

    print(f"✅ 已导入: {added} 个新增, {skipped} 个跳过")


def cmd_scan(args):
    """扫描订阅源获取新文章"""
    with _get_storage() as store:
        if args.name:
            blog = store.get_blog(args.name)
            if not blog:
                print(f"❌ 未找到: {args.name}")
                return
            blogs = [blog]
        else:
            blogs = store.list_blogs()

        if not blogs:
            print("📭 没有可扫描的订阅")
            return

        if not args.silent:
            print(f"🔍 正在扫描 {len(blogs)} 个订阅源 (workers={args.workers})...\n")

        results = scan_all(blogs, workers=args.workers, full_content=False)

        total_new = 0
        total_found = 0

        for scan_result, articles in results:
            if scan_result is None:
                continue

            # 如果 Feed 是自动发现的，更新博客记录
            if scan_result.discovered_feed_url:
                store.update_blog(scan_result.blog_id, feed_url=scan_result.discovered_feed_url)

            # 插入新文章
            if articles:
                new_count = store.insert_articles(scan_result.blog_id, articles)
                scan_result.new_articles = new_count
            else:
                scan_result.new_articles = 0

            # 更新上次扫描时间
            store.update_blog_last_scanned(scan_result.blog_id, datetime.now(timezone.utc).replace(tzinfo=None))

            total_new += scan_result.new_articles
            total_found += scan_result.total_found

            if not args.silent:
                source_tag = f" [{scan_result.source}]" if scan_result.source != "none" else ""
                if scan_result.error:
                    print(f"❌ {scan_result.blog_name}: {scan_result.error}")
                elif scan_result.new_articles > 0:
                    print(f"✅ {scan_result.blog_name}: "
                          f"{scan_result.new_articles} new / {scan_result.total_found} found{source_tag}")
                else:
                    print(f"   {scan_result.blog_name}: 没有新文章{source_tag}")

        if not args.silent:
            print(f"\n📊 合计: 从 {len(blogs)} 个订阅源获取 {total_new} 篇新文章")

        # 自动清理旧文章
        if store.get_config('auto_purge') == 'true':
            try:
                days = int(store.get_config('auto_purge_days'))
            except (ValueError, TypeError):
                days = 90
            purged = store.purge_articles(days=days, only_read=True)
            if purged > 0 and not args.silent:
                print(f"🧹 自动清理: 已删除 {purged} 篇超过 {days} 天的已读文章")


def _print_article_list(articles):
    """打印文章列表（共用格式）。"""
    for art in articles:
        status = "📖" if art['is_read'] else "🆕"
        art_id = art['id']
        title = art['title'][:60]
        if len(art['title']) > 60:
            title += "..."
        blog_name = art.get('blog_name', '?')

        print(f"  {status} [{art_id}] {title}")
        print(f"       博客: {blog_name}  |  {art.get('url', '')}")
        if art.get('published_date'):
            print(f"       发布时间: {art['published_date']}")
        print()


def cmd_articles(args):
    """列出文章"""
    with _get_storage() as store:
        blog_id = None
        if args.blog:
            blog = store.get_blog(args.blog)
            if not blog:
                print(f"❌ 未找到博客: {args.blog}")
                return
            blog_id = blog['id']

        total = store.count_articles(
            blog_id=blog_id,
            category=args.category,
            include_read=args.all,
        )

        articles = store.list_articles(
            blog_id=blog_id,
            category=args.category,
            include_read=args.all,
            limit=args.limit,
            offset=args.offset,
        )

    if not articles:
        print("📭 没有找到文章" if args.all else "📭 没有未读文章")
        return

    label = "（含已读）" if args.all else "（未读）"
    if args.offset:
        print(f"📰 显示第 {args.offset + 1}-{args.offset + len(articles)} 篇，共 {total} 篇{label}\n")
    else:
        shown = f"前 {len(articles)} / " if len(articles) < total else ""
        print(f"📰 {shown}共 {total} 篇文章{label}\n")

    _print_article_list(articles)

    remaining = total - args.offset - len(articles)
    if remaining > 0:
        next_offset = args.offset + len(articles)
        print(f"📄 还有 {remaining} 篇，使用 --offset {next_offset} 查看下一页")


def cmd_search(args):
    """按关键词搜索文章"""
    keyword = args.keyword
    with _get_storage() as store:
        blog_id = None
        if args.blog:
            blog = store.get_blog(args.blog)
            if not blog:
                print(f"❌ 未找到博客: {args.blog}")
                return
            blog_id = blog['id']

        articles = store.search_articles(
            keyword=keyword,
            blog_id=blog_id,
            category=args.category,
            include_read=args.all,
            limit=args.limit,
        )

    if not articles:
        scope = "所有文章" if args.all else "未读文章"
        print(f"📭 在{scope}中未找到 \"{keyword}\"")
        return

    label = "（含已读）" if args.all else "（未读）"
    print(f"🔍 搜索 \"{keyword}\"：找到 {len(articles)} 篇{label}\n")

    _print_article_list(articles)

    if len(articles) >= args.limit:
        print(f"📄 结果可能不完整，使用 -n 增加数量限制")


def cmd_read(args):
    """标记文章为已读"""
    with _get_storage() as store:
        article = store.get_article(args.id)
        if not article:
            print(f"❌ 未找到文章: {args.id}")
            return

        if article['is_read']:
            print(f"已经是已读状态: {article['title']}")
        else:
            store.mark_read(args.id)
            print(f"📖 已标记为已读: {article['title']}")


def cmd_unread(args):
    """标记文章为未读"""
    with _get_storage() as store:
        article = store.get_article(args.id)
        if not article:
            print(f"❌ 未找到文章: {args.id}")
            return

        if not article['is_read']:
            print(f"已经是未读状态: {article['title']}")
        else:
            store.mark_unread(args.id)
            print(f"🆕 已标记为未读: {article['title']}")


def cmd_read_all(args):
    """全部标记为已读"""
    with _get_storage() as store:
        blog_id = None
        if args.blog:
            blog = store.get_blog(args.blog)
            if not blog:
                print(f"❌ 未找到博客: {args.blog}")
                return
            blog_id = blog['id']

        # 先统计未读数量
        unread = store.list_articles(
            blog_id=blog_id,
            category=args.category,
            include_read=False,
        )

        if not unread:
            print("📭 没有未读文章")
            return

        if not args.yes:
            scope = ""
            if args.blog:
                scope = f"（来自 '{args.blog}'）"
            elif args.category:
                scope = f"（分类 '{args.category}'）"
            if not _confirm(f"将 {len(unread)} 篇文章{scope}标记为已读?"):
                print("已取消")
                return

        count = store.mark_all_read(blog_id=blog_id, category=args.category)
        print(f"📖 已将 {count} 篇文章标记为已读")


def cmd_digest(args):
    """获取每日更新摘要"""
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    if args.days:
        since = now - timedelta(days=args.days)
    else:
        since = now.replace(hour=0, minute=0, second=0, microsecond=0)

    print(f"📅 更新: {since.strftime('%Y-%m-%d %H:%M')} → "
          f"{now.strftime('%Y-%m-%d %H:%M')} (UTC)\n")

    # 使用 SQL 日期过滤查询已存储的文章
    with _get_storage() as store:
        blogs = store.list_blogs(category=args.category)
        if not blogs:
            print("📭 没有订阅")
            return

        recent = store.list_articles(
            category=args.category,
            include_read=True,
            since=since.isoformat(),
        )

    if recent:
        # 使用已存储的文章
        by_cat = {}
        for art in recent:
            cat = art.get('blog_category', 'Uncategorized')
            by_cat.setdefault(cat, []).append(art)

        print(f"📊 共 {len(recent)} 条\n")
        print("=" * 60)

        for cat in sorted(by_cat):
            items = by_cat[cat]
            print(f"\n【{cat}】({len(items)})")
            print("-" * 40)
            for item in items[:args.limit]:
                pub = item.get('published_date', '')
                if isinstance(pub, str) and pub:
                    try:
                        ts = datetime.fromisoformat(pub).strftime('%m-%d %H:%M')
                    except Exception:
                        ts = '??-??'
                else:
                    ts = '??-??'
                title = item['title'][:50]
                if len(item['title']) > 50:
                    title += "..."
                status = "📖" if item['is_read'] else "🆕"
                print(f"  {status} [{ts}] {title}")
                print(f"    来源: {item.get('blog_name', '?')}")
                if args.verbose and item.get('url'):
                    print(f"    链接: {item['url']}")
            if len(items) > args.limit:
                print(f"    ... 还有 {len(items) - args.limit} 条")
    else:
        # 回退：从订阅源实时拉取
        print("（该时间范围内无已存储文章，正在实时拉取...）\n")

        all_items = []
        from concurrent.futures import ThreadPoolExecutor, as_completed

        def fetch_one(blog):
            try:
                resp = fetch_url(blog['feed_url'], timeout=REQUEST_TIMEOUT)
                if resp.status_code == 200:
                    items = parse_feed_xml(resp.content, since=since)
                    for item in items:
                        item['feed_name'] = blog['name']
                        item['blog_category'] = blog.get('category', 'Uncategorized')
                    return items
            except Exception:
                pass
            return []

        max_workers = min(20, len(blogs))
        total_timeout = min(60 * len(blogs), 300)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(fetch_one, b): b for b in blogs}
            try:
                for future in as_completed(futures, timeout=total_timeout):
                    try:
                        all_items.extend(future.result(timeout=5))
                    except Exception:
                        pass
            except TimeoutError:
                # 总超时：静默跳过未完成的订阅源
                for future in futures:
                    future.cancel()

        all_items.sort(key=lambda x: x.get('published_date') or datetime.min, reverse=True)

        if not all_items:
            print(f"📭 没有新内容（已检查 {len(blogs)} 个订阅源）")
            return

        # 按分类分组
        by_cat = {}
        for item in all_items:
            cat = item.get('blog_category', 'Uncategorized')
            by_cat.setdefault(cat, []).append(item)

        print(f"📊 来自 {len(blogs)} 个订阅源的 {len(all_items)} 条内容\n")
        print("=" * 60)

        for cat in sorted(by_cat):
            items = by_cat[cat]
            print(f"\n【{cat}】({len(items)})")
            print("-" * 40)
            for item in items[:args.limit]:
                dt = item.get('published_date')
                ts = dt.strftime('%m-%d %H:%M') if dt else '??-??'
                title = item['title'][:50]
                if len(item['title']) > 50:
                    title += "..."
                print(f"  • [{ts}] {title}")
                print(f"    来源: {item.get('feed_name', '?')}")
                if args.verbose and item.get('link'):
                    print(f"    链接: {item['link']}")
            if len(items) > args.limit:
                print(f"    ... 还有 {len(items) - args.limit} 条")

    print(f"\n{'=' * 60}")
    print(f"🕐 更新时间: {now.strftime('%Y-%m-%d %H:%M')} (UTC)")


def cmd_stats(args):
    """显示订阅统计信息"""
    with _get_storage() as store:
        stats = store.get_stats()
        total_blogs = store.blog_count()
        total_unread = store.unread_count()
        db_size = store.db_size_bytes()

    if not stats:
        print("📭 没有订阅")
        return

    total_articles = sum(s['total_articles'] for s in stats)

    # 总览
    size_str = f"{db_size / 1024:.1f} KB" if db_size < 1024 * 1024 else f"{db_size / 1024 / 1024:.1f} MB"
    print(f"📊 订阅统计\n")
    print(f"   订阅源: {total_blogs}")
    print(f"   总文章: {total_articles}")
    print(f"   未读: {total_unread}")
    print(f"   数据库: {size_str}")
    print()

    # 按分类分组
    by_cat = {}
    for s in stats:
        cat = s['category'] or 'Uncategorized'
        by_cat.setdefault(cat, []).append(s)

    stale_threshold = args.stale_days
    stale_blogs = []
    now = datetime.now(timezone.utc).replace(tzinfo=None)

    for cat in sorted(by_cat):
        items = by_cat[cat]
        cat_articles = sum(s['total_articles'] for s in items)
        cat_unread = sum(s['unread_count'] or 0 for s in items)
        print(f"【{cat}】{len(items)} 个源, {cat_articles} 篇, {cat_unread} 未读")
        print("-" * 60)

        # 按未读数降序，方便发现积压
        items_sorted = sorted(items, key=lambda x: x['unread_count'] or 0, reverse=True)
        for s in items_sorted:
            name = s['name'][:25]
            if len(s['name']) > 25:
                name += "…"
            total = s['total_articles']
            unread = s['unread_count'] or 0
            latest = s['latest_article'] or ''

            # 检测最新文章日期
            latest_short = ''
            if latest:
                try:
                    latest_dt = datetime.fromisoformat(latest)
                    latest_short = latest_dt.strftime('%Y-%m-%d')
                    days_ago = (now - latest_dt).days
                    if days_ago > stale_threshold:
                        stale_blogs.append((s['name'], days_ago))
                except Exception:
                    latest_short = '?'

            bar = f"{'█' * min(unread, 20)}" if unread > 0 else ""
            print(f"  {name:<27s} {total:>4d} 篇  {unread:>3d} 未读  最新: {latest_short:<10s}  {bar}")

        print()

    # 疑似死源提示
    if stale_blogs:
        print(f"⚠️  疑似死源（超过 {stale_threshold} 天无更新）:")
        for name, days in sorted(stale_blogs, key=lambda x: x[1], reverse=True):
            print(f"   • {name} ({days} 天)")


def cmd_config(args):
    """查看或修改配置"""
    with _get_storage() as store:
        if args.key is None:
            # 列出所有配置
            config = store.list_config()
            if not config:
                print("📭 没有配置项")
                return
            print("⚙️  当前配置:\n")
            for key in sorted(config):
                value = config[key]
                default = _CONFIG_DEFAULTS.get(key)
                marker = "" if default is not None and value == default else " (已修改)"
                print(f"   {key} = {value}{marker}")
            print(f"\n   使用 'config <key> <value>' 修改配置")
            print(f"   使用 'config <key> --reset' 恢复默认值")
            return

        key = args.key

        if args.reset:
            if store.delete_config(key):
                default = _CONFIG_DEFAULTS.get(key, '(无默认值)')
                print(f"✅ 已恢复默认值: {key} = {default}")
            else:
                print(f"ℹ️  {key} 已经是默认值")
            return

        if args.value is None:
            # 查看单个配置
            value = store.get_config(key)
            default = _CONFIG_DEFAULTS.get(key)
            if value:
                marker = " (默认)" if default is not None and value == default else ""
                print(f"   {key} = {value}{marker}")
            else:
                print(f"   {key} 未设置")
            return

        # 设置配置
        value = args.value
        # 验证已知配置项
        if key == 'auto_purge' and value not in ('true', 'false'):
            print(f"❌ auto_purge 的值必须是 true 或 false")
            return
        if key == 'auto_purge_days':
            try:
                days = int(value)
                if days < 1:
                    raise ValueError
            except ValueError:
                print(f"❌ auto_purge_days 的值必须是正整数")
                return

        store.set_config(key, value)
        print(f"✅ 已设置: {key} = {value}")


def cmd_purge(args):
    """清理旧文章"""
    with _get_storage() as store:
        blog_id = None
        if args.blog:
            blog = store.get_blog(args.blog)
            if not blog:
                print(f"❌ 未找到博客: {args.blog}")
                return
            blog_id = blog['id']

        only_read = not args.include_unread
        count = store.count_purge_candidates(
            days=args.days, blog_id=blog_id, only_read=only_read)

        if count == 0:
            scope = "已读" if only_read else "所有"
            print(f"📭 没有超过 {args.days} 天的{scope}文章需要清理")
            return

        scope_desc = ""
        if args.blog:
            scope_desc += f"（来自 '{args.blog}'）"
        read_desc = "已读" if only_read else "所有（含未读）"

        print(f"🗑️  将清理 {count} 篇超过 {args.days} 天的{read_desc}文章{scope_desc}")

        if not args.yes:
            if not _confirm("确认清理?"):
                print("已取消")
                return

        deleted = store.purge_articles(
            days=args.days, blog_id=blog_id, only_read=only_read)
        print(f"✅ 已清理 {deleted} 篇旧文章")


def cmd_test(args):
    """测试 URL 是否可以被订阅（只读，不写入数据库）"""
    url = args.url

    # 第一步：URL 合法性验证
    print(f"🔍 正在测试 URL: {url}\n")
    print("=" * 60)

    print("[1/5] URL 验证...")
    if not _validate_url_format(url):
        print(f"  ❌ 无效的 URL（仅支持 http/https）: {url}")
        print(f"\n{'=' * 60}")
        print("❌ 结论: URL 无效，无法订阅")
        return

    from scanner import _validate_url_safe
    try:
        _validate_url_safe(url)
        print("  ✅ URL 格式与安全检查通过")
    except SSRFError as e:
        print(f"  ❌ 被 SSRF 防护拦截: {e}")
        print(f"\n{'=' * 60}")
        print("❌ 结论: URL 被安全策略拦截，无法订阅")
        return

    # 第二步：连通性测试
    print("\n[2/5] 连通性测试...")
    try:
        resp = fetch_url(url, timeout=15)
        ct = resp.headers.get('Content-Type', '').lower()
        print(f"  ✅ HTTP {resp.status_code} | Content-Type: {ct}")
    except Exception as e:
        print(f"  ❌ 连接失败: {e}")
        print(f"\n{'=' * 60}")
        print("❌ 结论: 无法访问该 URL，请检查网络或地址是否正确")
        return

    if resp.status_code != 200:
        print(f"  ⚠️  状态码非 200，订阅源可能无法正常访问")

    # 第三步：检测 URL 本身是否为 feed
    print("\n[3/5] 检测 Feed 类型...")
    is_feed = False
    feed_url = None

    if 'xml' in ct or 'rss' in ct or 'atom' in ct:
        is_feed = True
        feed_url = url
        print(f"  ✅ 该 URL 是 Feed（通过 Content-Type 识别）")
    else:
        text_head = resp.text[:500]
        if text_head.strip().startswith('<?xml') or '<rss' in text_head or '<feed' in text_head:
            is_feed = True
            feed_url = url
            print(f"  ✅ 该 URL 是 Feed（通过内容识别）")
        else:
            print(f"  ℹ️  该 URL 不是 Feed，将尝试自动发现")

    # 第四步：自动发现 feed
    if not is_feed:
        print("\n[4/5] 自动发现 Feed...")
        try:
            feed_url = discover_feed_url(url)
        except Exception as e:
            print(f"  ❌ 发现失败: {e}")
            feed_url = None

        if feed_url:
            print(f"  ✅ 发现 Feed: {feed_url}")
        else:
            print(f"  ⚠️  未通过 <link> 标签或常见路径发现 Feed")
    else:
        print("\n[4/5] 跳过自动发现（URL 本身已是 Feed）")

    # 第五步：获取并解析 feed，展示样本文章
    articles = []
    if feed_url:
        print("\n[5/5] 获取并解析 Feed...")
        try:
            if feed_url == url and resp.status_code == 200:
                feed_resp = resp  # 复用已有响应
            else:
                feed_resp = fetch_url(feed_url, timeout=15)

            if feed_resp.status_code == 200:
                articles = parse_feed_xml(feed_resp.content, limit=5)

                # 检测 feed 格式
                text_head = feed_resp.text[:500]
                if '<rss' in text_head:
                    fmt = "RSS 2.0"
                elif '<feed' in text_head or 'www.w3.org/2005/Atom' in text_head:
                    fmt = "Atom"
                elif 'purl.org/rss/1.0' in text_head:
                    fmt = "RSS 1.0 (RDF)"
                else:
                    fmt = "未知 XML 格式"

                print(f"  ✅ Feed 格式: {fmt}")
                print(f"  ✅ 解析到文章: {len(articles)} 篇")
            else:
                print(f"  ❌ Feed 返回 HTTP {feed_resp.status_code}")
        except Exception as e:
            print(f"  ❌ Feed 获取/解析失败: {e}")
    else:
        print("\n[5/5] 跳过 Feed 解析（无可用的 Feed URL）")

    # 展示样本文章
    if articles:
        print(f"\n{'─' * 60}")
        print(f"📰 样本文章（最多 3 篇）:\n")
        for i, art in enumerate(articles[:3], 1):
            title = art.get('title', '无标题')
            date_str = art.get('date_str', '')
            link = art.get('url') or art.get('link', '')
            summary = art.get('summary', '')
            print(f"  {i}. {title}")
            if date_str:
                print(f"     日期: {date_str}")
            if link:
                print(f"     链接: {link}")
            if summary:
                preview = summary[:100]
                if len(summary) > 100:
                    preview += "..."
                print(f"     摘要: {preview}")
            print()

    # 可选：HTML 抓取测试
    scrape_ok = False
    if args.scrape_selector:
        print(f"{'─' * 60}")
        print(f"🔧 测试 CSS 选择器: {args.scrape_selector}")
        try:
            scraped = scrape_articles_html(url, args.scrape_selector)
            if scraped:
                scrape_ok = True
                print(f"  ✅ 抓取到 {len(scraped)} 篇文章")
                for i, art in enumerate(scraped[:3], 1):
                    print(f"  {i}. {art.get('title', '无标题')}")
                    if art.get('url'):
                        print(f"     链接: {art['url']}")
            else:
                print(f"  ⚠️  选择器未匹配到任何内容")
        except Exception as e:
            print(f"  ❌ 抓取失败: {e}")

    # 最终结论
    print(f"\n{'=' * 60}")
    if articles:
        print(f"✅ 结论: 该 URL 可以订阅！")
        print(f"   推荐命令:")
        print(f"   python scripts/super_rss_agent.py add {url}")
    elif scrape_ok:
        print(f"✅ 结论: 该 URL 可通过 HTML 抓取方式订阅！")
        print(f"   推荐命令:")
        print(f"   python scripts/super_rss_agent.py add {url} --scrape-selector \"{args.scrape_selector}\"")
    elif feed_url:
        print(f"⚠️  结论: 已找到 Feed 但未返回任何文章")
        print(f"   Feed URL: {feed_url}")
        print(f"   该 Feed 可能为空或使用了不支持的格式")
    else:
        print(f"❌ 结论: 无法订阅该 URL")
        print(f"   未找到 RSS/Atom 订阅源")
        print(f"   建议: 使用 --feed-url 直接指定订阅源地址")
        print(f"   或者: 使用 --scrape-selector 测试 HTML 抓取")


# ---------------------------------------------------------------------------
# CLI 入口
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        prog='super_rss_agent',
        description='Super RSS Agent CLI - RSS 订阅管理工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  super_rss_agent --db custom.db list               # 使用自定义数据库文件
  super_rss_agent list                              # 列出所有订阅
  super_rss_agent add https://example.com           # 添加（自动发现 Feed）
  super_rss_agent add https://example.com/feed.xml --name "Blog" --category Tech
  super_rss_agent remove "订阅名称" -y              # 跳过确认直接删除
  super_rss_agent scan                              # 扫描所有订阅获取新文章
  super_rss_agent scan "博客名称" --workers 10      # 扫描指定博客
  super_rss_agent articles                          # 查看未读文章
  super_rss_agent articles --all --blog "Blog"      # 查看指定博客的所有文章
  super_rss_agent read 42                           # 标记文章 #42 为已读
  super_rss_agent read-all -y                       # 全部标记为已读
  super_rss_agent fetch "订阅名称" --full-content   # 实时拉取全文内容
  super_rss_agent digest -d 2                       # 近 2 天摘要
  super_rss_agent export -o backup.opml             # 导出为 OPML
  super_rss_agent import follow.opml                # 从 OPML 导入
  super_rss_agent test https://example.com          # 测试 URL 是否可以订阅
        '''
    )

    parser.add_argument('--db', help='自定义数据库文件路径')

    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # list
    p = subparsers.add_parser('list', help='列出所有订阅')
    p.add_argument('-c', '--category', help='按分类筛选')
    p.add_argument('-v', '--verbose', action='store_true', help='显示详细信息')

    # add
    p = subparsers.add_parser('add', help='添加订阅')
    p.add_argument('url', help='博客或 Feed URL')
    p.add_argument('-n', '--name', help='自定义名称')
    p.add_argument('-c', '--category', help='分类')
    p.add_argument('--feed-url', help='直接指定 RSS/Atom Feed URL')
    p.add_argument('--scrape-selector', help='HTML 抓取回退的 CSS 选择器')

    # remove
    p = subparsers.add_parser('remove', help='删除订阅')
    p.add_argument('identifier', help='订阅名称或 URL')
    p.add_argument('-y', '--yes', action='store_true', help='跳过确认')

    # update
    p = subparsers.add_parser('update', help='更新订阅信息')
    p.add_argument('identifier', help='订阅名称或 URL')
    p.add_argument('-n', '--name', help='新名称')
    p.add_argument('-c', '--category', help='新分类')
    p.add_argument('--feed-url', help='新 Feed URL')
    p.add_argument('--url', help='新主页 URL')
    p.add_argument('--scrape-selector', nargs='?', const='', help='新 CSS 选择器（不带值则清除）')

    # check
    subparsers.add_parser('check', help='检查订阅源健康状态')

    # fetch
    p = subparsers.add_parser('fetch', help='实时拉取订阅内容')
    p.add_argument('identifier', help='订阅名称或 URL')
    p.add_argument('-n', '--limit', type=int, default=5, help='条目数量（默认 5）')
    p.add_argument('-v', '--verbose', action='store_true', help='显示链接')
    p.add_argument('--full-content', action='store_true', help='获取全文内容')

    # scan
    p = subparsers.add_parser('scan', help='扫描订阅源获取新文章')
    p.add_argument('name', nargs='?', help='扫描指定博客（可选）')
    p.add_argument('-s', '--silent', action='store_true', help='静默模式')
    p.add_argument('-w', '--workers', type=int, default=5, help='并发线程数（默认 5）')

    # articles
    p = subparsers.add_parser('articles', help='列出文章')
    p.add_argument('-a', '--all', action='store_true', help='包含已读文章')
    p.add_argument('-b', '--blog', help='按博客名称筛选')
    p.add_argument('-c', '--category', help='按分类筛选')
    p.add_argument('-n', '--limit', type=int, default=50, help='每页条数（默认 50）')
    p.add_argument('--offset', type=int, default=0, help='跳过前 N 条（翻页用）')

    # search
    p = subparsers.add_parser('search', help='搜索文章')
    p.add_argument('keyword', help='搜索关键词')
    p.add_argument('-a', '--all', action='store_true', help='包含已读文章')
    p.add_argument('-b', '--blog', help='按博客名称筛选')
    p.add_argument('-c', '--category', help='按分类筛选')
    p.add_argument('-n', '--limit', type=int, default=50, help='最大结果数（默认 50）')

    # read
    p = subparsers.add_parser('read', help='标记文章为已读')
    p.add_argument('id', type=int, help='文章 ID')

    # unread
    p = subparsers.add_parser('unread', help='标记文章为未读')
    p.add_argument('id', type=int, help='文章 ID')

    # read-all
    p = subparsers.add_parser('read-all', help='全部标记为已读')
    p.add_argument('-b', '--blog', help='按博客名称筛选')
    p.add_argument('-c', '--category', help='按分类筛选')
    p.add_argument('-y', '--yes', action='store_true', help='跳过确认')

    # digest
    p = subparsers.add_parser('digest', help='获取每日摘要')
    p.add_argument('-d', '--days', type=int, help='最近 N 天')
    p.add_argument('-n', '--limit', type=int, default=5, help='每个分类的条目数（默认 5）')
    p.add_argument('-c', '--category', help='按分类筛选')
    p.add_argument('-v', '--verbose', action='store_true', help='显示链接和错误信息')

    # stats
    p = subparsers.add_parser('stats', help='显示订阅统计信息')
    p.add_argument('--stale-days', type=int, default=90, help='超过多少天视为死源（默认 90）')

    # config
    p = subparsers.add_parser('config', help='查看或修改配置')
    p.add_argument('key', nargs='?', help='配置项名称')
    p.add_argument('value', nargs='?', help='新值')
    p.add_argument('--reset', action='store_true', help='恢复为默认值')

    # purge
    p = subparsers.add_parser('purge', help='清理旧文章')
    p.add_argument('-d', '--days', type=int, default=90, help='清理多少天以前的文章（默认 90）')
    p.add_argument('-b', '--blog', help='仅清理指定博客的文章')
    p.add_argument('--include-unread', action='store_true', help='同时清理未读文章（默认只清已读）')
    p.add_argument('-y', '--yes', action='store_true', help='跳过确认')

    # export
    p = subparsers.add_parser('export', help='导出为 OPML')
    p.add_argument('-o', '--output', help='输出文件名')

    # import
    p = subparsers.add_parser('import', help='从 OPML 导入')
    p.add_argument('file', help='OPML 文件路径')

    # test
    p = subparsers.add_parser('test', help='测试 URL 是否可以订阅')
    p.add_argument('url', help='要测试的博客或 Feed URL')
    p.add_argument('--scrape-selector', help='测试 HTML 抓取的 CSS 选择器')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    global _custom_db_path
    if args.db:
        _custom_db_path = args.db

    commands = {
        'list': cmd_list,
        'add': cmd_add,
        'remove': cmd_remove,
        'update': cmd_update,
        'check': cmd_check,
        'fetch': cmd_fetch,
        'scan': cmd_scan,
        'articles': cmd_articles,
        'search': cmd_search,
        'read': cmd_read,
        'unread': cmd_unread,
        'read-all': cmd_read_all,
        'digest': cmd_digest,
        'stats': cmd_stats,
        'config': cmd_config,
        'purge': cmd_purge,
        'export': cmd_export,
        'import': cmd_import,
        'test': cmd_test,
    }

    commands[args.command](args)


if __name__ == '__main__':
    main()
