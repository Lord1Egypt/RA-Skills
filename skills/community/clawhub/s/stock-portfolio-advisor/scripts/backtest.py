"""Daily, long-only, next-open simulation. Cash dividends, splits, costs and blocked fills."""
import argparse
import bisect
import math
import statistics
from collections import defaultdict
from value_model import map_rating
from weight_registry import read_json, write_json, valid_weights
from build_backtest_dataset import verify_dataset

DEFAULT_STRATEGY = dict(top_k=10, initial_cash=1000000, equity_budget=.8, lot_size=100,
                        buy_fee_bps=3, sell_fee_bps=8, slippage_bps=5)


def validate_strategy(overrides):
    if overrides is not None and (not isinstance(overrides,dict) or set(overrides)-set(DEFAULT_STRATEGY)-{'fee_schedule'}):
        raise ValueError('Unknown backtest strategy configuration key')
    c = DEFAULT_STRATEGY | (overrides or {})
    for k in ('top_k', 'lot_size'):
        if isinstance(c[k], bool) or not isinstance(c[k], int) or c[k] < 1:
            raise ValueError(f'{k} must be a positive integer')
    if not 0 < c['equity_budget'] <= .95 or c['initial_cash'] <= 0:
        raise ValueError('Invalid equity budget / initial cash')
    for record in [c] + c.get('fee_schedule', []):
        for k in ('buy_fee_bps', 'sell_fee_bps', 'slippage_bps'):
            if not isinstance(record.get(k), (float, int)) or not math.isfinite(record[k]) or not 0 <= record[k] < 1000:
                raise ValueError('Costs must be finite, nonnegative basis points below 1000')
    if c.get('fee_schedule'):
        from datetime import date
        dates = [x['from'] for x in c['fee_schedule']]
        for d in dates: date.fromisoformat(d)
        if dates != sorted(set(dates)):
            raise ValueError('Fee schedule dates must be unique and sorted')
    return c


def rank(values):
    ordered = sorted(range(len(values)), key=values.__getitem__)
    result = [0.0] * len(values)
    i = 0
    while i < len(ordered):
        j = i + 1
        while j < len(ordered) and values[ordered[j]] == values[ordered[i]]:
            j += 1
        for k in ordered[i:j]: result[k] = (i+j-1)/2
        i = j
    return result


def correlation(a, b):
    a, b = rank(a), rank(b)
    am, bm = statistics.mean(a), statistics.mean(b)
    denominator = math.sqrt(sum((x-am)**2 for x in a)*sum((y-bm)**2 for y in b))
    return sum((x-am)*(y-bm) for x,y in zip(a,b))/denominator if denominator else None


def score(row, weights):
    return sum(row['dims'][k]*weights[k] for k in 'QGV')/100


def rank_ic(rows, weights, min_cross_section=8):
    groups = defaultdict(list)
    for r in rows:
        if r['eligible'] and r.get('label'): groups[r['date']].append(r)
    observations = []
    for d, group in sorted(groups.items()):
        if len(group) < min_cross_section: continue
        value = correlation([score(r,weights) for r in group], [r['label']['excess_return'] for r in group])
        if value is not None: observations.append({'date': d, 'ic': value, 'count': len(group)})
    return dict(mean=statistics.mean(x['ic'] for x in observations) if observations else None,
                months=len(observations), observations=observations)


def simulate(dataset, weights, start, end, profile=None, strategy=None, cost_multiplier=1):
    if not valid_weights(weights): raise ValueError('Weights must sum to 100')
    c = validate_strategy(strategy)
    sessions, bars, benchmark = dataset['sessions'], dataset['bars'], dataset['benchmark']
    if start not in benchmark or end not in benchmark or start >= end:
        raise ValueError('Backtest boundaries must be ordered trading sessions')
    selected_rows = [r for r in dataset['rows'] if start <= r['date'] < end and (profile is None or r['profile']==profile)]
    groups = defaultdict(list)
    for d in dataset.get('decision_dates',sorted({r['date'] for r in dataset['rows']})):
        if start <= d < end: groups[d]  # An empty universe still triggers liquidation.
    for r in selected_rows: groups[r['date']].append(r)
    execution = {}
    for d, group in groups.items():
        index = bisect.bisect_right(sessions, d)
        if index < len(sessions): execution[sessions[index]] = group
    cash, positions, classification = float(c['initial_cash']), {}, {}
    history, trades, blocked, total_cost = [], [], [], 0.0
    nav_previous = peak = cash
    max_dd = 0
    initial_benchmark = benchmark[start]['close_tr']
    for d in sessions[bisect.bisect_right(sessions,start):bisect.bisect_right(sessions,end)]:
        # Distribution is paid on pre-split shares before the day's open.
        for code in list(positions):
            b = bars.get(code,{}).get(d)
            if b is None: raise ValueError(f'Missing held-stock bar {code} {d}')
            cash += positions[code]*b['cash_dividend']
            positions[code] *= b['split_factor']
            if b['delisted']:
                cash += positions.pop(code)*b['close']
                trades.append(dict(date=d,code=code,side='terminal_settlement',price=b['close']))
        fees = c
        for schedule in c.get('fee_schedule',[]):
            if schedule['from'] <= d: fees = schedule
        slip = fees['slippage_bps']/10000*cost_multiplier
        buy_fee, sell_fee = (fees[k]/10000*cost_multiplier for k in ('buy_fee_bps','sell_fee_bps'))
        day_turnover = 0.0
        if d in execution:
            group = execution[d]
            # Universe membership and scores are known at signal close; execution flags are not used for ranking.
            eligible = sorted((r for r in group if r['eligible'] and score(r,weights)>=50),key=lambda r:(-score(r,weights),r['code']))[:c['top_k']]
            for r in group: classification[r['code']] = (r['industry'],r['exposure_group'])
            targets, used = {}, defaultdict(float)
            for r in eligible:
                cap = map_rating(score(r,weights))[2]/100
                limits = [c['equity_budget']/c['top_k'], cap]
                for i,g in enumerate(classification[r['code']]): limits.append(.30-used[(i,g)])
                w = max(0,min(limits))
                targets[r['code']] = w
                for i,g in enumerate(classification[r['code']]): used[(i,g)] += w
            def open_mark(code):
                b = bars.get(code,{}).get(d)
                if b is None: raise ValueError(f'Missing execution bar {code} {d}')
                return b['open'] if b['open']>0 else b['close']
            nav_open = cash + sum(q*open_mark(code) for code,q in positions.items())
            # Sell before buying. Blocked reductions stay held, with daily marked losses.
            for code in sorted(list(positions)):
                b, qty = bars[code][d], positions[code]
                desired = targets.get(code,0)*nav_open/open_mark(code)
                sell = qty if targets.get(code,0)==0 else min(qty, math.floor(max(0,qty-desired)/c['lot_size'])*c['lot_size'])
                if sell<=0: continue
                if not b['sell_allowed']:
                    blocked.append(dict(date=d,code=code,side='sell')); continue
                fill = b['open']*(1-slip)
                cash += sell*fill*(1-sell_fee)
                cost = sell*(b['open']-fill)+sell*fill*sell_fee
                total_cost += cost; day_turnover += sell*b['open']/nav_open
                positions[code] -= sell
                if positions[code]<1e-8: positions.pop(code)
                trades.append(dict(date=d,code=code,side='sell',shares=sell,price=fill,cost=cost))
            for code in targets:
                b = bars.get(code,{}).get(d)
                if b is None: raise ValueError(f'Missing execution bar {code} {d}')
                if b['delisted'] or not b['buy_allowed']:
                    blocked.append(dict(date=d,code=code,side='buy')); continue
                held_value = positions.get(code,0)*b['open']
                desired_value = max(0,targets[code]*nav_open-held_value)
                # Blocked holdings can consume group/equity capacity. Do not buy around them.
                equity_value = sum(q*open_mark(k) for k,q in positions.items())
                desired_value = min(desired_value,max(0,c['equity_budget']*nav_open-equity_value))
                for i,g in enumerate(classification[code]):
                    exposure = sum(q*open_mark(k) for k,q in positions.items() if classification[k][i]==g)
                    desired_value = min(desired_value,max(0,.30*nav_open-exposure))
                fill = b['open']*(1+slip)
                spendable = max(0,cash-(1-c['equity_budget'])*nav_open)
                qty = math.floor(min(desired_value/b['open'],spendable/(fill*(1+buy_fee)))/c['lot_size'])*c['lot_size']
                if qty<=0: continue
                cost = qty*(fill-b['open'])+qty*fill*buy_fee
                cash -= qty*fill*(1+buy_fee)
                positions[code] = positions.get(code,0)+qty
                total_cost += cost; day_turnover += qty*b['open']/nav_open
                trades.append(dict(date=d,code=code,side='buy',shares=qty,price=fill,cost=cost))
        nav = cash+sum(q*bars[code][d]['close'] for code,q in positions.items())
        if nav<0 or cash < -.001: raise ValueError('Simulation produced negative cash/NAV')
        peak=max(peak,nav); max_dd=max(max_dd,1-nav/peak)
        history.append(dict(date=d,nav=nav,daily_return=nav/nav_previous-1,turnover=day_turnover,
                            cash=cash,benchmark_nav=c['initial_cash']*benchmark[d]['close_tr']/initial_benchmark))
        nav_previous=nav
    if not history: raise ValueError('Empty backtest window')
    from datetime import date
    years=(date.fromisoformat(end)-date.fromisoformat(start)).days/365.25
    total=history[-1]['nav']/c['initial_cash']-1
    bench=benchmark[end]['close_tr']/initial_benchmark-1
    returns=[x['daily_return'] for x in history]
    vol=statistics.stdev(returns)*math.sqrt(252) if len(returns)>1 else 0
    return dict(start=start,end=end,total_return=total,benchmark_return=bench,excess_return=total-bench,
                annualized_return=(1+total)**(1/years)-1,max_drawdown=max_dd,annualized_vol=vol,
                annualized_turnover=sum(x['turnover'] for x in history)/years,total_cost=total_cost,
                blocked_orders=len(blocked),trades=trades,blocked=blocked,daily=history,
                note='Monthly rebalanced research strategy; 12-month labels measure ranking separately. No leverage/interest. Costs are supplied assumptions, not current statutory rates.')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--dataset',required=True);p.add_argument('--output',required=True)
    p.add_argument('--start',required=True);p.add_argument('--end',required=True)
    p.add_argument('--weights',default='40,30,30');p.add_argument('--profile')
    p.add_argument('--strategy',help='JSON simulation config')
    a=p.parse_args()
    try:
        ds=read_json(a.dataset);verify_dataset(ds)
        weights=dict(zip('QGV',map(float,a.weights.split(','))))
        report=simulate(ds,weights,a.start,a.end,a.profile,read_json(a.strategy) if a.strategy else None)
        report.update(synthetic=ds['synthetic'],dataset_hash=ds['dataset_hash'],weights=weights)
        write_json(a.output,report)
        print('[OK] Backtest written; synthetic='+str(ds['synthetic']))
    except (ValueError,KeyError,TypeError,OSError) as exc: p.error(str(exc))


if __name__=='__main__': main()
