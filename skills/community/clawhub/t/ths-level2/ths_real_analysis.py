# -*- coding: utf-8 -*-
"""
同花顺本地数据深度分析
从SQLite数据库和本地配置文件获取数据
"""
import sqlite3
import struct
import statistics
from pathlib import Path
from datetime import datetime

THS_PATH = Path(r"D:\同花顺远航版")

# 股票列表
STOCKS = [
    {'code': '600276', 'name': '恒瑞医药', 'market': 'USHA'},
    {'code': '688235', 'name': '百济神州', 'market': 'USHA'},
    {'code': '600760', 'name': '中航沈飞', 'market': 'USHA'},
    {'code': '601888', 'name': '中国中免', 'market': 'USHA'},
    {'code': '002202', 'name': '金风科技', 'market': 'USZA'},
]

def get_stock_info(code):
    """从SQLite获取股票信息"""
    db_path = THS_PATH / "bin" / "stockname" / "stocknameV2.db"
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    cursor.execute("SELECT CODE, NAME, MARKET FROM tablestock WHERE CODE = ?", (code,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {'code': row[0], 'name': row[1], 'market': row[2]}
    return None

def read_day_data(code, market):
    """读取通达信本地日线数据（同花顺也使用类似格式）"""
    if market in ['USHA', 'USHI']:
        path = r"D:\new_tdx\vipdoc\sh\lday"
        filename = f"sh{code}.day"
    else:
        path = r"D:\new_tdx\vipdoc\sz\lday"
        filename = f"sz{code}.day"
    
    filepath = Path(path) / filename
    records = []
    
    if filepath.exists():
        with open(filepath, 'rb') as f:
            while True:
                data = f.read(32)
                if len(data) < 32:
                    break
                date_int = struct.unpack('<I', data[0:4])[0]
                o = struct.unpack('<I', data[4:8])[0] / 100.0
                h = struct.unpack('<I', data[8:12])[0] / 100.0
                l = struct.unpack('<I', data[12:16])[0] / 100.0
                c = struct.unpack('<I', data[16:20])[0] / 100.0
                amt = struct.unpack('<f', data[20:24])[0]
                vol = struct.unpack('<I', data[24:28])[0]
                
                year = date_int // 10000
                month = (date_int % 10000) // 100
                day = date_int % 100
                
                records.append({
                    'date': f"{year}-{month:02d}-{day:02d}",
                    'date_int': date_int,
                    'open': o, 'high': h, 'low': l, 'close': c,
                    'volume': vol, 'amount': amt
                })
    
    return records

def analyze(df):
    """综合分析"""
    if not df or len(df) < 20:
        return None
    
    closes = [r['close'] for r in df]
    volumes = [r['volume'] for r in df]
    current = closes[-1]
    
    # 基础数据
    latest = df[-1]
    prev = df[-2] if len(df) > 1 else df[-1]
    change_pct = (current - prev['close']) / prev['close'] * 100
    
    # 筹码分析
    std = statistics.stdev(closes[-20:])
    mean = statistics.mean(closes[-20:])
    concentration = 1 - (std / mean) if mean > 0 else 0
    profitable = len([c for c in closes[-60:] if c < current]) / len(closes[-60:]) * 100
    
    if current < mean * 0.9:
        chip_state = '深度套牢'
    elif current < mean:
        chip_state = '多数套牢'
    elif current > mean * 1.1:
        chip_state = '多数获利'
    else:
        chip_state = '成本区震荡'
    
    # 资金抄底
    avg = statistics.mean(closes[-20:])
    deviation = (current - avg) / avg * 100
    vol5 = statistics.mean(volumes[-5:])
    vol20 = statistics.mean(volumes[-20:])
    vol_ratio = vol5 / vol20 if vol20 > 0 else 1
    
    if deviation < -10 and vol_ratio > 1.2:
        bottom_sig, bottom_str = '抄底信号', min(100, abs(deviation)*5)
    elif deviation < -5:
        bottom_sig, bottom_str = '偏弱', 30
    elif deviation > 10 and vol_ratio < 0.8:
        bottom_sig, bottom_str = '见顶信号', min(100, deviation*3)
    elif deviation > 5:
        bottom_sig, bottom_str = '偏强', 60
    else:
        bottom_sig, bottom_str = '中性', 50
    
    # 五线谱
    ma5 = statistics.mean(closes[-5:])
    ma10 = statistics.mean(closes[-10:])
    ma20 = statistics.mean(closes[-20:])
    
    up_vol = sum(volumes[i] for i in range(-20, 0) if closes[i] > closes[i-1])
    down_vol = sum(volumes[i] for i in range(-20, 0) if closes[i] < closes[i-1])
    money_ratio = up_vol / down_vol if down_vol > 0 else 1
    
    five_score = 50
    if ma5 > ma10 > ma20:
        five_score += 20
    elif ma5 < ma10 < ma20:
        five_score -= 20
    if current > ma5:
        five_score += 5
    if vol_ratio > 1.2:
        five_score += 10
    elif vol_ratio < 0.8:
        five_score -= 5
    if money_ratio > 1.2:
        five_score += 15
    elif money_ratio < 0.8:
        five_score -= 15
    five_score = max(0, min(100, five_score))
    
    five_sig = '强势' if five_score >= 70 else '偏强' if five_score >= 55 else '中性' if five_score >= 45 else '偏弱' if five_score >= 30 else '弱势'
    
    # 大单净量
    net_ratio = (up_vol - down_vol) / (up_vol + down_vol) if (up_vol + down_vol) > 0 else 0
    if net_ratio > 0.3:
        big_sig = '大单净流入'
    elif net_ratio < -0.3:
        big_sig = '大单净流出'
    else:
        big_sig = '大单平衡'
    
    # 成交量
    if vol_ratio > 1.5:
        vol_trend = '明显放量'
    elif vol_ratio > 1.2:
        vol_trend = '温和放量'
    elif vol_ratio < 0.7:
        vol_trend = '明显缩量'
    elif vol_ratio < 0.85:
        vol_trend = '温和缩量'
    else:
        vol_trend = '正常'
    
    # 综合评分
    total = 0
    if profitable > 50:
        total += 20
    total += bottom_str * 0.3
    total += five_score * 0.3
    if net_ratio > 0:
        total += 10
    
    sug = '积极关注' if total >= 70 else '适度关注' if total >= 55 else '观望' if total >= 40 else '回避'
    
    return {
        'latest': latest,
        'change_pct': round(change_pct, 2),
        'chips': {
            'concentration': round(concentration, 4),
            'profitable_ratio': round(profitable, 1),
            'avg_cost': round(mean, 2),
            'state': chip_state
        },
        'bottom': {
            'signal': bottom_sig,
            'strength': round(bottom_str, 1),
            'deviation': round(deviation, 2),
            'vol_ratio': round(vol_ratio, 2)
        },
        'five': {
            'score': round(five_score, 1),
            'signal': five_sig,
            'ma5': round(ma5, 2),
            'ma10': round(ma10, 2),
            'ma20': round(ma20, 2),
            'money_ratio': round(money_ratio, 2),
            'money_trend': '流入' if money_ratio > 1.2 else '流出' if money_ratio < 0.8 else '平衡'
        },
        'big': {
            'signal': big_sig,
            'net_ratio': round(net_ratio, 3),
            'up_vol': round(up_vol/10000, 1),
            'down_vol': round(down_vol/10000, 1)
        },
        'volume': {
            'vol_ma5': round(vol5/10000, 1),
            'vol_ma20': round(vol20/10000, 1),
            'ratio': round(vol_ratio, 2),
            'trend': vol_trend
        },
        'total': round(total, 1),
        'suggestion': sug
    }

def main():
    print("="*70)
    print(" 同花顺Level2 - 5只股票深度分析")
    print(f" 时间:{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("="*70)
    
    results = []
    
    for stock in STOCKS:
        print(f"\n{'='*70}")
        print(f" {stock['name']} ({stock['code']})")
        print(f"{'='*70}")
        
        # 获取股票信息
        info = get_stock_info(stock['code'])
        
        # 读取数据
        df = read_day_data(stock['code'], stock['market'])
        
        if not df or len(df) < 20:
            print("  数据不足")
            continue
        
        print(f"\n【基础数据】")
        print(f"  最新:{df[-1]['close']:.2f}元  日期:{df[-1]['date']}")
        print(f"  数据范围:{df[0]['date']} ~ {df[-1]['date']} ({len(df)}条)")
        
        # 分析
        r = analyze(df)
        if r:
            print(f"\n【筹码】集中度{r['chips']['concentration']:.1%}  获利盘{r['chips']['profitable_ratio']:.1f}%  {r['chips']['state']}")
            print(f"【抄底】{r['bottom']['signal']} ({r['bottom']['strength']}%)  偏离{r['bottom']['deviation']:.1f}%  量比{r['bottom']['vol_ratio']:.2f}")
            print(f"【五线】{r['five']['score']}/100 - {r['five']['signal']}")
            print(f"      MA5:{r['five']['ma5']}  MA10:{r['five']['ma10']}  MA20:{r['five']['ma20']}")
            print(f"      资金:{r['five']['money_trend']} (比{r['five']['money_ratio']:.2f})")
            print(f"【大单】{r['big']['signal']} (净量{r['big']['net_ratio']:.3f})")
            print(f"【成交】{r['volume']['vol_ma5']}万手  {r['volume']['trend']}")
            print(f"\n{'='*70}")
            print(f" 综合:{r['total']:.0f}分 - {r['suggestion']}")
            print(f"{'='*70}")
            
            r['code'] = stock['code']
            r['name'] = stock['name']
            results.append(r)
    
    # 汇总
    print(f"\n{'='*70}")
    print(" 综合对比")
    print(f"{'='*70}")
    print(f"{'股票':<8}{'价格':>8}{'五线':>8}{'抄底':>10}{'大单':>10}{'综合':>6}{'建议':>8}")
    print("-"*70)
    for r in sorted(results, key=lambda x:x['total'], reverse=True):
        print(f"{r['name']:<8}{r['latest']['close']:>8.2f}{r['five']['score']:>8.0f}{r['bottom']['signal']:>10}{r['big']['signal']:>10}{r['total']:>6.0f}{r['suggestion']:>8}")
    
    print(f"\n{'='*70}")
    print(" 操作策略")
    print(f"{'='*70}")
    for r in sorted(results, key=lambda x:x['total'], reverse=True):
        if r['total'] >= 55:
            print(f"✅ {r['name']}: {r['suggestion']}")
        elif r['total'] >= 40:
            print(f"⏳ {r['name']}: {r['suggestion']}")
        else:
            print(f"❌ {r['name']}: {r['suggestion']}")

if __name__ == '__main__':
    main()
