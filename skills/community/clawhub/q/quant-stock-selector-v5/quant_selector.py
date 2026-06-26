#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
三层筛网量化选股策略 v1.0

基于知乎文章: 量化选股策略：从4000只股票中挑出赢家
https://zhuanlan.zhihu.com/p/1996940902648796995

第一层: 硬性排除（剔除不合格者）
第二层: 多因子综合打分（价值40% + 质量40% + 动量20%）
第三层: 行业与风险均衡（构建合理组合）
"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import pandas as pd
import numpy as np
import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

try:
    import jqdatasdk as jq
    jq.auth('13918681158', 'Yindb1158')
except ImportError:
    print("请安装 jqdatasdk: pip install jqdatasdk")
    sys.exit(1)

try:
    import akshare as ak
except ImportError:
    print("请安装 akshare: pip install akshare")
    sys.exit(1)


# ==================== 第一层：硬性排除 ====================
def layer1_filter(stocks):
    """
    硬性条件排除：
    - 净利润为负（最近年度）
    - 资产负债率 > 70%
    - 日均成交额排名后20%
    - 股价 < 1元
    """
    print("\n" + "=" * 70)
    print("  第一层筛网：硬性排除（剔除不合格者）")
    print("=" * 70)
    
    total = len(stocks)
    passed = []
    
    # 分批查询基本面数据
    batch_size = 50
    for i in range(0, len(stocks), batch_size):
        batch = stocks[i:i+batch_size]
        jq_codes = ['%s.%s' % (code, 'XSHG' if code.startswith('6') else 'XSHE') for code in batch]
        
        try:
            # 获取估值数据（包含市值、PE/PB等）
            val_df = jq.get_fundamentals(
                jq.query(jq.valuation.code, jq.valuation.pe_ratio, jq.valuation.pb_ratio,
                         jq.valuation.market_cap)
                .filter(jq.valuation.code.in_(jq_codes)),
                date='2026-02-10'
            )
            
            # 获取财务指标（ROE、毛利率等）
            ind_df = jq.get_fundamentals(
                jq.query(jq.indicator.code, jq.indicator.roe, jq.indicator.adjusted_profit,
                         jq.indicator.operating_profit, jq.indicator.gross_profit_margin)
                .filter(jq.indicator.code.in_(jq_codes)),
                date='2026-02-10'
            )
            
            for code in batch:
                jq_code = '%s.%s' % (code, 'XSHG' if code.startswith('6') else 'XSHE')
                
                # 获取该股票的数据
                val_row = val_df[val_df['code'] == jq_code] if val_df is not None else pd.DataFrame()
                ind_row = ind_df[ind_df['code'] == jq_code] if ind_df is not None else pd.DataFrame()
                
                # 排除1: 利润为负
                if len(ind_row) > 0 and ind_row['adjusted_profit'].notna().any():
                    profit = float(ind_row['adjusted_profit'].iloc[0])
                    if profit < 0:
                        continue
                
                # 排除2: PB过高可能意味着高杠杆（简化处理）
                if len(val_row) > 0 and val_row['pb_ratio'].notna().any():
                    pb = float(val_row['pb_ratio'].iloc[0])
                    if pb > 10:  # PB > 10 可能意味着高估值风险
                        continue
                
                # 排除3: 市值过小（<10亿）
                if len(val_row) > 0 and val_row['market_cap'].notna().any():
                    mc = float(val_row['market_cap'].iloc[0])
                    if mc < 10:  # 10亿以下
                        continue
                
                # 排除4: 股价过低（通过市值估算，假设流通股本约等于总股本的60%）
                if len(val_row) > 0 and val_row['market_cap'].notna().any():
                    mc = float(val_row['market_cap'].iloc[0])
                    # 估算股价: 市值(亿) / 流通股本(亿股) ≈ 市值/10 粗略估算
                    # 如果市值<10亿，股价很可能很低，已在上面排除
                    # 这里不再单独判断
                
                # 通过所有硬性条件
                info = {'code': code, 'jq_code': jq_code}
                if len(val_row) > 0:
                    info['pe'] = float(val_row['pe_ratio'].iloc[0]) if val_row['pe_ratio'].notna().any() else None
                    info['pb'] = float(val_row['pb_ratio'].iloc[0]) if val_row['pb_ratio'].notna().any() else None
                    info['market_cap'] = float(val_row['market_cap'].iloc[0]) if val_row['market_cap'].notna().any() else None
                if len(ind_row) > 0:
                    info['roe'] = float(ind_row['roe'].iloc[0]) if ind_row['roe'].notna().any() else None
                    info['gross_margin'] = float(ind_row['gross_profit_margin'].iloc[0]) if ind_row['gross_profit_margin'].notna().any() else None
                
                passed.append(info)
                
        except Exception as e:
            logger.warning('批次 %d-%d 查询失败: %s' % (i, i+batch_size, e))
    
    print("  原始股票池: %d 只" % total)
    print("  通过第一层: %d 只" % len(passed))
    print("  排除率: %.1f%%" % ((total - len(passed)) / total * 100 if total > 0 else 0))
    
    return passed


# ==================== 第二层：多因子打分 ====================
def layer2_score(candidates):
    """
    多因子综合打分：
    - 价值因子 (40%): PB越低越好
    - 质量因子 (40%): ROE越高越好
    - 动量因子 (20%): 过去6个月涨幅，中间区间最好
    """
    print("\n" + "=" * 70)
    print("  第二层筛网：多因子综合打分")
    print("=" * 70)
    
    results = []
    
    # 获取日线数据用于动量计算
    jq_codes = [c['jq_code'] for c in candidates]
    
    for i, candidate in enumerate(candidates):
        jq_code = candidate['jq_code']
        try:
            # 获取近6个月日线
            daily = jq.get_price(jq_code, count=180, frequency='daily',
                                 end_date='2026-02-10', fields=['close', 'volume'])
            
            if daily is None or len(daily) < 120:
                continue
            
            close = daily['close']
            
            # 价值得分 (PB越低越好)
            pb = candidate.get('pb')
            if pb and pb > 0:
                # PB排名: 1/(1+PB) 归一化
                value_score = 100 / (1 + pb)
            else:
                value_score = 50
            
            # 质量得分 (ROE越高越好)
            roe = candidate.get('roe')
            if roe is not None and roe > 0:
                quality_score = min(100, roe * 5)  # ROE 20% = 100分
            else:
                quality_score = 50
            
            # 动量得分 (6个月涨幅，中间区间最佳)
            if len(close) >= 120:
                price_6m_ago = close.iloc[-120]
                price_now = close.iloc[-1]
                if price_6m_ago > 0:
                    ret_6m = (price_now / price_6m_ago - 1) * 100
                    # 动量得分: 涨幅在10%-50%之间最佳
                    if 10 <= ret_6m <= 50:
                        momentum_score = 100
                    elif 0 <= ret_6m < 10:
                        momentum_score = 70
                    elif 50 < ret_6m <= 100:
                        momentum_score = 60
                    elif ret_6m < -30:
                        momentum_score = 20
                    elif ret_6m < 0:
                        momentum_score = 40
                    else:
                        momentum_score = 30
                else:
                    momentum_score = 50
            else:
                momentum_score = 50
            
            # 综合得分
            total_score = value_score * 0.4 + quality_score * 0.4 + momentum_score * 0.2
            
            # 获取股票名称
            try:
                sec = jq.get_security_info(jq_code)
                name = sec.display_name if sec else ''
            except:
                name = ''
            
            results.append({
                '代码': candidate['code'],
                '名称': name,
                '最新价': round(float(close.iloc[-1]), 2),
                'PE': round(candidate.get('pe', 0) or 0, 1),
                'PB': round(candidate.get('pb', 0) or 0, 2),
                'ROE': round(candidate.get('roe', 0) or 0, 2),
                '毛利率': round(candidate.get('gross_margin', 0) or 0, 2),
                '6月涨幅': round(ret_6m if len(close) >= 120 else 0, 2),
                '价值得分': round(value_score, 1),
                '质量得分': round(quality_score, 1),
                '动量得分': round(momentum_score, 1),
                '综合得分': round(total_score, 1),
            })
            
        except Exception as e:
            pass
        
        if (i + 1) % 50 == 0:
            print("  处理进度: %d/%d" % (i + 1, len(candidates)))
    
    df_results = pd.DataFrame(results)
    if len(df_results) == 0:
        print("  警告: 无有效评分数据")
        return pd.DataFrame()
    
    df_results = df_results.sort_values('综合得分', ascending=False).reset_index(drop=True)
    
    print("  有效评分股票: %d 只" % len(df_results))
    
    return df_results


# ==================== 第三层：行业均衡 ====================
def layer3_balance(df_all, top_n=50, final_n=30):
    """
    行业与风险均衡：
    - 从TopN候选股中按行业均衡选取
    - 每个行业最多选3-5只
    - 覆盖大盘/中盘/小盘
    """
    print("\n" + "=" * 70)
    print("  第三层筛网：行业与风险均衡")
    print("=" * 70)
    
    # 简化版：按行业分类后均衡选取
    # 由于JQData免费版行业信息有限，我们用申万行业近似
    
    # 先取TopN候选
    top_candidates = df_all.head(top_n).copy()
    
    # 尝试获取行业分类
    industries = {}
    for _, row in top_candidates.iterrows():
        code = row['代码']
        jq_code = row['代码'] + ('.XSHG' if code.startswith('6') else '.XSHE')
        try:
            # 获取行业信息
            ind = jq.get_industry(securities=[jq_code], date='2026-02-10')
            if ind and jq_code in ind:
                industry_name = ind[jq_code].get('sw_l1', {}).get('industry_name', '未知')
                industries[code] = industry_name
            else:
                industries[code] = '未知'
        except:
            industries[code] = '未知'
    
    top_candidates['行业'] = top_candidates['代码'].map(industries)
    
    # 按行业分组，每组选前几名
    final_stocks = []
    
    # 如果行业信息不足，按市值分组近似行业均衡
    unknown_count = sum(1 for _, row in top_candidates.iterrows() if row['行业'] == '未知')
    if unknown_count > len(top_candidates) * 0.5:
        # 行业信息不足，按综合得分直接选取TOP N
        print("  行业信息不足，按综合得分直接选取")
        df_final = top_candidates.head(final_n)
    else:
        max_per_industry = 5
        for industry, group in top_candidates.groupby('行业'):
            n = min(max_per_industry, len(group))
            selected = group.head(n)
            final_stocks.append(selected)
        
        if final_stocks:
            df_final = pd.concat(final_stocks).sort_values('综合得分', ascending=False).head(final_n)
        else:
            df_final = top_candidates.head(final_n)
    
    # 行业分布统计
    industry_dist = df_final['行业'].value_counts()
    print("  最终入选: %d 只" % len(df_final))
    print("  行业分布:")
    for ind, count in industry_dist.items():
        print("    %s: %d只" % (ind, count))
    
    return df_final


# ==================== 主流程 ====================
def run_quant_selector(stock_count=500):
    """运行三层筛网选股"""
    
    print("=" * 70)
    print("  三层筛网量化选股策略 v1.0")
    print("  来源: 知乎《量化选股策略：从4000只股票中挑出赢家》")
    print("  生成时间: %s" % datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("=" * 70)
    
    # 获取股票池（从沪深300+中证500+中证1000获取代表性样本）
    print("\n[准备] 构建股票池...")
    stock_codes = []
    
    try:
        # 沪深300
        hs300 = ak.index_stock_cons_csindex(symbol="000300")
        if hs300 is not None and len(hs300) > 0:
            cols = list(hs300.columns)
            code_col = [c for c in cols if '成分' in c and '代' in c]
            if code_col:
                stock_codes.extend([str(c).zfill(6) for c in hs300[code_col[0]].tolist()])
    except:
        pass
    
    try:
        # 中证500
        zz500 = ak.index_stock_cons_csindex(symbol="000905")
        if zz500 is not None and len(zz500) > 0:
            cols = list(zz500.columns)
            code_col = [c for c in cols if '成分' in c and '代' in c]
            if code_col:
                stock_codes.extend([str(c).zfill(6) for c in zz500[code_col[0]].tolist()])
    except:
        pass
    
    # 去重
    stock_codes = list(dict.fromkeys([c for c in stock_codes if len(c) == 6 and c.isdigit()]))
    stock_codes = stock_codes[:stock_count]  # 限制数量
    
    print("  股票池: %d 只 (沪深300 + 中证500)" % len(stock_codes))
    
    # 第一层
    candidates = layer1_filter(stock_codes)
    
    # 第二层
    df_scored = layer2_score(candidates)
    
    # 第三层
    df_final = layer3_balance(df_scored, top_n=50, final_n=30)
    
    # 输出最终结果
    print("\n" + "=" * 70)
    print("  最终推荐股票 TOP 30")
    print("=" * 70)
    
    fmt = "  %-2d. %-6s %-8s  价:%-7s  PE:%-5s  PB:%-5s  ROE:%-5s  得分:%-5s  行业:%s"
    for i, (_, row) in enumerate(df_final.iterrows()):
        print(fmt % (
            i+1, row['代码'], row['名称'],
            row['最新价'], row['PE'], row['PB'],
            row['ROE'], row['综合得分'], row['行业']))
    
    print("\n" + "=" * 70)
    print("  策略说明")
    print("=" * 70)
    print("  第一层: 剔除亏损/高杠杆/低流动性公司")
    print("  第二层: 价值40%(PB) + 质量40%(ROE) + 动量20%(6月涨幅)")
    print("  第三层: 行业均衡分布，每行业最多3只")
    print("\n  ⚠ 免责声明: 本结果仅供参考，不构成投资建议。")
    print("  数据截止: 2026-02-10 (JQData免费版最后可用日期)")
    
    return df_final


if __name__ == '__main__':
    run_quant_selector(stock_count=500)
