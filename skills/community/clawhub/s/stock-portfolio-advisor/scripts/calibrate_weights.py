"""Purged rolling train/validation/holdout weight calibration; activation is optional."""
import argparse
import itertools
import statistics
from datetime import date
from value_model import WEIGHTS
from weight_registry import read_json, write_json, read_registry, resolve, normalize, digest, activate, DEFAULT_PATH
from build_backtest_dataset import verify_dataset
from backtest import rank_ic, simulate, validate_strategy

DEFAULTS = dict(train_months=36, validation_months=24, test_months=24, max_folds=3, min_folds=2,
                min_cross_section=8, min_train_ic_months=18, min_validation_ic_months=6,
                min_test_ic_months=6, grid_step=5, grid_span=10, shortlist=5,
                alpha=.2, max_change_pct=3, min_weight=10, max_weight=70,
                min_ic_gain=.005, min_excess_gain=.005, max_drawdown_worsening=.02,
                min_win_fraction=.6, max_turnover_ratio=1.25)


def configuration(value):
    if value is not None and (not isinstance(value,dict) or set(value)-set(DEFAULTS)):
        raise ValueError('Unknown calibration configuration key')
    c = DEFAULTS | (value or {})
    for k in ('train_months','validation_months','test_months','max_folds','min_folds','min_cross_section',
              'min_train_ic_months','min_validation_ic_months','min_test_ic_months','grid_step','grid_span','shortlist'):
        if isinstance(c[k],bool) or not isinstance(c[k],int) or c[k]<=0:
            raise ValueError(f'{k} must be positive integer')
    if c['grid_span']>30 or c['grid_step']<2 or c['max_folds']<c['min_folds']:
        raise ValueError('Search too wide or insufficient configured folds')
    if not 0<c['alpha']<=1 or not 0<c['max_change_pct']<=10 or not 0<=c['min_weight']<c['max_weight']<=100:
        raise ValueError('Invalid weight smoothing/bounds')
    if not 0<c['min_win_fraction']<=1 or c['max_turnover_ratio']<1:
        raise ValueError('Invalid validation gate')
    if min(c[k] for k in ('min_ic_gain','min_excess_gain','max_drawdown_worsening'))<0:
        raise ValueError('Gate thresholds must be nonnegative')
    return c


def candidates(base,c):
    seen = set()
    for dq,dg in itertools.product(range(-c['grid_span'],c['grid_span']+1,c['grid_step']),repeat=2):
        dv = -dq-dg
        if abs(dv)>c['grid_span']: continue
        raw = {k:base[k]+d for k,d in zip('QGV',(dq,dg,dv))}
        if any(not c['min_weight']<=x<=c['max_weight'] for x in raw.values()): continue
        # Smooth BEFORE validation/test; never validate one vector and deploy another.
        delta = {k:c['alpha']*(raw[k]-base[k]) for k in 'QGV'}
        scale = min(1,c['max_change_pct']/max(max(abs(x) for x in delta.values()),1e-9))
        w = {k:round(base[k]+delta[k]*scale,6) for k in 'QGV'}
        w['V']=round(100-w['Q']-w['G'],6)
        key=tuple(w.values())
        if key not in seen:
            seen.add(key);yield w


def compact(report):
    return {k:v for k,v in report.items() if k not in ('daily','trades','blocked','note')}


def split_rows(rows,start,end,maturity):
    # Date-grouped panel. Purge EVERY label crossing the next partition boundary.
    return [r for r in rows if start<=r['date']<end and r.get('label') and r['label']['label_end']<maturity]


def calibrate(dataset,as_of,registry=None,config=None,strategy=None,profiles=None):
    verify_dataset(dataset);date.fromisoformat(as_of)
    registry=registry if registry is not None else read_registry()
    c=configuration(config);strategy=validate_strategy(strategy)
    if c['validation_months']<=dataset['label_months'] or c['test_months']<=dataset['label_months']:
        raise ValueError('Validation/test spans must exceed forward label horizon to leave mature observations')
    dates=sorted(d for d in dataset.get('decision_dates',sorted({r['date'] for r in dataset['rows']})) if d<=as_of)
    observed=[d for d in dataset['sessions'] if d<=as_of]
    if (not dates or not observed or (date.fromisoformat(as_of)-date.fromisoformat(dates[-1])).days>35
            or (date.fromisoformat(as_of)-date.fromisoformat(observed[-1])).days>7):
        raise ValueError('Latest monthly snapshot/market data is stale at as-of date')
    total=c['train_months']+c['validation_months']+c['test_months']
    windows=[]
    i=len(dates)-1
    while i>=total and len(windows)<c['max_folds']:
        windows.append((dates[i-total],dates[i-c['validation_months']-c['test_months']],dates[i-c['test_months']],dates[i]))
        i-=c['test_months']  # Non-overlapping outer test blocks.
    windows.reverse()
    allowed=profiles or list(WEIGHTS)
    if any(p not in WEIGHTS for p in allowed): raise ValueError('Unknown profile')
    report=dict(schema_version=1,synthetic=dataset['synthetic'],as_of=as_of,dataset_hash=dataset['dataset_hash'],
                registry_hash=digest(registry),config=c,strategy=strategy,profiles={},max_label_end=as_of,
                note='Holdout validates the frozen smoothed vector. No post-holdout refit. Tests overlap neither future labels nor each other; thresholds are engineering defaults, not a statistical significance claim.')
    consumed=[]
    for profile in allowed:
        base,base_version,_=resolve(registry,profile,as_of,WEIGHTS[profile])
        entry=dict(accepted=False,incumbent_weights=base,incumbent_version=base_version,proposed_weights=base,folds=[],reasons=[])
        report['profiles'][profile]=entry
        rows=[r for r in dataset['rows'] if r['profile']==profile and r['eligible']]
        # A previous fit may already have consumed older holdouts. Do not reuse those as independent evidence.
        prior_cutoff=max((r['training_cutoff'] for r in registry.get('releases',[]) if profile in r.get('weights',{}) and r.get('validation_passed') is True),default='0001-01-01')
        for train_start,val_start,test_start,test_end in windows:
            if test_start<=prior_cutoff: continue
            train=split_rows(rows,train_start,val_start,val_start)
            val=split_rows(rows,val_start,test_start,test_start)
            test=split_rows(rows,test_start,test_end,test_end)
            train_base=rank_ic(train,base,c['min_cross_section'])
            val_base_ic=rank_ic(val,base,c['min_cross_section'])
            test_base_ic=rank_ic(test,base,c['min_cross_section'])
            if (train_base['months']<c['min_train_ic_months'] or val_base_ic['months']<c['min_validation_ic_months'] or test_base_ic['months']<c['min_test_ic_months']):
                entry['reasons'].append(f'{test_start}: insufficient mature train/validation/test cross-sections')
                continue
            training=[]
            for w in candidates(base,c):
                ic=rank_ic(train,w,c['min_cross_section'])
                if ic['mean'] is not None:
                    regularizer=.002*sum(abs(w[k]-base[k]) for k in 'QGV')/100
                    training.append((ic['mean']-regularizer,w))
            training.sort(key=lambda pair:(-pair[0],tuple(pair[1].values())))
            shortlist=[w for _,w in training[:c['shortlist']]]
            if base not in shortlist:shortlist.append(base)
            validation=[]
            for w in shortlist:
                ic=rank_ic(val,w,c['min_cross_section'])
                sim=simulate(dataset,w,val_start,test_start,profile,strategy)
                objective=ic['mean']+.2*sim['excess_return']-.2*sim['max_drawdown']-.02*sim['annualized_turnover']
                validation.append((objective,w,ic['mean']))
            validation.sort(key=lambda x:(-x[0],sum(abs(x[1][k]-base[k]) for k in 'QGV')))
            _,chosen,val_ic=validation[0]
            baseline=simulate(dataset,base,test_start,test_end,profile,strategy)
            candidate=simulate(dataset,chosen,test_start,test_end,profile,strategy)
            stress_base=simulate(dataset,base,test_start,test_end,profile,strategy,cost_multiplier=2)
            stress_new=simulate(dataset,chosen,test_start,test_end,profile,strategy,cost_multiplier=2)
            test_ic=rank_ic(test,chosen,c['min_cross_section'])
            fold=dict(train_start=train_start,validation_start=val_start,test_start=test_start,test_end=test_end,
                      train_rows=len(train),validation_rows=len(val),test_rows=len(test),
                      train_ic_months=train_base['months'],validation_ic_months=val_base_ic['months'],test_ic_months=test_ic['months'],
                      searched_candidates=len(training),validation_shortlist=[dict(objective=o,weights=w,ic=ic) for o,w,ic in validation],
                      train_label_end=max(r['label']['label_end'] for r in train),
                      validation_label_end=max(r['label']['label_end'] for r in val),
                      test_label_end=max(r['label']['label_end'] for r in test),
                      proposed_weights=chosen,validation_ic=val_ic,baseline_ic=test_base_ic['mean'],candidate_ic=test_ic['mean'],
                      ic_gain=test_ic['mean']-test_base_ic['mean'],baseline=compact(baseline),candidate=compact(candidate),
                      excess_gain=candidate['excess_return']-baseline['excess_return'],
                      stress_excess_gain=stress_new['excess_return']-stress_base['excess_return'])
            entry['folds'].append(fold)
            consumed.extend(r['label']['label_end'] for r in train+val+test)
        folds=entry['folds']
        if len(folds)<c['min_folds']:
            entry['reasons'].append('Insufficient independent mature holdout folds; keep incumbent')
            continue
        last=folds[-1]
        entry['proposed_weights']=last['proposed_weights']
        gates=dict(
            ic_improved=statistics.mean(f['ic_gain'] for f in folds)>=c['min_ic_gain'],
            positive_test_ic=statistics.mean(f['candidate_ic'] for f in folds)>0,
            net_excess_improved=statistics.mean(f['excess_gain'] for f in folds)>=c['min_excess_gain'],
            consistent=sum(f['excess_gain']>0 for f in folds)/len(folds)>=c['min_win_fraction'],
            latest_passed=last['ic_gain']>0 and last['excess_gain']>0,
            cost_stress=all(f['stress_excess_gain']>=0 for f in folds),
            drawdown=all(f['candidate']['max_drawdown']<=f['baseline']['max_drawdown']+c['max_drawdown_worsening'] for f in folds),
            turnover=all(f['candidate']['annualized_turnover']<=max(.05,f['baseline']['annualized_turnover']*c['max_turnover_ratio']) for f in folds),
            changed=any(abs(last['proposed_weights'][k]-base[k])>1e-6 for k in 'QGV'))
        entry['gates']=gates
        entry['accepted']=all(gates.values())
        entry['reasons'].extend(k for k,v in gates.items() if not v)
    if consumed:report['max_label_end']=max(consumed)
    report['calibration_id']=digest(report)
    return report


def write_summary(path,report,activation=None):
    lines=['# 历史回测与调权检查', '',
           '**合成测试数据，不可启用正式权重。**' if report['synthetic'] else '真实输入声明：仍需核查原始数据与历史假设来源。', '',
           f"检查截止日：{report['as_of']}；数据指纹：`{report['dataset_hash'][:16]}`。", '',
           '留出期只检查已冻结的候选权重，不在检验后重新拟合。未达门槛保留原权重。', '',
           '| 行业档位 | 结果 | 原Q/G/V | 候选Q/G/V | 有效留出窗口 |', '| --- | --- | --- | --- | --- |']
    for profile,p in report['profiles'].items():
        old='/'.join(f'{p["incumbent_weights"][k]:.2f}' for k in 'QGV')
        new='/'.join(f'{p["proposed_weights"][k]:.2f}' for k in 'QGV')
        lines.append(f'| {profile} | {"通过检验" if p["accepted"] else "保留原权重"} | {old} | {new} | {len(p["folds"])} |')
    for profile,p in report['profiles'].items():
        lines.extend(['',f'## {profile}', '', '检查未通过/样本不足原因：'+('；'.join(p['reasons']) or '无'), '',
                      '| 留出区间 | Rank IC改善 | 扣费超额收益改善 | 候选最大回撤 | 双倍成本改善 |',
                      '| --- | --- | --- | --- | --- |'])
        for f in p['folds']:
            lines.append(f"| {f['test_start']} ~ {f['test_end']} | {f['ic_gain']:.4f} | {f['excess_gain']*100:.2f}百分点 | {f['candidate']['max_drawdown']*100:.2f}% | {f['stress_excess_gain']*100:.2f}百分点 |")
    lines.extend(['', '程序执行状态：'+str(activation or {'status':'review_only'}), '',
                  '这些门槛为工程默认值，不构成统计显著性证明，也不保证未来收益。完整参数、样本数、日期边界和逐窗口结果见同名JSON。'])
    from pathlib import Path
    Path(path).write_text('\n'.join(lines)+'\n',encoding='utf-8')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--dataset',required=True);p.add_argument('--as-of',required=True);p.add_argument('--output',required=True)
    p.add_argument('--config');p.add_argument('--strategy');p.add_argument('--profiles',help='Comma-separated profiles; default all')
    p.add_argument('--weights-file',default=str(DEFAULT_PATH));p.add_argument('--apply',action='store_true',help='Activate only accepted real-data results')
    a=p.parse_args()
    try:
        ds=read_json(a.dataset);registry=read_registry(a.weights_file)
        report=calibrate(ds,a.as_of,registry,read_json(a.config) if a.config else None,
                         read_json(a.strategy) if a.strategy else None,a.profiles.split(',') if a.profiles else None)
        # Always persist audit, even if activation is refused for synthetic data.
        write_json(a.output,report)
        if a.apply:
            status=activate(report,a.weights_file)
        else:status={'status':'review_only'}
        from pathlib import Path
        write_summary(Path(a.output).with_suffix('.md'),report,status)
        print('[OK] '+str(status))
    except (ValueError,KeyError,TypeError,OSError) as exc:p.error(str(exc))


if __name__=='__main__':main()
