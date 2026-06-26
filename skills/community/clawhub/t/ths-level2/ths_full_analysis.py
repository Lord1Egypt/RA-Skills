# -*- coding: utf-8 -*-
"""
同花顺Level2 - 5只股票深度分析
筹码、资金抄底、五线谱、大单净量、成交量
"""
import os
import sys
import json
import statistics
import io
from datetime import datetime, timedelta
from pathlib import Path

# 设置UTF-8编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import tushare as ts

# 尝试从配置文件读取token
config_path = Path(__file__).parent / 'config.json'
token = os.environ.get('TUSHARE_TOKEN', '')

if not token and config_path.exists():
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
            token = config.get('tushare_token', '')
    except: pass

if token:
    try:
        ts.set_token(token)
        pro = ts.pro_api()
        print(f"✓ Tushare已连接")
    except Exception as e:
        print(f"✗ Tushare连接失败: {e}")
        pro = None
else:
    print("⚠ 未设置TUSHARE_TOKEN，请在config.json中配置")
    print("  或在环境变量中设置: setx TUSHARE_TOKEN your_token")
    pro = None

STOCKS = [
    {'code': '600276.SH', 'name': '恒瑞医药'},
    {'code': '688235.SH', 'name': '百济神州'},
    {'code': '600760.SH', 'name': '中航沈飞'},
    {'code': '601888.SH', 'name': '中国中免'},
    {'code': '002202.SZ', 'name': '金风科技'},
]

def get_data(code, days=60):
    """获取数据"""
    if pro is None:
        return None
    end = datetime.now().strftime('%Y%m%d')
    start = (datetime.now() - timedelta(days=days)).strftime('%Y%m%d')
    try:
        df = pro.daily(ts_code=code, start_date=start, end_date=end)
        if df is not None and len(df) > 0:
            return df.sort_values('trade_date').reset_index(drop=True)
    except: pass
    return None

def analyze_chips(df):
    """筹码分析"""
    if df is None or len(df) < 20: return {'status': '数据不足'}
    closes = df['close'].tolist()
    std = statistics.stdev(closes[-20:])
    mean = statistics.mean(closes[-20:])
    concentration = 1 - (std / mean) if mean > 0 else 0
    current = closes[-1]
    profitable = len([c for c in closes[-60:] if c < current]) / len(closes[-60:]) * 100
    if current < mean * 0.9: state = '深度套牢'
    elif current < mean: state = '多数套牢'
    elif current > mean * 1.1: state = '多数获利'
    else: state = '成本区震荡'
    return {'concentration': round(concentration, 4), 'profitable_ratio': round(profitable, 1), 'avg_cost': round(mean, 2), 'state': state}

def analyze_bottom(df):
    """资金抄底"""
    if df is None or len(df) < 20: return {'signal': '数据不足'}
    closes = df['close'].tolist()
    volumes = df['vol'].tolist()
    avg = statistics.mean(closes[-20:])
    current = closes[-1]
    dev = (current - avg) / avg * 100
    vol5 = statistics.mean(volumes[-5:])
    vol20 = statistics.mean(volumes[-20:])
    ratio = vol5 / vol20 if vol20 > 0 else 1
    if dev < -10 and ratio > 1.2: sig, str = '抄底信号', min(100, abs(dev)*5)
    elif dev < -5: sig, str = '偏弱', 30
    elif dev > 10 and ratio < 0.8: sig, str = '见顶信号', min(100, dev*3)
    elif dev > 5: sig, str = '偏强', 60
    else: sig, str = '中性', 50
    return {'signal': sig, 'strength': round(str, 1), 'deviation': round(dev, 2), 'vol_ratio': round(ratio, 2)}

def analyze_five(df):
    """五线谱"""
    if df is None or len(df) < 60: return {'score': 0, 'signal': '数据不足'}
    closes = df['close'].tolist()
    volumes = df['vol'].tolist()
    cur = closes[-1]
    ma5, ma10, ma20 = statistics.mean(closes[-5:]), statistics.mean(closes[-10:]), statistics.mean(closes[-20:])
    vol5, vol20 = statistics.mean(volumes[-5:]), statistics.mean(volumes[-20:])
    vol_r = vol5/vol20 if vol20>0 else 1
    vol_t = '放量' if vol_r>1.2 else '缩量' if vol_r<0.8 else '正常'
    up = sum(volumes[i] for i in range(-20,0) if closes[i]>closes[i-1])
    down = sum(volumes[i] for i in range(-20,0) if closes[i]<closes[i-1])
    money_r = up/down if down>0 else 1
    money_t = '流入' if money_r>1.2 else '流出' if money_r<0.8 else '平衡'
    score = 50
    if ma5>ma10>ma20: score+=20
    elif ma5<ma10<ma20: score-=20
    if cur>ma5: score+=5
    if vol_r>1.2: score+=10
    elif vol_r<0.8: score-=5
    if money_r>1.2: score+=15
    elif money_r<0.8: score-=15
    score = max(0, min(100, score))
    sig = '强势' if score>=70 else '偏强' if score>=55 else '中性' if score>=45 else '偏弱' if score>=30 else '弱势'
    return {'score': round(score,1), 'signal': sig, 'ma5': round(ma5,2), 'ma10': round(ma10,2), 'ma20': round(ma20,2), 'vol_ratio': round(vol_r,2), 'vol_trend': vol_t, 'money_ratio': round(money_r,2), 'money_trend': money_t}

def analyze_big(df):
    """大单净量"""
    if df is None or len(df)<20: return {'status': '数据不足'}
    volumes = df['vol'].tolist()
    closes = df['close'].tolist()
    up = sum(volumes[i] for i in range(-20,0) if closes[i]>closes[i-1])
    down = sum(volumes[i] for i in range(-20,0) if closes[i]<closes[i-1])
    net = (up-down)/(up+down) if (up+down)>0 else 0
    sig = '大单净流入' if net>0.3 else '大单净流出' if net<-0.3 else '大单平衡'
    return {'net_ratio': round(net,3), 'signal': sig, 'up_vol': round(up/10000,1), 'down_vol': round(down/10000,1)}

def analyze_vol(df):
    """成交量"""
    if df is None or len(df)<20: return {'status': '数据不足'}
    volumes = df['vol'].tolist()
    v5, v20 = statistics.mean(volumes[-5:]), statistics.mean(volumes[-20:])
    r = v5/v20 if v20>0 else 1
    t = '明显放量' if r>1.5 else '温和放量' if r>1.2 else '明显缩量' if r<0.7 else '温和缩量' if r<0.85 else '正常'
    return {'vol_ma5': round(v5/10000,1), 'vol_ma20': round(v20/10000,1), 'ratio': round(r,2), 'trend': t}

def analyze(code, name):
    """完整分析"""
    print(f"\n{'='*60}")
    print(f" {name} ({code})")
    print(f"{'='*60}")
    df = get_data(code)
    if df is None or len(df)==0:
        print("  无法获取数据")
        return None
    latest = df.iloc[-1]
    print(f"\n【基础】{latest['close']:.2f}元  {latest['pct_chg']:+.2f}%  {latest['trade_date']}")
    chips = analyze_chips(df)
    bottom = analyze_bottom(df)
    five = analyze_five(df)
    big = analyze_big(df)
    vol = analyze_vol(df)
    
    print(f"\n【筹码】集中度{chips.get('concentration',0):.1%}  获利盘{chips.get('profitable_ratio',0):.1f}%  {chips.get('state','-')}")
    print(f"【抄底】{bottom.get('signal','-')} ({bottom.get('strength',0)}%)  偏离{bottom.get('deviation',0):.1f}%  量比{bottom.get('vol_ratio',0):.2f}")
    print(f"【五线】评分{five.get('score',0)}/100 - {five.get('signal','-')}")
    print(f"      MA5:{five.get('ma5',0)}  MA10:{five.get('ma10',0)}  MA20:{five.get('ma20',0)}")
    print(f"      量能:{five.get('vol_trend','-')}  资金:{five.get('money_trend','-')}")
    print(f"【大单】{big.get('signal','-')} (净量{big.get('net_ratio',0):.3f})")
    print(f"【成交】{vol.get('vol_ma5',0)}万手  趋势:{vol.get('trend','-')}")
    
    score = 0
    if chips.get('profitable_ratio',0)>50: score+=20
    score += bottom.get('strength',0)*0.3
    score += five.get('score',0)*0.3
    if big.get('net_ratio',0)>0: score+=10
    sug = '积极关注' if score>=70 else '适度关注' if score>=55 else '观望' if score>=40 else '回避'
    print(f"\n{'='*60}")
    print(f" 综合:{score:.0f}分 - {sug}")
    print(f"{'='*60}")
    return {'code':code,'name':name,'price':latest['close'],'change':latest['pct_chg'],'chips':chips,'bottom':bottom,'five':five,'big':big,'vol':vol,'score':score,'sug':sug}

def main():
    print("="*60)
    print(" 同花顺Level2 - 5只股票深度分析")
    print(f" 时间:{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("="*60)
    results = []
    for s in STOCKS:
        try:
            r = analyze(s['code'], s['name'])
            if r: results.append(r)
        except Exception as e:
            print(f"\n{s['name']}分析失败:{e}")
    
    print(f"\n{'='*60}")
    print(" 汇总")
    print(f"{'='*60}")
    print(f"{'股票':<8}{'价格':>8}{'涨跌':>8}{'五线':>8}{'抄底':>10}{'大单':>10}{'综合':>6}{'建议':>8}")
    print("-"*60)
    for r in sorted(results, key=lambda x:x['score'], reverse=True):
        print(f"{r['name']:<8}{r['price']:>8.2f}{r['change']:>+8.1f}%{r['five'].get('score',0):>8.0f}{r['bottom'].get('signal','-'):>10}{r['big'].get('signal','-'):>10}{r['score']:>6.0f}{r['sug']:>8}")
    
    with open(Path(__file__).parent/'ths_analysis.json','w',encoding='utf-8') as f:
        json.dump(results,f,ensure_ascii=False,indent=2,default=str)
    print(f"\n已保存:ths_analysis.json")

if __name__=='__main__':
    main()
