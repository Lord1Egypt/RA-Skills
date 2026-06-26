#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
杨永兴尾盘选股法 - 增强版
功能：
1. 从 main_board_stocks.json 读取股票列表
2. 腾讯财经快速初筛（实时数据）
3. Baostock 深度筛选（历史数据）
4. 输出符合条件的股票

筛选条件：
1. 涨幅 3%-5%
2. 量比 > 1
3. 换手率 5%-10%
4. 市值 50 亿 -200 亿
5. 近 5 日成交量持续放大
6. 5/10/20 日均线在 60 日线上方（多头排列）
7. 股价创当天新高
8. 分时图价格在均线上方

数据源：
- 实时行情：腾讯财经 API
- 历史数据：Baostock（仅深度筛选）
- 股票列表：main_board_stocks.json
"""

import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import time
import os
import warnings
warnings.filterwarnings('ignore')

# ============== 市值缓存管理 ==============
def load_market_cap_cache():
    """加载市值缓存"""
    try:
        if os.path.exists(MARKET_CAP_CACHE_FILE):
            with open(MARKET_CAP_CACHE_FILE, 'r', encoding='utf-8') as f:
                cache = json.load(f)
            
            # 检查缓存是否过期（30 天）
            cache_date = datetime.strptime(cache.get('date', '1970-01-01'), '%Y-%m-%d')
            days_old = (datetime.now() - cache_date).days
            
            if days_old < MARKET_CAP_CACHE_DAYS:
                below_min = cache.get('below_min', [])
                print(f"✅ 加载市值缓存：{len(below_min)} 只股票（{days_old} 天前）")
                return set(below_min)
            else:
                print(f"⚠️ 市值缓存已过期（{days_old} 天），将重新生成")
                return set()
        else:
            print(f"📝 市值缓存不存在，将创建新缓存")
            return set()
    except Exception as e:
        print(f"⚠️ 加载市值缓存失败：{e}")
        return set()

def save_market_cap_cache(below_min_codes):
    """保存市值缓存"""
    try:
        cache = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'below_min': list(below_min_codes),
            'count': len(below_min_codes),
        }
        with open(MARKET_CAP_CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
        print(f"💾 已保存市值缓存：{len(below_min_codes)} 只股票 < {MARKET_CAP_MIN}亿")
    except Exception as e:
        print(f"⚠️ 保存市值缓存失败：{e}")

# ============== 配置 ==============
# 杨永兴尾盘买入法条件
YANG_CONDITIONS = {
    # 基础条件
    'pctChg_min': 3.0,       # 涨幅 3-5%
    'pctChg_max': 5.0,
    'turnover_min': 5.0,     # 换手率 5-10%
    'turnover_max': 10.0,
    'market_cap_min': 50,    # 市值 50-200 亿
    'market_cap_max': 200,
    
    # 量比条件
    'volume_ratio_min': 1.0, # 量比>1
    
    # 成交量条件
    'volume_increase_days': 5, # 近 5 日成交量放大
    
    # 均线条件
    'ma_above_ma60': True,   # 5/10/20 日均线在 60 日线上方
}

# 速率限制：每秒 10 个请求
REQUESTS_PER_SECOND = 10

# 股票数据文件路径（支持相对路径）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STOCK_FILE_RELATIVE = os.path.join(SCRIPT_DIR, '..', 'skills', 'query-main-board-stocks', 'main_board_stocks.json')
STOCK_FILE_ABSOLUTE = '/home/admin/.openclaw/workspace-feishu/skills/query-main-board-stocks/main_board_stocks.json'

# 市值缓存配置
MARKET_CAP_CACHE_FILE = os.path.join(SCRIPT_DIR, 'market_cap_cache.json')
MARKET_CAP_CACHE_DAYS = 30  # 缓存 30 天
MARKET_CAP_MIN = 50  # 最小市值 50 亿

# ============== 腾讯财经 API ==============
def get_tencent_realtime(code):
    """
    腾讯财经获取实时行情
    
    参数:
        code: 股票代码（支持两种格式：sh.600000 或 sh600000）
    
    返回:
        dict: 实时行情数据
    """
    # 代码格式转换：sh.600000 → sh600000
    code_clean = code.replace('.', '')
    url = f"http://qt.gtimg.cn/q={code_clean}"
    
    try:
        response = requests.get(url, timeout=5)
        response.encoding = 'gbk'
        
        data = response.text.strip()
        if not data or '=' not in data:
            return None
        
        quote_data = data.split('=')[1].strip().strip('"').split('~')
        
        if len(quote_data) < 50:
            return None
        
        # 计算涨跌幅
        price = float(quote_data[3]) if quote_data[3] else 0
        pre_close = float(quote_data[4]) if quote_data[4] else 0
        pctChg = (price - pre_close) / pre_close * 100 if pre_close > 0 else 0
        
        # 获取市值（字段 44 是总市值，45 是流通市值，单位亿）
        market_cap = float(quote_data[44]) if len(quote_data) > 44 and quote_data[44] else 0
        
        return {
            'code': code,
            'name': quote_data[1],
            'price': price,
            'open': float(quote_data[5]) if quote_data[5] else 0,
            'high': float(quote_data[33]) if quote_data[33] else 0,
            'low': float(quote_data[34]) if quote_data[34] else 0,
            'pre_close': pre_close,
            'pctChg': pctChg,
            'volume': int(quote_data[6]) if quote_data[6] else 0,
            'amount': float(quote_data[37]) if quote_data[37] else 0,
            'turnover': float(quote_data[38]) if quote_data[38] else 0,
            'market_cap': market_cap,
        }
    
    except Exception as e:
        return None

# ============== 基础条件筛选（腾讯财经数据）==============
def check_basic_conditions(realtime_data):
    """
    检查基础条件（仅使用腾讯财经实时数据）
    
    条件：
    1. 涨幅 3%-5%
    2. 换手率 5%-10%
    3. 市值 50 亿 -200 亿
    
    返回:
        (是否符合，详细条件字典)
    """
    if not realtime_data:
        return False, {}
    
    pctChg = realtime_data['pctChg']
    turnover = realtime_data.get('turnover', 0)
    market_cap = realtime_data.get('market_cap', 0)
    
    conditions = {
        'pctChg': pctChg,
        'pctChg_pass': YANG_CONDITIONS['pctChg_min'] <= pctChg <= YANG_CONDITIONS['pctChg_max'],
        'turnover': turnover,
        'turnover_pass': YANG_CONDITIONS['turnover_min'] <= turnover <= YANG_CONDITIONS['turnover_max'],
        'market_cap': market_cap,
        'market_cap_pass': YANG_CONDITIONS['market_cap_min'] <= market_cap <= YANG_CONDITIONS['market_cap_max'],
    }
    
    # 基础条件必须全部满足
    is_pass = all([
        conditions['pctChg_pass'],
        conditions['turnover_pass'],
        conditions['market_cap_pass'],
    ])
    
    return is_pass, conditions

# ============== 历史数据获取 ==============
def get_hist_data_batch(codes, days=100):
    """批量获取历史数据（一次登录，多次查询）"""
    try:
        import baostock as bs
        
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=int(days * 2))).strftime('%Y-%m-%d')
        
        bs.login()
        
        results = {}
        for i, code in enumerate(codes):
            try:
                rs = bs.query_history_k_data_plus(code,
                    "date,code,open,high,low,close,volume,amount,pctChg,turn",
                    start_date=start_date, end_date=end_date, frequency="d", adjustflag="3")
                
                data_list = [rs.get_row_data() for _ in iter(rs.next, False)]
                
                if data_list:
                    df = pd.DataFrame(data_list, columns=rs.fields)
                    for col in ['close', 'open', 'high', 'low', 'volume', 'amount', 'pctChg', 'turn']:
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                    df = df.dropna(subset=['close']).sort_values('date').reset_index(drop=True)
                    results[code] = df
                    
                # 每 100 只显示进度
                if (i + 1) % 100 == 0:
                    print(f"  历史数据进度：{i+1}/{len(codes)}")
                    
            except Exception as e:
                results[code] = pd.DataFrame()
        
        bs.logout()
        return results
    except Exception as e:
        print(f"❌ 批量获取历史数据失败：{e}")
        return {}

# ============== 深度条件筛选（需要历史数据）==============
def check_advanced_conditions(realtime_data, hist_df):
    """
    检查深度条件（需要历史数据）
    
    条件：
    1. 量比 > 1
    2. 近 5 日成交量持续放大
    3. 5/10/20 日均线在 60 日线上方（多头排列）
    4. 股价创当天新高
    
    返回:
        (是否符合，详细条件字典)
    """
    if not realtime_data or len(hist_df) < 60:
        return False, {}
    
    close = realtime_data['price']
    high = realtime_data['high']
    volume = realtime_data['volume']
    
    # 计算均线
    ma5 = hist_df['close'].rolling(5).mean().iloc[-1]
    ma10 = hist_df['close'].rolling(10).mean().iloc[-1]
    ma20 = hist_df['close'].rolling(20).mean().iloc[-1]
    ma60 = hist_df['close'].rolling(60).mean().iloc[-1]
    
    # 计算量比（今日成交量 / 近 5 日平均成交量）
    volume_ma5 = hist_df['volume'].rolling(5).mean().iloc[-1]
    volume_ratio = volume / (volume_ma5 + 0.001)
    
    # 检查近 5 日成交量是否持续放大
    volume_5days = hist_df['volume'].iloc[-5:].tolist()
    volume_increasing = all(volume_5days[i] >= volume_5days[i-1] for i in range(1, len(volume_5days))) if len(volume_5days) >= 5 else False
    
    # 检查多头排列
    ma_bullish = (ma5 > ma60) and (ma10 > ma60) and (ma20 > ma60)
    
    # 检查是否创当天新高
    is_new_high = (close >= high * 0.99)  # 接近最高价
    
    conditions = {
        'volume_ratio': round(volume_ratio, 2),
        'volume_ratio_pass': volume_ratio > YANG_CONDITIONS['volume_ratio_min'],
        'volume_increasing': volume_increasing,
        'ma5': round(ma5, 2),
        'ma10': round(ma10, 2),
        'ma20': round(ma20, 2),
        'ma60': round(ma60, 2),
        'ma_bullish': ma_bullish,
        'is_new_high': is_new_high,
    }
    
    # 深度条件（至少满足 3 个）
    pass_count = sum([
        conditions['volume_ratio_pass'],
        conditions['volume_increasing'],
        conditions['ma_bullish'],
        conditions['is_new_high'],
    ])
    
    is_pass = pass_count >= 3
    return is_pass, conditions

# ============== 加载股票列表 ==============
def load_stock_list():
    """从 main_board_stocks.json 加载股票列表"""
    possible_paths = [
        STOCK_FILE_RELATIVE,
        STOCK_FILE_ABSOLUTE,
        os.path.join(SCRIPT_DIR, 'main_board_stocks.json'),
    ]
    
    for stock_file in possible_paths:
        try:
            with open(stock_file, 'r', encoding='utf-8') as f:
                stock_data = json.load(f)
            
            stocks = stock_data.get('stocks', [])
            print(f"✅ 加载股票列表：{len(stocks)} 只")
            print(f"📂 数据来源：{stock_file}")
            return stocks
        except FileNotFoundError:
            continue
        except Exception as e:
            print(f"⚠️ 读取文件失败 ({stock_file}): {e}")
            continue
    
    print(f"❌ 无法找到股票数据文件 main_board_stocks.json")
    print(f"📂 尝试的路径:")
    for path in possible_paths:
        print(f"   - {path}")
    print(f"\n⚠️ 请先运行以下命令生成股票列表:")
    print(f"   cd /home/admin/.openclaw/workspace-feishu/skills/query-main-board-stocks")
    print(f"   python3 query_main_board_stocks.py")
    return []

# ============== 主函数 ==============
def main():
    print("=" * 90)
    print("杨永兴尾盘选股法 - 增强版")
    print("=" * 90)
    print(f"运行时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"数据源：腾讯财经 API + Baostock")
    print(f"速率限制：{REQUESTS_PER_SECOND} 只/秒")
    print("=" * 90)
    print(f"\n📋 筛选条件:")
    print(f"  1. 涨幅 3%-5%")
    print(f"  2. 量比 > 1")
    print(f"  3. 换手率 5%-10%")
    print(f"  4. 市值 50 亿 -200 亿")
    print(f"  5. 近 5 日成交量持续放大")
    print(f"  6. 5/10/20 日均线在 60 日线上方")
    print(f"  7. 股价创当天新高")
    print("=" * 90)
    
    # 加载股票列表
    main_stocks = load_stock_list()
    
    if not main_stocks:
        return
    
    # 过滤创业板和科创板
    filtered_stocks = []
    for stock in main_stocks:
        pure_code = stock.get('pure_code', stock['code'].replace('sh.', '').replace('sz.', ''))
        if pure_code[:3] not in ['300', '301', '688']:
            filtered_stocks.append(stock)
    
    print(f"✅ 过滤后主板股票：{len(filtered_stocks)} 只（排除创业板/科创板）")
    
    # 加载市值缓存，过滤市值低于 50 亿的股票
    market_cap_blacklist = load_market_cap_cache()
    if market_cap_blacklist:
        original_count = len(filtered_stocks)
        filtered_stocks = [s for s in filtered_stocks if s['code'] not in market_cap_blacklist]
        skipped_count = original_count - len(filtered_stocks)
        print(f"🚫 跳过市值缓存中的股票：{skipped_count} 只（市值 < {MARKET_CAP_MIN}亿）")
        print(f"✅ 待查询股票：{len(filtered_stocks)} 只")
    
    print("=" * 90)
    
    # ========== 步骤 1: 腾讯财经快速初筛 ==========
    print(f"\n【步骤 1】腾讯财经快速初筛（基础条件）...")
    print(f"{'-'*90}")
    
    initial_candidates = []
    new_below_min = set()  # 记录本次新发现的低市值股票
    total_count = len(filtered_stocks)
    start_time = time.time()
    
    for i, stock in enumerate(filtered_stocks):
        code = stock['code']
        
        # 速率限制
        if i > 0 and i % REQUESTS_PER_SECOND == 0:
            elapsed = time.time() - start_time
            expected_time = i / REQUESTS_PER_SECOND
            if elapsed < expected_time:
                time.sleep(expected_time - elapsed)
            start_time = time.time()
        
        # 显示进度
        if (i + 1) % 500 == 0:
            print(f"  进度：{i+1}/{total_count} ({(i+1)/total_count*100:.1f}%)")
        
        # 获取实时数据
        realtime = get_tencent_realtime(code)
        
        if not realtime:
            continue
        
        # 检查市值
        market_cap = realtime.get('market_cap', 0)
        if market_cap > 0 and market_cap < MARKET_CAP_MIN:
            new_below_min.add(code)
            print(f"[{i+1}/{total_count}] {code} {realtime['name']} 🚫 市值{market_cap:.0f}亿 < {MARKET_CAP_MIN}亿")
            continue
        
        # 基础条件筛选
        is_pass, conditions = check_basic_conditions(realtime)
        
        if is_pass:
            initial_candidates.append({
                'code': code,
                'name': realtime['name'],
                'price': realtime['price'],
                'pctChg': conditions['pctChg'],
                'turnover': conditions['turnover'],
                'market_cap': conditions['market_cap'],
            })
            print(f"[{len(initial_candidates)}] {code} {realtime['name']} ✅ 基础✅ 涨幅{conditions['pctChg']:.1f}% 换手{conditions['turnover']:.1f}% 市值{conditions['market_cap']:.0f}亿")
        else:
            reasons = []
            if not conditions.get('pctChg_pass', False):
                reasons.append(f"涨幅{conditions.get('pctChg', 0):.1f}%")
            if not conditions.get('turnover_pass', False):
                reasons.append(f"换手{conditions.get('turnover', 0):.1f}%")
            if not conditions.get('market_cap_pass', False):
                reasons.append(f"市值{conditions.get('market_cap', 0):.0f}亿")
            if reasons:
                print(f"[{i+1}/{total_count}] {code} {realtime['name']} ❌ {' '.join(reasons)}")
    
    # 保存新的市值缓存
    if new_below_min:
        save_market_cap_cache(new_below_min)
    
    print(f"\n✅ 通过基础筛选：{len(initial_candidates)} 只")
    
    if len(initial_candidates) == 0:
        print(f"\n⚠️ 无股票符合基础条件")
        return
    
    # ========== 步骤 2: Baostock 深度筛选 ==========
    print(f"\n【步骤 2】Baostock 深度筛选（高级条件）...")
    print(f"{'-'*90}")
    
    codes_to_check = [c['code'] for c in initial_candidates]
    hist_data_dict = get_hist_data_batch(codes_to_check, days=100)
    
    final_candidates = []
    
    for candidate in initial_candidates:
        code = candidate['code']
        hist_df = hist_data_dict.get(code, pd.DataFrame())
        
        if len(hist_df) < 60:
            print(f"{code} {candidate['name']} ❌ 历史数据不足")
            continue
        
        # 深度条件筛选
        is_pass, conditions = check_advanced_conditions(candidate, hist_df)
        
        if is_pass:
            final_candidates.append({
                **candidate,
                'volume_ratio': conditions['volume_ratio'],
                'ma5': conditions['ma5'],
                'ma10': conditions['ma10'],
                'ma20': conditions['ma20'],
                'ma60': conditions['ma60'],
                'ma_bullish': conditions['ma_bullish'],
                'is_new_high': conditions['is_new_high'],
            })
            print(f"{code} {candidate['name']} ✅ 深度✅ 量比{conditions['volume_ratio']:.2f} 多头{'✅' if conditions['ma_bullish'] else '❌'} 新高{'✅' if conditions['is_new_high'] else '❌'}")
        else:
            reasons = []
            if not conditions.get('volume_ratio_pass', False):
                reasons.append(f"量比{conditions.get('volume_ratio', 0):.2f}")
            if not conditions.get('ma_bullish', False):
                reasons.append("均线空头")
            if not conditions.get('is_new_high', False):
                reasons.append("未创新高")
            if reasons:
                print(f"{code} {candidate['name']} ❌ {' '.join(reasons)}")
    
    # ========== 输出最终结果 ==========
    total_elapsed = time.time() - start_time
    
    print(f"\n{'='*90}")
    print(f"📊 筛选结果")
    print(f"{'='*90}")
    print(f"\n符合杨永兴条件：{len(final_candidates)} 只")
    print(f"总耗时：{total_elapsed:.1f} 秒")
    
    if len(final_candidates) == 0:
        print(f"\n⚠️ 今日无股票符合杨永兴尾盘买入法条件")
        return
    
    # 输出最终结果
    print(f"\n{'='*90}")
    print(f"🏆 杨永兴选股最终结果")
    print(f"{'='*90}")
    print(f"\n{'排名':<6} {'代码':<12} {'名称':<12} {'现价':>10} {'涨幅':>8} {'换手':>8} {'市值':>8} {'量比':>8} {'均线':>6}")
    print(f"{'-'*90}")
    
    # 按涨幅排序
    final_candidates.sort(key=lambda x: x['pctChg'], reverse=True)
    
    for i, stock in enumerate(final_candidates):
        ma_status = '✅' if stock['ma_bullish'] else '❌'
        print(f"{i+1:<6} {stock['code']:<12} {stock['name']:<12} "
              f"{stock['price']:>10.2f} {stock['pctChg']:>7.1f}% {stock['turnover']:>7.1f}% {stock['market_cap']:>7.0f}亿 {stock['volume_ratio']:>8.2f} {ma_status:>6}")
    
    print(f"\n{'='*90}")
    print(f"✅ 筛选完成")
    print(f"{'='*90}")

if __name__ == '__main__':
    main()
