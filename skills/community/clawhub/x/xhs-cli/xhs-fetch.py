#!/usr/bin/env python3
"""
xhs-fetch.py — 小红书抓取 skill 核心脚本

子命令:
  1. search <keyword> [--sort hot|time] [--limit N]    主题搜索
  2. note   <note_id> [--comments N]                    单笔记详情 + 评论
  3. user-search <name>                                  用户名 → user_id
  4. user   <user_id> [--notes N]                        用户主页 + 作品列表
  5. paths                                                打印当前路径配置

数据路径: 全部走 agent-browser (官方 JS 环境 + 真实浏览器指纹)
         利用 xhs 页面已经加载的 X-s 签名函数 调 API
         不需要重写签名算法

cookie 路径由 paths.py 统一管理 (默认 $SKILL/data/, 可用 XHS_DATA_DIR 覆盖)
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from urllib.parse import urlparse, quote

# 路径统一管理
from paths import (
    COOKIE_FILE, STATE_FILE, DATA_DIR, NOTES_DIR, USERS_DIR, EXPORTS_DIR,
    report as report_paths,
)

# xhs API 域名
EDITH_BASE = "https://edith.xiaohongshu.com"
WEB_BASE = "https://www.xiaohongshu.com"


def err(msg):
    print(f"❌ {msg}", file=sys.stderr)


def ok(msg):
    print(f"✅ {msg}")


def run(cmd, timeout=30, check=True):
    """跑 agent-browser 命令"""
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if check and r.returncode != 0:
        print(f"  stdout: {r.stdout[:300]}")
        print(f"  stderr: {r.stderr[:300]}")
    return r


def ab_open(url, state_file=None, timeout=30):
    """open URL (with optional state)"""
    cmd = ['agent-browser', 'open', url]
    if state_file:
        cmd.extend(['--state', str(state_file)])
    return run(cmd, timeout=timeout)


def check_block(r_stdout):
    """检查返回结果是否被风控/拦截,返回错误码字符串或 None"""
    if '300012' in r_stdout or 'IP存在风险' in r_stdout:
        return '300012_ip_risk'
    if '300031' in r_stdout or '暂时无法浏览' in r_stdout or '页面不见了' in r_stdout:
        return '300031_note_blocked'
    if '300011' in r_stdout or '账号异常' in r_stdout:
        return '300011_account_abnormal'
    if '安全限制' in r_stdout or 'error_code' in r_stdout:
        return 'unknown_risk'
    return None


def ab_eval(js, timeout=15):
    """evaluate JS, return parsed Python object (dict / list / str / int)

    agent-browser eval 永远把返回值序列化成 JSON 字符串输出,
    而且是 双层 JSON 编码:
      1) JS 端 JSON.stringify(obj) -> '{"a":1}'
      2) agent-browser 把这个字符串当返回值再 dump 一次 -> '"{\\"a\\":1}"'
    所以 Python 端要 json.loads 两次才能拿到 dict。
    约定: JS 端必须用 JSON.stringify(...) 包裹返回值,保证序列化。
    """
    r = run(['agent-browser', 'eval', js], timeout=timeout)
    out = r.stdout.strip()
    if not out:
        return None
    # 第一次 json.loads: 拆掉外层 agent-browser 加的引号
    # 第二次 json.loads: 拆掉 JS 端 JSON.stringify 加的引号
    try:
        outer = json.loads(out)
    except json.JSONDecodeError:
        return out
    if isinstance(outer, str):
        try:
            return json.loads(outer)
        except json.JSONDecodeError:
            return outer
    return outer


def ab_screenshot(path, full=False):
    cmd = ['agent-browser', 'screenshot']
    if full:
        cmd.append('--full')
    cmd.append(str(path))
    return run(cmd, timeout=60)


def ensure_cookies_loaded():
    """确保 agent-browser 里有 cookies"""
    if not COOKIE_FILE.exists():
        err(f"cookie 文件不存在: {COOKIE_FILE}")
        print("  跑: xhs-keepalive.py inject")
        sys.exit(1)
    # 检查当前 cookies
    r = run(['agent-browser', 'cookies', 'get'], timeout=10)
    if not r.stdout.strip() or 'web_session' not in r.stdout:
        print("Loading cookies into agent-browser...")
        subprocess.run(
            ['python3', str(Path(__file__).parent / 'xhs-keepalive.py'), 'load'],
            timeout=30
        )


_AUTHOR_SUFFIX_RE = re.compile(
    r'(\d+\s*(秒|分钟|小时|天|周|月)前|\d{1,2}-\d{1,2}|\d{1,2}月\d{1,2}日|昨天|今天|编辑于.*|分钟前来|小时前来)$'
)


def strip_author_suffix(author: str) -> str:
    """清理 author 字段尾部的"2天前/05-31/昨天"等时间后缀,只留昵称

    例: "影视飓风2天前" → "影视飓风"
        "Yonna语歌"     → "Yonna语歌"  (无后缀不变)
        "改名了1天前"   → "改名了"
    """
    if not author:
        return ''
    s = author.strip()
    # 最多剥 2 次后缀(防止奇怪拼接)
    for _ in range(2):
        m = _AUTHOR_SUFFIX_RE.search(s)
        if m and m.start() > 0:
            s = s[:m.start()].strip()
        else:
            break
    return s


def author_matches(query: str, author: str) -> bool:
    """判断 search 命中的 author 是否就是 query 想要的那个用户

    规则(任一命中即可):
      - 完全相等
      - author 以 query 开头
      - query 以 author 开头(允许 query 比 author 更长)
    """
    a = strip_author_suffix(author)
    q = (query or '').strip()
    if not a or not q:
        return False
    return a == q or a.startswith(q) or q.startswith(a)


def parse_xhs_id(s):
    """从 URL 或纯 ID 解析 xhs note_id / user_id"""
    s = s.strip()
    if '/' in s:
        # URL 模式
        m = re.search(r'/explore/([a-f0-9]+)', s)
        if m:
            return m.group(1)
        m = re.search(r'/user/profile/([a-f0-9]+)', s)
        if m:
            return m.group(1)
        m = re.search(r'/discovery/item/([a-f0-9]+)', s)
        if m:
            return m.group(1)
        return None
    return s


def cmd_search(args):
    """主题搜索: agent-browser 打开 search_result 页面 + 抓 section.note-item"""
    keyword = args.keyword
    out_path = Path(args.out) if args.out else None
    limit = args.limit
    sort = args.sort  # general | hot | time

    ensure_cookies_loaded()

    # 构造 URL
    url = f"{WEB_BASE}/search_result?keyword={keyword}&source=web_explore_feed&type=51"
    if sort == 'hot':
        url += "&sort=hot"
    elif sort == 'time':
        url += "&sort=time_descending"

    print(f"Opening: {url}")
    r = ab_open(url)
    print(r.stdout.strip())

    block = check_block(r.stdout)
    if block == '300012_ip_risk':
        err("IP 被风控 (300012) — 网络层问题,不是 cookie 问题")
        return 2
    if block:
        err(f"页面被风控 ({block})")
        return 1

    # 等加载
    time.sleep(3)

    # 抓 note 列表 (含 note_id + xsec_token,方便后续 note --via-search 用)
    js = rf"""
    (() => {{
      const notes = document.querySelectorAll('section.note-item');
      const data = [];
      const seen = new Set();
      for (let i = 0; i < notes.length && data.length < {limit}; i++) {{
        const n = notes[i];
        // 取带 xsec_token 的链接 (SPA 路由,后续可以靠它绕开 300031)
        const tokenLink = n.querySelector('a[href*="xsec_token"]')?.href || '';
        const anyLink   = n.querySelector('a')?.href || '';
        const href = tokenLink || anyLink;
        let noteId = null, xsecToken = null;
        let m = href.match(/\/search_result\/([a-f0-9]+)\?xsec_token=([^&]+)/);
        if (m) {{ noteId = m[1]; xsecToken = m[2]; }}
        else  {{ m = href.match(/explore\/([a-f0-9]+)/); if (m) noteId = m[1]; }}
        if (!noteId || seen.has(noteId)) continue;
        seen.add(noteId);
        const title  = n.querySelector('.title, .footer-title, a.title span')?.textContent.trim() || '';
        const author = n.querySelector('.author, .nickname, .user-name')?.textContent.trim() || '';
        const likes  = n.querySelector('.like-wrapper .count, .interaction-info .count')?.textContent.trim() || '';
        const date   = n.querySelector('.date, .footer .date, .time')?.textContent.trim() || '';
        if (title) data.push({{note_id: noteId, xsec_token: xsecToken, title, author, likes, date, link: href}});
      }}
      return JSON.stringify({{
        keyword: {json.dumps(keyword)},
        count: data.length,
        notes: data
      }});
    }})()
    """
    raw = ab_eval(js, timeout=20)
    if not raw or isinstance(raw, str):
        err(f"eval 失败,可能页面没加载完成: {str(raw)[:200]}")
        return 1
    result = raw

    # 落盘
    if out_path:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, 'w') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        ok(f"已保存 {result['count']} 条到 {out_path}")
    else:
        # 打印紧凑视图
        print(f"\n关键词: {result['keyword']} (共 {result['count']} 条)\n")
        for i, n in enumerate(result['notes'][:20], 1):
            tok = f" token={n['xsec_token'][:24]}…" if n.get('xsec_token') else " (no token)"
            print(f"{i:3d}. [{n.get('likes', '0'):>6}] {n.get('title', '')}")
            print(f"     {n.get('author', '')}  ·  id={n.get('note_id','-')[:18]}{tok}")
        if result['count'] > 20:
            print(f"\n  ... 还有 {result['count'] - 20} 条,用 --out 落盘查看全部")
        print(f"\n💡 拿 id+token 直接抓详情: xhs-fetch.py note <id> --via-search --token <token> --comments 12")

    return 0


def cmd_note(args):
    """单笔记详情: 进 explore 页面 + 抓 note 标题/正文/评论

    三种模式:
      默认  — 走 /explore/{id} 直链 (通常 300031 不可见)
      --via-search — ⚠️ DEPRECATED,仅适用于 search 桶的 token
                    走 /search_result/{id}?xsec_token=...&xsec_source=pc_note
                    注意: search 桶与 user_profile 桶是不同 captcha,search 桶锁了会 300017
      --via-user-profile — ⭐ 推荐: 主页 token 必须走这个
                    走 /user/profile/{uid}/{nid}?xsec_token=...&xsec_source=pc_user
                    user_id 从 --user-id 传
                    走这个能完全绕开 search 桶 captcha
    """
    note_id = parse_xhs_id(args.note_id)
    if not note_id:
        err(f"无法解析 ID: {args.note_id}")
        return 1

    ensure_cookies_loaded()

    # 选 URL
    if args.via_user_profile:
        if not args.token or not args.user_id:
            err("--via-user-profile 需要 --token <XSEC_TOKEN> 和 --user-id <USER_ID>")
            print("  提示: 从 xhs-fetch.py user <user_id> 拿主页,那里有 xsec_token + xsec_source")
            return 1
        # xsec_source 必须为 pc_user (主页里的 token 都是这个)
        url = f"{WEB_BASE}/user/profile/{args.user_id}/{note_id}?xsec_token={args.token}&xsec_source=pc_user"
        print(f"Opening (via-user-profile): {url}")
    elif args.via_search:
        if not args.token:
            err("--via-search 需要 --token <XSEC_TOKEN>")
            print("  提示: 先跑 `xhs-fetch.py search <keyword>` 拿 note 的 xsec_token")
            return 1
        # search_result 路径默认 xsec_source=pc_note
        xsrc = args.xsec_source or 'pc_note'
        url = f"{WEB_BASE}/search_result/{note_id}?xsec_token={args.token}&xsec_source={xsrc}"
        print(f"Opening (via-search): {url}")
    else:
        url = f"{WEB_BASE}/explore/{note_id}"
        print(f"Opening: {url}")

    r = ab_open(url)
    print(r.stdout.strip())

    block = check_block(r.stdout)
    if block == '300012_ip_risk':
        err("IP 被风控")
        return 2
    if block == '300031_note_blocked':
        err(f"该笔记无法浏览 (300031)")
        if not args.via_search:
            print()
            print("💡 试试用 search 拿 xsec_token 后绕开:")
            print(f"   xhs-fetch.py search <keyword> --limit 30")
            print(f"   # 找一条 title 匹配 {note_id} 的,从输出里拿 xsec_token")
            print(f"   xhs-fetch.py note {note_id} --via-search --token <TOKEN> --comments 12")
        return 1
    if block:
        err(f"页面被风控 ({block})")
        return 1

    time.sleep(3)

    js = f"""
    (() => {{
      const txt = (el) => el ? el.textContent.trim().replace(/\\s+/g, ' ') : '';
      const title = txt(document.querySelector('.note-content .title, #detail-title, .title, h1'));
      const author = txt(document.querySelector('.author-wrapper .username, .info .username, .user-name'));
      const date = txt(document.querySelector('.date, .bottom-container .date, .publish-date'));
      const desc = txt(document.querySelector('.note-content .desc, #detail-desc, .desc, .content'));
      const likes = txt(document.querySelector('.like-wrapper .count, .interaction-info .like .count, .like .count'));
      const collects = txt(document.querySelector('.collect-wrapper .count, .collected .count, .collect .count'));
      const commentsCount = txt(document.querySelector('.chat-wrapper .count, .comment .count, .comment-count'));
      const list = document.querySelectorAll('.comments-container .comment-item, [class*="comment-item"]');
      const comments = Array.from(list).slice(0, {args.comments}).map(c => {{
        const name = txt(c.querySelector('.author .name, .user-name, .username')) || '?';
        const t = txt(c.querySelector('.content, .comment-content, .text, .commentText'));
        const time = txt(c.querySelector('.date, .info .date, .time'));
        const lk = txt(c.querySelector('.like .count, .interaction .like')) || '0';
        return {{name, time, likes: lk, text: t}};
      }});
      return JSON.stringify({{
        note_id: {json.dumps(note_id)},
        title, author, date, desc: desc.slice(0, 3000),
        likes, collects, comments_count: commentsCount, comments
      }});
    }})()
    """
    parsed = ab_eval(js, timeout=20)
    if not parsed:
        err("eval 失败,可能页面没加载完")
        return 1
    if isinstance(parsed, str):
        try:
            result = json.loads(parsed)
        except json.JSONDecodeError:
            err(f"无法解析: {parsed[:200]}")
            return 1
    else:
        result = parsed
    result['via'] = 'search_result' if args.via_search else 'explore'
    result['url'] = url

    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, 'w') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        ok(f"已保存到 {out}")
    else:
        print(f"\n标题: {result['title']}")
        print(f"作者: {result['author']}  |  {result.get('date','')}  |  ❤️ {result['likes']}  |  ⭐ {result['collects']}  |  💬 {result.get('comments_count','?')}")
        print(f"\n正文:\n{result['desc'][:600]}")
        if result.get('comments'):
            print(f"\n前 {len(result['comments'])} 条评论:")
            for i, c in enumerate(result['comments'], 1):
                t = (c.get('text') or '').strip()
                if not t: continue
                print(f"  [{i}] {c.get('name','?')}  ❤️{c.get('likes','0')}: {t[:120]}")

    return 0


def cmd_user_search(args):
    """用户名 → user_id 解析。

    流程:
      1. 搜该用户名的笔记,取 top 8 (带 xsec_token)
      1.5. 验证 Top 笔记的 author 跟关键词匹配 (避免抓错用户)
            - 不匹配 → 扫描 Top 2-8 找匹配的
            - Top 8 全不匹配 → 报清晰错误,建议加"官方/本人"后缀或换拼音
      2. 打开该笔记(走 /search_result 旁路避免 300031)
      3. eval DOM 找 author 主页链接(过滤掉评论者/侧边栏/当前登录用户)

    适用场景:用户给的是显示名"小Lin说"这种,而不是 32 位 hex user_id。

    ⚠️ 限制:本命令依赖 search 桶(IP captcha 绑定),search 桶被锁时不可用。
       此时应该直接传 user_id: xhs-harvest.py user <user_id> --limit 15
    """
    ensure_cookies_loaded()
    keyword = args.keyword

    # Stage 1: 搜索 top 1
    print(f"🔍 搜索: {keyword}")
    search_url = f"{WEB_BASE}/search_result?keyword={quote(keyword)}&source=web_explore_feed&type=51"
    r = ab_open(search_url)
    if check_block(r.stdout):
        err("搜索页被风控(300012) — 等几分钟再试,或换网络")
        return 2
    time.sleep(2)

    js_search = """
    (() => {
      const items = Array.from(document.querySelectorAll('section.note-item'));
      const out = items.slice(0, 5).map(s => {
        const a = s.querySelector('a[href*="/search_result/"]');
        if (!a) return null;
        const m = a.href.match(/\\/search_result\\/([a-f0-9]+)\\?xsec_token=([^&]+)/);
        if (!m) return null;
        return {
          note_id: m[1],
          xsec_token: m[2],
          title: s.querySelector('.title, .footer-title')?.textContent.trim() || '',
          author: s.querySelector('.author, .user-name, [class*="author"]')?.textContent.trim() || '',
          link: a.href
        };
      }).filter(Boolean);
      return JSON.stringify(out);
    })()
    """
    raw = ab_eval(js_search, timeout=15)
    if not raw or not isinstance(raw, list) or not raw:
        err(f"未找到匹配 '{keyword}' 的笔记(搜索无结果或 SPA 未渲染)")
        err(f"  可能原因:")
        err(f"    · search 桶被 captcha 锁 (多并发触发后需等 5-10 min)")
        err(f"    · 关键词拼写不准")
        err(f"  绕开方法: 直接传 user_id (走 user/profile 桶,不依赖 search)")
        err(f"    1. 浏览器登录 xhs → 点进该用户主页 → URL 末尾 32 位 hex = user_id")
        err(f"    2. xhs-harvest.py user <user_id> --limit 15 --comments 15")
        return 1

    # Stage 1.5: 验证 Top 笔记的 author 真的就是搜索词想找的那个用户
    # (历史教训:搜"影视飓风" → Top1 是 @GOODLUCK 写的"达拉斯偶遇影视飓风",作者完全不匹配)
    top = None
    for i, cand in enumerate(raw[:8]):
        clean_a = strip_author_suffix(cand.get('author',''))
        clean_a = clean_a.split()[0] if clean_a else ''  # 有些 author 是 "name 城市" 拼接
        if author_matches(keyword, cand.get('author','')):
            top = cand
            if i > 0:
                print(f"  ⚠️  Top1 不匹配({cand.get('author','')}),改用 Top{i+1}: {top['author']}")
            break
    if top is None:
        # 完全没匹配 → 报清晰错误,引导用户换关键词
        seen_authors = [f"{strip_author_suffix(c.get('author',''))}  (《{c.get('title','')[:30]}》)" for c in raw[:8]]
        err(f"搜索 Top {len(raw[:8])} 笔记中无 author 匹配 '{keyword}' 的作者")
        err(f"  Top {len(raw[:8])} 作者:")
        for s in seen_authors:
            err(f"    - {s}")
        err(f"  → 关键词不够精确,试试:")
        err(f"     · 加后缀: {keyword}官方 / {keyword}本人 / {keyword}本人 / {keyword}ID")
        err(f"     · 用准确的英文 id / 拼音(影视飓风 → yingshijufeng)")
        err(f"     · 如果是搜具体内容,应该用 xhs-fetch.py search 而不是 user-search")
        return 1
    print(f"  top 笔记: 《{top['title'][:40]}》  作者: {top['author']}")

    # Stage 2: 打开该笔记(走 xsec_token 旁路)
    time.sleep(3)  # eval→open 间隔,防 300012
    print(f"📖 打开笔记,定位 author 主页链接 ...")
    note_url = f"{WEB_BASE}/search_result/{top['note_id']}?xsec_token={quote(top['xsec_token'])}&xsec_source="
    r = ab_open(note_url)
    block = check_block(r.stdout)
    if block == '300012_ip_risk':
        err("笔记页被风控(300012) — 等几分钟再试")
        return 2
    if block:
        err(f"笔记页加载失败 ({block})")
        return 1
    time.sleep(3)

    # Stage 3: DOM 找 author user_id
    # 排除:
    #   - xsec_source=pc_comment → 评论者
    #   - grandClass 含 side-bar → 侧边栏(可能是当前登录用户)
    #   - 自己的 user_id(从 cookie 读)
    js_author = """
    (() => {
      const MY_ID = (document.cookie.match(/(?:^|; )x-user-id-redlive\\.xiaohongshu\\.com=([^;]+)/) || [])[1] || '';
      const all = Array.from(document.querySelectorAll('a[href*="/user/profile/"]'));
      const candidates = all.map(a => {
        let el = a, classes = [];
        for (let i = 0; i < 8 && el; i++) {
          if (el.className && typeof el.className === 'string') classes.push(el.className);
          el = el.parentElement;
        }
        return { href: a.href, classes: classes.slice(0, 3) };
      }).filter(c => {
        if (c.href.includes('pc_comment')) return false;
        if (c.href.includes('side-bar')) return false;
        if (MY_ID && c.href.includes(MY_ID)) return false;
        return true;
      });
      const uniq = [];
      const seen = new Set();
      for (const c of candidates) {
        const m = c.href.match(/\\/user\\/profile\\/([a-f0-9]+)/);
        if (m && !seen.has(m[1])) {
          seen.add(m[1]);
          uniq.push({ user_id: m[1], href: c.href, classes: c.classes });
        }
      }
      return JSON.stringify(uniq);
    })()
    """
    raw = ab_eval(js_author, timeout=15)
    if not raw or not isinstance(raw, list) or not raw:
        err("未找到 author user_id(SPA 还没渲染完?重试一次)")
        return 1

    user_id = raw[0]['user_id']
    print(f"  候选 user_id: {user_id}")

    # (v1.2.0 后: --verify flag 已完全删除,Stage 1.5 已自动验证 author 匹配)

    result = {
        "keyword": keyword,
        "user_id": user_id,
        "via_note": {"note_id": top["note_id"], "title": top["title"], "author": top["author"]},
        "candidates": raw,
    }
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, 'w') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        ok(f"已保存到 {out}")
    else:
        print()
        print(f"👉 user_id = {user_id}")
        if name:
            print(f"   name    = {name}")
        print(f"   用法: xhs-harvest.py user {user_id} --notes 50 --limit 20")
    return 0


def cmd_user(args):
    """用户主页: 拿用户基本信息 + 作品列表"""
    user_id = parse_xhs_id(args.user_id)
    if not user_id:
        err(f"无法解析 ID: {args.user_id}")
        return 1

    ensure_cookies_loaded()

    url = f"{WEB_BASE}/user/profile/{user_id}"
    print(f"Opening: {url}")
    r = ab_open(url)
    print(r.stdout.strip())

    # 滑块验证检测(xhs 对 user/profile/... 路径有独立 captcha,不是 300012)
    if 'Security Verification' in r.stdout or 'website-login/captcha' in r.stdout:
        err("触发滑块验证(verifyType=124) — user/profile 路径有独立 captcha")
        err("  解决:等 30+ 分钟 OR 浏览器人工过滑块 + 重导 cookies")
        return 3

    block = check_block(r.stdout)
    if block == '300012_ip_risk':
        err("IP 被风控")
        return 2
    if block:
        err(f"页面被风控 ({block})")
        return 1

    # 额外检测 user-page 内部错误
    time.sleep(2)
    page_err = ab_eval("document.querySelector('.user-page .error .message')?.textContent.trim() || ''", timeout=10)
    if page_err:
        err(f"用户页面加载失败: {page_err}")
        return 1

    time.sleep(3)

    js = f"""
    (() => {{
      const name = document.querySelector('.user-info .username, .user-name, h1')?.textContent.trim() || '';
      const bio = document.querySelector('.user-desc, .desc, .bio')?.textContent.trim() || '';
      const followers = document.querySelector('.fans .count, .follower-count')?.textContent.trim() || '';
      const notes = Array.from(document.querySelectorAll('section.note-item')).slice(0, {args.notes}).map(n => {{
        const title = n.querySelector('.title, .footer-title')?.textContent.trim() || '';
        const likes = n.querySelector('.like-wrapper .count')?.textContent.trim() || '';
        // 关键:从 note-item 内的 <a> 抓 xsec_token
        // 主页的 note-item 里有 2 种带 xsec_token 的链接:
        //   1. /user/profile/{{uid}}/{{nid}}?xsec_token=...&xsec_source=pc_user  (推荐,token 最稳定)
        //   2. /search_result/{{nid}}?xsec_token=...&xsec_source=pc_user        (有些模板会用)
        // 第一个匹配为准,这样后续 harvest.py 直接用 token 走 --via-search
        const linkWithToken = n.querySelector('a[href*="xsec_token="]')?.href || '';
        const linkAny = n.querySelector('a')?.href || '';
        const link = linkWithToken || linkAny;
        const tm = link.match(/[?&]xsec_token=([^&]+)/);
        const xsec_token = tm ? tm[1] : null;
        // 提取 note_id (从 /user/profile/.../<nid> 或 /search_result/<nid> 或 /explore/<nid>)
        const im = link.match(/\\/user\\/profile\\/[a-f0-9]+\\/([a-f0-9]+)/)
                || link.match(/\\/(?:explore|search_result)\\/([a-f0-9]+)/);
        const note_id = im ? im[1] : null;
        return {{ title, likes, link, note_id, xsec_token }};
      }});
      return JSON.stringify({{user_id: {json.dumps(user_id)}, name, bio, followers, notes}});
    }})()
    """
    raw = ab_eval(js, timeout=20)
    if not raw or isinstance(raw, str):
        err(f"eval 失败: {str(raw)[:200]}")
        return 1
    result = raw

    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, 'w') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        ok(f"已保存到 {out}")
    else:
        print(f"\n用户: {result['name']}")
        print(f"ID: {result['user_id']}")
        print(f"粉丝: {result['followers']}")
        print(f"简介: {result['bio'][:200]}")
        if result['notes']:
            print(f"\n最近 {len(result['notes'])} 个作品:")
            for n in result['notes']:
                print(f"  [{n['likes']:>6}] {n['title']}")
    return 0


def cmd_paths(args):
    report_paths()
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="小红书抓取 (搜索/笔记/用户)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
子命令:
  search      <keyword>      主题搜索 (默认按热度)
  note        <note_id>      单笔记详情 (推荐 --via-user-profile 绕开 300031)
  user-search <name>         用户名 → user_id (先解析再喂给 user/harvest)
  user        <user_id>      用户主页 + 作品列表
  paths                      打印路径配置

xsec_token 旁路 (300031 绕开):
  当 explore 链接被风控时 (300031 笔记不可见):
    ⭐ 推荐: xhs-fetch.py note <note_id> --via-user-profile --user-id <uid> --token <TOKEN>
       (主页 token 配 xsec_source=pc_user,走 user/profile 桶,完全绕开 search 桶 captcha)
    备选: xhs-fetch.py note <note_id> --via-search --token <TOKEN>
       (search token 配 xsec_source=pc_note,走 search_result 桶)
        """
    )
    sub = parser.add_subparsers(dest='cmd', required=True)

    # search
    p = sub.add_parser('search', help='主题搜索')
    p.add_argument('keyword', help='搜索关键词')
    p.add_argument('--limit', type=int, default=50, help='最多拿几条 (默认 50)')
    p.add_argument('--sort', choices=['general', 'hot', 'time'], default='general',
                   help='排序: general(综合) / hot(最热) / time(最新) (默认 general)')
    p.add_argument('--out', help='落盘到 JSON 文件 (默认打到 stdout)')

    # note
    p = sub.add_parser('note', help='单笔记详情 (支持 via-search / via-user-profile 绕开 300031)')
    p.add_argument('note_id', help='note_id 或 explore URL')
    p.add_argument('--comments', type=int, default=10, help='评论数 (默认 10)')
    p.add_argument('--out', help='落盘 JSON')
    p.add_argument('--via-search', action='store_true',
                   help='走 /search_result/{id}?xsec_token=...&xsec_source=pc_note 路径 (需要 --token)')
    p.add_argument('--via-user-profile', action='store_true',
                   help='走 /user/profile/{uid}/{nid}?xsec_token=...&xsec_source=pc_user 路径 (推荐,需要 --token + --user-id)')
    p.add_argument('--token', help='xsec_token (配合 --via-search / --via-user-profile 使用)')
    p.add_argument('--user-id', help='user_id (配合 --via-user-profile 使用)')
    p.add_argument('--xsec-source', help='覆盖默认 xsec_source (默认 search: pc_note, user_profile: pc_user)')

    # user-search (用户名 → user_id 解析)
    p = sub.add_parser('user-search', help='用户名 → user_id (搜→note DOM→user_profile 链接)')
    p.add_argument('keyword', help='用户显示名(中文/英文均可)')
    p.add_argument('--out', help='落盘 JSON')

    # user
    p = sub.add_parser('user', help='用户主页')
    p.add_argument('user_id', help='user_id 或 profile URL')
    p.add_argument('--notes', type=int, default=20, help='拿几个作品 (默认 20)')
    p.add_argument('--out', help='落盘 JSON')

    # paths
    sub.add_parser('paths', help='打印路径配置')

    args = parser.parse_args()
    fn = globals().get(f"cmd_{args.cmd.replace('-', '_')}")
    if not fn:
        err(f"未知子命令: {args.cmd}")
        return 1
    return fn(args) or 0


if __name__ == '__main__':
    sys.exit(main())
