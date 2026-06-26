import json
from datetime import datetime
def add_months(date_str, months):
    from datetime import datetime
    d = datetime.strptime(date_str, '%Y-%m-%d')
    month = d.month - 1 + months
    year = d.year + month // 12
    month = month % 12 + 1
    day = min(d.day, [31,
        29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28,
        31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month-1])
    return datetime(year, month, day).strftime('%Y-%m-%d')

def gen_milestones(u):
    ms = []
    # DP
    ms.append({
        'idx': 0,
        'label': f"DP ({u['first_pct']}%)",
        'month': 0,
        'pct': u['first_pct'],
        'date': u['signing_date'],
        'cost': round(u['price'] * u['first_pct'] / 100) + u.get('fees', 0)
    })
    
    for i in range(1, u['milestone_count']):
        mo = i * u['months_between']
        d_str = add_months(u['signing_date'], mo)
        ms.append({
            'idx': i,
            'label': f"Installment {i}",
            'month': mo,
            'pct': u['inst_pct'],
            'date': d_str,
            'cost': round(u['price'] * u['inst_pct'] / 100)
        })
    return ms

def simulate(config):
    accounts = config['accounts']
    units = config['units']
    cash_pool = sum(e.get('amount', 0) for e in config.get('my_cash', {}).get('entries', []))
    
    monthly_total = sum(a.get('monthly', 0) for a in accounts)
    total_upfront = sum(a.get('upfront', 0) for a in accounts)
    
    unit_data = []
    for u in units:
        u_copy = u.copy()
        u_copy['milestones'] = gen_milestones(u)
        unit_data.append(u_copy)
        
    max_month = max((m['month'] for u in unit_data for m in u['milestones']), default=0)
    
    available = cash_pool + total_upfront
    
    # ms_fund[unit_id][ms_idx] = {total: 0, pa: {acc_id: 0}}
    ms_fund = {}
    for u in unit_data:
        ms_fund[u['id']] = {}
        for ms in u['milestones']:
            ms_fund[u['id']][ms['idx']] = {'total': 0, 'pa': {a['id']: 0 for a in accounts}}
            
    ms_ptr = {u['id']: 0 for u in unit_data}
    
    for mo in range(max_month + 1):
        if mo > 0:
            available += monthly_total
            
        needs = []
        for u in unit_data:
            while ms_ptr[u['id']] < len(u['milestones']):
                ms = u['milestones'][ms_ptr[u['id']]]
                if ms_fund[u['id']][ms['idx']]['total'] >= ms['cost']:
                    ms_ptr[u['id']] += 1
                    continue
                if ms['month'] <= mo:
                    rem = ms['cost'] - ms_fund[u['id']][ms['idx']]['total']
                    needs.append({'uid': u['id'], 'ms': ms, 'need': rem})
                break
                
        if not needs or available <= 0:
            continue
            
        total_need = sum(n['need'] for n in needs)
        
        for n in needs:
            share = min(n['need'], int(available * n['need'] / total_need))
            if share <= 0: continue
            
            # Allocation rates
            rates = []
            for a in accounts:
                rate = a.get('upfront', 0) if mo == 0 else a.get('monthly', 0)
                if mo == 0 and a['id'] == 'inv1': # Admin share of cash pool
                    rate += cash_pool
                rates.append({'id': a['id'], 'rate': rate})
            
            rate_total = sum(r['rate'] for r in rates)
            rem_share = share
            
            for r in rates:
                amt = int(share * r['rate'] / rate_total) if rate_total > 0 else 0
                actual = min(amt, rem_share)
                ms_fund[n['uid']][n['ms']['idx']]['total'] += actual
                ms_fund[n['uid']][n['ms']['idx']]['pa'][r['id']] += actual
                rem_share -= actual
                
            # Remainder to admin (inv1)
            if rem_share > 0:
                ms_fund[n['uid']][n['ms']['idx']]['total'] += rem_share
                ms_fund[n['uid']][n['ms']['idx']]['pa']['inv1'] += rem_share
                
            available -= (share - rem_share)
            
    # Format output for JSON
    results = []
    for u in unit_data:
        res = {
            'id': u['id'],
            'name': u['name'],
            'milestones': []
        }
        for ms in u['milestones']:
            ms_res = ms.copy()
            ms_res['funding'] = ms_fund[u['id']][ms['idx']]
            res['milestones'].append(ms_res)
        results.append(res)
        
    return results

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            cfg = json.load(f)
        print(json.dumps(simulate(cfg), indent=2))
