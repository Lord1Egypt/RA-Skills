#!/usr/bin/env python3
"""
v4.0 纪律层模块 - 4 大守护能力

1. risk_reward - 风险收益比量化
2. emotion_guard - 情绪化交易拦截
3. plan_freezer - 入场计划冻结
4. leverage_gate - 杠杆使用门禁

基于 memory/principle-trading-discipline.md
"""
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ============================================================
# 1. 风险收益比量化
# ============================================================

def calculate_risk_reward(current_price, targets):
    """
    计算风险收益比
    
    Args:
        current_price: float, 当前价
        targets: dict {
            'conservative_target': X,  # 保守目标
            'neutral_target': Y,       # 中性目标
            'aggressive_target': Z,    # 乐观目标
            'tech_stop': A,            # 技术止损
            'hard_stop': B,            # 硬止损
            'extreme_stop': C,         # 极限止损
        }
    
    Returns:
        dict 包含 6 大数据和评级
    """
    if not targets:
        return None
    
    cp = current_price
    
    upside = {
        'conservative': (targets.get('conservative_target', cp) - cp) / cp * 100,
        'neutral': (targets.get('neutral_target', cp) - cp) / cp * 100,
        'aggressive': (targets.get('aggressive_target', cp) - cp) / cp * 100,
    }
    
    downside = {
        'tech': (cp - targets.get('tech_stop', cp)) / cp * 100,
        'hard': (cp - targets.get('hard_stop', cp)) / cp * 100,
        'extreme': (cp - targets.get('extreme_stop', cp)) / cp * 100,
    }
    
    # 风险收益比（取保守/技术止损作为主要参考）
    rr = {
        'conservative': upside['conservative'] / downside['tech'] if downside['tech'] > 0 else 0,
        'neutral': upside['neutral'] / downside['hard'] if downside['hard'] > 0 else 0,
        'aggressive': upside['aggressive'] / downside['extreme'] if downside['extreme'] > 0 else 0,
    }
    
    main_rr = rr['neutral']
    
    if main_rr >= 3:
        grade = '⭐⭐⭐⭐⭐ 强烈推荐'
        advice = '入场'
    elif main_rr >= 2:
        grade = '⭐⭐⭐⭐ 推荐'
        advice = '入场'
    elif main_rr >= 1:
        grade = '⭐⭐⭐ 谨慎'
        advice = '小仓位试探'
    else:
        grade = '❌ 不入场'
        advice = '风险大于收益，等待更好机会'
    
    return {
        'upside': upside,
        'downside': downside,
        'risk_reward': rr,
        'grade': grade,
        'advice': advice,
        'main_rr': main_rr,
    }

def format_risk_reward(result, name=''):
    """格式化风险收益比输出"""
    if not result:
        return "❌ 无法计算风险收益比"
    
    lines = []
    if name:
        lines.append(f"📊 {name} 风险收益比分析\n")
    
    u = result['upside']
    d = result['downside']
    r = result['risk_reward']
    
    lines.append("📈 上涨空间(3 档):")
    lines.append(f"  保守(短线止盈): +{u['conservative']:.2f}%")
    lines.append(f"  中性(趋势目标): +{u['neutral']:.2f}%")
    lines.append(f"  乐观(极端目标): +{u['aggressive']:.2f}%")
    
    lines.append("\n📉 下跌空间(3 档):")
    lines.append(f"  技术止损(跌均线): -{d['tech']:.2f}%")
    lines.append(f"  硬止损(破位):    -{d['hard']:.2f}%")
    lines.append(f"  极限止损(趋势变): -{d['extreme']:.2f}%")
    
    lines.append("\n⚖️ 风险收益比:")
    lines.append(f"  保守: {r['conservative']:.2f}:1")
    lines.append(f"  中性: {r['neutral']:.2f}:1")
    lines.append(f"  乐观: {r['aggressive']:.2f}:1")
    
    lines.append(f"\n🎯 评级: {result['grade']}")
    lines.append(f"💡 建议: {result['advice']}")
    
    return '\n'.join(lines)

# ============================================================
# 2. 情绪化交易拦截器
# ============================================================

EMOTION_PATTERNS = {
    'fomo': {
        'keywords': ['追涨', '追买', '怕错过', '别人都赚', '错过了', '再升'],
        'check': lambda ctx: ctx.get('recent_gain_30d', 0) > 30,
        'message': "🚨 FOMO 心态拦截!\n你想买的票近期已涨 {recent_gain}%\n按《纪律》:暂停 24 小时\n建议: 加入盯盘 等回调 -10% 后再入"
    },
    'compensate': {
        'keywords': ['太保守', '应该多卖', '错过了', '保守了'],
        'check': lambda ctx: ctx.get('recent_reflection', False),
        'message': "🚨 反思补偿拦截!\n你刚反思过保守\n按《纪律》:不因后悔改变规则\n建议:严格按 当前计划 执行"
    },
    'revenge': {
        'keywords': ['赶紧赚回', '补一下', '亏了再赌'],
        'check': lambda ctx: ctx.get('last_24h_loss', 0) > 10000,
        'message': "🚨 报复性交易拦截!\n24h 内你亏损 ¥{loss}\n按《纪律》:强制 24h 冷静期\n建议:不立刻新决策"
    },
    'bottom_fishing': {
        'keywords': ['便宜了', '跌得多', '抄底', '低位'],
        'check': lambda ctx: ctx.get('has_bottom_signal', True) == False,
        'message': "🚨 抄底心态拦截!\n仅凭'便宜'不是入场理由\n缺少 多重底部信号\n建议:等 3/3 信号确认 再入"
    }
}

def check_emotional_trading(user_input, context=None):
    """
    检查用户输入是否触发情绪化交易
    
    Args:
        user_input: 用户输入文本
        context: 上下文字典 (历史信息)
    
    Returns:
        list of 触发的拦截项
    """
    triggered = []
    user_lower = user_input.lower() if user_input else ''
    context = context or {}
    
    for name, pattern in EMOTION_PATTERNS.items():
        # 检查关键词
        keyword_hit = any(kw in user_input for kw in pattern['keywords'])
        # 检查上下文条件
        try:
            condition_hit = pattern['check'](context)
        except:
            condition_hit = False
        
        if keyword_hit or condition_hit:
            triggered.append({
                'pattern': name,
                'message': pattern['message'],
                'severity': 'high'
            })
    
    return triggered

# ============================================================
# 3. 入场计划冻结器
# ============================================================

PLANS_DIR = ROOT / "data" / "plans"
PLANS_DIR.mkdir(parents=True, exist_ok=True)

def create_entry_plan(code, name, entry_price, position_size, targets):
    """
    创建入场计划并锁定
    
    Args:
        code: 股票代码
        name: 股票名称
        entry_price: 入场价
        position_size: 仓位金额
        targets: dict 出场计划
    """
    plan = {
        'code': code,
        'name': name,
        'entry_price': entry_price,
        'position_size': position_size,
        'targets': targets,
        'created_at': datetime.now().isoformat(),
        'locked': True,
        'modifications': []
    }
    
    plan_file = PLANS_DIR / f"{code}_{datetime.now():%Y%m%d_%H%M%S}.json"
    with open(plan_file, 'w', encoding='utf-8') as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)
    
    return plan_file

def attempt_modify_plan(code, reason='want_to_add'):
    """
    尝试修改已锁定的入场计划 - 触发拦截
    """
    return {
        'allowed': False,
        'message': f"""🚨 入场计划已锁定!

按《纪律》第三、五条:
  ❌ 入场后不得新增止盈条件
  ❌ 不因 '再涨一点' 而改

允许的修改:
  ✅ 触发硬止损时 紧急减仓
  ✅ 重大利空 重新评估
  ✅ 周期性 整体复盘

你现在想改的属于以下哪种?
  1. 触发硬止损（允许）
  2. 重大利空（允许）
  3. 单纯想加挂止盈（❌ 拦截）
  4. 单纯想改止损（❌ 拦截）

请明确告知 是否符合允许的修改类型
""",
        'severity': 'medium'
    }

# ============================================================
# 4. 杠杆使用门禁
# ============================================================

LEVERAGE_GATES = {
    'systematic': {
        'question': '这是 体系性策略 还是 单次博弈?',
        'options': ['体系性', '单次博弈'],
        'pass_condition': lambda ans: ans == '体系性'
    },
    'verified': {
        'question': '正期望策略 已验证 多少次成功?',
        'options': ['< 5 次', '5-20 次', '> 20 次'],
        'pass_condition': lambda ans: ans == '> 20 次'
    },
    'stress_test': {
        'question': '如果该票 -20% 你能否还款?',
        'options': ['能', '不能'],
        'pass_condition': lambda ans: ans == '能'
    }
}

def check_leverage_request(amount, stock_code=''):
    """
    检查融资请求 - 3 道关卡
    """
    return {
        'allowed': False,
        'message': f"""🚨 杠杆使用门禁! (3 道关卡)

你想用融资买入 {stock_code} ({amount:,.0f} 元)

关卡 1: 体系性检查
  ❓ 这是 体系性策略 还是 单次博弈?
  你的回答: 影响是否通过

关卡 2: 正期望验证
  ❓ 你的策略 已验证 多少次成功?
  • > 20 次 → 通过
  • < 20 次 → ⚠️ 风险大

关卡 3: 压力测试
  ❓ 如果 -20% 你能否还款?
  • 能 → 通过
  • 不能 → ❌ 拒绝

3/3 通过 才进入下一步
否则 ❌ 拒绝执行融资买入

按《纪律》: 未建立可验证正期望策略前 不得使用杠杆
""",
        'severity': 'critical',
        'gates': LEVERAGE_GATES
    }

# ============================================================
# 综合纪律检查（buy 决策前自动调用）
# ============================================================

def comprehensive_check(stock_code, action='buy', context=None):
    """
    综合纪律检查 - 入场前必跑
    
    Returns:
        dict {
            'pass': bool,
            'warnings': list,
            'blockers': list,
        }
    """
    context = context or {}
    result = {
        'pass': True,
        'warnings': [],
        'blockers': [],
    }
    
    # 1. 情绪化检查
    emotions = check_emotional_trading(
        context.get('user_request', ''),
        context
    )
    if emotions:
        result['warnings'].extend(emotions)
    
    # 2. 仓位检查
    if action == 'buy':
        position_pct = context.get('after_buy_position_pct', 0)
        if position_pct > 50:
            result['blockers'].append({
                'type': 'position_limit',
                'message': f'单股仓位将达 {position_pct:.1f}%，超过 50% 上限'
            })
            result['pass'] = False
        elif position_pct > 40:
            result['warnings'].append({
                'type': 'position_warning',
                'message': f'单股仓位将达 {position_pct:.1f}%，接近 50% 上限'
            })
    
    # 3. 持仓数检查
    holding_count = context.get('holding_count', 0)
    if action == 'buy' and not context.get('is_existing_holding', False):
        if holding_count >= 5:
            result['blockers'].append({
                'type': 'holding_count',
                'message': '已持仓 5 只，达到上限，新建仓需先减仓 1 只'
            })
            result['pass'] = False
    
    # 4. 杠杆检查
    if context.get('using_leverage', False):
        leverage_check = check_leverage_request(
            context.get('amount', 0),
            stock_code
        )
        result['blockers'].append({
            'type': 'leverage',
            'message': leverage_check['message']
        })
    
    return result

def format_check_result(result):
    """格式化纪律检查结果"""
    lines = []
    if result['pass'] and not result['warnings']:
        return "✅ 纪律检查通过"
    
    if result['blockers']:
        lines.append("🚨 拦截项 (必须解决):")
        for b in result['blockers']:
            lines.append(f"  • {b['message']}")
    
    if result['warnings']:
        lines.append("\n⚠️ 警告项 (建议关注):")
        for w in result['warnings']:
            if isinstance(w, dict):
                lines.append(f"  • {w.get('message', str(w))}")
    
    return '\n'.join(lines)

# ============================================================
# 测试入口
# ============================================================

if __name__ == '__main__':
    # 测试 风险收益比
    print("="*60)
    print("测试 1: 风险收益比")
    print("="*60)
    result = calculate_risk_reward(
        current_price=650,
        targets={
            'conservative_target': 670,
            'neutral_target': 688,
            'aggressive_target': 720,
            'tech_stop': 640,
            'hard_stop': 615,
            'extreme_stop': 570,
        }
    )
    print(format_risk_reward(result, '罗博特科'))
    
    # 测试 情绪化
    print("\n" + "="*60)
    print("测试 2: 情绪化拦截")
    print("="*60)
    triggered = check_emotional_trading(
        '我想追买再升科技，怕错过了',
        {'recent_gain_30d': 45}
    )
    if triggered:
        for t in triggered:
            print(f"⚠️ 触发: {t['pattern']}")
            print(f"  {t['message'].format(recent_gain=45)}")
    
    # 测试 综合检查
    print("\n" + "="*60)
    print("测试 3: 综合纪律检查")
    print("="*60)
    result = comprehensive_check(
        '300757',
        'buy',
        {
            'user_request': '想加仓罗博，反正之前太保守',
            'recent_reflection': True,
            'after_buy_position_pct': 35,
            'holding_count': 5,
            'is_existing_holding': True,
            'using_leverage': False,
        }
    )
    print(format_check_result(result))


# ============================================================
# v4.2 新增模块（基于 5/29 复盘）
# ============================================================

def check_action_necessity(stock, action, context=None):
    """铁律 4: '不操作' 为默认选项
    
    任何操作建议前必跑此检查
    """
    context = context or {}
    
    if action in ['reduce', 'sell']:
        questions = [
            "Q1: 这只票的入场计划中是否写明了减仓条件?",
            "Q2: 当前价格是否触发了入场时设的减仓位?",
            "Q3: 不操作会有什么实质损失?(机会成本 vs 实际损失)",
            "Q4: 是否同板块集中度过高才考虑换仓?",
            "Q5: 7 天内是否已经对这只票操作过?",
        ]
        warnings = []
        
        # 检查是否已浮盈 +30% 小仓位（铁律 5）
        if context.get('profit_pct', 0) > 30 and context.get('position_size_pct', 100) < 5:
            warnings.append(f"⚠️ 该仓位浮盈 +{context['profit_pct']:.1f}% 且仓位仅 {context['position_size_pct']:.1f}% - 受铁律5保护")
        
        # 检查频次（铁律 8）
        if context.get('last_action_hours_ago', 999) < 24:
            warnings.append(f"⚠️ 24h 内已操作过 - 触发铁律 8 频次限制")
        
        # 检查卖飞防御（铁律 9）
        if context.get('recent_sell_then_rose', 0) > 5:
            warnings.append(f"⚠️ 卖出后该票涨 +{context['recent_sell_then_rose']:.1f}% - 触发铁律 9 卖飞防御")
        
        return {
            'default_recommendation': '不操作',
            'questions_required': questions,
            'warnings': warnings,
            'must_pass_all': True,
        }
    return {'default_recommendation': 'PROCEED'}


def check_sector_concentration(new_buy_stock, new_buy_sector, current_portfolio):
    """铁律 6: 同板块集中度上限
    
    加仓前必查
    """
    same_sector_total = 0
    related_sectors = {
        'CPO': ['CPO', '光通信', '光模块', '光芯片'],
        'CoWoS': ['CoWoS', '先进封装', '封测'],
        'MLCC': ['MLCC', '被动元件', '电容'],
        '半导体': ['半导体', '芯片', '存储'],
    }
    
    for pos in current_portfolio:
        pos_sector = pos.get('sector', '')
        # 同板块或相关板块
        for category, terms in related_sectors.items():
            if any(t in new_buy_sector for t in terms) and any(t in pos_sector for t in terms):
                same_sector_total += pos.get('market_value', 0)
                break
    
    total_portfolio = sum(p.get('market_value', 0) for p in current_portfolio)
    new_buy_value = new_buy_stock.get('value', 0)
    
    concentration_after = (same_sector_total + new_buy_value) / (total_portfolio + new_buy_value) if total_portfolio > 0 else 0
    
    if concentration_after > 0.8:
        return {
            'status': 'BLOCK',
            'message': f'🚨 加仓后同板块集中度 {concentration_after*100:.1f}% > 80%，禁止加仓'
        }
    elif concentration_after > 0.6:
        return {
            'status': 'WARN',
            'message': f'⚠️ 加仓后同板块集中度 {concentration_after*100:.1f}% > 60%，过度集中'
        }
    return {'status': 'PASS'}


def detect_user_phase(portfolio_state):
    """铁律 10: 用户阶段识别
    
    根据用户当前状态调整建议风格
    """
    cash_ratio = portfolio_state.get('cash_ratio', 0.5)
    realized_profit = portfolio_state.get('realized_profit_this_month', 0)
    unrealized_profit_pct = portfolio_state.get('unrealized_profit_pct', 0)
    
    # 收割期：已落袋 ¥100 万+ 或 浮盈占总资产 50%+
    if realized_profit > 1000000 or unrealized_profit_pct > 0.5:
        return {
            'phase': 'harvesting',
            'description': '🔴 收割期 - 保护胜利果实',
            'recommendation_style': '减少推荐操作 / 主推减仓 + 现金为王',
            'advice': '已落袋 + 浮盈巨大 → 不需要 频繁换仓 追加收益'
        }
    
    # 建仓期：现金 > 60%
    if cash_ratio > 0.6:
        return {
            'phase': 'building',
            'description': '🟢 建仓期 - 积极寻找机会',
            'recommendation_style': '积极推荐主线龙头操作',
            'advice': '现金充裕 → 主动 锁定主线 + 龙头入场'
        }
    
    # 持有期：50-70% 持仓
    if 0.3 < cash_ratio < 0.6:
        return {
            'phase': 'holding',
            'description': '🟡 持有期 - 让利润奔跑',
            'recommendation_style': '减少操作推荐 / 重点持有',
            'advice': '持仓适中 → 主线龙头 持有 / 不轻易换仓'
        }
    
    return {'phase': 'normal', 'description': '⚖️ 正常状态'}


def winning_position_protection(stock_holding):
    """铁律 5: 已浮盈 +30% 小仓位特殊保护"""
    profit_pct = stock_holding.get('profit_pct', 0)
    position_pct = stock_holding.get('position_size_pct', 100)
    
    if profit_pct > 30 and position_pct < 5:
        return {
            'protected': True,
            'reason': f'浮盈 +{profit_pct:.1f}% + 仓位 {position_pct:.1f}% < 5% = 受保护',
            'recommendation': '不主动建议减仓 / Let winners run',
            'override_conditions': [
                '触发入场时设的减仓位',
                '出现重大利空（业绩/监管/财务造假）',
                '用户主动要求'
            ]
        }
    return {'protected': False}


def post_action_review(action_log):
    """铁律 9: 卖飞反思 + 24h 禁言"""
    if not action_log.get('was_sell'):
        return {'block': False}
    
    rise_after = action_log.get('rise_pct_after_sell', 0)
    hours_since = action_log.get('hours_since_action', 0)
    
    if rise_after > 5 and hours_since < 24:
        return {
            'block': True,
            'message': f'🚨 卖飞防御触发：该票卖出后涨 +{rise_after:.1f}%',
            'duration': f'24h 禁止对该票新操作建议',
            'remaining_hours': max(0, 24 - hours_since)
        }
    return {'block': False}


def comprehensive_v42_check(stock_code, action, full_context):
    """v4.2 综合纪律检查 - 决策前必跑"""
    results = {
        'pass': True,
        'blockers': [],
        'warnings': [],
        'default_recommendation': None,
    }
    
    # 1. 操作必要性
    necessity = check_action_necessity(stock_code, action, full_context.get('stock_context', {}))
    if necessity.get('default_recommendation') == '不操作':
        results['default_recommendation'] = '不操作 (铁律 4)'
        results['warnings'].extend(necessity.get('warnings', []))
    
    # 2. 同板块集中度
    if action == 'buy' and full_context.get('new_buy'):
        conc = check_sector_concentration(
            full_context['new_buy'],
            full_context['new_buy'].get('sector', ''),
            full_context.get('portfolio', [])
        )
        if conc['status'] == 'BLOCK':
            results['blockers'].append(conc['message'])
            results['pass'] = False
        elif conc['status'] == 'WARN':
            results['warnings'].append(conc['message'])
    
    # 3. 用户阶段
    phase = detect_user_phase(full_context.get('portfolio_state', {}))
    if phase['phase'] == 'harvesting' and action in ['buy', 'add']:
        results['warnings'].append(f"📊 用户当前 {phase['description']} - {phase['advice']}")
    
    # 4. winning position 保护
    if action in ['reduce', 'sell'] and full_context.get('stock_context'):
        protect = winning_position_protection(full_context['stock_context'])
        if protect.get('protected'):
            results['warnings'].append(f"🛡 {protect['reason']} - {protect['recommendation']}")
    
    # 5. 卖飞防御
    if full_context.get('action_log'):
        block = post_action_review(full_context['action_log'])
        if block.get('block'):
            results['blockers'].append(block['message'])
            results['pass'] = False
    
    return results
