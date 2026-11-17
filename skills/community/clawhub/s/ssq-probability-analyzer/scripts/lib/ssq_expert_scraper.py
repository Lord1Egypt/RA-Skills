"""
双色球专家推荐自动抓取 / 解析模块  (V1.7 升级)

设计目标：把"专家推荐"从「手动改 JSON」变成「自动化、可校验」的环节。
提供三种获取途径，按优先级自动组合：
  1. 通用文本解析 (parse_experts_from_text)：从任意粘贴/搜索结果文本中抽取
     "红球 XX XX XX XX XX + 蓝球 XX XX" 或 "XX XX XX XX XX + XX XX" 形态，
     自动命名专家。这是最稳的方式——自动化任务把 WebSearch 结果写入
     ssq_expert_input.txt，本脚本即可解析并更新 ssq_expert_picks.json。
  2. 站点直抓 (--live)：尝试新浪/中彩网/头条等 HTTP 源（best-effort，失败不致命）。
  3. 本地输入文件 (--from-file PATH)：解析指定文本文件。

用法：
  python ssq_expert_scraper.py --auto            # 自动：尝试live + 读取 ssq_expert_input.txt
  python ssq_expert_scraper.py --from-file txt  # 解析指定文本文件并更新JSON
  python ssq_expert_scraper.py --live            # 仅尝试HTTP直抓
"""
import re
import json
import sys
import os
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime

try:
    from ssq_expert_roster import EXPERTS as _ROSTER, DATA_SOURCES as _DATA_SOURCES, meta_for
except Exception:  # 独立运行/未随包时降级, 不致命
    _ROSTER, _DATA_SOURCES, meta_for = [], [], lambda n: None


# ---------------------------------------------------------------------------
# 通用文本解析器（核心能力：把人类/搜索结果文本变成结构化专家）
# ---------------------------------------------------------------------------
def parse_experts_from_text(text, require_named=False):
    """从任意文本中抽取专家推荐。

    Args:
        text: 待解析文本
        require_named: True 时仅接受带真实专家名的块 (用于 HTTP/搜索公开源,
            避免把历史开奖数据页/噪声数字行误当成专家推荐); 本地信任文件用 False。

    支持的形态（不区分全角/半角、空格/逗号/加号）：
      红球 05 08 11 24 31 + 蓝球 03 10
      红球: 05 08 11 24 31  蓝球: 03 10
      05 08 11 24 31 + 03 10
      张三：红球 05 08 11 24 31 + 蓝球 03 10
    每段/每行一个专家；带"XXX："前缀则采用该名，否则自动编号。

    Returns: list of dict {name, front:[...], back:[...], source}
    """
    if not text:
        return []

    # 切分段落：优先按换行；若整段无换行则整体一次
    blocks = [b for b in re.split(r'\n+', text) if b.strip()]
    if not blocks:
        blocks = [text]

    NOT_NAME = {'红球', '蓝球', '单注', '推荐', '预测', '分析', '双色球',
                '复式', '缩水', '精选', '专家', '老师', '红球', '蓝球'}
    experts = []
    auto_idx = 0
    for blk in blocks:
        blk = blk.strip()
        if not blk:
            continue

        front, back = [], []
        # 形态1: 显式 "红球 ... 蓝球 ..."
        m_exp = re.search(r'红球[：:\s]*([\d\s、,，+]+?)\s*蓝球[：:\s]*([\d\s、,，+]+)', blk)
        if m_exp:
            front = _extract(m_exp.group(1), 1, 35, 5)
            back = _extract(m_exp.group(2), 1, 12, 2)
        # 形态2: "X X X X X + X X"（以加号分割，最稳健）
        elif '+' in blk:
            left, right = blk.split('+', 1)
            front = _extract(left, 1, 35, 5)
            back = _extract(right, 1, 12, 2)
        # 形态3: 兜底——取前5个合法红球 + 后2个合法蓝球
        else:
            nums = [int(x) for x in re.findall(r'\d{1,2}', blk)]
            front = [n for n in nums if 1 <= n <= 35][:5]
            back = [n for n in nums if 1 <= n <= 12][:2]

        front = sorted(set(front))
        back = sorted(set(back))
        if len(front) != 5 or len(back) != 2:
            continue

        # 专家名：前缀 "XXX：" 且非关键词
        name = None
        m_name = re.match(r'^([\u4e00-\u9fa5A-Za-z·]{1,10})[：:\s]', blk)
        if m_name:
            cand = re.sub(r'(预测|推荐|分析|老师|专家|缩水|复式|精选)$', '', m_name.group(1))
            if cand and cand not in NOT_NAME and len(cand) >= 2:
                name = cand
        if not name:
            auto_idx += 1
            name = f"WebSearch专家{auto_idx}"
            named = False
        else:
            named = True

        if len(front) != 5 or len(back) != 2:
            continue
        if require_named and not named:
            # HTTP/搜索公开源必须带真实专家名, 否则极可能是历史开奖数据/噪声被误当推荐
            continue

        experts.append({'name': name, 'front': front, 'back': back, 'source': 'text-parsed'})

    # 去重（同名保留首个）
    seen, uniq = set(), []
    for e in experts:
        key = (e['name'], tuple(e['front']), tuple(e['back']))
        if key in seen:
            continue
        seen.add(key)
        uniq.append(e)
    return uniq


def _extract(s, lo, hi, n):
    """从字符串抽取 n 个 [lo,hi] 范围内的数字（按出现顺序）"""
    nums = [int(x) for x in re.findall(r'\d{1,2}', s) if lo <= int(x) <= hi]
    return nums[:n]


def fetch_from_file(filepath):
    """读取本地文本文件并解析为专家列表"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
        experts = parse_experts_from_text(text)
        print(f"  ✓ 从文件解析到 {len(experts)} 位专家: {filepath}")
        return experts
    except Exception as e:
        print(f"  ✗ 读取/解析文件失败 {filepath}: {e}")
        return []


# ---------------------------------------------------------------------------
# HTTP 直抓（best-effort，失败不致命）
# ---------------------------------------------------------------------------
def fetch_url(url, timeout=15):
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            for enc in ['utf-8', 'gb18030', 'gbk']:
                try:
                    return raw.decode(enc)
                except UnicodeDecodeError:
                    continue
            return raw.decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"  获取失败 {url}: {e}")
        return ""


def _parse_single_front_back(html, expert_name):
    single_pattern = re.compile(
        r'(\d{2})[、,， ](\d{2})[、,， ](\d{2})[、,， ](\d{2})[、,， ](\d{2})\s*\+\s*(\d{2})[、,， ](\d{2})')
    m = single_pattern.search(html)
    if m:
        return {
            'name': expert_name,
            'front': [int(m.group(i)) for i in range(1, 6)],
            'back': [int(m.group(i)) for i in range(6, 8)],
            'source': 'http',
        }
    return None


def _html_to_text(html):
    """去掉 HTML 标签, 保留纯文本(供 parse_experts_from_text 解析)。"""
    html = re.sub(r'<script.*?</script>', ' ', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<style.*?</style>', ' ', html, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text


# 公开可访问的"双色球专家推荐/号码分析"页面(非付费、best-effort)。
# 说明: 多数专家站点为 JS 渲染或付费墙, 定时任务里的纯 HTTP 抓取只能尽力而为;
# 最稳的"实时"路径是智能体(本系统宿主)用 WebSearch 抓取后写入 ssq_expert_input.txt。
# 注意: 仅保留"专家推荐/分析"类资讯页。datachart.500.com/ssq/ 是历史开奖数据页,
# 含大量 "XX XX XX XX XX + XX XX" 形态的历史号码, 会被通用解析器误当成专家推荐,
# 故不纳入 HTTP 直抓源(开奖数据由 ssq_huiniao_api 负责, 不在此重复)。
# V1.0.8: 新增指向"已知名家榜单页"的源(乐彩原创/彩宝贝十大/彩经网榜), 提升抓取针对性与时效。
LIVE_SOURCES = [
    ('乐彩网-原创分析', 'https://www.17500.cn/arts/'),
    ('彩宝贝-十大专家', 'https://www.78500.cn/ssqyuce/'),
    ('彩经网-专家排行榜', 'https://www.cjcp.com.cn/showsortchannel.php?type=ssq&sm=2'),
    ('中彩网-双色球', 'https://www.zhcw.com/ssq/'),
    ('新浪彩票-双色球', 'https://sports.sina.com.cn/lottery/'),
    ('今日头条搜索', 'https://so.toutiao.com/search?keyword=' + urllib.parse.quote('双色球 专家推荐 预测 下期')),
]


def fetch_live_experts():
    """尝试多个公开 HTTP 源(best-effort), 返回专家列表。
    对抓回的页面做标签剥离后用通用解析器抽取 '红球...蓝球...' 形态。"""
    experts = []
    for name, url in LIVE_SOURCES:
        try:
            html = fetch_url(url)
            if not html:
                continue
            text = _html_to_text(html)
            # 防误报: 仅当页面确实含双色球推荐特征时才解析, 避免随机数字被当成专家
            if not (('红球' in text or '蓝球' in text or '双色球' in text)
                    and ('+' in text or '红球' in text or '蓝球' in text)):
                continue
            # 防误报(强): HTTP源必须是"专家推荐"明确语境, 否则纯历史开奖数据页会被误当推荐
            if not re.search(r'专家|推荐|预测|分析师|老师|锦鲤|精选', text):
                continue
            found = parse_experts_from_text(text, require_named=True)
            for e in found:
                e['source'] = f'http:{name}'
                experts.append(e)
            if found:
                print(f"    ✓ {name}: 解析到 {len(found)} 条")
        except Exception:
            pass
    return experts


def fetch_search_experts(query='双色球 专家推荐 预测 下期'):
    """通过公开搜索页(best-effort)检索专家推荐文本并解析。"""
    experts = []
    try:
        url = 'https://www.bing.com/search?q=' + urllib.parse.quote(query)
        html = fetch_url(url, timeout=20)
        if html:
            text = _html_to_text(html)
            if (('红球' in text or '蓝球' in text or '双色球' in text) and '+' in text
                    and re.search(r'专家|推荐|预测|分析师|老师|锦鲤|精选', text)):
                found = parse_experts_from_text(text, require_named=True)
                for e in found:
                    e['source'] = 'http:search'
                    experts.append(e)
                if found:
                    print(f"    ✓ 搜索检索到 {len(found)} 条")
    except Exception:
        pass
    return experts


# ---------------------------------------------------------------------------
# 汇总 + 写回 JSON
# ---------------------------------------------------------------------------
def fetch_all_experts(target_period=None, text_file=None):
    """汇总专家推荐。

    Args:
        target_period: 目标期号（None 时自动推算）
        text_file: 本地文本文件路径（优先解析，最稳）
    """
    print(f"开始抓取专家推荐 (目标期号: {target_period})...")

    all_experts = []

    # 1) 本地文本文件（最优先，最可靠）
    if text_file and os.path.exists(text_file):
        all_experts.extend(fetch_from_file(text_file))

    # 2) 默认输入文件（自动化任务写入的 WebSearch 结果）
    default_input = 'ssq_expert_input.txt'
    if os.path.exists(default_input):
        all_experts.extend(fetch_from_file(default_input))

    # 3) HTTP 直抓（best-effort）
    try:
        all_experts.extend(fetch_live_experts())
    except Exception as e:
        print(f"  HTTP直抓失败(非致命): {e}")
    # 3b) 公开搜索抓取（best-effort, 全网检索专家推荐文本）
    try:
        all_experts.extend(fetch_search_experts())
    except Exception as e:
        print(f"  搜索抓取失败(非致命): {e}")

    # 过滤无效
    valid = [e for e in all_experts if e.get('front') and len(e['front']) == 5]
    print(f"\n抓取完成: {len(valid)} 位有效专家")
    return {
        'target_period': target_period,
        'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'source_count': len(valid),
        'experts': valid,
    }


def _normalize_expert(e):
    """把任意来源的专家 dict 规范为 {expert,front,back,source,scraped_at}。

    规范：专家名统一用键 'expert'(与 ssq_auto.py 消费端一致)，红球5个
    [1,35] 去重升序、蓝球2个 [1,12] 去重升序；不合法返回 None。"""
    if not isinstance(e, dict):
        return None
    name = e.get('expert') or e.get('name')
    if not name or not isinstance(name, str) or not name.strip():
        return None
    front = e.get('front') or []
    back = e.get('back') or []
    try:
        front = sorted({int(x) for x in front})
        back = sorted({int(x) for x in back})
    except (TypeError, ValueError):
        return None
    if len(front) != 5 or not all(1 <= n <= 35 for n in front):
        return None
    if len(back) != 2 or not all(1 <= n <= 12 for n in back):
        return None
    out = {
        'expert': name.strip(),
        'front': front,
        'back': back,
        'source': e.get('source', 'auto'),
        'scraped_at': e.get('scraped_at', ''),
    }
    # 若抓到的专家在常驻名录中, 补权威元数据(类型/平台/专长)——解决"不权威"观感
    m = meta_for(name.strip())
    if m:
        out['type'] = m['type']
        out['platform'] = m['platform']
        out['specialty'] = m['specialty']
    return out


def _source_prio(source):
    """来源可信度优先级：人工精选/智能体抓取 > 在线实时爬取 > 兜底。"""
    s = (source or '')
    if s.startswith('websearch') or s == 'text-parsed':
        return 3
    if s.startswith('http'):
        return 2
    return 1


def update_expert_picks_json(filepath='ssq_expert_picks.json', scraped_data=None,
                             curated_data=None, max_experts=40):
    """汇总并写回 ssq_expert_picks.json。

    - 读取现有文件(若存在)并规范化；
    - 合并 scraped_data(实时爬取) 与 curated_data(人工精选)；
    - 按专家名去重，高优先级来源覆盖低优先级；
    - 校验红球5/蓝球2 合法性，超限截断。
    """
    if not scraped_data and not curated_data:
        print("  无新专家数据，跳过 JSON 更新")
        return False
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            existing = json.load(f)
    except Exception:
        existing = {'experts': []}

    merged = {}  # name -> entry(含辅助键 _prio)

    def put(entry):
        name = entry['expert']
        if name.startswith('WebSearch专家'):
            # 无名自动编号 = HTTP/搜索源解析噪声或历史开奖数据误报, 不入专家库
            return
        prio = _source_prio(entry.get('source'))
        cur = merged.get(name)
        if cur is None or prio > cur['_prio'] or (
                prio == cur['_prio'] and entry.get('scraped_at', '') > cur.get('scraped_at', '')):
            entry = dict(entry)
            entry['_prio'] = prio
            merged[name] = entry

    for e in existing.get('experts', []):
        n = _normalize_expert(e)
        if n:
            put(n)
    if scraped_data:
        for e in scraped_data.get('experts', []):
            n = _normalize_expert(e)
            if n:
                put(n)
    if curated_data:
        for e in curated_data.get('experts', []):
            n = _normalize_expert(e)
            if n:
                put(n)

    experts = [ {k: v for k, v in e.items() if k != '_prio'}
                for e in merged.values() ][:max_experts]
    now = (scraped_data or curated_data or {}).get('updated_at') or \
        datetime.now().strftime('%Y-%m-%d %H:%M')
    # V1.0.5 主动体检修复: 此前写回时只保留旧 _meta, 从不吸收最新 target_period,
    # 导致自动刷新后标注期永远停在首次写入值, 跨期后与实际预测期错位、引发误报。
    # 现从最新抓取/精选数据(由 _auto_target 基于本地最新开奖推算)同步当前预测期。
    src_tp = (scraped_data or {}).get('target_period') or (curated_data or {}).get('target_period')
    new_meta = dict(existing.get('_meta', {
        'description': '双色球专家推荐数据 - 实时全网爬虫(智能体WebSearch + 脚本HTTP/搜索)',
        'auto_scraped': True,
        'note': '每期开奖前由智能体WebSearch实时检索全网专家推荐;定时任务亦由 ssq_expert_scraper.py --auto 做 best-effort HTTP/搜索抓取。模型仅将专家数据用作逆向(避开热门)信号,数学上不改变中奖概率(no_edge)。',
    }))
    if src_tp is not None:
        new_meta['target_period'] = src_tp
    new_meta['last_updated'] = now
    out = {
        '_meta': new_meta,
        'experts': experts,
        'updated_at': now,
        'auto_scraped': True,
        'source_count': len(experts),
    }
    # V1.0.8: 常驻专家名录段——即使实时抓取失败, 系统也始终'拥有'权威+野路子专家
    out = _append_catalog(out)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"  ✓ 专家推荐已更新到 {filepath} (共 {len(experts)} 位有效推荐, 去重后)")
    return True


def _append_catalog(out):
    """把常驻名录段并入已构建的 out dict(不覆盖 experts 数组)。"""
    try:
        out['_catalog'] = build_catalog()
    except Exception:
        pass
    return out


def build_catalog():
    """构建常驻名录段(始终写入 JSON, 即使实时抓取失败系统也'拥有'这批专家)。
    含权威名家 + 野路子高手 + 官方数据源; 仅元数据, 不带具体推荐号
    (具体推荐号由实时抓取/智能体 WebSearch 填充到 experts 数组)。"""
    catalog = {
        'authoritative': [
            {k: e[k] for k in ('name', 'platform', 'specialty', 'followers', 'verified', 'note')}
            for e in _ROSTER if e['type'] == '权威'
        ],
        'grassroots': [
            {k: e[k] for k in ('name', 'platform', 'specialty', 'followers', 'verified', 'note')}
            for e in _ROSTER if e['type'] == '野路子'
        ],
        'data_sources': [
            {k: d[k] for k in ('name', 'url', 'type', 'note')}
            for d in _DATA_SOURCES
        ],
    }
    return catalog


def _auto_target():
    try:
        from ssq_period import next_period as _np
        d = json.load(open('ssq_history.json', encoding='utf-8'))
        return _np(int(d[-1]['period']), d[-1].get('date'))
    except Exception:
        return None


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else '--auto'
    text_file = None
    if mode == '--from-file' and len(sys.argv) > 2:
        text_file = sys.argv[2]

    # V1.0.8: 打印常驻专家名录(供诊断/展示"系统拥有哪些专家")
    if mode == '--roster':
        try:
            from ssq_expert_roster import catalog_summary
            print("专家名录汇总:", catalog_summary())
            print("运行 `python ssq_expert_roster.py` 查看完整名单与官方数据源。")
        except Exception as e:
            print("名录模块不可用:", e)
        sys.exit(0)

    target = _auto_target()
    if mode == '--live':
        # 仅HTTP直抓
        data = {'target_period': target,
                'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'source_count': 0, 'experts': fetch_live_experts()}
        data['source_count'] = len(data['experts'])
    else:
        data = fetch_all_experts(target, text_file=text_file)

    print(json.dumps(data, ensure_ascii=False, indent=2))
    if data['source_count'] > 0:
        update_expert_picks_json('ssq_expert_picks.json', data)
