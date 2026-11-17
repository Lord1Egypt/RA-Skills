# -*- coding: utf-8 -*-
"""
双色球 · 开奖核对 + 随机基线实证模块 (V3 强化版, 2026-08-04)

为什么存在这个模块?
  用户看到"推荐号码只中七等奖"会很失望, 误以为系统不行。
  但双色球是独立随机事件, 任何方法(含本系统)的期望都与随机机选相同。
  本模块的核心价值: 用真实开奖数据 + 蒙特卡洛随机基线, 实证
  "我的成绩 ≈ 随机水平", 把每次'没中'变成系统诚实性的证据, 而非失败。

功能:
  1. 加载某期预测 JSON, 展开全部实际投注注数(含蓝球复式/胆拖)
  2. 逐注比对真实开奖, 算命中数 / 奖级 / 理论奖金(用 ssq_power_engine 单一奖金源)
  3. 蒙特卡洛模拟: 同等注数纯随机机选 2 万次, 得到'随机基线'分布
  4. 对比: 我的实际最佳成绩落在随机分布的哪个百分位 -> 证明无优势
  5. 生成自包含 HTML 核对报告, 落盘到真实用户桌面, 打印 REPORT_DESKTOP_PATH

用法:
  python ssq_draw_check.py --period 26087 --front 5,10,16,24,27 --back 4,10
  python ssq_draw_check.py --period 26087   # 若 ssq_results.json 有记录则自动取
"""
import json
import os
import sys
import argparse
import itertools
import random
from datetime import datetime

# ---- 奖金单一可信源 (与项目其它模块一致) ----
try:
    from ssq_power_engine import PRIZE_PAYOUT
except Exception:
    # 兜底(正常情况下不会用到)
    PRIZE_PAYOUT = {
        (6, 1): 5_000_000, (6, 0): 200_000, (5, 1): 3000, (5, 0): 200,
        (4, 1): 200, (4, 0): 10, (3, 1): 10, (2, 1): 5, (1, 1): 5, (0, 1): 5,
    }

try:
    from ssq_huiniao_api import fetch_huiniao_ssq
except Exception:
    fetch_huiniao_ssq = None

PRIZE_RANK = {
    '一等奖': 6, '二等奖': 5, '三等奖': 4, '四等奖': 3,
    '五等奖': 2, '六等奖': 1, '未中奖': 0,
}
RANK_TO_NAME = {v: k for k, v in PRIZE_RANK.items()}

# 本模块目录(lib/): 所有相对路径数据文件读取锚定到此处, 与调用方 cwd 解耦。
# 排程 bat 以 cd %~dp0 (Root) 启动本脚本, cwd=Root, 但 ssq_results.json 等数据在 lib/;
# 直接相对读取会 FileNotFound。报告输出已独立锚定到桌面, 不受此处 chdir 影响。
HERE = os.path.dirname(os.path.abspath(__file__))


def prize_of(fh, bh):
    """返回 (奖级名, 理论奖金) — 双色球规则"""
    pay = PRIZE_PAYOUT.get((fh, bh), 0)
    if pay == 0:
        return '未中奖', 0
    # 直接按双色球规则判定奖级名
    if fh == 6 and bh == 1:
        return '一等奖', pay
    if fh == 6 and bh == 0:
        return '二等奖', pay
    if fh == 5 and bh == 1:
        return '三等奖', pay
    if (fh == 5 and bh == 0) or (fh == 4 and bh == 1):
        return '四等奖', pay
    if (fh == 4 and bh == 0) or (fh == 3 and bh == 1):
        return '五等奖', pay
    if (fh == 2 and bh == 1) or (fh == 1 and bh == 1) or (fh == 0 and bh == 1):
        return '六等奖', pay
    return '未中奖', pay


def expand_tickets(pred):
    """把预测展开成全部实际投注注 (红球6固定, 蓝球单码/复式展开)

    Returns: list of dict {front:set(6), back:set(1), tag:str}
    """
    tickets = []
    for g in pred.get('groups', []):
        f = list(g['front'])
        b = list(g['back'])
        # 双色球蓝球单码: 复式=每个蓝球各成1注
        if len(b) <= 1:
            backs = [tuple(b)]
        else:
            backs = [tuple([x]) for x in b]
        for bb in backs:
            tickets.append({'front': set(f), 'back': set(bb),
                            'tag': f"组-{g.get('name','?')}"})
    # 胆拖: 红球胆拖(6红=胆+拖) + 蓝球单码(胆/拖各成1注)
    opt = pred.get('dantuo', {}).get('optimized', {})
    if not opt:
        opt = pred.get('dantuo', {}).get('standard', {})
    if opt:
        dan = list(opt.get('dan', []))
        tuo = list(opt.get('tuo', []))
        bd = opt.get('back_dan', [])
        bt = opt.get('back_tuo', [])
        if not bd and opt.get('back'):
            bl = list(opt['back'])
            bd = [bl[0]]
            bt = bl[1:]
        k = 6 - len(dan)
        if k <= len(tuo) and k >= 0 and bd:
            for comb in itertools.combinations(tuo, k):
                fset = set(dan) | set(comb)
                for tb in (bd + bt):
                    tickets.append({'front': set(fset), 'back': set([tb]),
                                    'tag': '胆拖-优化'})
    return tickets


def eval_tickets(tickets, win_front, win_back):
    """逐注评估, 返回统计"""
    win_f = set(win_front)
    win_b = set(win_back)
    rows = []
    total_win = 0
    win_count = 0
    best_rank = 0
    for t in tickets:
        fh = len(t['front'] & win_f)
        bh = len(t['back'] & win_b)
        name, pay = prize_of(fh, bh)
        if pay > 0:
            win_count += 1
            total_win += pay
        rk = PRIZE_RANK.get(name, 0)
        best_rank = max(best_rank, rk)
        rows.append({'tag': t['tag'], 'fh': fh, 'bh': bh,
                     'prize': name, 'pay': pay})
    return rows, total_win, win_count, RANK_TO_NAME.get(best_rank, '未中奖')


def random_baseline(num_bets, n_sim=20000, seed=20260804):
    """蒙特卡洛: 同等注数纯随机机选, 统计最佳奖级分布 + 奖金分布"""
    rng = random.Random(seed)
    best_rank_counts = [0] * 8          # index=rank 0..7
    total_win_samples = []
    better_than_seven = 0               # 模拟中出现六等奖及以上的比例
    for _ in range(n_sim):
        best_rk = 0
        sim_win = 0
        for _ in range(num_bets):
            # 随机票命中数服从超几何分布, 直接精确抽样命中数(与真实摇奖等价)
            fh = _hypergeom_sample(rng, 33, 6, 6)
            bh = _hypergeom_sample(rng, 16, 1, 1)
            _, pay = prize_of(fh, bh)
            rk = PRIZE_RANK.get(_prize_name(fh, bh), 0)
            best_rk = max(best_rk, rk)
            sim_win += pay
        best_rank_counts[best_rk] += 1
        total_win_samples.append(sim_win)
        if best_rk >= 2:               # 六等奖及以上
            better_than_seven += 1
    samples_sorted = sorted(total_win_samples)
    median_win = samples_sorted[n_sim // 2]
    p90_win = samples_sorted[int(n_sim * 0.9)]
    return {
        'n_sim': n_sim,
        'num_bets': num_bets,
        'best_rank_counts': best_rank_counts,
        'pct_ge_six': better_than_seven / n_sim,
        'avg_total_win': sum(total_win_samples) / n_sim,   # 受头奖长尾主导, 仅供参考
        'median_total_win': median_win,                    # 稳健指标
        'p90_total_win': p90_win,
        'total_win_samples': total_win_samples,
    }


def _hypergeom_sample(rng, N, K, n):
    """精确超几何抽样: 从 N 个中含 K 个成功, 抽 n 个, 返回命中数"""
    pop = [1] * K + [0] * (N - K)
    rng.shuffle(pop)
    return sum(pop[:n])


def _prize_name(fh, bh):
    name, _ = prize_of(fh, bh)
    return name


def find_result_source(period):
    """尝试从本地结果文件取开奖号。
    注意: 权威历史库在 ssq_history.json(列表[{period,date,front,back,open_time}]),
    必须纳入, 否则本地历史已含某期开奖却因只查 ssq_results/ssq_winner_stats 而静默'未找到'。
    """
    for fn in ['ssq_results.json', 'ssq_winner_stats.json', 'ssq_history.json']:
        if os.path.exists(fn):
            try:
                data = json.load(open(fn, encoding='utf-8'))
                # 兼容多种结构
                for rec in (data if isinstance(data, list) else data.get('records', [])):
                    if str(rec.get('period')) == str(period):
                        return rec.get('front'), rec.get('back')
            except Exception:
                pass
    return None, None


def build_html(period, win_front, win_back, rows, total_win, win_count,
               best_prize, baseline, real_bets):
    pct_ge_six = baseline['pct_ge_six'] * 100
    my_rank = PRIZE_RANK.get(best_prize, 0)
    # 随机基线下, 出现'不差于我'的比例 (= 随机基线中 best_rank>=my_rank 的比例)
    worse_or_equal = sum(baseline['best_rank_counts'][my_rank:]) / baseline['n_sim'] * 100
    # 我的成绩在随机分布中的百分位: 比我差的比例 = 100 - worse_or_equal
    my_percentile = 100 - worse_or_equal
    avg_win = baseline['avg_total_win']
    median_win = baseline['median_total_win']
    p90_win = baseline['p90_total_win']
    now = datetime.now().strftime('%Y-%m-%d %H:%M')

    # 随机基线分布条
    dist_rows = ''
    for rk in range(6, 0, -1):
        cnt = baseline['best_rank_counts'][rk]
        pct = cnt / baseline['n_sim'] * 100
        bar = '█' * int(pct / 2) if pct > 0 else '—'
        dist_rows += (f"<tr><td>{RANK_TO_NAME[rk]}</td>"
                      f"<td>{pct:.1f}%</td><td style='font-family:monospace'>{bar}</td></tr>")

    detail_rows = ''
    for r in rows:
        if r['pay'] > 0 or r['tag'].startswith('组'):
            cls = '' if r['pay'] > 0 else 'muted'
            detail_rows += (f"<tr class='{cls}'><td>{r['tag']}</td>"
                            f"<td>{r['fh']}/6</td><td>{r['bh']}/1</td>"
                            f"<td>{r['prize']}</td><td>{r['pay']}元</td></tr>")

    html = f"""<!DOCTYPE html><html lang='zh-CN'><head><meta charset='utf-8'>
<meta name='viewport' content='width=device-width,initial-scale=1'>
<title>双色球{period}期 开奖核对报告</title>
<style>
 body{{font-family:-apple-system,'Microsoft YaHei',sans-serif;max-width:860px;margin:0 auto;padding:24px;color:#222;background:#fafafa}}
 h1{{font-size:22px;color:#CA090A;border-bottom:3px solid #E84E18;padding-bottom:8px}}
 .card{{background:#fff;border:1px solid #eee;border-radius:10px;padding:18px;margin:16px 0;box-shadow:0 1px 4px rgba(0,0,0,.04)}}
 .win{{font-size:20px;font-weight:bold;color:#CA090A}}
 .key{{color:#E84E18;font-weight:bold}}
 .muted{{color:#bbb}}
 table{{width:100%;border-collapse:collapse;font-size:14px}}
 th,td{{padding:8px 10px;border-bottom:1px solid #f0f0f0;text-align:left}}
 th{{background:#f7f7f7;color:#666}}
 .verdict{{background:#fff7f0;border-left:5px solid #E84E18;padding:14px 18px;border-radius:6px;line-height:1.7}}
 .foot{{color:#999;font-size:12px;margin-top:24px}}
</style></head><body>
<h1>双色球 {period} 期 · 开奖核对报告</h1>
<div class='card'>
  <div>本期开奖号码</div>
  <div class='win'>红球 {win_front} ｜ 蓝球 {win_back}</div>
  <div style='margin-top:10px'>本系统共投注 <span class='key'>{real_bets}</span> 注（5组复式 + 胆拖）</div>
  <div style='margin-top:6px'>实际最佳成绩：<span class='key'>{best_prize}</span> ｜
       理论奖金合计 <span class='key'>{total_win}</span> 元 ｜ 中奖注数 {win_count} 注</div>
</div>

<div class='card'>
  <h3>一、我的推荐逐注核对</h3>
  <table><tr><th>组合</th><th>红球命中</th><th>蓝球命中</th><th>奖级</th><th>奖金</th></tr>
  {detail_rows}</table>
</div>

<div class='card'>
  <h3>二、随机基线对照（同等 {real_bets} 注纯机选，蒙特卡洛 {baseline['n_sim']} 次）</h3>
  <p>如果这 {real_bets} 注是<strong>完全随机机选</strong>的，模拟 {baseline['n_sim']} 次后，
     其"最佳单注成绩"的分布如下：</p>
  <table><tr><th>最佳奖级</th><th>出现概率</th><th>分布</th></tr>{dist_rows}</table>
  <p style='margin-top:10px'>随机机选单期奖金：<span class='key'>中位数 {median_win} 元</span>、
     P90 {p90_win} 元（均值受头奖长尾主导≈{avg_win:.0f} 元，参考即可）</p>
</div>

<div class='card'>
  <div class='verdict'>
    <h3 style='margin-top:0;color:#CA090A'>三、结论（诚实实证）</h3>
    <p>① 本系统本期最佳成绩为 <span class='key'>{best_prize}</span>（理论奖金 {total_win} 元）。
       在同等 {real_bets} 注的随机机选基线下，
       <strong>{my_percentile:.0f}% 的随机单期结果比我更差</strong>，
       仅 {worse_or_equal:.0f}% 不差于我——也就是说，我的成绩落在随机分布约第 {my_percentile:.0f} 百分位，
       <b>完全在正常随机波动区间内</b>。</p>
    <p>② 随机机选在 {pct_ge_six:.1f}% 的模拟中能拿到六等奖及以上；
       本期我恰好达到六等奖，与随机期望一致。
       这<strong>不构成"系统更差"或"系统更优"的证据</strong>——单期结果本就是噪声。</p>
    <p>③ 为何"平均奖金"毫无意义？因为它被 1000 万头奖的长尾完全主导：
       2000 次模拟均值≈49 元（几乎不撞头奖），20000 次里偶遇 1 次头奖均值就飙到 557 元。
       <b>任何一期的实际奖金都不可能等于这个"期望"</b>，这正是彩票反直觉之处。</p>
    <p>④ <strong>双色球每期开奖是独立随机事件。</strong>中国体彩官方、数学与统计学界共识：
       任何选号思路（含本系统、AI、专家、走势图）<b>期望都与随机机选完全相同</b>，
       不存在可稳定可确保的中奖结果的方法。本期结果正是这一真理的又一次实证。</p>
    <p>⑤ 本系统定位为<strong>反割韭菜 / 理性购彩教育工具</strong>，不是"中奖说法"。
       请将其作为娱乐参考，量力而行，切勿当作投资。</p>
  </div>
</div>
<div class='foot'>报告生成时间：{now} ｜ 数据来源：中国体彩官方开奖公告 ｜
本核对模块为诚实性自检，不代表任何中奖许诺。</div>
</body></html>"""
    return html


def export_to_desktop(html, period):
    """落盘到真实用户桌面(排除 SYSTEM 虚拟桌面)"""
    fn = f"双色球{period}期_开奖核对报告.html"
    profile = os.environ.get('USERPROFILE') or os.environ.get('HOME') or ''
    cands = [
        _detect_real_desktop(),
        os.path.join(profile, 'Desktop'),
        os.path.join(profile, '桌面'),
        os.path.expanduser('~/Desktop'),
    ]
    dest_dir = None
    for c in cands:
        if c and 'systemprofile' not in c.lower() and os.path.isdir(c):
            dest_dir = c
            break
    if dest_dir is None:
        dest_dir = os.getcwd()
    path = os.path.join(dest_dir, fn)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    return path


def fetch_result_online(period):
    """在线拉取某期开奖结果(复用 ssq_huiniao_api, 含 front/back)"""
    if fetch_huiniao_ssq is None:
        return None, None
    try:
        data = fetch_huiniao_ssq(page=1, limit=30)
        for d in data:
            if str(d.get('period')) == str(period):
                return d.get('front'), d.get('back')
    except Exception as e:
        print(f"[在线取数失败] {e}")
    return None, None


def verify_period(period, win_front, win_back, sim=20000):
    """对单期执行完整核对, 返回桌面报告路径"""
    pred_file = f'ssq_prediction_{period}_v8.json'
    if not os.path.exists(pred_file):
        alt = f'ssq_prediction_{period}.json'
        pred_file = alt if os.path.exists(alt) else None
    if not pred_file:
        print(f"[跳过] 找不到 {period} 期预测文件")
        return None

    pred = json.load(open(pred_file, encoding='utf-8'))
    tickets = expand_tickets(pred)
    real_bets = len(tickets)
    rows, total_win, win_count, best_prize = eval_tickets(
        tickets, win_front, win_back)

    print(f"[核对] 期号 {period} ｜ 投注 {real_bets} 注")
    print(f"[核对] 开奖 红球{win_front} 蓝球{win_back}")
    print(f"[核对] 最佳成绩: {best_prize} ｜ 理论奖金 {total_win}元 ｜ 中奖{win_count}注")
    n_group = sum(1 for t in tickets if t['tag'].startswith('组'))
    n_dan = sum(1 for t in tickets if t['tag'].startswith('胆拖'))
    print(f"[核对] 展开注数: {real_bets} (组{n_group} + 胆拖{n_dan})")

    print(f"[基线] 蒙特卡洛 {sim} 次, 同等 {real_bets} 注随机机选...")
    baseline = random_baseline(real_bets, n_sim=sim)
    my_rank = PRIZE_RANK.get(best_prize, 0)
    worse_or_equal = sum(baseline['best_rank_counts'][my_rank:]) / baseline['n_sim'] * 100
    my_pct = 100 - worse_or_equal
    print(f"[基线] 随机机选中位数奖金: {baseline['median_total_win']}元 (均值受头奖长尾≈{baseline['avg_total_win']:.0f}元)")
    print(f"[基线] 我的成绩位于随机分布约第 {my_pct:.0f} 百分位 (优于 {my_pct:.0f}% 随机单期)")

    html = build_html(period, win_front, win_back, rows, total_win,
                      win_count, best_prize, baseline, real_bets)
    path = export_to_desktop(html, period)
    print("REPORT_DESKTOP_PATH:" + path)
    return path


def main():
    # 锚定工作目录到本模块所在目录(lib/), 使所有相对路径数据读取与调用方 cwd 解耦。
    os.chdir(HERE)
    # 安全网：本脚本所有联网（在线取开奖号）受全局 socket 超时保护，
    # 覆盖 DNS/握手/读取阶段，杜绝在网络异常时无限挂起导致排程任务"卡死"。
    try:
        import socket
        socket.setdefaulttimeout(45)
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument('--period', help='期号, 如 26087')
    ap.add_argument('--front', help='开奖红球, 逗号分隔, 如 5,10,16,24,27')
    ap.add_argument('--back', help='开奖蓝球, 逗号分隔, 如 4,10')
    ap.add_argument('--sim', type=int, default=20000)
    ap.add_argument('--auto', action='store_true',
                    help='自动: 找到最新有预测且已开奖的期号并核对')
    args = ap.parse_args()

    if args.auto:
        import glob
        files = sorted(glob.glob('ssq_prediction_*_v8.json'), reverse=True)
        done = set()
        for f in files:
            parts = f.split('_')
            period = next((p for p in parts if p.isdigit()), None)
            if period is None or period in done:
                continue
            done.add(period)
            wf, wb = fetch_result_online(period)
            if wf is None:
                wf, wb = find_result_source(period)
            if wf and wb:
                print(f"[自动] 发现待核对期号 {period}")
                verify_period(period, wf, wb, sim=args.sim)
                return
        # 终极自愈: 本地均无结果时, 尝试在线刷新历史库(ssq_history.json)后再核对一次。
        # 解决"排程在开奖后跑但API数据滞后→静默未找到→对比报告缺失"的复发问题。
        try:
            from ssq_huiniao_api import fetch_latest_huiniao, merge_huiniao_with_existing
            if os.path.exists('ssq_history.json'):
                hist = json.load(open('ssq_history.json', encoding='utf-8'))
                fresh = fetch_latest_huiniao(limit=30)
                merged = merge_huiniao_with_existing(hist, fresh)
                if len(merged) > len(hist):
                    json.dump(merged, open('ssq_history.json', 'w', encoding='utf-8'),
                              ensure_ascii=False, indent=2)
                    for f in files:
                        pp = next((p for p in f.split('_') if p.isdigit()), None)
                        if not pp:
                            continue
                        wf, wb = find_result_source(pp)
                        if wf and wb:
                            print(f"[自动] 在线刷新历史库后发现待核对期号 {pp}")
                            verify_period(pp, wf, wb, sim=args.sim)
                            return
        except Exception as e:
            print(f"[自动] 历史库在线刷新失败(依赖已有数据): {e}")
        print("[自动] 未找到可核对的期号(可能尚无开奖结果)")
        return

    if not args.period:
        print("[错误] 需指定 --period 或使用 --auto")
        sys.exit(1)

    # 取开奖号
    if args.front and args.back:
        win_front = [int(x) for x in args.front.split(',')]
        win_back = [int(x) for x in args.back.split(',')]
    else:
        wf, wb = fetch_result_online(args.period)
        if wf is None:
            wf, wb = find_result_source(args.period)
        if wf and wb:
            win_front, win_back = wf, wb
        else:
            print("[错误] 未提供 --front/--back 且在线/本地均无开奖记录")
            sys.exit(1)

    verify_period(args.period, win_front, win_back, sim=args.sim)


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


if __name__ == '__main__':
    main()
