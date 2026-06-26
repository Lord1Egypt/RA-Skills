#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stock Decision Analysis Script
股票买入决策分析脚本
"""

import json
import subprocess
import re
from datetime import datetime, timedelta

class StockDecisionAnalyzer:
    """股票决策分析器"""

    def __init__(self, stock_input):
        self.stock_input = stock_input.strip()
        self.stock_code = None
        self.stock_name = None
        self.current_price = None
        self.kline_data = None
        self.technical_data = None
        self.ma_data = {}
        self.macd_data = {}
        self.kdj_data = {}
        self.rsi_data = {}
        self.boll_data = {}
        self.dmi_data = {}
        self.obv_data = {}

    def search_stock(self):
        """搜索股票"""
        print(f"\n🔍 搜索股票: {self.stock_input}")
        cmd = f"node ~/.workbuddy/skills/westock-data/scripts/index.js search '{self.stock_input}'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            output = result.stdout
            # 解析股票代码
            match = re.search(r'(hk\d{5}|sz\d{6}|sh\d{6})', output, re.IGNORECASE)
            if match:
                self.stock_code = match.group(1).lower()
                # 尝试获取股票名称
                name_match = re.search(r'名称[：:]\s*([^\n]+)', output)
                if name_match:
                    self.stock_name = name_match.group(1).strip()
                print(f"✅ 找到股票: {self.stock_name} ({self.stock_code})")
                return True
            else:
                print(f"❌ 未找到股票: {self.stock_input}")
                return False
        else:
            print(f"❌ 搜索失败: {result.stderr}")
            return False

    def get_kline_data(self, days=30):
        """获取K线数据"""
        print(f"\n📊 获取近{days}日K线数据...")
        cmd = f"node ~/.workbuddy/skills/westock-data/scripts/index.js kline {self.stock_code} day {days} qfq"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            try:
                self.kline_data = json.loads(result.stdout)
                # 获取最新价格
                if self.kline_data and len(self.kline_data) > 0:
                    latest = self.kline_data[-1]
                    self.current_price = latest.get('close', latest.get('price'))
                    print(f"✅ 当前价格: {self.current_price}港元")
                return True
            except json.JSONDecodeError:
                print(f"❌ K线数据解析失败")
                return False
        else:
            print(f"❌ 获取K线数据失败: {result.stderr}")
            return False

    def get_technical_data(self):
        """获取技术指标数据"""
        print(f"\n📈 获取技术指标数据...")
        # 获取最近30天的技术指标
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        cmd = f"node ~/.workbuddy/skills/westock-data/scripts/index.js technical {self.stock_code} all {start_date} {end_date}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            try:
                self.technical_data = json.loads(result.stdout)
                # 解析技术指标
                self._parse_technical_data()
                print(f"✅ 技术指标获取成功")
                return True
            except json.JSONDecodeError:
                print(f"❌ 技术指标解析失败")
                return False
        else:
            print(f"❌ 获取技术指标失败: {result.stderr}")
            return False

    def _parse_technical_data(self):
        """解析技术指标数据"""
        if not self.technical_data or len(self.technical_data) == 0:
            return

        # 获取最新的技术指标数据
        latest = self.technical_data[-1]

        # MA均线
        self.ma_data = {
            'MA5': latest.get('MA5', 0),
            'MA10': latest.get('MA10', 0),
            'MA20': latest.get('MA20', 0),
            'MA60': latest.get('MA60', 0),
        }

        # MACD
        self.macd_data = {
            'DIF': latest.get('DIF', 0),
            'DEA': latest.get('DEA', 0),
            'MACD': latest.get('MACD', 0),
        }

        # KDJ
        self.kdj_data = {
            'K': latest.get('K', 0),
            'D': latest.get('D', 0),
            'J': latest.get('J', 0),
        }

        # RSI
        self.rsi_data = {
            'RSI6': latest.get('RSI6', 0),
            'RSI12': latest.get('RSI12', 0),
            'RSI24': latest.get('RSI24', 0),
        }

        # 布林带
        self.boll_data = {
            'UPPER': latest.get('BOLL_UPPER', 0),
            'MID': latest.get('BOLL_MID', 0),
            'LOWER': latest.get('BOLL_LOWER', 0),
        }

        # DMI
        self.dmi_data = {
            'PDI': latest.get('PDI', 0),
            'MDI': latest.get('MDI', 0),
            'ADX': latest.get('ADX', 0),
        }

        # OBV
        self.obv_data = {
            'OBV': latest.get('OBV', 0),
        }

    def analyze_technical(self):
        """技术面分析"""
        print(f"\n🔬 技术面分析 (改进策略一)")

        # 7个买入条件
        buy_conditions = {
            '均线多头排列': self._check_ma_bullish(),
            'MACD金叉': self._check_macd_golden_cross(),
            'KDJ金叉': self._check_kdj_golden_cross(),
            'RSI适中': self._check_rsi_normal(),
            '价格站上MA20': self._check_price_above_ma20(),
            '成交量放大': self._check_volume_increase(),
            'DMI多头': self._check_dmi_bullish(),
        }

        # 6个高位预警
        high_warnings = {
            'KDJ超买': self._check_kdj_overbought(),
            'RSI超买': self._check_rsi_overbought(),
            '偏离MA20': self._check_deviation_ma20(),
            '突破上轨': self._check_break_upper_band(),
            '近期涨幅': self._check_recent_rise(),
            'OBV背离': self._check_obv_divergence(),
        }

        # 计算满足度
        buy_satisfied = sum(buy_conditions.values())
        buy_score = buy_satisfied / 7

        # 计算预警数量
        warning_count = sum(high_warnings.values())

        # 技术评分
        technical_score = (buy_satisfied * 10) - (warning_count * 5) + 50
        technical_score = max(0, min(100, technical_score))  # 限制在0-100之间

        return {
            'buy_conditions': buy_conditions,
            'high_warnings': high_warnings,
            'buy_satisfied': buy_satisfied,
            'buy_score': buy_score,
            'warning_count': warning_count,
            'technical_score': technical_score,
        }

    def _check_ma_bullish(self):
        """检查均线多头排列"""
        return (self.ma_data['MA5'] > self.ma_data['MA10'] and
                self.ma_data['MA10'] > self.ma_data['MA20'] and
                self.ma_data['MA20'] > self.ma_data['MA60'])

    def _check_macd_golden_cross(self):
        """检查MACD金叉"""
        return (self.macd_data['DIF'] > self.macd_data['DEA'] and
                self.macd_data['DIF'] > 0 and
                self.macd_data['DEA'] > 0)

    def _check_kdj_golden_cross(self):
        """检查KDJ金叉"""
        k = self.kdj_data['K']
        d = self.kdj_data['D']
        return (k > d and 20 <= k <= 80)

    def _check_rsi_normal(self):
        """检查RSI适中"""
        rsi12 = self.rsi_data['RSI12']
        return 50 <= rsi12 <= 70

    def _check_price_above_ma20(self):
        """检查价格站上MA20"""
        return self.current_price > self.ma_data['MA20']

    def _check_volume_increase(self):
        """检查成交量放大"""
        if not self.kline_data or len(self.kline_data) < 5:
            return False
        # 计算近5日平均成交量
        recent_5_days = self.kline_data[-5:]
        avg_volume = sum(day.get('volume', 0) for day in recent_5_days) / 5
        # 当前成交量
        current_volume = self.kline_data[-1].get('volume', 0)
        # 检查是否放大30%以上
        return current_volume > avg_volume * 1.3

    def _check_dmi_bullish(self):
        """检查DMI多头"""
        return (self.dmi_data['PDI'] > self.dmi_data['MDI'] and
                self.dmi_data['ADX'] > 20)

    def _check_kdj_overbought(self):
        """检查KDJ超买"""
        return self.kdj_data['K'] > 70

    def _check_rsi_overbought(self):
        """检查RSI超买"""
        return self.rsi_data['RSI12'] > 65

    def _check_deviation_ma20(self):
        """检查偏离MA20"""
        deviation = (self.current_price / self.ma_data['MA20'] - 1) * 100
        return deviation > 15

    def _check_break_upper_band(self):
        """检查突破布林带上轨"""
        return self.current_price > self.boll_data['UPPER']

    def _check_recent_rise(self):
        """检查近期涨幅"""
        if not self.kline_data or len(self.kline_data) < 5:
            return False
        recent_5_days = self.kline_data[-5:]
        first_price = recent_5_days[0].get('close', 0)
        last_price = recent_5_days[-1].get('close', 0)
        rise = ((last_price - first_price) / first_price) * 100
        return rise > 25

    def _check_obv_divergence(self):
        """检查OBV背离"""
        if not self.kline_data or len(self.kline_data) < 3:
            return False
        # 简化检查: 最近3天价格上涨但OBV下降
        recent_3_days = self.kline_data[-3:]
        price_rising = all(
            recent_3_days[i].get('close', 0) > recent_3_days[i-1].get('close', 0)
            for i in range(1, 3)
        )
        obv_falling = all(
            self.technical_data[i].get('OBV', 0) < self.technical_data[i-1].get('OBV', 0)
            for i in range(-2, 0)
        )
        return price_rising and obv_falling

    def generate_decision_report(self):
        """生成决策报告"""
        print(f"\n📝 生成决策报告...")

        # 执行分析
        if not self.search_stock():
            return "❌ 股票搜索失败"

        if not self.get_kline_data():
            return "❌ 获取K线数据失败"

        if not self.get_technical_data():
            return "❌ 获取技术指标失败"

        # 技术面分析
        tech_analysis = self.analyze_technical()

        # 计算止盈止损
        stop_loss = self.ma_data['MA20']
        stop_loss_strict = self.ma_data['MA60']
        profit_targets = {
            'first': self.ma_data['MA20'] * 1.15,
            'second': self.ma_data['MA20'] * 1.20,
            'third': self.current_price * 1.05,
            'ideal': self.ma_data['MA60'] * 1.30,
        }

        # 生成报告
        report = f"""
📊 股票基本信息
━━━━━━━━━━━━━━━━━━━━━━━━━━
股票名称: {self.stock_name or self.stock_code}
股票代码: {self.stock_code}
当前价格: {self.current_price}港元
MA5: {self.ma_data['MA5']:.2f}
MA10: {self.ma_data['MA10']:.2f}
MA20: {self.ma_data['MA20']:.2f}
MA60: {self.ma_data['MA60']:.2f}

📈 技术面分析 (改进策略一)
━━━━━━━━━━━━━━━━━━━━━━━━━━

7个买入条件满足情况:
{'✅' if tech_analysis['buy_conditions']['均线多头排列'] else '❌'} 1. 均线多头排列: {self.ma_data['MA5']:.2f} vs {self.ma_data['MA10']:.2f} vs {self.ma_data['MA20']:.2f} vs {self.ma_data['MA60']:.2f}
{'✅' if tech_analysis['buy_conditions']['MACD金叉'] else '❌'} 2. MACD金叉: DIF={self.macd_data['DIF']:.2f}, DEA={self.macd_data['DEA']:.2f}
{'✅' if tech_analysis['buy_conditions']['KDJ金叉'] else '❌'} 3. KDJ金叉: K={self.kdj_data['K']:.2f}, D={self.kdj_data['D']:.2f}
{'✅' if tech_analysis['buy_conditions']['RSI适中'] else '❌'} 4. RSI适中: RSI12={self.rsi_data['RSI12']:.2f}
{'✅' if tech_analysis['buy_conditions']['价格站上MA20'] else '❌'} 5. 价格站上MA20: {self.current_price:.2f} vs {self.ma_data['MA20']:.2f}
{'✅' if tech_analysis['buy_conditions']['成交量放大'] else '❌'} 6. 成交量放大: 需手动确认
{'✅' if tech_analysis['buy_conditions']['DMI多头'] else '❌'} 7. DMI多头: PDI={self.dmi_data['PDI']:.2f}, MDI={self.dmi_data['MDI']:.2f}, ADX={self.dmi_data['ADX']:.2f}

满足度: {tech_analysis['buy_satisfied']}/7 ({tech_analysis['buy_score']:.1%})

6个高位预警信号:
{'⚠️' if tech_analysis['high_warnings']['KDJ超买'] else '✅'} 1. KDJ超买: K={self.kdj_data['K']:.2f} {'已触发!' if tech_analysis['high_warnings']['KDJ超买'] else '未触发'}
{'⚠️' if tech_analysis['high_warnings']['RSI超买'] else '✅'} 2. RSI超买: RSI12={self.rsi_data['RSI12']:.2f} {'已触发!' if tech_analysis['high_warnings']['RSI超买'] else '未触发'}
{'⚠️' if tech_analysis['high_warnings']['偏离MA20'] else '✅'} 3. 偏离MA20: {((self.current_price/self.ma_data['MA20']-1)*100):.1f}% {'已触发!' if tech_analysis['high_warnings']['偏离MA20'] else '未触发'}
{'⚠️' if tech_analysis['high_warnings']['突破上轨'] else '✅'} 4. 突破上轨: {self.current_price:.2f} vs {self.boll_data['UPPER']:.2f} {'已触发!' if tech_analysis['high_warnings']['突破上轨'] else '未触发'}
{'⚠️' if tech_analysis['high_warnings']['近期涨幅'] else '✅'} 5. 近期涨幅: {'已触发!' if tech_analysis['high_warnings']['近期涨幅'] else '未触发'}
{'⚠️' if tech_analysis['high_warnings']['OBV背离'] else '✅'} 6. OBV背离: {'已触发!' if tech_analysis['high_warnings']['OBV背离'] else '未触发'}

技术评分: {tech_analysis['technical_score']:.0f}/100

⭐ 技术评级
━━━━━━━━━━━━━━━━━━━━━━━━━━
{self._get_technical_rating(tech_analysis['technical_score'])}

🎯 止盈止损建议
━━━━━━━━━━━━━━━━━━━━━━━━━━

止盈点设置:
- 第一止盈点: {profit_targets['first']:.2f}港元 (偏离MA20达15%)
- 第二止盈点: {profit_targets['second']:.2f}港元 (偏离MA20达20%)
- 第三止盈点: {profit_targets['third']:.2f}港元 (回本+5%)
- 理想止盈点: {profit_targets['ideal']:.2f}港元

止损点设置:
- 基础止损: {stop_loss:.2f}港元 (MA20)
- 严格止损: {stop_loss_strict:.2f}港元 (MA60)
- 最大风险: {((stop_loss/self.current_price-1)*100):.1f}%

⚠️ 风险提示
━━━━━━━━━━━━━━━━━━━━━━━━━━

{self._generate_risk_warnings(tech_analysis)}

💡 操作建议
━━━━━━━━━━━━━━━━━━━━━━━━━━

{self._generate_operation_suggestions(tech_analysis, profit_targets, stop_loss)}

━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ 免责声明
━━━━━━━━━━━━━━━━━━━━━━━━━━
本分析仅供参考,不构成投资建议。投资有风险,入市需谨慎。
请根据自身风险承受能力独立做出决策。
━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        return report

    def _get_technical_rating(self, score):
        """获取技术评级"""
        if score >= 85:
            return f"✅✅✅ 强烈推荐买入\n综合评分: {score:.0f}/100\n风险等级: 🟢 低风险"
        elif score >= 70:
            return f"✅✅ 推荐买入\n综合评分: {score:.0f}/100\n风险等级: 🟢 中低风险"
        elif score >= 60:
            return f"✅ 谨慎买入\n综合评分: {score:.0f}/100\n风险等级: 🟡 中等风险"
        elif score >= 50:
            return f"⏸️ 观望\n综合评分: {score:.0f}/100\n风险等级: 🟡 中高风险"
        else:
            return f"❌ 不建议买入\n综合评分: {score:.0f}/100\n风险等级: 🔴 高风险"

    def _generate_risk_warnings(self, tech_analysis):
        """生成风险提示"""
        warnings = []

        if tech_analysis['technical_score'] < 50:
            warnings.append("🔴 技术面评分低于50,不建议买入")

        if tech_analysis['warning_count'] >= 3:
            warnings.append("🟡 触发多个高位预警信号,短期回调风险大")

        if tech_analysis['buy_satisfied'] < 4:
            warnings.append("🟡 买入条件满足不足,技术面不支持买入")

        if not tech_analysis['buy_conditions']['均线多头排列']:
            warnings.append("🟡 均线空头排列,短期趋势向下")

        if tech_analysis['high_warnings']['KDJ超买']:
            warnings.append("🟡 KDJ超买,短期有回调压力")

        if tech_analysis['high_warnings']['RSI超买']:
            warnings.append("🟡 RSI超买,需防范回调风险")

        return "\n".join(warnings) if warnings else "✅ 当前无明显风险"

    def _generate_operation_suggestions(self, tech_analysis, profit_targets, stop_loss):
        """生成操作建议"""
        score = tech_analysis['technical_score']

        if score >= 70:
            return f"""
✅ 建议买入

理由:
- 技术面评分较高({score:.0f}分),买入条件满足度{tech_analysis['buy_satisfied']}/7
- 高位预警信号较少({tech_analysis['warning_count']}个),风险可控
- 多头趋势明确,上涨空间可期

建议操作:
- 买入仓位: 30-50%
- 第一止盈: {profit_targets['first']:.2f}港元
- 止损位: {stop_loss:.2f}港元
- 严格执行止损纪律
"""
        elif score >= 60:
            return f"""
✅ 谨慎买入

理由:
- 技术面评分中等({score:.0f}分),有一定买入价值
- 存在{tech_analysis['warning_count']}个高位预警,需注意
- 可考虑小仓位试探

建议操作:
- 买入仓位: 10-30%
- 止损位: {stop_loss:.2f}港元
- 密切关注后续走势
- 若跌破止损,坚决清仓
"""
        else:
            return f"""
❌ 不建议买入

理由:
- 技术面评分过低({score:.0f}分),买入条件满足仅{tech_analysis['buy_satisfied']}/7
- 存在{tech_analysis['warning_count']}个高位预警信号
- 技术面不支持入场,风险较大

建议操作:
- 不建议买入
- 若持有,考虑减仓止损
- 等待以下信号再考虑:
  * 均线开始多头排列
  * MACD金叉且站上零轴
  * 价格站上MA20
  * 高位预警信号减少
"""

# 使用示例
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("使用方法: python analyze.py <股票名称或代码>")
        print("示例: python analyze.py 腾讯")
        sys.exit(1)

    stock_input = sys.argv[1]
    analyzer = StockDecisionAnalyzer(stock_input)
    report = analyzer.generate_decision_report()
    print(report)
