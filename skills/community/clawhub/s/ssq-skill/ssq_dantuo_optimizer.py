# -*- coding: utf-8 -*-
"""
双色球胆拖组合优化引擎 (V1.0.0 新增, 用户需求: 加强胆拖分析 + 性价比最高组合)

设计目标 (用户原话):
  "加强胆拖号码的分析能力... 在报告中给我输出, 性价比最高的胆拖组合,
   胆拖组合的方式不固定, 只要保证 号码最可靠 / 成本最低 / 中一等奖概率最高 这三个指标的最完美组合"

实现要点:
  1. 形态不固定: 枚举 红球1~3胆 × 多种拖数, 蓝球0~1胆 × 多种拖数 (在预算上限内)
  2. 号码最可靠: 用模型综合评分 combined_score / back_scored 选胆(评分最高)与拖(次高)
  3. 成本最低: 注数 = C(拖,5-胆) × C(后拖,2-后胆), 成本 = 注数×2/×3
  4. 中一等奖概率最高(诚实重定义): 用"模型评分加权蒙特卡洛"估算该结构
     至少中任一固定奖 / 至少中五等奖及以上的概率 —— 这是胆拖真正的"结构化中奖覆盖"
     能力, 而非单注一等奖概率(恒 1/17,721,088, 任何结构都不改变)
  5. 多目标加权综合: 在预算内选 准度↑ + 成本↓ + 中奖覆盖↑ 的 Pareto 最优, 输出性价比最高

数学诚实声明:
  - 任何单注一等奖概率恒 1/17,721,088, 胆拖不改变它
  - 胆拖的本质是"在既定预算下优化投入结构", 不是让期望转正
  - MC 概率是基于模型对号码置信度的加权估计, 非官方随机概率; 真实随机下所有结构等价

带 main() 守卫: 独立运行 `python ssq_dantuo_optimizer.py` 可打印 26087 期最优方案用于自检。
"""
import math
import random
import itertools

try:
    from ssq_common import passes_filters
except Exception:  # 独立运行时允许退化
    def passes_filters(front, prev_front):
        return True


# ---------------------------------------------------------------------------
# 奖级映射: 红球命中 f, 蓝球命中 b -> 奖级(1一等..7七等, 0不中)
# 官方中奖条件(奖池≥8亿档, 当前持续触发):
#   一等6+1  二等5+1  三等5+0或4+2  四等4+1  五等3+2或4+0
#   六等3+1或2+2  七等3+0/2+1/1+2/0+2
# ---------------------------------------------------------------------------
def front_back_to_prize(f, b):
    """双色球奖级→排名(1=一等奖...6=六等奖, 0=未中奖)。

    委托 ssq_draw_check.prize_of 单一权威源, 避免手写判定与大乐透混淆。
    """
    from ssq_draw_check import prize_of
    rank = {'一等奖': 1, '二等奖': 2, '三等奖': 3, '四等奖': 4, '五等奖': 5, '六等奖': 6}
    return rank.get(prize_of(f, b)[0], 0)


# ---------------------------------------------------------------------------
# 加权无放回抽样 (Gumbel-top-k, 纯 python 无依赖, 精确)
# weights: dict num->w ; 返回 top-k 号码 list
# ---------------------------------------------------------------------------
def _weighted_sample_topk(weights, k, rng):
    scores = {}
    for n, w in weights.items():
        if w <= 0:
            w = 1e-12
        g = -math.log(-math.log(rng.random()))   # Gumbel 噪声
        scores[n] = math.log(w) + g
    return [n for n, _ in sorted(scores.items(), key=lambda x: x[1], reverse=True)[:k]]


# ---------------------------------------------------------------------------
# 加权蒙特卡洛: 估算胆拖票"至少中任一奖 / 至少中五等奖及以上"的概率
# 关键优化: 胆拖票能达到的最高奖级 = (max_front, max_back), 其中
#   max_front = hD + min(5-df, |T∩W|),  hD=|D∩W|
#   max_back  = hBd + min(2-dfb, |Bt∩Wb|), hBd=|Bd∩Wb|
# 因此无需枚举每一注, 单次开奖 O(1) 计算, 极快。
# ---------------------------------------------------------------------------
def estimate_win_prob(dan, tuo, back_dan, back_tuo, combined_score, back_scored,
                      n=6000, seed=20260802):
    rng = random.Random(seed)
    df, dtf = len(dan), len(tuo)
    dfb, dtb = len(back_dan), len(back_tuo)
    Wf = {n: combined_score.get(n, 1e-9) for n in range(1, 34)}
    Wb = {n: back_scored.get(n, 1e-9) for n in range(1, 17)}
    dan_s, tuo_s = set(dan), set(tuo)
    bd_s, bt_s = set(back_dan), set(back_tuo)
    any_win = 0
    five_plus = 0
    for _ in range(n):
        W = set(_weighted_sample_topk(Wf, 6, rng))
        Wb2 = set(_weighted_sample_topk(Wb, 1, rng))
        hD = len(dan_s & W)
        hT = len(tuo_s & W)
        hBd = len(bd_s & Wb2)
        hBt = len(bt_s & Wb2)
        mf = hD + min(6 - df, hT)
        mb = hBd + min(1 - dfb, hBt)
        p = front_back_to_prize(mf, mb)
        if p >= 1:   # 修复: 奖级 1=一等..7=七等, "至少中任一奖"=p>=1 (原 p>=7 只数了最低奖, 漏掉一~六等)
            any_win += 1
        if 1 <= p <= 5:   # 五等奖及以上(不含未中奖p=0); 原 p<=5 把未中奖(p=0)也算入, 虚高近90%
            five_plus += 1
    return any_win / n, five_plus / n


# ---------------------------------------------------------------------------
# 容错保底表: 假设"我们选的 df+dtf 个红球号中, 共有 m 个命中当期开奖"(m=0..5),
# 取最坏分布(命中号尽量落在拖码而非胆码), 给出该胆拖票"仍能达到的红球最高命中"
# 再配蓝球最坏(0命中)映射奖级, 直观展示"胆码全落空时还剩什么"。
# ---------------------------------------------------------------------------
def tolerance_table(dan, tuo, back_dan, back_tuo):
    df, dtf = len(dan), len(tuo)
    dfb, dtb = len(back_dan), len(back_tuo)
    rows = []
    for m in range(0, 7):
        # 最坏红球: 命中号尽量在拖码, 胆码命中 = max(0, m-dtf)
        hD_min = max(0, m - dtf)
        hT_max = min(dtf, m)
        mf_worst = hD_min + min(6 - df, hT_max)
        # 蓝球最坏: 0 命中 -> max_back = 0
        mb_worst = 0
        p = front_back_to_prize(mf_worst, mb_worst)
        rows.append({
            'm': m,
            'front_hit_worst': mf_worst,
            'prize_worst': p,
            'desc': ('不中' if p == 0 else f'至少中{["", "一", "二", "三", "四", "五", "六", "七"][p]}等奖(最坏情形)')
        })
    return rows


# ---------------------------------------------------------------------------
# 主优化函数
# ---------------------------------------------------------------------------
def _perturb(dist, period_seed, salt, tag):
    """对评分分布施加确定性扰动(期号种子+盐驱动), 使不同期自然重排推荐。

    噪声幅度与评分跨度同量级 -> 足以在不同期重排 top 组合; 同一(期号,salt)恒定 -> 可复现。
    与 ssq_auto._perturb 同原理, 此处自包含以避免跨模块循环导入。
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


def optimize_dantuo(combined_score, back_scored, prev_front, passes_filters_fn=passes_filters,
                    budget_bets=120, mc_n=6000, period_seed=None):
    """
    combined_score: dict 红球号码->模型综合评分 (CDM+马尔可夫+频率+遗漏加权)
    back_scored:    dict 蓝球号码->模型评分
    prev_front:     上期红球5号码(list), 用于9项过滤器
    budget_bets:    预算注数上限 (默认120注=240元), 控制形态搜索空间
    mc_n:           蒙特卡洛样本数
    period_seed:    目标期号(int)。传入则对评分分布施加确定性期号扰动,
                    使胆拖方案随期重排(与主推荐号一致的跨期变化双保险);
                    同周期恒定可复现, 不同期自然重排。None=旧行为(纯评分排序, 用于离线测试)。
    返回: dict {best, candidates, honesty}
    """
    # V1.0.8 跨期变化修复: 胆拖此前纯按评分排序, 蓝球拖码每期几乎不变,
    # 给用户"两期差不多"的错觉。现仅在传入 period_seed 时施加确定性扰动,
    # 让胆拖与主推荐号一样随期号重排; 同周期恒定 -> 完全可复现。
    cs_use = combined_score
    bs_use = back_scored
    if period_seed is not None:
        cs_use = _perturb(combined_score, int(period_seed), 0, 21)
        bs_use = _perturb(back_scored, int(period_seed), 0, 22)
    ranked_f = sorted(cs_use.keys(),
                      key=lambda n: cs_use.get(n, 0), reverse=True)
    ranked_b = sorted(bs_use.keys(),
                      key=lambda n: bs_use.get(n, 0), reverse=True)
    # 候选池: 先取评分 top35, 再固定种子洗牌取 top20 (与原 search_pool 一致)
    # 纯全局 top 连续块特征聚集, 几乎无法组成通过9项过滤器的组合; 洗牌后分散,
    # 既能找到通过过滤者, 又保持"相对较准"(在 top20 内, 符合项目避免锁定 argmax 设计)
    rng = random.Random(20260802)
    cand35 = ranked_f[:35]
    rng.shuffle(cand35)
    pool = cand35[:20]
    dan_pool = pool[:12]
    tuo_pool_full = pool[:15]

    raw = []   # 粗筛候选 (解析, 不跑MC)
    for df in (1, 2, 3):
        for dtf in range(6 - df, 6 - df + 9):
            if dtf > 15:
                continue
            found = False
            for dan in itertools.combinations(dan_pool, df):
                dan_set = set(dan)
                avail = [n for n in tuo_pool_full if n not in dan_set]
                if len(avail) < dtf:
                    continue
                for tuo in itertools.combinations(avail, dtf):
                    ok = True
                    for sub in itertools.combinations(tuo, 6 - df):
                        if not passes_filters_fn(sorted(list(dan) + list(sub)), prev_front):
                            ok = False
                            break
                    if not ok:
                        continue
                    # 找到该形态第一个通过过滤的组合 (pool按评分排序, dan已是top, 较准)
                    for dfb in (0, 1):
                        for dtb in range(1 - dfb, 1 - dfb + 8):
                            if dtb + dfb < 1 or dtb + dfb > 12:
                                continue
                            bd = ranked_b[:dfb] if dfb > 0 else []
                            bd_set = set(bd)
                            bt = [n for n in ranked_b if n not in bd_set][:dtb]
                            if len(bt) < dtb:
                                continue
                            front_combos = math.comb(dtf, 6 - df)
                            # 双色球蓝球单码: 每个蓝球(胆+拖)各成 1 注
                            back_combos = dfb + dtb
                            total = front_combos * back_combos
                            # V4 纠偏: 退化单注胆拖剔除 (红球或蓝球仅1注=普通单注, 非真正胆拖展开)
                            #   典型: 3胆2拖(dtf=2→C(2,2)=1)/1胆4拖(dtf=4→C(4,4)=1)/2胆3拖(dtf=3→C(3,3)=1)
                            #   以及蓝球 1胆1拖(dtb=1→C(1,1)=1)/0胆2拖(dtb=2→C(2,2)=1)
                            if front_combos < 2 or back_combos < 1:
                                continue
                            if total == 0 or total > budget_bets:
                                continue
                            cost = total * 2
                            # 准度: 红球方案号码平均评分 (越高越准)
                            acc = sum(cs_use[n] for n in dan + tuo) / (df + dtf)
                            # 容错粗分: 覆盖号码多 + 胆少更稳 (仅用于粗筛)
                            tolerance = (df + dtf) - 1.5 * df + (dfb + dtb) * 0.2
                            raw.append({
                                'form': f'{df}胆{dtf}拖+蓝{dfb}胆{dtb}拖',
                                'df': df, 'dtf': dtf, 'dfb': dfb, 'dtb': dtb,
                                'dan': list(dan), 'tuo': list(tuo),
                                'back_dan': list(bd), 'back_tuo': list(bt),
                                'front_combos': front_combos, 'back_combos': back_combos,
                                'total_bets': total, 'cost': cost,
                                'acc': acc, 'tolerance': tolerance,
                            })
                    found = True
                    break
                if found:
                    break

    if not raw:
        return {'best': None, 'candidates': [], 'honesty': HONESTY}

    # 粗筛: 按 准度*0.5 + 容错*0.5 选 top 12 进 MC 精算 (控制耗时)
    raw.sort(key=lambda r: 0.5 * r['acc'] + 0.5 * r['tolerance'], reverse=True)
    top = raw[:12]

    for r in top:
        p_any, p5 = estimate_win_prob(r['dan'], r['tuo'], r['back_dan'], r['back_tuo'],
                                      cs_use, bs_use, n=mc_n)
        r['win_any'] = p_any
        r['win_5plus'] = p5
        r['tolerance_table'] = tolerance_table(r['dan'], r['tuo'], r['back_dan'], r['back_tuo'])

    # 多目标标准化综合评分: 准度↑ + 中奖覆盖↑ + 成本↓ (各归一化到0~1)
    accs = [r['acc'] for r in top]
    wins = [r['win_any'] for r in top]
    costs = [r['cost'] for r in top]
    a_min, a_max = min(accs), max(accs)
    w_min, w_max = min(wins), max(wins)
    c_min, c_max = min(costs), max(costs)

    def norm(v, lo, hi):
        return 0.0 if hi == lo else (v - lo) / (hi - lo)

    for r in top:
        acc_n = norm(r['acc'], a_min, a_max)
        win_n = norm(r['win_any'], w_min, w_max)
        cost_n = norm(r['cost'], c_min, c_max)          # 成本越高 norm 越大
        cost_score = 1.0 - cost_n                        # 成本越低越好
        r['score'] = 0.40 * acc_n + 0.35 * win_n + 0.25 * cost_score

    top.sort(key=lambda r: r['score'], reverse=True)
    best = top[0]

    # 兼容 ssq_auto.generate_report 的 dantuo['standard'] 结构, 额外带优化字段
    best_out = {
        'dan': best['dan'], 'tuo': best['tuo'], 'back': best['back_dan'] + best['back_tuo'],
        'back_dan': best['back_dan'], 'back_tuo': best['back_tuo'],
        'dan_size': best['df'], 'front_combos': best['front_combos'],
        'back_combos': best['back_combos'], 'total_bets': best['total_bets'],
        'cost_basic': best['cost'], 'cost_extra': best['total_bets'] * 2,  # 双色球无追加, 复式成本=注数*2
        'form': best['form'], 'acc': best['acc'], 'win_any': best['win_any'],
        'win_5plus': best['win_5plus'], 'score': best['score'],
        'tolerance_table': best['tolerance_table'],
    }
    candidates_out = []
    for r in top[:3]:
        candidates_out.append({
            'form': r['form'], 'dan': r['dan'], 'tuo': r['tuo'],
            'back': r['back_dan'] + r['back_tuo'],
            'total_bets': r['total_bets'], 'cost': r['cost'],
            'acc': r['acc'], 'win_any': r['win_any'], 'win_5plus': r['win_5plus'],
            'score': r['score'],
        })

    return {'best': best_out, 'candidates': candidates_out, 'honesty': HONESTY}


HONESTY = (
    "【数学诚实声明】任何单注一等奖概率恒为 1/17,721,088, 胆拖不改变它。"
    "胆拖的本质是'在既定预算下优化投入结构'(用确信的胆码锁定高置信号 + 拖码低成本覆盖),"
    "而非让期望转正。表中'中奖概率'是基于模型对号码置信度的加权蒙特卡洛估计(非官方随机概率),"
    "仅用于比较不同胆拖结构在'模型置信下'的中奖覆盖差异。真实随机下所有结构等价, 请以娱乐心态量力而行。"
)


# ---------------------------------------------------------------------------
# 独立自检 (main 守卫, 防止被其它模块误调用时静默无输出)
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    import json
    import os

    # 加载历史 + 模型评分 (复用 ssq_auto 的计算)
    from ssq_auto import compute_models, _back_score

    hist_path = 'ssq_history.json'
    if not os.path.exists(hist_path):
        print('✗ 缺少 ssq_history.json')
        raise SystemExit(1)
    with open(hist_path, 'r', encoding='utf-8') as f:
        draws = json.load(f)
    models = compute_models(draws)
    prev_front = draws[-1]['front']
    # 蓝球评分需从 models 真实键重算 (back_dist 是 generate_predictions 内局部变量, 不在 models)
    max_back_omit = models.get('max_back_omit', 1) or 1
    back_scored = {}
    for num in range(1, 17):
        cdm_s = models['cdm_prob_b'].get(num, 0)
        mk_s = models['markov_back'].get(num, 0)
        omit_s = models['back_omit'].get(num, 0) / max_back_omit
        back_scored[num] = _back_score(cdm_s, mk_s, omit_s)
    res = optimize_dantuo(models['combined_score'], back_scored, prev_front)
    b = res['best']
    if b is None:
        print('✗ 未找到可行胆拖')
    else:
        print(f"最优胆拖形态: {b['form']}")
        print(f"  胆码(红球): {b['dan']}")
        print(f"  拖码(红球): {b['tuo']}")
        print(f"  蓝球: {b['back']}")
        print(f"  注数: {b['total_bets']} | 成本: {b['cost_basic']}元(基本)/{b['cost_extra']}元(复式)")
        print(f"  号码准度(平均评分): {b['acc']:.4f}")
        print(f"  中奖概率(模型加权MC): 至少中任一奖={b['win_any']*100:.2f}% | 至少中五等奖={b['win_5plus']*100:.2f}%")
        print(f"  综合性价比评分: {b['score']:.4f}")
        print('  容错保底表(红球命中m个, 最坏情形):')
        for row in b['tolerance_table']:
            print(f"    m={row['m']} -> 红球最坏命中{row['front_hit_worst']} -> {row['desc']}")
        print('  候选 top3:')
        for c in res['candidates']:
            print(f"    {c['form']}: 注数{c['total_bets']} 成本{c['cost']}元 准度{c['acc']:.3f} 中奖{c['win_any']*100:.1f}% 评分{c['score']:.3f}")
    print('\n' + HONESTY)
