"""
股票PE/PB历史水位分析器
功能：根据股票名称或代码，分析其PE、PB在过去十年中的历史水位
数据源：使用BaoStock API获取真实实盘数据
"""

import baostock as bs
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Optional, Tuple, Dict, List
import warnings
import time
import json
import os
import sys

warnings.filterwarnings('ignore')


class StockPEPBAnalyzer:
    """股票PE/PB历史水位分析器"""
    
    def __init__(self):
        self.lg = None
        self.stock_list_cache = None
        self.stock_name_to_code = {}
        self._login()
        self._init_stock_list()
    
    def _login(self):
        """登录BaoStock"""
        print("正在登录BaoStock...")
        self.lg = bs.login()
        if self.lg.error_code != '0':
            print(f"✗ 登录失败: {self.lg.error_msg}")
        else:
            print(f"✓ 登录成功")
    
    def _logout(self):
        """登出BaoStock"""
        if self.lg:
            bs.logout()
            print("已登出BaoStock")
    
    def _init_stock_list(self):
        """初始化股票列表缓存"""
        try:
            print("正在加载股票列表...")
            
            # 获取沪深A股列表（使用最近的一个交易日）
            today = datetime.now()
            for i in range(5):
                date_str = (today - timedelta(days=i)).strftime("%Y-%m-%d")
                rs = bs.query_all_stock(day=date_str)
                
                stock_list = []
                while (rs.error_code == '0') & rs.next():
                    stock_list.append(rs.get_row_data())
                
                if len(stock_list) > 1000:
                    print(f"  使用日期: {date_str}")
                    break
            
            self.stock_list_cache = pd.DataFrame(stock_list, columns=rs.fields)
            self._enrich_stock_info()
            print(f"✓ 已加载 {len(self.stock_list_cache)} 只股票")
        except Exception as e:
            print(f"✗ 初始化失败: {e}")
            self.stock_list_cache = pd.DataFrame()
    
    def _enrich_stock_info(self):
        """获取股票详细信息（名称、行业等）"""
        print("正在获取股票详细信息...")
        
        if 'code_name' in self.stock_list_cache.columns:
            stock_df = self.stock_list_cache[
                self.stock_list_cache['code'].str.match(r'^(sh\.(6|9)|sz\.(0|3|2))', na=False)
            ].copy()
            
            for _, row in stock_df.iterrows():
                name = row.get('code_name', '')
                code = row['code']
                if name and code:
                    self.stock_name_to_code[name] = code
            
            print(f"  ✓ 成功获取 {len(self.stock_name_to_code)} 只股票名称信息")
        else:
            print("  ! 股票列表中没有code_name字段，将仅支持股票代码查询")
    
    def search_stock(self, keyword: str) -> List[Dict[str, str]]:
        """
        根据关键词搜索股票
        
        Args:
            keyword: 股票名称或代码（支持模糊匹配）
            
        Returns:
            匹配的股票列表
        """
        if self.stock_list_cache is None or len(self.stock_list_cache) == 0:
            print("股票列表未加载，重新初始化...")
            self._init_stock_list()
        
        results = []
        keyword = keyword.strip()
        keyword_upper = keyword.upper()
        
        # 精确匹配代码
        exact_code_match = self.stock_list_cache[self.stock_list_cache['code'].str.upper() == keyword_upper]
        if len(exact_code_match) == 0 and not keyword.startswith(('SH.', 'SZ.', 'sh.', 'sz.')):
            if keyword.startswith('6'):
                exact_code_match = self.stock_list_cache[self.stock_list_cache['code'] == f'sh.{keyword}']
            else:
                exact_code_match = self.stock_list_cache[self.stock_list_cache['code'] == f'sz.{keyword}']
        
        if len(exact_code_match) > 0:
            for _, row in exact_code_match.iterrows():
                results.append({
                    'code': row['code'],
                    'name': row.get('code_name', 'N/A'),
                    'tradeStatus': row.get('tradeStatus', 'N/A')
                })
            return results
        
        # 精确匹配名称
        if 'code_name' in self.stock_list_cache.columns:
            exact_name_match = self.stock_list_cache[self.stock_list_cache['code_name'] == keyword]
            if len(exact_name_match) > 0:
                for _, row in exact_name_match.iterrows():
                    results.append({
                        'code': row['code'],
                        'name': row['code_name'],
                        'tradeStatus': row.get('tradeStatus', 'N/A')
                    })
                return results
        
        # 模糊匹配代码
        code_matches = self.stock_list_cache[self.stock_list_cache['code'].str.contains(keyword, case=False, na=False)]
        for _, row in code_matches.iterrows():
            results.append({
                'code': row['code'],
                'name': row.get('code_name', 'N/A'),
                'tradeStatus': row.get('tradeStatus', 'N/A')
            })
        
        # 模糊匹配名称
        if 'code_name' in self.stock_list_cache.columns:
            name_matches = self.stock_list_cache[self.stock_list_cache['code_name'].str.contains(keyword, na=False)]
            for _, row in name_matches.iterrows():
                if not any(r['code'] == row['code'] for r in results):
                    results.append({
                        'code': row['code'],
                        'name': row['code_name'],
                        'tradeStatus': row.get('tradeStatus', 'N/A')
                    })
        
        return results[:20]
    
    def get_stock_code(self, input_str: str) -> Optional[str]:
        """
        获取股票代码（支持自动解析名称或代码）
        
        Args:
            input_str: 输入的股票名称或代码
            
        Returns:
            股票代码或None
        """
        results = self.search_stock(input_str)
        
        if len(results) == 0:
            print(f"✗ 未找到匹配 '{input_str}' 的股票")
            return None
        elif len(results) == 1:
            print(f"✓ 找到股票: {results[0]['name']} ({results[0]['code']})")
            return results[0]['code']
        else:
            print(f"\n找到 {len(results)} 只匹配股票：")
            for i, r in enumerate(results[:10], 1):
                status = "正常" if r.get('tradeStatus') == '1' else "停牌"
                print(f"  {i}. {r['name']} ({r['code']}) [{status}]")
            
            print("请通过analyze()方法直接传入确定的代码，或传入唯一匹配的名称")
            return None
    
    def get_historical_valuation(self, stock_code: str, years: int = 10) -> pd.DataFrame:
        """
        获取历史估值数据（包含PE、PB）
        
        Args:
            stock_code: 股票代码（BaoStock格式: sh.600000或sz.000001）
            years: 获取几年的数据（默认10年）
            
        Returns:
            包含日期、PE、PB的DataFrame
        """
        print(f"\n正在获取 {stock_code} 过去{years}年的历史估值数据...")
        
        if self.lg is None or self.lg.error_code != '0':
            print("  检测到未登录，正在重新登录...")
            self._login()
        
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=years * 365 + 100)
            
            start_str = start_date.strftime("%Y-%m-%d")
            end_str = end_date.strftime("%Y-%m-%d")
            
            rs = bs.query_history_k_data_plus(
                stock_code,
                "date,peTTM,pbMRQ,psTTM,pcfNcfTTM",
                start_date=start_str,
                end_date=end_str,
                frequency="d",
                adjustflag="3"
            )
            
            if rs.error_code != '0':
                if '未登录' in rs.error_msg or 'login' in rs.error_msg.lower():
                    print(f"  ! 登录状态失效，正在重新登录...")
                    self._login()
                    rs = bs.query_history_k_data_plus(
                        stock_code,
                        "date,peTTM,pbMRQ,psTTM,pcfNcfTTM",
                        start_date=start_str,
                        end_date=end_str,
                        frequency="d",
                        adjustflag="3"
                    )
                    if rs.error_code != '0':
                        print(f"✗ 查询失败: {rs.error_msg}")
                        return pd.DataFrame()
                else:
                    print(f"✗ 查询失败: {rs.error_msg}")
                    return pd.DataFrame()
            
            data_list = []
            while (rs.error_code == '0') & rs.next():
                data_list.append(rs.get_row_data())
            
            if len(data_list) == 0:
                print(f"✗ 未获取到数据")
                return pd.DataFrame()
            
            result = pd.DataFrame(data_list, columns=rs.fields)
            
            result['date'] = pd.to_datetime(result['date'])
            result['peTTM'] = pd.to_numeric(result['peTTM'], errors='coerce')
            result['pbMRQ'] = pd.to_numeric(result['pbMRQ'], errors='coerce')
            result['psTTM'] = pd.to_numeric(result['psTTM'], errors='coerce')
            result['pcfNcfTTM'] = pd.to_numeric(result['pcfNcfTTM'], errors='coerce')
            
            result = result[(result['peTTM'] > 0) | (result['pbMRQ'] > 0)]
            
            print(f"  ✓ 获取到 {len(result)} 条历史估值数据")
            
            return result
            
        except Exception as e:
            print(f"✗ 获取历史估值数据失败: {e}")
            import traceback
            traceback.print_exc()
            return pd.DataFrame()
    
    def calculate_percentiles(self, df: pd.DataFrame) -> Dict:
        """
        计算PE/PB的历史水位（百分位）
        
        Args:
            df: 历史估值数据
            
        Returns:
            水位分析结果
        """
        if df is None or len(df) == 0:
            return {}
        
        df = df.copy()
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        latest = df.iloc[-1]
        current_pe = latest['peTTM'] if 'peTTM' in latest else np.nan
        current_pb = latest['pbMRQ'] if 'pbMRQ' in latest else np.nan
        
        result = {
            'current_pe': current_pe,
            'current_pb': current_pb,
            'periods': {}
        }
        
        periods = {
            '10年': 3650,
            '5年': 1825,
            '3年': 1095,
            '1年': 365
        }
        
        end_date = df['date'].max()
        
        for period_name, days in periods.items():
            start_date = end_date - timedelta(days=days)
            period_df = df[df['date'] >= start_date]
            
            if len(period_df) < 30:
                continue
            
            pe_values = period_df['peTTM'].dropna()
            pb_values = period_df['pbMRQ'].dropna()
            
            pe_values = pe_values[pe_values < 1000]
            pb_values = pb_values[pb_values < 100]
            
            pe_stats = self._calc_stats(pe_values, current_pe)
            pb_stats = self._calc_stats(pb_values, current_pb)
            
            result['periods'][period_name] = {
                'data_points': len(period_df),
                'pe': pe_stats,
                'pb': pb_stats
            }
        
        return result
    
    def _calc_stats(self, values: pd.Series, current: float) -> Dict:
        """计算统计指标"""
        if len(values) == 0:
            return {
                'current': current,
                'percentile': np.nan,
                'min': np.nan,
                'max': np.nan,
                'median': np.nan,
                'mean': np.nan,
                'std': np.nan
            }
        
        return {
            'current': current,
            'percentile': (values < current).mean() * 100 if not pd.isna(current) else np.nan,
            'min': values.min(),
            'max': values.max(),
            'median': values.median(),
            'mean': values.mean(),
            'std': values.std()
        }
    
    def analyze(self, stock_input: str, years: int = 10) -> Optional[Dict]:
        """
        分析单只股票的PE/PB历史水位
        
        Args:
            stock_input: 股票名称或代码
            years: 分析历史年数
            
        Returns:
            分析结果字典
        """
        print("=" * 80)
        print(f"股票PE/PB历史水位分析")
        print("=" * 80)
        
        stock_code = self.get_stock_code(stock_input)
        if stock_code is None:
            return None
        
        hist_data = self.get_historical_valuation(stock_code, years)
        
        if len(hist_data) == 0:
            print(f"\n✗ 无法获取 {stock_code} 的历史估值数据")
            return None
        
        percentiles = self.calculate_percentiles(hist_data)
        
        stock_info = self.stock_list_cache[self.stock_list_cache['code'] == stock_code]
        stock_name = stock_info.iloc[0].get('code_name', 'Unknown') if len(stock_info) > 0 else 'Unknown'
        
        result = {
            'code': stock_code,
            'name': stock_name,
            'current_pe': percentiles.get('current_pe', np.nan),
            'current_pb': percentiles.get('current_pb', np.nan),
            'historical_data': hist_data,
            'percentiles': percentiles
        }
        
        return result
    
    def print_report(self, result: Dict):
        """
        打印分析报告
        
        Args:
            result: 分析结果字典
        """
        if result is None:
            print("\n✗ 分析失败，无法生成报告")
            return
        
        print("\n" + "=" * 80)
        print(f"📊 {result['name']} ({result['code']}) PE/PB历史水位分析报告")
        print("=" * 80)
        
        pe_str = f"{result['current_pe']:.2f}" if not pd.isna(result['current_pe']) else "N/A"
        pb_str = f"{result['current_pb']:.2f}" if not pd.isna(result['current_pb']) else "N/A"
        print(f"\n📈 当前估值指标:")
        print(f"   PE (TTM): {pe_str}")
        print(f"   PB (MRQ): {pb_str}")
        
        percentiles = result.get('percentiles', {})
        periods = percentiles.get('periods', {})
        
        if len(periods) == 0:
            print("\n⚠️ 历史估值数据不足，无法计算水位")
            return
        
        print(f"\n📉 历史水位分析（基于历史估值数据）:")
        print("-" * 80)
        print(f"{'周期':<10} {'数据点':<10} {'PE当前':<12} {'PE水位':<20} {'PB当前':<12} {'PB水位':<20}")
        print("-" * 80)
        
        for period_name in ['10年', '5年', '3年', '1年']:
            if period_name in periods:
                p = periods[period_name]
                data_points = p.get('data_points', 0)
                
                pe_current = p['pe'].get('current', np.nan)
                pe_percentile = p['pe'].get('percentile', np.nan)
                pb_current = p['pb'].get('current', np.nan)
                pb_percentile = p['pb'].get('percentile', np.nan)
                
                pe_curr_str = f"{pe_current:.2f}" if not pd.isna(pe_current) else "N/A"
                pe_pct_str = f"{pe_percentile:.1f}%" if not pd.isna(pe_percentile) else "N/A"
                pb_curr_str = f"{pb_current:.2f}" if not pd.isna(pb_current) else "N/A"
                pb_pct_str = f"{pb_percentile:.1f}%" if not pd.isna(pb_percentile) else "N/A"
                
                if not pd.isna(pe_percentile):
                    if pe_percentile < 20:
                        pe_pct_str += " 🟢低估"
                    elif pe_percentile < 50:
                        pe_pct_str += " 🟡适中"
                    else:
                        pe_pct_str += " 🔴偏高"
                
                if not pd.isna(pb_percentile):
                    if pb_percentile < 20:
                        pb_pct_str += " 🟢低估"
                    elif pb_percentile < 50:
                        pb_pct_str += " 🟡适中"
                    else:
                        pb_pct_str += " 🔴偏高"
                
                print(f"{period_name:<10} {data_points:<10} {pe_curr_str:<12} {pe_pct_str:<20} {pb_curr_str:<12} {pb_pct_str:<20}")
        
        print("-" * 80)
        print("水位说明: 🟢低估(0-20%) | 🟡适中(20-50%) | 🔴偏高(>50%)")
        
        print(f"\n📊 详细统计指标:")
        for period_name in ['10年', '5年', '3年']:
            if period_name in periods:
                p = periods[period_name]
                print(f"\n   【{period_name}】")
                
                pe_stats = p['pe']
                if not pd.isna(pe_stats.get('min', np.nan)):
                    print(f"   PE - 最低: {pe_stats['min']:.2f}, 最高: {pe_stats['max']:.2f}, "
                          f"中位数: {pe_stats['median']:.2f}, 平均: {pe_stats['mean']:.2f}")
                
                pb_stats = p['pb']
                if not pd.isna(pb_stats.get('min', np.nan)):
                    print(f"   PB - 最低: {pb_stats['min']:.2f}, 最高: {pb_stats['max']:.2f}, "
                          f"中位数: {pb_stats['median']:.2f}, 平均: {pb_stats['mean']:.2f}")
        
        print(f"\n💡 参考建议:")
        
        latest_period = None
        for p in ['1年', '3年', '5年', '10年']:
            if p in periods:
                latest_period = periods[p]
                break
        
        if latest_period:
            pe_pct = latest_period['pe'].get('percentile', np.nan)
            pb_pct = latest_period['pb'].get('percentile', np.nan)
            
            if not pd.isna(pe_pct) and not pd.isna(pb_pct):
                avg_percentile = (pe_pct + pb_pct) / 2
                
                print(f"\n   基于PE/PB综合水位分析:")
                
                if avg_percentile < 20:
                    print(f"   • 当前PE/PB综合水位为 {avg_percentile:.1f}%，处于历史较低水平")
                    print(f"   • 从估值角度看，可能存在估值修复机会，建议关注")
                elif avg_percentile < 40:
                    print(f"   • 当前PE/PB综合水位为 {avg_percentile:.1f}%，处于历史偏低水平")
                    print(f"   • 估值相对合理，可适当关注")
                elif avg_percentile < 60:
                    print(f"   • 当前PE/PB综合水位为 {avg_percentile:.1f}%，处于历史中等水平")
                    print(f"   • 估值相对合理")
                elif avg_percentile < 80:
                    print(f"   • 当前PE/PB综合水位为 {avg_percentile:.1f}%，处于历史偏高水平")
                    print(f"   • 估值偏高，建议谨慎")
                else:
                    print(f"   • 当前PE/PB综合水位为 {avg_percentile:.1f}%，处于历史较高水平")
                    print(f"   • 估值较高，需注意估值回调风险")
                
                print(f"\n   分项分析:")
                if not pd.isna(pe_pct):
                    if pe_pct < 20:
                        print(f"   • PE水位{pe_pct:.1f}%：市盈率处于历史低位")
                    elif pe_pct > 80:
                        print(f"   • PE水位{pe_pct:.1f}%：市盈率处于历史高位，关注盈利增长能否支撑")
                
                if not pd.isna(pb_pct):
                    if pb_pct < 20:
                        print(f"   • PB水位{pb_pct:.1f}%：市净率处于历史低位")
                    elif pb_pct > 80:
                        print(f"   • PB水位{pb_pct:.1f}%：市净率处于历史高位")
        
        print("\n" + "=" * 80)
        print("⚠️ 免责声明：本分析仅供参考，不构成投资建议。投资有风险，入市需谨慎。")
        print("=" * 80)
    
    def save_to_csv(self, result: Dict, filename: Optional[str] = None):
        """
        保存分析结果到CSV
        
        Args:
            result: 分析结果字典
            filename: 文件名（可选）
        """
        if result is None:
            return
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            code_clean = result['code'].replace('.', '_')
            filename = f"pe_pb_analysis_{code_clean}_{timestamp}.csv"
        
        hist_df = result.get('historical_data')
        if hist_df is not None and len(hist_df) > 0:
            hist_df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"\n💾 历史估值数据已保存: {filename}")
            
            summary_file = filename.replace('.csv', '_summary.txt')
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write(f"股票PE/PB历史水位分析报告\n")
                f.write(f"=" * 80 + "\n")
                f.write(f"股票名称: {result['name']}\n")
                f.write(f"股票代码: {result['code']}\n")
                f.write(f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(f"当前PE: {result.get('current_pe', 'N/A')}\n")
                f.write(f"当前PB: {result.get('current_pb', 'N/A')}\n\n")
                
                percentiles = result.get('percentiles', {}).get('periods', {})
                for period_name in ['10年', '5年', '3年', '1年']:
                    if period_name in percentiles:
                        p = percentiles[period_name]
                        f.write(f"\n【{period_name}】\n")
                        f.write(f"  PE水位: {p['pe'].get('percentile', 'N/A')}\n")
                        f.write(f"  PB水位: {p['pb'].get('percentile', 'N/A')}\n")
            
            print(f"💾 分析摘要已保存: {summary_file}")


def main():
    """主函数 - 命令行入口"""
    if len(sys.argv) < 2:
        print("用法: python analyze_stock.py <股票名称或代码>")
        print("示例: python analyze_stock.py 贵州茅台")
        print("      python analyze_stock.py 600519")
        sys.exit(1)
    
    stock_input = sys.argv[1]
    analyzer = None
    
    try:
        analyzer = StockPEPBAnalyzer()
        result = analyzer.analyze(stock_input, years=10)
        analyzer.print_report(result)
    except Exception as e:
        print(f"✗ 发生错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if analyzer:
            analyzer._logout()


if __name__ == "__main__":
    main()
