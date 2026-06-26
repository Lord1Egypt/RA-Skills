# -*- coding: utf-8 -*-
"""
获取5只股票的详细数据分析
"""
import os
import sys
import json
from datetime import datetime, timedelta

# 设置环境
os.environ['PYTHONIOENCODING'] = 'utf-8'

try:
    import tushare as ts
    import pandas as pd
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 200)
except ImportError:
    print("请安装: pip install tushare pandas")
    sys.exit(1)

# 获取token
TUSHARE_TOKEN = os.environ.get('TUSHARE_TOKEN', '')
if not TUSHARE_TOKEN:
    print("错误: 请设置 TUSHARE_TOKEN 环境变量")
    sys.exit(1)

# 初始化
ts.set_token(TUSHARE_TOKEN)
pro = ts.pro_api()

# 股票列表
STOCKS = [
    {'code': '600760.SH', 'name': '中航沈飞', 'industry': '航空军工'},
    {'code': '601888.SH', 'name': '中国中免', 'industry': '免税零售'},
    {'code': '600276.SH', 'name': '恒瑞医药', 'industry': '医药'},
    {'code': '002202.SZ', 'name': '金风科技', 'industry': '风电设备'},
    {'code': '688235.SH', 'name': '百济神州', 'industry': '生物医药'},
]

def get_daily_data(ts_code, start_date, end_date):
    """获取日线数据"""
    try:
        df = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
        return df.sort_values('trade_date') if df is not None and len(df) > 0 else None
    except Exception as e:
        print(f"获取日线数据失败: {e}")
        return None

def get_moneyflow(ts_code, start_date, end_date):
    """获取资金流向"""
    try:
        df = pro.moneyflow(ts_code=ts_code, start_date=start_date, end_date=end_date)
        return df.sort_values('trade_date') if df is not None and len(df) > 0 else None
    except Exception as e:
        return None

def get_daily_basic(ts_code, start_date, end_date):
    """获取每日基本面指标"""
    try:
        df = pro.daily_basic(ts_code=ts_code, start_date=start_date, end_date=end_date)
        return df.sort_values('trade_date') if df is not None and len(df) > 0 else None
    except Exception as e:
        return None

def get_fina_indicator(ts_code):
    """获取财务指标"""
    try:
        df = pro.fina_indicator(ts_code=ts_code, start_date='20240101')
        return df.head(4) if df is not None and len(df) > 0 else None
    except Exception as e:
        return None

def analyze_stock(stock):
    """分析单只股票"""
    print(f"\n{'='*60}")
    print(f" {stock['name']} ({stock['code']}) - {stock['industry']}")
    print('='*60)
    
    # 日期范围
    end_date = datetime.now().strftime('%Y%m%d')
    start_date = (datetime.now() - timedelta(days=40)).strftime('%Y%m%d')
    
    result = {'stock': stock, 'data': {}}
    
    # 1. 日线数据
    print("\n[1] 近30天行情数据:")
    daily = get_daily_data(stock['code'], start_date, end_date)
    if daily is not None and len(daily) > 0:
        result['data']['daily'] = daily.to_dict('records')
        
        # 计算涨跌幅
        latest = daily.iloc[-1]
        first = daily.iloc[0]
        change_pct = ((latest['close'] - first['close']) / first['close']) * 100
        
        print(f"   最新价: {latest['close']:.2f}")
        print(f"   30天涨跌幅: {change_pct:.2f}%")
        print(f"   30天最高: {daily['high'].max():.2f}")
        print(f"   30天最低: {daily['low'].min():.2f}")
        print(f"   30天成交量合计: {daily['vol'].sum()/10000:.0f}万手")
        print(f"   30天成交额合计: {daily['amount'].sum()/100000000:.2f}亿")
        
        # 最近5天数据
        print("\n   最近5个交易日:")
        for _, row in daily.tail(5).iterrows():
            pct = row['pct_chg'] if pd.notna(row['pct_chg']) else 0
            vol = row['vol']/10000 if pd.notna(row['vol']) else 0
            print(f"   {row['trade_date']}: {row['close']:.2f} ({pct:+.2f}%) 成交{vol:.0f}万手")
    
    # 2. 资金流向
    print("\n[2] 资金流向分析:")
    moneyflow = get_moneyflow(stock['code'], start_date, end_date)
    if moneyflow is not None and len(moneyflow) > 0:
        result['data']['moneyflow'] = moneyflow.to_dict('records')
        
        # 计算主力资金净流入
        buy_elg_vol = moneyflow['buy_elg_vol'].sum() if 'buy_elg_vol' in moneyflow.columns else 0
        sell_elg_vol = moneyflow['sell_elg_vol'].sum() if 'sell_elg_vol' in moneyflow.columns else 0
        buy_lg_vol = moneyflow['buy_lg_vol'].sum() if 'buy_lg_vol' in moneyflow.columns else 0
        sell_lg_vol = moneyflow['sell_lg_vol'].sum() if 'sell_lg_vol' in moneyflow.columns else 0
        
        main_net = (buy_elg_vol + buy_lg_vol - sell_elg_vol - sell_lg_vol) / 100000000
        
        print(f"   近30天主力净流入: {main_net:.2f}亿")
        
        # 最近资金流向
        print("\n   最近5天资金流向(万元):")
        for _, row in moneyflow.tail(5).iterrows():
            net_mf = row.get('net_mf_vol', 0)
            if pd.notna(net_mf):
                print(f"   {row['trade_date']}: 净流入 {net_mf/10000:+.2f}万")
    
    # 3. 每日基本面指标
    print("\n[3] 估值指标:")
    basic = get_daily_basic(stock['code'], start_date, end_date)
    if basic is not None and len(basic) > 0:
        result['data']['daily_basic'] = basic.to_dict('records')
        latest_basic = basic.iloc[-1]
        
        pe = latest_basic.get('pe', 0)
        pb = latest_basic.get('pb', 0)
        turnover = latest_basic.get('turnover_rate', 0)
        total_mv = latest_basic.get('total_mv', 0)
        circ_mv = latest_basic.get('circ_mv', 0)
        
        print(f"   市盈率(PE): {pe:.2f}" if pd.notna(pe) else "   市盈率: N/A")
        print(f"   市净率(PB): {pb:.2f}" if pd.notna(pb) else "   市净率: N/A")
        print(f"   换手率: {turnover:.2f}%" if pd.notna(turnover) else "   换手率: N/A")
        print(f"   总市值: {total_mv:.0f}亿" if pd.notna(total_mv) else "   总市值: N/A")
        print(f"   流通市值: {circ_mv:.0f}亿" if pd.notna(circ_mv) else "   流通市值: N/A")
    
    # 4. 财务指标
    print("\n[4] 财务数据:")
    fina = get_fina_indicator(stock['code'])
    if fina is not None and len(fina) > 0:
        result['data']['fina_indicator'] = fina.to_dict('records')
        latest_fina = fina.iloc[0]
        
        roe = latest_fina.get('roe', 0)
        gross_margin = latest_fina.get('grossprofit_margin', 0)
        net_margin = latest_fina.get('netprofit_margin', 0)
        debt_ratio = latest_fina.get('debt_to_assets', 0)
        
        print(f"   ROE: {roe:.2f}%" if pd.notna(roe) else "   ROE: N/A")
        print(f"   毛利率: {gross_margin:.2f}%" if pd.notna(gross_margin) else "   毛利率: N/A")
        print(f"   净利率: {net_margin:.2f}%" if pd.notna(net_margin) else "   净利率: N/A")
        print(f"   资产负债率: {debt_ratio:.2f}%" if pd.notna(debt_ratio) else "   资产负债率: N/A")
    
    return result

def main():
    """主函数"""
    print("="*60)
    print(" 5只股票深度分析报告")
    print(f" 分析日期: {datetime.now().strftime('%Y-%m-%d')}")
    print("="*60)
    
    all_results = []
    
    for stock in STOCKS:
        try:
            result = analyze_stock(stock)
            all_results.append(result)
        except Exception as e:
            print(f"\n分析 {stock['name']} 时出错: {e}")
    
    # 保存结果
    output_file = 'stock_analysis_result.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"\n\n结果已保存到: {output_file}")
    
    # 汇总
    print("\n" + "="*60)
    print(" 汇总对比")
    print("="*60)
    
    for r in all_results:
        stock = r['stock']
        daily = r['data'].get('daily', [])
        if daily:
            latest = daily[-1]
            first = daily[0]
            change = ((latest['close'] - first['close']) / first['close']) * 100
            print(f" {stock['name']}: {latest['close']:.2f} (30天{change:+.2f}%)")

if __name__ == '__main__':
    main()