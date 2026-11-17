"""A股价值模型v2：规则阈值为工程参数，未经过收益回测校准。"""
import math
from datetime import date
from weight_registry import read_registry, resolve, DEFAULT_PATH

VERSION = "2.4.0"
MIN_COVERAGE = 70
# 结构性缺失项的总体期望分插补表。
# 只收"第三方来源缺失、公司自身并不掌握"的前瞻/行业项：没有机构覆盖就没有一致预期，
# 没有行业数据就没有景气度，这不代表公司表现差。公司自己披露的财务/资金/技术项一律不在此表，
# 缺失仍贡献0，避免"漏报坏数据反而加分"。
IMPUTE = {'forecast': 60, 'industry_boom': 50}
# 观测项（公司自己应披露的财务/资金/技术等）缺失时的兜底策略。处置顺序永远是「先补、再派生、最后兜底」：
#   ① 补数据：按 references/data-playbook.md 的取数路径去把缺的字段取回来（首选）；
#   ② 派生：能从已有原始数据算出来的，引擎自己算（ocf_to_np / np_yoy / dividend_* / industry_boom）；
#   ③ 结构性缺失（第三方来源，IMPUTE 白名单）：按总体期望分计价；
#   ④ 观测项缺失（下面的策略）——'neutral' 给中性默认分，'renorm' 从分母剔除后按剩余项归一。
# 默认 'neutral'：本 skill 的核心用法是「跨快照跟踪评分Δ」，归一会让数据完整度不同的标的
# 失去可比性（少报两项的分数会虚高），所以默认保留分母、只把缺项按中性分计价。
MISSING_FILL = 'neutral'
NEUTRAL_FALLBACK = 60
# 股息子项曲线与权重。分工刻意不重叠：
#   V 放"股息率−无风险利率"的利差 —— 衡量现金回报的吸引力，属估值；
#   Q 放"净利润/现金分红"的覆盖倍数 —— 衡量派息能否持续，属质量。
# 两者只在数据齐备时进入分母，缺一即整块不启用，避免只报对自己有利的那一半。
DIV_SPREAD_CURVE = [(-1,0),(0,50),(1,80),(2.5,100)]        # 单位：百分点
DIV_COVERAGE_CURVE = [(0.8,0),(1.2,45),(1.7,75),(2.5,100)]  # 单位：倍
DIV_V_WEIGHT = 20
DIV_Q_WEIGHT = 10
# 行业景气度：由申万行业财报TTM同比派生，净利为主(70)、营收为辅(30)
SECTOR_NP_CURVE = [(-20,0),(0,35),(10,60),(25,85),(50,100)]
SECTOR_REV_CURVE = [(-10,0),(0,40),(10,70),(25,100)]
# 大盘温度：4 个指标里拿到 ≥3 项即出分，按**可用项的权重和**归一（不再要求 4 项全齐）。
MIN_MARKET_ITEMS = 3
FINANCIAL = {"bank", "broker", "insurance"}
WEIGHTS = {"default": (25,20,20), "growth": (20,30,15), "value": (30,10,30),
           "cyclical": (25,15,25), "bank": (30,10,25), "broker": (30,10,25), "insurance": (30,10,25)}
DIM_NAME = dict(Q="基本面质量", G="成长性", V="估值", F="资金面", T="技术形态", N="消息情绪")
RATINGS = [(80,"A+","价值评分很高",15),(70,"A","价值评分较高",12),(60,"B+","价值评分中上",10),
           (50,"B","观察",6),(40,"C","价值评分偏低",3),(0,"D","回避",0)]


def number(x):
    return isinstance(x, (int,float)) and not isinstance(x,bool) and math.isfinite(x)


def positive(x):
    return number(x) and x > 0


def one_year_apart(later, earlier):
    """两个 period_end 是否相差约一年（350–380 天）。用于同比类派生，防止拿错窗口硬算。"""
    try:
        a, b = date.fromisoformat(str(later)[:10]), date.fromisoformat(str(earlier)[:10])
    except (TypeError, ValueError):
        return False
    return 350 <= (a-b).days <= 380


def calc_peg(pe, forecast_growth_pct):
    """仅作辅助展示：PE20、预测增长20(即20%) => 1；无预期/负增长不计算。"""
    return pe/forecast_growth_pct if positive(pe) and positive(forecast_growth_pct) else None


def day(x):
    try:
        return date.fromisoformat(x)
    except (TypeError,ValueError):
        return None


def evidence_error(meta, as_of, age=7, financial=False):
    if not isinstance(meta,dict) or not str(meta.get("source") or "").strip():
        return "缺少来源"
    now, obs = day(as_of), day(meta.get("as_of"))
    if not now or not obs or not 0 <= (now-obs).days <= age:
        return "数据日期无效、过期或晚于分析日"
    pub = day(meta.get("published_at"))
    if meta.get("published_at") and (not pub or pub > obs):
        return "公告日期无效或晚于数据日"
    if financial:
        end = day(meta.get("period_end"))
        if not end or not pub or not end <= pub <= obs or not 0 <= (now-end).days <= 550:
            return "财报报告期/公告日期缺失、过期或前后不一致"
    return None


def resolve_profile(industry, explicit=None):
    if explicit in WEIGHTS:
        return explicit
    groups = [(('银行',),'bank'),(('证券','券商'),'broker'),(('保险',),'insurance'),
              (('煤炭','钢铁','有色','石油','化工','水泥','造纸','养殖','金属'),'cyclical'),
              (('半导体','软件','计算机','电池','光伏','军工','游戏','通信','医疗器械'),'growth'),
              (('电力','公路','铁路','港口','水务','燃气','公用事业'),'value')]
    for names, profile in groups:
        if any(x in (industry or '') for x in names):
            return profile
    return 'unclassified_financial' if explicit == 'financial' or '金融' in (industry or '') else 'default'


def interp(x, pts):
    if not number(x):
        return None
    if x <= pts[0][0]:
        return pts[0][1]
    for (a,b),(c,d) in zip(pts,pts[1:]):
        if x <= c:
            return b+(x-a)/(c-a)*(d-b)
    return pts[-1][1]


def avg(xs):
    return sum(xs)/len(xs) if xs else None


def industry_boom_from_sector(np_yoy_pct, rev_yoy_pct=None):
    """申万行业财报TTM同比 → 0–100 行业景气分。

    净利同比权重70、营收同比权重30；只有净利时按净利单口径给分。
    取行业聚合数据派生，而不是让调用方手填一个0–100的中性值——
    手填会让所有标的拿到同一个数，等于不含个股信息。
    """
    np_score = interp(np_yoy_pct, SECTOR_NP_CURVE)
    if np_score is None:
        return None
    rev_score = interp(rev_yoy_pct, SECTOR_REV_CURVE)
    return round(np_score if rev_score is None else .7*np_score+.3*rev_score, 1)


# 字段、权重、0–100分的插值点/枚举；缺失项保留分母，不赠送中性分。
Q = [('roe_ttm',30,[(0,0),(5,40),(10,67),(15,87),(20,100)]),
     ('gross_margin',15,[(5,0),(15,40),(30,73),(50,100)]),
     ('net_margin',15,[(0,0),(5,40),(10,67),(20,100)]),
     ('debt_ratio',15,[(35,100),(55,73),(70,40),(85,0)]),
     ('ocf_to_np',15,[(0,0),(.5,40),(.8,67),(1.2,100)]),
     ('np_cv_3y',10,[(.1,100),(.3,70),(.6,40),(1,0)])]
Q_FIN = {
 'bank': [('roe_ttm',30,[(0,0),(4,33),(8,67),(12,100)]),
          ('provision_coverage',20,[(100,0),(150,53),(250,100)]),
          ('npl_ratio',25,[(0,100),(1,85),(2,50),(4,0)]),
          ('cet1_buffer_pct',25,[(0,0),(1,40),(3,80),(5,100)])],
 'broker': [('roe_normalized',35,[(0,0),(5,40),(10,80),(15,100)]),
            ('risk_coverage_ratio',35,[(100,0),(150,50),(250,100)]),
            ('net_capital_to_netasset',30,[(20,0),(40,50),(70,100)])],
 'insurance': [('roe_normalized',30,[(0,0),(5,40),(10,80),(15,100)]),
               ('core_solvency_ratio',35,[(50,0),(100,50),(200,100)]),
               ('comprehensive_solvency_ratio',35,[(100,0),(150,50),(250,100)])]}
G = [('rev_yoy',25,[(-10,0),(0,32),(10,60),(20,84),(35,100)]),
     ('np_yoy',30,[(-20,0),(0,33),(15,60),(30,83),(50,100)]),
     ('qoq_trend',15,dict(improving=100,flat=53,deteriorating=0)),
     ('forecast',20,dict(beat=100,inline=70,flat=40,miss=0)),
     ('industry_boom',10,[(0,0),(100,100)])]
F = [('main_inflow_20d_pct',30,[(-2,0),(0,40),(1,67),(3,100)]),
     ('inflow_5d',20,{'in':100,'flat':50,'out':0}),
     ('institution_change_pct',20,[(-.5,0),(0,50),(.5,100)]),
     ('volume_signal',15,dict(rising_expansion=100,normal=67,weak=33)),
     ('holders_change',15,dict(down=100,flat=53,up=0))]
T = [('ma_alignment',25,dict(bull=100,tangle=48,bear=0)),
     ('rs_60d',30,[(-10,0),(0,33),(5,67),(20,100)]),
     ('macd',20,dict(golden_expand=100,golden=70,death=20,death_expand=0)),
     ('drawdown_from_250d_high',15,[(0,100),(10,100),(20,73),(35,40),(50,0)]),
     ('annual_vol',10,[(25,100),(40,60),(60,0)])]
N = [('rating_buy_ratio',25,[(30,0),(50,60),(80,100)]),
     ('news_sentiment',25,dict(positive=100,neutral=52,negative=0)),
     ('major_announcement',20,dict(positive=100,neutral=50,negative=0)),
     ('risk_score',20,[(0,0),(100,100)]),
     ('research_visits_3m',10,[(0,20),(1,60),(4,60),(5,100)])]


def score_dimension(m, specs, na=()):
    """维度分=Σ(单项分×权重)/Σ计分权重。

    缺失项分三层处理（顺序即优先级）：
    1. 能补就补：派生字段（ocf_to_np / np_yoy / dividend_spread_pct / dividend_coverage /
       industry_boom）已在 checked_metrics 里由原始数据算出，这里拿到的已是补齐后的值；
    2. 结构性缺失（第三方来源缺失，IMPUTE 白名单）：按总体期望分计价，计入 imputed；
    3. 观测项缺失（公司应披露的财务/资金/技术等）：按 MISSING_FILL 兜底 ——
       'neutral' 给中性默认分 NEUTRAL_FALLBACK 并计入 neutral；'renorm' 从计分分母剔除。
    两个分母是分开的，这点很关键：
      - `all_weight`（所有适用项权重）只用于算 coverage —— 兜底/插补/归一都**不抬高覆盖率**，
        MIN_COVERAGE=70 的 NR 门槛完全不受本策略影响；
      - `used_weight`（实际计入计分的权重）只用于算 score —— neutral 时等于 all_weight，
        renorm 时等于「真实可用 + 插补」的权重和。
    """
    earned = available = all_weight = used_weight = imputed_weight = neutral_weight = 0
    missing, imputed, neutral = [], [], []
    for key, weight, curve in specs:
        if key in na:
            continue
        all_weight += weight
        value = m.get(key)
        sc = curve.get(value) if isinstance(curve,dict) and isinstance(value,str) else interp(value,curve) if isinstance(curve,list) else None
        if sc is not None:
            earned += sc*weight/100
            available += weight
            used_weight += weight
        elif key in IMPUTE:
            earned += IMPUTE[key]*weight/100
            imputed_weight += weight
            used_weight += weight
            imputed.append(key)
        elif MISSING_FILL == 'neutral':
            earned += NEUTRAL_FALLBACK*weight/100
            neutral_weight += weight
            used_weight += weight
            neutral.append(key)
        else:                                  # renorm：该权重整块退出计分分母
            missing.append(key)
    coverage = available/all_weight*100 if all_weight else 0
    return dict(score=round(earned/used_weight*100,1) if coverage >= MIN_COVERAGE and used_weight else None,
                coverage=round(coverage,1), imputed_weight=imputed_weight, neutral_weight=neutral_weight,
                missing=missing, imputed=imputed, neutral=neutral, not_applicable=list(na))


def checked_metrics(stock, as_of, risk_free=None):
    raw, meta = stock.get('indicators',{}), stock.get('indicator_meta',{})
    financial = {s[0] for s in Q+G+sum(Q_FIN.values(),[])} | {'net_profit_ttm','operating_cashflow_ttm','prior_net_profit','normalized_profit_growth_pct','cash_dividend_ttm'}
    financial -= {'forecast','industry_boom'}
    slow = {'forecast','industry_boom','cycle_recovery','institution_change_pct','holders_change','research_visits_3m',
            'dividend_yield_pct','sector_np_yoy_pct','sector_rev_yoy_pct'}
    clean, notes = {}, []
    for key,value in raw.items():
        if value is None:
            continue
        fin = key in financial
        err = evidence_error(meta.get(key),as_of,550 if fin else 90 if key in slow else 7,fin)
        if not (number(value) or isinstance(value,str)):
            err = '指标必须为有限数值或枚举；风险使用独立risk对象'
        if err:
            notes.append(f'{key}: {err}')
        else:
            clean[key] = value
    np_,ocf = clean.get('net_profit_ttm'),clean.get('operating_cashflow_ttm')
    clean.pop('ocf_to_np',None)
    if positive(np_) and number(ocf) and meta.get('net_profit_ttm',{}).get('period_end') == meta.get('operating_cashflow_ttm',{}).get('period_end'):
        clean['ocf_to_np'] = ocf/np_
    # 股息子项：利差与覆盖倍数都派生，不接受直接输入比值。
    # 两条必须同时成立才整块启用——否则调用方可以只报有利的那一半。
    clean.pop('dividend_spread_pct',None); clean.pop('dividend_coverage',None)
    if number(clean.get('dividend_yield_pct')) and number(risk_free):
        clean['dividend_spread_pct'] = round(clean['dividend_yield_pct']-risk_free,2)
    if positive(np_) and positive(clean.get('cash_dividend_ttm')):
        clean['dividend_coverage'] = round(np_/clean['cash_dividend_ttm'],2)
    # 行业景气度：有申万行业财报就用真实景气度派生，覆盖调用方手填值。
    # 留着手填路径是兼容旧输入，但派生一旦可用就以派生为准。
    boom = industry_boom_from_sector(clean.get('sector_np_yoy_pct'),clean.get('sector_rev_yoy_pct'))
    if boom is not None:
        clean['industry_boom'] = boom
    # np_yoy：有净利润TTM与去年同期利润就直接算，不必等调用方手填（与 ocf_to_np 同一套"能补就补"思路）。
    # 只在缺 np_yoy 时补，调用方已给就尊重其口径；两侧 period_end 需相差约一年，避免拿错窗口硬算。
    if (not number(clean.get('np_yoy')) and positive(np_) and positive(clean.get('prior_net_profit'))
            and one_year_apart(meta.get('net_profit_ttm',{}).get('period_end'),
                               meta.get('prior_net_profit',{}).get('period_end'))):
        clean['np_yoy'] = round((np_/clean['prior_net_profit']-1)*100,2)
        notes.append(f"np_yoy 由净利润TTM与去年同期利润派生：({np_}/{clean['prior_net_profit']}-1)×100"
                     f" = {clean['np_yoy']}%")
    if not positive(clean.get('prior_net_profit')):
        clean.pop('np_yoy',None)
    cv = meta.get('np_cv_3y',{})
    if cv.get('positive_mean') is not True or not number(cv.get('annual_samples')) or cv['annual_samples'] < 3:
        clean.pop('np_cv_3y',None)
    for key in ('debt_ratio','gross_margin','rating_buy_ratio','industry_boom','pe_pct','pb_pct','ps_pct','drawdown_from_250d_high','dividend_yield_pct'):
        if key in clean and (not number(clean[key]) or not 0 <= clean[key] <= 100):
            clean.pop(key)
            notes.append(f'{key}: 超出0–100有效范围')
    for key in ('annual_vol','np_cv_3y','npl_ratio','provision_coverage','core_solvency_ratio','comprehensive_solvency_ratio','research_visits_3m','cash_dividend_ttm'):
        if key in clean and (not number(clean[key]) or clean[key] < 0):
            clean.pop(key)
    for key in ('pe_pct','pb_pct','ps_pct'):
        history = meta.get(key,{})
        if key in clean and (history.get('basis')!='point_in_time' or not number(history.get('history_months')) or history['history_months']<36):
            clean.pop(key)
            notes.append(f'{key}: 需至少36个月同口径时点估值序列，不能用当前财务倒推历史')
    return clean,notes


def check_risk(stock, as_of):
    risk = stock.get('risk',{})
    events = risk.get('events')
    valid = risk.get('status') == 'checked' and isinstance(events,list) and all(isinstance(e,str) for e in events) and not evidence_error(risk,as_of)
    known = list(events) if isinstance(events,list) else []
    old = stock.get('indicators',{}).get('risk_events')
    if isinstance(old,list):
        known += old
    hard = {'ST','*ST','退市','退市预警','立案','立案调查','SPECIALTRADE'}
    flags = [str(e) for e in known if str(e).upper().strip() in hard or any(k in str(e) for k in ('退市','立案'))]
    return valid,flags,(100 if not events else 50 if len(events)==1 else 0) if valid else None


METHODS = {'default':{'normalized_pe','fcfe','fcff'}, 'growth':{'normalized_pe','fcfe','fcff','ev_sales'},
           'value':{'normalized_pe','ddm','fcfe','fcff'}, 'cyclical':{'normalized_pe','ev_ebitda','fcfe','fcff'},
           'bank':{'justified_pb','ddm','fcfe'}, 'broker':{'justified_pb','normalized_pe','ddm','fcfe'},
           'insurance':{'embedded_value','ddm','fcfe'}}


def required(s,key,pos=False):
    x = s.get(key)
    if not number(x) or (pos and x <= 0):
        raise ValueError(f'{key}缺失、非有限值或不满足正数要求')
    return x


def equity_bridge(s,ev):
    minority, assets = required(s,'minority_interest'), required(s,'non_operating_assets')
    if minority < 0 or assets < 0:
        raise ValueError('少数股东权益与非经营资产不得为负；净债务可为负')
    return (ev-required(s,'net_debt')-minority+assets)/required(s,'diluted_shares',True)


def scenario_value(method,s):
    if method == 'normalized_pe':
        return required(s,'eps_normalized',True)*required(s,'fair_pe',True)
    if method == 'justified_pb':
        roe,ke,g = (required(s,k)/100 for k in ('sustainable_roe_pct','cost_of_equity_pct','terminal_growth_pct'))
        if not ke > g >= 0 or roe <= g or ke <= 0:
            raise ValueError('PB稳态要求Ke>g>=0、ROE>g、Ke>0')
        return required(s,'bps',True)*(roe-g)/(ke-g)
    if method == 'embedded_value':
        return required(s,'embedded_value_per_share',True)*required(s,'fair_ev_multiple',True)
    if method in {'ev_ebitda','ev_sales'}:
        key = 'ebitda_normalized' if method=='ev_ebitda' else 'revenue_forward'
        return equity_bridge(s,required(s,key,True)*required(s,'fair_multiple',True))
    if method in {'fcfe','fcff','ddm'}:
        flows = s.get('cashflows')
        if not isinstance(flows,list) or not 3 <= len(flows) <= 10 or not all(number(x) for x in flows):
            raise ValueError('cashflows必须是3–10年的有限年末现金流')
        if method == 'ddm' and any(x<0 for x in flows):
            raise ValueError('股利不得为负')
        r,g = required(s,'discount_rate_pct',True)/100,required(s,'terminal_growth_pct')/100
        terminal = required(s,'terminal_cashflow',True)
        if not -1 < g < r:
            raise ValueError('终值增长必须大于-100%并低于折现率')
        pv = sum(x/(1+r)**i for i,x in enumerate(flows,1))+terminal/(r-g)/(1+r)**len(flows)
        return equity_bridge(s,pv) if method=='fcff' else pv
    raise ValueError('不支持的估值方法')


def calc_valuation(stock,profile,as_of):
    v = stock.get('valuation',{})
    method = v.get('method')
    out = dict(status='unavailable',method=method,valuation_as_of=as_of,horizon='current_fair_value',
               fair_value_bear=None,fair_value_base=None,fair_value_bull=None,
               assumptions=v.get('assumptions',{}),sources=v.get('sources',[]),scenario_inputs=v.get('scenarios',{}),
               confidence='insufficient',confidence_reason='',excluded_methods=['consensus_target','tech_resistance'])
    reasons = []
    err = evidence_error(v,as_of,90)
    if err:
        reasons.append(err)
    if method not in METHODS.get(profile,set()):
        reasons.append('方法不适用于当前行业，需选择适用基本面模型')
    if v.get('horizon') != 'current_fair_value':
        reasons.append('只接受估值日公允价值；未来目标价不得混入')
    assumptions = v.get('assumptions')
    if not isinstance(assumptions,dict) or not assumptions:
        reasons.append('缺少经营、倍数及再投资/资本约束假设')
    if not isinstance(v.get('sources'),list) or not v['sources'] or not all(isinstance(x,str) and x.strip() for x in v['sources']):
        reasons.append('缺少估值输入来源清单')
    if profile=='cyclical' and (not isinstance(assumptions,dict) or not assumptions.get('cycle_normalization')):
        reasons.append('周期企业需说明完整周期正常化和恢复路径')
    values = {}
    scenarios = v.get('scenarios',{})
    if not reasons:
        for name in ('bear','base','bull'):
            try:
                s = scenarios.get(name) if isinstance(scenarios,dict) else None
                if not isinstance(s,dict):
                    raise ValueError('缺少完整情景输入')
                value = scenario_value(method,s)
                if not positive(value):
                    raise ValueError('股权价值非正，需困境或清算分析')
                values[name] = value
            except (ValueError,TypeError,OverflowError) as exc:
                reasons.append(f'{name}: {exc}')
        if len(values)==3 and not values['bear'] <= values['base'] <= values['bull']:
            reasons.append('情景结果未满足保守≤基准≤乐观；不自动排序')
    if reasons:
        out['confidence_reason'] = '；'.join(reasons)
    else:
        out.update(status='available',confidence='scenario_based',confidence_reason='单一适用模型的条件情景；未校准概率，不是统计置信区间')
        for k,x in values.items():
            out[f'fair_value_{k}'] = round(x,2)
    return out


def derive_market_indicators(mk):
    """市场温度所需指标的自算层：显式给值优先，缺失才从原始序列自算。

    拿不到现成的 volume_ratio_5_250 / up_ratio_20d 时不再直接放弃温度分，
    改为用全市场成交额序列与逐日上涨占比序列算出来（成交额近似全市场量能）。
    派生值继承来源序列的 meta（`indicator_meta.<序列名>`），仍要过证据门槛，不走后门。
    返回 (补齐后的 market, {派生指标: 来源序列名})。
    """
    out, derived = dict(mk), {}
    source_meta = dict(out.get('indicator_meta') or {})
    meta = dict(source_meta)

    def usable(name, least, ok):
        s = out.get(name)
        if not isinstance(s,list) or len(s) < least or not all(number(x) and ok(x) for x in s):
            return None
        return s

    close = usable('hs300_close_series',250,lambda x:x>0)
    turnover = usable('turnover_series',250,lambda x:x>0)
    advance = usable('advance_ratio_series',20,lambda x:0<=x<=100)
    for key, src, value in (
            ('hs300_ma250_dev','hs300_close_series',
             (close[-1]/avg(close[-250:])-1)*100 if close else None),
            ('volume_ratio_5_250','turnover_series',
             avg(turnover[-5:])/avg(turnover[-250:]) if turnover else None),
            ('up_ratio_20d','advance_ratio_series',
             avg(advance[-20:]) if advance else None)):
        if number(out.get(key)) or not number(value):
            continue
        out[key] = value
        derived[key] = src
        if isinstance(source_meta.get(src),dict):
            meta[key] = source_meta[src]
    out['indicator_meta'] = meta
    return out, derived


def market_temperature(mk,as_of):
    mk, derived = derive_market_indicators(mk if isinstance(mk,dict) else {})
    specs = [('hs300_ma250_dev',30,[(-15,15),(0,50),(15,85)]),
             ('volume_ratio_5_250',20,[(.6,15),(1,50),(1.5,85)]),
             ('up_ratio_20d',20,[(35,15),(50,50),(60,85)]),
             ('broken_net_ratio',15,[(3,85),(10,50),(15,15)])]
    valid = {k:mk[k] for k,_,_ in specs if number(mk.get(k)) and not evidence_error(mk.get('indicator_meta',{}).get(k),as_of)}
    for k in ('up_ratio_20d','broken_net_ratio'):
        if k in valid and not 0 <= valid[k] <= 100:
            valid.pop(k)
    if 'volume_ratio_5_250' in valid and valid['volume_ratio_5_250']<0:
        valid.pop('volume_ratio_5_250')
    # 出分口径：4 项里拿到 ≥MIN_MARKET_ITEMS 项就出分，分母改用**可用项的权重和**（按权重归一）。
    # 旧口径要求 4 项全齐，缺任意一项就让整个温度分变成"数据不足"——等于让缺数据掩盖已有信息。
    used = [(k,w,pts) for k,w,pts in specs if k in valid]
    total_weight = sum(w for _,w,_ in specs)
    used_weight = sum(w for _,w,_ in used)
    temp = (round(sum(interp(valid[k],pts)*w for k,w,pts in used)/used_weight,1)
            if len(used) >= MIN_MARKET_ITEMS else None)
    coverage = round(used_weight/total_weight*100,1) if total_weight else 0.0
    state = '数据不足' if temp is None else '过热' if temp>=80 else '偏热' if temp>=65 else '中性' if temp>=40 else '偏冷' if temp>=25 else '冰点'
    notes = [f'缺失或过期：{k}' for k,_,_ in specs if k not in valid]
    notes += [f'{k} 由 {src} 自算（未提供现成值）' for k,src in derived.items()]
    if temp is not None and len(used) < len(specs):
        notes.append(f'温度分由 {len(used)}/{len(specs)} 项按权重归一得出'
                     f'（可用权重 {used_weight}/{total_weight}，覆盖率 {coverage}%）')
    return dict(temperature=temp,state=state,equity_range=None,cash_range=None,tone='市场温度不自动决定仓位',
                comment=mk.get('comment',''),coverage=coverage,used=[k for k,_,_ in used],
                missing=[k for k,_,_ in specs if k not in valid],min_items=MIN_MARKET_ITEMS,
                derived=derived,notes=notes)


def allocate(stocks,policy):
    out = dict(status='blocked',equity_pct=None,cash_pct=None,targets={},actions=[],warnings=[],
               watch_only=[{k:s.get(k) for k in ('code','name','total','grade')} for s in stocks if not s.get('holding')])
    reasons = []
    if policy.get('risk_tolerance') not in {'conservative','balanced','aggressive'}:
        reasons.append('缺少有效风险承受度')
    for k in ('horizon_years','max_drawdown_pct','total_assets'):
        if not positive(policy.get(k)):
            reasons.append(f'{k}需为正数')
    for k in ('cash_need_pct','equity_budget_pct','other_assets_pct'):
        if not number(policy.get(k)) or not 0 <= policy[k] <= 100:
            reasons.append(f'{k}需为0–100百分数')
    if policy.get('holdings_complete') is not True or policy.get('weight_basis')!='total_assets':
        reasons.append('需完整持仓及总资产分母，包含现金与其他资产')
    holdings = [s for s in stocks if s.get('holding')]
    if not holdings:
        reasons.append('无完整持仓，暂不配置')
    for s in holdings:
        if not s['risk_checked'] or s['grade']=='NR':
            reasons.append(f"{s['code']}风险未核查或证据不足")
        if not number(s.get('current_weight')) or not 0 <= s['current_weight'] <= 100:
            reasons.append(f"{s['code']}当前权重无效")
        if not s.get('industry') or not s.get('exposure_group'):
            reasons.append(f"{s['code']}缺少行业/产业链分组")
        if s.get('tradability')!='normal':
            reasons.append(f"{s['code']}停牌、涨跌停或交易状态未核实")
    if not reasons and sum(s['current_weight'] for s in holdings)+policy['other_assets_pct']>100+1e-6:
        reasons.append('持仓加其他资产权重超过100%')
    if reasons:
        out['warnings'] = reasons
        return out
    cash_min,other = max(5,policy['cash_need_pct']),policy['other_assets_pct']
    if cash_min+other>100:
        out['warnings'] = ['现金需求与其他资产合计超过100%']
        return out
    budget = min(policy['equity_budget_pct'],100-cash_min-other)
    pool = [s for s in holdings if s['grade'] not in {'C','D','NR'} and s['total'] is not None and s['total']>=50]
    weights = allocate_budget(holdings,pool,budget)
    equity = round(sum(weights.values()),2)
    out.update(status='reference',equity_pct=equity,requested_equity_pct=budget,other_assets_pct=other,
               cash_pct=round(100-other-equity,2),targets=weights)
    out['actions'] = [dict(code=s['code'],name=s['name'],current=s['current_weight'],target=weights[s['code']],
                           delta=round(weights[s['code']]-s['current_weight'],2),action='复核目标权重') for s in holdings]
    out['warnings'] = ['仅为约束预算参考，未生成买卖订单；交易费用、最小交易单位、实际可成交性需另行核实。',
                       '风险承受度、期限和回撤为政策记录；不推断个人最优预算，不保证回撤上限。']
    if equity<budget-.1:
        out['warnings'].append('受评级/集中度上限约束，未用预算留作现金')
    return out


def allocate_budget(holdings, pool, budget, group_cap=30):
    """按 merit（总分-45）比例填充预算，受单票评级上限与行业/产业链分组上限约束。

    每一轮都先基于**同一份权重快照**计算各标的额度，再一次性提交本轮增量。
    分组额度不足时按 merit 比例等比压缩该组额度，且压缩发生在单票上限之前——
    否则会被单票上限先截成同一数值、压缩后退化成平均分配，丢掉评分差异。
    逐只顺序提交会让排序靠前的标的先占满分组额度，使结果依赖股票代码顺序而非评分质量，
    因此这里必须同轮同步提交。
    """
    groups = ('industry','exposure_group')
    weights = {s['code']:0.0 for s in holdings}
    merits = {s['code']:max(s['total']-45,0) for s in pool}
    def own_room(s):
        return max(0.0,s['position_cap']-weights[s['code']])
    def group_room(s, group):
        return max(0.0,group_cap-sum(weights[x['code']] for x in holdings if x[group]==s[group]))
    for _ in range(100):
        remain = budget-sum(weights.values())
        active = [s for s in pool if merits[s['code']]>0
                  and min(own_room(s),*(group_room(s,g) for g in groups))>1e-8]
        if remain<1e-8 or not active:
            break
        total_merit = sum(merits[s['code']] for s in active)
        base = {s['code']:remain*merits[s['code']]/total_merit for s in active}
        limit = {s['code']:own_room(s) for s in active}
        for group in groups:
            for name in {s[group] for s in active}:
                members = [s['code'] for s in active if s[group]==name]
                room = group_cap-sum(weights[x['code']] for x in holdings if x[group]==name)
                if sum(min(base[c],limit[c]) for c in members)>room:
                    scale = room/sum(base[c] for c in members)
                    for c in members:
                        limit[c] = min(limit[c],base[c]*scale)
        step = {c:min(base[c],limit[c]) for c in base}
        if sum(step.values())<1e-12:
            break
        for code,value in step.items():
            weights[code] += value
    return {k:math.floor((v+1e-9)*100)/100 for k,v in weights.items()}


def map_rating(total):
    return ('NR','暂不评级',None) if total is None else next((g,a,c) for t,g,a,c in RATINGS if total>=t)


def evaluate(data, registry=None):
    if not isinstance(data,dict) or not isinstance(data.get('stocks',[]),list):
        raise ValueError('输入需为JSON对象，stocks需为数组')
    for k in ('market','portfolio_policy'):
        if not isinstance(data.get(k,{}),dict):
            raise ValueError(f'{k}需为对象，未知可省略或填空对象')
    as_of,results,codes = data.get('date'),[],set()
    weight_warnings = []
    # 无风险利率是市场级输入，供股息利差使用；同样要过证据门槛，缺失则股息子项整体不启用
    market = data.get('market',{})
    risk_free = market.get('risk_free_rate_pct')
    if not (number(risk_free) and 0 < risk_free <= 20) or evidence_error(market.get('indicator_meta',{}).get('risk_free_rate_pct'),as_of,90):
        risk_free = None
    if registry is None:
        try:
            registry = read_registry(DEFAULT_PATH)
        except (ValueError, OSError, TypeError):
            registry = {'schema_version':1, 'releases':[]}
            weight_warnings.append('权重文件无效，回退内置权重')
    for stock in data.get('stocks',[]):
        if not isinstance(stock,dict):
            raise ValueError('stocks的每个元素需为对象')
        for k in ('indicators','indicator_meta','risk','valuation','consensus'):
            if not isinstance(stock.get(k,{}),dict):
                raise ValueError(f'{k}需为对象，未知可省略或填空对象')
        if any(not isinstance(x,dict) for x in stock.get('indicator_meta',{}).values()):
            raise ValueError('indicator_meta的每项需为对象')
        for k in ('key_points','risks'):
            if not isinstance(stock.get(k,[]),list):
                raise ValueError(f'{k}需为数组')
        v=stock.get('valuation',{})
        if not isinstance(v.get('assumptions',{}),dict) or not isinstance(v.get('sources',[]),list):
            raise ValueError('valuation.assumptions需为对象，sources需为数组')
        code = stock.get('code')
        if not isinstance(code,str) or not code or code in codes:
            raise ValueError('每只股票必须有唯一非空code')
        codes.add(code)
        profile = resolve_profile(stock.get('industry'),stock.get('profile'))
        value_weights, weight_version, _ = resolve(registry,profile,as_of,WEIGHTS.get(profile,WEIGHTS['default']))
        w = value_weights | dict(F=15,T=10,N=10)
        m,notes = checked_metrics(stock,as_of,risk_free)
        risk_checked,flags,risk_score = check_risk(stock,as_of)
        m['risk_score'] = risk_score
        valuation = calc_valuation(stock,profile,as_of)
        price = stock.get('price') if positive(stock.get('price')) and not evidence_error(stock.get('price_meta'),as_of) else None
        fair = valuation['fair_value_base']
        margin = (1-price/fair)*100 if price and fair else None
        na = ['ocf_to_np','np_cv_3y'] if number(m.get('net_profit_ttm')) and m['net_profit_ttm']<=0 and profile not in FINANCIAL else []
        gs = list(G)
        if profile=='cyclical':
            gs[1] = ('cycle_recovery',30,dict(improving=100,flat=50,deteriorating=0))
        elif profile in {'broker','insurance'}:
            gs[1] = ('normalized_profit_growth_pct',30,G[1][2])
        elif number(m.get('net_profit_ttm')) and m['net_profit_ttm']<=0:
            gs[1] = ('loss_recovery',30,dict(improving=100,flat=50,deteriorating=0))
        pct = 'pb_pct' if profile in FINANCIAL|{'cyclical'} else 'ps_pct' if number(m.get('net_profit_ttm')) and m['net_profit_ttm']<=0 else 'pe_pct'
        vm = dict(m,margin_of_safety_pct=margin)
        if stock.get('indicator_meta',{}).get('rel_industry_discount',{}).get('multiple')!=pct[:2].upper():
            vm.pop('rel_industry_discount',None)
        # 股息子项：利差与覆盖倍数必须同时可用才启用，缺一即整块退出分母。
        # 这样没有股息数据的标的评分与旧版完全一致，不会被"没查分红"变相扣分。
        dividend_on = 'dividend_spread_pct' in m and 'dividend_coverage' in m
        if dividend_on:
            vs = [('margin_of_safety_pct',50,[(-50,0),(-20,20),(0,50),(20,75),(40,100)]),
                  (pct,15,[(0,100),(20,80),(50,50),(80,15),(100,0)]),
                  ('rel_industry_discount',15,[(-30,100),(-10,72),(0,48),(30,16),(60,0)]),
                  ('dividend_spread_pct',DIV_V_WEIGHT,DIV_SPREAD_CURVE)]
        else:
            vs = [('margin_of_safety_pct',60,[(-50,0),(-20,20),(0,50),(20,75),(40,100)]),
                  (pct,20,[(0,100),(20,80),(50,50),(80,15),(100,0)]),
                  ('rel_industry_discount',20,[(-30,100),(-10,72),(0,48),(30,16),(60,0)])]
        qs = list(Q_FIN.get(profile,Q))
        if dividend_on:
            # 追加股息子项时按比例压缩其余项，使 Q 的权重总和仍为100。
            # 不压缩的话分母变成110，等于给原有每一项都悄悄降权，Q 会被动漂移。
            scale = (100-DIV_Q_WEIGHT)/100
            qs = [(k,round(w*scale,6),c) for k,w,c in qs]+[('dividend_coverage',DIV_Q_WEIGHT,DIV_COVERAGE_CURVE)]
        quality = dict(Q=score_dimension(m,qs,na),G=score_dimension(m,gs),V=score_dimension(vm,vs),
                       F=score_dimension(m,F),T=score_dimension(m,T),N=score_dimension(m,N))
        notes = notes + [f'{k}维度：{", ".join(quality[k]["imputed"])} 无有效来源，按总体期望分插补；插补不提高覆盖率'
                         for k in ('Q','G','V','F','T','N') if quality[k]['imputed']]
        notes = notes + [f'{k}维度：{", ".join(quality[k]["neutral"])} 缺失，按中性默认分{NEUTRAL_FALLBACK}兜底计价'
                         f'（真实覆盖率{quality[k]["coverage"]}%，兜底不提高覆盖率，仍需先尝试补数据）'
                         for k in ('Q','G','V','F','T','N') if quality[k]['neutral']]
        if dividend_on:
            notes.append(f"股息子项已启用：利差{m['dividend_spread_pct']}pp（股息率{m['dividend_yield_pct']}%−无风险利率{risk_free}%），"
                         f"盈利覆盖{m['dividend_coverage']}倍；利差计V、覆盖计Q，不重复计分")
        elif number(m.get('dividend_yield_pct')):
            notes.append('已提供股息率，但缺有效无风险利率或现金分红，股息子项不启用，不进分母')
        if number(m.get('sector_np_yoy_pct')):
            notes.append(f"行业景气度由申万行业财报派生：净利同比{m['sector_np_yoy_pct']}%"
                         + (f"、营收同比{m['sector_rev_yoy_pct']}%" if number(m.get('sector_rev_yoy_pct')) else '（无营收项，按净利单口径）')
                         + '；派生优先于手填')
        dims = {k:x['score'] for k,x in quality.items()}
        gates = [f'{DIM_NAME[k]}覆盖率不足{MIN_COVERAGE}%' for k in 'QGV' if dims[k] is None]
        critical = {'bank':['roe_ttm','npl_ratio','cet1_buffer_pct'],'broker':['roe_normalized','risk_coverage_ratio'],
                    'insurance':['roe_normalized','core_solvency_ratio']}.get(profile,['roe_ttm','net_profit_ttm','operating_cashflow_ttm'])
        if any(not number(m.get(k)) for k in critical):
            gates.append('关键基本面数据缺失')
        if profile=='unclassified_financial':
            gates.append('金融企业需明确子行业')
        if not risk_checked:
            gates.append('风险核查未完成或已过期')
        if price is None or fair is None:
            gates.append('有效现价或基本面情景估值缺失')
        total = round(sum(dims[k]*w[k] for k in 'QGV')/sum(w[k] for k in 'QGV'),1) if not gates else None
        trading = round(sum(dims[k]*w[k] for k in 'FTN')/35,1) if all(dims[k] is not None for k in 'FTN') else None
        grade,action,cap = map_rating(total)
        if flags:
            grade,action,cap = 'D','硬风险：回避',0
            total = min(total,39) if total is not None else None
        elif grade!='NR':
            if profile not in FINANCIAL and number(m.get('debt_ratio')) and m['debt_ratio']>90 and number(m.get('operating_cashflow_ttm')) and m['operating_cashflow_ttm']<0:
                total = min(total,49)
                grade,action,cap = map_rating(total)
                flags.append('高负债且经营现金流金额为负，评级封顶C')
            for key,limit in (('major_shareholder_reduce_pct',2),('goodwill_to_netasset',30)):
                if number(m.get(key)) and m[key]>limit:
                    ladder = [r[1] for r in RATINGS]
                    grade = ladder[min(ladder.index(grade)+1,len(ladder)-1)]
                    _,_,action,cap = next(r for r in RATINGS if r[1]==grade)
                    flags.append(f'{key}>{limit}，评级下调一档')
        supports = [m[k]*.97 for k in ('ma60','low_3m') if positive(m.get(k)) and price and m[k]<price]
        stop = round(max(supports),2) if supports else None
        refs = dict(technical_resistance=m.get('tech_resistance'),consensus_target=None)
        ct = stock.get('consensus',{})
        inst = ct.get('institutions',[])
        if isinstance(inst,list) and len({x.strip() for x in inst if isinstance(x,str) and x.strip()})>=3 and not evidence_error(ct,as_of,90) and positive(ct.get('target')) and ct.get('horizon'):
            refs.update(consensus_target=ct['target'],consensus_horizon=ct['horizon'])
        results.append({**{k:stock.get(k) for k in ('code','name','industry','holding','current_weight','cost_price','market_value','pnl_pct','exposure_group','tradability')},
                        'dividend':dict(enabled=dividend_on,yield_pct=m.get('dividend_yield_pct'),spread_pct=m.get('dividend_spread_pct'),
                                        coverage=m.get('dividend_coverage'),
                                        spread_score=round(interp(m.get('dividend_spread_pct'),DIV_SPREAD_CURVE),1) if dividend_on else None,
                                        coverage_score=round(interp(m.get('dividend_coverage'),DIV_COVERAGE_CURVE),1) if dividend_on else None) if (dividend_on or number(m.get('dividend_yield_pct'))) else None,
                        'profile':profile,'price':price,'dims':dims,'weights':w,'weights_version':weight_version,'total':total,'trading_score':trading,
                        'tradability':stock.get('tradability') if not evidence_error(stock.get('tradability_meta'),as_of,1) else None,
                        'grade':grade,'action':action,'position_cap':cap,'risk_checked':risk_checked,'red_flags':flags,
                        'data_quality':quality,'rating_blockers':gates,'notes':notes,'valuation':valuation,
                        'target_price':fair,'target_methods':{valuation['method']:fair} if fair else {},'target_note':valuation['confidence_reason'],
                        'reference_prices':refs,'margin_of_safety_pct':round(margin,1) if margin is not None else None,
                        'upside_pct':round((fair/price-1)*100,1) if fair and price else None,
                        'stop_loss':stop,'stop_methods':{'技术支撑参考':stop} if stop else {},
                        'key_points':stock.get('key_points',[]),'risks':stock.get('risks',[]),
                        'sources':dict(indicator_meta=stock.get('indicator_meta',{}),price_meta=stock.get('price_meta',{}),risk=stock.get('risk',{}))})
    results.sort(key=lambda s:(s['total'] is None,-(s['total'] or 0),s['code']))
    return dict(model_version=VERSION,date=as_of,weight_warnings=weight_warnings,synthetic=data.get('synthetic') is True,stocks=results,market=market_temperature(data.get('market',{}),as_of),
                allocation=allocate(results,data.get('portfolio_policy',{})),
                disclaimer='评分与条件估值仅为公开数据量化参考，不构成投资建议，不承诺收益；v2阈值尚未完成历史收益校准。')


def compute_delta(cur,prev):
    old = {s['code']:s for s in prev.get('stocks',[])}
    deltas = []
    for s in cur['stocks']:
        p = old.get(s['code'])
        item = dict(code=s['code'],name=s['name'],new=p is None,total_delta=None,top_dims=[])
        if p and (cur.get('model_version')!=prev.get('model_version') or s['profile']!=p.get('profile') or s['total'] is None or p.get('total') is None):
            item.update(comparable=False,reason='模型版本/行业档位变化或存在未评级数据，重新建立基线')
        elif p:
            delta = round(s['total']-p['total'],1)
            old_w = {k:p['weights'][k]/sum(p['weights'][x] for x in 'QGV') for k in 'QGV'}
            new_w = {k:s['weights'][k]/sum(s['weights'][x] for x in 'QGV') for k in 'QGV'}
            contribution = [dict(dim=DIM_NAME[k],delta=round((s['dims'][k]-p['dims'][k])*old_w[k],2)) for k in 'QGV' if number(s['dims'].get(k)) and number(p.get('dims',{}).get(k))]
            weight_effect = sum(s['dims'][k]*(new_w[k]-old_w[k]) for k in 'QGV')
            data_effect = sum((s['dims'][k]-p['dims'][k])*old_w[k] for k in 'QGV')
            item.update(comparable=True,prev_total=p['total'],total_delta=delta,trend='改善' if delta>=3 else '恶化' if delta<=-3 else '基本持平',
                        grade_change=f"{p['grade']}→{s['grade']}",top_dims=contribution,
                        data_effect=round(data_effect,2),weight_effect=round(weight_effect,2),
                        risk_and_rounding_effect=round(delta-data_effect-weight_effect,2),
                        weights_version_change=f"{p.get('weights_version','legacy')}→{s.get('weights_version','legacy')}",
                        action_hint='数据变化按旧权重归因；调权影响及风险/舍入另列，不触发自动交易')
        deltas.append(item)
    cur['deltas'] = deltas
    return cur


def template():
    fields = {s[0] for s in Q+G+F+T+N+sum(Q_FIN.values(),[])} | {'net_profit_ttm','operating_cashflow_ttm','prior_net_profit','pe_pct','pb_pct','ps_pct','rel_industry_discount','cycle_recovery','loss_recovery','normalized_profit_growth_pct','ma60','low_3m','tech_resistance','major_shareholder_reduce_pct','goodwill_to_netasset','dividend_yield_pct','cash_dividend_ttm','sector_np_yoy_pct','sector_rev_yoy_pct'}
    # 派生项不填：ocf_to_np、risk_score 由模型算；dividend_spread_pct/dividend_coverage/industry_boom 同理
    fields -= {'risk_score','ocf_to_np'}
    return dict(schema_version=VERSION,date=None,market={},
                portfolio_policy={k:None for k in ('risk_tolerance','horizon_years','max_drawdown_pct','total_assets','cash_need_pct','equity_budget_pct','other_assets_pct','holdings_complete','weight_basis')},
                stocks=[dict(code='example',name='待填标的',industry=None,profile=None,holding=False,price=None,price_meta={},current_weight=None,
                             exposure_group=None,tradability=None,tradability_meta={},indicators={k:None for k in sorted(fields)},indicator_meta={},
                             risk=dict(status='not_checked',events=None,source=None,as_of=None),
                             valuation=dict(method='normalized_pe',source=None,sources=[],as_of=None,horizon='current_fair_value',assumptions={},
                                            scenarios={k:dict(eps_normalized=None,fair_pe=None) for k in ('bear','base','bull')}))])
