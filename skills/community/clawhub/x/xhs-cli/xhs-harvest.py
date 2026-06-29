#!/usr/bin/env python3
"""
xhs-harvest.py — 小红书"主题收割"工作流 (编排)

子命令:
  hot      <keyword>              收割一个主题的热门笔记
  user     <user_id|url>          收割某个用户的所有作品 (推荐)
  ids      <id1,id2,...>          收割指定的 note_id 列表
  paths                            打印路径配置

优先路径(不依赖 search 桶,不受 search captcha 影响):
  1. user 子命令 → user/profile 主页拿 xsec_token → 走 via-user-profile 拿详情
  2. ids 子命令 + 传 user_id → 同上

需要 search 桶的路径(search 桶被锁时会失败):
  - hot 子命令(必须 search 拿候选)
  - user-search(从显示名解析 user_id)
  - auto-resolve-tokens(兑底拿 token)
  - --via-search 抓详情 (只适用于 search 来源的 token)

captcha 分桶处理:search 桶 / user_profile 桶 独立计数。走 user/profile 路径可绕开 search captcha。

工作流 (user 子命令,推荐):
  1. xhs-fetch.py user-search "影视飓风" → user_id (可选,也可用 --from-name 跳这一步)
  2. xhs-fetch.py user <user_id> --notes 50  → user.json (30 篇笔记,带 xsec_token)
  3. 对每条 note, 走 --via-user-profile (token 配 xsec_source=pc_user) 抓详情
  4. 落盘 + 报告

数据路径: $SKILL/data/harvests/<topic>/
增量: 已落盘的 note 跳过 (--force 强制重抓)
限速: --sleep N 秒 (默认 4s, 防 300012 IP 风险)
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

# 路径管理 (复用 fetch 的 paths.py)
from paths import DATA_DIR, HARVESTS_DIR, report as report_paths

# 自动建子目录
HARVESTS_DIR.mkdir(parents=True, exist_ok=True)

# xhs-fetch.py 的绝对路径 (同目录)
FETCH_SCRIPT = Path(__file__).parent / "xhs-fetch.py"
WEB_BASE = "https://www.xiaohongshu.com"


def err(msg):
    print(f"❌ {msg}", file=sys.stderr)


def ok(msg):
    print(f"✅ {msg}")


def run_fetch(args, timeout=60):
    """subprocess 调 xhs-fetch.py, 捕获 stdout (JSON 路径在 ok 行里有)"""
    cmd = ['python3', str(FETCH_SCRIPT)] + args
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def safe_int(s, default=0):
    try:
        return int(str(s).replace(',', '').replace('+', '').replace('万', '0000').replace('赞', '').strip() or default)
    except (ValueError, TypeError):
        return default


def parse_user_note_link(link):
    """从主页 note-item 里的 <a href> 提取 (note_id, xsec_token, link_kind)

    主页 note-item 里有 3 种链接:
      - /user/profile/{uid}/{nid}?xsec_token=...&xsec_source=pc_user  (推荐,token 稳定)
      - /search_result/{nid}?xsec_token=...&xsec_source=pc_user
      - /explore/{nid}                                              (无 token,需要 fallback search)
    """
    if not link:
        return None, None, None
    m = re.search(r'/user/profile/[a-f0-9]+/([a-f0-9]+)\?.*?xsec_token=([^&]+)', link)
    if m:
        return m.group(1), m.group(2), 'user_profile'
    m = re.search(r'/search_result/([a-f0-9]+)\?xsec_token=([^&]+)', link)
    if m:
        return m.group(1), m.group(2), 'search_result'
    m = re.search(r'/explore/([a-f0-9]+)', link)
    if m:
        return m.group(1), None, 'explore'
    return None, None, None


def slugify(s):
    """把 keyword 转成安全的目录名"""
    s = re.sub(r'[^\w\u4e00-\u9fff\-]+', '-', s.strip())
    s = re.sub(r'-+', '-', s).strip('-')
    return s[:60] or 'topic'


# ─────────────────────────────────────────────────────────────
# 核心 fetch: 抓一条 note 详情 (走 via-search 旁路)
# ─────────────────────────────────────────────────────────────

def fetch_one_note(note_id, xsec_token, out_path, comments=10, sleep_after=4, user_id=None, xsec_source=None):
    """抓一条 note; 成功落盘返 True,失败返 False

    路径优先级:
      1. user_id 给定 → 走 /user/profile/{uid}/{nid}?xsec_token=...&xsec_source=pc_user (主页 token 必走这个)
      2. 否则 → 走 /search_result/{nid}?xsec_token=...&xsec_source=pc_note

    captcha 处理:**不重试**,直接报错。连发会加锁,手动重跑更安全。
    """
    if out_path.exists():
        # 已落盘 → 跳过 (增量)
        return True, "已存在 (跳过)"

    if not xsec_token:
        return False, "无 xsec_token,无法走 via-search"

    # 构造 note 命令参数
    note_args = ['note', note_id, '--token', xsec_token, '--comments', str(comments), '--out', str(out_path)]
    if user_id:
        note_args += ['--via-user-profile', '--user-id', user_id]
    else:
        note_args.append('--via-search')
        if xsec_source:
            note_args += ['--xsec-source', xsec_source]

    r = run_fetch(note_args)
    out = r.stdout + r.stderr
    time.sleep(sleep_after)

    if '✅ 已保存到' in r.stdout or out_path.exists():
        return True, "ok"
    if '300012' in out:
        return False, "IP 风控 (300012) — 换网络或等 30+ 分钟"
    if '300031' in out:
        return False, "笔记不可见 (300031) — xsec_token 失效,需要重拿"
    if 'Security Verification' in out or 'verifyType=124' in out:
        return False, "captcha 锁中 (verifyType=124) — 等 5-30 min 或换 IP 后重跑 (不自动重试避免加锁)"
    return False, f"未知失败: {out[:150]}"


# ─────────────────────────────────────────────────────────────
# subcommand: hot — 抓一个主题的热门笔记
# ─────────────────────────────────────────────────────────────

def cmd_hot(args):
    """
    用 search 拿一批 note_id+xsec_token, 逐个抓详情落盘, 生成报告
    支持多关键词 (--keywords k1,k2,k3)
    """
    keywords = [args.keyword]
    if args.keywords:
        keywords.extend([k.strip() for k in args.keywords.split(',') if k.strip()])
    keywords = list(dict.fromkeys(keywords))   # 去重保持顺序

    # 准备输出目录
    if args.out:
        out_dir = Path(args.out)
    else:
        # 默认: $SKILL/data/harvests/<slug>-<timestamp>/
        ts = time.strftime('%Y%m%d-%H%M%S')
        out_dir = HARVESTS_DIR / f"{slugify('-'.join(keywords))}-{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)
    notes_dir = out_dir / 'notes'
    notes_dir.mkdir(exist_ok=True)
    print(f"📁 输出目录: {out_dir}")
    print(f"🔑 关键词: {keywords}")
    print(f"📊 每个关键词拿 top {args.per_keyword} 条, 每条 {args.comments} 条评论, sleep {args.sleep}s")
    print()

    # Phase 1: 多关键词搜索, 收集 (note_id, xsec_token, keyword, likes)
    all_candidates = []
    seen = set()
    for kw in keywords:
        print(f"━━ Phase 1: search '{kw}' (sort={args.sort}, limit={args.per_keyword}) ━━")
        search_json = out_dir / f"search-{slugify(kw)}.json"
        r = run_fetch(['search', kw, '--sort', args.sort,
                       '--limit', str(args.per_keyword), '--out', str(search_json)])
        if r.returncode != 0 or not search_json.exists():
            err(f"search '{kw}' 失败: {r.stderr[:200] or r.stdout[:200]}")
            continue
        d = json.load(open(search_json))
        added = 0
        for n in d.get('notes', []):
            nid = n.get('note_id')
            if not nid or nid in seen:
                continue
            seen.add(nid)
            all_candidates.append({
                'note_id': nid,
                'xsec_token': n.get('xsec_token'),
                'title': n.get('title', ''),
                'author': n.get('author', ''),
                'likes_raw': n.get('likes', '0'),
                'likes': safe_int(n.get('likes')),
                'date': n.get('date', ''),
                'keyword': kw,
            })
            added += 1
        ok(f"  '{kw}': {added} 条新候选 (累计 {len(all_candidates)})")
        time.sleep(args.sleep)

    if not all_candidates:
        err("没有候选笔记 (可能被风控或关键词无结果)")
        return 1

    # 按点赞排序
    all_candidates.sort(key=lambda x: x['likes'], reverse=True)
    top = all_candidates[:args.limit]
    print(f"\n🎯 排序后取 top {len(top)} (共候选 {len(all_candidates)} 条)")
    for i, c in enumerate(top, 1):
        print(f"   {i:2d}. ❤️{c['likes']:>5}  {c['title'][:40]}  ({c['keyword']})")

    # 保存候选清单
    (out_dir / 'candidates.json').write_text(
        json.dumps(top, ensure_ascii=False, indent=2), encoding='utf-8'
    )

    # Phase 2: 逐个抓详情
    print(f"\n━━ Phase 2: 抓详情 + 评论 ━━")
    print(f"  (每条之间 sleep {args.sleep}s 防 300012)\n")
    results = []
    for i, c in enumerate(top, 1):
        out = notes_dir / f"n{i:02d}-{c['note_id'][:8]}.json"
        print(f"  [{i}/{len(top)}] {c['title'][:38]}  ", end='', flush=True)
        ok_status, msg = fetch_one_note(
            c['note_id'], c.get('xsec_token'), out,
            comments=args.comments, sleep_after=args.sleep
        )
        status_icon = '✅' if ok_status else '❌'
        print(f"{status_icon} {msg}")
        results.append({**c, 'file': out.name if ok_status else None,
                        'fetch_ok': ok_status, 'fetch_msg': msg})
        # 不重试 IP 风控,避免连发加锁

    (out_dir / 'results.json').write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8'
    )

    # Phase 3: 生成报告
    print(f"\n━━ Phase 3: 生成报告 ━━")
    n_ok = sum(1 for r in results if r['fetch_ok'])
    n_comments = 0
    for f in notes_dir.glob('*.json'):
        try:
            n_comments += len(json.load(open(f)).get('comments', []))
        except Exception:
            pass

    report_path = out_dir / 'REPORT.md'
    write_report(report_path, keywords, results, n_ok, n_comments, args)
    ok(f"报告: {report_path}")

    print(f"\n{'='*70}")
    print(f"📊 抓取结果: {n_ok}/{len(results)} 成功 · {n_comments} 条评论")
    print(f"📁 落盘目录: {out_dir}")
    print(f"📄 报告:     {report_path}")
    print('='*70)

    return 0 if n_ok > 0 else 1


def write_report(path, keywords, results, n_ok, n_comments, args):
    """生成人类可读 markdown 报告"""
    lines = []
    lines.append(f"# 小红书「{' / '.join(keywords)}」 收割报告")
    lines.append('')
    lines.append(f"- **关键词**: {', '.join(keywords)}")
    lines.append(f"- **抓取时间**: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"- **排序**: {getattr(args, 'sort', 'n/a')}")
    lines.append(f"- **每关键词 top**: {getattr(args, 'per_keyword', 'n/a')}")
    lines.append(f"- **实际抓取**: {n_ok}/{len(results)} 成功")
    lines.append(f"- **总评论数**: {n_comments}")
    lines.append(f"- **每条评论上限**: {args.comments}")
    lines.append('')
    lines.append('---')
    lines.append('')

    # 表格概览
    lines.append('## 概览 (按点赞排序)')
    lines.append('')
    lines.append('| # | ❤️ | 标题 | 作者 | 时间 | 状态 |')
    lines.append('|---|---:|------|------|------|------|')
    for i, r in enumerate(results, 1):
        title = (r.get('title') or r.get('note_id', '?')[:14])[:40].replace('|', '\\|')
        author = (r.get('author') or '')[:15].replace('|', '\\|')
        date = r.get('date', '') or ''
        likes = r.get('likes', 0) or 0
        if r.get('fetch_ok'):
            status = '✅'
        else:
            status = f"❌ {(r.get('fetch_msg','') or 'failed')[:20]}"
        lines.append(f"| {i} | {likes} | {title} | {author} | {date} | {status} |")
    lines.append('')

    # 详情 (只列成功的)
    ok_results = [r for r in results if r['fetch_ok']]
    notes_dir = path.parent / 'notes'   # 报告在 out_dir/REPORT.md, notes 在 out_dir/notes/
    if ok_results:
        lines.append('---')
        lines.append('')
        lines.append('## 笔记详情')
        lines.append('')
        for i, r in enumerate(ok_results, 1):
            f = notes_dir / r['file'] if r.get('file') else None
            if not f or not f.exists():
                continue
            d = json.load(open(f))
            lines.append(f"### {i}. {d.get('title', r['title'])}")
            lines.append('')
            lines.append(f"- **作者**: {d.get('author', r['author'])}")
            lines.append(f"- **时间**: {d.get('date', r['date'])}")
            lines.append(f"- **点赞**: {d.get('likes','-')}  |  **收藏**: {d.get('collects','-')}  |  **评论**: {d.get('comments_count','-')}")
            lines.append(f"- **note_id**: `{r['note_id']}`")
            lines.append(f"- **数据文件**: `notes/{f.name}`")
            lines.append('')
            desc = (d.get('desc') or '').strip()
            if desc:
                lines.append('**正文**:')
                lines.append('')
                lines.append(f"> {desc[:600]}{'...' if len(desc) > 600 else ''}")
                lines.append('')
            cmts = [c for c in d.get('comments', []) if (c.get('text') or '').strip()]
            if cmts:
                lines.append(f"**热门评论 (前 {min(5, len(cmts))} 条)**:")
                lines.append('')
                for c in cmts[:5]:
                    text = c['text'][:150].replace('\n', ' ')
                    lines.append(f"- **{c.get('name','?')}** ❤️{c.get('likes','0')}: {text}")
                lines.append('')

    lines.append('---')
    lines.append('')
    lines.append('## 文件清单')
    lines.append('')
    lines.append(f"```")
    lines.append(f".")
    lines.append(f"├── REPORT.md            ← 本报告")
    lines.append(f"├── candidates.json      ← 候选清单 (按点赞排序)")
    lines.append(f"├── results.json         ← 抓取结果 (含成功/失败状态)")
    for f in sorted(Path(path).parent.glob('search-*.json')):
        lines.append(f"├── {f.name}      ← 搜索原始结果")
    lines.append(f"└── notes/")
    for i, r in enumerate(results, 1):
        fname = f"n{i:02d}-{r['note_id'][:8]}.json"
        status = "✅" if r['fetch_ok'] else "❌"
        lines.append(f"    ├── {fname}  {status}")
    lines.append(f"```")
    lines.append('')

    path.write_text('\n'.join(lines), encoding='utf-8')


# ─────────────────────────────────────────────────────────────
# subcommand: user — 抓用户的所有作品
# ─────────────────────────────────────────────────────────────

def auto_resolve_tokens(candidates_needing_token, sleep=4, sort='time', token_cache=None):
    """对没有 xsec_token 的候选,自动用 title 搜一下拿 token

    candidates_needing_token: [{note_id, title}, ...]
    返回: {(note_id, title): xsec_token} (拿不到的不会出现在结果里)

    captcha 处理:遇到 captcha 直接报失败,不重试、不冷却、不跳过后续。
    """
    import tempfile
    out_map = {}
    cache = token_cache or {}
    captcha_failed = False
    for i, c in enumerate(candidates_needing_token, 1):
        nid = c['note_id']
        title = c['title']
        if nid in cache:
            out_map[nid] = cache[nid]
            print(f"  [{i}/{len(candidates_needing_token)}] {title[:30]:30s} ✅ cache hit")
            continue
        if captcha_failed:
            # 一次 captcha 就停止,避免连发加锁
            print(f"  [{i}/{len(candidates_needing_token)}] {title[:30]:30s} ❌ 跳过 (search captcha 后已停止)")
            continue
        # 试多个关键词:全标题 > 15 字 > 10 字
        kw_candidates = [title, title[:15], title[:10]]
        seen_kw = set()
        kw_candidates = [k.strip() for k in kw_candidates if k.strip() and not (k.strip() in seen_kw or seen_kw.add(k.strip()))]
        found = None
        for kw in kw_candidates:
            if len(kw) < 4:
                continue
            tmp = Path(tempfile.mkstemp(suffix='.json')[1])
            r = run_fetch(['search', kw, '--sort', sort, '--limit', '10', '--out', str(tmp)])
            out_combined = r.stdout + r.stderr
            if 'Security Verification' in out_combined or 'verifyType=124' in out_combined:
                print(f"  [{i}/{len(candidates_needing_token)}] {title[:30]:30s} ❌ search captcha,停止 auto-token (避免连发加锁)")
                tmp.unlink(missing_ok=True)
                captcha_failed = True
                break
            if r.returncode != 0:
                print(f"  [{i}/{len(candidates_needing_token)}] {title[:30]:30s}  search 失败: {r.stderr[:60]}")
                tmp.unlink(missing_ok=True)
                time.sleep(sleep)
                continue
            try:
                d = json.load(open(tmp))
                notes = d.get('notes', d) if isinstance(d, dict) else d
            except Exception:
                notes = []
            tmp.unlink(missing_ok=True)
            for nd in notes:
                if nd.get('note_id') == nid and nd.get('xsec_token'):
                    found = nd['xsec_token']
                    break
            if found:
                break
            time.sleep(2)
        if found:
            out_map[nid] = found
            cache[nid] = found
            print(f"  [{i}/{len(candidates_needing_token)}] {title[:30]:30s} ✅ auto-search 拿 token")
        elif not captcha_failed:
            print(f"  [{i}/{len(candidates_needing_token)}] {title[:30]:30s} ❌ 搜索不到,放弃")
    return out_map, cache


def cmd_user(args):
    """抓一个用户主页的所有作品 (复用 fetch user, 然后逐个走 via-search 抓详情)

    支持两种入口:
      - 传 user_id (position)              → 传统路径
      - 传 --from-name "显示名"             → 内部调 user-search 解析为 user_id 再走主流程

    token 来源(三选一,按优先级):
      1. 主页 DOM 里 <a href> 自带的 xsec_token (最常见,/user/profile/... 链接里)
      2. --auto-token (默认开) → 自动用 title search 拿 xsec_token (仅 1、2 失败时走)
      3. 全失败 → 该笔记跳过(只在报告里记元数据)
    """
    # 参数互斥检查
    if args.from_name and args.user_id:
        err("--from-name 和 user_id 互斥,只能选一个")
        return 1
    if not args.from_name and not args.user_id:
        err("需要传 user_id (positional) 或 --from-name '显示名'")
        return 1

    # --from-name 路径: 调 user-search 解析 user_id
    user_id = args.user_id
    if args.from_name:
        print(f"🔍 从显示名解析 user_id: {args.from_name}")
        r = run_fetch(['user-search', args.from_name])  # 不传 --verify,避开额外 captcha
        if r.returncode != 0:
            err(f"user-search 失败:\n{r.stdout[:500]}\n{r.stderr[:200]}")
            return 1
        m = re.search(r'user_id = ([a-f0-9]+)', r.stdout)
        if not m:
            err(f"未从 user-search 输出中解析出 user_id:\n{r.stdout[:500]}")
            return 1
        user_id = m.group(1)
        print(f"  → user_id: {user_id}\n")

    if '/' in user_id:
        m = re.search(r'/user/profile/([a-f0-9]+)', user_id)
        if m:
            user_id = m.group(1)
    print(f"👤 user_id: {user_id}")

    out_dir = HARVESTS_DIR / f"user-{user_id[:12]}-{time.strftime('%Y%m%d-%H%M%S')}"
    out_dir.mkdir(parents=True, exist_ok=True)
    notes_dir = out_dir / 'notes'
    notes_dir.mkdir(exist_ok=True)

    # Phase 1: 拿用户主页 + 作品列表 (captcha 不重试,直接报错)
    user_json = out_dir / 'user.json'
    r = run_fetch(['user', user_id, '--notes', str(args.notes), '--out', str(user_json)])
    if not user_json.exists():
        if r.returncode == 3:  # captcha (verifyType=124)
            err("user/profile 路径 captcha 锁中 (verifyType=124) — 等 30+ 分钟或换 IP 后重跑")
        else:
            err(f"拿用户主页失败: {r.stderr[:200] or r.stdout[:200]}")
        return 1
    user_data = json.load(open(user_json))
    n_notes = len(user_data.get('notes', []))
    if n_notes == 0:
        err("用户主页 0 作品(captcha 可能未完全衰减,或用户本身没发笔记)")
        return 1
    ok(f"用户: {user_data.get('name','')} · 粉丝 {user_data.get('followers','?')} · 作品 {n_notes}")
    print()

    # Phase 2: 走 user 列表里的 link → 拿 xsec_token
    #         1) DOM 自带的 token (/user/profile/.../...?... 链接里)
    #         2) --auto-token (默认): 拿到 note_id 但没 token 的,自动 search 补
    candidates = []
    seen = set()
    for n in user_data.get('notes', []):
        link = n.get('link', '')
        nid, tok, kind = parse_user_note_link(link)
        if not nid or nid in seen:
            continue
        seen.add(nid)
        candidates.append({
            'note_id': nid, 'xsec_token': tok,
            'link_kind': kind,
            'title': n.get('title', ''),
            'likes': safe_int(n.get('likes')),
        })
    candidates.sort(key=lambda x: x['likes'], reverse=True)
    top = candidates[:args.limit]

    # Phase 2.5: 那些只有 /explore/ 链接的(没 token),如果 --auto-token 开就自动 search 补
    n_with_token = sum(1 for c in top if c.get('xsec_token'))
    n_need_token = len(top) - n_with_token
    print(f"🎯 抓 top {len(top)} 篇 (按点赞排序)")
    print(f"   {n_with_token} 篇 DOM 自带 token, {n_need_token} 篇需补 token")
    if n_need_token > 0 and not args.auto_token:
        print(f"   ⚠️  --no-auto-token 开了,那 {n_need_token} 篇会被跳过。加 --auto-token (默认开) 启用自动 search。")

    if n_need_token > 0 and args.auto_token:
        # 读缓存 (上次同用户的 token)
        cache_path = out_dir / 'token_cache.json'
        token_cache = {}
        if cache_path.exists():
            try:
                token_cache = json.load(open(cache_path))
            except Exception:
                pass
        needing = [c for c in top if not c.get('xsec_token')]
        print(f"\n🔧 auto-token: 拿 {len(needing)} 篇的 xsec_token (sleep {args.sleep}s/次)...")
        resolved, token_cache = auto_resolve_tokens(
            needing, sleep=args.sleep, sort='time', token_cache=token_cache
        )
        for c in top:
            if not c.get('xsec_token') and c['note_id'] in resolved:
                c['xsec_token'] = resolved[c['note_id']]
        # 写缓存
        try:
            cache_path.write_text(json.dumps(token_cache, ensure_ascii=False, indent=2))
        except Exception:
            pass
        print()

    # Phase 3: 逐个 fetch
    # 走 via-user-profile 路径(user.json 的 token 配 xsec_source=pc_user,不用 search_result)
    results = []
    for i, c in enumerate(top, 1):
        out = notes_dir / f"n{i:02d}-{c['note_id'][:8]}.json"
        print(f"  [{i}/{len(top)}] {c['title'][:38]}  ", end='', flush=True)
        # 只有从 user_profile link 拿的 token 才能走 --via-user-profile
        # search_result link 拿的 token 必须走 search_result 路径
        use_user_path = c.get('link_kind') == 'user_profile'
        ok_s, msg = fetch_one_note(c['note_id'], c.get('xsec_token'), out,
                                   comments=args.comments, sleep_after=args.sleep,
                                   user_id=user_id if use_user_path else None,
                                   xsec_source='pc_note' if not use_user_path else None)
        # 成功后回填标题/作者/日期/点赞,避免 write_report KeyError
        file_ref = out.name if ok_s else None
        title = c['title']
        author = user_data.get('name', '')
        date = ''
        likes = c.get('likes', 0)
        if ok_s and out.exists():
            try:
                d = json.load(open(out))
                title = d.get('title') or title
                author = d.get('author') or author
                date = d.get('date') or ''
            except Exception:
                pass
        print(f"{'✅' if ok_s else '❌'} {msg}")
        results.append({
            'note_id': c['note_id'],
            'xsec_token': c.get('xsec_token'),
            'link_kind': c.get('link_kind'),
            'title': title,
            'author': author,
            'date': date,
            'likes': likes,
            'fetch_ok': ok_s,
            'fetch_msg': msg,
            'file': file_ref,
        })
        # 不重试 IP 风控,避免连发加锁

    n_ok = sum(1 for r in results if r['fetch_ok'])
    n_comments = 0
    for f in notes_dir.glob('*.json'):
        try:
            n_comments += len(json.load(open(f)).get('comments', []))
        except Exception:
            pass
    report_path = out_dir / 'REPORT.md'
    write_report(report_path, [f"@{user_data.get('name', user_id)}"], results, n_ok, n_comments, args)
    ok(f"报告: {report_path}")
    return 0


# ─────────────────────────────────────────────────────────────
# subcommand: ids — 抓指定的 note_id 列表
# ─────────────────────────────────────────────────────────────

def cmd_ids(args):
    """直接抓给定的 note_id 列表 (--tokens 配套给 xsec_token)
    用法:
      xhs-harvest.py ids id1 id2 id3
      xhs-harvest.py ids id1 id2 --tokens "tok1,tok2"
      xhs-harvest.py ids id1 id2 --auto-token          # 没传 token 的,用 note_id 作 search keyword
    """
    ids = args.ids
    tokens = []
    if args.tokens:
        tokens = [t.strip() for t in args.tokens.split(',')]

    out_dir = HARVESTS_DIR / f"ids-{time.strftime('%Y%m%d-%H%M%S')}"
    out_dir.mkdir(parents=True, exist_ok=True)
    notes_dir = out_dir / 'notes'
    notes_dir.mkdir(exist_ok=True)

    # 对齐 tokens 和 ids 长度(缺位的填 None)
    while len(tokens) < len(ids):
        tokens.append(None)

    # auto-token: 为没 token 的跑 search (用 note_id 作 keyword 拿到同笔记在搜索结果里的 xsec_token)
    if args.auto_token:
        need_idx = [i for i, t in enumerate(tokens) if not t]
        if need_idx:
            print(f"🔧 auto-token: 拿 {len(need_idx)} 个 note_id 的 xsec_token (用 note_id 搜)...")
            from urllib.parse import quote
            import tempfile
            for j, i in enumerate(need_idx, 1):
                nid = ids[i]
                tmp = Path(tempfile.mkstemp(suffix='.json')[1])
                r = run_fetch(['search', nid, '--sort', 'time', '--limit', '10', '--out', str(tmp)])
                if r.returncode != 0:
                    print(f"  [{j}/{len(need_idx)}] {nid[:14]} ❌ search fail")
                    tmp.unlink(missing_ok=True)
                    time.sleep(args.sleep)
                    continue
                try:
                    d = json.load(open(tmp))
                    notes = d.get('notes', d) if isinstance(d, dict) else d
                except Exception:
                    notes = []
                tmp.unlink(missing_ok=True)
                found = None
                for nd in notes:
                    if nd.get('note_id') == nid and nd.get('xsec_token'):
                        found = nd['xsec_token']
                        break
                if found:
                    tokens[i] = found
                    print(f"  [{j}/{len(need_idx)}] {nid[:14]} ✅")
                else:
                    print(f"  [{j}/{len(need_idx)}] {nid[:14]} ❌ 搜索无匹配")
                time.sleep(args.sleep)

    results = []
    for i, nid in enumerate(ids, 1):
        tok = tokens[i-1]
        out = notes_dir / f"n{i:02d}-{nid[:8]}.json"
        print(f"  [{i}/{len(ids)}] {nid}  ", end='', flush=True)
        ok_s, msg = fetch_one_note(nid, tok, out, comments=args.comments, sleep_after=args.sleep)
        print(f"{'✅' if ok_s else '❌'} {msg}")
        # 成功后回填 title/author/date/likes
        title = nid[:14]
        author = ''
        date = ''
        likes = 0
        if ok_s and out.exists():
            try:
                d = json.load(open(out))
                title = d.get('title') or title
                author = d.get('author') or ''
                date = d.get('date') or ''
                likes = safe_int(d.get('likes'))
            except Exception:
                pass
        results.append({
            'note_id': nid, 'xsec_token': tok,
            'title': title, 'author': author, 'date': date, 'likes': likes,
            'fetch_ok': ok_s, 'fetch_msg': msg,
            'file': out.name if ok_s else None,
        })
    n_ok = sum(1 for r in results if r['fetch_ok'])
    n_comments = 0
    for f in notes_dir.glob('*.json'):
        try:
            n_comments += len(json.load(open(f)).get('comments', []))
        except Exception:
            pass
    report_path = out_dir / 'REPORT.md'
    write_report(report_path, ['指定 IDs'], results, n_ok, n_comments, args)
    ok(f"报告: {report_path}")
    return 0


def cmd_paths(args):
    report_paths()
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="小红书收割 — 一次命令完成 '搜 → 抓详情+评论 → 落盘 → 报告'",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
3 个使用模式:

1) 主题收割 (最常用):
   xhs-harvest.py hot "AI"
   xhs-harvest.py hot "AI" --sort hot --limit 20 --comments 15
   xhs-harvest.py hot "Claude" --keywords "Anthropic,Cursor,vibe coding" --limit 30

2) 用户收割 (一条命令拿到用户全部视频数据 + 评论):
   xhs-harvest.py user --from-name "影视飓风" --notes 50 --limit 20 --comments 15
   xhs-harvest.py user 5c6391880000000012009893 --notes 50 --limit 20 --comments 15
   # 内部流程: user-search 解析 id → 主页拿笔记列表 → DOM 自带 xsec_token
   #          → 缺的 auto-token search 补 → ids + tokens 批量抓 → 报告

3) 指定 ID 收割 (你已经知道 id+token):
   xhs-harvest.py ids id1 id2 id3 --tokens "tok1,tok2,tok3"
   xhs-harvest.py ids id1 id2 --auto-token     # 没 token 的自动 search 拿

数据落盘: $SKILL/data/harvests/<topic>-<时间戳>/
  ├── REPORT.md          ← 人类可读报告
  ├── candidates.json    ← 候选清单 (按点赞排序)
  ├── results.json       ← 抓取状态 (含失败原因)
  ├── user.json         ← (仅 user 子命令) 主页笔记列表 + xsec_token
  ├── token_cache.json  ← (仅 user 子命令) xsec_token 缓存,重跑节省请求
  ├── search-*.json      ← 各关键词的原始搜索结果
  └── notes/
      ├── n01-*.json     ← 笔记详情 + 评论
      └── ...
        """
    )
    sub = parser.add_subparsers(dest='cmd', required=True)

    # hot
    p = sub.add_parser('hot', help='收割一个主题的热门笔记 (search + 详情+评论 + 报告)')
    p.add_argument('keyword', help='主关键词')
    p.add_argument('--keywords', help='附加关键词 (逗号分隔), 合并去重')
    p.add_argument('--sort', choices=['general', 'hot', 'time'], default='hot',
                   help='搜索排序 (默认 hot, 适合热点采集)')
    p.add_argument('--per-keyword', type=int, default=15,
                   help='每个关键词搜几条 (默认 15)')
    p.add_argument('--limit', type=int, default=10,
                   help='最终抓多少条 (按点赞排序后取 top, 默认 10)')
    p.add_argument('--comments', type=int, default=10, help='每条笔记抓多少评论 (默认 10)')
    p.add_argument('--sleep', type=int, default=4, help='请求间隔秒数 (默认 4, 防 300012)')
    p.add_argument('--out', help='输出目录 (默认 $SKILL/data/harvests/<topic>-<ts>/)')

    # user
    p = sub.add_parser('user', help='收割某用户的所有作品 (支持 --from-name 从显示名开始)')
    p.add_argument('user_id', nargs='?', default=None, help='user_id 或 profile URL (与 --from-name 互斥)')
    p.add_argument('--from-name', help='用户显示名(中文/英文),自动调 user-search 解析为 user_id')
    p.add_argument('--notes', type=int, default=30, help='用户主页拿几条 (默认 30)')
    p.add_argument('--limit', type=int, default=10, help='最终抓多少条 (按点赞排序)')
    p.add_argument('--comments', type=int, default=10, help='每条笔记抓多少评论')
    p.add_argument('--sleep', type=int, default=4, help='请求间隔秒数')
    p.add_argument('--auto-token', dest='auto_token', action='store_true', default=True,
                   help='主页 link 没 xsec_token 时,自动用 title search 拿 (默认开)')
    p.add_argument('--no-auto-token', dest='auto_token', action='store_false',
                   help='禁用 auto-token 兑底(那些拿不到 token 的会跳过)')

    # ids
    p = sub.add_parser('ids', help='收割指定 note_id 列表 (nargs=*)')
    p.add_argument('ids', nargs='+', help='note_id 列表')
    p.add_argument('--tokens', help='配套 xsec_token (逗号分隔,顺序对应 ids)')
    p.add_argument('--comments', type=int, default=10, help='每条笔记抓多少评论')
    p.add_argument('--sleep', type=int, default=4, help='请求间隔秒数')
    p.add_argument('--auto-token', dest='auto_token', action='store_true', default=False,
                   help='为没传 token 的 note_id,自动用 note_id 搜拿 token (默认关)')

    sub.add_parser('paths', help='打印路径配置')

    args = parser.parse_args()
    fn = globals().get(f'cmd_{args.cmd}')
    if not fn:
        err(f"未知子命令: {args.cmd}")
        return 1
    return fn(args) or 0


if __name__ == '__main__':
    sys.exit(main())
