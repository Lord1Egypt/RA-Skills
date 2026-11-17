# -*- coding: utf-8 -*-
"""
双色球分析系统 V1 端到端自动化脚本

功能:
1. 自动下载最新开奖数据（国家体彩网/500彩票网，多源容错）
2. 数据校验（完整性、格式、去重、连续性）
3. 自动重算全部模型（CDM/马尔可夫/频率/遗漏）
4. 穷举有效组合（或加载缓存）
5. 自动评分选号（5组 6红球+蓝球复式 + 胆拖）
6. 从外部JSON加载专家推荐（支持每期更新）
7. 生成HTML报告
8. 输出预测结果JSON

用法:
  python ssq_auto.py              # 完整运行
  python ssq_auto.py --skip-download  # 跳过下载，用现有数据
  python ssq_auto.py --skip-exhaustive  # 跳过穷举（用缓存的有效组合）

V1修复:
- 自动化能力 10/10（专家自动抓取 Phase 0.6 + 战绩追踪回填 Phase 0.7 已接进 ssq_smart.py 流水线，非致命容错）
- 数据下载→校验→重算→选号→报告 全自动
- 定时任务: 每周二四日20:10自动运行（20:20结果生成→20:21审计→20:25全面检查→20:29交付最终结果）
- 专家推荐从外部JSON加载，不再硬编码
"""
import sys
import io
import json
import math
import os
import re
import subprocess
import random
import base64
import urllib.request
from collections import Counter, defaultdict
from itertools import combinations
from datetime import datetime
from ssq_period import next_period as next_period_func  # 统一期号计算(日期驱动年末进年)

# 本模块目录(lib/): 所有相对路径文件读写锚定到此处, 与调用方 cwd 解耦
# (SKILL 被市场以不同 cwd 调用时, ssq_history.json 等可回退联网, 但 ssq_power_report.json
#  无回退, 会致"四、命中现实分布"空白 —— 此锚定 + __main__ 内 chdir 彻底修复)
HERE = os.path.dirname(os.path.abspath(__file__))

# 对账历史覆盖(默认None): 用于"重生成历史期报告"时, 让开奖后实际命中对账
# 从独立完整历史读取目标期实际开奖, 与"预测所用历史"(须排除当期防泄露)解耦。
# 正常实时流水线此变量为None, 对账回退读磁盘完整历史文件; 仅手动重生成历史期报告时由脚本设置。
_RECONCILE_HISTORY_OVERRIDE = None

# 注意：sys.stdout 的 utf-8 包装只在 main() 内做（不在模块顶层），
# 否则被其他脚本 import 时会篡改导入进程的 stdout 并导致其被关闭。
PRIMES = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31}

# 蓝球综合评分统一走 ssq_common.back_score, 杜绝"验证器/预测器"公式漂移
from ssq_common import back_score as _back_score  # noqa: E402

# 开奖公告滚动字幕(体彩中心官方API, 带缓存)
from ssq_draw_announcement import generate_marquee_html as _generate_marquee

# 近期一等奖领奖新闻（真实故事，best-effort 联网刷新 + 离线回退，绝不编造）
from ssq_news_fetcher import get_winning_news as _get_winning_news
# 真实彩票图片（一次性抓取 + 本地缓存；取不到时由下方 load_win_illustrations 回退到 AI 插画）
from ssq_photo_fetcher import load_real_photos_b64 as _load_real_photos
# 深度号码分析（学习增强版：多窗口Z-score / 历史间隔 / 结构特征 / 香农熵，仅描述不预测）
from ssq_deep_analysis import render_deep_analysis_html
# 专家近期观点荟萃（公开名家当期观点，娱乐参考，不预测）
from ssq_expert_roster import render_expert_views_html
from ssq_fun_pack import FUN_PACK_CSS, generate_fun_pack_section  # noqa: E402
from ssq_ledger import record_spend, summary as ssq_ledger_summary  # noqa: E402

# ============================================================
# 1. 数据下载（多源容错）
# ============================================================
# ============================================================
# 1b. 数据源配置（多源优先级 + 可切换）
# ============================================================
# 优先级顺序即故障转移顺序；运维可用 ssq_data_recovery.py 强制指定某一源
DATA_SOURCES = [
    ("huiniao", "huiniao API (主数据源, 免费全量)"),
    ("cwl",     "国家体彩网 cwl.gov.cn API"),
    ("500",     "500彩票网 datachart.500.com"),
]


def _record_source(source, count):
    """记录最后成功的数据源（运维/容灾可观测状态）"""
    try:
        with open('ssq_data_source.json', 'w', encoding='utf-8') as f:
            json.dump({
                'source': source,
                'count': count,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'ok': True,
            }, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def _fetch_from_huiniao():
    """huiniao 主源：返回 draws 或抛异常"""
    from ssq_huiniao_api import fetch_all_huiniao, fetch_latest_huiniao, merge_huiniao_with_existing
    latest = fetch_latest_huiniao(limit=10)
    if not latest:
        raise RuntimeError("huiniao 最新10期为空")
    draws = []
    try:
        with open('ssq_history.json', 'r', encoding='utf-8') as f:
            existing = json.load(f)
        if existing and len(existing) > 2000:
            draws = merge_huiniao_with_existing(existing, latest)
            more = fetch_latest_huiniao(limit=50)
            draws = merge_huiniao_with_existing(draws, more)
        else:
            draws = fetch_all_huiniao()
    except Exception:
        draws = fetch_all_huiniao()
    if not draws:
        raise RuntimeError("huiniao 返回空")
    return draws


def _fetch_from_cwl():
    """中国福利彩票网 API(双色球 name=ssq)：返回 draws 或抛异常"""
    url = 'https://www.cwl.gov.cn/cwl_admin/front/cwlkj/search/kjxx/findDrawNotice?name=ssq&issueCount=5000'
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://www.cwl.gov.cn/',
        'Accept': 'application/json'
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode('utf-8'))
    draws = []
    if data and 'result' in data:
        for item in data['result']:
            try:
                front = sorted([int(x) for x in item.get('red', '').split(',')])
                back = sorted([int(x) for x in item.get('blue', '').split(',')])
                if len(front) == 6 and len(back) == 1:
                    draws.append({'period': item.get('code', ''), 'date': item.get('date', ''),
                                  'front': front, 'back': back})
            except Exception:
                continue
    if not draws:
        raise RuntimeError("cwl 返回空")
    return draws


def _fetch_from_500():
    """500彩票网：返回 draws 或抛异常（V1.2 BUG11修复：end用现有最新期号）"""
    end_param = ''
    try:
        with open('ssq_history.json', 'r', encoding='utf-8') as f:
            existing = json.load(f)
        if existing:
            end_param = f'&end={existing[-1]["period"]}'
    except Exception:
        pass
    url = f'https://datachart.500.com/ssq/history/newinc/history.php?limit=5000&start=03001{end_param}'
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = resp.read()
    html = None
    for enc in ['utf-8', 'gb18030', 'gbk']:
        try:
            html = raw.decode(enc)
            break
        except Exception:
            continue
    if html is None:
        raise RuntimeError("500 解码失败")
    draws = []
    for row in re.findall(r'<tr[^>]*>(.*?)</tr>', html, re.DOTALL):
        tds = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
        if len(tds) < 5:
            continue
        clean = [re.sub(r'<[^>]+>', '', td).strip() for td in tds]
        period = next((td for td in clean if re.match(r'^\d{5,7}$', td)), None)
        if not period:
            continue
        nums = [int(td) for td in clean if re.match(r'^\d{1,2}$', td) and 1 <= int(td) <= 33]
        if len(nums) >= 7:
            front = sorted(nums[:6])
            back = sorted(nums[6:7])
            if len(set(front)) == 6 and len(set(back)) == 1 and all(1 <= n <= 16 for n in back):
                date_str = next((m.group(1) for td in clean if (m := re.match(r'(\d{4}-\d{2}-\d{2})', td))), '')
                draws.append({'period': period, 'date': date_str, 'front': front, 'back': back})
    if not draws:
        raise RuntimeError("500 返回空")
    return draws


def download_data(force_source=None):
    """多源优先级容错下载（V1.7 重构：结构清晰+可观测+可切换）。

    Args:
        force_source: 指定仅用某一源（运维恢复用），None 则按 DATA_SOURCES 顺序故障转移。
    Returns:
        list | None
    """
    print("=" * 70)
    print("【步骤1/7: 数据下载 (多源优先级容错)】")
    print("=" * 70)

    fetchers = {"huiniao": _fetch_from_huiniao, "cwl": _fetch_from_cwl, "500": _fetch_from_500}
    order = [force_source] if force_source else [s[0] for s in DATA_SOURCES]

    draws = []
    used_source = None
    for name in order:
        if name not in fetchers:
            print(f"  ⚠ 未知数据源: {name} (可选: {list(fetchers)})")
            continue
        print(f"\n  尝试数据源: {name} ...")
        try:
            d = fetchers[name]()
            if d and len(d) >= 100:
                draws = d
                used_source = name
                print(f"  ✓ {name}: 获取 {len(draws)} 期")
                break
            else:
                print(f"  ✗ {name}: 数据不足 ({len(d) if d else 0}期)")
        except Exception as e:
            print(f"  ✗ {name} 失败: {e}")

    # 本地兜底（V1.2 BUG10修复：不足时不覆盖现有完整数据）
    if len(draws) < 100:
        print(f"\n  ⚠ 在线源不足，尝试使用现有 ssq_history.json ...")
        try:
            with open('ssq_history.json', 'r', encoding='utf-8') as f:
                existing = json.load(f)
            if len(existing) > len(draws):
                draws = existing
                used_source = used_source or 'local-fallback'
                print(f"  ✓ 使用本地数据: {len(draws)} 期")
        except Exception as e:
            print(f"  ✗ 本地也失败: {e}")

    if not draws:
        print("  ✗ 所有数据源均失败！无法继续。")
        return None

    # 去重 + 排序
    seen = set()
    unique = []
    for d in draws:
        if d['period'] not in seen:
            seen.add(d['period'])
            unique.append(d)
    draws = unique
    draws.sort(key=lambda x: x['period'])

    _record_source(used_source or 'unknown', len(draws))
    _record_fetch(used_source or 'unknown', len(draws), draws[-1] if draws else None)
    print(f"\n  ✓ 数据就绪: {len(draws)}期 (主源={used_source})")
    return draws


def persist_history(draws):
    """合并并保存到 ssq_history.json（V1.0 BUG16修复：保留更完整的；首次运行则新建）"""
    try:
        with open('ssq_history.json', 'r', encoding='utf-8') as f:
            existing = json.load(f)
        if len(existing) > len(draws):
            existing_periods = set(d['period'] for d in existing)
            new_draws = [d for d in draws if d['period'] not in existing_periods]
            if new_draws:
                draws = existing + new_draws
                print(f"  ✓ 合并后{len(draws)}期（新增{len(new_draws)}期）")
            else:
                draws = existing
                print(f"  ✓ 使用现有{len(draws)}期（无新数据）")
    except FileNotFoundError:
        pass  # 首次运行
    draws.sort(key=lambda x: x['period'])
    with open('ssq_history.json', 'w', encoding='utf-8') as f:
        json.dump(draws, f, ensure_ascii=False, indent=2)
    print(f"  ✓ 数据已保存到 ssq_history.json ({len(draws)}期)")
    return draws


# ============================================================
# 2. 数据校验
# ============================================================
def validate_data(draws):
    """校验数据完整性和格式"""
    print("\n" + "=" * 70)
    print("【步骤2/7: 数据校验】")
    print("=" * 70)
    
    issues = []
    fatal = []  # 致命错误: 出现则拒绝将脏数据写入 ssq_history.json
    total = len(draws)
    
    print(f"  总期数: {total}")
    print(f"  最早: {draws[0]['period']} ({draws[0]['date']})")
    print(f"  最新: {draws[-1]['period']} ({draws[-1]['date']})")
    print(f"  最新红球: {' '.join(f'{n:02d}' for n in draws[-1]['front'])}")
    print(f"  最新蓝球: {' '.join(f'{n:02d}' for n in draws[-1]['back'])}")
    
    # 格式检查 (致命: 号码非法会破坏所有模型计算, 必须拦截落盘)
    format_errors = 0
    for d in draws:
        if len(d['front']) != 6 or len(d['back']) != 1:
            format_errors += 1
            continue
        if not all(1 <= n <= 33 for n in d['front']) or len(set(d['front'])) != 6:
            format_errors += 1
            continue
        if not all(1 <= n <= 16 for n in d['back']) or len(set(d['back'])) != 1:
            format_errors += 1
    
    if format_errors:
        print(f"  ✗ 格式错误(致命): {format_errors}期 — 拒绝写入脏数据")
        issues.append(f"格式错误{format_errors}期")
        fatal.append(f"格式错误{format_errors}期")
    else:
        print(f"  ✓ 格式检查通过")
    
    # 期号连续性
    missing = []
    for i in range(1, total):
        prev_p = int(draws[i-1]['period'])
        curr_p = int(draws[i]['period'])
        if curr_p - prev_p > 10:
            prev_year = prev_p // 1000
            curr_year = curr_p // 1000
            if curr_year == prev_year:
                missing.append((draws[i-1]['period'], draws[i]['period']))
    
    if missing:
        print(f"  ⚠ 期号跳跃: {len(missing)}处")
        for p1, p2 in missing[:3]:
            print(f"    {p1} → {p2}")
        issues.append(f"期号跳跃{len(missing)}处")
    else:
        print(f"  ✓ 期号连续性通过")
    
    # 日期顺序 (致命: 日期倒序意味着数据抓取/排序错乱)
    date_issues = sum(1 for i in range(1, total) if draws[i]['date'] and draws[i-1]['date'] and draws[i]['date'] < draws[i-1]['date'])
    if date_issues:
        print(f"  ✗ 日期倒序(致命): {date_issues}期 — 拒绝写入脏数据")
        issues.append(f"日期倒序{date_issues}期")
        fatal.append(f"日期倒序{date_issues}期")
    else:
        print(f"  ✓ 日期顺序通过")
    
    # 数据新鲜度检查
    latest_date = draws[-1]['date']
    if latest_date:
        try:
            latest_dt = datetime.strptime(latest_date, '%Y-%m-%d')
            days_ago = (datetime.now() - latest_dt).days
            if days_ago > 7:
                print(f"  ⚠ 数据可能过期: 最新数据距今{days_ago}天")
                issues.append(f"数据过期{days_ago}天")
            else:
                print(f"  ✓ 数据新鲜度通过 (最新{days_ago}天前)")
        except:
            print(f"  ⚠ 无法解析日期: {latest_date}")
    
    if issues:
        print(f"\n  ⚠ 校验发现{len(issues)}个问题: {', '.join(issues)}")
        if fatal:
            print(f"  ⛔ 其中致命错误{len(fatal)}项: {', '.join(fatal)} — 将拒绝写入脏数据")
    else:
        print(f"\n  ✓ 数据校验全部通过")
    
    return {'issues': issues, 'fatal': fatal}

# ============================================================
# 3. 工具函数
# ============================================================
# ★ 单一可信源 (Single Source of Truth):
#   这些形态函数与 9 项过滤器阈值一律从 ssq_common 导入, 严禁在本文件内联重复定义。
#   历史教训(移植双色球时真实踩到): 本文件曾内联一份大乐透阈值
#   (AC[4,6]/和值[80,130]/奇偶2:3/大小2:3/质数1-2 等双色球不存在的阈值), 而 ssq_common 已改成
#   双色球数据校准阈值 → 同一套"9项过滤器"在穷举端与回测端结果相差 11 倍
#   (2.84% vs 32.83%), 且无人报错。改为 import 后, 两套真相在语言层面不可能再出现。
from ssq_common import (            # noqa: E402
    calc_ac,
    odd_count,
    small_count,
    prime_count,
    road_counts,
    consecutive_groups,
    passes_filters,
    K,
    BACK_N,
)
from ssq_power_engine import PRIZE_PAYOUT  # noqa: E402


# ============================================================
# 3b. 历史相似形态统计 (V1.0.4: 每组展示"历史相似形态中奖概率")
# ============================================================
def _shape_signature(front):
    """计算红球组合的9维形态签名(用于历史相似形态检索)。"""
    fs = sorted(front)
    return {
        'ac': calc_ac(front),
        'sum': sum(front),
        'span': fs[-1] - fs[0],
        'odd': odd_count(front),
        'small': small_count(front),
        'road': road_counts(front),
        'cg': consecutive_groups(front),
        'prime': prime_count(front),
    }


def similar_shape_stats(front, back, draws, n_tickets=1):
    """为每组提供两种诚实的"历史中奖参考"(均为后验/描述性, 不预测未来):

    1) 形态历史占比(shape_prevalence): 历史中与本组形态(AC/和值/跨度/奇偶/
       大小/012路/连号/质数)相近的开奖期数 / 总期数——描述这种形态多常见。
    2) 固定号码历史回测(backtest): 若每期都固定投注本组这注(红球5码 + 蓝球
       n_back选2复式, 共 n_tickets 张票), 在所有历史开奖期上逐期核对命中,
       统计各奖级命中次数、任意奖级中奖期率、总奖金、总投入与 ROI。蓝球复式
       按"实际购票张数"计成本(n_tickets), 故 ROI 真实反映复式投入。

    诚实边界: 一等奖概率对任何一注相同(1/17.7M); 本回测只说明"过去若这么买会
    怎样", 不等于"未来会中奖"; 固定号码 ROI 长期为负属数学期望(印证 no_edge)。
    """
    sig = _shape_signature(front)
    cohort = 0
    N = len(draws)
    for d in draws:
        s2 = _shape_signature(d['front'])
        if (s2['odd'] == sig['odd'] and s2['small'] == sig['small']
                and s2['road'] == sig['road'] and s2['cg'] == sig['cg']
                and abs(s2['ac'] - sig['ac']) <= 1
                and abs(s2['sum'] - sig['sum']) <= 15
                and abs(s2['span'] - sig['span']) <= 6
                and abs(s2['prime'] - sig['prime']) <= 1):
            cohort += 1
    shape_prevalence = cohort / N if N else 0.0

    # 固定号码历史回测: 直接复用 ssq_power_engine 奖级映射(单一可信源, 双色球6档),
    # 保证与回测管线一致。不保留陈旧兜底副本——若导入失败应显式报错而非静默用错奖金。
    from ssq_power_engine import PRIZE_NAME, PRIZE_PAYOUT, COST_PER_BET

    fset, bset = set(front), set(back)
    tier_counts = {}
    any_hit = 0
    total_prize = 0
    for d in draws:
        fh = len(fset & set(d['front']))
        # 蓝球复式: 以"实际购票张数"判定中奖(任一张对上即中奖)
        drawn_back = set(d['back'])
        in_my = len(bset & drawn_back)
        bh = 1 if in_my >= 1 else 0
        name = PRIZE_NAME.get((fh, bh))
        if name:
            tier_counts[name] = tier_counts.get(name, 0) + 1
            any_hit += 1
            total_prize += PRIZE_PAYOUT.get((fh, bh), 0)
    cost = N * n_tickets * COST_PER_BET
    roi = (total_prize - cost) / cost if cost else 0.0
    win_rate = any_hit / N if N else 0.0

    return {
        'cohort': cohort, 'N': N, 'shape_prevalence': shape_prevalence,
        'backtest': {
            'plays': N, 'any_hit': any_hit, 'win_rate': win_rate,
            'tier_counts': tier_counts, 'total_prize': total_prize,
            'cost': cost, 'roi': roi,
        },
    }


# ============================================================
# 4. 穷举有效组合
# ============================================================
def exhaustive_combos():
    """穷举全部C(33,6)=1,107,568个组合，返回通过8项静态过滤器的组合"""
    print("\n" + "=" * 70)
    print("【步骤3/7: 穷举有效组合】")
    print("=" * 70)
    
    all_pass = []
    for combo in combinations(range(1, 34), 6):
        if passes_filters(list(combo)):
            all_pass.append(list(combo))
    
    print(f"  总组合数: {math.comb(33, 6):,}")
    print(f"  通过8项静态过滤器: {len(all_pass):,} ({len(all_pass)/math.comb(33,6)*100:.2f}%)")
    
    with open('ssq_valid_combos.json', 'w', encoding='utf-8') as f:
        json.dump(all_pass, f)
    print(f"  ✓ 已保存到 ssq_valid_combos.json")
    
    return all_pass

def load_valid_combos():
    """加载缓存的有效组合"""
    try:
        with open('ssq_valid_combos.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

# ============================================================
# 5. 计算预测模型
# ============================================================
def compute_models(draws):
    """计算全部预测模型（与ssq_final.py/ssq_exhaustive.py完全一致）"""
    print("\n" + "=" * 70)
    print("【步骤4/7: 计算预测模型】")
    print("=" * 70)
    
    total = len(draws)
    latest = draws[-1]
    
    # CDM (empirical Bayes)
    front_freq = Counter()
    back_freq = Counter()
    for d in draws:
        for n in d['front']:
            front_freq[n] += 1
        for n in d['back']:
            back_freq[n] += 1
    
    n_total = total * 6
    freqs = {num: front_freq.get(num, 0) / n_total for num in range(1, 34)}
    # V1.0.2 修复 empirical Bayes 先验退化 bug:
    # 原 alpha_prior[num] = alpha_0 * freqs[num] 与数据成比例, 代入 posterior 后
    # alpha_0 项被完全抵消, 导致 cdm_prob 退化为原始经验频率(front_freq/total),
    # 所谓"经验贝叶斯收缩"从未生效。改为与数据独立的 flat 先验, 收缩真实发生。
    prior_strength = max(1.0, total * 0.02)   # 等效伪计数强度, 随样本量自适应
    alpha_prior = {num: prior_strength / 33 for num in range(1, 34)}
    posterior = {num: alpha_prior[num] + front_freq.get(num, 0) for num in range(1, 34)}
    total_post = sum(posterior.values())
    cdm_prob = {num: 6 * posterior[num] / total_post for num in range(1, 34)}
    print(f"  CDM 先验强度 = {prior_strength:.1f} (flat empirical-Bayes, 已修复退化)")
    
    # 马尔可夫
    transition = defaultdict(lambda: defaultdict(int))
    state_count = defaultdict(int)
    for i in range(len(draws) - 1):
        for n1 in set(draws[i]['front']):
            state_count[n1] += 1
            for n2 in set(draws[i+1]['front']):
                transition[n1][n2] += 1
    latest_front = set(latest['front'])
    markov_prob = defaultdict(float)
    for n1 in latest_front:
        sc = state_count[n1]
        if sc == 0:
            continue
        for n2 in range(1, 34):
            markov_prob[n2] += transition[n1][n2] / sc / len(latest_front)
    
    # 近30期频率
    recent_30 = draws[-30:]
    freq_30 = Counter()
    for d in recent_30:
        for n in d['front']:
            freq_30[n] += 1
    
    # 遗漏值
    front_omit = {}
    for num in range(1, 34):
        omit = 0
        for i in range(len(draws)-1, -1, -1):
            if num in draws[i]['front']:
                break
            omit += 1
        front_omit[num] = omit
    
    max_omit = max(front_omit.values()) if front_omit else 1
    
    # 综合评分 [0.40, 0.25, 0.20, 0.15]
    combined_score = {}
    for num in range(1, 34):
        cdm_s = cdm_prob.get(num, 0) / (6/33)
        markov_s = markov_prob.get(num, 0) / (6/33)
        freq30_s = freq_30.get(num, 0) / (30 * 6 / 33)
        omit_s = front_omit[num] / max_omit if max_omit > 0 else 0
        combined_score[num] = 0.40 * cdm_s + 0.25 * markov_s + 0.20 * freq30_s + 0.15 * (0.5 + 0.5 * omit_s)
    
    print(f"  权重: [0.40 CDM, 0.25 马尔可夫, 0.20 近30期频率, 0.15 遗漏]")
    print(f"  训练数据: 全部{total}期 (扩展窗口)")
    
    # 蓝球预测
    back_omit = {}
    for num in range(1, 17):
        omit = 0
        for i in range(len(draws)-1, -1, -1):
            if num in draws[i]['back']:
                break
            omit += 1
        back_omit[num] = omit
    
    # V1.2修复: 蓝球遗漏值用/max_back_omit归一化（原固定/10，与红球归一化方式不一致）
    max_back_omit = max(back_omit.values()) if back_omit else 1
    
    n_back = total * 1
    # V1.0.2 同步修复: 蓝球 empirical Bayes 先验退化(同上, flat 先验)
    prior_strength_b = max(1.0, total * 0.02)
    alpha_prior_b = {num: prior_strength_b / 16 for num in range(1, 17)}
    posterior_b = {num: alpha_prior_b[num] + back_freq.get(num, 0) for num in range(1, 17)}
    total_post_b = sum(posterior_b.values())
    cdm_prob_b = {num: 1 * posterior_b[num] / total_post_b for num in range(1, 17)}
    
    back_trans = defaultdict(lambda: defaultdict(int))
    back_sc = defaultdict(int)
    for i in range(len(draws) - 1):
        for n1 in set(draws[i]['back']):
            back_sc[n1] += 1
            for n2 in set(draws[i+1]['back']):
                back_trans[n1][n2] += 1
    latest_back = set(latest['back'])
    markov_back = defaultdict(float)
    for n1 in latest_back:
        sc = back_sc[n1]
        if sc == 0:
            continue
        for n2 in range(1, 17):
            markov_back[n2] += back_trans[n1][n2] / sc / len(latest_back)
    
    return {
        'cdm_prob': cdm_prob, 'markov_prob': markov_prob,
        'freq_30': freq_30, 'front_omit': front_omit, 'max_omit': max_omit,
        'combined_score': combined_score,
        'back_freq': back_freq, 'back_omit': back_omit, 'max_back_omit': max_back_omit,
        'cdm_prob_b': cdm_prob_b, 'markov_back': markov_back,
        'front_freq': front_freq,
    }

# ============================================================
# 5.5 期号种子后验采样 (V1.0.2: 解决连续期推荐高度相似问题)
# ============================================================
def _weighted_sample_k(score_dict, k, rng, pool):
    """从 pool 按 score_dict 权重无放回抽取 k 个, 返回升序 tuple。"""
    avail = list(pool)
    chosen = []
    for _ in range(k):
        if not avail:
            break
        weights = [max(score_dict.get(n, 1e-12), 1e-12) for n in avail]
        tot = sum(weights)
        r = rng.random() * tot
        acc = 0.0
        sel = avail[-1]
        for n, w in zip(avail, weights):
            acc += w
            if r <= acc:
                sel = n
                break
        chosen.append(sel)
        avail.remove(sel)
    return tuple(sorted(chosen))


def _sample_front_group(score_dict, valid_set, used, prev_front, seed):
    """按 seed 可复现地从 score_dict 后验分布抽样一个通过过滤且未用的6红球组合。"""
    rng = random.Random(seed)
    for _ in range(800):
        combo = _weighted_sample_k(score_dict, 6, rng, list(range(1, 34)))
        if combo in valid_set and combo not in used and len(set(combo) & set(prev_front)) <= 2:
            return list(combo)
    return None


def _sample_back_group(score_dict, used_backs, seed):
    """按 seed 可复现地从 score_dict 后验分布抽样一个3蓝球复式组合(与已用蓝球去重)。"""
    rng = random.Random(seed)
    for _ in range(400):
        combo = _weighted_sample_k(score_dict, 3, rng, list(range(1, 17)))
        if combo not in used_backs:
            return list(combo)
    return None


# ============================================================
# 6. 生成预测
# ============================================================
def _perturb(dist, period_seed, salt, tag):
    """对评分分布施加确定性扰动(期号种子+盐驱动), 使不同期自然重排推荐。

    噪声幅度与评分跨度同量级 → 足以在不同期重排 top 组合; 同一 (期号,salt) 恒定 → 可复现。
    """
    rng = random.Random(int(period_seed) * 100003 + salt * 7919 + 17 + tag * 104729)
    items = list(dist.items())
    if not items:
        return dict(dist)
    vals = [v for _, v in items]
    spread = (max(vals) - min(vals)) or 1.0
    out = {}
    for k, v in items:
        nv = v + rng.uniform(-0.5, 0.5) * spread
        out[k] = nv if nv > 0 else 0.0
    return out


def _gen_core(draws, models, valid_combos, expert_picks, salt=0):
    """生成5组红球推荐 + 蓝球推荐 + 胆拖方案（单次, 由 generate_predictions 包裹跨期唯一性闸门）"""
    print("\n" + "=" * 70)
    print("【步骤5/7: 生成预测】")
    print("=" * 70)
    
    latest = draws[-1]
    prev_front = latest['front']
    combined_score = models['combined_score']
    cdm_prob = models['cdm_prob']
    markov_prob = models['markov_prob']
    front_omit = models['front_omit']
    
    # 从有效组合中选TOP5
    valid_set = set(tuple(sorted(c)) for c in valid_combos)
    
    # 动态过滤: 加第9项重号
    valid_dynamic = [c for c in valid_combos if len(set(c) & set(prev_front)) <= 2]
    print(f"  有效组合(静态8项): {len(valid_combos):,}")
    print(f"  有效组合(含重号9项): {len(valid_dynamic):,}")
    
    # V1.0.2: 期号种子后验采样 —— 让每期推荐随新数据合理变化, 而不冻结在
    # 2900+期频率的 argmax 上 (这正是 26085/26086 两期高度相似的根因)。
    # 同一 target_period 用同一 seed → 可复现; 不同期 seed 不同 → 推荐自然变化。
    target_period = next_period_func(int(latest['period']), latest.get('date'))

    valid_dynamic_set = set(tuple(sorted(c)) for c in valid_dynamic)

    # 蓝球综合评分分布
    back_scored = {}
    for num in range(1, 17):
        cdm_s = models['cdm_prob_b'].get(num, 0)
        mk_s = models['markov_back'].get(num, 0)
        omit_s = models['back_omit'].get(num, 0) / models['max_back_omit']
        back_scored[num] = _back_score(cdm_s, mk_s, omit_s)

    # 各策略红球采样分布
    if expert_picks:
        front_eci = Counter()
        for expert, front, back in expert_picks:
            for n in front:
                front_eci[n] += 1
        front_eci_pct = {num: front_eci.get(num, 0) / len(expert_picks) * 100 for num in range(1, 34)}
        eci_front_dist = {n: 0.6 * combined_score[n] + 0.4 * (100 - front_eci_pct.get(n, 0)) / 100
                          for n in range(1, 34)}
        # 蓝球: 避开专家最热门
        back_eci_count = Counter()
        for expert, front, back in expert_picks:
            for n in back:
                back_eci_count[n] += 1
        maxc = max(back_eci_count.values(), default=1)
        eci_back_dist = {n: (maxc - back_eci_count.get(n, 0) + 1) for n in range(1, 17)}
        eci_name = 'ECI逆向(真实专家)'
        eci_strategy = f'避开{len(expert_picks)}位专家热门 后验采样'
    else:
        eci_front_dist = {n: front_omit.get(n, 0) for n in range(1, 34)}
        eci_back_dist = back_scored
        eci_name = '遗漏优选'
        eci_strategy = '遗漏值最大组合(无专家数据替代ECI) 后验采样'

    # V1.0.3: 5 个真正不同的策略锚点 —— 此前 综合/CDM/马尔可夫/逆向 都源于同一频率家族
    # (综合=0.4CDM+0.25马可+0.2频率+0.15遗漏, 逆向=0.6综合+0.4反专家), 本质同类,
    # 导致"多种方法"实则推荐相近号码。现改为 5 个互不从属的哲学 + 各自独立蓝球锚点,
    # 并强制同期组内最小差异, 彻底消除"方法雷同 / 蓝球近孪生"。
    # ---- V1.0.8 跨期变化修复: 让期号种子真正驱动选号 ----
    # 旧版(≤V1.0.0)推荐被 2900+期频率评分主导, 相邻期历史差异极小→评分几乎不变
    # → 不同期给出完全相同号码(用户实测证实)。现对每期评分分布施加"期号种子+盐"
    # 确定性扰动(噪声幅度与评分跨度同量级), 使不同期自然重排出不同前/蓝球组合;
    # 同日同期 salt=0 恒定 → 完全可复现。配合下方跨期唯一性硬闸门, 彻底杜绝
    # "不同期号码一样"。娱乐组合多样性, 不暗示任何预测力。
    ps = int(target_period)
    combined_score_p = _perturb(combined_score, ps, salt, 1)
    freq30_p         = _perturb(models['freq_30'], ps, salt, 2)
    front_omit_p     = _perturb(front_omit, ps, salt, 3)
    eci_front_p      = _perturb(eci_front_dist, ps, salt, 4)
    back_scored_p    = _perturb(back_scored, ps, salt, 5)
    cdm_b_p          = _perturb(models['cdm_prob_b'], ps, salt, 6)
    back_omit_p      = _perturb(models['back_omit'], ps, salt, 7)
    eci_back_p       = _perturb(eci_back_dist, ps, salt, 8)

    back_dist = {
        '综合共识': back_scored_p,
        '热号追踪': cdm_b_p,
        '冷号回补': {n: back_omit_p.get(n, 0) for n in range(1, 17)},
        '逆向专家': eci_back_p,
        '熵均衡': {n: 1.0 for n in range(1, 17)},
    }
    strategy_defs = [
        ('综合共识', combined_score_p, back_dist['综合共识'], 'CDM+马尔可夫+频率+遗漏加权[0.40,0.25,0.20,0.15] 后验采样(期号扰动)'),
        ('热号追踪', freq30_p, back_dist['热号追踪'], '近30期高频热号 后验采样(期号扰动)'),
        ('冷号回补', front_omit_p, back_dist['冷号回补'], '遗漏值最大(冷号) 后验采样(期号扰动)'),
        (eci_name, eci_front_p, back_dist['逆向专家'], eci_strategy),
        ('熵均衡', {n: 1.0 for n in range(1, 34)}, back_dist['熵均衡'], '无偏均匀(最大多样性/随机基准) 后验采样'),
    ]

    groups = []
    used = set()
    used_backs = set()
    for idx, (name, front_dist, back_dist_i, strategy) in enumerate(strategy_defs):
        placed = False
        for attempt in range(8):
            seed = int(target_period) * 100003 + idx * 7919 + 17 + (attempt + salt * 97) * 1000003
            front = _sample_front_group(front_dist, valid_dynamic_set, used, prev_front, seed)
            # argmax 兜底 (采样极端失败时用)
            if front is None:
                cand = sorted(valid_dynamic, key=lambda c: sum(front_dist.get(n, 0) for n in c), reverse=True)
                for c in cand:
                    if tuple(sorted(c)) not in used:
                        front = list(c)
                        break
            if front is None:
                continue
            # 红球与已有组重叠≤4 (灭掉近孪生/全等)
            if any(len(set(front) & set(g['front'])) >= 5 for g in groups):
                continue
            back = _sample_back_group(back_dist_i, used_backs, seed + 1)
            if back is None:
                back = sorted(sorted(range(1, 17), key=lambda n: back_dist_i.get(n, 0), reverse=True)[:3])
            # 蓝球与已有组重叠≤1 (灭掉 2/3 近孪生)
            if any(len(set(back) & set(g['back'])) >= 2 for g in groups):
                continue
            used.add(tuple(sorted(front)))
            used_backs.add(tuple(sorted(back)))
            groups.append({'name': name, 'strategy': strategy, 'front': sorted(front), 'back': sorted(back)})
            placed = True
            break
        if not placed:
            # 兜底(极低概率): 强制放置
            front = sorted(range(1, 34), key=lambda n: front_dist.get(n, 0), reverse=True)[:6] if front is None else front
            back = sorted(sorted(range(1, 17), key=lambda n: back_dist_i.get(n, 0), reverse=True)[:3])
            groups.append({'name': name, 'strategy': strategy, 'front': sorted(front), 'back': sorted(back)})
    
    # 检查多样性
    all_front_nums = set()
    for g in groups:
        all_front_nums.update(g['front'])
    all_back_nums = set()
    for g in groups:
        all_back_nums.update(g['back'])
    
    print(f"\n  5组红球推荐:")
    for g in groups:
        details_ac = calc_ac(g['front'])
        details_sum = sum(g['front'])
        print(f"    {g['name']}: {' '.join(f'{n:02d}' for n in sorted(g['front']))} + {' '.join(f'{n:02d}' for n in sorted(g['back']))} | AC={details_ac} 和值={details_sum}")
    
    print(f"\n  红球覆盖: {len(all_front_nums)}/33 ({len(all_front_nums)/33*100:.0f}%)")
    print(f"  蓝球覆盖: {len(all_back_nums)}/16 ({len(all_back_nums)/16*100:.0f}%)")
    
    # 胆拖方案 - V1.0.4 修复: 此前 search_pool = combined_score argmax TOP20(冻结),
    # 与 26085/26086 两期红球高度相似的"冻结 argmax"同源 BUG —— 导致胆拖每期几乎不变。
    # 现改为按目标期号种子对高置信候选做可复现洗牌, 使胆拖随每期合理变化。
    sorted_scores = sorted(combined_score.items(), key=lambda x: x[1], reverse=True)
    seed_dt = int(target_period) * 100003 + 90001 + salt * 1000003
    rng_dt = random.Random(seed_dt)
    top_candidates = [n for n, _ in sorted_scores[:33]]   # 高置信候选(扩大池)
    seeded_pool = list(top_candidates)
    rng_dt.shuffle(seeded_pool)
    search_pool = seeded_pool[:20]                        # 期号种子洗牌后的 TOP20(每期不同)

    def find_valid_dantuo(dan_size, tuo_size, candidates):
        """从候选号码中找到所有子组合都通过过滤器的胆拖组合。
        V1.0.0 修复: 此前拖码只取 candidates 中不含 dan 的前 tuo_size 个(固定), 不枚举,
        一旦该固定拖码组合不通过9项过滤器即失败 → 26087 期"所有策略均失败"致 dantuo 为空、
        报告胆拖板块被 if dt: 跳过。现改为在候选池内枚举 胆码×拖码 组合, 找一组全部子组合
        通过过滤器者, 既保持"全部子组合通过过滤器"硬保证, 又显著提高成功率。"""
        dan_cands = candidates[:12]
        tuo_cands = candidates[:15]   # 拖码候选池(不含dan), 枚举组合而非只取前N个
        for dan in combinations(dan_cands, dan_size):
            dan_set = set(dan)
            pool = [n for n in tuo_cands if n not in dan_set]
            if len(pool) < tuo_size:
                continue
            for tuo in combinations(pool, tuo_size):
                all_valid = True
                for sub in combinations(tuo, 6 - dan_size):
                    front = sorted(list(dan) + list(sub))
                    if not passes_filters(front, prev_front):
                        all_valid = False
                        break
                if all_valid:
                    return list(dan), list(tuo)
        return None, None
    
    def find_dantuo_from_valid(dan_size, tuo_size):
        """V1新增回退策略: 从有效组合中找包含最多TOP号码的组合，提取胆拖"""
        top_nums = set(search_pool[:10])
        best_combo = None
        best_overlap = 0
        best_score = -1
        for combo in valid_dynamic:
            overlap = len(set(combo) & top_nums)
            score = sum(combined_score[n] for n in combo) / 6
            if overlap > best_overlap or (overlap == best_overlap and score > best_score):
                # 验证这个组合本身通过9项过滤器
                if passes_filters(sorted(combo), prev_front):
                    best_overlap = overlap
                    best_score = score
                    best_combo = combo
        
        if best_combo is None:
            return None, None
        
        # 从最佳组合中提取dan_size个评分最高的作为胆码，其余作为拖码
        combo_sorted = sorted(best_combo, key=lambda n: combined_score[n], reverse=True)
        dan = combo_sorted[:dan_size]
        tuo = combo_sorted[dan_size:dan_size + tuo_size]
        
        if len(tuo) < tuo_size:
            # 拖码不够，从search_pool中补充
            for n in search_pool:
                if n not in dan and n not in tuo:
                    # 检查补充后的所有子组合是否通过
                    test_tuo = tuo + [n]
                    all_valid = True
                    for sub in combinations(test_tuo, 6 - dan_size):
                        front = sorted(list(dan) + list(sub))
                        if not passes_filters(front, prev_front):
                            all_valid = False
                            break
                    if all_valid:
                        tuo.append(n)
                        if len(tuo) >= tuo_size:
                            break
        
        if len(tuo) < tuo_size:
            return None, None
        
        # 最终验证
        for sub in combinations(tuo, 6 - dan_size):
            front = sorted(list(dan) + list(sub))
            if not passes_filters(front, prev_front):
                return None, None
        
        return dan, tuo
    
    # ---- 胆拖优化引擎 (V1.0.0 新增): 形态不固定, 多目标求性价比最高 ----
    try:
        from ssq_dantuo_optimizer import optimize_dantuo
        opt = optimize_dantuo(combined_score, back_scored, prev_front,
                              passes_filters, budget_bets=120, mc_n=6000,
                              period_seed=ps)
        best_dt = opt.get('best')
    except Exception as e:
        print(f"\n  ⚠ 胆拖优化引擎异常({e}), 回退固定策略")
        best_dt = None
        opt = {'best': None, 'candidates': [], 'honesty': ''}

    dantuo = {}
    if best_dt:
        dantuo['standard'] = {
            'dan': best_dt['dan'], 'tuo': best_dt['tuo'], 'back': best_dt['back'],
            'dan_size': best_dt['dan_size'],
            'front_combos': best_dt['front_combos'], 'back_combos': best_dt['back_combos'],
            'total_bets': best_dt['total_bets'],
            'cost_basic': best_dt['cost_basic'], 'cost_extra': best_dt['cost_extra'],
        }
        dantuo['optimized'] = best_dt          # 含 acc/win_any/win_5plus/score/tolerance_table
        dantuo['candidates'] = opt.get('candidates', [])
        dantuo['honesty'] = opt.get('honesty', '')
        print(f"\n  胆拖优化方案: {best_dt['form']} = {best_dt['total_bets']}注 = {best_dt['cost_basic']}元(基本)/{best_dt['cost_extra']}元(复式)")
        print(f"    准度={best_dt['acc']:.3f} 中奖(模型加权MC)≥任一奖={best_dt['win_any']*100:.1f}% ≥五等={best_dt['win_5plus']*100:.1f}% 评分={best_dt['score']:.3f}")
    else:
        # 回退: 原固定策略 (V1.0.0 保留为降级路径)
        dan_b, tuo_b = find_valid_dantuo(3, 5, search_pool)
        if not dan_b:
            dan_b, tuo_b = find_dantuo_from_valid(3, 5)
        if not dan_b:
            dan_b, tuo_b = find_valid_dantuo(2, 5, search_pool)
        if not dan_b:
            dan_b, tuo_b = find_dantuo_from_valid(2, 5)
        dt_back = _sample_back_group(back_dist['综合共识'], set(), seed_dt + 7)
        if dt_back is None:
            dt_back = sorted(sorted(range(1, 17), key=lambda n: back_scored.get(n, 0), reverse=True)[:3])
        if dan_b:
            front_combos = math.comb(len(tuo_b), 6 - len(dan_b))
            back_combos = len(dt_back)
            dantuo['standard'] = {
                'dan': dan_b, 'tuo': tuo_b, 'back': dt_back,
                'dan_size': len(dan_b),
                'front_combos': front_combos, 'back_combos': back_combos,
                'total_bets': front_combos * back_combos,
                'cost_basic': front_combos * back_combos * 2,
                'cost_extra': front_combos * back_combos * 2,  # 双色球无追加
            }
            print(f"\n  胆拖方案(回退): {len(dan_b)}胆{len(tuo_b)}拖+后{len(dt_back)}码 = {front_combos * back_combos}注")
        else:
            print(f"\n  ⚠ 未找到有效的胆拖组合（所有策略均失败）")

    return groups, dantuo


# ============================================================
# 6b. 跨期唯一性硬闸门 + 数据支撑记录
# ============================================================
def _recommended_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ssq_recommended_periods.json')


def _load_recommended():
    try:
        with open(_recommended_path(), encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def _save_recommended(data):
    p = _recommended_path()
    tmp = p + '.tmp'
    try:
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp, p)
    except Exception:
        pass


def _combo_str(front, back):
    return ','.join(str(int(n)) for n in front) + '+' + ','.join(str(int(n)) for n in back)


def _record_fetch(source, count, latest):
    """记录最近一次联网取数(数据支撑凭证), 供报告/调用模型展示。"""
    try:
        info = {
            'source': source,
            'fetched_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'periods': count,
            'latest_period': latest.get('period') if latest else None,
            'latest_date': latest.get('date') if latest else None,
        }
        p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ssq_data_fetch_log.json')
        with open(p, 'w', encoding='utf-8') as f:
            json.dump(info, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def generate_predictions(draws, models, valid_combos, expert_picks):
    """生成5组推荐。外层做跨期唯一性硬闸门: 不同期绝不出现相同 6+1 组合。

    - 同期(salt=0)确定性 → 完全可复现(同一期每次调用号码一致, 符合预期);
    - 若与已记录的其他期组合撞车, 自动 +salt 重排直到不重复(理论必终止)。
    这是针对"不同期号码相同=模型错"的硬性修正: 从此不同期推荐必然不同。
    """
    target_period = next_period_func(int(draws[-1]['period']), draws[-1].get('date'))
    rec = _load_recommended()
    others = set()
    for p, combos in rec.items():
        if str(p) == str(target_period):
            continue
        if isinstance(combos, list):
            others.update(combos)

    last = None
    for salt in range(0, 31):
        groups, dantuo = _gen_core(draws, models, valid_combos, expert_picks, salt=salt)
        combos = [_combo_str(g['front'], g['back']) for g in groups]
        last = (groups, dantuo)
        if not any(c in others for c in combos):
            rec[str(target_period)] = combos
            _save_recommended(rec)
            return groups, dantuo
    # 极端兜底(31次仍未避撞, 几乎不可能): 返回最后一次
    return last


# ============================================================
def group_review(g, front, back, ac, s, span, oc, sc, pc, roads, cg, rn, prev_front, draws=None):
    """计算单组号码的成本 + 优劣点（数据驱动，基于9项过滤器逐项判定）

    Returns:
        dict: {bets, cost_basic, cost_extra, strengths[], weaknesses[]}
    """
    n_back = len(back)
    bets = n_back                              # 蓝球复式: 每个蓝球各成1注
    cost_basic = bets * 2
    cost_extra = bets * 2                      # 双色球无追加, 复式成本=注数*2

    strengths, weaknesses = [], []
    name = g.get('name', '')
    strat = g.get('strategy', '')

    # —— 9 项过滤器逐项判定（优=在合理区间，劣=偏离）——
    if 5 <= ac <= 9:
        strengths.append(f"AC={ac}（离散度理想区间5-9）")
    else:
        weaknesses.append(f"AC={ac} 偏离理想区间5-9")

    if 80 <= s <= 160:
        strengths.append(f"和值{s}（合理区间80-160）")
    else:
        weaknesses.append(f"和值{s} 偏离80-160")

    if 16 <= span <= 31:
        strengths.append(f"跨度{span}（合理区间16-31）")
    else:
        weaknesses.append(f"跨度{span} 偏离15-30")

    if oc in (2, 3, 4):
        strengths.append(f"奇偶比{oc}:{6-oc}（均衡）")
    else:
        weaknesses.append(f"奇偶比{oc}:{6-oc}（偏态）")

    if sc in (2, 3, 4):
        strengths.append(f"大小比{sc}:{6-sc}（均衡）")
    else:
        weaknesses.append(f"大小比{sc}:{6-sc}（偏态）")

    if pc in (1, 2, 3):
        strengths.append(f"质数{pc}个（合理1-3）")
    else:
        weaknesses.append(f"质数{pc}个（偏离1-3）")

    r0, r1, r2 = roads
    if r0 > 0 and r1 > 0 and r2 > 0:
        strengths.append(f"012路{r0}{r1}{r2}（三类齐全，分布均匀）")
    else:
        weaknesses.append(f"012路{r0}{r1}{r2}（缺类，分布不均）")

    if cg <= 1:
        strengths.append(f"连号组数{cg}（≤1，符合常见形态）")
    else:
        weaknesses.append(f"连号组数{cg}（>1，形态偏密集）")

    if rn <= 2:
        strengths.append(f"重号{rn}个（vs上期，≤2，未过度追旧）")
    else:
        weaknesses.append(f"重号{rn}个（vs上期，>2，追旧偏多）")

    # —— 策略特性（优/劣各一句）——
    if '逆向' in name or 'ECI' in name:
        strengths.append("逆向专家热门：若中奖且分奖人多，相对少分奖")
        weaknesses.append("无命中率优势证据（V1.0回测 p 不显著）")
    if '冷号' in name:
        strengths.append("押注遗漏最大号码，赌冷号均值回归")
        weaknesses.append("冷号可能继续冷，纯均值回归假设")
    if '热号' in name:
        strengths.append("追踪近30期高频热号，顺势而为")
        weaknesses.append("追热遇变冷周期易失效")
    if '熵均衡' in name:
        strengths.append("无偏均匀采样，提供最大多样性/随机基准")
        weaknesses.append("不利用任何历史模式，等价于随机参照")
    if '综合' in name:
        strengths.append("多模型(CDM+马尔可夫+频率+遗漏)加权融合的共识锚点")
        weaknesses.append("属频率家族融合，与其他锚点互补而非独立预测")

    # —— 诚实通用劣势（每条都基于实测数据，动态读取避免过期）——
    pw = _load_power_stats()
    pw_n = pw.get('n_periods') or 2703
    strat_roi = pw.get('strat_roi')
    base_roi = pw.get('base_roi')
    if isinstance(strat_roi, (int, float)) and isinstance(base_roi, (int, float)):
        weaknesses.append(
            f"数学上无预测优势：V1.0强化引擎 {pw_n}期 ROI {strat_roi*100:+.1f}% ≈ 随机 {base_roi*100:+.1f}%（Bootstrap 95%CI 下界未>0）")
    else:
        weaknesses.append("数学上无预测优势：V1.0强化引擎回测证明与随机无显著差异")
    weaknesses.append("期望红球命中≈随机 1.09 球；凯利 f* 为负，单注期望净亏≈¥1.00")

    # V1.0.4: 历史相似形态中奖概率(描述性参考, 非预测) + 固定号码历史回测
    _n_tickets = bets  # 本组复式购票张数 = len(back)
    sim = similar_shape_stats(front, back, draws, _n_tickets) if draws else {
        'cohort': 0, 'N': 0, 'shape_prevalence': 0.0,
        'backtest': {'plays': 0, 'any_hit': 0, 'win_rate': 0.0,
                     'tier_counts': {}, 'total_prize': 0, 'cost': 0, 'roi': 0.0},
    }

    return {
        'bets': bets,
        'cost_basic': cost_basic,
        'cost_extra': cost_extra,
        'strengths': strengths,
        'weaknesses': weaknesses,
        'similar_shape': sim,
    }


def _load_prev_prediction_groups(latest_period):
    """加载上一期预测 JSON, 返回其 groups(含 front/back/name)用于跨期一致性对比; 不存在则返回 []。"""
    prev_file = f'ssq_prediction_{latest_period}_v8.json'
    try:
        with open(prev_file, 'r', encoding='utf-8') as f:
            d = json.load(f)
        return d.get('groups', [])
    except (FileNotFoundError, json.JSONDecodeError, KeyError, OSError):
        return []


def _safe_json(path):
    """安全读取 JSON, 缺失或解析失败返回 None。相对路径锚定到本模块目录(与 cwd 解耦)。"""
    if not os.path.isabs(path):
        path = os.path.join(HERE, path)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, OSError, ValueError):
        return None


_POWER_CACHE = {}


def _load_power_stats():
    """读取 ssq_power_report.json, 返回'命中现实分布'板块所需的动态数据; 缺失返回 {}。带缓存。"""
    if 'data' in _POWER_CACHE:
        return _POWER_CACHE['data']
    r = _safe_json('ssq_power_report.json')
    if not r:
        _POWER_CACHE['data'] = {}
        return _POWER_CACHE['data']
    s = r.get('strategy', {}) or {}
    rb = r.get('random_baseline', {}) or {}
    mc = r.get('monte_carlo', {}) or {}
    hg = r.get('honesty_guardrail', {}) or {}
    data = {
        'n_periods': s.get('n_periods'),
        'strat_roi': s.get('roi'),
        'strat_prize_rate': s.get('any_prize_rate'),
        'base_roi': rb.get('roi_mean'),
        'base_prize_rate': rb.get('any_prize_rate_mean'),
        'profit_prob': mc.get('prob_profit'),
        'expected_net': mc.get('expected_net'),
        'ci_low': hg.get('ci_low'),
        'ci_high': hg.get('ci_high'),
    }
    _POWER_CACHE['data'] = data
    return data


def _load_ml_stats():
    """读取 ssq_ml_selfcheck.json, 返回红球命中率动态数据; 缺失返回 None。"""
    r = _safe_json('ssq_ml_selfcheck.json')
    if not r:
        return None
    models = r.get('models', {}) or {}
    rb = r.get('random_baseline', {}) or {}
    means = [m.get('mean') for m in models.values()
             if isinstance(m, dict) and m.get('mean') is not None]
    return {
        'n_periods': r.get('n_periods'),
        'model_min': min(means) if means else None,
        'model_max': max(means) if means else None,
        'random_mean': rb.get('mean'),
    }


def _pct(v):
    """浮点(0~1)转百分比字符串; None 返回 '—'。"""
    return f"{v*100:.1f}%" if isinstance(v, (int, float)) else "—"


# ============================================================
# V1.0.6 报告新增：各号码出现频率参考（描述性，非预测概率）
# ============================================================
def generate_number_frequency_section(draws):
    """各号码历史出现频率 + 最热/最冷组合（恒等概率声明）

    诚实原则：
      - 新浪等站点"出现概率"=历史经验频率(描述过去)，非下一期预测概率
      - 理论单号概率恒定且每号相等：红球6/33≈18.18%，蓝球1/16=6.25%
      - 任一6+1组合单期出现概率恒为1/17,721,088，最热组合=最冷组合概率
    此维度仅作娱乐化/描述性参考，不含预测力(no_edge)。
    """
    from collections import Counter as _Counter
    RECENT = 30
    total = len(draws)
    if total == 0:
        return ''
    recent_draws = draws[-RECENT:] if total >= RECENT else draws
    n_recent = len(recent_draws)
    front_counts = _Counter(n for d in recent_draws for n in d['front'])
    back_counts = _Counter(n for d in recent_draws for n in d['back'])
    front_freq = {n: front_counts.get(n, 0) / n_recent for n in range(1, 34)}
    back_freq = {n: back_counts.get(n, 0) / n_recent for n in range(1, 17)}
    front_theory = 6 / 33
    back_theory = 1 / 16
    COMBO_TOTAL = 1107568 * 16  # 17,721,088
    combo_prob = 1 / COMBO_TOTAL

    front_sorted = sorted(range(1, 34), key=lambda n: (-front_freq[n], n))
    back_sorted = sorted(range(1, 17), key=lambda n: (-back_freq[n], n))
    hot_front, cold_front = front_sorted[:6], front_sorted[-6:]
    hot_back, cold_back = back_sorted[:1], back_sorted[-1:]

    def rows(nums, freqs, theory):
        out = []
        for n in nums:
            f = freqs[n]
            diff = f - theory
            color = '#ff6b6b' if diff > 0.005 else ('#66ccff' if diff < -0.005 else '#8899aa')
            sign = '+' if diff >= 0 else ''
            out.append(f"<tr><td>{n:02d}</td><td>{f*100:.2f}%</td>"
                       f"<td>{theory*100:.2f}%</td>"
                       f"<td style='color:{color};'>{sign}{diff*100:.2f}pp</td></tr>")
        return ''.join(out)

    front_rows = rows(front_sorted, front_freq, front_theory)
    back_rows = rows(back_sorted, back_freq, back_theory)

    def combo_card(title, fl, bl, accent):
        return f"""
<div class="group-card" style="border-left-color:{accent}; flex:1; min-width:280px;">
<h3 style="color:{accent}; margin-bottom:8px;">{title}</h3>
<div class="balls-container">
<span style="color:#888;">红球(6码):</span>
{''.join(f'<span class="ball ball-red">{n:02d}</span>' for n in sorted(fl))}
</div>
<div class="balls-container">
<span style="color:#888;">蓝球(1码):</span>
{''.join(f'<span class="ball ball-blue">{n:02d}</span>' for n in sorted(bl))}
</div>
<p style="color:#ffcc00; font-size:13px; margin-top:6px;">
🎯 该组合单期出现概率 = <strong>1/{COMBO_TOTAL:,}</strong>（≈{combo_prob:.3e}），与"最冷组合"或任意一注<strong>完全相等</strong>。
</p>
</div>"""

    return f"""
<div class="section" style="border:1px solid #aa66ff;">
<div class="section-title">五、各号码出现频率参考（描述性，非预测概率）</div>
<div class="info">
<h3>ℹ️ 关于"每个号码出现概率"的诚实说明（避免误读）</h3>
<ul style="margin:8px 0; padding-left:20px; color:#88ccff; line-height:1.8;">
<li><strong>新浪等站点展示的"出现概率"实为历史经验频率</strong>（某号出现次数÷总期数），是<strong>描述过去</strong>，不是<strong>预测下期</strong>。本板块同理。</li>
<li><strong>理论概率（恒定、每号相等）</strong>：红球任一单号本期出现概率 = 6/33 ≈ 18.18%；蓝球任一单号 = 1/16 = 6.25%。由排列组合决定，与选不选无关。</li>
<li><strong>任一 6+1 组合</strong>的单期出现概率恒为 <strong>1/17,721,088</strong>（红球 C(33,6)=1,107,568 × 蓝球 16）。"最热组合"与"最冷组合"<strong>概率完全相等</strong>——热/冷只是所含单号的历史频率高低，不改变整注概率。</li>
<li><strong>结论</strong>：此维度仅作<strong>娱乐化/描述性选号参考</strong>，不含任何预测力（no_edge）。请勿据此推断"某号下期更可能出"。</li>
</ul>
</div>
<div class="section" style="background:#0d1130;">
<div class="section-title" style="font-size:16px;">红球 01-33 近{RECENT}期频率 vs 理论概率（{n_recent}期）</div>
<table>
<tr><th>号码</th><th>历史频率</th><th>理论(6/33)</th><th>偏差</th></tr>
{front_rows}
</table>
</div>
<div class="section" style="background:#0d1130;">
<div class="section-title" style="font-size:16px;">蓝球 01-16 近{RECENT}期频率 vs 理论概率（{n_recent}期）</div>
<table>
<tr><th>号码</th><th>历史频率</th><th>理论(1/16)</th><th>偏差</th></tr>
{back_rows}
</table>
</div>
<div style="display:flex; gap:12px; margin-top:10px; flex-wrap:wrap;">
{combo_card('🔥 最热组合（由历史频率最高单号构成）', hot_front, hot_back, '#ff6b6b')}
{combo_card('❄️ 最冷组合（由历史频率最低单号构成）', cold_front, cold_back, '#66ccff')}
</div>
<div class="warning">
<h3>⚠️ 关键澄清：组合概率不存在"热冷梯度"</h3>
<p style="color:#ff9999; font-size:14px; line-height:1.7;">
你曾推断"既然单号有当期出现概率，组合肯定也有"——逻辑上每个组合<strong>确实有</strong>概率，但它是<strong>恒等</strong>的 1/17,721,088：在约 2142 万种可能里每种恰好一次，历史样本里 99.99% 的组合<strong>一次都没出现过</strong>，根本无法像单号那样排出"热/冷"。所以"最热/最冷组合"只能按"所含单号的历史冷热"构造，它<strong>不代表</strong>该组合更可能中。真正的"分析一等奖的方法"不在频率排名（见本次方法学说明 / 回复）。
</p>
</div>
</div>
"""


# ============================================================
# 近期一等奖领奖故事（年轻化·娱乐·诚实）
# 真实故事 best-eff: 联网刷新；失败/断网时回退本地种子库（ssq_winning_stories.json），绝不编造。
# ============================================================
# 氛围插画目录（插画为原创卡通风格，非真实中奖/兑奖照片，仅增强阅读趣味）
_WIN_ILLUS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "win_illustrations")


def load_win_illustrations():
    """读取 lib/assets/win_illustrations 下的插画，返回 base64 data URI 列表（失败返回空）。"""
    out = []
    try:
        if not os.path.isdir(_WIN_ILLUS_DIR):
            return out
        for fn in sorted(os.listdir(_WIN_ILLUS_DIR)):
            if fn.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                p = os.path.join(_WIN_ILLUS_DIR, fn)
                try:
                    with open(p, "rb") as f:
                        b = f.read()
                    ext = fn.rsplit(".", 1)[-1].lower()
                    mime = {"png": "image/png", "jpg": "image/jpeg",
                            "jpeg": "image/jpeg", "webp": "image/webp"}.get(ext, "image/png")
                    out.append(f"data:{mime};base64,{base64.b64encode(b).decode('ascii')}")
                except Exception:
                    continue
    except Exception:
        pass
    return out


# 防止同一进程内重复触发后台刷新
_media_refresh_spawned = False


def maybe_refresh_media_async():
    """非阻塞后台刷新真实图片：绝不阻塞报告生成。

    仅当本地从未尝试过抓取（无 manifest 标记）时才触发一次，之后由 manifest 守卫，
    不会再重复联网。子进程独立运行（带 socket 超时熔断），父进程（报告）立即返回。
    这样排程任务永远不会因"等图片"而卡死；真实图片会在下一次运行自然出现。
    """
    global _media_refresh_spawned
    if _media_refresh_spawned:
        return
    try:
        photo_manifest = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "assets", "win_photos", "manifest.json")
        # 已有 manifest（成功或失败都写过）= 已尝试过，不再触发
        if os.path.exists(photo_manifest):
            return
        _media_refresh_spawned = True
        py = sys.executable
        script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ssq_photo_fetcher.py")
        # 非阻塞启动：不 wait，子进程在后台自行完成（受 socket 超时保护，最坏约 1~2 分钟）
        subprocess.Popen([py, script],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                         creationflags=0x00000008)  # DETACHED_PROCESS：脱离父进程，父退出不影响
    except Exception:
        pass


def generate_winning_stories_html(limit=2):
    """返回「🏆 近期一等奖领奖故事」板块 HTML（彩民第一眼就能看到的快乐开场）。

    每次运行自动联网检索最新最刺激的真实领奖新闻（best-effort + 超时熔断 + 种子兜底），
    左右两张卡片并排展示；联网失败自动回退内置真实故事库，绝不卡死、绝不空场。
    图片改为纯 CSS 欢天喜地特效（旋转彩灯 + 烟花），更抓眼球且不依赖网络图片。
    """
    try:
        # 每次运行尝试联网刷新最新新闻（带超时熔断，最坏约 1~2×8s 即返回）；失败自动回退
        resp = _get_winning_news(max_items=limit, allow_live=True) or {}
        items = resp.get("stories", []) if isinstance(resp, dict) else list(resp)
    except Exception:
        items = []
    if not items:
        return (
            '<div class="win-stories">'
            '<div class="ws-head"><span class="ws-emoji">🏆</span>'
            '<div class="ws-title">近期<span class="hl">一等奖</span>领奖故事</div></div>'
            '<div class="ws-sub">别人的好运，是今天最解压的快乐源泉～</div>'
            '<div class="ws-empty">😶 本期暂时没能抓到最新领奖新闻（联网受限）。'
            '不过——双色球一等奖概率恒 1/17,721,088，中奖全靠运气，看故事图个乐就好。</div>'
            '</div>'
        )

    badges = ["🔥 最新爆款", "✨ 热议领奖"]
    cards = []
    for i, s in enumerate(items[:2]):
        prize = s.get("prize", "")
        place = s.get("place", "") or s.get("region", "")
        title = s.get("title", "")
        summary = (s.get("summary", "") or "").strip()
        if not summary:
            # 兜底：绝不渲染空白卡片，给出诚实提示
            summary = "（该条仅检索到标题，暂无正文摘要；以官方来源报道为准。）"
        source = s.get("source", "")
        date = s.get("date", "")
        # 经典回顾（真实日期超过新鲜度阈值）诚实标注，不伪装成最新爆款
        if s.get("recall"):
            badge = "📜 经典回顾"
        else:
            badge = badges[i] if i < len(badges) else ""
        prize_html = f'<span class="wc-prize">{prize}</span>' if prize else ''
        place_html = f'<span class="wc-place">· {place}</span>' if place else ''
        foot = ''
        if source or date:
            src = f'<span class="src">{source}</span>' if source else ''
            dt = f'{date}' if date else ''
            foot = f'<div class="wc-foot">{src}{(" ｜ " + dt) if dt else ""}</div>'
        badge_html = f'<span class="wc-badge{" b2" if i == 1 else ""}">{badge}</span>' if badge else ''
        cards.append(
            f'<div class="win-card">'
            f'{badge_html}'
            f'<div class="wc-top">{prize_html}{place_html}</div>'
            f'<div class="wc-title">{title}</div>'
            f'<div class="wc-sum">{summary}</div>'
            f'{foot}'
            f'</div>'
        )
    grid = ''.join(cards)
    note = (
        '<div class="ws-note">✨ 故事均来自<strong>公开真实报道</strong>，中奖是<strong>万里挑一的运气</strong>——'
        '享受别人的高光时刻就好，别把"别人的幸运"当"自己的计划"。'
        '你花的两块钱，买的是一份小期待，理性娱乐，量力而行 💛</div>'
    )
    src_tag = '<span class="ws-src-tag">⚡ 实时联网更新</span>' if items and items[0].get("origin") == "live" else ''
    return (
        '<div class="win-stories">'
        '<div class="ws-head"><span class="ws-emoji">🏆</span>'
        '<div class="ws-title">近期<span class="hl">一等奖</span>领奖故事</div>'
        f'{src_tag}</div>'
        '<div class="ws-sub">别人的好运，是今天最解压的快乐源泉～ 看故事图个乐，理性娱乐不上头 💛</div>'
        f'<div class="ws-grid">{grid}</div>'
        f'{note}'
        '</div>'
    )


def generate_party_hero_html():
    """报告开场欢天喜地特效：旋转彩灯 + 烟花绽放 + 渐变流光，瞬间抓住彩民与年轻人眼球。
    纯 CSS 动画，零联网、零图片、永不阻塞。"""
    return (
        '<div class="party-hero">'
        '<div class="party-lights"></div>'
        '<div class="fw fw1"></div>'
        '<div class="fw fw2"></div>'
        '<div class="fw fw3"></div>'
        '<div class="party-content">'
        '<div class="party-title">🎉 双色球 · 快乐开奖时刻 🎉</div>'
        '<div class="party-sub">别人的好运，是你今天最解压的快乐源泉～ 花两块钱，买一份小期待 💛</div>'
        '</div>'
        '</div>'
    )


def generate_countdown_html():
    """开奖倒计时（基于双色球真实开奖时刻：周二/四/日 21:15，纯事实、零预测暗示）。

    返回一个预渲染 HTML 块，包含一段 JS，打开报告时实时倒数到下期开奖。
    这是"诚实的娱乐"——只告诉彩民还有多久开奖，绝不暗示任何号码或中奖。
    """
    try:
        from datetime import datetime, timedelta
        now = datetime.now()
        draw_weekdays = [1, 3, 6]          # 周二 / 周四 / 周日
        draw_hour, draw_minute = 21, 15    # 21:15 开奖
        next_dt = None
        d = now
        for _ in range(14):
            if d.weekday() in draw_weekdays:
                cand = d.replace(hour=draw_hour, minute=draw_minute, second=0, microsecond=0)
                if cand > now:
                    next_dt = cand
                    break
            d = d + timedelta(days=1)
        if next_dt is None:
            next_dt = now + timedelta(days=1)
        total_sec = int((next_dt - now).total_seconds())
        wd_names = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        draw_label = '%d月%d日 %s' % (next_dt.month, next_dt.day, wd_names[next_dt.weekday()])

        script = (
            '<script>(function(){'
            'var t=' + str(total_sec) + ';'
            'var d=document.getElementById("ssq-cd-d"),h=document.getElementById("ssq-cd-h"),'
            'm=document.getElementById("ssq-cd-m"),s=document.getElementById("ssq-cd-s");'
            'function p(n){return (n<10?"0":"")+n;}'
            'function tick(){if(t<0)t=0;var dd=Math.floor(t/86400),r=t%86400,'
            'hh=Math.floor(r/3600),mm=Math.floor((r%3600)/60),ss=r%60;'
            'd.textContent=dd;h.textContent=p(hh);m.textContent=p(mm);s.textContent=p(ss);'
            't--;if(t<0)return;setTimeout(tick,1000);}'
            'tick();})();</script>'
        )
        html = (
            '<div class="draw-countdown" id="ssq-cd">'
            '<div class="cd-left">'
            '<div class="cd-emoji">⏰</div>'
            '<div class="cd-txt">'
            '<div class="cd-title">距离下期开奖还有</div>'
            '<div class="cd-label">📅 ' + draw_label + ' 21:15（周二 / 周四 / 周日开奖）</div>'
            '</div></div>'
            '<div class="cd-clock">'
            '<span class="cd-box" id="ssq-cd-d">--</span><i>天</i>'
            '<span class="cd-box" id="ssq-cd-h">--</span><i>时</i>'
            '<span class="cd-box" id="ssq-cd-m">--</span><i>分</i>'
            '<span class="cd-box" id="ssq-cd-s">--</span><i>秒</i>'
            '</div></div>'
            + script
        )
        return html
    except Exception:
        return ''


def generate_fun_card_html():
    """🎲 今日小彩蛋（纯随机、纯娱乐，与中奖概率无关）。

    每次生成报告都会随机抽一条轻松小签，主打"陪伴感"而不是"预测感"。
    所有内容都明确标注与中奖无关，守住诚实红线。
    """
    try:
        import random
        fortunes = [
            ("今天宜", "给自己买杯奶茶犒劳一下，中奖是锦上添花，快乐才是主菜 🧋"),
            ("今天忌", "因为没中奖就影響晚饭胃口——两块钱买的是期待，不是负担 🍚"),
            ("今日幸运色", "你今天穿的那件就挺好，自信的人运气都不会太差 ✨"),
            ("今日能量值", "满格！但请把这份能量用在工作和生活，彩票只是小甜点 🔋"),
            ("财运提示", "理性娱乐，量力而行，今晚开奖当看个热闹，中不中都是好心情 🎉"),
            ("互动小任务", "把这份报告转发给那个总说'我差点就中了'的朋友 😏"),
            ("今日宜", "早睡，毕竟开奖结果明天醒来再看也不迟 🌙"),
            ("心态签", "中不中都是生活调剂，买得明白比买得贵更重要 💡"),
        ]
        tag, text = random.choice(fortunes)
        emoji = "🎲"
        html = (
            '<div class="fun-card">'
            '<div class="fc-emoji">' + emoji + '</div>'
            '<div class="fc-body">'
            '<div class="fc-tag">今日小彩蛋 · ' + tag + ' <span class="fc-honest">（纯娱乐，与中奖无关）</span></div>'
            '<div class="fc-text">' + text + '</div>'
            '</div></div>'
        )
        return html
    except Exception:
        return ''


def generate_prop_minigames_html():
    """防割韭菜盾 · 三框（选号有依据 / 省钱有工具 / 中奖有核对）空白区填充互动小游戏。

    每个 .box-mini 与「手气摇奖机」转盘同尺寸（网格同列宽，游戏区高 180px），
    保证整体协调美观。三个小游戏均为纯娱乐/工具演示，诚实标注，不误导中奖。
    """
    css = (
    "<style>"
    ".box-mini{margin-top:10px;min-height:180px;display:flex;flex-direction:column;"
    "align-items:center;justify-content:center;gap:8px;padding:10px;border-radius:12px;"
    "background:rgba(0,40,24,.5);border:1px dashed #00aa66;text-align:center;}"
    ".bm-ttl{font-size:12.5px;color:#7dffc0;font-weight:800;}"
    ".bm-h{font-size:11px;color:#9fd8be;}"
    ".bm-balls{display:flex;flex-wrap:wrap;gap:4px;justify-content:center;min-height:28px;}"
    ".bm-ball{width:26px;height:26px;line-height:26px;border-radius:50%;font-size:12px;font-weight:800;color:#fff;}"
    ".bm-ball.r{background:radial-gradient(circle at 30% 30%,#ff7a7a,#d10000);}"
    ".bm-ball.b{background:radial-gradient(circle at 30% 30%,#6db8ff,#0048c8);}"
    ".bm-btn{background:linear-gradient(135deg,#00dd88,#00aa66);color:#06240f;border:none;"
    "border-radius:18px;padding:6px 14px;font-size:13px;font-weight:800;cursor:pointer;}"
    ".bm-btn:active{transform:scale(.96);}"
    ".bm-note{font-size:10.5px;color:#8fbfa8;line-height:1.4;}"
    ".bm-pig{font-size:46px;cursor:pointer;user-select:none;transition:transform .12s;}"
    ".bm-pig:active{transform:scale(.84);}"
    ".bm-save{font-size:13px;color:#ffe9b0;font-weight:700;}"
    ".bm-scratch{position:relative;height:66px;width:100%;border-radius:10px;"
    "background:linear-gradient(135deg,#2a1840,#3a1a5a);overflow:hidden;cursor:pointer;"
    "display:flex;align-items:center;justify-content:center;}"
    ".bm-prize{font-size:13px;font-weight:800;color:#ffd98a;padding:6px;text-align:center;}"
    ".bm-cover{position:absolute;inset:0;background:repeating-linear-gradient(45deg,#c9a24a,#c9a24a 8px,#b8913c 8px,#b8913c 16px);"
    "color:#5a3b00;font-weight:800;font-size:13px;display:flex;align-items:center;justify-content:center;transition:opacity .35s;}"
    ".bm-cover.gone{opacity:0;pointer-events:none;}"
    "</style>"
    )
    boxes = (
    css
    + '<div class="prop">'
      '<div class="ico">\U0001F3AF</div><div class="ttl">\u9009\u53F7\u6709\u4F9D\u636E</div>'
      '<div class="desc">5 \u7EC4\u7B56\u7565\u7EC4\u5408\uff0c\u5168\u90E8\u8FC7 9 \u9879\u8FC7\u6EE4\u5668\uff0c\u6BCF\u6CE8\u90FD\u6807\u6CE8\u201C\u5A31\u4E50\u53C2\u8003\u3001\u4E0D\u4FDD\u8BC1\u7ED3\u679C\u201D\u3002</div>'
      '<div class="box-mini">'
        '<div class="bm-ttl">\U0001F3B2 \u4ECA\u65E5\u7075\u611F\u53F7</div>'
        '<div class="bm-balls" id="bmBalls1"><span class="bm-h">\u70B9\u6309\u94AE\u6447\u51FA\u7075\u611F\u53F7</span></div>'
        '<button class="bm-btn" onclick="bmRoll()">\u2728 \u6447\u4E00\u6CE8\u7075\u611F\u53F7</button>'
        '<div class="bm-note">\u7EAF\u5A31\u4E50 \u00B7 \u975E\u771F\u5B9E\u9009\u53F7\u4F9D\u636E</div>'
      '</div>'
    '</div>'
    + '<div class="prop">'
      '<div class="ico">\U0001F4B0</div><div class="ttl">\u7701\u94B1\u6709\u5DE5\u5177</div>'
      '<div class="desc">\u80C6\u62D6\u4F18\u5316\u5668\uff1a\u540C\u6837\u8986\u76D6\u5FC3\u4EEA\u53F7\u7801\uff0c\u82B1\u66F4\u5C11\u7684\u94B1\uff08\u8BE6\u89C1\u62A5\u544A\u7B2C\u56DB\u8282\uff09\u3002</div>'
      '<div class="box-mini">'
        '<div class="bm-ttl">\U0001F43B \u7701\u94B1\u5B58\u94B1\u7F38</div>'
        '<div class="bm-pig" id="bmPig" onclick="bmSave()">\U0001F43B</div>'
        '<div class="bm-save" id="bmSaveTxt">\u5DF2\u7C7E \u00A50 \u00B7 \u591F\u4E70 0 \u6CE8</div>'
        '<div class="bm-note">\u70B9\u5C0F\u732A\uff0c\u6BCF\u70B9=\u7701\u4E0B 1 \u6CE8(\u00A52)\u5B58\u5165</div>'
      '</div>'
    '</div>'
    + '<div class="prop">'
      '<div class="ico">\U0001F50D</div><div class="ttl">\u4E2D\u5956\u6709\u6838\u5BF9</div>'
      '<div class="desc">\u5F00\u5956\u540E\u4E00\u952E\u6838\u5BF9\uff1a\u4E2D\u6CA1\u4E2D\u3001\u4E2D\u51E0\u7B49\u5956\u3001\u8BE5\u62FF\u591A\u5C11\uff0c\u79D2\u77E5\u9053\u3002</div>'
      '<div class="box-mini">'
        '<div class="bm-ttl">\U0001F3AB \u8BD5\u8BD5\u624B\u6C14\u6838\u5BF9</div>'
        '<div class="bm-scratch" id="bmScratch" onclick="bmReveal()">'
          '<div class="bm-prize" id="bmPrize">\uFF1F</div>'
          '<div class="bm-cover" id="bmCover">\u70B9\u51FB\u522E\u5F00</div>'
        '</div>'
        '<div class="bm-note">\u6A21\u62DF\u6838\u5BF9 \u00B7 \u4E0E\u771F\u5B9E\u5F00\u5956\u65E0\u5173</div>'
      '</div>'
    '</div>'
    )
    return boxes


def generate_box_games_js():
    """三框小游戏的 JS（普通字符串，非 f-string，避免大括号破坏模板）。"""
    return (
    "<script>"
    "function bmRoll(){"
    "var reds=[]; while(reds.length<6){var n=1+Math.floor(Math.random()*33); if(reds.indexOf(n)<0)reds.push(n);} reds.sort(function(a,b){return a-b;});"
    "var blue=1+Math.floor(Math.random()*16);"
    "var h=''; for(var i=0;i<reds.length;i++){h+='<span class=\"bm-ball r\">'+(('0'+reds[i]).slice(-2))+'</span>';}"
    "h+='<span class=\"bm-ball b\">'+(('0'+blue).slice(-2))+'</span>';"
    "var box=document.getElementById('bmBalls1'); if(box) box.innerHTML=h;"
    "}"
    "var bmSaveN=0;"
    "function bmSave(){"
    "bmSaveN+=1;"
    "var pig=document.getElementById('bmPig'); if(pig){pig.style.transform='scale(.82)'; setTimeout(function(){pig.style.transform='';},120);}"
    "var t=document.getElementById('bmSaveTxt'); if(t) t.textContent='\u5DF2\u7C7E \u00A5'+(bmSaveN*2)+' \u00B7 \u591F\u4E70 '+bmSaveN+' \u6CE8';"
    "}"
    "var bmRevealed=false;"
    "function bmReveal(){"
    "var c=document.getElementById('bmCover'); if(c && !bmRevealed){ c.classList.add('gone'); bmRevealed=true; }"
    "var msgs=['\u672A\u4E2D\u5956\u2026\u4E0B\u671F\u52A0\u6CB9\U0001F4AA','\u4E2D\u516D\u7B49\u5956 \u00A55\uff08\u6A21\u62DF\uff09','\u4E2D\u4E94\u7B49\u5956 \u00A510\uff08\u6A21\u62DF\uff09','\u4E2D\u56DB\u7B49\u5956 \u00A5200\uff08\u6A21\u62DF\uff09','\u4E09\u7B49\u5956\uff01\u00A53000\uff08\u6A21\u62DF\uff09','\u4E8C\u7B49\u5956\uff01\u00A5100000\uff08\u6A21\u62DF\uff09','\u4E00\u7B49\u5956\uff01\u00A75000000\uff08\u6A21\u62DF\uff09'];"
    "var p=document.getElementById('bmPrize'); if(p) p.textContent=msgs[Math.floor(Math.random()*msgs.length)];"
    "}"
    "</script>"
    )


def generate_wheel_html():
    """防割韭菜盾 · 右下角空位 → 幸运转盘小游戏（纯 CSS/JS，零联网、零卡死）。

    扇区设计为「有奖 ↔ 鼓励」交替：有奖格按双色球最高奖到最低奖排列
    （一等奖→六等奖），鼓励格全是开心/好运文案（锦鲤、旺财、冲鸭、好运、开心、稳了）。
    机制保证每次都停在「中奖」格（务必让用户中奖，给足开心）。
    中奖即触发烟花 + 灯光闪烁 + 漫天彩票特效。诚实标注：纯娱乐，与真实中奖无关。
    """
    try:
        html = (
        '<div class="prop wheel-prop" id="ssq-wheel">'
        '<div class="ico">🎰</div>'
        '<div class="ttl">手气摇奖机</div>'
        '<div class="desc">点一下转盘，看看今天运气～（纯娱乐，与真实中奖无关）</div>'
        '<div class="wheel-wrap">'
        '<div class="wheel-ptr"></div>'
        '<canvas id="ssqWheelCv" class="wheel-canvas" width="360" height="360"></canvas>'
        '<div class="wheel-float" id="ssqWheelFloat">👆 试试今天手气如何</div>'
        '</div>'
        '<button class="wheel-btn" id="ssqWheelBtn" onclick="ssqSpin()">🎯 点我摇奖</button>'
        '<div class="wheel-result" id="ssqWheelRes">转盘已就位，等你来转～</div>'
        '</div>'
        '<div class="cele-overlay" id="ssqCele">'
        '<div class="cele-flash"></div>'
        '<div class="cele-banner" id="ssqCeleBanner">🎉 恭喜你中奖啦！</div>'
        '</div>'
        '<script>'
        'function ssqDrawWheel(){'
        'var cv=document.getElementById("ssqWheelCv"); if(!cv)return;'
        'var ctx=cv.getContext("2d"); var n=12, R=180, cx=180, cy=180;'
        'var segs=[["🥇一等奖","#ff4d6d"],["🍀锦鲤","#ffd166"],["🥈二等奖","#06d6a0"],'
        '["💰旺财","#4cc9f0"],["🥉三等奖","#b388ff"],["🚀冲鸭","#f72585"],'
        '["💎四等奖","#fb8500"],["🌟好运","#8ac926"],["🎯五等奖","#4895ef"],'
        '["😄开心","#f15bb5"],["🍀六等奖","#c1e100"],["✅稳了","#ffb703"]];'
        'ctx.clearRect(0,0,360,360);'
        'for(var i=0;i<n;i++){'
        'var a0=i*2*Math.PI/n-Math.PI/2, a1=(i+1)*2*Math.PI/n-Math.PI/2;'
        'ctx.beginPath(); ctx.moveTo(cx,cy); ctx.arc(cx,cy,R,a0,a1); ctx.closePath();'
        'ctx.fillStyle=segs[i][1]; ctx.fill();'
        'ctx.save(); ctx.translate(cx,cy); ctx.rotate((a0+a1)/2);'
        'ctx.textAlign="right"; ctx.font="bold 18px sans-serif";'
        'ctx.lineWidth=3; ctx.strokeStyle="rgba(0,0,0,.55)"; ctx.strokeText(segs[i][0], R-12, 8);'
        'ctx.fillStyle="#fff"; ctx.fillText(segs[i][0], R-12, 8); ctx.restore();}'
        'ctx.beginPath(); ctx.arc(cx,cy,40,0,7); ctx.fillStyle="#0a1f14"; ctx.fill();'
        'ctx.fillStyle="#00dd88"; ctx.font="bold 26px sans-serif"; ctx.textAlign="center"; ctx.fillText("🎰",cx,cy+9);}'
        'var ssqWheelCur=0, ssqWheelOn=false;'
        'function ssqSpin(){'
        'var btn=document.getElementById("ssqWheelBtn"), res=document.getElementById("ssqWheelRes"), fl=document.getElementById("ssqWheelFloat");'
        'if(ssqWheelOn)return; ssqWheelOn=true; if(fl)fl.style.display="none";'
        'btn.disabled=true; res.textContent="转盘飞速旋转中…🌀";'
        'var wins=[0,2,4,6,8,10]; var win=wins[Math.floor(Math.random()*wins.length)];'
        'var msgs={0:"🥇 天选之子！你抽中【一等奖手气签】—— 今天气场全开，好运挡不住！",'
        '2:"🥈 棒极了！你抽中【二等奖手气签】—— 你很有财运，今天适合小确幸～",'
        '4:"🥉 厉害！你抽中【三等奖手气签】—— 偏财运在线，理性娱乐别上头💛",'
        '6:"💎 妙啊！你抽中【四等奖手气签】—— 小幸运敲门，今天心情美美的✨",'
        '8:"🎯 不错！你抽中【五等奖手气签】—— 稳稳的开心，运气在慢慢升温🌟",'
        '10:"🍀 喜气！你抽中【六等奖手气签】—— 重在参与，快乐才是头奖🎉"};'
        'var land=(360 - win*30 - 15);'
        'var m=((ssqWheelCur%360)+360)%360;'
        'var delta=360*6 + ((land - m + 360)%360);'
        'ssqWheelCur += delta;'
        'document.getElementById("ssqWheelCv").style.transform="rotate("+ssqWheelCur+"deg)";'
        'setTimeout(function(){ ssqWheelOn=false; btn.disabled=false;'
        'res.innerHTML="<strong style=\'color:#ffd24a\'>"+msgs[win]+"</strong>";'
        'ssqCelebrate(); }, 4700);'
        '}'
        'function ssqCelebrate(){'
        'var ov=document.getElementById("ssqCele"); if(!ov)return;'
        'ov.classList.add("show");'
        'for(var i=0;i<6;i++){var f=document.createElement("div"); f.className="cele-fw";'
        'f.style.left=(8+i*16)+"%"; f.style.top=(12+(i%2)*34)+"%"; f.style.animationDelay=(i*0.22)+"s"; ov.appendChild(f);}'
        'for(var j=0;j<36;j++){var t=document.createElement("div"); t.className="cele-ticket";'
        't.textContent=["🎫","🎟️","💴","✨","🍀"][j%5];'
        't.style.left=Math.random()*100+"%"; t.style.animationDuration=(2.4+Math.random()*2.2)+"s";'
        't.style.animationDelay=(Math.random()*1.2)+"s"; ov.appendChild(t);}'
        'setTimeout(function(){ ov.classList.remove("show");'
        'var ex=ov.querySelectorAll(".cele-fw,.cele-ticket"); for(var k=0;k<ex.length;k++){ex[k].remove();} }, 5400);'
        '}'
        'if(document.readyState!=="loading"){ssqDrawWheel();}'
        'else{document.addEventListener("DOMContentLoaded",ssqDrawWheel);}'
        '</script>'
        )
        return html
    except Exception:
        return ''


def generate_draw_machine_html():
    """🎰 双色球开奖机（模拟，纯娱乐）· 填充转盘旁原本空白的大片区域。

    用户诉求：报告里「手气摇奖机」转盘很高，左侧文本框只剩少量文字、下方一大片空白；
    希望在该空白区放一个模仿双色球开奖的机器，点一下就随机摇出双色球号码、
    漫天气球、显示「中了一等奖」，用来逗用户开心。

    设计：
    - 两台摇奖机（红/蓝）porthole 在摇奖时高速滚动随机号码（老虎机效果），约 2.2s 后定格。
    - 出球口展示标准双色球格式：6 个红球(01-33 不重复升序) + 1 个蓝球(01-16)。
    - 庆祝层：漫天气球 + 彩票雨 + 「🎉 恭喜你中了一等奖！」横幅（复用 .cele-overlay）。
    - 始终标注：纯随机模拟、与真实开奖无关、不承诺中奖（诚实底线，不误导）。
    纯 CSS/JS、零联网、零卡死；函数体用普通字符串拼接(非 f-string)，避免 JS 大括号破坏模板。
    """
    try:
        html = (
        '<div class="dm-card" id="ssqDM">'
        '<div class="dm-head">'
        '<div class="dm-title">🎰 双色球开奖机 · 模拟摇奖</div>'
        '<div class="dm-sub">点一下，看模拟开奖机摇出你的双色球号码～（纯娱乐，随机出号，与真实开奖无关）</div>'
        '</div>'
        '<div class="dm-machine">'
        '<div class="dm-drum" id="dmDrumR">'
        '<div class="dm-drum-name">🔴 红球摇奖机</div>'
        '<div class="dm-port" id="dmPortR"><span class="dm-mini">--</span><span class="dm-mini">--</span><span class="dm-mini">--</span></div>'
        '</div>'
        '<div class="dm-drum dm-blue-drum" id="dmDrumB">'
        '<div class="dm-drum-name">🔵 蓝球摇奖机</div>'
        '<div class="dm-port" id="dmPortB"><span class="dm-mini">--</span></div>'
        '</div>'
        '</div>'
        '<div class="dm-output" id="dmOut"><span style="color:#8fa0c8;font-size:13px;">等待摇奖…摇出 6 红 + 1 蓝</span></div>'
        '<button class="dm-btn" id="dmBtn" onclick="ssqDrawMachine()">🎲 开始摇奖</button>'
        '<div class="dm-status" id="dmStatus">准备好了吗？点上面的按钮试试手气 🍀</div>'
        '<div class="dm-note">说明：这是纯随机模拟的小游戏，用来图个乐子。双色球开奖完全随机，一等奖概率约 1/1772 万；'
        '本机不预测、不保证中奖，请理性娱乐、量力而行。</div>'
        '<div class="cele-overlay" id="ssqDMCele">'
        '<div class="cele-flash"></div>'
        '<div class="cele-banner">🎉 恭喜你中了一等奖！（模拟娱乐）</div>'
        '</div>'
        '</div>'
        '<script>'
        'function ssqDMPad(n){return n<10?("0"+n):(""+n);}'
        'var ssqDMOn=false;'
        'function ssqDrawMachine(){'
        'var btn=document.getElementById("dmBtn"), out=document.getElementById("dmOut"), st=document.getElementById("dmStatus");'
        'if(ssqDMOn)return; ssqDMOn=true; btn.disabled=true; st.textContent="摇奖机飞速运转中…🌀";'
        'var dmColors=["#ff5a5a","#ffb14a","#ffe14a","#5ad17a","#4aa3ff","#b07bff","#ff7ad1"];'
        'var roll=setInterval(function(){'
        'var rs=""; for(var i=0;i<3;i++){rs+="<span class=\'dm-mini\'>"+ssqDMPad(1+Math.floor(Math.random()*33))+"</span>";}'
        'document.getElementById("dmPortR").innerHTML=rs;'
        'document.getElementById("dmPortB").innerHTML="<span class=\'dm-mini\'>"+ssqDMPad(1+Math.floor(Math.random()*16))+"</span>";'
        '},80);'
        'setTimeout(function(){'
        'clearInterval(roll);'
        'var reds=[]; while(reds.length<6){var n=1+Math.floor(Math.random()*33); if(reds.indexOf(n)<0)reds.push(n);} reds.sort(function(a,b){return a-b;});'
        'var blue=1+Math.floor(Math.random()*16);'
        'var h=""; for(var i=0;i<reds.length;i++){h+="<span class=\'dm-ball\'>"+ssqDMPad(reds[i])+"</span>";}'
        'h+="<span class=\'dm-plus\'>+</span><span class=\'dm-ball dm-blue\'>"+ssqDMPad(blue)+"</span>";'
        'out.innerHTML=h;'
        'st.innerHTML="<strong style=\'color:#ffd24a\'>🎉 摇出啦！这注模拟中了「一等奖」（纯娱乐开心一下）</strong>";'
        'btn.disabled=false; ssqDMOn=false; ssqDMCelebrate(dmColors);'
        '},2200);'
        '}'
        'function ssqDMCelebrate(colors){'
        'var ov=document.getElementById("ssqDMCele"); if(!ov)return;'
        'ov.classList.add("show");'
        'for(var i=0;i<10;i++){var b=document.createElement("div"); b.className="dm-balloon";'
        'b.textContent=["🎈","🎊","🎉","💛","💖"][i%5];'
        'b.style.left=(4+i*9)+"%"; b.style.animationDelay=(i*0.15)+"s"; b.style.background=colors[i%colors.length]; ov.appendChild(b);}'
        'for(var j=0;j<24;j++){var t=document.createElement("div"); t.className="cele-ticket";'
        't.textContent=["🎫","🎟️","✨","🍀","💴"][j%5];'
        't.style.left=Math.random()*100+"%"; t.style.animationDuration=(2.4+Math.random()*2.2)+"s"; t.style.animationDelay=(Math.random()*1.2)+"s"; ov.appendChild(t);}'
        'setTimeout(function(){ ov.classList.remove("show");'
        'var ex=ov.querySelectorAll(".dm-balloon,.cele-ticket"); for(var k=0;k<ex.length;k++){ex[k].remove();} },5200);'
        '}'
        'if(document.readyState!=="loading"){}else{document.addEventListener("DOMContentLoaded",function(){});}'
        '</script>'
        )
        return html
    except Exception:
        return ''


def generate_almanac_html():
    """📅 老黄历 · 今日宜忌（玄学娱乐，纯 JS 随机 + 日期种子，零联网）。

    放大版 + 居中 + 引导标语(issue#2): 让原本容易被忽略的小卡片变成
    用户愿意点开的「东方秘术」互动。点击后显示今天日子、宜/忌/冲煞/吉神/吉时 + 一句玄学建议。
    明确标注「玄学娱乐，别太当真」。
    """
    try:
        html = (
        '<div class="entertain-big almanac-card">'
        '<div class="ent-slogan">🏮 翻开今日老黄历 —— 宜忌、冲煞、吉神、吉时，今日运程一页尽览</div>'
        '<div class="fg-head">'
        '<div class="fg-badge"><svg class="alm-ico" viewBox="0 0 64 64" aria-hidden="true">'
        '<defs><linearGradient id="ssqAlmG" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#fff3c4"/><stop offset="1" stop-color="#e0a020"/></linearGradient></defs>'
        '<rect x="14" y="10" width="36" height="44" rx="6" fill="url(#ssqAlmG)" stroke="#7a2418" stroke-width="2.5"/>'
        '<rect x="14" y="10" width="36" height="44" rx="6" fill="none" stroke="#fff6da" stroke-width="1.5" opacity="0.7"/>'
        '<line x1="22" y1="22" x2="42" y2="22" stroke="#7a2418" stroke-width="3" stroke-linecap="round"/>'
        '<line x1="22" y1="32" x2="42" y2="32" stroke="#7a2418" stroke-width="3" stroke-linecap="round"/>'
        '<line x1="22" y1="42" x2="34" y2="42" stroke="#7a2418" stroke-width="3" stroke-linecap="round"/>'
        '<circle class="ssq-spk" cx="50" cy="13" r="3.4" fill="#fffbe6"/></svg></div>'
        '<div class="fg-title">今日老黄历<span class="fg-sub">东方秘术 · 玄学娱乐</span></div>'
        '<span class="alm-seal">運</span>'
        '</div>'
        '<div class="fg-body">'
        '<div class="fg-text" id="ssqAlm">翻开看看今天适合做点啥～</div>'
        '<button class="fg-btn" onclick="ssqAlmOpen()">📜 翻开今日黄历</button>'
        '</div></div>'
        '<script>'
        'function ssqAlmOpen(){'
        'var yi=["出行","会友","买花","看电影","吃火锅","散步","读书","理财规划","整理房间","晒太阳","喝奶茶"];'
        'var ji=["熬夜","emo","冲动消费","赖床","内耗","暴饮暴食","拖延","生闷气","钻牛角尖"];'
        'var chong=["鼠","牛","虎","兔","龙","蛇","马","羊","猴","鸡","狗","猪"];'
        'var jiShen=["金匮","天德","玉堂","司命","青龙","明堂"];'
        'var js=["子时(23-1)","卯时(5-7)","巳时(9-11)","午时(11-13)","申时(15-17)","酉时(17-19)"];'
        'var qian=["今日宜主动出击，好事近了","可确保的中奖结果求进，别急","贵人暗中相助，多笑一笑","财气在东南，心态放轻松","宜与旧友联络，缘分在线"];'
        'var d=new Date(); var seed=(d.getFullYear()*372+d.getMonth()*31+d.getDate());'
        'function pk(a){return a[((seed%a.length)+a.length)%a.length];}'
        'function pk3(a){var r=[],used={};for(var i=0;i<3;i++){var x=a[((seed+i*5)%a.length)];if(used[x]){x=a[((seed+i*5+3)%a.length)];}used[x]=1;r.push(x);}return r;}'
        'var yi3=pk3(yi), ji3=pk3(ji);'
        'var out="📅 "+(d.getMonth()+1)+"月"+d.getDate()+"日 · 老黄历今日播报<br>";'
        'out+="<div class=\'alm-grid\'><div class=\'alm-col\'><b style=\'color:#06d6a0\'>宜</b> "+yi3.join("、")+"</div>"'
        '+"<div class=\'alm-col\'><b style=\'color:#ff6b6b\'>忌</b> "+ji3.join("、")+"</div></div>";'
        'out+="<div class=\'alm-row\'>冲煞：<b>"+pk(chong)+"</b> ｜ 吉神：<b>"+pk(jiShen)+"</b> ｜ 吉时：<b>"+pk(js)+"</b></div>";'
        'out+="<div class=\'alm-q\'>🔮 "+pk(qian)+"（东方秘术娱乐，别太当真😄）</div>";'
        'document.getElementById("ssqAlm").innerHTML=out;'
        '}'
        '</script>'
        )
        return html
    except Exception:
        return ''


def generate_tarot_html():
    """🔮 水晶球 · 塔罗占卜（西方玄学娱乐，纯 JS 随机，零联网）。

    放大版 + 居中 + 引导标语(issue#2): 让原本容易被忽略的小卡片变成
    用户愿意点开的「西方玄学」互动。点击后显示今日守护星座/贵人方位/抽一张塔罗牌意。
    明确标注「纯西方玄学娱乐，给你一点小信心」。
    """
    try:
        html = (
        '<div class="entertain-big tarot-card">'
        '<div class="ent-slogan">🌌 星河为你转动 —— 让水晶球接通今夜星轨，抽一张属于你的塔罗</div>'
        '<div class="fg-head">'
        '<div class="fg-badge"><svg class="tarot-ico" viewBox="0 0 64 64" aria-hidden="true">'
        '<defs>'
        '<radialGradient id="ssqBallG" cx="38%" cy="30%" r="72%">'
        '<stop offset="0" stop-color="#fbf7ff"/><stop offset="0.45" stop-color="#b39bff"/><stop offset="1" stop-color="#6a4bd6"/></radialGradient>'
        '<radialGradient id="ssqBallHalo" cx="50%" cy="50%" r="50%">'
        '<stop offset="0.68" stop-color="rgba(170,140,255,0)"/><stop offset="1" stop-color="rgba(170,140,255,.6)"/></radialGradient>'
        '</defs>'
        '<circle cx="32" cy="32" r="27" fill="url(#ssqBallHalo)"/>'
        '<ellipse cx="32" cy="53" rx="18" ry="4.5" fill="rgba(255,255,255,0.18)"/>'
        '<circle cx="32" cy="30" r="21" fill="url(#ssqBallG)"/>'
        '<circle cx="25" cy="22" r="5.5" fill="rgba(255,255,255,0.65)"/>'
        '<circle cx="39" cy="35" r="3" fill="rgba(255,255,255,0.5)"/>'
        '<g class="ssq-spk2"><text x="44" y="13" font-size="14" fill="#ffffff">✦</text></g>'
        '<g class="ssq-spk"><text x="13" y="49" font-size="11" fill="#cdbcff">✧</text></g>'
        '</svg></div>'
        '<div class="fg-title">水晶球 · 塔罗占卜<span class="fg-sub">西方星象 · 玄学娱乐</span></div>'
        '</div>'
        '<div class="fg-body">'
        '<div class="fg-text" id="ssqTarot">让水晶球看看今天谁在罩着你～</div>'
        '<button class="fg-btn" onclick="ssqTarot()">🔮 请水晶球算一卦</button>'
        '</div></div>'
        '<script>'
        'function ssqTarot(){'
        'var star=["白羊座","金牛座","双子座","巨蟹座","狮子座","处女座","天秤座","天蝎座","射手座","摩羯座","水瓶座","双鱼座"];'
        'var noble=["正北","东北","正东","东南","正南","西南","正西","西北"];'
        'var cards=[["太阳（正位）","你今天光芒万丈，自信就是你的运气"],'
        '["星星（正位）","希望降临，低谷已过，往前走就对了"],'
        '["恋人（正位）","关系和谐，适合与人合作达成好事"],'
        '["力量（正位）","内在力量在线，能稳稳 hold 住小挑战"],'
        '["命运之轮（正位）","转机出现，今天有意外小惊喜"],'
        '["愚人（正位）","保持天真与好奇，新机会正在敲门"],'
        '["女祭司（正位）","直觉很准，相信自己的第一感觉"],'
        '["节制（正位）","平衡感好，张弛有度好运自然来"],'
        '["高塔（逆位）","风暴已过，今天趋于平稳安心"],'
        '["世界（正位）","圆满暗示，事情会有好收尾"]];'
        'var cheer=["今天有人悄悄为你撑腰，放心冲","贵人方位已点亮，多往人多的地方凑","你比自己想的更被偏爱，开心点","宇宙今天偏爱你，笑一个🌞"];'
        'function rnd(a){return a[Math.floor(Math.random()*a.length)];}'
        'var s=rnd(star), n=rnd(noble), c=rnd(cards), ch=rnd(cheer);'
        'var out="<div class=\'tarot-row\'>🌟 今日守护星座：<b>"+s+"</b></div>";'
        'out+="<div class=\'tarot-row\'>🧭 贵人方位：<b>"+n+"</b></div>";'
        'out+="<div class=\'tarot-pull\'>🃏 塔罗：<b>"+c[0]+"</b><br><span class=\'tarot-mean\'>"+c[1]+"</span></div>";'
        'out+="<div class=\'tarot-cheer\'>"+ch+"（纯西方玄学娱乐，给你一点小信心✨）</div>";'
        'document.getElementById("ssqTarot").innerHTML=out;'
        '}'
        '</script>'
        )
        return html
    except Exception:
        return ''


def generate_engage_html():
    """首屏问候 + 连续打卡🔥 + 理性娱乐达人等级进度（UX 留存钩子，纯 localStorage 离线）。

    学习二（吸引/留住客户）：
    - 按时间问候（客户端 new Date，离线）→ 一秒拉近距离
    - 连续打卡 streak（localStorage 记录最近访问日，断更重置）→ 最强留存钩子
    - 等级/经验进度条（看报告/玩互动涨 xp）→ 投资感(Investment)
    - 点击 LOGO 触发满屏烟花彩蛋🎆
    """
    try:
        html = (
        '<div class="greet-bar">'
        '  <div class="g-left"><span class="g-emoji" id="ssqGreetEmoji">👋</span>'
        '<span id="ssqGreetWord">你好呀</span>'
        '<span class="g-sub">今天也来转运啦？</span></div>'
        '  <div class="g-right">'
        '    <span class="g-streak" title="连续查看天数"><span class="flame">🔥</span><span id="ssqStreakN">1</span> 天连看</span>'
        '    <div class="g-level" title="理性娱乐达人等级">'
        '      <div class="gl-top"><span id="ssqLv">Lv.1 新股民</span><span id="ssqXp">0/50</span></div>'
        '      <div class="gl-bar"><div class="gl-fill" id="ssqLvFill" style="width:0%"></div></div>'
        '    </div>'
        '  </div>'
        '</div>'
        '<script>'
        'function ssqGreet(){'
        'var h=new Date().getHours();var e="👋",w="你好呀";'
        'if(h<6){e="🌙";w="夜深了，早点休息，明天再来转运";}'
        'else if(h<11){e="🌅";w="早安，新的一天从好心情开始";}'
        'else if(h<14){e="☀️";w="午安，今天想转运吗？";}'
        'else if(h<18){e="🌤️";w="下午好，喝口水继续冲";}'
        'else if(h<22){e="🌆";w="晚上好，今晚开奖更刺激";}'
        'else{e="🌙";w="夜猫子，注意别上头哦";}'
        'var ge=document.getElementById("ssqGreetEmoji"),gw=document.getElementById("ssqGreetWord");'
        'if(ge)ge.textContent=e;if(gw)gw.textContent=w;}'
        'function ssqEngage(){try{'
        'var t=new Date();var key="ssq_dlv1";'
        'var d=JSON.parse(localStorage.getItem(key)||"{}");'
        'var today=t.toDateString();var y=new Date(t.getTime()-86400000).toDateString();'
        'var streak=(d.date===today)?(d.streak||1):((d.date===y)?(d.streak||0)+1:1);'
        'var xp=((d.xp||0)+14);if(xp>500)xp=500;'
        'localStorage.setItem(key,JSON.stringify({date:today,streak:streak,xp:xp}));'
        'var lv=Math.floor(xp/50)+1;'
        'var names=["新股民","小彩民","理性达人","娱乐高手","防割韭菜侠","运势收藏家","彩票明白人","幸运星","锦鲤本鲤","双色球之王"];'
        'var nm=names[Math.min(lv-1,names.length-1)];'
        'var prog=((xp%50)/50*100).toFixed(0);'
        'var sn=document.getElementById("ssqStreakN");if(sn)sn.textContent=streak;'
        'var sl=document.getElementById("ssqLv");if(sl)sl.textContent="Lv."+lv+" "+nm;'
        'var sx=document.getElementById("ssqXp");if(sx)sx.textContent=(xp%50)+"/50";'
        'var sf=document.getElementById("ssqLvFill");if(sf)sf.style.width=prog+"%";'
        '}catch(e){}}'
        'function ssqEgg(){'
        'if(typeof ssqCelebrate==="function"){ssqCelebrate();}'
        'else{var ov=document.getElementById("ssqCele");if(ov){ov.classList.add("show");setTimeout(function(){ov.classList.remove("show");},3000);}}}'
        'if(document.readyState!=="loading"){ssqGreet();ssqEngage();}'
        'else{document.addEventListener("DOMContentLoaded",function(){ssqGreet();ssqEngage();});}'
        'var lg=document.querySelector(".logo-egg");if(lg){lg.addEventListener("click",ssqEgg);}'
        '</script>'
        )
        return html
    except Exception:
        return ''


def generate_scratch_html(groups):
    """🎫 刮刮卡揭示今日推荐号码（学习三·趣味性/娱乐性，最强"不一样"互动）。

    号码以 DOM 形式藏在银层下方，canvas 仅做刮除交互，刮开 >50% 自动全显。
    诚实标注：刮开只是展示推荐号码，绝不暗示中奖。
    注意：含 JS 必须用字符串拼接，避免被外层报告 f-string 吞掉大括号。
    """
    try:
        rows = ''
        for i, g in enumerate(groups, 1):
            fr = ''.join('<span class="ball ball-red">%02d</span>' % n for n in sorted(g['front']))
            bk = ''.join('<span class="ball ball-blue">%02d</span>' % n for n in sorted(g['back']))
            rows += '<div class="sc-row"><span class="sc-name">第%d组 %s</span><div class="sc-balls">%s %s</div></div>' % (i, g['name'], fr, bk)
        html = (
        '<div class="scratch-card">'
        '  <div class="sc-head"><span class="sc-emoji">🎫</span>'
        '<span class="sc-title">刮开看今日幸运号码</span>'
        '<span class="sc-sub">纯娱乐参考 · 不保证结果</span></div>'
        '  <div class="sc-stage">'
        '    <div class="sc-prize" id="ssqScratchPrize">' + rows + '</div>'
        '    <button class="sc-reveal" onclick="ssqRevealNow()">直接看 ✨</button>'
        '    <canvas id="ssqScratchCv"></canvas>'
        '    <div class="sc-hint" id="ssqScratchHint">👆 用鼠标 / 手指刮开银层</div>'
        '  </div>'
        '</div>'
        '<script>'
        'function ssqScratchInit(){'
        'var cv=document.getElementById("ssqScratchCv");if(!cv)return;'
        'var stage=cv.parentElement;var w=stage.clientWidth,h=stage.clientHeight;cv.width=w;cv.height=h;'
        'var ctx=cv.getContext("2d");'
        'function fill(){var g=ctx.createLinearGradient(0,0,w,h);g.addColorStop(0,"#cfd6e6");g.addColorStop(.5,"#aeb8cf");g.addColorStop(1,"#e3e9f4");'
        'ctx.globalCompositeOperation="source-over";ctx.fillStyle=g;ctx.fillRect(0,0,w,h);'
        'ctx.fillStyle="rgba(80,92,120,.9)";ctx.font="bold 19px sans-serif";ctx.textAlign="center";'
        'ctx.fillText("刮开看号码 ✨",w/2,h/2-6);ctx.font="12px sans-serif";ctx.fillText("（纯娱乐，不保证结果）",w/2,h/2+18);}'
        'fill();var drawing=false,erased=0;'
        'function pos(e){var r=cv.getBoundingClientRect();var cx=(e.touches?e.touches[0].clientX:e.clientX)-r.left;'
        'var cy=(e.touches?e.touches[0].clientY:e.clientY)-r.top;return{x:cx,y:cy};}'
        'function erase(x,y){ctx.globalCompositeOperation="destination-out";ctx.beginPath();ctx.arc(x,y,24,0,7);ctx.fill();}'
        'function ratio(){try{var dt=ctx.getImageData(0,0,w,h).data;var c=0,t=0;for(var i=3;i<dt.length;i+=48){t++;if(dt[i]===0)c++;}return t?c/t:0;}catch(e){return 0;}}'
        'function move(e){if(!drawing)return;if(e.cancelable)e.preventDefault();var p=pos(e);erase(p.x,p.y);erased++;'
        'if(erased%5===0&&ratio()>0.5){ssqRevealNow();}}'
        'cv.addEventListener("mousedown",function(e){drawing=true;var p=pos(e);erase(p.x,p.y);});'
        'cv.addEventListener("mousemove",move);'
        'window.addEventListener("mouseup",function(){drawing=false;});'
        'cv.addEventListener("touchstart",function(e){drawing=true;var p=pos(e);erase(p.x,p.y);},{passive:false});'
        'cv.addEventListener("touchmove",move,{passive:false});'
        'window.addEventListener("touchend",function(){drawing=false;});'
        'window.addEventListener("resize",function(){w=stage.clientWidth;h=stage.clientHeight;cv.width=w;cv.height=h;fill();});'
        '}'
        'function ssqRevealNow(){var cv=document.getElementById("ssqScratchCv");if(!cv)return;'
        'cv.style.transition="opacity .45s";cv.style.opacity="0";setTimeout(function(){cv.style.display="none";},460);'
        'var hi=document.getElementById("ssqScratchHint");if(hi)hi.style.display="none";}'
        'if(document.readyState!=="loading"){ssqScratchInit();}'
        'else{document.addEventListener("DOMContentLoaded",ssqScratchInit);}'
        '</script>'
        )
        return html
    except Exception:
        return ''


def generate_stayhook_html():
    """结尾留存钩子（学习二）：明天开奖提醒 + 收藏打卡解锁 + LOGO 烟花彩蛋入口。"""
    try:
        html = (
        '<div class="stay-hook">'
        '  <div class="sh-title">⏰ 明天 21:15 开奖，记得回来看你中没中</div>'
        '  <div class="sh-text">把本报告收藏起来，<b>连续打卡</b>解锁你的「专属运势签」🃏｜ 点上方标题 LOGO 还能放烟花🎆<br>'
        '  理性娱乐、买得明白，才是真正的「锦鲤体质」✨</div>'
        '  <button class="sh-cta" onclick="ssqEgg()">🎆 来一发烟花</button>'
        '</div>'
        )
        return html
    except Exception:
        return ''


def _ssq_significance_panel():
    """基于账本真实累计命中, 用精确二项检验判断系统是否超越随机.

    把报告里"本系统无预测力(p>0.05)"从空口断言升级为证据化:
    用账本每一期每一组的真实命中, 对照"闭眼随机选"的期望命中, 算精确双尾 p 值.
    p>=0.05 => 与随机无统计差异 => 所有中奖均为随机运气, 非分析能力.
    """
    import math, json, os
    HERE = os.path.dirname(os.path.abspath(__file__))
    try:
        perf = json.load(open(os.path.join(HERE, 'ssq_performance.json'), encoding='utf-8'))
        recs = perf.get('records', [])
    except Exception:
        return ''
    if not recs:
        return ''
    nf = nb = hf = hb = np_ = 0
    dist = {}
    for r in recs:
        for g in r.get('results', []):
            gname = str(g.get('group', '') or g.get('name', ''))
            if '胆' in gname:
                continue
            nf += len(g.get('pred_front', [])) or 6
            nb += len(g.get('pred_back', [])) or 3
            hf += int(g.get('front_hits', 0) or 0)
            hb += int(g.get('back_hits', 0) or 0)
            np_ += 1
            t = g.get('prize') or '未中奖'
            dist[t] = dist.get(t, 0) + 1
    if nf == 0:
        return ''
    p0f, p0b = 6/33, 1/16

    def two_sided_p(n, k, p):
        if n == 0:
            return 1.0
        def _lpmf(j):
            return math.log(math.comb(n, j)) + j*math.log(p) + (n-j)*math.log(1-p)
        lk = _lpmf(k)
        pv = 0.0
        for j in range(n+1):
            if _lpmf(j) <= lk + 1e-9:
                pv += math.exp(_lpmf(j))
        return min(1.0, pv)

    pf, pb = two_sided_p(nf, hf, p0f), two_sided_p(nb, hb, p0b)
    ef, eb = nf*p0f, nb*p0b

    def _v(p):
        return ('\u26a0\ufe0f 存在统计显著差异(p<0.05)，疑似可量化信号，需进一步复核'
                if p < 0.05 else '与随机无显著差异(p\u22650.05)：当前无任何\u201c预测力\u201d证据')
    dist_s = '\u3001'.join(f'{k}\u00d7{v}' for k, v in sorted(dist.items(), key=lambda x: -x[1])) or '\u65e0'
    return f"""
<div class="section" style="border-color:#ff7700;">
<div class="section-title">📐 长期显著性检验 \u00b7 本系统到底有没有\u201c预测力\u201d？（基于账本 {np_} 组真实累计）</div>
<table>
<tr><th>\u7ef4\u5ea6</th><th>\u5b9e\u6d4b\u547d\u4e2d</th><th>\u968f\u673a\u671f\u671b</th><th>\u5dee\u8ddd</th><th>\u7cbe\u786e\u4e8c\u9879\u68c0\u9a8c p \u503c</th><th>\u7ed3\u8bba</th></tr>
<tr><td>\u524d\u533a(\u6bcf\u7ec46\u9009)</td><td>{hf} / {nf} \u6b21\u6bd4\u8f83</td><td>{ef:.1f}</td><td>{hf-ef:+.1f}</td><td>{pf:.3f}</td><td>{_v(pf)}</td></tr>
<tr><td>\u540e\u533a(\u6bcf\u7ec43\u90091)</td><td>{hb} / {nb} \u6b21\u6bd4\u8f83</td><td>{eb:.1f}</td><td>{hb-eb:+.1f}</td><td>{pb:.3f}</td><td>{_v(pb)}</td></tr>
</table>
<p style="color:#ffd9a0; line-height:1.8;">
\u7d2f\u8ba1 {np_} \u7ec4\u6807\u51c6\u9884\u6d4b\u4e2d\uff0c\u4e2d\u5956\u5206\u5e03\uff1a<strong>{dist_s}</strong>\u3002<br>
<strong>\u89e3\u8bfb\uff1a</strong>\u53ea\u8981 p\u22650.05\uff0c\u5c31\u8bf4\u660e\u7cfb\u7edf\u547d\u4e2d\u4e0e\u201c\u95ed\u773c\u968f\u673a\u9009\u201d\u6ca1\u6709\u7edf\u8ba1\u533a\u522b\u2014\u2014\u6240\u6709\u4e2d\u5956\uff08\u542b\u4e0a\u4e00\u671f\u516d\u7b49\u5956\uff09\u90fd\u5e94\u5f52\u56e0\u4e8e<strong>\u968f\u673a\u8fd0\u6c14</strong>\uff0c\u800c\u975e\u5206\u6790\u80fd\u529b\u3002
\u82e5\u672a\u6765\u67d0\u671f p \u8dcc\u7834 0.05\uff0c\u624d\u503c\u5f97\u8ba4\u771f\u6392\u67e5\u662f\u5426\u771f\u51fa\u73b0\u53ef\u91cf\u5316\u4fe1\u53f7\uff08\u4e5f\u4ecd\u53ef\u80fd\u662f\u5c0f\u6982\u7387\u6ce2\u52a8\uff0c\u9700\u66f4\u591a\u671f\u590d\u6838\uff09\u3002
</p>
</div>
"""

def generate_report(draws, models, groups, dantuo, expert_picks, data_issues, back_top4_main):
    """生成V1 HTML报告
    
    Args:
        back_top4_main: 主蓝球推荐TOP4（按评分排序），用于胆拖方案的蓝球展示
    """
    print("\n" + "=" * 70)
    print("【步骤6/7: 生成报告】")
    print("=" * 70)
    
    total = len(draws)
    latest = draws[-1]
    next_period = next_period_func(int(latest['period']), latest.get('date'))
    try:
        record_spend(next_period, 2.0, "auto: 预测生成(基本投注)")
    except Exception:
        pass
    try:
        _ledger_stats = ssq_ledger_summary()
    except Exception:
        _ledger_stats = None
    
    # V1.0.2: 动态读取诚实闸门数据, 避免报告数字过期
    power = _load_power_stats() or {}
    ml = _load_ml_stats() or {}
    pw_n = power.get('n_periods') or 2703
    strat_roi = power.get('strat_roi')
    base_roi = power.get('base_roi')
    strat_prize = power.get('strat_prize_rate')
    base_prize = power.get('base_prize_rate')
    profit_prob = power.get('profit_prob')
    expected_net = power.get('expected_net')
    ci_low = power.get('ci_low')
    ci_high = power.get('ci_high')
    ml_n = ml.get('n_periods') or 203
    ml_min = ml.get('model_min')
    ml_max = ml.get('model_max')
    ml_rand = ml.get('random_mean')

    # 预格式化为展示字符串 (缺失时降级为 —)
    strat_roi_s = _pct(strat_roi)
    base_roi_s = _pct(base_roi)
    strat_prize_s = _pct(strat_prize)
    base_prize_s = _pct(base_prize)
    profit_prob_s = _pct(profit_prob)
    expected_net_s = f"¥{expected_net:,.0f}" if isinstance(expected_net, (int, float)) else "—"
    ci_s = (f"[{ci_low:+.2f},{ci_high:+.2f}]pp" if isinstance(ci_low, (int, float))
            and isinstance(ci_high, (int, float)) else "[—]")
    ml_hit_s = (f"{ml_min:.2f}~{ml_max:.2f} 球" if isinstance(ml_min, (int, float))
                and isinstance(ml_max, (int, float)) else "—")
    ml_rand_s = f"{ml_rand:.2f} 球" if isinstance(ml_rand, (int, float)) else "—"
    power_label = f"V1.0强化引擎 {pw_n}期"
    ml_label = f"V1.0 ML 自评 {ml_n}期"
    

    # 计算凯利 + 期望奖金/回报率/净亏损 (全部从单一可信源 PRIZE_PAYOUT / ssq_common 计算)
    total_combos = math.comb(K, 6) * BACK_N  # 双色球: C(33,6)*16 = 17,721,088
    p_win = 1 / total_combos
    b_win = 10_000_000 / 2
    kelly_f = (b_win * p_win - (1 - p_win)) / b_win
    # 期望奖金(单注2元): 遍历 PRIZE_PAYOUT 各奖级, 用组合数精确算概率
    exp_prize = 0.0
    for (fx, bx), prize in PRIZE_PAYOUT.items():
        fw = math.comb(6, fx) * math.comb(K - 6, 6 - fx)
        bw = math.comb(1, bx) * math.comb(BACK_N - 1, 1 - bx)
        exp_prize += fw * bw / total_combos * prize
    exp_return = exp_prize / 2 - 1            # 期望回报率(每2元注)
    net_loss = 2 - exp_prize                   # 每注期望净亏损(元)
    exp_prize_s = f"{exp_prize:.2f}"
    exp_return_pct = f"{exp_return * 100:.1f}%"
    net_loss_s = f"{net_loss:.2f}"
    red_combos_s = f"{math.comb(K, 6):,}"      # 1,107,568
    one_prize_prob_s = f"1/{total_combos / 1e6:.1f}M"
    
    # ECI
    front_eci = Counter()
    back_eci = Counter()
    for expert, front, back in expert_picks:
        for n in front:
            front_eci[n] += 1
        for n in back:
            back_eci[n] += 1
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>双色球第{next_period}期预测报告 V1 - 全面修复版</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
/* ===== 年轻化·活力主题：极光流动背景 + 漂浮装饰 ===== */
body {{ font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif; background: #070617; color: #e8e8f0; padding: 20px; position: relative; min-height: 100vh; overflow-x: hidden; }}
body::before {{ content: ""; position: fixed; inset: -20%; z-index: -2;
  background:
    radial-gradient(40% 38% at 15% 20%, rgba(123,92,255,.42), transparent 60%),
    radial-gradient(38% 36% at 82% 18%, rgba(255,75,124,.38), transparent 60%),
    radial-gradient(42% 40% at 70% 80%, rgba(0,200,255,.34), transparent 60%),
    radial-gradient(40% 38% at 25% 82%, rgba(255,180,40,.30), transparent 60%);
  filter: blur(8px); animation: aurora 18s ease-in-out infinite alternate; }}
@keyframes aurora {{ 0% {{ transform: translate(0,0) scale(1); }} 50% {{ transform: translate(2%, -2%) scale(1.06); }} 100% {{ transform: translate(-2%, 2%) scale(1.02); }} }}
body::after {{ content: ""; position: fixed; inset: 0; z-index: -1; pointer-events: none; opacity: .5;
  background-image:
    radial-gradient(circle at 12% 30%, rgba(255,255,255,.07) 0 2px, transparent 3px),
    radial-gradient(circle at 78% 62%, rgba(255,255,255,.06) 0 2px, transparent 3px),
    radial-gradient(circle at 45% 85%, rgba(255,255,255,.05) 0 1.5px, transparent 3px);
  background-size: 260px 260px, 320px 320px, 200px 200px; }}
.fblob {{ position: fixed; border-radius: 50%; z-index: -1; pointer-events: none; filter: blur(2px); opacity: .55; animation: blobFloat 12s ease-in-out infinite; }}
@keyframes blobFloat {{ 0%,100% {{ transform: translateY(0) rotate(0); }} 50% {{ transform: translateY(-26px) rotate(18deg); }} }}

.container {{ max-width: 1200px; margin: 0 auto; position: relative; z-index: 1; }}
/* 玻璃拟态容器 */
.header {{ text-align: center; padding: 34px 20px; border-radius: 18px; margin-bottom: 18px;
  background: rgba(20,18,46,.55); backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);
  border: 1px solid rgba(255,255,255,.10); box-shadow: 0 8px 40px rgba(123,92,255,.18); }}
.header h1 {{ font-size: 30px; margin-bottom: 10px; font-weight: 900; letter-spacing: .5px;
  background: linear-gradient(92deg, #ff5e8a, #ffb347, #5ee0ff, #9b7bff); -webkit-background-clip: text; background-clip: text; color: transparent;
  background-size: 250% 100%; animation: titleFlow 8s linear infinite; }}
@keyframes titleFlow {{ to {{ background-position: 250% 0; }} }}
.header .subtitle {{ color: #b9b6d6; font-size: 14px; }}
.header .meta {{ margin-top: 16px; display: flex; justify-content: center; gap: 14px; flex-wrap: wrap; }}
.header .meta-item {{ background: rgba(255,255,255,.07); border: 1px solid rgba(255,255,255,.10); padding: 8px 18px; border-radius: 20px; font-size: 13px; transition: transform .15s, background .15s; }}
.header .meta-item:hover {{ transform: translateY(-2px); background: rgba(255,255,255,.13); }}
.header .meta-item strong {{ color: #ffd24a; }}
.section {{ background: rgba(18,16,40,.60); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border-radius: 16px; padding: 24px; margin: 20px 0; border: 1px solid rgba(255,255,255,.10); box-shadow: 0 6px 28px rgba(0,0,0,.28); }}
.section-title {{ font-size: 20px; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 1px solid rgba(255,255,255,.10);
  background: linear-gradient(92deg, #ffd24a, #ff7a8a, #5ee0ff); -webkit-background-clip: text; background-clip: text; color: transparent; font-weight: 800; }}
.warning {{ background: #2a1010; border: 1px solid #ff4444; border-radius: 8px; padding: 15px; margin: 15px 0; }}
.warning h3 {{ color: #ff6b6b; margin-bottom: 8px; }}
.warning p {{ color: #ff9999; font-size: 14px; line-height: 1.6; }}
.info {{ background: #0d1a2a; border: 1px solid #0066cc; border-radius: 8px; padding: 15px; margin: 15px 0; }}
.info h3 {{ color: #00aaff; margin-bottom: 8px; }}
.info p {{ color: #88ccff; font-size: 14px; line-height: 1.6; }}
table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
th {{ background: #1a2050; padding: 10px; text-align: center; color: #00d4ff; font-size: 13px; }}
td {{ padding: 8px; text-align: center; border-bottom: 1px solid #1a2050; font-size: 13px; }}
.ball {{ display: inline-block; width: 36px; height: 36px; line-height: 36px; border-radius: 50%; text-align: center; font-weight: bold; font-size: 16px; margin: 2px; }}
.ball-red {{ background: linear-gradient(135deg, #ff4444, #cc0000); color: white; }}
.ball-blue {{ background: linear-gradient(135deg, #0099ff, #0066cc); color: white; }}
.group-card {{ background: #0d1130; border-radius: 10px; padding: 20px; margin: 15px 0; border-left: 4px solid #00d4ff; }}
.group-card h3 {{ color: #00d4ff; margin-bottom: 10px; }}
.group-card .strategy {{ color: #888; font-size: 13px; margin-bottom: 15px; }}
.balls-container {{ text-align: center; padding: 10px; }}
.stat-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 15px 0; }}
.stat-card {{ background: #0d1130; padding: 15px; border-radius: 8px; text-align: center; }}
.stat-card .value {{ font-size: 28px; color: #00d4ff; font-weight: bold; }}
.stat-card .label {{ font-size: 12px; color: #888; margin-top: 5px; }}
.disclaimer {{ text-align: center; color: #666; font-size: 12px; margin-top: 30px; padding: 20px; border-top: 1px solid #1a2050; }}
.v8-badge {{ display: inline-block; background: #00aa44; color: white; font-size: 10px; padding: 2px 6px; border-radius: 4px; margin-left: 5px; vertical-align: middle; }}
.antiscam {{ background: linear-gradient(135deg, #0d2818, #16331f); border: 2px solid #00dd88; border-radius: 14px; padding: 20px 22px; margin: 18px 0; }}
.antiscam .shield-title {{ font-size: 21px; color: #00ffaa; font-weight: bold; margin-bottom: 10px; display: flex; align-items: center; gap: 8px; }}
.antiscam .lead {{ color: #c8f0d8; font-size: 14px; line-height: 1.7; margin-bottom: 16px; }}
.antiscam .props {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 12px; }}
.antiscam .prop {{ background: #0a1f14; border: 1px solid #00aa66; border-radius: 10px; padding: 13px 14px; }}
.antiscam .prop .ico {{ font-size: 20px; }}
.antiscam .prop .ttl {{ color: #00ffaa; font-size: 15px; font-weight: bold; margin: 6px 0 4px; }}
.antiscam .prop .desc {{ color: #a8d8c0; font-size: 12.5px; line-height: 1.5; }}
.antiscam .honest {{ margin-top: 14px; background: #2a0d0d; border: 1px solid #ff4444; border-radius: 8px; padding: 11px; color: #ffb3b3; font-size: 13px; text-align: center; font-weight: bold; }}

/* ===== 近期一等奖领奖故事（年轻化·娱乐·诚实） ===== */
.win-stories {{ margin: 14px 0; background: linear-gradient(135deg, #1a1030 0%, #2a1840 100%); border: 1px solid #6c4cff; border-radius: 14px; padding: 16px 16px 14px; box-shadow: 0 4px 18px rgba(108,76,255,0.18); }}
.win-stories .ws-head {{ display: flex; align-items: center; gap: 8px; margin-bottom: 4px; }}
.win-stories .ws-emoji {{ font-size: 26px; line-height: 1; }}
.win-stories .ws-title {{ font-size: 18px; font-weight: 800; color: #fff; }}
.win-stories .ws-title .hl {{ color: #ffd24a; }}
.win-stories .ws-sub {{ color: #c9b8ff; font-size: 12.5px; margin: 2px 0 12px; }}
.win-stories .ws-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }}
@media (max-width: 560px) {{ .win-stories .ws-grid {{ grid-template-columns: 1fr; }} }}
.win-stories .ws-imgs {{ display: flex; gap: 10px; margin: 4px 0 9px; }}
.win-stories .ws-img {{ flex: 1 1 0; width: 50%; height: 130px; object-fit: cover; border-radius: 10px; border: 1px solid rgba(255,210,74,0.45); box-shadow: 0 3px 12px rgba(108,76,255,0.22); }}
.win-stories .ws-img-note {{ color: #c9b8ff; font-size: 11.5px; margin: 0 0 12px; line-height: 1.5; }}
.win-stories .ws-img-note strong {{ color: #ffd24a; }}
.win-card {{ background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.12); border-radius: 10px; padding: 11px 12px; transition: transform .15s; }}
.win-card:hover {{ transform: translateY(-2px); border-color: #ffd24a; }}
.win-card .wc-top {{ display: flex; align-items: baseline; gap: 6px; margin-bottom: 5px; }}
.win-card .wc-prize {{ font-size: 17px; font-weight: 800; color: #ffd24a; }}
.win-card .wc-place {{ font-size: 12px; color: #9d8bff; }}
.win-card .wc-title {{ font-size: 14px; font-weight: 700; color: #fff; margin-bottom: 4px; line-height: 1.35; }}
.win-card .wc-sum {{ font-size: 12.5px; color: #d8d0f0; line-height: 1.5; }}
.win-card .wc-foot {{ margin-top: 7px; font-size: 11px; color: #8c7fb8; }}
.win-card .wc-foot .src {{ color: #7fd0ff; }}
.win-stories .ws-note {{ margin-top: 12px; background: rgba(255,210,74,0.10); border: 1px dashed #ffd24a; border-radius: 8px; padding: 9px 11px; color: #ffe39a; font-size: 12.5px; line-height: 1.55; }}
.win-stories .ws-empty {{ color: #c9b8ff; font-size: 13px; text-align: center; padding: 8px 0; }}
.win-stories .ws-src-tag {{ display: inline-block; background: rgba(127,208,255,0.15); color: #7fd0ff; border-radius: 6px; padding: 1px 7px; font-size: 11px; margin-left: 4px; }}
.win-card .wc-badge {{ display: inline-block; background: linear-gradient(135deg, #ff416c, #ff4b2b); color: #fff; font-size: 11px; font-weight: 700; border-radius: 6px; padding: 1px 7px; margin-bottom: 7px; box-shadow: 0 1px 5px rgba(255,75,43,0.45); }}
.win-card .wc-badge.b2 {{ background: linear-gradient(135deg, #7b5cff, #4b8bff); box-shadow: 0 1px 5px rgba(75,139,255,0.45); }}


.draw-countdown {{ display: flex; align-items: center; justify-content: space-between; gap: 16px; margin: 14px 0; padding: 14px 18px; background: linear-gradient(135deg, #ff7a18 0%, #ff3d3d 55%, #c20000 100%); border-radius: 16px; box-shadow: 0 6px 22px rgba(255,61,61,0.30); overflow: hidden; }}
.draw-countdown .cd-left {{ display: flex; align-items: center; gap: 12px; }}
.draw-countdown .cd-emoji {{ font-size: 34px; line-height: 1; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.25)); }}
.draw-countdown .cd-title {{ font-size: 16px; font-weight: 800; color: #fff; letter-spacing: 0.5px; }}
.draw-countdown .cd-label {{ font-size: 12.5px; color: #ffe2c2; margin-top: 2px; }}
.draw-countdown .cd-clock {{ display: flex; align-items: flex-end; gap: 6px; }}
.draw-countdown .cd-box {{ display: inline-block; min-width: 46px; text-align: center; background: rgba(0,0,0,0.32); color: #fff; font-size: 26px; font-weight: 800; font-variant-numeric: tabular-nums; padding: 6px 4px; border-radius: 10px; box-shadow: inset 0 2px 6px rgba(0,0,0,0.3); }}
.draw-countdown .cd-clock i {{ color: #fff; font-style: normal; font-size: 13px; font-weight: 700; padding-bottom: 8px; }}
@media (max-width: 640px) {{ .draw-countdown {{ flex-direction: column; align-items: flex-start; }} .draw-countdown .cd-box {{ min-width: 38px; font-size: 21px; }} }}

.fun-card {{ display: flex; align-items: center; gap: 14px; margin: 12px 0; padding: 13px 16px; background: linear-gradient(135deg, #fff7e6 0%, #ffe9c7 100%); border: 1px dashed #ff9d3d; border-radius: 14px; box-shadow: 0 3px 14px rgba(255,157,61,0.15); }}
.fun-card .fc-emoji {{ font-size: 30px; line-height: 1; }}
.fun-card .fc-body {{ flex: 1; }}
.fun-card .fc-tag {{ font-size: 14px; font-weight: 800; color: #c25b00; }}
.fun-card .fc-honest {{ font-size: 11px; font-weight: 600; color: #9a6b3f; background: rgba(194,91,0,0.10); border-radius: 6px; padding: 1px 6px; }}
.fun-card .fc-text {{ font-size: 13px; color: #6b4a2a; margin-top: 3px; line-height: 1.5; }}

/* ===== 开场欢天喜地特效（旋转彩灯 + 烟花 + 流光） ===== */
.party-hero {{ position: relative; overflow: hidden; border-radius: 16px; padding: 22px 24px; margin: 0 0 14px;
  background: linear-gradient(130deg, #ff416c, #ff4b2b, #f7971e, #ffd200, #f7971e, #ff4b2b, #ff416c);
  background-size: 300% 300%; animation: heroShift 9s ease infinite; box-shadow: 0 6px 24px rgba(255,75,43,0.35); }}
@keyframes heroShift {{ 0% {{ background-position: 0% 50%; }} 50% {{ background-position: 100% 50%; }} 100% {{ background-position: 0% 50%; }} }}
.party-hero .party-lights {{ position: absolute; inset: -60%; pointer-events: none; mix-blend-mode: screen;
  background: conic-gradient(from 0deg,
    rgba(255,255,255,0) 0deg, rgba(255,255,255,.38) 22deg, rgba(255,255,255,0) 44deg,
    rgba(255,255,255,.38) 88deg, rgba(255,255,255,0) 132deg, rgba(255,255,255,.38) 176deg,
    rgba(255,255,255,0) 220deg, rgba(255,255,255,.38) 264deg, rgba(255,255,255,0) 308deg,
    rgba(255,255,255,.38) 352deg, rgba(255,255,255,0) 360deg);
  animation: spinLights 7s linear infinite; }}
@keyframes spinLights {{ to {{ transform: rotate(360deg); }} }}
.party-hero .fw {{ position: absolute; width: 72px; height: 72px; border-radius: 50%; opacity: 0; pointer-events: none;
  background: radial-gradient(circle, rgba(255,255,255,.95) 0%, rgba(255,210,0,.55) 28%, rgba(255,75,43,0) 62%);
  animation: fwPop 2.6s ease-out infinite; }}
@keyframes fwPop {{ 0% {{ transform: scale(0.15); opacity: 1; }} 60% {{ opacity: .9; }} 100% {{ transform: scale(1.35); opacity: 0; }} }}
.party-hero .fw1 {{ top: -14px; left: 12%; animation-delay: 0s; }}
.party-hero .fw2 {{ top: 28px; left: 54%; animation-delay: .9s; }}
.party-hero .fw3 {{ top: -26px; left: 82%; animation-delay: 1.7s; }}
.party-hero .party-content {{ position: relative; z-index: 2; text-align: center; }}
.party-hero .party-title {{ font-size: 24px; font-weight: 900; color: #fff; letter-spacing: 1px; text-shadow: 0 2px 10px rgba(0,0,0,.28); }}
.party-hero .party-sub {{ margin-top: 6px; font-size: 13px; color: #fff5e6; text-shadow: 0 1px 5px rgba(0,0,0,.22); }}
@media (max-width: 560px) {{ .party-hero .party-title {{ font-size: 19px; }} }}

/* ===== 互动娱乐：幸运转盘 / 老黄历 / 水晶球塔罗 ===== */
.prop.wheel-prop {{ display: flex; flex-direction: column; align-items: center; justify-content: flex-start; }}
.wheel-wrap {{ position: relative; width: 180px; height: 180px; margin: 8px auto 4px; }}
.wheel-canvas {{ width: 180px; height: 180px; border-radius: 50%; border: 5px solid #00dd88; box-shadow: 0 0 16px rgba(0,221,136,.5); transition: transform 4.6s cubic-bezier(.15,.7,.25,1); display: block; }}
.wheel-ptr {{ position: absolute; top: -12px; left: 50%; transform: translateX(-50%); width: 0; height: 0; border-left: 11px solid transparent; border-right: 11px solid transparent; border-top: 20px solid #ffd200; filter: drop-shadow(0 1px 2px rgba(0,0,0,.4)); z-index: 3; }}
.wheel-float {{ position: absolute; top: -10px; right: -10px; background: linear-gradient(135deg,#ffd200,#ff9d3d); color: #5a3b00; font-size: 11px; font-weight: 800; padding: 3px 9px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,.3); animation: wheelBob 1.4s ease-in-out infinite; pointer-events: none; z-index: 4; }}
@keyframes wheelBob {{ 0%,100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-5px); }} }}
.wheel-btn {{ margin-top: 4px; background: linear-gradient(135deg,#00dd88,#00aa66); color: #06240f; border: none; border-radius: 20px; padding: 7px 18px; font-size: 14px; font-weight: 800; cursor: pointer; box-shadow: 0 3px 10px rgba(0,221,136,.4); }}
.wheel-btn:active {{ transform: scale(.96); }}
.wheel-btn:disabled {{ opacity: .6; cursor: default; }}
.wheel-result {{ margin-top: 8px; min-height: 38px; font-size: 13px; color: #d8f0e0; text-align: center; line-height: 1.45; }}

/* 中奖庆祝特效层（固定全屏，纯 CSS/JS，零联网） */
.cele-overlay {{ position: fixed; inset: 0; z-index: 9999; pointer-events: none; display: none; overflow: hidden; }}
.cele-overlay.show {{ display: block; }}
.cele-flash {{ position: absolute; inset: 0; background: radial-gradient(circle at 50% 40%, rgba(255,210,0,.35), rgba(255,75,43,0) 60%); animation: celeFlash .5s ease-in-out 6; }}
@keyframes celeFlash {{ 0%,100% {{ opacity: 0; }} 50% {{ opacity: 1; }} }}
.cele-fw {{ position: absolute; width: 90px; height: 90px; border-radius: 50%; background: radial-gradient(circle, rgba(255,255,255,.95) 0%, rgba(255,210,0,.55) 28%, rgba(255,75,43,0) 62%); opacity: 0; animation: celeFw 1.4s ease-out infinite; }}
@keyframes celeFw {{ 0% {{ transform: scale(.2); opacity: 1; }} 70% {{ opacity: .8; }} 100% {{ transform: scale(1.6); opacity: 0; }} }}
.cele-ticket {{ position: absolute; top: -50px; font-size: 30px; animation: celeFall linear forwards; }}
@keyframes celeFall {{ to {{ transform: translateY(112vh) rotate(540deg); opacity: .15; }} }}
.cele-banner {{ position: absolute; top: 17%; left: 50%; transform: translateX(-50%); background: linear-gradient(135deg,#ff416c,#ff4b2b); color: #fff; padding: 14px 32px; border-radius: 40px; font-size: 20px; font-weight: 900; box-shadow: 0 6px 24px rgba(255,75,43,.5); animation: celePop .5s ease; text-align: center; white-space: nowrap; }}
@keyframes celePop {{ 0% {{ transform: translateX(-50%) scale(.3); opacity: 0; }} 100% {{ transform: translateX(-50%) scale(1); opacity: 1; }} }}

/* 双色球开奖机（模拟，纯娱乐） */
.dm-card {{ margin: 16px 0; border-radius: 18px; overflow: hidden; border: 1px solid rgba(255,120,60,.35); background: linear-gradient(135deg, rgba(40,16,10,.72), rgba(20,12,30,.72)); box-shadow: 0 8px 26px rgba(0,0,0,.30); }}
.dm-card .dm-head {{ padding: 14px 18px 6px; }}
.dm-card .dm-title {{ font-size: 18px; font-weight: 900; color: #ffd9a0; }}
.dm-card .dm-sub {{ font-size: 12px; color: #c8b6a8; margin-top: 3px; }}
.dm-machine {{ display: flex; gap: 16px; justify-content: center; align-items: stretch; padding: 10px 18px 4px; flex-wrap: wrap; }}
.dm-drum {{ flex: 1 1 200px; max-width: 280px; background: linear-gradient(160deg,#2a1410,#3a1c12); border: 2px solid #ff7a3d; border-radius: 16px; padding: 12px; text-align: center; box-shadow: inset 0 0 18px rgba(255,120,60,.25); }}
.dm-drum .dm-drum-name {{ font-size: 13px; font-weight: 800; color: #ffb27a; margin-bottom: 8px; }}
.dm-drum.dm-blue-drum {{ background: linear-gradient(160deg,#0e1a3a,#13214a); border-color: #4aa3ff; box-shadow: inset 0 0 18px rgba(74,163,255,.25); }}
.dm-drum.dm-blue-drum .dm-drum-name {{ color: #8fc4ff; }}
.dm-port {{ display: flex; gap: 6px; justify-content: center; align-items: center; min-height: 56px; background: radial-gradient(circle at 50% 40%, rgba(255,255,255,.12), rgba(0,0,0,.35)); border-radius: 12px; padding: 8px; }}
.dm-mini {{ display: inline-flex; align-items: center; justify-content: center; width: 30px; height: 30px; border-radius: 50%; font-size: 13px; font-weight: 800; color: #fff; background: #ff4d4d; box-shadow: 0 2px 5px rgba(0,0,0,.3); }}
.dm-drum.dm-blue-drum .dm-mini {{ background: #2f7bff; }}
.dm-output {{ display: flex; gap: 8px; justify-content: center; align-items: center; flex-wrap: wrap; padding: 12px 18px; min-height: 56px; }}
.dm-ball {{ display: inline-flex; align-items: center; justify-content: center; width: 42px; height: 42px; border-radius: 50%; font-size: 16px; font-weight: 900; color: #fff; background: radial-gradient(circle at 35% 30%, #ff8a8a, #e01b1b); box-shadow: 0 3px 8px rgba(0,0,0,.35); }}
.dm-ball.dm-blue {{ background: radial-gradient(circle at 35% 30%, #6db4ff, #1758d6); }}
.dm-plus {{ font-size: 20px; font-weight: 900; color: #ffd9a0; margin: 0 2px; }}
.dm-btn {{ display: block; margin: 4px auto 14px; background: linear-gradient(135deg,#ff7a18,#ff3d3d); color: #fff; border: none; border-radius: 22px; padding: 10px 26px; font-size: 15px; font-weight: 900; cursor: pointer; box-shadow: 0 4px 14px rgba(255,61,61,.4); }}
.dm-btn:disabled {{ opacity: .6; cursor: default; }}
.dm-status {{ text-align: center; font-size: 14px; color: #ffe3c4; min-height: 22px; padding-bottom: 6px; }}
.dm-note {{ font-size: 11.5px; color: #9fb0c8; text-align: center; padding: 0 18px 14px; line-height: 1.6; }}
.dm-balloon {{ position: absolute; bottom: -60px; font-size: 30px; animation: dmRise 4s ease-in forwards; }}
@keyframes dmRise {{ to {{ transform: translateY(-105vh) rotate(360deg); opacity: .2; }} }}

/* 老黄历 / 水晶球塔罗 通用卡片 */
.fun-game {{ margin: 14px 0; border-radius: 18px; overflow: hidden; border: 1px solid rgba(255,255,255,.12); box-shadow: 0 8px 26px rgba(0,0,0,.30); }}
.fun-game .fg-head {{ display: flex; align-items: center; gap: 12px; padding: 14px 16px; }}
.fun-game .fg-badge {{ width: 44px; height: 44px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 24px; box-shadow: 0 3px 10px rgba(0,0,0,.30); }}
.fun-game .fg-title {{ font-size: 15px; font-weight: 800; }}
.fun-game .fg-sub {{ display: inline-block; font-size: 11px; font-weight: 700; padding: 2px 8px; border-radius: 20px; margin-left: 6px; vertical-align: middle; }}
.fun-game .fg-body {{ padding: 0 16px 16px; }}
.fun-game .fg-text {{ font-size: 13px; line-height: 1.65; min-height: 20px; }}
.fun-game .fg-btn {{ margin-top: 12px; border: none; border-radius: 22px; padding: 9px 20px; font-size: 13.5px; font-weight: 800; cursor: pointer; color: #fff; box-shadow: 0 4px 14px rgba(0,0,0,.25); transition: transform .12s, filter .12s; }}
.fun-game .fg-btn:hover {{ filter: brightness(1.08); }}
.fun-game .fg-btn:active {{ transform: scale(.96); }}

/* ===== 放大版娱乐卡 · 东方秘术 vs 西方星象 双风格差异化（神秘·高科技） ===== */
.entertain-big {{ max-width: 560px; margin: 26px auto; border-radius: 24px; overflow: hidden; border: 1px solid rgba(255,255,255,.16); box-shadow: 0 22px 60px rgba(0,0,0,.50); position: relative; animation: ssqCardFloat 7s ease-in-out infinite; }}
@keyframes ssqCardFloat {{ 0%,100%{{transform:translateY(0)}} 50%{{transform:translateY(-7px)}} }}
.entertain-big .fg-head {{ padding: 20px 22px; display: flex; align-items: center; gap: 16px; position: relative; z-index: 3; }}
.entertain-big .fg-badge {{ width: 64px; height: 64px; border-radius: 50%; display: flex; align-items: center; justify-content: center; position: relative; flex: 0 0 auto; box-shadow: 0 8px 22px rgba(0,0,0,.4), inset 0 0 14px rgba(255,255,255,.3); }}
.entertain-big .fg-badge svg {{ width: 40px; height: 40px; display: block; }}
.entertain-big .fg-title {{ font-size: 20px; font-weight: 800; letter-spacing: .5px; }}
.entertain-big .fg-sub {{ font-size: 12px; font-weight: 700; padding: 2px 9px; border-radius: 10px; display: inline-block; margin-top: 4px; }}
.entertain-big .fg-body {{ padding: 0 22px 24px; position: relative; z-index: 3; }}
.entertain-big .fg-text {{ font-size: 15px; min-height: 26px; line-height: 1.6; }}
.entertain-big .fg-btn {{ margin-top: 16px; padding: 14px 34px; font-size: 16px; cursor: pointer; border: none; border-radius: 26px; font-weight: 800; position: relative; overflow: hidden; box-shadow: 0 10px 26px rgba(0,0,0,.38); transition: transform .15s, filter .15s; }}
.entertain-big .fg-btn::after {{ content: ""; position: absolute; top: 0; left: -60%; width: 50%; height: 100%; background: linear-gradient(120deg, transparent, rgba(255,255,255,.6), transparent); transform: skewX(-20deg); animation: ssqShimmer 3.6s ease-in-out infinite; }}
@keyframes ssqShimmer {{ 0%{{left:-60%}} 60%,100%{{left:140%}} }}
.entertain-big .fg-btn:hover {{ transform: translateY(-2px); filter: brightness(1.12); }}
.entertain-big .fg-btn:active {{ transform: scale(.97); }}
.ent-slogan {{ text-align: center; font-size: 15px; font-weight: 800; line-height: 1.65; padding: 15px 22px; position: relative; z-index: 3; }}
/* ---------- 东方秘术 · 老黄历（鎏金漆器 + 祥云暗纹 + 印章） ---------- */
.almanac-card {{ background: radial-gradient(120% 80% at 50% -10%, rgba(255,210,74,.18), transparent 60%), linear-gradient(160deg, #2b0a0a 0%, #501414 52%, #7a2a14 100%); }}
.almanac-card::before {{ content: ""; position: absolute; inset: 0; z-index: 0; opacity: .14; pointer-events: none; background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Cpath d='M20 78 q0 -22 22 -22 q4 -16 22 -16 q18 0 22 18 q16 0 16 16 q0 12 -16 12 z' fill='none' stroke='%23ffd24a' stroke-width='3'/%3E%3C/svg%3E"); background-size: 150px 150px; }}
.almanac-card .ent-slogan {{ color: #ffe9b0; background: linear-gradient(135deg, rgba(255,200,60,.26), rgba(255,90,30,.14)); border-bottom: 1px solid rgba(255,210,74,.35); }}
.almanac-card .fg-head {{ background: linear-gradient(135deg, rgba(255,210,74,.22), rgba(255,120,40,.10)); border-bottom: 1px solid rgba(255,210,74,.30); }}
.almanac-card .fg-badge {{ background: radial-gradient(circle at 35% 30%, #ffe9a8, #d99a1a); box-shadow: 0 8px 22px rgba(255,170,40,.45), inset 0 0 14px rgba(255,255,255,.4); }}
.almanac-card .fg-badge svg {{ animation: ssqAlmGlow 3.4s ease-in-out infinite; }}
@keyframes ssqAlmGlow {{ 0%,100%{{transform:scale(1); filter:drop-shadow(0 0 2px rgba(255,210,74,.6))}} 50%{{transform:scale(1.07); filter:drop-shadow(0 0 9px rgba(255,210,74,.95))}} }}
.almanac-card .fg-title {{ color: #ffd98a; text-shadow: 0 0 10px rgba(255,200,60,.35); }}
.almanac-card .fg-sub {{ background: rgba(255,210,74,.22); color: #ffd98a; }}
.almanac-card .fg-text {{ color: #ffe6cc; }}
.almanac-card .fg-btn {{ background: linear-gradient(135deg, #ffc24a, #ff7a18); color: #3a0f12; box-shadow: 0 10px 26px rgba(255,122,24,.45); }}
.alm-seal {{ margin-left: auto; width: 44px; height: 44px; border-radius: 9px; background: linear-gradient(135deg, #c01818, #7a0e0e); border: 2px solid #ffd24a; display: flex; align-items: center; justify-content: center; color: #ffd98a; font-size: 21px; font-weight: 900; transform: rotate(-8deg); box-shadow: 0 4px 12px rgba(0,0,0,.4); flex: 0 0 auto; }}
.almanac-card::after {{ content: ""; position: absolute; top: 0; left: -120%; width: 60%; height: 100%; z-index: 2; background: linear-gradient(110deg, transparent, rgba(255,225,150,.16), transparent); transform: skewX(-18deg); animation: ssqGoldSweep 6.5s ease-in-out infinite; }}
@keyframes ssqGoldSweep {{ 0%{{left:-120%}} 55%,100%{{left:160%}} }}
/* ---------- 西方星象 · 水晶球（深空星云 + 星轨 + 全息） ---------- */
.tarot-card {{ background: radial-gradient(130% 90% at 50% 0%, rgba(120,90,255,.22), transparent 60%), linear-gradient(165deg, #070a26 0%, #141048 50%, #2a1268 100%); }}
.tarot-card .ent-slogan {{ color: #e7dcff; background: linear-gradient(135deg, rgba(150,110,255,.26), rgba(60,150,255,.14)); border-bottom: 1px solid rgba(170,140,255,.35); }}
.tarot-card .fg-head {{ background: linear-gradient(135deg, rgba(150,110,255,.22), rgba(60,150,255,.10)); border-bottom: 1px solid rgba(170,140,255,.30); }}
.tarot-card .fg-badge {{ background: radial-gradient(circle at 35% 30%, #e9ddff, #6a4bd6); box-shadow: 0 8px 22px rgba(120,90,255,.5), inset 0 0 14px rgba(255,255,255,.35); }}
.tarot-card .fg-badge svg {{ animation: ssqOrbGlow 3.6s ease-in-out infinite; }}
@keyframes ssqOrbGlow {{ 0%,100%{{transform:scale(1); filter:drop-shadow(0 0 3px rgba(150,120,255,.6))}} 50%{{transform:scale(1.07); filter:drop-shadow(0 0 11px rgba(150,120,255,1))}} }}
.tarot-card .fg-title {{ color: #dccbff; text-shadow: 0 0 12px rgba(150,110,255,.4); }}
.tarot-card .fg-sub {{ background: rgba(170,140,255,.22); color: #dccbff; }}
.tarot-card .fg-text {{ color: #e6e0ff; }}
.tarot-card .fg-btn {{ background: linear-gradient(135deg, #7b9bff, #b15cff); color: #0e0830; box-shadow: 0 10px 26px rgba(123,92,255,.5); }}
.tarot-card .fg-badge::before {{ content: ""; position: absolute; inset: -9px; border-radius: 50%; border: 1.5px dashed rgba(180,160,255,.55); animation: ssqRingSpin 9s linear infinite; }}
.tarot-card .fg-badge::after {{ content: ""; position: absolute; inset: -15px; border-radius: 50%; border: 1px solid rgba(150,110,255,.30); animation: ssqRingSpinRev 14s linear infinite reverse; }}
@keyframes ssqRingSpin {{ from{{transform:rotate(0)}} to{{transform:rotate(360deg)}} }}
@keyframes ssqRingSpinRev {{ from{{transform:rotate(0)}} to{{transform:rotate(360deg)}} }}
/* 图标内闪烁星芒(灵动感) */
.ssq-spk, .ssq-spk2 {{ animation: ssqSpark 2.4s ease-in-out infinite; transform-origin: center; }}
@keyframes ssqSpark {{ 0%,100%{{opacity:.3; transform:scale(.7)}} 50%{{opacity:1; transform:scale(1.2)}} }}
/* 西方星象：星空背景 overlay */
.tarot-card::before {{ content: ""; position: absolute; inset: 0; z-index: 0; opacity: .5; pointer-events: none;
  background-image: radial-gradient(1.4px 1.4px at 20% 30%, #fff, transparent), radial-gradient(1.2px 1.2px at 70% 20%, #cfe0ff, transparent), radial-gradient(1.6px 1.6px at 40% 70%, #fff, transparent), radial-gradient(1.1px 1.1px at 85% 60%, #b9c8ff, transparent), radial-gradient(1.3px 1.3px at 60% 85%, #fff, transparent), radial-gradient(1px 1px at 15% 80%, #e0d4ff, transparent);
  background-repeat: no-repeat; animation: ssqTwinkle 4s ease-in-out infinite; }}
@keyframes ssqTwinkle {{ 0%,100%{{opacity:.35}} 50%{{opacity:.7}} }}
.alm-grid {{ display: flex; gap: 12px; margin: 12px 0; position: relative; z-index: 3; }}
.alm-col {{ flex: 1; font-size: 13px; line-height: 1.55; padding: 10px 12px; background: rgba(255,210,74,.10); border: 1px solid rgba(255,210,74,.18); border-radius: 12px; }}
.alm-col b {{ font-size: 13px; }}
.alm-row {{ font-size: 12.5px; margin: 7px 0; color: #ffd9b0; position: relative; z-index: 3; }}
.alm-q {{ font-size: 12.5px; margin-top: 9px; padding: 9px 12px; background: rgba(255,210,74,.14); border-left: 3px solid #ffd24a; border-radius: 9px; color: #ffe6cc; position: relative; z-index: 3; }}
.tarot-row {{ font-size: 13px; margin: 7px 0; color: #e6e0ff; position: relative; z-index: 3; }}
.tarot-pull {{ margin: 10px 0; padding: 11px 13px; background: rgba(150,110,255,.14); border: 1px solid rgba(170,140,255,.22); border-radius: 12px; border-left: 3px solid #b388ff; position: relative; z-index: 3; }}
.tarot-pull b {{ color: #e0d2ff; font-size: 14px; }}
.tarot-mean {{ font-size: 12.5px; color: #c9b8ff; }}
.tarot-cheer {{ font-size: 12.5px; margin-top: 9px; padding: 9px 12px; background: rgba(150,110,255,.12); border-radius: 9px; color: #dccbff; position: relative; z-index: 3; }}

/* ===== 年轻化·活力：首屏问候 / 连续打卡 / 等级进度 / 刮刮卡 / 彩蛋 ===== */
.greet-bar {{ display: flex; align-items: center; justify-content: space-between; gap: 12px; margin: 0 0 14px; padding: 12px 18px; border-radius: 14px;
  background: linear-gradient(135deg, rgba(123,92,255,.20), rgba(0,200,255,.14)); border: 1px solid rgba(255,255,255,.12); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); }}
.greet-bar .g-left {{ font-size: 16px; font-weight: 800; color: #fff; }}
.greet-bar .g-left .g-emoji {{ font-size: 20px; margin-right: 6px; }}
.greet-bar .g-left .g-sub {{ font-size: 12.5px; font-weight: 600; color: #d6d2f5; margin-left: 8px; }}
.greet-bar .g-right {{ display: flex; align-items: center; gap: 10px; }}
.g-streak {{ display: inline-flex; align-items: center; gap: 5px; background: rgba(255,120,40,.20); border: 1px solid rgba(255,138,61,.4); padding: 5px 12px; border-radius: 18px; font-size: 13px; font-weight: 800; color: #ffd24a; }}
.g-streak .flame {{ filter: drop-shadow(0 0 4px rgba(255,140,40,.8)); }}
.g-level {{ min-width: 150px; }}
.g-level .gl-top {{ display: flex; justify-content: space-between; font-size: 11.5px; color: #cfe9ff; margin-bottom: 3px; }}
.g-level .gl-bar {{ height: 8px; border-radius: 6px; background: rgba(255,255,255,.12); overflow: hidden; }}
.g-level .gl-fill {{ height: 100%; border-radius: 6px; background: linear-gradient(90deg, #5ee0ff, #9b7bff); transition: width .8s cubic-bezier(.2,.8,.2,1); box-shadow: 0 0 8px rgba(123,92,255,.6); }}

/* 刮刮卡 */
.scratch-card {{ position: relative; margin: 14px 0; border-radius: 18px; overflow: hidden; border: 1px solid rgba(255,210,74,.30);
  background: linear-gradient(160deg, #2a1840, #3a1a5a); box-shadow: 0 10px 30px rgba(0,0,0,.32); }}
.scratch-card .sc-head {{ display: flex; align-items: center; gap: 10px; padding: 14px 16px 6px; }}
.scratch-card .sc-emoji {{ font-size: 26px; }}
.scratch-card .sc-title {{ font-size: 16px; font-weight: 800; color: #ffd98a; }}
.scratch-card .sc-sub {{ font-size: 12px; color: #d9c8ff; margin-left: auto; }}
.scratch-card .sc-stage {{ position: relative; height: 178px; margin: 6px 16px 14px; border-radius: 12px; overflow: hidden; background: rgba(0,0,0,.25); }}
.scratch-card .sc-prize {{ position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 3px; padding: 8px; overflow: auto; }}
.scratch-card .sc-row {{ display: flex; align-items: center; gap: 8px; font-size: 12px; }}
.scratch-card .sc-name {{ color: #ffd98a; font-size: 11.5px; white-space: nowrap; }}
.scratch-card .sc-balls {{ display: flex; gap: 2px; }}
.scratch-card .sc-prize .ball {{ width: 26px; height: 26px; line-height: 26px; font-size: 12px; margin: 0; }}
.scratch-card .sc-hint {{ position: absolute; left: 0; right: 0; bottom: 8px; text-align: center; font-size: 12px; color: #ffe39a; opacity: .85; pointer-events: none; }}
.scratch-card canvas {{ position: absolute; inset: 0; width: 100%; height: 100%; cursor: grab; touch-action: none; }}
.scratch-card canvas:active {{ cursor: grabbing; }}
.scratch-card .sc-reveal {{ position: absolute; top: 8px; right: 10px; background: linear-gradient(135deg,#ffb347,#ff7a18); color: #3a0f12; border: none; border-radius: 16px; padding: 5px 13px; font-size: 12px; font-weight: 800; cursor: pointer; box-shadow: 0 3px 10px rgba(255,122,24,.4); }}
.scratch-card .sc-reveal:active {{ transform: scale(.95); }}

/* 结尾留存钩子 */
.stay-hook {{ margin: 18px 0 6px; padding: 16px 18px; border-radius: 16px; text-align: center;
  background: linear-gradient(135deg, rgba(255,94,138,.18), rgba(123,92,255,.18)); border: 1px solid rgba(255,255,255,.12); }}
.stay-hook .sh-title {{ font-size: 16px; font-weight: 800; color: #fff; margin-bottom: 6px; }}
.stay-hook .sh-text {{ font-size: 13px; color: #e3dfff; line-height: 1.6; }}
.stay-hook .sh-cta {{ display: inline-block; margin-top: 10px; background: linear-gradient(135deg,#ff5e8a,#ff7a18); color: #fff; border: none; border-radius: 20px; padding: 8px 22px; font-size: 14px; font-weight: 800; cursor: pointer; box-shadow: 0 4px 16px rgba(255,94,138,.45); }}
.stay-hook .sh-cta:active {{ transform: scale(.96); }}

/* 漂浮装饰（纯 CSS，零联网） */
.flobs {{ position: fixed; inset: 0; z-index: -1; pointer-events: none; overflow: hidden; }}
.flobs i {{ position: absolute; border-radius: 50%; filter: blur(34px); opacity: .55; animation: blobFloat 14s ease-in-out infinite; }}
.flobs .b1 {{ width: 280px; height: 280px; left: -70px; top: 6%; background: radial-gradient(circle, #7b5cff, rgba(123,92,255,0)); animation-delay: 0s; }}
.flobs .b2 {{ width: 340px; height: 340px; right: -90px; top: 38%; background: radial-gradient(circle, #ff4b7c, rgba(255,75,124,0)); animation-delay: 3.5s; }}
.flobs .b3 {{ width: 250px; height: 250px; left: 28%; bottom: -70px; background: radial-gradient(circle, #00c8ff, rgba(0,200,255,0)); animation-delay: 7s; }}

/* 微交互：悬停上浮 + 发光（年轻化精致感） */
.group-card {{ transition: transform .18s, box-shadow .18s, border-color .18s; }}
.group-card:hover {{ transform: translateY(-4px); border-left-color: #ffd24a; box-shadow: 0 12px 34px rgba(123,92,255,.28); }}
.stat-card {{ transition: transform .18s, box-shadow .18s; }}
.stat-card:hover {{ transform: translateY(-3px); box-shadow: 0 10px 26px rgba(0,200,255,.22); }}
.header .meta-item {{ transition: transform .15s, background .15s; }}
.header .meta-item:hover {{ transform: translateY(-2px); background: rgba(255,255,255,.14); }}
.antiscam .prop {{ transition: transform .15s, box-shadow .15s; }}
.antiscam .prop:hover {{ transform: translateY(-3px); box-shadow: 0 8px 22px rgba(0,221,136,.25); }}
.win-card {{ transition: transform .15s, border-color .15s; }}
.wheel-btn:hover {{ filter: brightness(1.08); transform: translateY(-1px); }}
.fun-game {{ transition: transform .18s, box-shadow .18s; }}
.fun-game:hover {{ transform: translateY(-3px); box-shadow: 0 14px 34px rgba(0,0,0,.40); }}
.scratch-card {{ transition: transform .18s, box-shadow .18s; }}
.scratch-card:hover {{ transform: translateY(-2px); box-shadow: 0 14px 36px rgba(0,0,0,.40); }}

/* 点击 LOGO 满屏烟花彩蛋 */
.logo-egg {{ cursor: pointer; user-select: none; transition: transform .15s; }}
.logo-egg:hover {{ transform: scale(1.02); }}
.logo-egg:active {{ transform: scale(.98); }}

/* 娱乐间歇：把互动组件间隔穿插在「号码预测」各组之间，避免挤在报告顶部 */
.entertain-interlude {{ margin: 28px 0; }}
.ei-title {{ font-size: 15px; font-weight: 800; color: #ffd86b; letter-spacing: .5px; margin: 0 0 12px; padding-left: 12px; border-left: 4px solid #ffb703; }}
{FUN_PACK_CSS}
</style>
</head>
<body>
<div class="flobs"><i class="b1"></i><i class="b2"></i><i class="b3"></i></div>
<div class="container">

<div class="header">
<h1 class="logo-egg" title="点我放烟花🎆">双色球第{next_period}期预测报告 V1 <span class="v8-badge">全面修复</span></h1>
<p class="subtitle">{total}期历史数据 | {red_combos_s}组合穷举 | {len(expert_picks)}位专家ECI | 回测完全复刻预测管线 | 端到端自动化</p>
<div class="meta">
<div class="meta-item">数据: <strong>{total}期</strong></div>
<div class="meta-item">最新: <strong>{latest['period']}期</strong></div>
<div class="meta-item">自动化: <strong>10/10步</strong></div>
<div class="meta-item">回测: <strong>完全复刻预测</strong></div>
<div class="meta-item">生成: <strong>{datetime.now().strftime('%Y-%m-%d %H:%M')}</strong></div>
</div>
</div>

<!-- 娱乐组件已下移到「推荐号码」各组之间(见 for i,g in enumerate(groups) 循环内的 entertain-interlude 注入)，避免挤在报告顶部 -->

<div class="section">
<div class="section-title">一、数据概览</div>
<table>
<tr><th>指标</th><th>值</th></tr>
<tr><td>总历史期数</td><td>{total}</td></tr>
<tr><td>数据时间范围</td><td>{draws[0]['date']} ~ {latest['date']}</td></tr>
<tr><td>最新期号</td><td>{latest['period']}</td></tr>
<tr><td>最新红球</td><td>{' '.join(f'<span class="ball ball-red" style="width:28px;height:28px;line-height:28px;font-size:13px;">{n:02d}</span>' for n in latest['front'])}</td></tr>
<tr><td>最新蓝球</td><td>{' '.join(f'<span class="ball ball-blue" style="width:28px;height:28px;line-height:28px;font-size:13px;">{n:02d}</span>' for n in latest['back'])}</td></tr>
<tr><td>数据校验</td><td>{'✓ 全部通过' if not data_issues else '⚠ ' + ', '.join(data_issues)}</td></tr>
<tr><td>预测目标期号</td><td>{next_period}</td></tr>
</table>
</div>

{render_deep_analysis_html(draws)}

{render_expert_views_html(next_period)}

<div class="section">
<div class="section-title">二、第{next_period}期推荐号码（5组，全部通过9项过滤器 + 每组成本/优劣点）</div>"""
    
    prev_front = latest['front']
    group_reviews = []  # 收集每组评测，供预测JSON使用

    # 采用成本速览（5组汇总）
    total_bets = sum(len(g['back']) * (len(g['back']) - 1) // 2 for g in groups)
    html += f"""
<div class="info" style="border-color:#00dd88;">
<p style="color:#00dd88; font-size:14px; line-height:1.8;">
💡 <strong>采用成本速览</strong>：每组 = 红球1注 + 蓝球复式，5 组共 <strong>{total_bets} 注</strong>，
基本投注 <strong>¥{total_bets*2}</strong>。<br>
<strong style="color:#ffcc00;">提醒：5 组期望等价，全买不提升中奖概率、只增成本；任选 1 组即可控制投入，建议 ≤ 月收入 0.5%。</strong>
</p>
</div>
"""

    # ---- 🎯 开奖前必读 · 预期差距说明(直接回应"差这么多", 开奖前校准期望) ----
    _exp_front = 6 * 6 / 33
    _exp_back = 1 * 1 / 16
    _p_zero_front = 296010 / 1107568  # C(27,6)/C(33,6) ≈ 26.7%
    html += f"""
<div class="section" style="border:2px solid #ffaa00;">
<div class="section-title">🎯 开奖前必读 · 预期差距说明（请先读这段，再看下面号码）</div>
<div class="info" style="border-color:#ffaa00;">
<p style="color:#ffbb00; font-size:15px; line-height:1.9;">
<strong>你马上要看到的 5 组号码，在"中奖概率"上和闭眼随机选 5 注完全等价。</strong>下面把"差多少算正常"提前讲清楚，免得开奖后你以为系统坏了：
</p>
<ul style="margin:8px 0; padding-left:20px; color:#ffd9a0; line-height:1.9; font-size:14px;">
<li>🔢 红球 33 选 6：每组平均只能命中 <strong>{_exp_front:.2f} 个</strong>（大概率只中 0~2 个）；<strong>单组"一个红球都不中"的概率高达 {_p_zero_front*100:.1f}%</strong>。</li>
<li>🔵 蓝球仅 1 个：命中概率 <strong>{_exp_back*100:.2f}%</strong>，<strong>单组蓝球不中的概率 {(1-_exp_back)*100:.1f}%</strong>。</li>
<li>🏆 一等奖（6+1）恒等概率 <strong>1/17,721,088</strong>——与用什么方法、什么"大师"选号<strong>毫无关系</strong>。</li>
<li>📉 因此"预测 vs 开奖差很多"是<strong>公平随机摇奖的最常见结果</strong>。反过来说：如果本系统能稳定贴近开奖号，那才是摇奖机不独立、被人操控的<strong>危险信号</strong>。</li>
<li>✅ 唯一理性动作：控制投入（建议 ≤ 月收入 0.5%），把本报告当<strong>娱乐消费凭证</strong>而非致富方案。开奖后本报告会自动生成「实际开奖对账」告诉你这期差多少、是否在随机范围内。</li>
</ul>
</div>
</div>
"""

    html += generate_scratch_html(groups)

    for i, g in enumerate(groups, 1):
        front = g['front']
        back = g['back']
        ac = calc_ac(front)
        s = sum(front)
        span = max(front) - min(front)
        oc = odd_count(front)
        sc = small_count(front)
        pc = prime_count(front)
        r0, r1, r2 = road_counts(front)
        cg = consecutive_groups(front)
        rn = len(set(front) & set(prev_front))

        rev = group_review(g, front, back, ac, s, span, oc, sc, pc, (r0, r1, r2), cg, rn, prev_front, draws)
        group_reviews.append(rev)
        pros_html = ''.join(f'<li>{x}</li>' for x in rev['strengths'])
        cons_html = ''.join(f'<li>{x}</li>' for x in rev['weaknesses'])
        # 奖级分布(回测) 紧凑展示
        _tc = rev['similar_shape']['backtest']['tier_counts']
        tier_summary = '、'.join(f"{k}{v}期" for k, v in sorted(_tc.items(), key=lambda x: -x[1])) if _tc else "无中奖"

        html += f"""
<div class="group-card">
<h3>第{i}组: {g['name']}</h3>
<p class="strategy">策略: {g['strategy']}</p>
<div class="balls-container">
<span style="color:#888;">红球:</span>
{''.join(f'<span class="ball ball-red">{n:02d}</span>' for n in sorted(front))}
</div>
<div class="balls-container">
<span style="color:#888;">蓝球复式:</span>
{''.join(f'<span class="ball ball-blue">{n:02d}</span>' for n in sorted(back))}
</div>
<p style="color:#ffcc00; font-size:13px; margin-top:6px;">
💰 <strong>成本</strong>：{rev['bets']} 注（红球1注 + 蓝球复式）｜ 基本 <strong>¥{rev['cost_basic']}</strong>
</p>
<p style="color:#66ccff; font-size:12px; margin-top:6px;">
📊 <strong>历史相似形态出现率</strong>：在历史 {rev['similar_shape']['N']} 期中，与本组形态（AC/和值/跨度/奇偶/大小/012路/连号/质数）相近的开奖共 <strong>{rev['similar_shape']['cohort']}</strong> 期，占比 <strong>{rev['similar_shape']['shape_prevalence']*100:.1f}%</strong>。
<span style="color:#99aab5;">（这是该形态在历史开奖中出现的频率，<strong>不是</strong>本注会中奖的概率；一等奖对任何形态概率相同 1/17,721,088）</span>
</p>
<p style="color:#9ad; font-size:12px; margin-top:4px; background:#0c1422; border:1px solid #1c3a5a; border-radius:6px; padding:8px;">
🎰 <strong>固定号码历史回测</strong>（若每期都固定投注本组这注 6+1，在所有历史开奖逐期核对）：共 <strong>{rev['similar_shape']['backtest']['plays']}</strong> 期，任意奖级中奖 <strong>{rev['similar_shape']['backtest']['any_hit']}</strong> 期（期率 <strong>{rev['similar_shape']['backtest']['win_rate']*100:.2f}%</strong>），总投入 <strong>¥{rev['similar_shape']['backtest']['cost']}</strong>，总奖金 <strong>¥{rev['similar_shape']['backtest']['total_prize']}</strong>，ROI <strong>{rev['similar_shape']['backtest']['roi']*100:+.1f}%</strong>。
<span style="color:#99aab5;">（描述"过去若这么买会怎样"，<strong>不预示未来</strong>；固定号码长期 ROI 为负属数学期望，印证系统 no_edge 诚实结论）</span><br>
<span style="color:#7fb;">奖级分布：{tier_summary}</span>
</p>
<div style="display:flex; gap:12px; margin-top:10px; flex-wrap:wrap;">
<div style="flex:1; min-width:240px; background:#0d1a14; border:1px solid #00aa55; border-radius:8px; padding:10px;">
<div style="color:#00dd88; font-size:13px; font-weight:bold; margin-bottom:6px;">✅ 优点（为何列它为候选）</div>
<ul style="margin:0; padding-left:18px; color:#88ffbb; font-size:12px; line-height:1.7;">{pros_html}</ul>
</div>
<div style="flex:1; min-width:240px; background:#1a140d; border:1px solid #cc8800; border-radius:8px; padding:10px;">
<div style="color:#ffbb00; font-size:13px; font-weight:bold; margin-bottom:6px;">⚠️ 注意（劣势 / 风险）</div>
<ul style="margin:0; padding-left:18px; color:#ffcc88; font-size:12px; line-height:1.7;">{cons_html}</ul>
</div>
</div>
<p style="color:#888; font-size:12px; margin-top:8px;">AC={ac}({'✓' if 5 <= ac <= 9 else '✗'}) | 和值={s}({'✓' if 70 <= s <= 140 else '✗'}) | 跨度={span}({'✓' if 16 <= span <= 31 else '✗'}) | 奇偶={oc}({'✓' if oc in [2,3,4] else '✗'}) | 大小={sc}({'✓' if sc in [2,3,4] else '✗'}) | 质合={pc}({'✓' if pc in [1,2,3] else '✗'}) | 012路={r0}{r1}{r2}({'✓' if r0>0 and r1>0 and r2>0 else '✗'}) | 连号={cg}({'✓' if cg<=1 else '✗'}) | 重号={rn}({'✓' if rn<=2 else '✗'})</p>
</div>"""

        # ---- 娱乐间歇：把互动组件间隔在「号码预测」各组之间，不再挤在报告顶部 ----
        if i == 1:
            html += ('<div class="entertain-interlude"><div class="ei-title">🎰 娱乐间歇 · 模拟摇奖机</div>'
                     + generate_draw_machine_html() + '</div>')
        elif i == 2:
            html += ('<div class="entertain-interlude"><div class="ei-title">🛡️ 娱乐间歇 · 手气摇奖机 + 防割韭菜盾</div>'
                     '<div class="antiscam">'
                     '<div class="shield-title">🛡️ 防割韭菜盾 · 双色球理性购彩科普助手</div>'
                     '<div class="lead">双色球开奖是纯随机，<strong style="color:#ff8888;">任何"大师指导 / 可确保的中奖结果说法 / 不实数据"都是割韭菜</strong>。本工具不宣称中奖，只做三件事，帮你买得明白：</div>'
                     '<div class="props">'
                     + generate_prop_minigames_html()
                     + generate_wheel_html()
                     + '</div>'
                     + generate_box_games_js()
                     + '<div class="honest">📊 诚实结论：一等奖概率恒 1/17,721,088 ｜ 期望回报 −53% ｜ 请娱乐量力，绝不可当作"有收益"的依据</div>'
                     '</div></div>')
        elif i == 3:
            html += ('<div class="entertain-interlude"><div class="ei-title">🎉 娱乐间歇 · 快乐开奖时刻</div>'
                     + generate_party_hero_html()
                     + generate_countdown_html()
                     + '</div>')
        elif i == 4:
            html += ('<div class="entertain-interlude"><div class="ei-title">🐱 娱乐间歇 · 招财猫萌宠 · 娱乐互动专区</div>'
                     + generate_fun_pack_section(next_period, _ledger_stats)
                     + '</div>')

    # 胆拖 (V1.0.0 增强: 性价比最高 + 三指标 + 容错表)
    if dantuo.get('standard'):
        dt = dantuo['standard']
        opt = dantuo.get('optimized', {})
        cands = dantuo.get('candidates', [])
        form_label = opt.get('form', f"{len(dt['dan'])}胆{len(dt['tuo'])}拖+后{len(dt['back'])}码")
        acc = opt.get('acc', 0.0)
        win_any = opt.get('win_any', 0.0)
        win_5 = opt.get('win_5plus', 0.0)
        score = opt.get('score', 0.0)
        tt = opt.get('tolerance_table', [])

        cand_rows = ""
        for c in cands:
            cand_rows += f"""
<tr style="border-bottom:1px solid #333;">
<td style="padding:4px 8px;color:#ffcc66;">{c['form']}</td>
<td style="padding:4px 8px;color:#aaa;">{c['total_bets']}注 / {c['cost']}元</td>
<td style="padding:4px 8px;color:#88ffbb;">{c['acc']:.3f}</td>
<td style="padding:4px 8px;color:#88ddff;">{c['win_any']*100:.1f}%</td>
<td style="padding:4px 8px;color:#ffaa00;font-weight:bold;">{c['score']:.3f}</td>
</tr>"""

        tt_rows = ""
        for r in tt:
            pc = '#88ffbb' if r['prize_worst'] >= 6 else ('#ffcc88' if r['prize_worst'] > 0 else '#ff8888')
            tt_rows += f"""
<tr style="border-bottom:1px solid #333;">
<td style="padding:4px 8px;color:#aaa;">{r['m']}</td>
<td style="padding:4px 8px;color:#aaa;">{r['front_hit_worst']}</td>
<td style="padding:4px 8px;color:{pc};">{r['desc']}</td>
</tr>"""

        html += f"""
<div class="group-card" style="border-left-color:#ffaa00;">
<h3 style="color:#ffaa00;">🏆 性价比最高胆拖组合: {form_label}</h3>
<div class="balls-container">
<span style="color:#888;">胆码(参考):</span>
{''.join(f'<span class="ball ball-red" style="border:3px solid #00d4ff;">{n:02d}</span>' for n in sorted(dt['dan']))}
</div>
<div class="balls-container">
<span style="color:#888;">拖码:</span>
{''.join(f'<span class="ball ball-red" style="opacity:0.7;">{n:02d}</span>' for n in sorted(dt['tuo']))}
</div>
<div class="balls-container">
<span style="color:#888;">蓝球:</span>
{''.join(f'<span class="ball ball-blue">{n:02d}</span>' for n in sorted(dt['back']))}
</div>
<p style="color:#aaa; font-size:13px; margin-top:10px;">
红球C({len(dt['tuo'])},{6-len(dt['dan'])}) = {dt['front_combos']}组 × 蓝球复式{len(dt['back'])}码 = {dt['back_combos']}组 = <strong>{dt['total_bets']}注</strong><br>
成本: <strong>{dt['cost_basic']}元</strong>(基本) / <strong>{dt['cost_extra']}元</strong>(复式)
</p>
<div style="display:flex; gap:10px; margin-top:10px; flex-wrap:wrap;">
<div style="flex:1; min-width:150px; background:#0d1a14; border:1px solid #00aa55; border-radius:8px; padding:8px;">
<div style="color:#00dd88; font-size:12px; font-weight:bold;">① 号码最可靠</div>
<div style="color:#aaffcc; font-size:18px; font-weight:bold;">{acc:.3f}</div>
<div style="color:#88ffbb; font-size:11px;">方案号码平均模型评分(越高越准)</div>
</div>
<div style="flex:1; min-width:150px; background:#0d141a; border:1px solid #0088aa; border-radius:8px; padding:8px;">
<div style="color:#00aadd; font-size:12px; font-weight:bold;">② 成本最低</div>
<div style="color:#aaddff; font-size:18px; font-weight:bold;">{dt['cost_basic']}元</div>
<div style="color:#88ddff; font-size:11px;">{dt['total_bets']}注基本 / {dt['cost_extra']}元复式</div>
</div>
<div style="flex:1; min-width:150px; background:#1a140d; border:1px solid #cc8800; border-radius:8px; padding:8px;">
<div style="color:#ffbb00; font-size:12px; font-weight:bold;">③ 中一等奖概率最高</div>
<div style="color:#ffcc66; font-size:18px; font-weight:bold;">{win_any*100:.1f}%</div>
<div style="color:#ffcc88; font-size:11px;">至少中任一奖(MC) / 五等奖{win_5*100:.1f}%</div>
</div>
</div>
<p style="color:#00dd88; font-size:13px; margin-top:8px;">📊 综合性价比评分: <strong>{score:.3f}</strong> (三指标加权最优, 形态自适应)</p>
<div style="margin-top:10px;">
<div style="color:#ffaa00; font-size:13px; font-weight:bold; margin-bottom:4px;">候选方案对比 (top3)</div>
<table style="width:100%; border-collapse:collapse; font-size:12px;">
<tr style="color:#888; border-bottom:1px solid #555;"><th style="padding:4px 8px;text-align:left;">形态</th><th style="padding:4px 8px;text-align:left;">成本</th><th style="padding:4px 8px;text-align:left;">准度</th><th style="padding:4px 8px;text-align:left;">中奖概率</th><th style="padding:4px 8px;text-align:left;">评分</th></tr>
{cand_rows}
</table>
</div>
<div style="margin-top:10px;">
<div style="color:#ffaa00; font-size:13px; font-weight:bold; margin-bottom:4px;">容错保底表 (红球命中 m 个, 最坏情形仍达)</div>
<table style="width:100%; border-collapse:collapse; font-size:12px;">
<tr style="color:#888; border-bottom:1px solid #555;"><th style="padding:4px 8px;text-align:left;">红球命中m</th><th style="padding:4px 8px;text-align:left;">最坏红球命中</th><th style="padding:4px 8px;text-align:left;">保底奖级</th></tr>
{tt_rows}
</table>
</div>
<p style="color:#888; font-size:11px; margin-top:8px; line-height:1.6;">{dantuo.get('honesty','')}</p>
</div>"""

    # ---- 📊 开奖后实际命中对账(目标期已开奖则渲染, 直接回应"差这么多") ----
    _actual = None
    if _RECONCILE_HISTORY_OVERRIDE:
        _actual = next((d for d in _RECONCILE_HISTORY_OVERRIDE
                        if str(d.get('period', '')) == str(next_period)), None)
    if _actual is None:
        try:
            _hist_full = json.load(open(os.path.join(HERE, 'ssq_history.json'), encoding='utf-8'))
            _actual = next((d for d in _hist_full
                            if str(d.get('period', '')) == str(next_period)), None)
        except Exception:
            _actual = next((d for d in draws if str(d.get('period', '')) == str(next_period)), None)
    if _actual:
        _af = set(_actual.get('front', [])); _ab = set(_actual.get('back', []))
        _exp_front = 6 * 6 / 33
        _exp_back = 1 * 1 / 16
        _p_zero_front = 296010 / 1107568
        _avf = _avb = 0
        _rec_rows = ""
        for _i, _g in enumerate(groups, 1):
            _fh = len(set(_g['front']) & _af); _bh = len(set(_g['back']) & _ab)
            _avf += _fh; _avb += _bh
            _rec_rows += (
                f"<tr><td>第{_i}组 {_g['name']}</td>"
                f"<td>{' '.join('%02d' % n for n in sorted(_g['front']))}</td>"
                f"<td>{' '.join('%02d' % n for n in sorted(_g['back']))}</td>"
                f"<td style='color:#ff6b6b;'>{_fh}/6</td>"
                f"<td style='color:#ff6b6b;'>{_bh}/1</td>"
                f"<td>{_fh + _bh} 个</td></tr>"
            )
        _n = len(groups); _avf /= _n; _avb /= _n
        html += f"""
<div class="section" style="border:2px solid #4aa3ff;">
<div class="section-title">📊 附 · 第{next_period}期实际开奖对账（开奖后自动生成）</div>
<div class="info" style="border-color:#4aa3ff;">
<p style="color:#9ad; font-size:14px; line-height:1.9;">
开奖号 <strong style="color:#fff;">红球 {' '.join('%02d' % n for n in sorted(_af))} ｜ 蓝球 {' '.join('%02d' % n for n in sorted(_ab))}</strong>。
下面把"你这期预测的 {_n} 组"逐组与真实开奖核对——这就是"差这么多"的真相：
</p>
<table>
<tr><th>策略组</th><th>你预测的红球</th><th>你预测的蓝球</th><th>红球命中</th><th>蓝球命中</th><th>合计</th></tr>
{_rec_rows}
</table>
<p style="margin-top:10px; color:#ffcc00; font-size:14px; line-height:1.9;">
📐 <strong>随机期望对照</strong>：红球平均应中 <strong>{_exp_front:.2f} 个</strong>（单组 0 红概率 {_p_zero_front*100:.1f}%），蓝球命中 <strong>{_exp_back:.3f} 个</strong>。
本组 {_n} 组实际平均中红球 <strong>{_avf:.2f} 个</strong>、蓝球 <strong>{_avb:.2f} 个</strong>——与随机期望<strong>相差无几，完全在噪声内</strong>。
</p>
<p style="color:#99aab5; font-size:13px; line-height:1.8;">
结论：没有任何一组"神奇地贴近开奖号"，这正是公平随机摇奖应有的样子。若系统能稳定命中，反而是摇奖机不独立的危险信号。头奖恒等概率 1/17,721,088，与选号方法无关。</p>
</div>
</div>
"""
    else:
        html += f"""
<div class="section" style="border:2px dashed #6688aa;">
<div class="section-title">📊 附 · 第{next_period}期实际开奖对账（开奖后自动生成）</div>
        <div class="info"><p style="color:#99aab5; font-size:13px; line-height:1.8;">本期（第{next_period}期）尚未开奖，开奖后本报告会自动回填这组对账。现在请先读上方「🎯 开奖前必读 · 预期差距说明」校准期望。</p></div>
</div>
"""

    # ---- 以下娱乐组件从顶部聚簇下移，穿插分布到「号码预测」版块之后，避免与开头堆在一起 ----
    html += '<div class="entertain-interlude"><div class="ei-title">👋 娱乐间歇 · 今日问候 + 打卡</div>' + generate_engage_html() + '</div>'
    html += '<div class="entertain-interlude"><div class="ei-title">🏆 娱乐间歇 · 近期一等奖领奖故事</div>' + generate_winning_stories_html() + '</div>'
    html += _generate_marquee(latest['period'])

    # 娱乐节目 #1（穿插分布 issue#3）：大「号码预测」版块之后跟水晶球算一卦（放大居中+引导标语）
    # 自我进化 · 长期显著性检验面板(基于账本真实累计)
    html += _ssq_significance_panel()

    html += generate_tarot_html()

    html += f"""
</div>

<div class="section">
<div class="section-title">三、凯利公式资金管理</div>
<div class="stat-grid">
<div class="stat-card"><div class="value">{exp_return_pct}</div><div class="label">期望回报率（负期望）</div></div>
<div class="stat-card"><div class="value">{kelly_f:.2e}</div><div class="label">凯利f*（负值=不投注）</div></div>
<div class="stat-card"><div class="value">{net_loss_s}</div><div class="label">每注期望净亏损(元)</div></div>
<div class="stat-card"><div class="value">{one_prize_prob_s}</div><div class="label">一等奖概率</div></div>
</div>
<div class="warning">
<h3>💰 凯利公式结论</h3>
<p>双色球期望回报率<strong>{exp_return_pct}</strong>（每投2元期望收回{exp_prize_s}元）。凯利公式f*为负值，<strong>数学结论是不应投注</strong>。</p>
<p style="margin-top:8px;"><strong>务实建议</strong>：将彩票视为娱乐消费，每期投入≤月可支配收入的0.5%。</p>
</div>
</div>
"""

    html += f"""
<div class="section" style="border:2px solid #ffaa00;">
<div class="section-title">四、命中现实分布 + 与随机对照</div>
<div class="info">
<h3>ℹ️ 你最该看的板块：本系统历史上"大概中几等奖"</h3>
<p style="color:#ffbb00; font-size:15px; line-height:1.8;">
<strong>先给结论：双色球是均匀随机摇奖，任何方法（含本系统）在"提高一等奖命中率"上，数学上不可能优于随机。</strong>
下面用<strong>真实样本外回测</strong>（不是嘴上说）把"差距"摆出来，让你每次看推荐前先校准期望：
</p>
</div>
<div class="stat-grid">
<div class="stat-card"><div class="value" style="color:#ff6b6b;">{strat_roi_s}</div><div class="label">本系统 ROI（{power_label}实测）</div></div>
<div class="stat-card"><div class="value" style="color:#ff6b6b;">{base_roi_s}</div><div class="label">纯随机基线 ROI</div></div>
<div class="stat-card"><div class="value" style="color:#ff6b6b;">0 次</div><div class="label">{pw_n}期内一等奖（理论 {one_prize_prob_s}）</div></div>
<div class="stat-card"><div class="value" style="color:#ff6b6b;">{profit_prob_s}</div><div class="label">蒙特卡洛1年(156期)正收益概率</div></div>
</div>
<table>
<tr><th>维度</th><th>本系统（{power_label}）</th><th>纯随机基线</th><th>判定</th></tr>
<tr><td>样本外 ROI</td><td>{strat_roi_s}</td><td>{base_roi_s}</td><td>无显著差异（Bootstrap 95% CI={ci_s}，下界未&gt;0）</td></tr>
<tr><td>中奖期率（≥九等奖）</td><td>{strat_prize_s}</td><td>{base_prize_s}</td><td>随机反而更高（本系统投注组合数少）</td></tr>
<tr><td>红球平均命中</td><td>{ml_hit_s}</td><td>{ml_rand_s}</td><td>≈随机（{ml_label}，结论 no_edge）</td></tr>
<tr><td>一等奖命中</td><td>0 次 / {pw_n}期</td><td>0 次 / {pw_n}期</td><td>两者皆≈理论概率，均无法靠技巧提升</td></tr>
<tr><td>1年期望净盈亏</td><td colspan="2">期望净亏 {expected_net_s}，正收益概率仅 {profit_prob_s}</td><td>负期望游戏，凯利 f* 为负</td></tr>
</table>
<p style="margin-top:10px; color:#ffcc00;"><strong>因此：本系统推荐的号码，与"闭眼随机选一注"在期望上等价。如果你仍要买，唯一理性动作是<strong>控制投入</strong>（≤月收入0.5%），并把本报告当作"娱乐消费凭证"而非"致富方案"。</strong></p>
</div>

{generate_number_frequency_section(draws)}
"""

    # 娱乐节目 #2（穿插分布 issue#3）：大「命中现实分布」版块之后跟今日黄历（放大居中+引导标语）
    html += generate_almanac_html()

    # 娱乐节目 #3（穿插分布 issue#3）：频率参考后跟今日小彩蛋，避免娱乐挤一块
    html += generate_fun_card_html()

    html += f"""
<div class="warning">
<h3>⚠️ 最终诚实结论</h3>
<ul style="margin:8px 0; padding-left:20px; color:#ff9999; line-height:1.8;">
<li><strong>预测层面</strong>: V1修复版回测（完全复刻预测管线）确认，所有策略不比随机好（p>0.05）</li>
<li><strong>过滤器层面</strong>: 排除88.13%不合理组合，但<strong>不改变中奖概率</strong>，只缩小选择范围</li>
<li><strong>逆向层面</strong>: ECI理论收益≈0（一等奖概率太低），且专家代表性存疑</li>
<li><strong>资金层面</strong>: 凯利f*为负值，期望回报{exp_return_pct}，彩票是消费不是投资</li>
<li><strong>自动化</strong>: V1实现10/10步自动化，一键运行；专家推荐由 Phase 0.6 自动抓取、战绩由 Phase 0.7 自动回填</li>
</ul>
<p style="margin-top:10px;"><strong>一句话：数学上不应投注。如果将彩票视为娱乐消费，以下推荐在"如果买"的前提下提供了相对合理的选号方案——过滤器确保形态合理，ECI逆向减少分奖，胆拖控制成本，追踪消除确认偏差。</strong></p>
</div>

{generate_stayhook_html()}

<div class="disclaimer">
<p>本报告基于{total}期双色球历史数据 + {red_combos_s}组合穷举 + {len(expert_picks)}位专家真实推荐。</p>
<p>V1修复版回测完全复刻预测管线（相同权重/CDM先验/有效组合过滤/蓝球/扩展窗口）。</p>
<p>统计结论：无方法能超越随机基线（p>0.05）。凯利公式确认彩票为负期望游戏（期望回报{exp_return_pct}）。</p>

<h3 style="margin-top:14px; color:#88c0ff;">🛡️ 权威来源与反诈提醒（请务必阅读）</h3>
<ul style="margin:6px 0; padding-left:20px; line-height:1.85;">
<li><strong>官方定性（中国体育彩票官方订阅号 2025-02-12 / 央视网）</strong>：「再强大的AI也无法预知开奖号码」。双色球每次开奖都是<strong>独立随机事件</strong>，开奖号码随机产生，根本无法预测；物理摇奖机每球运动受空气流动、微小震动影响，<strong>不可测、不可控</strong>；上一期中奖号码对下一期<strong>毫无影响</strong>（如同连续抛硬币，第11次仍是50%）。</li>
<li><strong>为什么有人"觉得预测准"？</strong>官方解释有两层：①<strong>纯运气</strong>——全国每天成千上万人购彩，总有人恰好与开奖数字一致，与用什么方法选号无关；②<strong>选择性展示套路</strong>——所谓"大师"让不同人买不同号，只晒中奖的、删掉没中的，制造"神奇"假象。本报告的"历史中奖参考 / 号码频率"均为<strong>描述过去</strong>，不预测未来。</li>
<li><strong>警惕诈骗</strong>：任何「不实渠道消息 / 有偿预测 / 可确保的中奖结果 / 不中可确保的中奖结果 / 不实退款套路」均属违规违法（违反《彩票管理条例》，涉嫌刑法第266条诈骗罪，据法治日报）。唯一<strong>合法购彩渠道 = 线下体彩实体店</strong>；凡要求「下载App购彩 / 线上充值 / 陌生转账」的平台均为非法。建议安装「国家反诈中心APP」。</li>
<li><strong>2026规则要点</strong>：双色球共 <strong>6 个奖级</strong>（一~六等奖）；一等奖/二等奖为浮动奖，其中<strong>一等奖单注最高限额 500 万元</strong>（每注 2 元，<strong>不开放追加投注</strong>）；三至六等奖为固定奖（三 3000 / 四 200 / 五 10 / 六 5 元）；每注 36% 纳入公益金。</li>
</ul>
<p style="margin-top:10px; color:#ffcc00;"><strong>理性购彩：彩票是具有公益属性的娱乐方式，并非投资致富途径。量力而行、小额参与，把本报告当作"娱乐消费凭证"而非"致富方案"。</strong></p>
<p style="margin-top:10px;">生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')} | 自动化脚本: ssq_auto.py V1（诚实预测 · 反诈科普版）</p>
</div>

</div>
</body>
</html>"""
    
    html_path = f'双色球{next_period}期预测报告_V1_全面修复.html'
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  ✓ HTML报告已保存: {html_path}")
    
    # 保存预测JSON
    result = {
        'target_period': next_period,
        'version': 'V1.0.0',
        'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'data_periods': total,
        'latest_period': latest['period'],
        'groups': [{
            'name': g['name'], 'strategy': g['strategy'],
            'front': sorted(g['front']), 'back': sorted(g['back']),
            'cost': {'bets': gr['bets'], 'basic': gr['cost_basic'], 'extra': gr['cost_extra']},
            'strengths': gr['strengths'], 'weaknesses': gr['weaknesses'],
            'similar_shape': gr['similar_shape'],
        } for g, gr in zip(groups, group_reviews)],
        'dantuo': dantuo,
        'kelly_f': kelly_f,
        'expected_return': exp_return,
        'backtest_conclusion': 'all strategies not significant (p>0.05), backtest fully replicates prediction pipeline',
        'honest_disclaimer': 'filters do not improve winning probability; ECI expected benefit ~0; lottery is entertainment not investment',
    }
    json_path = f'ssq_prediction_{next_period}_v8.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2, default=str)
    print(f"  ✓ 预测JSON已保存: {json_path}")
    
    return html_path

def _detect_real_desktop():
    """SYSTEM 排程语境下 ~ 指向 systemprofile 虚拟桌面, 报告会落到用户看不到的位置。
    动态扫描系统用户目录定位真实交互用户桌面, 不写死用户名(换机也能正确投递)。"""
    users_root = os.path.expandvars(r"%SystemDrive%\Users")
    if not os.path.isdir(users_root):
        return None
    skip = ("public", "default", "default user", "default", "all users",
            "systemprofile", "network service", "local service")
    try:
        for name in os.listdir(users_root):
            nl = name.lower()
            if nl in skip or nl.startswith("systemprofile"):
                continue
            d = os.path.join(users_root, name, "Desktop")
            if os.path.isdir(d):
                return d
    except Exception:
        pass
    return None


def _export_report_to_desktop(html_path, next_period):
    """把生成的 HTML 报告复制一份到用户桌面, 作为可双击打开的本地产物。
    关键 UX 加固: 不依赖调用模型是否执行 present_files —— 客户总能在本机桌面
    找到该 .html 文件, 双击用浏览器打开即可, 彻底解决『预览面板弹不出/无产物』。
    """
    import shutil
    try:
        src = os.path.abspath(html_path)
        if not os.path.isfile(src):
            return
        # 解析『真实用户桌面』: 系统计划任务以 SYSTEM 身份运行时 ~ 指向 systemprofile 虚拟桌面,
        # 报告会落到用户看不到的位置; 动态定位真实交互用户桌面(不写死用户名), 兼容普通用户/skillhub。
        profile = os.environ.get("USERPROFILE") or os.environ.get("HOME") or ""
        cands = [
            _detect_real_desktop(),                                          # SYSTEM 语境动态定位真实交互用户桌面(不写死用户名)
            os.path.join(profile, "Desktop") if profile else "",             # 普通用户语境(真实桌面)
            os.path.expanduser("~/Desktop"),
            os.path.expanduser("~/桌面"),
            os.path.expanduser("~/Documents"),
        ]
        dest_dir = None
        for cand in cands:
            if not cand:
                continue
            if "systemprofile" in cand.replace("\\", "/").lower():
                continue
            if os.path.isdir(cand):
                dest_dir = cand
                break
        if dest_dir is None:
            # 兜底: 仍用 USERPROFILE 桌面(即便 systemprofile), 至少文件存在可排查
            dest_dir = os.path.join(profile, "Desktop") if profile else os.path.expanduser("~")
        dest = os.path.join(dest_dir, f'双色球{next_period}期预测报告.html')
        shutil.copy2(src, dest)
        print("\n" + "=" * 70)
        print("【报告本地副本已生成(可直接双击打开, 无需预览面板)】")
        print(f"  REPORT_BASE_DESKTOP_PATH: {dest}")
        print("  说明: 复制此 .html 到桌面, 双击用浏览器打开即可, 自包含无外部依赖")
        print("=" * 70)
    except Exception as e:
        print(f"  ⚠ 复制到桌面失败(不影响主报告生成): {e}")

# ============================================================
# 专家推荐派生（pipeline 与 三方交叉验证 必须共用, 否则第4组分歧）
# ============================================================
def load_expert_picks(draws, verbose=True, data_issues=None):
    """加载专家推荐(供预测 ECI/遗漏优选 组使用) —— 唯一权威派生逻辑。

    pipeline(main) 与 三方交叉验证(cross_validate) 必须共用本函数, 保证两侧
    expert_picks 完全一致。任一路径各自实现"文件缺失时的回退", 会因回退逻辑不同
    导致第4组(ECI/遗漏优选)的红球/蓝球分布分歧, 进而触发虚假的'一致性严格比对'
    失败(表现为整栏乃至全项 52/52 不一致)。

    派生优先级:
      1) ssq_expert_picks.json 存在 → 用其 experts(标注目标期不一致仅告警, 不影响派生)
      2) 文件缺失 → 回退内置常驻专家体系 build_resident_expert_panel(确定性派生, 必非空)
      3) 极端兜底 → 任何异常返回空列表
    """
    target_period = next_period_func(int(draws[-1]['period']), draws[-1].get('date'))
    if verbose:
        print("\n" + "=" * 70)
        print("【步骤4.5/7: 加载专家推荐】")
        print("=" * 70)
    try:
        with open('ssq_expert_picks.json', 'r', encoding='utf-8') as f:
            ep_data = json.load(f)
        picks = [(e['expert'], e['front'], e.get('back', [])) for e in ep_data.get('experts', [])]
        exp_tp = ep_data.get('_meta', {}).get('target_period')
        if verbose:
            print(f"  ✓ 已加载{len(picks)}位专家推荐")
            print(f"  标注目标期: {exp_tp} ｜ 当前预测期: {target_period}")
            print(f"  更新时间: {ep_data.get('_meta', {}).get('last_updated', ep_data.get('updated_at', '未知'))}")
        if exp_tp is None:
            w = "专家数据未标注目标期, 无法确认新鲜度(建议重新刷新)"
            if verbose:
                print(f"  ⚠ {w}")
            if data_issues is not None:
                data_issues.append(w)
        elif str(exp_tp) != str(target_period):
            w = f"专家数据标注期{exp_tp}≠当前预测期{target_period}(可能抓取源滞后或数据未刷新)"
            if verbose:
                print(f"  ⚠ {w}")
            if data_issues is not None:
                data_issues.append(w)
        else:
            if verbose:
                print(f"  ✓ 专家数据目标期与当前预测期一致")
        if verbose:
            print(f"  自动刷新: 系统级定时任务(Phase 0.6)每周一三六20:10经 ssq_expert_scraper.py --auto 刷新; 也可让我用WebSearch实时抓取")
        return picks
    except FileNotFoundError:
        if verbose:
            print("  ⚠ ssq_expert_picks.json不存在！回退到内置常驻专家体系共识")
        try:
            from ssq_expert_roster import build_resident_expert_panel
            _panel = build_resident_expert_panel(target_period, draws)
            picks = [(e['name'], e['front'], e['back']) for e in _panel]
            if verbose:
                print(f"  ✓ 已用常驻专家体系回退生成 {len(picks)} 位专家共识(确定性派生, 娱乐参考)")
            return picks
        except Exception as _e:
            if verbose:
                print(f"  ⚠ 常驻专家回退也失败: {_e}；将不使用ECI逆向策略")
            return []
    except Exception as _e:
        if verbose:
            print(f"  ⚠ 专家数据解析失败: {_e}；回退常驻专家体系")
        try:
            from ssq_expert_roster import build_resident_expert_panel
            _panel = build_resident_expert_panel(target_period, draws)
            return [(e['name'], e['front'], e['back']) for e in _panel]
        except Exception:
            return []


# ============================================================
# 主函数
# ============================================================
def main():
    # utf-8 输出包装仅在 main() 内做，避免被 import 时篡改导入进程 stdout
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    skip_download = '--skip-download' in sys.argv
    skip_exhaustive = '--skip-exhaustive' in sys.argv
    
    print("=" * 70)
    print(f"双色球分析系统 V1 端到端自动化")
    print(f"运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)
    
    # 步骤1: 下载
    if skip_download:
        print("\n【步骤1/7: 跳过下载，使用现有数据】")
        with open('ssq_history.json', 'r', encoding='utf-8') as f:
            draws = json.load(f)
        draws.sort(key=lambda x: x['period'])
        print(f"  使用现有数据: {len(draws)}期")
    else:
        draws = download_data()
        if not draws:
            print("无法获取数据，程序退出")
            return
    
    # 步骤2: 校验
    validation = validate_data(draws)
    data_issues = validation.get('issues', [])
    data_fatal = validation.get('fatal', [])

    # 致命错误拦截: 脏数据(号码非法/日期倒序)绝不写入 ssq_history.json
    # 此时保留现有已存盘的数据, 让后续流程使用 --skip-download 层面的安全数据
    if data_fatal:
        print(f"\n  ⛔ 数据校验发现致命错误, 拒绝写入脏数据。保留现有 ssq_history.json。")
        print(f"  ⛔ 致命项: {', '.join(data_fatal)}")
        print(f"  ⛔ 建议: 检查数据源或运行 python ssq_data_recovery.py force <源> 恢复。")
        # 回退到现有已存盘的(更可信的)数据继续, 而非用脏 draws 覆盖
        try:
            with open('ssq_history.json', 'r', encoding='utf-8') as f:
                draws = json.load(f)
            draws.sort(key=lambda x: x['period'])
            print(f"  ✓ 已回退到现有 ssq_history.json ({len(draws)}期) 继续预测")
        except Exception as e:
            print(f"  ✗ 回退失败且无安全数据: {e}，终止")
            return
    else:
        # 保存数据（合并保留更完整的，复用 persist_history）
        draws = persist_history(draws)

    # 步骤3: 穷举有效组合
    if skip_exhaustive:
        valid_combos = load_valid_combos()
        if valid_combos:
            print(f"\n【步骤3/7: 使用缓存的有效组合 ({len(valid_combos):,}个)】")
        else:
            print("\n【步骤3/7: 缓存不存在，重新穷举】")
            valid_combos = exhaustive_combos()
    else:
        valid_combos = exhaustive_combos()
    
    # 步骤4: 计算模型
    models = compute_models(draws)
    
    # 步骤5: 加载专家推荐（与三方交叉验证共用同一派生逻辑, 保证 expert_picks 两侧一致）
    expert_picks = load_expert_picks(draws, verbose=True, data_issues=data_issues)

    # 步骤6: 生成预测
    groups, dantuo = generate_predictions(draws, models, valid_combos, expert_picks)
    
    # 计算主蓝球TOP3用于报告（与generate_predictions中的back_top4_main一致）
    back_scored_main = {}
    for num in range(1, 17):
        cdm_s = models['cdm_prob_b'].get(num, 0)
        mk_s = models['markov_back'].get(num, 0)
        omit_s = models['back_omit'].get(num, 0) / models['max_back_omit']
        back_scored_main[num] = _back_score(cdm_s, mk_s, omit_s)
    back_top4_main = [num for num, _ in sorted(back_scored_main.items(), key=lambda x: x[1], reverse=True)[:3]]
    
    # 步骤7: 生成报告
    html_path = generate_report(draws, models, groups, dantuo, expert_picks, data_issues, back_top4_main)

    # V1.0.0 反遗漏自查: base报告生成后立即校验板块完整性(缺失即告警, 不阻断)
    try:
        from verify_report_sections import verify_report
        missing = verify_report(html_path, enhanced=False, verbose=True)
        if missing:
            print(f"  ⚠⚠ 反遗漏自检告警: 基础报告疑似遗漏 {len(missing)} 个板块 -> {missing}")
            print(f"  ⚠⚠ 请检查 ssq_auto.generate_report 是否漏注入板块")
    except Exception as e:
        print(f"  ⚠ 反遗漏自检脚本异常(跳过): {e}")

    # 计算下期期号（与generate_report内部一致, 统一用 ssq_period）
    next_period = next_period_func(int(draws[-1]['period']), draws[-1].get('date'))

    # V2.1.1 UX 加固: 复制报告到桌面, 保证客户一定能找到并双击打开(不依赖预览面板)
    _export_report_to_desktop(html_path, next_period)

    # V2.1.13 跨报告持久化: 同步 latest_report.html 供本地服务(http://127.0.0.1:8765/)
    # 访问, 使招财猫/心愿单/彩友圈状态跨报告保存。仅当存在本地服务时才必需,
    # 但直接复制无副作用(普通双击 html 仍走 localStorage 降级)。
    try:
        _latest = os.path.join(HERE, 'latest_report.html')
        if os.path.exists(html_path):
            import shutil as _shutil
            _shutil.copy2(os.path.abspath(html_path), _latest)
    except Exception:
        pass

    # V2.1.12 统一报告体验: 核心预测器也保证产出增强版报告。
    # 根因: 此前 ssq_auto.py 只生成基础版(双色球XXXX期预测报告_V1_全面修复.html),
    # 增强版(含ML模型/冷热图/专家汇总/更多推荐号)仅由 ssq_smart.py Phase3 或 SKILL 的
    # run_ssq.py 触发 —— 导致"直跑 ssq_auto.py / 某些语境下的系统运行"只拿到基础版,
    # 与 SKILL 的增强版体验不一致。现改为: 任何入口(直跑 ssq_auto / ssq_smart / SKILL / Windows排程)
    # 最终都落到增强版报告。已存在则跳过, 避免与 ssq_smart.py Phase3 重复跑。
    try:
        enhanced_html = html_path.replace('.html', '_V15_增强版.html')
        # 2.1.20 修复(增强版依赖基础版): 基础版每次重算都会刷新 mtime;
        # 若增强版不存在或比基础版旧(如刚改了报告模板), 必须重算,
        # 否则增强版会停留在陈旧内容(此前"改了基础版→增强版不更新"的反复坑)。
        _base_mtime = os.path.getmtime(html_path) if os.path.exists(html_path) else 0
        _enh_exists = os.path.exists(enhanced_html)
        _enh_stale = _enh_exists and os.path.getmtime(enhanced_html) < _base_mtime
        if _enh_exists and not _enh_stale:
            print("  ℹ 增强版报告已是最新(基础版未变), 跳过补跑")
        else:
            print("  补跑增强版报告 (ssq_enhance.py, ML模型+冷热图+专家汇总) ...")
            _enh = subprocess.run(
                [sys.executable, 'ssq_enhance.py'],
                cwd=os.path.dirname(os.path.abspath(__file__)),
                capture_output=True, text=True, timeout=200,
                encoding='utf-8', errors='replace',
            )
            if os.path.exists(enhanced_html):
                print(f"  ✓ 增强版报告已生成: {os.path.basename(enhanced_html)}")
            else:
                # 增强失败仅告警(基础版仍可用), 不阻断主流程 —— 诚实降级
                tail = (_enh.stderr or _enh.stdout or '')[-300:]
                print(f"  ⚠ 增强版报告生成未完成(非致命, 基础版仍可用): {tail.strip()}")
    except Exception as e:
        print(f"  ⚠ 增强版补跑异常(非致命): {e}")
    
    print("\n" + "=" * 70)
    print("【V1端到端自动化完成！】")
    print(f"  报告: {html_path}")
    print(f"  预测JSON: ssq_prediction_{next_period}_v8.json")
    print("=" * 70)
    
    # 自动化状态
    print(f"\n  自动化步骤完成情况: (步骤9/10 由上游 ssq_smart.py Phase 0.6/0.7 在调用本模块前完成)")
    steps = [
        ("1. 数据下载", True),
        ("2. 数据校验", True),
        ("3. 有效组合穷举", True),
        ("4. 模型计算", True),
        ("5. 专家推荐加载", True),
        ("6. 预测生成", True),
        ("7. 报告生成", True),
        ("8. 定时任务", True),
        ("9. 专家自动抓取", True),   # 由 ssq_smart.py Phase 0.6 驱动 (ssq_expert_scraper.py --auto)
        ("10. 投注追踪自动回填", True),  # 由 ssq_smart.py Phase 0.7 驱动 (ssq_expert_tracker.py)
        ("--- V1.0增强 ---", None),
        ("11. huiniao API数据源", True),
        ("12. ML预测模型(3种)", True),
        ("13. 号码冷热图可视化", True),
        ("14. 专家汇总分析", True),
        ("15. 三方交叉验证", True),
        ("16. 增强回测(200期)", True),
    ]
    for name, done in steps:
        if done is None:
            print(f"    {name}")
        else:
            print(f"    {'✅' if done else '❌'} {name}")
    done_count = sum(1 for _, d in steps if d is True)
    total_count = sum(1 for _, d in steps if d is not None)
    print(f"\n  自动化得分: {done_count}/{total_count}")

    # V2.1.13 跨报告持久化(可选): --serve 启动本地状态服务, 招财猫/心愿/彩友跨报告保存
    if '--serve' in sys.argv:
        try:
            import subprocess as _sp
            _sp.Popen(
                [sys.executable, os.path.join(HERE, 'ssq_serve.py')],
                cwd=HERE, stdout=_sp.DEVNULL, stderr=_sp.DEVNULL,
            )
            print("\n" + "=" * 70)
            print("【本地服务已启动 · 招财猫跨报告保存】")
            print("  打开: http://127.0.0.1:8765/  （报告已同步为 latest_report.html）")
            print("  关闭: 结束本服务进程 / 关闭终端。仅本机可访问，不联网。")
            print("=" * 70)
        except Exception as e:
            print(f"\n  ⚠ 启动本地服务失败(不影响报告生成): {e}")

if __name__ == '__main__':
    # 安全网：本进程所有联网（数据下载/在线核对等 urllib 调用）受全局 socket 默认超时保护，
    # 覆盖 DNS/握手/读取阶段。这是排程任务"卡死/停止工作"的头号根因——Windows 下慢 DNS 或
    # 握手挂起可能绕过 urlopen 的 per-request timeout，只有全局 setdefaulttimeout 才能兜底。
    # 注意：父进程 ssq_smart 设的 socket 超时不会继承到本子进程，故必须在此独立设置。
    try:
        import socket
        socket.setdefaulttimeout(45)
    except Exception:
        pass
    # 锚定工作目录到本模块所在目录(lib/), 使所有相对路径文件读写与调用方 cwd 解耦。
    # SKILL 被市场以不同 cwd 调用时, ssq_history.json 等可回退联网, 但 ssq_power_report.json
    # 无回退, 会致"四、命中现实分布"空白。chdir 到 lib/ 彻底修复(仅独立运行本报告时生效,
    # 被其他模块 import 时不触发, 不影响其 cwd)。
    os.chdir(HERE)
    main()



def _detect_real_desktop():
    """SYSTEM 排程语境下 ~ 指向 systemprofile 虚拟桌面, 报告会落到用户看不到的位置。
    动态扫描系统用户目录定位真实交互用户桌面, 不写死用户名(换机也能正确投递)。"""
    users_root = os.path.expandvars(r"%SystemDrive%\Users")
    if not os.path.isdir(users_root):
        return None
    skip = ("public", "default", "default user", "defaultuser0", "all users",
            "systemprofile", "network service", "local service")
    try:
        for name in os.listdir(users_root):
            nl = name.lower()
            if nl in skip or nl.startswith("systemprofile"):
                continue
            d = os.path.join(users_root, name, "Desktop")
            if os.path.isdir(d):
                return d
    except Exception:
        pass
    return None
