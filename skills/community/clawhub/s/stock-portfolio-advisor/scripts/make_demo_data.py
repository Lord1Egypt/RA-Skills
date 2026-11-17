"""Generate labelled SYNTHETIC historical inputs. No network or real stock data."""
import argparse
import calendar
import csv
import math
from datetime import date, timedelta
from pathlib import Path
from weight_registry import write_json


def generate(folder, years=12, count=12):
    if years<2 or not 8<=count<=100:raise ValueError('Use years>=2 and 8..100 securities')
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    start=date(2010,1,1);stop=date(2010+years,1,1)
    sessions=[];d=start
    while d<stop:
        if d.weekday()<5:sessions.append(d)
        d+=timedelta(days=1)
    month_ends={}
    for d in sessions:month_ends[(d.year,d.month)]=d
    codes=[f'SYN{i:03}' for i in range(count)]
    prices={c:20+i for i,c in enumerate(codes)}
    snapshots=[];benchmark=1000
    with (folder/'bars.csv').open('w',newline='',encoding='utf-8') as bf,(folder/'benchmark.csv').open('w',newline='',encoding='utf-8') as mf:
        bars=csv.DictWriter(bf,fieldnames=['date','code','open','close','split_factor','cash_dividend','buy_allowed','sell_allowed','delisted'])
        bmk=csv.DictWriter(mf,fieldnames=['date','open_tr','close_tr']);bars.writeheader();bmk.writeheader()
        for d in sessions:
            month=(d.year-2010)*12+d.month-1
            op=benchmark;benchmark*=1+.00015
            bmk.writerow(dict(date=d.isoformat(),open_tr=op,close_tr=benchmark))
            for i,code in enumerate(codes):
                signal=math.sin((month-1)/8+i*.9)
                op=prices[code];prices[code]*=1+.00015+.00065*signal
                bars.writerow(dict(date=d.isoformat(),code=code,open=op,close=prices[code],split_factor=1,cash_dividend=0,
                                   buy_allowed='true',sell_allowed='true',delisted='false'))
            if d != month_ends[(d.year,d.month)]:continue
            stocks=[]
            for i,code in enumerate(codes):
                signal=math.sin(month/8+i*.9);noise=math.sin(month*.51+i*2.2)
                indicators=dict(roe_ttm=13+5*noise,gross_margin=35+10*noise,net_margin=15+4*noise,debt_ratio=40,
                                net_profit_ttm=100,operating_cashflow_ttm=120,prior_net_profit=90,np_cv_3y=.2,
                                rev_yoy=17+15*signal,np_yoy=20+25*signal,qoq_trend='improving' if signal>0 else 'flat',
                                forecast='inline',industry_boom=50+40*signal,pe_pct=50-25*noise,rel_industry_discount=-10*noise)
                meta={k:dict(source='SYNTHETIC: no actual financial statements',as_of=d.isoformat(),published_at=d.isoformat(),
                             period_end=d.isoformat(),unit='see schema') for k in indicators}
                meta['np_cv_3y'].update(positive_mean=True,annual_samples=3)
                meta['pe_pct'].update(basis='point_in_time',history_months=60)
                meta['rel_industry_discount']['multiple']='PE'
                fair=prices[code]*(1.15+.15*noise)
                stocks.append(dict(code=code,name='合成证券'+str(i),profile='default',industry='合成行业'+str(i%4),
                                   exposure_group='合成链'+str(i%3),holding=False,price=prices[code],price_meta=meta['pe_pct'],
                                   indicators=indicators,indicator_meta=meta,
                                   risk=dict(status='checked',events=[],source='synthetic',as_of=d.isoformat()),
                                   valuation=dict(method='normalized_pe',source='synthetic',sources=['synthetic only'],as_of=d.isoformat(),
                                                  horizon='current_fair_value',assumptions={'normalization':'合成数据，禁止用于投资结论'},
                                                  scenarios={k:dict(eps_normalized=fair*factor/10,fair_pe=10) for k,factor in [('bear',.8),('base',1),('bull',1.2)]})))
            relative=f'snapshots/{d.isoformat()}.json';snapshots.append(relative)
            write_json(folder/relative,dict(date=d.isoformat(),synthetic=True,stocks=stocks))
    manifest=dict(synthetic=True,point_in_time=True,includes_delisted=True,historical_assumptions_verified=True,
                  source='Synthetic deterministic generator, not real market data',universe_description='Synthetic fixed universe; no delistings occur in this fixture',
                  label_months=12,bars_csv='bars.csv',benchmark_csv='benchmark.csv',snapshots=snapshots)
    write_json(folder/'manifest.json',manifest)
    return folder/'manifest.json'


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output-dir',required=True)
    p.add_argument('--years',type=int,default=12);p.add_argument('--count',type=int,default=12)
    a=p.parse_args();print('[OK] SYNTHETIC manifest: '+str(generate(a.output_dir,a.years,a.count)))


if __name__=='__main__':main()
