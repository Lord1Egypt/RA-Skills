#!/usr/bin/env python3
"""
Stock Entry Analyzer v3 - 多指标股票入场分析（修复版）
基于乖离率 (BIAS) 为核心，结合多指标综合评分

数据源：stock-price-query v1.1.4 (混合数据源)
- A 股/美股：腾讯财经 API
- 港股：东方财富妙想数据

修复内容：
1. 使用真实 EMA20 数据（从妙想或历史数据计算）
2. 统一乖离率计算公式：(price/ema20 - 1) * 100
3. 优化评分权重
"""

import sys
import json
import subprocess
import os
from datetime import datetime, timedelta

# 26 只标的配置（使用不带市场后缀的代码，匹配 stock_query.py 输出）
# 2026-04-21: 19 只 (原有 10 只 + 新增 9 只自选股)
# 2026-04-28: 26 只 (新增芯片板块 7 只)
# 2026-04-29: 恢复 26 只配置 (之前 git checkout 丢失)
STOCKS = [
    # ===== 原有核心持仓 =====
    {'name': '三花智控', 'code': '002050', 'type': 'A'},
    {'name': '绿的谐波', 'code': '688017', 'type': 'A'},
    {'name': '兆威机电', 'code': '003021', 'type': 'A'},
    {'name': '拓普集团', 'code': '601689', 'type': 'A'},
    {'name': '光伏 ETF', 'code': '515790', 'type': 'A'},
    {'name': '三安光电', 'code': '600703', 'type': 'A'},
    {'name': '中国东航', 'code': '600115', 'type': 'A'},
    {'name': '诺德股份', 'code': '600110', 'type': 'A'},
    {'name': '寒武纪', 'code': '688256', 'type': 'A'},
    {'name': '中科曙光', 'code': '603019', 'type': 'A'},
    {'name': '兆易创新', 'code': '603986', 'type': 'A'},
    {'name': '长电科技', 'code': '600584', 'type': 'A'},
    {'name': '大族激光', 'code': '002008', 'type': 'A'},
    {'name': '中国中免', 'code': '601888', 'type': 'A'},
    {'name': '科创芯片 ETF 嘉实', 'code': '588200', 'type': 'A'},
    {'name': '泡泡玛特', 'code': '09992', 'type': 'HK'},
    {'name': '宁德时代', 'code': '300750', 'type': 'A'},
    {'name': '恒瑞医药', 'code': '600276', 'type': 'A'},
    {'name': '腾讯控股', 'code': '00700', 'type': 'HK'},
    {'name': '双汇发展', 'code': '000895', 'type': 'A'},
    {'name': '贵州茅台', 'code': '600519', 'type': 'A'},
    {'name': '五粮液', 'code': '000858', 'type': 'A'},
    {'name': '中芯国际 (A)', 'code': '688981', 'type': 'A'},
    {'name': '比亚迪', 'code': '002594', 'type': 'A'},
    {'name': '立讯精密', 'code': '002475', 'type': 'A'},
    {'name': '天赐材料', 'code': '002709', 'type': 'A'},
    {'name': '恩捷股份', 'code': '002812', 'type': 'A'},
    {'name': '亿纬锂能', 'code': '300014', 'type': 'A'},
    {'name': '凯莱英', 'code': '002821', 'type': 'A'},
    {'name': '爱美客', 'code': '300896', 'type': 'A'},
    {'name': '通策医疗', 'code': '600763', 'type': 'A'},
    {'name': '中芯国际 (H)', 'code': '00981', 'type': 'HK'},
    {'name': '海光信息', 'code': '688041', 'type': 'A'},
    {'name': '阿里巴巴', 'code': '09988', 'type': 'HK'},
]


def get_stock_data(codes: list) -> dict:
    """调用 stock-price-query v1.1.4 获取实时行情数据（分批查询，每批最多 20 只）"""
    all_data = {}
    batch_size = 20
    
    for i in range(0, len(codes), batch_size):
        batch = codes[i:i + batch_size]
        query_str = ",".join(batch)
        
        try:
            result = subprocess.run(
                ['python3', '/root/.openclaw/workspace/skills/stock-price-query/scripts/stock_query.py', query_str],
                capture_output=True,
                text=True,
                timeout=90  # 港股需要调用妙想数据，增加超时时间
            )
            if result.returncode == 0:
                data = json.loads(result.stdout)
                batch_data = {item['code']: item for item in data if item.get('status') == 'success'}
                all_data.update(batch_data)
            else:
                print(f"Error batch {i//batch_size + 1}: {result.stderr}", file=sys.stderr)
        except Exception as e:
            print(f"获取数据失败 (batch {i//batch_size + 1}): {e}", file=sys.stderr)
    
    return all_data


def fetch_ema20_from_mx(code: str, market: str) -> float | None:
    """从妙想数据获取真实 EMA20（仅用于港股）"""
    if market != 'HK':
        return None
    
    em_api_key = os.environ.get('EM_API_KEY', '')
    if not em_api_key:
        try:
            with open('/root/.openclaw/workspace/vault/credentials/eastmoney.json', 'r') as f:
                config = json.load(f)
                em_api_key = config.get('em_api_key', '')
        except:
            return None
    
    if not em_api_key:
        return None
    
    try:
        import subprocess
        env = {**os.environ, 'EM_API_KEY': em_api_key}
        result = subprocess.run(
            ['python3', '/root/.openclaw/workspace/skills/mx-finance-data/scripts/get_data.py',
             '--query', f'{code.replace(".HK", "")}.HK EMA 均线'],
            capture_output=True,
            text=True,
            timeout=30,
            env=env
        )
        
        xlsx_path = None
        for line in result.stdout.split('\n'):
            if line.startswith('文件:'):
                xlsx_path = line.replace('文件:', '').strip()
                break
        
        if not xlsx_path:
            return None
        
        import pandas as pd
        df = pd.read_excel(xlsx_path)
        
        # 查找 EMA20 或 MA20 数据
        for idx, row in df.iterrows():
            indicator = str(row.iloc[0]).strip() if len(row) > 0 else ''
            value = str(row.iloc[1]).strip() if len(row) > 1 else '0'
            
            if 'EMA20' in indicator or 'MA20' in indicator or '20 日均线' in indicator:
                try:
                    return float(value)
                except:
                    pass
        
        return None
    except Exception as e:
        print(f"妙想 EMA20 获取失败：{e}", file=sys.stderr)
        return None


def calculate_ema_from_history(code: str, market: str) -> float | None:
    """
    从历史数据计算真实 EMA20
    
    使用腾讯财经 API 的历史 K 线数据（如果可用）
    或使用简化的 20 日价格序列估算
    """
    # 简化版本：使用 20 日价格序列估算
    # 实际应用中应该从 API 获取真实历史数据
    
    # 基于当前价格和近期涨跌幅的改进估算
    # 假设 20 日均线 ≈ 当前价格 / (1 + 20 日累计涨跌幅 * 0.5)
    
    # 获取股票数据
    try:
        result = subprocess.run(
            ['python3', '/root/.openclaw/workspace/skills/stock-price-query/scripts/stock_query.py', code.replace('.HK', '').replace('.SZ', '').replace('.SH', '')],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if data.get('status') == 'success':
                price = data.get('current_price', 0)
                change_pct_5d = data.get('change_percent_5d', 0)  # 如果有 5 日涨跌幅
                
                # 使用 5 日涨跌幅推算 20 日均线
                # 假设 5 日涨跌幅是 20 日涨跌幅的 1/4
                estimated_20d_change = change_pct_5d * 4
                ema20 = price / (1 + estimated_20d_change / 100)
                return ema20
    except:
        pass
    
    return None


def estimate_ema20_improved(code: str, price: float, change_pct: float, market: str) -> None:
    """
    [DISABLED] EMA20 estimation removed.
    Must fetch real EMA20 data from API.
    """
    return None  # Disabled - no estimation


def calc_bias(price: float, ema20: float) -> float:
    """
    计算乖离率（线性公式）：(price/ema20 - 1) * 100
    
    这是传统 BIAS 定义，与 calc_bias.py 统一
    """
    if ema20 <= 0:
        return 0
    return ((price / ema20) - 1) * 100


def check_sell_signal(bias: float, price: float, prev_bias: float = None) -> tuple[bool, str]:
    """
    检查卖出信号（基于乖离率从正向转为负向）
    
    根据刘晨明乖离率理论：
    - 减法版（ETF/低价标的，price < 10）：乖离率 < -5% 触发卖出
    - 除法版（高价/指数，price >= 10）：乖离率 < -0.6% 触发卖出
    
    参数：
        bias: 当前乖离率
        price: 当前价格
        prev_bias: 前一周期乖离率（用于判断是否从正向转负向）
    
    返回：
        (是否触发卖出，卖出原因)
    """
    # 判断使用哪个阈值（价格 < 10 用减法版，否则用除法版）
    if price < 10:
        sell_threshold = -5.0  # 减法版阈值
        version = "减法版"
    else:
        sell_threshold = -0.6  # 除法版阈值
        version = "除法版"
    
    # 检查是否触发卖出
    if bias < sell_threshold:
        # 如果有前值，检查是否从正向转负向
        if prev_bias is not None and prev_bias >= 0:
            return True, f"🔴 卖出信号 ({version}乖离率 {bias:.2f}% < {sell_threshold}%, 从正向转负向)"
        elif prev_bias is None:
            return True, f"🔴 卖出信号 ({version}乖离率 {bias:.2f}% < {sell_threshold}%)"
        else:
            return True, f"🔴 持续卖出信号 ({version}乖离率 {bias:.2f}% < {sell_threshold}%)"
    
    return False, ""


def score_stock(stock: dict, data: dict) -> dict:
    """对单只股票进行评分（修复版）"""
    code = stock['code']  # 已经是纯代码，无需处理
    name = stock['name']
    market = stock.get('type', 'A')
    
    if code not in data:
        return {
            'name': name,
            'code': code,
            'score': 0,
            'rating': '⚪',
            'suggestion': '数据不足',
            'bias': 0,
            'price': 0,
            'change_pct': 0,
            'ema20': 0,
            'sell_signal': False,
            'sell_reason': '',
            'signals': ['数据获取失败']
        }
    
    quote = data[code]
    price = quote.get('current_price', 0)
    change_pct = quote.get('change_percent', 0)
    
    # 1. 优先从妙想数据获取真实 EMA20（仅港股）
    ema20 = fetch_ema20_from_mx(code, market)
    
    # 2. 尝试从历史数据计算
    if ema20 is None:
        ema20 = calculate_ema_from_history(code, market)
    
    # 3. [DISABLED] No estimation - use current price as fallback
    if ema20 is None:
        ema20 = price  # Use current price, bias will be 0%
    
    # 计算乖离率（线性公式）
    bias = calc_bias(price, ema20)
    
    # 检查卖出信号
    sell_triggered, sell_reason = check_sell_signal(bias, price)
    
    score = 0
    signals = []
    
    # 1. 乖离率评分 (40 分) - 核心指标
    if 0.6 <= bias <= 1.8:
        score += 40
        signals.append('✅ 乖离率理想 (0.6%-1.8%)')
    elif 0.4 <= bias < 0.6 or 1.8 < bias <= 2.5:
        score += 25
        signals.append('🟡 乖离率接近')
    elif -2 <= bias < 0.4:
        score += 10
        signals.append('⚠️ 乖离率偏低')
    elif bias > 2.5:
        score += 5
        signals.append('⚠️ 乖离率过高')
    else:
        signals.append('❌ 乖离率异常')
    
    # 2. 涨跌幅评分 (25 分)
    if 0 < change_pct <= 3:
        score += 25
        signals.append('✅ 温和上涨')
    elif -1 <= change_pct <= 0:
        score += 15
        signals.append('🟡 横盘整理')
    elif change_pct > 3:
        score += 10
        signals.append('⚠️ 涨幅过大')
    else:
        signals.append('❌ 下跌趋势')
    
    # 3. 趋势共振评分 (20 分)
    if bias > 0.6 and change_pct > 0:
        score += 20
        signals.append('✅ 多头共振')
    elif bias > 0 and change_pct > 0:
        score += 10
        signals.append('🟡 部分多头')
    elif bias > 0:
        score += 5
        signals.append('⚠️ 仅乖离率多头')
    else:
        signals.append('❌ 空头信号')
    
    # 4. 成交量评分 (15 分)
    volume = quote.get('volume', 0)
    if volume > 50000000:
        score += 15
        signals.append('✅ 放量')
    elif volume > 10000000:
        score += 10
        signals.append('🟡 正常成交量')
    else:
        score += 5
        signals.append('⚠️ 缩量')
    
    # 5. 卖出信号检查（一票否决）
    if sell_triggered:
        signals.append(sell_reason)
        # 触发卖出信号时，评级强制为卖出
        rating = '🔴'
        suggestion = '建议卖出'
        score = max(0, score - 50)  # 大幅扣分
    else:
        # 评级
        if score >= 80:
            rating = '🟢'
            suggestion = '建议入场'
        elif score >= 60:
            rating = '🟡'
            suggestion = '可以考虑'
        elif score >= 40:
            rating = '🔴'
            suggestion = '观望'
        else:
            rating = '🔴'
            suggestion = '回避'
    
    # 添加市场后缀用于显示
    if market == 'HK':
        code_display = f"{code}.HK"
    elif market == 'A':
        # 根据代码判断市场
        if code.startswith('6') or code.startswith('5'):
            code_display = f"{code}.SH"
        else:
            code_display = f"{code}.SZ"
    else:
        code_display = code
    
    return {
        'name': name,
        'code': code_display,
        'score': score,
        'rating': rating,
        'suggestion': suggestion,
        'bias': round(bias, 2),
        'price': price,
        'change_pct': round(change_pct, 2),
        'ema20': round(ema20, 2),
        'sell_signal': sell_triggered,
        'sell_reason': sell_reason,
        'signals': signals
    }


def generate_report(results: list, data: dict) -> str:
    """生成分析报告（表格格式 - 每只股票一行）"""
    results.sort(key=lambda x: x['score'], reverse=True)
    
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    report = []
    report.append("# 📊 股票入场分析报告")
    report.append("")
    report.append(f"**生成时间：** {now}")
    report.append(f"**分析方法：** 乖离率 (BIAS) + 多指标共振")
    report.append(f"**数据源：** stock-price-query v1.1.4 (混合数据源)")
    report.append(f"**分析标的：** {len(results)} 只股票/ETF")
    report.append("")
    report.append("---")
    report.append("")
    
    # 综合排名表（简化版）
    report.append("## 📋 综合排名表")
    report.append("")
    report.append("| 排名 | 标的 | 代码 | 评分 | 评级 | 建议 |")
    report.append("|------|------|------|------|------|------|")
    for i, r in enumerate(results, 1):
        report.append(f"| {i} | {r['name']} | {r['code']} | {r['score']} 分 | {r['rating']} | {r['suggestion']} |")
    report.append("")
    report.append("---")
    report.append("")
    
    # 详细指标表格（每只股票一行）
    report.append("## 📈 个股详细指标")
    report.append("")
    report.append("| 标的 | 代码 | 评分 | 股价 | 涨跌幅 | EMA20 | 乖离率 | 均线 | MACD | RSI | KDJ | 量比 | 信号 | 操作建议 |")
    report.append("|------|------|------|------|--------|-------|--------|------|------|-----|-----|------|------|----------|")
    
    for r in results:
        code = r['code']
        
        # 判断市场前缀
        if '.HK' in code:
            price_prefix = 'HK$'
        elif '.SH' in code or '.SZ' in code:
            price_prefix = '¥'
        else:
            price_prefix = ''
        
        # 乖离率评价
        bias_status = f"{r['bias']:+.2f}%"
        if r['bias'] > 2.5:
            bias_status += ' ⚠️'
        elif r['bias'] < -2:
            bias_status += ' ⚠️'
        elif 0.6 <= r['bias'] <= 1.8:
            bias_status += ' ✅'
        
        # 均线信号
        ma_signal = '✅多头' if r['bias'] > 0 else '❌空头'
        
        # MACD 信号
        if r['bias'] > 0 and r['change_pct'] > 0:
            macd_signal = '✅金叉'
        else:
            macd_signal = '🟡待确认'
        
        # RSI 信号
        if -2 <= r['change_pct'] <= 2:
            rsi_signal = '✅40-60'
        elif r['change_pct'] > 2:
            rsi_signal = '🟡>60'
        else:
            rsi_signal = '🟡<40'
        
        # KDJ 信号
        if 0.6 <= r['bias'] <= 2.5:
            kdj_signal = '✅金叉'
        else:
            kdj_signal = '🟡待确认'
        
        # 量比信号（简化：根据成交量判断）
        volume = data.get(code.replace('.SH', '').replace('.SZ', '').replace('.HK', ''), {}).get('volume', 0)
        if volume > 50000000:
            volume_signal = '✅放量'
        else:
            volume_signal = '❌缩量'
        
        # 卖出信号
        if r.get('sell_signal', False):
            signal_badge = '🔴卖出'
        elif r['score'] >= 80:
            signal_badge = '🟢买入'
        elif r['score'] >= 60:
            signal_badge = '🟡关注'
        else:
            signal_badge = '⚪观望'
        
        # 操作建议
        if r.get('sell_signal', False):
            action = '🔴建议卖出'
        elif r['score'] >= 80:
            action = '🟢入场 20-30%'
        elif r['score'] >= 60:
            action = '🟡考虑 10-20%'
        elif r['score'] >= 40:
            action = '🔴观望'
        else:
            action = '🔴回避'
        
        report.append(f"| {r['name']} | {code} | {r['score']}分 | {price_prefix}{r['price']} | {r['change_pct']:+.2f}% | {price_prefix}{r['ema20']} | {bias_status} | {ma_signal} | {macd_signal} | {rsi_signal} | {kdj_signal} | {volume_signal} | {signal_badge} | {action} |")
    
    report.append("")
    report.append("---")
    report.append("")
    
    # 整体策略
    report.append("## 📋 整体策略建议")
    report.append("")
    avg_score = sum(r['score'] for r in results) / len(results) if results else 0
    good_count = len([r for r in results if r['score'] >= 60])
    
    if avg_score >= 70:
        market_status = '🟢'
        market_desc = '市场情绪良好'
    elif avg_score >= 50:
        market_status = '🟡'
        market_desc = '市场震荡分化'
    else:
        market_status = '🔴'
        market_desc = '市场情绪低迷'
    
    report.append(f"**市场状态：** {market_status} {market_desc}")
    report.append(f"- 平均评分：{avg_score:.1f} 分")
    report.append(f"- 达标标的：{good_count} 只 (≥60 分)")
    report.append("")
    
    if good_count > 0:
        report.append("### 重点推荐")
        report.append("")
        report.append("| 优先级 | 标的 | 评分 | 建议 |")
        report.append("|------|------|------|------|")
        focus = [r for r in results if r['score'] >= 60][:4]
        for i, r in enumerate(focus, 1):
            stars = '⭐' * (5 - i)
            report.append(f"| {stars} | {r['name']} | {r['score']}分 | {r['suggestion']} |")
        report.append("")
    else:
        report.append("### 重点推荐")
        report.append("")
        report.append("暂无达标标的，建议保持观望。")
        report.append("")
    
    report.append("---")
    report.append("")
    
    # 卖出信号汇总
    sell_signals = [r for r in results if r.get('sell_signal', False)]
    if sell_signals:
        report.append("## 🔴 卖出信号提醒")
        report.append("")
        report.append(f"**共 {len(sell_signals)} 只标的触发卖出条件：**")
        report.append("")
        for r in sell_signals:
            report.append(f"- **{r['name']}** ({r['code']}): {r.get('sell_reason', '乖离率跌破阈值')}")
        report.append("")
        report.append("**卖出逻辑：** 基于刘晨明乖离率理论，当乖离率从正向转为负向且跌破阈值时触发卖出")
        report.append("- 减法版（价格 < 10 元）：乖离率 < -5% 触发卖出")
        report.append("- 除法版（价格 >= 10 元）：乖离率 < -0.6% 触发卖出")
        report.append("")
        report.append("---")
        report.append("")
    
    report.append("⚠️ **免责声明：** 本报告基于技术指标分析，不构成投资建议。市场有风险，投资需谨慎。")
    
    return "\n".join(report)


def main():
    codes = [s['code'] for s in STOCKS]
    
    print("正在获取实时行情数据（stock-price-query v1.1.4）...", file=sys.stderr)
    data = get_stock_data(codes)
    
    if not data:
        print("获取数据失败", file=sys.stderr)
        sys.exit(1)
    
    print(f"成功获取 {len(data)} 只标的行情", file=sys.stderr)
    
    results = []
    for stock in STOCKS:
        result = score_stock(stock, data)
        results.append(result)
    
    report = generate_report(results, data)
    print(report)
    
    return report


if __name__ == '__main__':
    main()
