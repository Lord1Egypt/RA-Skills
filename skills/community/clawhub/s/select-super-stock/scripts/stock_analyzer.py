#!/home/linuxbrew/.linuxbrew/bin/python3.10
# -*- coding: utf-8 -*-
"""
优质股票筛选专家 - 主分析脚本 (v1.3)
基于双核心模型：长线稳步上涨型 + 历史低位反弹型
数据源：强制使用 AKShare + 缓存机制

缓存策略：
- 交易时间：使用 AKShare 获取实时数据
- 非交易时间：使用缓存数据（有效期 24 小时）
"""

import sys
import os
import json
import argparse
import time
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple

import pandas as pd

# 导入缓存工具
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '_shared'))
try:
    from cache_utils import StockDataCache
    HAS_CACHE = True
except ImportError:
    HAS_CACHE = False
    print("⚠️ 缓存模块未找到，将禁用缓存功能")

try:
    import akshare as ak
    HAS_AKSHARE = True
except ImportError:
    HAS_AKSHARE = False
    print("❌ AKShare 未安装，请运行：pip3 install akshare pandas -U")


# 初始化缓存
SCRIPT_DIR = os.path.dirname(__file__)
CACHE_DIR = os.path.join(SCRIPT_DIR, '..', '.cache')
cache = StockDataCache(CACHE_DIR, cache_max_age_hours=24) if HAS_CACHE else None


@dataclass
class StockSignal:
    """股票信号"""
    symbol: str
    name: str
    category: str  # 长线稳步上涨型 / 历史低位反弹型 / 垃圾股规避 / 观察区
    score: int  # 0-100
    similar_stock: str  # 相似标的参考
    technical_analysis: Dict = field(default_factory=dict)
    fundamental_analysis: Dict = field(default_factory=dict)
    recommendation: str = ""
    strategy: str = ""
    risks: List[str] = field(default_factory=list)


def get_stock_name(symbol: str) -> str:
    """获取股票名称（仅使用 AKShare）"""
    if HAS_AKSHARE:
        try:
            stock_info = ak.stock_individual_info_em(symbol=symbol)
            if stock_info is not None and len(stock_info) > 0:
                for _, row in stock_info.iterrows():
                    if '股票简称' in str(row.get('item', '')):
                        return row.get('value', symbol)
        except Exception:
            pass
    return symbol


def fetch_kline_data(symbol: str, period: str = "daily", count: int = 500, max_retries: int = 3) -> pd.DataFrame:
    """
    获取 K 线数据（仅使用 AKShare，带重试机制）
    
    ⚠️ 强制使用 AKShare 数据源，确保数据准确性
    如果 AKShare 失败，不会 fallback 到其他数据源
    
    Args:
        symbol: 股票代码
        period: daily/weekly/monthly
        count: 数据条数
        max_retries: 最大重试次数
    
    Returns:
        DataFrame with columns: date, open, high, low, close, volume
    """
    df = pd.DataFrame()
    
    if not HAS_AKSHARE:
        print("  ❌ 错误：AKShare 未安装，无法获取数据")
        print("  请运行：pip3 install akshare pandas -U")
        return pd.DataFrame()
    
    # 仅使用 AKShare，带重试机制
    for attempt in range(1, max_retries + 1):
        try:
            if attempt > 1:
                import time
                wait_time = 2 ** (attempt - 1)  # 指数退避：2s, 4s, 8s
                print(f"  ⏳ 等待 {wait_time} 秒后重试 (第 {attempt}/{max_retries} 次)...")
                time.sleep(wait_time)
            else:
                print(f"  [AKShare] 获取数据中... (第 {attempt}/{max_retries} 次尝试)")
            
            df = ak.stock_zh_a_hist(symbol=symbol, period=period, adjust="qfq")
            
            if df is not None and len(df) > 0:
                print(f"  ✓ AKShare 成功获取 {len(df)} 条数据")
                df = df.tail(count)
                # 适配 AKShare 列名
                expected_cols = ['date', 'open', 'close', 'high', 'low', 'volume', 
                                'turnover', 'amplitude', 'pct_change', 'change', 'turnover_rate']
                if len(df.columns) == len(expected_cols):
                    df.columns = expected_cols
                elif len(df.columns) == 12:
                    # 某些版本多一列，跳过最后一列
                    df = df.iloc[:, :11]
                    df.columns = expected_cols
                else:
                    print(f"  ⚠️ 列数不匹配：期望 {len(expected_cols)} 列，实际 {len(df.columns)} 列")
                    print(f"  实际列名：{df.columns.tolist()}")
                    # 尝试按位置映射
                    if len(df.columns) >= 6:
                        df = df.rename(columns={
                            df.columns[0]: 'date',
                            df.columns[1]: 'open',
                            df.columns[2]: 'close',
                            df.columns[3]: 'high',
                            df.columns[4]: 'low',
                            df.columns[5]: 'volume'
                        })
                return df.reset_index(drop=True)
            else:
                print(f"  ⚠️ AKShare 返回空数据")
        except Exception as e:
            print(f"  ⚠️ AKShare 尝试 {attempt}/{max_retries} 失败：{e}")
            if attempt == max_retries:
                print(f"  ❌ AKShare 所有重试均失败，请检查网络连接或稍后再试")
                return pd.DataFrame()
    
    print(f"  ❌ AKShare 数据获取失败")
    return pd.DataFrame()


def calculate_ma(prices: pd.Series, periods: List[int] = [5, 10, 20, 60, 120, 250]) -> Dict[str, pd.Series]:
    """计算均线"""
    mas = {}
    for period in periods:
        mas[f'MA{period}'] = prices.rolling(window=period).mean()
    return mas


def calculate_macd(prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Dict:
    """计算 MACD"""
    ema_fast = prices.ewm(span=fast, adjust=False).mean()
    ema_slow = prices.ewm(span=slow, adjust=False).mean()
    dif = ema_fast - ema_slow
    dea = dif.ewm(span=signal, adjust=False).mean()
    macd = (dif - dea) * 2
    
    return {
        'DIF': dif,
        'DEA': dea,
        'MACD': macd
    }


def calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
    """计算 RSI"""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def check_model_a(df: pd.DataFrame, mas: Dict) -> Tuple[bool, int]:
    """
    检查是否符合模型 A：长线稳步上涨型
    
    Returns:
        (是否符合，评分)
    """
    if len(df) < 250:
        return False, 0
    
    score = 0
    current_price = df['close'].iloc[-1]
    
    # 1. 年线多头排列 (250 日均线向上)
    ma250_current = mas['MA250'].iloc[-1]
    ma250_prev = mas['MA250'].iloc[-30] if len(mas['MA250']) > 30 else ma250_current
    
    if current_price > ma250_current:
        score += 20  # 股价在年线上方
    
    if ma250_current > ma250_prev:
        score += 15  # 年线向上
    
    # 2. 均线多头排列
    ma_order = [
        mas['MA5'].iloc[-1],
        mas['MA10'].iloc[-1],
        mas['MA20'].iloc[-1],
        mas['MA60'].iloc[-1],
        mas['MA120'].iloc[-1],
        mas['MA250'].iloc[-1]
    ]
    
    if all(ma_order[i] >= ma_order[i+1] for i in range(len(ma_order)-1)):
        score += 25  # 完美多头排列
    
    # 3. MACD 零轴上方
    macd = calculate_macd(df['close'])
    if macd['DIF'].iloc[-1] > 0:
        score += 20  # DIF 在零轴上方
    
    # 4. 温和上涨（非暴涨）
    price_change_60d = (df['close'].iloc[-1] / df['close'].iloc[-60] - 1) * 100 if len(df) > 60 else 0
    if 5 < price_change_60d < 50:
        score += 20  # 60 日涨幅在 5%-50% 之间，稳步上涨
    
    return score >= 60, score


def check_model_b(df: pd.DataFrame, mas: Dict) -> Tuple[bool, int]:
    """
    检查是否符合模型 B：历史低位反弹型
    
    Returns:
        (是否符合，评分)
    """
    if len(df) < 250:
        return False, 0
    
    score = 0
    current_price = df['close'].iloc[-1]
    
    # 1. 距离历史高点大幅回撤
    high_52w = df['high'].max()
    drawdown = (high_52w - current_price) / high_52w * 100
    
    if drawdown > 50:
        score += 30  # 回撤超过 50%
    elif drawdown > 30:
        score += 20  # 回撤超过 30%
    
    # 2. 底部企稳信号
    low_60d = df['low'].iloc[-60:].min() if len(df) > 60 else current_price
    if current_price > low_60d * 1.05:
        score += 20  # 从最低点反弹超过 5%
    
    # 3. MACD 底背离
    macd = calculate_macd(df['close'])
    macd_recent = macd['MACD'].iloc[-10:].mean()
    macd_prev = macd['MACD'].iloc[-30:-20].mean() if len(macd['MACD']) > 30 else macd_recent
    
    if macd_recent > macd_prev and macd_recent < 0:
        score += 25  # MACD 底背离
    
    # 4. 温和放量
    volume_recent = df['volume'].iloc[-10:].mean()
    volume_prev = df['volume'].iloc[-30:-10].mean() if len(df) > 30 else volume_recent
    
    if volume_recent > volume_prev * 1.2:
        score += 15  # 温和放量
    
    # 5. 股价在底部区域
    if current_price < df['high'].max() * 0.6:
        score += 10  # 处于历史低位
    
    return score >= 50, score


def check_blacklist(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """
    检查是否属于黑名单股票（垃圾股）
    
    Returns:
        (是否规避，原因列表)
    """
    reasons = []
    
    if len(df) < 60:
        return False, []
    
    current_price = df['close'].iloc[-1]
    
    # 1. 暴涨暴跌
    price_changes = df['pct_change'].iloc[-30:] if 'pct_change' in df.columns else pd.Series()
    if len(price_changes) > 0:
        extreme_days = (price_changes.abs() > 9).sum()
        if extreme_days >= 3:
            reasons.append("近期多次出现涨跌停，波动极端")
    
    # 2. 高位巨量换手
    turnover_rate = df['turnover_rate'].iloc[-1] if 'turnover_rate' in df.columns else 0
    if turnover_rate > 20:
        reasons.append(f"单日换手率过高 ({turnover_rate:.1f}%)，警惕出货")
    
    # 3. 长上影线/下影线频繁
    recent_klines = df.tail(20)
    long_shadow_days = 0
    for _, row in recent_klines.iterrows():
        upper_shadow = (row['high'] - max(row['open'], row['close'])) / row['close']
        lower_shadow = (min(row['open'], row['close']) - row['low']) / row['close']
        if upper_shadow > 0.05 or lower_shadow > 0.05:
            long_shadow_days += 1
    
    if long_shadow_days >= 8:
        reasons.append("K 线频繁出现长影线，走势不连贯")
    
    # 4. 织布机走势（横盘震荡）
    price_range = (df['high'].iloc[-30:].max() - df['low'].iloc[-30:].min()) / df['close'].iloc[-30] * 100
    if price_range < 10:
        reasons.append("长期横盘震荡，疑似庄家控盘")
    
    return len(reasons) >= 2, reasons


def get_fundamental_data(symbol: str) -> Dict:
    """获取基本面数据"""
    data = {
        'pe_ratio': None,
        'pb_ratio': None,
        'roe': None,
        'dividend_yield': None,
        'market_cap': None,
        'revenue_growth': None,
        'profit_growth': None
    }
    
    try:
        # 获取个股信息
        info = ak.stock_individual_info_em(symbol=symbol)
        if info is not None:
            for _, row in info.iterrows():
                if '市盈率' in str(row['item']):
                    try:
                        data['pe_ratio'] = float(row['value'])
                    except:
                        pass
                elif '市净率' in str(row['item']):
                    try:
                        data['pb_ratio'] = float(row['value'])
                    except:
                        pass
                elif '总市值' in str(row['item']):
                    try:
                        data['market_cap'] = row['value']
                    except:
                        pass
    except Exception:
        pass
    
    return data


def analyze_stock(symbol: str, full: bool = False) -> StockSignal:
    """
    分析股票
    
    ⚠️ 强制使用 AKShare 数据源，确保数据准确性
    
    Args:
        symbol: 股票代码
        full: 是否完整分析
    
    Returns:
        StockSignal
    """
    # 获取股票名称
    name = get_stock_name(symbol)
    
    # 获取 K 线数据（仅 AKShare，带重试）
    print(f"\n🔍 开始分析股票：{symbol}")
    print("=" * 50)
    df_daily = fetch_kline_data(symbol, period="daily", count=500, max_retries=3)
    df_weekly = fetch_kline_data(symbol, period="weekly", count=200, max_retries=2) if full else pd.DataFrame()
    df_monthly = fetch_kline_data(symbol, period="monthly", count=100, max_retries=2) if full else pd.DataFrame()
    
    # ⚠️ 如果 AKShare 数据获取失败，直接返回错误，不使用备用数据
    if df_daily.empty:
        return StockSignal(
            symbol=symbol,
            name=name,
            category="数据获取失败",
            score=0,
            similar_stock="N/A",
            recommendation="❌ AKShare 数据源连接失败，请检查网络后重试",
            strategy="建议：1) 检查网络连接 2) 稍后再试 3) 不要使用其他数据源替代",
            risks=["数据源不可用", "网络问题", "API 限流"]
        )
    
    # 计算技术指标
    mas = calculate_ma(df_daily['close'])
    macd = calculate_macd(df_daily['close'])
    rsi = calculate_rsi(df_daily['close'])
    
    # 模型判断
    is_model_a, score_a = check_model_a(df_daily, mas)
    is_model_b, score_b = check_model_b(df_daily, mas)
    is_blacklist, blacklist_reasons = check_blacklist(df_daily)
    
    # 确定分类
    if is_blacklist:
        category = "垃圾股规避"
        similar_stock = "类似中远海发"
        score = 0
    elif is_model_a:
        category = "长线稳步上涨型"
        similar_stock = "类似中国海油"
        score = min(score_a, 100)
    elif is_model_b:
        category = "历史低位反弹型"
        similar_stock = "类似万华化学"
        score = min(score_b, 100)
    else:
        category = "观察区"
        similar_stock = "N/A"
        score = max(score_a, score_b)
    
    # 技术面分析
    current_price = df_daily['close'].iloc[-1]
    technical_analysis = {
        'current_price': current_price,
        'ma250': mas['MA250'].iloc[-1] if len(mas['MA250']) > 0 else None,
        'ma60': mas['MA60'].iloc[-1] if len(mas['MA60']) > 0 else None,
        'macd_dif': macd['DIF'].iloc[-1],
        'rsi': rsi.iloc[-1],
        'price_change_60d': (current_price / df_daily['close'].iloc[-60] - 1) * 100 if len(df_daily) > 60 else 0
    }
    
    # 基本面分析
    fundamental = get_fundamental_data(symbol)
    
    # 生成建议
    if category == "长线稳步上涨型":
        recommendation = "适合中长期布局"
        strategy = f"建议分批建仓，依托{mas['MA250'].iloc[-1]:.2f}元（年线）作为防守位"
        risks = ["警惕短期涨幅过大回调", "关注行业政策变化"]
    elif category == "历史低位反弹型":
        recommendation = "处于建仓击球区"
        strategy = "可逐步建仓，关注右侧信号确认"
        risks = ["行业周期可能继续下行", "需耐心等待反转信号"]
    elif category == "垃圾股规避":
        recommendation = "坚决规避空仓"
        strategy = "不建议参与，风险极高"
        risks = blacklist_reasons
    else:
        recommendation = "等待右侧信号"
        strategy = "继续观察，等待更明确的信号"
        risks = ["方向不明确", "建议等待"]
    
    return StockSignal(
        symbol=symbol,
        name=name,
        category=category,
        score=score,
        similar_stock=similar_stock,
        technical_analysis=technical_analysis,
        fundamental_analysis=fundamental,
        recommendation=recommendation,
        strategy=strategy,
        risks=risks
    )


def format_output(signal: StockSignal) -> str:
    """格式化输出"""
    ta = signal.technical_analysis
    
    def safe_float(val, decimals=2):
        """安全格式化浮点数"""
        if val is None:
            return "N/A"
        try:
            return f"{float(val):.{decimals}f}"
        except:
            return str(val)
    
    output = f"""
### 📊 股票名称/代码：[{signal.name}({signal.symbol})]

**1. 资产定性分析**
* **分类归属**：{signal.category}
* **相似标的参考**：{signal.similar_stock}
* **综合评分**：{signal.score}/100

**2. 技术面解析 (Technical)**
* **当前价格**：{safe_float(ta.get('current_price'))}元
* **年线 (MA250)**：{safe_float(ta.get('ma250'))}元
* **60 日均线**：{safe_float(ta.get('ma60'))}元
* **MACD-DIF**：{safe_float(ta.get('macd_dif'), 4)}
* **RSI(14)**：{safe_float(ta.get('rsi'))}
* **60 日涨幅**：{safe_float(ta.get('price_change_60d', 0))}%

**3. 基本面与消息面 (Fundamental & News)**
* **市盈率 (PE)**：{signal.fundamental_analysis.get('pe_ratio', 'N/A')}
* **市净率 (PB)**：{signal.fundamental_analysis.get('pb_ratio', 'N/A')}
* **总市值**：{signal.fundamental_analysis.get('market_cap', 'N/A')}

**4. 综合投资建议 (Actionable Advice)**
* **结论**：{signal.recommendation}
* **操作策略**：{signal.strategy}
* **风险提示**：{"; ".join(signal.risks) if signal.risks else "无明显风险"}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ 风险提示：本分析仅供参考，不构成投资建议。股市有风险，入市需谨慎。
"""
    return output


def main():
    parser = argparse.ArgumentParser(description='优质股票筛选专家')
    parser.add_argument('--symbol', required=True, help='股票代码')
    parser.add_argument('--full', action='store_true', help='完整分析（包含周线/月线）')
    parser.add_argument('--json', action='store_true', help='JSON 格式输出')
    
    args = parser.parse_args()
    
    if not HAS_AKSHARE:
        print("⚠️ 未安装 AKShare，使用备用数据源（东方财富/新浪财经）...")
        # 继续执行，使用 HTTP API 数据源
    
    # 分析股票
    signal = analyze_stock(args.symbol, full=args.full)
    
    # 输出结果
    if args.json:
        print(json.dumps({
            'symbol': signal.symbol,
            'name': signal.name,
            'category': signal.category,
            'score': signal.score,
            'similar_stock': signal.similar_stock,
            'recommendation': signal.recommendation,
            'strategy': signal.strategy,
            'risks': signal.risks
        }, ensure_ascii=False, indent=2))
    else:
        print(format_output(signal))


if __name__ == '__main__':
    main()
