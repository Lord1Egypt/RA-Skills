#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日股市数据分析 - 纯离线教学版 v15.0
⚠️ 本版本完全离线，无任何网络调用，仅用于学习演示
"""

import json
import sys
import os
import random
from datetime import datetime

# ========== 配置管理（仅当前目录）==========

CONFIG_FILE = 'config.json'
LOG_DIR = 'logs'

def load_config():
    """加载配置（纯本地，无网络）"""
    if not os.path.exists(CONFIG_FILE):
        # 创建默认配置（模拟数据）
        default_config = {
            "holdings": [
                {"code": "000001", "name": "平安银行", "shares": 1000, "cost_price": 10.0},
                {"code": "000002", "name": "万科A", "shares": 1000, "cost_price": 20.0},
                {"code": "000858", "name": "五粮液", "shares": 100, "cost_price": 150.0}
            ],
            "user_open_id": "ou_xxxxxxxxxxxxx",
            "push_channel": "none"  # 可选: none, console
        }
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, ensure_ascii=False, indent=2)
        print(f"📝 已创建默认配置: {CONFIG_FILE}")
        return default_config
    
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# ========== 纯模拟数据（无API调用）==========

def get_mock_indices():
    """生成模拟大盘指数"""
    return {
        '上证指数': {'close': round(random.uniform(3000, 4200), 2), 'change_pct': round(random.uniform(-2, 2), 2)},
        '深证成指': {'close': round(random.uniform(10000, 15000), 2), 'change_pct': round(random.uniform(-2, 2), 2)},
        '创业板指': {'close': round(random.uniform(2000, 3000), 2), 'change_pct': round(random.uniform(-2, 2), 2)}
    }

def get_mock_stock_quote(code, name, cost_price, shares):
    """生成模拟股票数据（无网络）"""
    base_price = cost_price
    change_pct = random.uniform(-5, 5)
    close = round(base_price * (1 + change_pct / 100), 2)
    
    return {
        'code': code,
        'name': name,
        'close': close,
        'change': round(close - base_price, 2),
        'change_pct': round(change_pct, 2),
        'cost_price': cost_price,
        'shares': shares,
        'position_pnl': round((close - cost_price) / cost_price * 100, 2),
        'source': '模拟数据',
        'verified': False
    }

def get_mock_sector_flow():
    """生成模拟板块资金流向"""
    sectors = [
        {'name': '军工', 'flow_3d': '持续流入', 'strength': '强', 'reason': '地缘政治因素'},
        {'name': '新能源', 'flow_3d': '持续流入', 'strength': '中', 'reason': '政策支持'},
        {'name': '黄金', 'flow_3d': '持续流入', 'strength': '强', 'reason': '避险需求'},
        {'name': '科技', 'flow_3d': '震荡', 'strength': '中', 'reason': '概念分化'},
        {'name': '金融', 'flow_3d': '流出', 'strength': '中', 'reason': '利率压力'},
        {'name': '消费', 'flow_3d': '流出', 'strength': '弱', 'reason': '复苏不及预期'}
    ]
    return sectors

# ========== 技术分析（纯计算）==========

def calculate_technical_levels(stock_data, market_trend):
    """计算技术位（纯本地计算）"""
    for s in stock_data:
        close = s['close']
        cost = s['cost_price']
        change_pct = s['change_pct']
        
        support = round(close * 0.985, 2)
        resistance = round(close * 1.015, 2)
        stop_loss = round(min(cost * 0.92, support * 0.98), 2)
        
        s['support'] = support
        s['resistance'] = resistance
        s['stop_loss'] = stop_loss
        
        actions = []
        if close <= stop_loss:
            actions.append("❌ 立即止损（跌破止损位）")
        elif close >= resistance:
            actions.append("🎯 突破压力，可加仓1/3")
        elif close <= support:
            actions.append("⚠️ 跌破支撑，减仓至50%")
        elif change_pct > 5:
            actions.append("📈 强势上涨，可部分止盈（卖出1/3）")
        elif change_pct > 2:
            actions.append("✅ 持有，关注压力位")
        elif change_pct > -2:
            actions.append("↔️ 小幅震荡，持有观望")
        else:
            actions.append("📉 回调明显，减仓至30%")
        
        if market_trend in ['明显下跌', '弱势'] and close > support:
            actions.append("大盘走弱，建议降低仓位")
        
        s['action_plan'] = '；'.join(actions)
        s['risk_level'] = '高' if abs(change_pct) > 5 else '中' if abs(change_pct) > 2 else '低'
        
        if change_pct > 3:
            s['technical_signal'] = "强势上涨"
        elif change_pct > 0:
            s['technical_signal'] = "小幅上涨"
        elif change_pct > -3:
            s['technical_signal'] = "小幅回调"
        else:
            s['technical_signal'] = "明显下跌"
    
    return stock_data

# ========== 选股策略（纯模拟）==========

class StockSelectionStrategies:
    """选股策略（教学示例）"""
    
    @staticmethod
    def high_roe_quality():
        return {
            'code': '600519', 'name': '贵州茅台',
            'logic': '高ROE质量策略：盈利能力强，现金流充裕（示例）',
            'signal': '企稳回升', 'suggestion': '逢低布局，支撑位1650，止损位1500'
        }
    
    @staticmethod
    def low_pe_rotation():
        return {
            'code': '600036', 'name': '招商银行',
            'logic': '低PE轮动：估值处于历史低位（示例）',
            'signal': '估值修复', 'suggestion': '分批建仓，支撑位35，止损位32'
        }
    
    @staticmethod
    def momentum_breakout():
        return {
            'code': '002594', 'name': '比亚迪',
            'logic': '动量突破：技术面突破箱体（示例）',
            'signal': '突破上行', 'suggestion': '回踩确认加仓，支撑位220，止损位200'
        }
    
    @staticmethod
    def sector_fund_inflow(sector_name):
        sector_map = {
            '军工': {'code': '000768', 'name': '中航西飞', 'logic': '军工板块资金流入（示例）', 'signal': '资金流入'},
            '新能源': {'code': '300014', 'name': '亿纬锂能', 'logic': '新能源板块流入（示例）', 'signal': '资金流入'},
            '黄金': {'code': '600988', 'name': '赤峰黄金', 'logic': '黄金板块流入（示例）', 'signal': '资金流入'}
        }
        return sector_map.get(sector_name, {'code': '600519', 'name': '贵州茅台', 'logic': 'default', 'signal': '企稳回升'})

def recommend_three_new_stocks(sector_flow):
    """推荐3只股票（模拟）"""
    recommendations = []
    used = set()
    
    # 策略1: 最强流入板块
    strong = [s for s in sector_flow if s['flow_3d'] == '持续流入' and s['strength'] == '强']
    if strong:
        stock = StockSelectionStrategies.sector_fund_inflow(strong[0]['name'])
        if stock['code'] not in used:
            stock['strategy'] = '资金流向策略'
            recommendations.append(stock)
            used.add(stock['code'])
    
    # 策略2: 高ROE
    stock = StockSelectionStrategies.high_roe_quality()
    if stock['code'] not in used:
        stock['strategy'] = '高ROE质量策略'
        recommendations.append(stock)
        used.add(stock['code'])
    
    # 策略3: 随机选一个
    import random
    stock = random.choice([
        StockSelectionStrategies.low_pe_rotation(),
        StockSelectionStrategies.momentum_breakout()
    ])
    if stock['code'] not in used:
        stock['strategy'] = '动量策略' if '动量' in stock['logic'] else '低PE轮动'
        recommendations.append(stock)
    
    return recommendations[:3]

# ========== 日志（纯本地）==========

def save_log(report):
    """保存报告到本地日志"""
    os.makedirs(LOG_DIR, exist_ok=True)
    log_file = os.path.join(LOG_DIR, f"briefing-{datetime.now().strftime('%Y-%m-%d')}.md")
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"💾 报告已保存: {log_file}")

# ========== 报告生成 ===========

def generate_educational_report(stock_data, indices, sectors, recommendations):
    """生成教育演示报告"""
    date_str = datetime.now().strftime('%Y-%m-%d')
    
    report = f"# 📈 股市数据分析示例 - {date_str}\n\n"
    report += "> ⚠️ **教学演示用途 only**\n"
    report += "> - 纯模拟数据，无真实API调用\n"
    report += "> - 不构成投资建议\n"
    report += "> - 仅供学习OpenClaw开发\n\n"
    
    report += "## 📊 大盘模拟数据\n"
    for name, data in indices.items():
        icon = "📈" if data['change_pct'] >= 0 else "📉"
        report += f"- {icon} {name}: {data['change_pct']:+.2f}%\n"
    report += "\n"
    
    report += "## 💰 板块资金流向（模拟）\n"
    for s in sectors:
        if s['flow_3d'] == '持续流入':
            icon = "📈"
        elif s['flow_3d'] == '流出':
            icon = "📉"
        else:
            icon = "➖"
        report += f"- {icon} **{s['name']}**：{s['flow_3d']}（{s['strength']}）\n"
    report += "\n"
    
    report += "## 🎯 技术分析示例\n\n"
    report += "| 标的 | 现价 | 信号 | 操作参考 | 风险 |\n"
    report += "|------|------|------|----------|------|\n"
    
    for s in stock_data:
        report += f"| {s['name']}({s['code']}) | {s['close']:.2f} | {s['technical_signal']} | {s['action_plan']} | {s['risk_level']} |\n"
    
    report += "\n"
    
    report += "## 🚀 股票筛选示例（5种策略）\n\n"
    report += "> ⚠️ 以下为策略演示，非真实推荐\n\n"
    
    for rec in recommendations:
        report += f"### {rec['name']} ({rec['code']})\n\n"
        report += f"- **策略**：{rec.get('strategy', '多因子')}\n"
        report += f"- **选股逻辑**：{rec['logic']}\n"
        report += f"- **信号**：{rec['signal']}\n"
        if rec.get('suggestion'):
            report += f"- **参考**：{rec['suggestion']}\n"
        report += "\n"
    
    report += "---\n"
    report += "⚠️ **重要声明**\n"
    report += "- 本报告完全离线生成，使用模拟数据\n"
    report += "- 不涉及任何真实API调用\n"
    report += "- 仅供学习OpenClaw开发技术\n"
    report += "- 不构成任何投资建议\n"
    
    return report

# ========== 主流程 ===========

def main():
    print("="*60)
    print("📈 股市数据分析 - 纯离线教学版 v15.0")
    print("="*60)
    print("🔒 安全特性：")
    print("  ✓ 无网络调用")
    print("  ✓ 无API密钥")
    print("  ✓ 纯模拟数据")
    print("  ✓ 本地日志存储")
    print("="*60)
    
    try:
        config = load_config()
        holdings = config['holdings']
        print(f"\n📊 分析标的：{len(holdings)} 只（模拟）")
        
        # 1. 获取模拟数据
        print("\n1️⃣ 生成模拟数据...")
        stock_data = []
        for stock in holdings:
            data = get_mock_stock_quote(stock['code'], stock['name'], stock['cost_price'], stock['shares'])
            stock_data.append(data)
            print(f"  {stock['name']}: {data['close']:.2f} ({data['change_pct']:+.2f}%)")
        
        # 2. 模拟大盘
        print("\n2️⃣ 大盘指数（模拟）")
        indices = get_mock_indices()
        for name, data in indices.items():
            print(f"  {name}: {data['change_pct']:+.2f}%")
        
        # 3. 板块流向
        print("\n3️⃣ 板块资金流向（模拟）")
        sectors = get_mock_sector_flow()
        for s in sectors[:3]:
            print(f"  {s['name']}: {s['flow_3d']}")
        
        # 4. 大盘趋势
        avg_change = sum(d['change_pct'] for d in indices.values()) / len(indices)
        trend_key = '强势上涨' if avg_change > 1 else '小幅上涨' if avg_change > 0 else '小幅回调' if avg_change > -1 else '明显下跌'
        
        # 5. 技术分析
        print("\n4️⃣ 技术分析计算...")
        stock_data = calculate_technical_levels(stock_data, trend_key)
        for s in stock_data:
            print(f"  {s['name']}: {s['technical_signal']}")
        
        # 6. 选股推荐
        print("\n5️⃣ 股票筛选（5种策略）...")
        recommendations = recommend_three_new_stocks(sectors)
        print(f"  推荐: {', '.join([r['name'] for r in recommendations])}")
        
        # 7. 生成报告
        print("\n6️⃣ 生成报告...")
        report = generate_educational_report(stock_data, indices, sectors, recommendations)
        save_log(report)
        
        # 8. 控制台输出
        print("\n" + "="*60)
        print("📋 报告预览（前500字）：")
        print("="*60)
        print(report[:500] + "...\n")
        
        print("✅ 完成！")
        print("💡 这是一个纯离线教学版本，无任何网络调用")
        return 0
        
    except Exception as e:
        print(f"\n❌ 失败: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())