"""人工构造数据的回归测试；不代表真实行情或历史收益回测。"""
import copy
import json
import unittest
import tempfile
import io
from argparse import Namespace
from contextlib import redirect_stdout
from pathlib import Path
import value_model as m
import build_report
import portfolio_ledger

DATE = '2026-09-05'


def meta(**extra):
    return dict(source='synthetic fixture / not real market data',as_of=DATE,
                published_at='2026-08-25',period_end='2026-06-30',**extra)


def stock(code='demo',profile='default'):
    indicators = dict(roe_ttm=18,gross_margin=40,net_margin=20,debt_ratio=35,
                      net_profit_ttm=100,operating_cashflow_ttm=150,prior_net_profit=80,np_cv_3y=.1,
                      rev_yoy=25,np_yoy=25,qoq_trend='improving',forecast='inline',industry_boom=80,
                      pe_pct=20,pb_pct=20,ps_pct=20,rel_industry_discount=-20,
                      main_inflow_20d_pct=1,inflow_5d='in',institution_change_pct=.2,
                      volume_signal='normal',holders_change='down',ma_alignment='bull',rs_60d=10,
                      macd='golden',drawdown_from_250d_high=10,annual_vol=25,
                      rating_buy_ratio=80,news_sentiment='neutral',major_announcement='neutral',research_visits_3m=4,
                      tech_resistance=100,ma60=12,low_3m=10,cycle_recovery='improving',loss_recovery='improving',
                      roe_normalized=12,risk_coverage_ratio=250,net_capital_to_netasset=70,
                      provision_coverage=250,npl_ratio=1,cet1_buffer_pct=4,
                      core_solvency_ratio=200,comprehensive_solvency_ratio=250,normalized_profit_growth_pct=20)
    metadata = {k:meta() for k in indicators}
    metadata['np_cv_3y'].update(positive_mean=True,annual_samples=3)
    for k in ('pe_pct','pb_pct','ps_pct'):
        metadata[k].update(basis='point_in_time',history_months=60)
    metadata['rel_industry_discount']['multiple'] = 'PB' if profile in m.FINANCIAL|{'cyclical'} else 'PE'
    valuation = dict(method='normalized_pe',source='synthetic',sources=['synthetic financial statements'],as_of=DATE,
                     horizon='current_fair_value',assumptions={'normalization':'合成样本，非真实预测','cycle_normalization':'合成完整周期'},
                     scenarios={k:dict(eps_normalized=eps,fair_pe=10) for k,eps in [('bear',1.5),('base',2),('bull',2.5)]})
    if profile in {'bank','broker'}:
        valuation['method'] = 'justified_pb'
        valuation['scenarios'] = {k:dict(bps=10,sustainable_roe_pct=roe,cost_of_equity_pct=10,terminal_growth_pct=2) for k,roe in [('bear',10),('base',12),('bull',14)]}
    if profile=='insurance':
        valuation['method']='embedded_value'
        valuation['scenarios']={k:dict(embedded_value_per_share=20,fair_ev_multiple=x) for k,x in [('bear',.7),('base',1),('bull',1.2)]}
    return dict(code=code,name='合成样本 '+code,industry='合成行业',profile=profile,holding=True,price=15,
                price_meta=meta(),indicators=indicators,indicator_meta=metadata,current_weight=5,
                exposure_group='合成产业链',tradability='normal',tradability_meta=meta(),
                risk=dict(status='checked',events=[],source='synthetic risk check',as_of=DATE),valuation=valuation)


def data(stocks=None):
    market = dict(hs300_ma250_dev=0,volume_ratio_5_250=1,up_ratio_20d=50,broken_net_ratio=10)
    market['indicator_meta']={k:meta() for k in market}
    return dict(synthetic=True,date=DATE,stocks=stocks if stocks is not None else [stock()],market=market,
                portfolio_policy=dict(risk_tolerance='balanced',horizon_years=5,max_drawdown_pct=20,
                                      total_assets=1000000,cash_need_pct=10,equity_budget_pct=70,
                                      other_assets_pct=15,holdings_complete=True,weight_basis='total_assets'))


def first(s):
    return m.evaluate(data([s]))['stocks'][0]


class ModelTests(unittest.TestCase):
    def test_pressure_and_consensus_do_not_change_fair_value(self):
        s=stock()
        a=first(s)
        s['indicators']['tech_resistance']=10000
        s['consensus']=dict(target=1000,institutions=['a','b','c'],source='synthetic',as_of=DATE,horizon='12 months')
        b=first(s)
        self.assertEqual(a['target_price'],20)
        self.assertEqual(a['target_price'],b['target_price'])
        self.assertEqual(a['total'],b['total'])
        self.assertEqual(b['reference_prices']['consensus_target'],1000)

    def test_technical_only_no_value(self):
        s=stock();s.pop('valuation')
        r=first(s)
        self.assertIsNone(r['target_price']);self.assertEqual(r['grade'],'NR')

    def test_empty_data_no_rating_allocation_or_market(self):
        r=m.evaluate(dict(stocks=[dict(code='empty',holding=True)]))
        self.assertIsNone(r['stocks'][0]['total']);self.assertEqual(r['stocks'][0]['grade'],'NR')
        self.assertIsNone(r['market']['temperature']);self.assertIsNone(r['allocation']['cash_pct'])
        self.assertFalse(r['allocation']['targets']);self.assertFalse(r['allocation']['actions'])

    def test_risk_missing_is_not_checked_empty(self):
        s=stock();valid=first(s);s.pop('risk');missing=first(s)
        self.assertNotEqual(valid['grade'],'NR');self.assertEqual(missing['grade'],'NR')
        self.assertFalse(missing['risk_checked'])

    def test_hard_risk_overrides_missing_data(self):
        for event in ('ST','*ST','立案调查','退市预警'):
            r=first(dict(code='risk',risk=dict(events=[event])))
            self.assertEqual(r['grade'],'D');self.assertEqual(r['position_cap'],0)

    def test_unknown_english_risk_not_substring_st(self):
        s=stock();s['risk']['events']=['cost increase']
        self.assertNotEqual(first(s)['grade'],'D')

    def test_financial_profiles_and_debt_not_rewarded(self):
        for profile in m.FINANCIAL:
            s=stock(profile=profile);s['indicators']['debt_ratio']=85;a=first(s)
            s['indicators']['debt_ratio']=99;b=first(s)
            self.assertEqual(a['dims']['Q'],b['dims']['Q'])
            self.assertIsNotNone(a['total'])
            if profile!='bank':
                s['indicators'].pop('provision_coverage');self.assertEqual(first(s)['dims']['Q'],b['dims']['Q'])

    def test_unclassified_financial_not_default_bank(self):
        s=stock();s['profile']='financial';self.assertEqual(first(s)['grade'],'NR')

    def test_cyclical_requires_normalization_and_uses_recovery(self):
        s=stock(profile='cyclical');a=first(s)
        s['indicators']['np_yoy']=-99;self.assertEqual(first(s)['dims']['G'],a['dims']['G'])
        s['valuation']['assumptions'].pop('cycle_normalization');self.assertIsNone(first(s)['target_price'])

    def test_negative_cashflow_ratio_not_sign_proxy(self):
        s=stock();s['indicators'].update(debt_ratio=95,net_profit_ttm=-100,operating_cashflow_ttm=20,ocf_to_np=-.2)
        s['indicator_meta']['rel_industry_discount']['multiple']='PS'
        r=first(s)
        self.assertFalse(any('经营现金流金额为负' in x for x in r['red_flags']))
        self.assertIn('ocf_to_np',r['data_quality']['Q']['not_applicable'])
        s['indicators']['operating_cashflow_ttm']=-20
        r=first(s)
        self.assertTrue(any('经营现金流金额为负' in x for x in r['red_flags']))

    def test_missing_data_cannot_improve_dimension(self):
        s=stock();a=first(s);s['indicators'].pop('gross_margin');b=first(s)
        self.assertLess(b['dims']['Q'],a['dims']['Q'])
        s['indicators'].pop('roe_ttm');self.assertEqual(first(s)['grade'],'NR')

    def test_structural_missing_uses_expectation_score(self):
        """无机构覆盖/无行业数据属结构性缺失，按期望分插补，不再当作0分。"""
        s=stock();a=first(s)
        self.assertEqual(a['dims']['G'],81.9);self.assertFalse(a['data_quality']['G']['imputed'])
        for key in ('forecast','industry_boom'):
            s['indicators'].pop(key)
        b=first(s)
        self.assertEqual(b['data_quality']['G']['imputed'],['forecast','industry_boom'])
        self.assertFalse(b['data_quality']['G']['missing'])
        self.assertEqual(b['dims']['G'],76.9)
        self.assertLess(b['dims']['G'],a['dims']['G'])
        self.assertGreater(b['dims']['G'],59.9)

    def test_imputation_does_not_raise_coverage_or_bypass_nr(self):
        s=stock()
        for key in ('forecast','industry_boom'):
            s['indicators'].pop(key)
        b=first(s)
        self.assertEqual(b['data_quality']['G']['coverage'],70.0)
        self.assertEqual(b['data_quality']['G']['imputed_weight'],30)
        self.assertIsNotNone(b['dims']['G'])
        s['indicators'].pop('qoq_trend')
        c=first(s)
        self.assertLess(c['data_quality']['G']['coverage'],m.MIN_COVERAGE)
        self.assertIsNone(c['dims']['G']);self.assertEqual(c['grade'],'NR')

    def test_observable_missing_item_gets_neutral_not_expected_impute(self):
        """观测项缺失：不走结构性期望分插补，改按中性默认分兜底；
        且兜底必须高于已知最差表现、且不抬高覆盖率——否则"漏报坏数据反而加分"。"""
        for key in ('net_margin','debt_ratio','main_inflow_20d_pct','annual_vol'):
            self.assertNotIn(key,m.IMPUTE)
        full=first(stock())
        s=stock();s['indicators'].pop('net_margin');b=first(s)
        q=b['data_quality']['Q']
        self.assertIn('net_margin',q['neutral'])        # 走中性兜底
        self.assertNotIn('net_margin',q['imputed'])     # 不是结构性期望分
        self.assertNotIn('net_margin',q['missing'])     # 也不再被丢弃计0
        self.assertEqual(q['neutral_weight'],15)
        self.assertEqual(q['coverage'],85.0)            # 兜底不抬高覆盖率
        self.assertLess(b['dims']['Q'],full['dims']['Q'])
        s=stock();s['indicators']['debt_ratio']=85;worst=first(s)
        s=stock();s['indicators'].pop('debt_ratio');absent=first(s)
        self.assertGreater(absent['dims']['Q'],worst['dims']['Q'])   # 缺项 ≠ 最差
        self.assertEqual(absent['data_quality']['Q']['imputed_weight'],0)
        self.assertLess(absent['dims']['Q'],full['dims']['Q'])       # 兜底仍低于真实数据

    def test_neutral_fill_keeps_score_comparable(self):
        """中性兜底的分母与齐全时一致，所以"分数Δ"在数据完整度变化时仍可比。"""
        full=first(stock())
        s=stock();s['indicators'].pop('net_margin');partial=first(s)
        self.assertEqual(partial['data_quality']['Q']['neutral'],['net_margin'])
        self.assertTrue(any('中性默认分' in n for n in partial['notes']))
        self.assertLessEqual(partial['dims']['Q'],full['dims']['Q'])

    def test_renorm_policy_drops_weight_from_denominator(self):
        """MISSING_FILL='renorm' 时缺项退出计分分母，但覆盖率仍按真实数据算。"""
        old=m.MISSING_FILL
        try:
            m.MISSING_FILL='renorm'
            s=stock();s['indicators'].pop('net_margin');r=first(s)
            q=r['data_quality']['Q']
            self.assertIn('net_margin',q['missing'])
            self.assertFalse(q['neutral'])
            self.assertEqual(q['neutral_weight'],0)
            self.assertEqual(q['coverage'],85.0)        # 覆盖率不受策略影响
        finally:
            m.MISSING_FILL=old

    def test_np_yoy_is_derived_from_ttm_and_prior(self):
        """能补就补：给了净利润TTM与去年同期利润，np_yoy 由引擎自己算。"""
        s=stock()
        s['indicators'].pop('np_yoy')
        s['indicators']['net_profit_ttm']=120
        s['indicators']['prior_net_profit']=100
        s['indicator_meta']['net_profit_ttm']['period_end']='2026-06-30'
        s['indicator_meta']['prior_net_profit']['period_end']='2025-06-30'
        r=first(s)
        self.assertTrue(any('np_yoy 由净利润TTM' in n for n in r['notes']))
        self.assertEqual(r['data_quality']['G']['neutral'].count('np_yoy'),0)
        # 期间不是"约一年"时不派生，退回兜底
        s2=stock();s2['indicators'].pop('np_yoy')
        s2['indicator_meta']['prior_net_profit']['period_end']='2026-06-30'
        self.assertEqual(first(s2)['data_quality']['G']['neutral'].count('np_yoy'),1)

    def test_imputation_is_traced_in_notes_and_report(self):
        css=Path(__file__).resolve().parent.parent.joinpath('assets/report.css').read_text(encoding='utf-8')
        s=stock()
        for key in ('forecast','industry_boom'):
            s['indicators'].pop(key)
        r=first(s)
        self.assertTrue(any('期望分插补' in n for n in r['notes']))
        html=build_report.render(m.evaluate(data([s])),css)
        self.assertIn('按总体期望分插补',html)

    def test_stale_future_and_missing_sources(self):
        for edit in ({'as_of':'2025-01-01'},{'as_of':'2026-10-01'},{'source':''}):
            s=stock();s['price_meta'].update(edit)
            self.assertEqual(first(s)['grade'],'NR')
        s=stock();s['indicator_meta']['roe_ttm']['published_at']='2026-10-01'
        self.assertEqual(first(s)['grade'],'NR')

    def test_history_cannot_use_today_eps(self):
        s=stock();s['indicator_meta']['pe_pct']['basis']='today_eps'
        v=first(s)['data_quality']['V']
        self.assertIn('pe_pct',v['neutral'])      # 口径不合规被剔除，不进真实计分
        self.assertFalse(v['imputed'])
        self.assertLess(v['coverage'],100.0)

    def test_peg_units_and_invalid_growth(self):
        self.assertEqual(m.calc_peg(20,20),1)
        for g in (None,0,-10,float('nan')):
            self.assertIsNone(m.calc_peg(20,g))

    def test_valuation_scenarios_invalid_inputs(self):
        for invalid in (0,-1,float('nan'),float('inf'),True):
            s=stock();s['valuation']['scenarios']['base']['fair_pe']=invalid
            self.assertIsNone(first(s)['target_price'])
        s=stock();s['valuation']['scenarios']['bear']['eps_normalized']=100
        self.assertIsNone(first(s)['target_price'])
        s=stock();s['valuation']['horizon']='12_months';self.assertIsNone(first(s)['target_price'])

    def test_pb_formula_and_growth_constraint(self):
        scenario=dict(bps=10,sustainable_roe_pct=12,cost_of_equity_pct=10,terminal_growth_pct=2)
        self.assertAlmostEqual(m.scenario_value('justified_pb',scenario),12.5)
        scenario['terminal_growth_pct']=10
        with self.assertRaises(ValueError):m.scenario_value('justified_pb',scenario)

    def test_dcf_and_ev_bridge(self):
        s=dict(cashflows=[1,1,1],discount_rate_pct=10,terminal_growth_pct=0,terminal_cashflow=1)
        self.assertAlmostEqual(m.scenario_value('fcfe',s),10)
        s.update(net_debt=2,minority_interest=1,non_operating_assets=1,diluted_shares=2)
        self.assertAlmostEqual(m.scenario_value('fcff',s),4)
        self.assertAlmostEqual(m.scenario_value('ev_ebitda',dict(ebitda_normalized=10,fair_multiple=5,net_debt=10,minority_interest=2,non_operating_assets=4,diluted_shares=2)),21)
        s['terminal_growth_pct']=10
        with self.assertRaises(ValueError):m.scenario_value('fcfe',s)

    def test_trading_environment_does_not_change_value(self):
        s=stock();a=first(s)
        s['indicators'].update(ma_alignment='bear',news_sentiment='negative',main_inflow_20d_pct=-10)
        b=first(s);self.assertEqual(a['total'],b['total']);self.assertLess(b['trading_score'],a['trading_score'])

    def test_allocation_ignores_code_order_within_group(self):
        """分组额度是共享的：分配必须按评分比例，不能因为代码排序靠前就多吃额度。"""
        def run(pairs):
            stocks=[]
            for code,roe in pairs:
                s=stock(code);s['industry']='同一行业';s['exposure_group']='同一产业链'
                s['indicators']['roe_ttm']=roe
                stocks.append(s)
            r=m.evaluate(data(stocks))
            return ({s['code']:s['total'] for s in r['stocks']},r['allocation']['targets'])
        weak,mid,strong=5,12,25
        results=[]
        for pairs in ([('aaa',weak),('mmm',mid),('zzz',strong)],
                      [('zzz',weak),('aaa',mid),('mmm',strong)]):
            totals,targets=run(pairs)
            order=[c for c,_ in pairs]
            self.assertLess(totals[order[0]],totals[order[2]])
            self.assertLess(targets[order[0]],targets[order[1]])
            self.assertLess(targets[order[1]],targets[order[2]])
            self.assertGreater(targets[order[0]],0)
            self.assertAlmostEqual(sum(targets.values()),30.0,places=1)
            results.append(sorted(targets.values()))
        self.assertEqual(results[0],results[1])

    def test_allocation_constraints_and_zero_grade_exits(self):
        stocks=[stock(str(i)) for i in range(12)]
        for i,s in enumerate(stocks):
            s['industry']=f'industry{i//3}';s['exposure_group']=f'chain{i//4}'
        stocks[0]['risk']['events']=['ST']
        r=m.evaluate(data(stocks));a=r['allocation']
        self.assertEqual(a['status'],'reference');self.assertEqual(a['targets']['0'],0)
        self.assertAlmostEqual(sum(a['targets'].values())+a['cash_pct']+a['other_assets_pct'],100)
        self.assertGreaterEqual(a['cash_pct'],10)
        for s in r['stocks']:
            self.assertLessEqual(a['targets'][s['code']],s['position_cap'])
        for group in ('industry','exposure_group'):
            for name in {s[group] for s in stocks}:
                self.assertLessEqual(sum(a['targets'][s['code']] for s in stocks if s[group]==name),30+1e-6)
        self.assertLessEqual(sum(sorted(a['targets'].values(),reverse=True)[:3]),55)

    def test_policy_trading_or_risk_missing_blocks_allocation(self):
        d=data();d.pop('portfolio_policy');self.assertEqual(m.evaluate(d)['allocation']['status'],'blocked')
        for field in ('risk','tradability_meta'):
            d=data();d['stocks'][0].pop(field);self.assertEqual(m.evaluate(d)['allocation']['status'],'blocked')

    def test_empty_eligible_pool_is_cash_not_phantom_equity(self):
        d=data();d['stocks'][0]['risk']['events']=['ST']
        a=m.evaluate(d)['allocation'];self.assertEqual(a['equity_pct'],0);self.assertEqual(a['cash_pct'],85)

    def test_duplicate_stock_rejected(self):
        with self.assertRaises(ValueError):m.evaluate(data([stock(),stock()]))

    def test_malformed_structures_rejected(self):
        for bad in ([],dict(stocks={}),dict(stocks=[None]),dict(stocks=[dict(code='x',indicator_meta=None)])):
            with self.assertRaises(ValueError):m.evaluate(bad)

    def test_ledger_requires_total_assets_and_handles_margin(self):
        with tempfile.TemporaryDirectory() as folder:
            positions=[dict(code='demo',shares=100,current_price=10,cost_price=8)]
            path=Path(folder)/'positions.json'
            path.write_text(json.dumps(dict(positions=positions)),encoding='utf-8')
            def weights(total_assets):
                output=io.StringIO()
                with redirect_stdout(output):
                    portfolio_ledger.cmd_weights(Namespace(dir=folder,prices=None,total_assets=total_assets))
                return json.loads(output.getvalue())
            self.assertIsNone(weights(None)['positions'][0]['current_weight'])
            self.assertEqual(weights(10000)['positions'][0]['current_weight'],10)
            with self.assertRaises(ValueError):weights(500)
            positions[0]['margin']=True
            path.write_text(json.dumps(dict(positions=positions)),encoding='utf-8')
            self.assertIsNone(weights(10000)['positions'][0]['current_weight'])

    def test_delta_legacy_and_unrated(self):
        r=m.evaluate(data());old=copy.deepcopy(r);old['model_version']='1.0.0'
        self.assertFalse(m.compute_delta(r,old)['deltas'][0]['comparable'])
        r=m.evaluate(data());self.assertEqual(m.compute_delta(r,copy.deepcopy(r))['deltas'][0]['total_delta'],0)
        old=copy.deepcopy(r);old['stocks'][0]['total']=None
        self.assertFalse(m.compute_delta(r,old)['deltas'][0]['comparable'])

    def test_reports_for_complete_empty_and_legacy_delta(self):
        css=Path(__file__).resolve().parent.parent.joinpath('assets/report.css').read_text(encoding='utf-8')
        for r in (m.evaluate(data()),m.evaluate(dict(stocks=[dict(code='empty')]))):
            html=build_report.render(r,css)
            self.assertIn('基准公允价值',html);self.assertNotIn('>None<',html)
        d=data();d['stocks'][0]['name']='<script>alert(1)</script>'
        r=m.evaluate(d);old=copy.deepcopy(r);old['model_version']='1.0'
        html=build_report.render(m.compute_delta(r,old),css)
        self.assertNotIn('<script>alert(1)</script>',html)
        self.assertIn('&lt;script&gt;',html)


def eval_one(s, **market):
    """在默认市场上叠加市场级输入；新增键自动补合成 meta。"""
    d = data([s])
    for k, v in market.items():
        d['market'][k] = v
        d['market']['indicator_meta'][k] = meta()
    return m.evaluate(d)['stocks'][0]


def with_dividend(s, yld=4.5, cash_dividend=40):
    """补股息原始输入。利差与覆盖倍数由模型派生，不接受直接输入。"""
    s['indicators'].update(dividend_yield_pct=yld, cash_dividend_ttm=cash_dividend)
    for k in ('dividend_yield_pct','cash_dividend_ttm'):
        s['indicator_meta'][k] = meta()
    return s


def with_sector(s, np_yoy=30, rev_yoy=None):
    s['indicators']['sector_np_yoy_pct'] = np_yoy
    s['indicator_meta']['sector_np_yoy_pct'] = meta()
    if rev_yoy is not None:
        s['indicators']['sector_rev_yoy_pct'] = rev_yoy
        s['indicator_meta']['sector_rev_yoy_pct'] = meta()
    return s


class DividendTests(unittest.TestCase):
    """股息子项：V 收利差、Q 收覆盖倍数；缺一半就整块不启用。"""

    def test_absent_dividend_data_changes_nothing(self):
        base = eval_one(stock(profile='value'))
        self.assertIsNone(base['dividend'])
        s = stock(profile='value')
        s['indicators'].pop('pe_pct')          # 只动无关项，确认基线可比
        self.assertNotEqual(eval_one(s)['dims']['V'], base['dims']['V'])

    def test_each_half_alone_does_not_activate(self):
        base = eval_one(stock(profile='value'))
        # 只有股息率、没有现金分红
        s = stock(profile='value')
        s['indicators']['dividend_yield_pct'] = 4.5
        s['indicator_meta']['dividend_yield_pct'] = meta()
        half = eval_one(s, risk_free_rate_pct=2.0)
        self.assertFalse(half['dividend']['enabled'])
        self.assertEqual(half['dims'], base['dims'])
        self.assertEqual(half['total'], base['total'])
        # 原始数据齐全但没有无风险利率
        no_rf = eval_one(with_dividend(stock(profile='value')))
        self.assertFalse(no_rf['dividend']['enabled'])
        self.assertEqual(no_rf['dims'], base['dims'])

    def test_high_yield_raises_and_negative_spread_lowers(self):
        base = eval_one(stock(profile='value'))
        rich = eval_one(with_dividend(stock(profile='value')), risk_free_rate_pct=2.0)
        self.assertTrue(rich['dividend']['enabled'])
        self.assertEqual(rich['dividend']['spread_pct'], 2.5)     # 4.5 − 2.0
        self.assertEqual(rich['dividend']['coverage'], 2.5)       # 100 / 40
        self.assertGreater(rich['dims']['V'], base['dims']['V'])
        self.assertGreater(rich['dims']['Q'], base['dims']['Q'])
        self.assertGreater(rich['total'], base['total'])
        # 股息率低于无风险利率：利差为负，应按 0 分处理并压低估值分
        poor = eval_one(with_dividend(stock(profile='value'), yld=0.5), risk_free_rate_pct=2.0)
        self.assertEqual(poor['dividend']['spread_pct'], -1.5)
        self.assertLess(poor['dims']['V'], base['dims']['V'])
        self.assertLess(poor['total'], base['total'])

    def test_low_earnings_coverage_scores_lower(self):
        thin = eval_one(with_dividend(stock(profile='value'), cash_dividend=95), risk_free_rate_pct=2.0)
        thick = eval_one(with_dividend(stock(profile='value'), cash_dividend=30), risk_free_rate_pct=2.0)
        self.assertLess(thin['dividend']['coverage'], thick['dividend']['coverage'])
        self.assertLess(thin['dims']['Q'], thick['dims']['Q'])

    def test_derived_fields_cannot_be_injected(self):
        """利差与覆盖倍数一律由原始数据重算，直接塞分值不生效。"""
        s = with_dividend(stock(profile='value'))
        s['indicators'].update(dividend_spread_pct=999, dividend_coverage=999)
        for k in ('dividend_spread_pct','dividend_coverage'):
            s['indicator_meta'][k] = meta()
        r = eval_one(s, risk_free_rate_pct=2.0)
        self.assertEqual(r['dividend']['spread_pct'], 2.5)
        self.assertEqual(r['dividend']['coverage'], 2.5)
        # 只塞派生字段、不给原始数据 → 完全不启用
        bare = stock(profile='value')
        bare['indicators'].update(dividend_spread_pct=999, dividend_coverage=999)
        for k in ('dividend_spread_pct','dividend_coverage'):
            bare['indicator_meta'][k] = meta()
        off = eval_one(bare, risk_free_rate_pct=2.0)
        self.assertIsNone(off['dividend'])
        self.assertEqual(off['dims'], eval_one(stock(profile='value'))['dims'])

    def test_weights_stay_summed_to_hundred(self):
        """股息子项只在维度内部让权，Q/G/V 之间的相对权重与总和都不变。"""
        base = eval_one(stock(profile='value'))
        on = eval_one(with_dividend(stock(profile='value')), risk_free_rate_pct=2.0)
        self.assertEqual(sum(base['weights'][k] for k in 'QGV'), 100)
        self.assertEqual(sum(on['weights'][k] for k in 'QGV'), 100)
        self.assertEqual(base['weights'], on['weights'])
        self.assertEqual(on['dividend']['spread_score'], 100.0)      # 利差 2.5pp 顶格
        self.assertEqual(on['dividend']['coverage_score'], 100.0)    # 覆盖 2.5 倍顶格

    def test_dividend_block_is_rendered_in_report(self):
        css = Path(__file__).resolve().parent.parent.joinpath('assets/report.css').read_text(encoding='utf-8')
        s = with_dividend(stock(profile='value'))
        d = data([s])
        d['market']['risk_free_rate_pct'] = 2.0
        d['market']['indicator_meta']['risk_free_rate_pct'] = meta()
        html = build_report.render(m.evaluate(d), css)
        self.assertIn('股息利差', html)
        self.assertIn('盈利覆盖', html)
        self.assertIn('股息子项已启用', html)

    def test_activation_is_traced_in_notes(self):
        r = eval_one(with_dividend(stock(profile='value')), risk_free_rate_pct=2.0)
        self.assertTrue(any('股息子项已启用' in n for n in r['notes']))
        r = eval_one(with_dividend(stock(profile='value')))
        self.assertTrue(any('股息子项不启用' in n for n in r['notes']))


class IndustryBoomTests(unittest.TestCase):
    """行业景气度改由申万行业财报派生,替代对所有标的等额 50 分的插补。"""

    def test_sector_finance_overrides_handtyped_value(self):
        base = eval_one(stock())                    # 手填 industry_boom=80
        self.assertEqual(base['dims']['G'], 81.9)
        self.assertFalse(base['data_quality']['G']['imputed'])
        derived = eval_one(with_sector(stock(), np_yoy=30))
        self.assertFalse(derived['data_quality']['G']['imputed'])
        self.assertNotIn('industry_boom', derived['data_quality']['G']['missing'])
        self.assertGreater(derived['dims']['G'], base['dims']['G'])

    def test_boom_differs_across_stocks(self):
        hot = eval_one(with_sector(stock('hot'), np_yoy=45, rev_yoy=20))
        cold = eval_one(with_sector(stock('cold'), np_yoy=-10, rev_yoy=-10))
        self.assertGreater(hot['dims']['G'], cold['dims']['G'])
        self.assertGreater(m.industry_boom_from_sector(45, 20), m.industry_boom_from_sector(-10, -10))

    def test_revenue_component_has_thirty_percent_weight(self):
        np_only = m.industry_boom_from_sector(30)
        self.assertEqual(np_only, 88.0)
        self.assertGreater(m.industry_boom_from_sector(30, 30), np_only)
        self.assertLess(m.industry_boom_from_sector(30, -10), np_only)
        self.assertIsNone(m.industry_boom_from_sector(None))

    def test_falls_back_to_impute_without_sector_data(self):
        s = stock(); s['indicators'].pop('industry_boom')
        r = eval_one(s)
        self.assertEqual(r['data_quality']['G']['imputed'], ['industry_boom'])
        self.assertGreater(r['dims']['G'], 59.9)

    def test_sector_data_must_pass_evidence_gate(self):
        s = with_sector(stock(), np_yoy=30)
        s['indicators'].pop('industry_boom')
        # 有有效行业数据 → 派生，不走插补
        self.assertFalse(eval_one(copy.deepcopy(s))['data_quality']['G']['imputed'])
        # 无 meta / 过期 / 无来源 → 过不了门槛，退回插补
        for edit in ({'as_of':'2025-01-01'}, {'source':''}):
            s2 = copy.deepcopy(s)
            s2['indicator_meta']['sector_np_yoy_pct'].update(edit)
            self.assertIn('industry_boom', eval_one(s2)['data_quality']['G']['imputed'])
        s2 = copy.deepcopy(s); s2['indicator_meta'].pop('sector_np_yoy_pct')
        self.assertIn('industry_boom', eval_one(s2)['data_quality']['G']['imputed'])


class MarketTemperatureTests(unittest.TestCase):
    """市场温度：现成标量优先，缺失时从原始序列自算。"""

    def test_derive_exact_values_from_series(self):
        out, derived = m.derive_market_indicators(dict(
            turnover_series=[100.0]*245+[300.0]*5,
            advance_ratio_series=[40.0]*5+[60.0]*20,
            hs300_close_series=[100.0]*249+[110.0]))
        self.assertEqual(round(out['volume_ratio_5_250'],6), round(300/104,6))
        self.assertEqual(out['up_ratio_20d'], 60.0)
        self.assertEqual(round(out['hs300_ma250_dev'],6), round((110/100.04-1)*100,6))
        self.assertEqual(set(derived), {'hs300_ma250_dev','volume_ratio_5_250','up_ratio_20d'})

    def test_explicit_scalar_wins_over_series(self):
        out, derived = m.derive_market_indicators(dict(
            volume_ratio_5_250=1.0, turnover_series=[100.0]*245+[300.0]*5))
        self.assertEqual(out['volume_ratio_5_250'], 1.0)
        self.assertNotIn('volume_ratio_5_250', derived)

    def test_too_short_or_out_of_range_series_is_ignored(self):
        for mk, key in ((dict(turnover_series=[1.0]*100),'volume_ratio_5_250'),
                        (dict(turnover_series=[1.0]*249+[0.0]),'volume_ratio_5_250'),
                        (dict(advance_ratio_series=[101.0]*20),'up_ratio_20d'),
                        (dict(advance_ratio_series=[50.0]*19),'up_ratio_20d')):
            out, _ = m.derive_market_indicators(mk)
            self.assertNotIn(key, out)

    def test_temperature_becomes_available_from_series_alone(self):
        d = data(); mkt = d['market']
        for k in ('hs300_ma250_dev','volume_ratio_5_250','up_ratio_20d'):
            mkt.pop(k); mkt['indicator_meta'].pop(k)
        self.assertIsNone(m.evaluate(d)['market']['temperature'])      # 原本数据不足
        mkt['turnover_series'] = [100.0]*245+[300.0]*5
        mkt['advance_ratio_series'] = [60.0]*20
        mkt['hs300_close_series'] = [100.0]*249+[110.0]
        for k in ('turnover_series','advance_ratio_series','hs300_close_series'):
            mkt['indicator_meta'][k] = meta()
        market = m.evaluate(d)['market']
        self.assertIsNotNone(market['temperature'])
        self.assertEqual(set(market['derived']), {'hs300_ma250_dev','volume_ratio_5_250','up_ratio_20d'})
        self.assertTrue(any('自算' in n for n in market['notes']))

    def test_derived_indicator_inherits_source_evidence(self):
        d = data(); mkt = d['market']
        for k in ('volume_ratio_5_250','up_ratio_20d'):
            mkt.pop(k); mkt['indicator_meta'].pop(k)
        mkt['turnover_series'] = [100.0]*245+[300.0]*5
        mkt['advance_ratio_series'] = [60.0]*20
        # 序列无 meta：派生值继承不到来源，过不了证据门槛
        self.assertIsNone(m.evaluate(d)['market']['temperature'])
        for k in ('turnover_series','advance_ratio_series'):
            mkt['indicator_meta'][k] = meta()
        self.assertIsNotNone(m.evaluate(d)['market']['temperature'])

    def test_three_items_are_enough_and_weights_renormalize(self):
        """4 项里拿到 3 项就出分，分母改用可用项权重和（旧口径缺 1 项直接不显示温度）。"""
        d = data(); mkt = d['market']
        mkt['up_ratio_20d'] = 60                      # 该点插值=85，使归一化可见
        mkt.pop('broken_net_ratio'); mkt['indicator_meta'].pop('broken_net_ratio')
        market = m.evaluate(d)['market']
        self.assertIsNotNone(market['temperature'])
        self.assertEqual(set(market['used']),
                         {'hs300_ma250_dev','volume_ratio_5_250','up_ratio_20d'})
        self.assertEqual(market['missing'], ['broken_net_ratio'])
        self.assertEqual(market['coverage'], 82.4)    # (30+20+20)/85
        # (50*30 + 50*20 + 85*20)/70 = 60.0；若误用 85 做分母会得到 49.4
        self.assertEqual(market['temperature'], 60.0)
        self.assertTrue(any('按权重归一' in n for n in market['notes']))

    def test_fewer_than_three_items_stays_unavailable(self):
        """不足 3 项仍判数据不足，不硬凑温度分。"""
        d = data(); mkt = d['market']
        for k in ('up_ratio_20d','broken_net_ratio'):
            mkt.pop(k); mkt['indicator_meta'].pop(k)
        market = m.evaluate(d)['market']
        self.assertIsNone(market['temperature'])
        self.assertEqual(market['state'], '数据不足')
        self.assertEqual(market['coverage'], 58.8)    # (30+20)/85
        self.assertIn(m.MIN_MARKET_ITEMS, (market['min_items'],))


if __name__=='__main__':
    unittest.main()
