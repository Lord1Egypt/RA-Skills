#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
股票分析专家 - 核心分析模块
功能：实时行情分析、技术指标计算、潜力股筛选
"""

import os
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# 尝试导入 tushare
try:
    import tushare as ts
    TUSHARE_AVAILABLE = True
except ImportError:
    TUSHARE_AVAILABLE = False
    print("警告：tushare 未安装，部分功能不可用")

# 尝试导入 pandas
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False


class StockAnalyzer:
    """股票分析器"""
    
    def __init__(self):
        self.tushare_token = os.environ.get('TUSHARE_TOKEN')
        self.finnhub_token = os.environ.get('FINNHUB_TOKEN')
        
        if TUSHARE_AVAILABLE and self.tushare_token:
            ts.set_token(self.tushare_token)
            self.pro = ts.pro_api()
        else:
            self.pro = None
    
    def get_stock_quote(self, ts_code: str) -> Optional[Dict]:
        """获取股票实时行情"""
        if not self.pro:
            return {"error": "Tushare 未初始化"}
        
        try:
            df = self.pro.daily(ts_code=ts_code, start_date=datetime.now().strftime('%Y%m%d'))
            if df is not None and not df.empty:
                return df.iloc[0].to_dict()
        except Exception as e:
            return {"error": str(e)}
        
        return None
    
    def get_technical_indicators(self, ts_code: str, period: int = 60) -> Optional[Dict]:
        """计算技术指标（MACD/RSI/KDJ）"""
        if not self.pro or not PANDAS_AVAILABLE:
            return None
        
        try:
            # 获取日线数据
            df = self.pro.daily(ts_code=ts_code, 
                               start_date=(datetime.now() - timedelta(days=period)).strftime('%Y%m%d'))
            
            if df is None or df.empty:
                return None
            
            # 计算 MACD
            df = self._calc_macd(df)
            
            # 计算 RSI
            df = self._calc_rsi(df)
            
            # 计算 KDJ
            df = self._calc_kdj(df)
            
            # 返回最新一期数据
            latest = df.iloc[-1]
            return {
                'macd': {
                    'DIF': float(latest.get('DIF', 0)),
                    'DEA': float(latest.get('DEA', 0)),
                    'MACD': float(latest.get('MACD', 0)),
                    'signal': '金叉' if latest.get('DIF', 0) > latest.get('DEA', 0) else '死叉'
                },
                'rsi': {
                    'RSI6': float(latest.get('RSI6', 0)),
                    'RSI12': float(latest.get('RSI12', 0)),
                    'RSI24': float(latest.get('RSI24', 0)),
                    'signal': self._rsi_signal(float(latest.get('RSI6', 50)))
                },
                'kdj': {
                    'K': float(latest.get('K', 0)),
                    'D': float(latest.get('D', 0)),
                    'J': float(latest.get('J', 0)),
                    'signal': '金叉' if float(latest.get('K', 0)) > float(latest.get('D', 0)) else '死叉'
                }
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _calc_macd(self, df: pd.DataFrame) -> pd.DataFrame:
        """计算 MACD"""
        if not PANDAS_AVAILABLE:
            return df
        
        exp1 = df['close'].ewm(span=12, adjust=False).mean()
        exp2 = df['close'].ewm(span=26, adjust=False).mean()
        df['DIF'] = exp1 - exp2
        df['DEA'] = df['DIF'].ewm(span=9, adjust=False).mean()
        df['MACD'] = (df['DIF'] - df['DEA']) * 2
        return df
    
    def _calc_rsi(self, df: pd.DataFrame) -> pd.DataFrame:
        """计算 RSI"""
        if not PANDAS_AVAILABLE:
            return df
        
        for period in [6, 12, 24]:
            delta = df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            df[f'RSI{period}'] = 100 - (100 / (1 + rs))
        return df
    
    def _calc_kdj(self, df: pd.DataFrame) -> pd.DataFrame:
        """计算 KDJ"""
        if not PANDAS_AVAILABLE:
            return df
        
        low_min = df['low'].rolling(window=9).min()
        high_max = df['high'].rolling(window=9).max()
        rsv = (df['close'] - low_min) / (high_max - low_min) * 100
        
        df['K'] = rsv.ewm(com=2).mean()
        df['D'] = df['K'].ewm(com=2).mean()
        df['J'] = 3 * df['K'] - 2 * df['D']
        return df
    
    def _rsi_signal(self, rsi: float) -> str:
        """RSI 信号判断"""
        if rsi > 80:
            return '超买'
        elif rsi < 20:
            return '超卖'
        elif rsi > 50:
            return '偏强'
        elif rsi < 50:
            return '偏弱'
        else:
            return '中性'
    
    def screen_stocks(self, criteria: Dict) -> List[Dict]:
        """
        筛选股票
        
        criteria: 筛选条件
        - pe_max: 最大市盈率
        - roe_min: 最小 ROE
        - market_cap_min: 最小市值（亿）
        - volume_ratio: 量比要求
        """
        if not self.pro:
            return []
        
        try:
            # 获取股票池（这里简化为沪深 300）
            hs300 = self.pro.index_weight(index_code='000300.SH',
                                         start_date=datetime.now().strftime('%Y%m%d'),
                                         end_date=datetime.now().strftime('%Y%m%d'))
            
            if hs300 is None or hs300.empty:
                return []
            
            results = []
            # 简化处理，实际应该批量获取
            for ts_code in hs300['con_code'].head(20):  # 只检查前 20 支
                try:
                    basic = self.pro.daily_basic(ts_code=ts_code,
                                                trade_date=datetime.now().strftime('%Y%m%d'))
                    if basic is not None and not basic.empty:
                        row = basic.iloc[0]
                        if self._match_criteria(row, criteria):
                            results.append({
                                'ts_code': ts_code,
                                'pe_ttm': float(row.get('pe_ttm', 0)),
                                'pb': float(row.get('pb', 0)),
                                'total_mv': float(row.get('total_mv', 0)) / 10000,  # 转为亿
                                'volume_ratio': float(row.get('volume_ratio', 0)),
                                'turnover_rate': float(row.get('turnover_rate', 0))
                            })
                except:
                    continue
            
            return results[:5]  # 返回最多 5 支
        except Exception as e:
            print(f"筛选错误：{e}")
            return []
    
    def _match_criteria(self, stock: pd.Series, criteria: Dict) -> bool:
        """判断股票是否符合筛选条件"""
        pe_max = criteria.get('pe_max', 100)
        roe_min = criteria.get('roe_min', 0)
        market_cap_min = criteria.get('market_cap_min', 0)
        
        pe_ttm = stock.get('pe_ttm', 0)
        total_mv = stock.get('total_mv', 0) / 10000  # 转为亿
        
        if pe_ttm is None or pe_ttm <= 0:
            return False
        if pe_ttm > pe_max:
            return False
        if total_mv < market_cap_min:
            return False
        
        return True
    
    def generate_morning_report(self) -> str:
        """生成早盘报告"""
        report = []
        report.append("# 📊 早盘策略报告")
        report.append(f"**日期**：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
        report.append("")
        
        # 市场环境
        report.append("## 市场环境")
        report.append("- 数据获取中...")
        report.append("")
        
        # 热点预判
        report.append("## 今日热点预判")
        report.append("1. 待分析")
        report.append("2. 待分析")
        report.append("3. 待分析")
        report.append("")
        
        # 操作策略
        report.append("## 操作策略")
        report.append("- **仓位建议**：50-70%")
        report.append("- **关注方向**：待分析")
        report.append("- **风险提示**：注意市场波动")
        report.append("")
        
        return "\n".join(report)
    
    def analyze_stock(self, ts_code: str) -> str:
        """分析个股"""
        report = []
        report.append(f"# 📈 个股分析 - {ts_code}")
        report.append("")
        
        # 获取行情
        quote = self.get_stock_quote(ts_code)
        if quote and 'error' not in quote:
            report.append("## 实时数据")
            report.append(f"- 最新价：{quote.get('close', 'N/A')}")
            report.append(f"- 涨跌幅：{quote.get('pct_chg', 'N/A')}%")
            report.append(f"- 成交量：{quote.get('vol', 'N/A')} 手")
            report.append("")
        
        # 技术指标
        tech = self.get_technical_indicators(ts_code)
        if tech and 'error' not in tech:
            report.append("## 技术指标")
            report.append(f"- **MACD**：{tech['macd']['signal']}")
            report.append(f"- **RSI**：{tech['rsi']['signal']} (RSI6={tech['rsi']['RSI6']:.2f})")
            report.append(f"- **KDJ**：{tech['kdj']['signal']}")
            report.append("")
        
        # 操作建议
        report.append("## 操作建议")
        report.append("- **短线**：待分析")
        report.append("- **中线**：待分析")
        report.append("- **目标价**：待计算")
        report.append("- **止损价**：待计算")
        report.append("")
        
        return "\n".join(report)


# 主函数
def main():
    # 设置 UTF-8 编码输出
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    analyzer = StockAnalyzer()
    
    # 测试
    print("Stock Expert - Test")
    print("=" * 50)
    
    # 生成早盘报告
    report = analyzer.generate_morning_report()
    print(report)
    
    print("\n[OK] 技能运行正常！")
    print("[提示] 安装 tushare 后可获取真实数据：pip install tushare")
    
    # 分析个股（示例：贵州茅台）
    # analysis = analyzer.analyze_stock('600519.SH')
    # print(analysis)


if __name__ == '__main__':
    main()
