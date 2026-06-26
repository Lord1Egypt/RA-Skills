#!/usr/bin/env python3
"""
Trump跨平台情绪分析器 V3.0 - T-Back系统
=====================================
核心概念：
- X平台: "西装面" (Suit Side) - 伪装性强，传播快
- Truth Social: "底牌面" (True Side) - 真实度高
- 双面转换 (Split Persona): 15分钟内X发利好+Truth发利空 = 市场诡异洗盘预警
"""

import json
from datetime import datetime, timedelta
from mood_analyzer import analyze_post
from typing import List, Dict, Tuple

# 平台权重配置
PLATFORM_WEIGHTS = {
    'X': 1.2,           # X/Twitter 权重稍高（传播更快）
    'Truth Social': 1.0  # Truth Social 权重
}

# 时间窗口（分钟）
CROSS_PLATFORM_WINDOW = 15  # 缩短到15分钟

# 共振强度系数
RESONANCE_K = 1.5

# T-Back阈值
SPLIT_PERSONA_THRESHOLD = 30  # 双面差异超过30分触发预警

def unified_t_back_processor(all_posts: List[Dict]) -> Dict:
    """
    统一的T-Back处理器
    
    伪代码逻辑：
    1. 按时间戳排序 (X + Truth)
    2. 计算"跨平台密度" - 15分钟内双平台发帖，k=1.5
    3. 检测"人格分裂" - X和Truth信号矛盾
    4. 汇总计算综合Clinical Score
    """
    
    # 1. 排序
    sorted_posts = sorted(all_posts, key=lambda x: x.get('timestamp', ''))
    
    print(f"\n📝 收到 {len(sorted_posts)} 条帖子")
    
    # 2. 分析每条帖子
    analyzed = []
    for post in sorted_posts:
        platform = post.get('platform', 'Unknown')
        text = post.get('text', '')
        
        result = analyze_post(text)
        result['platform'] = platform
        result['timestamp'] = post.get('timestamp', datetime.now().isoformat())
        
        # 平台权重
        weight = PLATFORM_WEIGHTS.get(platform, 1.0)
        result['weighted_t'] = result['t_back'] * weight
        
        analyzed.append(result)
    
    # 3. 计算跨平台共振 + 人格分裂检测
    resonance_events, split_persona_events = find_cross_platform_resonance(analyzed)
    
    # 4. 计算综合分数
    final_score = calculate_unified_score(analyzed, resonance_events, split_persona_events)
    
    return {
        'posts': analyzed,
        'resonance_events': resonance_events,
        'split_persona_events': split_persona_events,
        'final_score': final_score,
        'resonance_detected': len(resonance_events) > 0,
        'split_persona_detected': len(split_persona_events) > 0
    }

def find_cross_platform_resonance(posts: List[Dict]) -> List[Dict]:
    """
    查找跨平台共振事件
    如果15分钟内在两个平台都有发帖，触发共振
    同时检测"人格分裂" (Split Persona) 事件
    """
    resonance_events = []
    split_persona_events = []
    
    x_posts = [p for p in posts if p['platform'] == 'X']
    truth_posts = [p for p in posts if p['platform'] == 'Truth Social']
    
    for x_post in x_posts:
        for truth_post in truth_posts:
            # 解析时间
            try:
                x_time = datetime.fromisoformat(x_post.get('timestamp', '').replace('Z', '+00:00'))
                truth_time = datetime.fromisoformat(truth_post.get('timestamp', '').replace('Z', '+00:00'))
                time_diff = abs((x_time - truth_time).total_seconds() / 60)
            except:
                time_diff = 999  # 如果解析失败，跳过时间检测
            
            if time_diff <= CROSS_PLATFORM_WINDOW:
                # 共振事件
                resonance_events.append({
                    'x_post': x_post,
                    'truth_post': truth_post,
                    'time_diff_minutes': time_diff,
                    'combined_t': (x_post['t_back'] + truth_post['t_back']) / 2
                })
                
                # 检测人格分裂 (Split Persona)
                # X发利好(低T) + Truth发利空(高T) = 分裂
                # 或者 X发利空 + Truth发利好
                t_diff = abs(x_post['t_back'] - truth_post['t_back'])
                
                if t_diff >= SPLIT_PERSONA_THRESHOLD:
                    # 判断方向
                    if x_post['t_back'] < 40 and truth_post['t_back'] > 60:
                        # X利好 + Truth利空 = 诡异信号
                        split_persona_events.append({
                            'type': 'BULLISH_X_BEARISH_TRUTH',
                            'x_t': x_post['t_back'],
                            'truth_t': truth_post['t_back'],
                            'x_text': x_post.get('text', '')[:50],
                            'truth_text': truth_post.get('text', '')[:50],
                            'time_diff': time_diff,
                            'warning': '⚠️ 西装面利好 + 底牌面利空 = 人格分裂！市场将诡异洗盘！'
                        })
                    elif x_post['t_back'] > 60 and truth_post['t_back'] < 40:
                        # X利空 + Truth利好 = 分裂
                        split_persona_events.append({
                            'type': 'BEARISH_X_BULLISH_TRUTH',
                            'x_t': x_post['t_back'],
                            'truth_t': truth_post['t_back'],
                            'x_text': x_post.get('text', '')[:50],
                            'truth_text': truth_post.get('text', '')[:50],
                            'time_diff': time_diff,
                            'warning': '⚠️ 西装面利空 + 底牌面利好 = 人格分裂！反向收割信号！'
                        })
    
    return resonance_events, split_persona_events

def parse_timestamp(ts: str) -> datetime:
    """解析时间戳"""
    try:
        return datetime.fromisoformat(ts.replace('Z', '+00:00'))
    except:
        return datetime.now()

def calculate_unified_score(posts: List[Dict], resonance_events: List[Dict], split_persona_events: List[Dict] = None) -> Dict:
    """计算综合Clinical Score"""
    
    if split_persona_events is None:
        split_persona_events = []
    
    if not posts:
        return {'score': 0, 'level': 'UNKNOWN', 'description': '无数据'}
    
    # 基础分数：加权平均
    total_weight = sum(PLATFORM_WEIGHTS.get(p['platform'], 1.0) for p in posts)
    weighted_sum = sum(p['weighted_t'] for p in posts)
    base_score = weighted_sum / total_weight
    
    # 共振加成
    resonance_bonus = 0
    if resonance_events:
        avg_resonance_t = sum(e['combined_t'] for e in resonance_events) / len(resonance_events)
        resonance_bonus = (avg_resonance_t * (RESONANCE_K - 1)) / RESONANCE_K
    
    # 人格分裂加成 (Split Persona = 额外风险信号)
    split_bonus = 0
    if split_persona_events:
        split_bonus = 15  # 人格分裂额外+15分
    
    # 最终分数 (支持负轴：-100 到 +100)
    final_score = base_score + resonance_bonus + split_bonus
    final_score = min(100, max(-100, final_score))
    
    # 临床等级 (支持负轴)
    if final_score >= 80:
        level = "🔴 CRITICAL"
        description = "传教士模式-极端亢奋"
    elif final_score >= 60:
        level = "🟠 HIGH"
        description = "传教士模式-高度自信"
    elif final_score >= 40:
        level = "🟡 ELEVATED"
        description = "传教士模式-成就宣传"
    elif final_score >= 20:
        level = "🟢 WATCH"
        description = "传教士模式-轻微乐观"
    elif final_score > -20:
        level = "⚪ MASK"
        description = "面具模式-中性"
    elif final_score > -40:
        level = "🟢 WATCH"
        description = "掠食者模式-轻微不安"
    elif final_score > -60:
        level = "🟡 ELEVATED"
        description = "掠食者模式-负面施压"
    elif final_score > -80:
        level = "🟠 HIGH"
        description = "掠食者模式-高度攻击"
    else:
        level = "🔴 CRITICAL"
        description = "掠食者模式-极端威胁"
    
    return {
        'score': round(final_score, 1),
        'level': level,
        'description': description,
        'base_score': round(base_score, 1),
        'resonance_bonus': round(resonance_bonus, 1),
        'split_bonus': round(split_bonus, 1),
        'resonance_count': len(resonance_events),
        'split_persona_count': len(split_persona_events)
    }

def generate_resonance_alert(final_score: Dict, resonance_events: List[Dict], split_persona_events: list = None) -> str:
    """生成共振警告 + 人格分裂警告"""
    if split_persona_events is None:
        split_persona_events = []
    
    alerts = []
    
    # 人格分裂警告优先
    if split_persona_events and len(split_persona_events) > 0:
        for sp in split_persona_events:
            alerts.append(f"""
🎭 人格分裂警报 🎭
════════════════════════════════════
⚠️ 检测到"双面人格"信号！

🏛️ 西装面(X): T-Back = {sp['x_t']:.0f}
   "{sp['x_text']}..."

🎭 底牌面(Truth): T-Back = {sp['truth_t']:.0f}
   "{sp['truth_text']}..."

⏱️ 时间差: {sp['time_diff']:.0f}分钟

{sp['warning']}

⚠️ 市场将出现诡异双边洗盘！
════════════════════════════════════
""")
    
    # 共振警告
    if not final_score.get('resonance_detected') and not alerts:
        return ""
    
    dangerous_resonance = False
    for event in resonance_events:
        if event['combined_t'] >= 60:
            dangerous_resonance = True
            break
    
    if dangerous_resonance:
        alerts.append("""
🎆 共振警报 🎆
══════════════════════════════
检测到跨平台高风险共振！

X平台和Truth Social同时发出
强烈信号 - "真实风险"确认

建议：立即启动对冲预案
══════════════════════════════
""")
    
    return "\n".join(alerts)

# 测试
if __name__ == "__main__":
    # 模拟跨平台数据
    test_posts = [
        {'platform': 'X', 'text': 'TARIFFS ON CHINA! BIGGEST EVER!', 'timestamp': '2026-04-05T12:00:00'},
        {'platform': 'Truth Social', 'text': 'FED MUST LOWER RATES!', 'timestamp': '2026-04-05T12:15:00'},  # 15分钟内 - 共振！
        {'platform': 'X', 'text': 'GREAT SUCCESS!', 'timestamp': '2026-04-05T11:00:00'},
        {'platform': 'Truth Social', 'text': 'FAKE NEWS IS THE ENEMY!', 'timestamp': '2026-04-05T10:00:00'},
    ]
    
    print("=" * 70)
    print("🦞 跨平台T-Index共振分析器 - 测试")
    print("=" * 70)
    
    result = unified_t_back_processor(test_posts)
    
    print(f"\n📊 综合Clinical Score: {result['final_score']['score']}")
    print(f"   等级: {result['final_score']['level']}")
    print(f"   说明: {result['final_score']['description']}")
    print(f"   基础分: {result['final_score']['base_score']}")
    print(f"   共振加成: {result['final_score']['resonance_bonus']}")
    print(f"   共振事件: {result['final_score']['resonance_count']}个")
    
    if result['resonance_events']:
        print(f"\n🔗 共振详情:")
        for i, e in enumerate(result['resonance_events']):
            print(f"   事件{i+1}: X={e['x_post']['t_back']:.0f} | Truth={e['truth_post']['t_back']:.0f} | 时间差={e['time_diff_minutes']:.0f}分钟")
    
    alert = generate_resonance_alert(result['final_score'], result['resonance_events'])
    if alert:
        print(alert)
