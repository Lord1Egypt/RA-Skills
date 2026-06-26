#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Backtest Engine
历史回测引擎 - 验证策略有效性
"""

import json
import subprocess
from datetime import datetime, timedelta
from collections import defaultdict

class BacktestEngine:
    """历史回测引擎"""

    def __init__(self, stock_code, strategy_name="改进策略一"):
        self.stock_code = stock_code
        self.strategy_name = strategy_name
        self.kline_data = None
        self.technical_data = None
        self.trades = []
        self.results = {}

    def get_historical_data(self, days=120):
        """获取历史数据"""
        print(f"\n📊 获取过去{days}天历史数据...")

        # 获取K线数据
        cmd = f"node ~/.workbuddy/skills/westock-data/scripts/index.js kline {self.stock_code} daily {days} hfq"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            try:
                data = json.loads(result.stdout)
                # 提取nodes数据
                if 'data' in data and 'nodes' in data['data']:
                    self.kline_data = data['data']['nodes']
                    print(f"✅ 获取到{len(self.kline_data)}天K线数据")
                    return True
                else:
                    print(f"❌ K线数据格式错误")
                    return False
            except json.JSONDecodeError:
                print(f"❌ K线数据解析失败")
                return False
        else:
            print(f"❌ 获取K线数据失败")
            return False

    def get_historical_technical(self, days=120):
        """获取历史技术指标"""
        print(f"\n📈 获取过去{days}天技术指标...")

        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        cmd = f"node ~/.workbuddy/skills/westock-data/scripts/index.js technical {self.stock_code} ma,macd,kdj,rsi,dmi,vol,boll {start_date} {end_date}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            try:
                data = json.loads(result.stdout)
                # 提取items数据
                if 'data' in data and 'items' in data['data']:
                    self.technical_data = data['data']['items']
                    print(f"✅ 获取到{len(self.technical_data)}天技术指标")
                    return True
                else:
                    print(f"❌ 技术指标数据格式错误")
                    return False
            except json.JSONDecodeError:
                print(f"❌ 技术指标解析失败")
                return False
        else:
            print(f"❌ 获取技术指标失败")
            return False

    def check_buy_signal(self, index):
        """检查买入信号"""
        if index >= len(self.technical_data) or index >= len(self.kline_data):
            return False, 0, []

        try:
            tech = self.technical_data[index]
            kline = self.kline_data[index]

            # 7个买入条件
            conditions = []

            # 1. 均线多头排列
            ma5 = tech.get('ma', {}).get('MA_5', 0)
            ma10 = tech.get('ma', {}).get('MA_10', 0)
            ma20 = tech.get('ma', {}).get('MA_20', 0)
            ma60 = tech.get('ma', {}).get('MA_60', 0)
            condition1 = (ma5 > ma10 > ma20 > ma60)
            conditions.append(condition1)

            # 2. MACD金叉
            dif = tech.get('macd', {}).get('DIF', 0)
            dea = tech.get('macd', {}).get('DEA', 0)
            condition2 = (dif > dea and dif > 0 and dea > 0)
            conditions.append(condition2)

            # 3. KDJ金叉
            k = tech.get('kdj', {}).get('KDJ_K', 0)
            d = tech.get('kdj', {}).get('KDJ_D', 0)
            condition3 = (k > d and 20 <= k <= 80)
            conditions.append(condition3)

            # 4. RSI适中
            rsi12 = tech.get('rsi', {}).get('RSI_12', 0)
            condition4 = (50 <= rsi12 <= 70)
            conditions.append(condition4)

            # 5. 价格站上MA20
            close = kline.get('close', kline.get('last', kline.get('price', 0)))
            condition5 = (close > ma20)
            conditions.append(condition5)

            # 6. 成交量放大
            condition6 = self._check_volume_increase(index)
            conditions.append(condition6)

            # 7. DMI多头
            pdi = tech.get('dmi', {}).get('PDI', 0)
            mdi = tech.get('dmi', {}).get('MDI', 0)
            adx = tech.get('dmi', {}).get('ADX', 0)
            condition7 = (pdi > mdi and adx > 20)
            conditions.append(condition7)

            # 计算满足度
            satisfied_count = sum(conditions)
            buy_signal = satisfied_count >= 5  # 至少满足5个条件

            return buy_signal, satisfied_count, conditions

        except Exception as e:
            print(f"    ⚠️ 检查买入信号时出错 (index={index}): {e}")
            return False, 0, []

    def check_high_risk_warning(self, index):
        """检查高位预警"""
        if index >= len(self.technical_data) or index >= len(self.kline_data):
            return 0, []

        try:
            tech = self.technical_data[index]
            kline = self.kline_data[index]

            warnings = []

            # 1. KDJ超买
            k = tech.get('kdj', {}).get('KDJ_K', 0)
            if k > 70:
                warnings.append('KDJ超买')

            # 2. RSI超买
            rsi12 = tech.get('rsi', {}).get('RSI_12', 0)
            if rsi12 > 65:
                warnings.append('RSI超买')

            # 3. 偏离MA20
            close = kline.get('close', kline.get('last', kline.get('price', 0)))
            ma20 = tech.get('ma', {}).get('MA_20', 0)
            if ma20 > 0 and close > 0:
                deviation = (close / ma20 - 1) * 100
                if deviation > 15:
                    warnings.append(f'偏离MA20 {deviation:.1f}%')

            # 4. 突破上轨
            boll_upper = tech.get('boll', {}).get('BOLL_UPPER', 0)
            if close > boll_upper:
                warnings.append('突破上轨')

            # 5. 近期涨幅
            if index >= 5:
                recent_rise = self._calculate_recent_rise(index)
                if recent_rise > 25:
                    warnings.append(f'近期涨幅{recent_rise:.1f}%')

            return len(warnings), warnings

        except Exception as e:
            print(f"    ⚠️ 检查高位预警时出错 (index={index}): {e}")
            return 0, []

    def check_sell_signal(self, index, buy_price):
        """检查卖出信号"""
        if index >= len(self.technical_data) or index >= len(self.kline_data):
            return False, "数据不足"

        try:
            tech = self.technical_data[index]
            kline = self.kline_data[index]
            close = kline.get('close', kline.get('last', kline.get('price', 0)))

            # 计算收益率
            return_rate = (close - buy_price) / buy_price * 100

            # 卖出条件
            sell_reasons = []

            # 1. 止损: 跌破MA20且亏损超过5%
            ma20 = tech.get('ma', {}).get('MA_20', 0)
            if close < ma20 and return_rate < -5:
                sell_reasons.append("止损-跌破MA20")

            # 2. 止盈1: 收益超过20%
            if return_rate >= 20:
                sell_reasons.append("止盈+20%")

            # 3. 止盈2: 偏离MA20超过25%
            if ma20 > 0 and close > 0:
                deviation = (close / ma20 - 1) * 100
                if deviation > 25:
                    sell_reasons.append("止盈-高位预警")

            # 4. 止盈3: RSI严重超买且收益超过15%
            rsi12 = tech.get('rsi', {}).get('RSI_12', 0)
            if rsi12 > 75 and return_rate >= 15:
                sell_reasons.append("止盈-RSI超买")

            # 5. 止盈4: 连续3天下跌且收益为正
            if index >= 3 and return_rate > 0:
                three_days_down = all(
                    self.kline_data[i].get('close', 0) < self.kline_data[i-1].get('close', 0)
                    for i in range(index-2, index+1)
                )
                if three_days_down:
                    sell_reasons.append("止盈-连续下跌")

            return len(sell_reasons) > 0, ", ".join(sell_reasons)

        except Exception as e:
            print(f"    ⚠️ 检查卖出信号时出错 (index={index}): {e}")
            return False, "检查错误"

    def _check_volume_increase(self, index):
        """检查成交量是否放大"""
        if index < 5:
            return False

        try:
            recent_5_days = self.kline_data[index-4:index+1]
            avg_volume = sum(day.get('volume', 0) for day in recent_5_days) / 5
            current_volume = self.kline_data[index].get('volume', 0)

            return current_volume > avg_volume * 1.3
        except Exception:
            return False

    def _calculate_recent_rise(self, index):
        """计算近期涨幅"""
        if index < 5:
            return 0

        try:
            first_price = self.kline_data[index-5].get('close', self.kline_data[index-5].get('last', 0))
            last_price = self.kline_data[index].get('close', self.kline_data[index].get('last', 0))

            if first_price <= 0:
                return 0

            return ((last_price - first_price) / first_price) * 100
        except Exception:
            return 0

    def run_backtest(self, initial_capital=100000):
        """运行回测"""
        print(f"\n🚀 开始回测 {self.strategy_name}...")
        print(f"初始资金: {initial_capital:,.0f}港元")

        capital = initial_capital
        position = 0  # 持股数量
        buy_price = 0  # 买入价格
        in_position = False

        for i in range(20, len(self.kline_data) - 10):  # 从第20天开始,留10天缓冲
            date = self.kline_data[i].get('date', '')
            close = self.kline_data[i].get('close', self.kline_data[i].get('last', self.kline_data[i].get('price', 0)))

            # 如果在持仓中,检查卖出信号
            if in_position:
                should_sell, sell_reason = self.check_sell_signal(i, buy_price)
                if should_sell:
                    # 卖出
                    sell_price = close
                    profit = (sell_price - buy_price) * position
                    profit_rate = (sell_price - buy_price) / buy_price * 100

                    capital += (sell_price * position)

                    trade = {
                        'buy_date': self.trades[-1]['buy_date'] if self.trades else '',
                        'buy_price': buy_price,
                        'sell_date': date,
                        'sell_price': sell_price,
                        'shares': position,
                        'profit': profit,
                        'profit_rate': profit_rate,
                        'reason': sell_reason
                    }
                    self.trades.append(trade)

                    print(f"📤 {date} 卖出 {position:.0f}股 @ {sell_price:.2f} | "
                          f"收益: {profit_rate:.2f}% | 原因: {sell_reason}")

                    position = 0
                    buy_price = 0
                    in_position = False
            else:
                # 如果不在持仓中,检查买入信号
                should_buy, satisfied_count, conditions = self.check_buy_signal(i)
                warning_count, warnings = self.check_high_risk_warning(i)

                if should_buy and warning_count <= 2:  # 买入且高位预警不超过2个
                    # 买入
                    if close <= 0:
                        print(f"    ⚠️ {date} 价格异常: {close}, 跳过买入")
                        continue

                    buy_price = close
                    position = int(capital * 0.3 / buy_price)  # 每次买入30%仓位
                    capital -= (buy_price * position)

                    trade = {
                        'buy_date': date,
                        'buy_price': buy_price,
                        'sell_date': '',
                        'sell_price': 0,
                        'shares': position,
                        'profit': 0,
                        'profit_rate': 0,
                        'reason': f'满足{satisfied_count}/7条件, {warning_count}个预警'
                    }
                    self.trades.append(trade)

                    print(f"📥 {date} 买入 {position:.0f}股 @ {buy_price:.2f} | "
                          f"满足{satisfied_count}/7条件, {warning_count}个预警")

                    in_position = True

        # 如果最后还在持仓中,按最后价格平仓
        if in_position:
            last_price = self.kline_data[-1].get('close', self.kline_data[-1].get('last', self.kline_data[-1].get('price', 0)))
            profit = (last_price - buy_price) * position
            profit_rate = (last_price - buy_price) / buy_price * 100

            capital += (last_price * position)

            self.trades[-1]['sell_date'] = self.kline_data[-1].get('date', '')
            self.trades[-1]['sell_price'] = last_price
            self.trades[-1]['profit'] = profit
            self.trades[-1]['profit_rate'] = profit_rate
            self.trades[-1]['reason'] = '回测结束强制平仓'

            print(f"📤 回测结束 强制平仓 {position:.0f}股 @ {last_price:.2f} | "
                  f"收益: {profit_rate:.2f}%")

        return self._calculate_results(initial_capital)

    def _calculate_results(self, initial_capital):
        """计算回测结果"""
        if not self.trades:
            return {
                'error': '无交易记录'
            }

        total_trades = len(self.trades)
        profitable_trades = sum(1 for t in self.trades if t['profit'] > 0)
        win_rate = profitable_trades / total_trades * 100 if total_trades > 0 else 0

        total_profit = sum(t['profit'] for t in self.trades)
        avg_profit = total_profit / total_trades if total_trades > 0 else 0

        max_profit = max(t['profit'] for t in self.trades) if self.trades else 0
        min_profit = min(t['profit'] for t in self.trades) if self.trades else 0

        total_return = (sum(t['profit_rate'] for t in self.trades) / total_trades) if total_trades > 0 else 0

        # 计算最大回撤
        max_drawdown = 0
        peak = 0
        for t in self.trades:
            peak = max(peak, t['profit'])
            drawdown = (peak - t['profit']) / peak * 100 if peak > 0 else 0
            max_drawdown = max(max_drawdown, drawdown)

        results = {
            'total_trades': total_trades,
            'profitable_trades': profitable_trades,
            'win_rate': win_rate,
            'total_profit': total_profit,
            'avg_profit': avg_profit,
            'avg_profit_rate': total_return,
            'max_profit': max_profit,
            'max_profit_rate': max(t['profit_rate'] for t in self.trades) if self.trades else 0,
            'min_profit': min_profit,
            'min_profit_rate': min(t['profit_rate'] for t in self.trades) if self.trades else 0,
            'max_drawdown': max_drawdown,
            'trades': self.trades
        }

        return results

    def generate_report(self):
        """生成回测报告"""
        if not self.results or 'error' in self.results:
            return "❌ 回测失败,无结果"

        r = self.results

        risk_reward_ratio = f"1:{abs(r['avg_profit_rate'] / r['max_drawdown']):.1f}" if r['max_drawdown'] > 0 else "N/A"

        report = f"""
📊 {self.strategy_name} 回测报告
━━━━━━━━━━━━━━━━━━━━━━━━━━

股票代码: {self.stock_code}
回测天数: {len(self.kline_data) if self.kline_data else 0}天

📈 交易统计
━━━━━━━━━━━━━━━━━━━━━━━━━━
总交易次数: {r['total_trades']}次
盈利交易: {r['profitable_trades']}次
亏损交易: {r['total_trades'] - r['profitable_trades']}次
胜率: {r['win_rate']:.2f}%

💰 收益统计
━━━━━━━━━━━━━━━━━━━━━━━━━━
总收益: {r['total_profit']:,.0f}港元
平均收益: {r['avg_profit']:,.0f}港元
平均收益率: {r['avg_profit_rate']:.2f}%
最大单笔收益: {r['max_profit']:,.0f}港元 ({r['max_profit_rate']:.2f}%)
最大单笔亏损: {r['min_profit']:,.0f}港元 ({r['min_profit_rate']:.2f}%)

⚠️ 风险指标
━━━━━━━━━━━━━━━━━━━━━━━━━━
最大回撤: {r['max_drawdown']:.2f}%
风险收益比: {risk_reward_ratio}

📋 交易明细
━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

        for i, trade in enumerate(r['trades'], 1):
            report += f"""
交易 #{i}
- 买入: {trade['buy_date']} @ {trade['buy_price']:.2f}港元
- 卖出: {trade['sell_date']} @ {trade['sell_price']:.2f}港元
- 数量: {trade['shares']:.0f}股
- 收益: {trade['profit']:,.0f}港元 ({trade['profit_rate']:.2f}%)
- 原因: {trade['reason']}
"""

        return report

# 使用示例
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("使用方法: python backtest.py <股票代码> [回测天数]")
        print("示例: python backtest.py hk00700 120")
        sys.exit(1)

    stock_code = sys.argv[1]
    days = int(sys.argv[2]) if len(sys.argv) > 2 else 120

    engine = BacktestEngine(stock_code)

    if engine.get_historical_data(days) and engine.get_historical_technical(days):
        results = engine.run_backtest(initial_capital=100000)
        engine.results = results
        report = engine.generate_report()
        print(report)
    else:
        print("❌ 获取历史数据失败")
