#!/usr/bin/env python3
"""
Trump Mood & T-Index Backend Module
核心情绪分析和市场敏感度计算
"""

import re
from datetime import datetime
from typing import Dict, List, Tuple

# ========== 情绪指数系统 ==========
POSITIVE_WORDS = {
    'great': 1.0, 'amazing': 1.2, 'wonderful': 1.0, 'fantastic': 1.2,
    'incredible': 1.2, 'tremendous': 1.5, 'best': 1.3, 'biggest': 1.0,
    'beautiful': 1.2, 'perfect': 1.2, 'success': 1.5, 'winning': 1.8,
    'victory': 1.8, 'strong': 1.0, 'powerful': 1.2, 'smart': 0.8,
    'brilliant': 1.2, 'genius': 1.5, 'happy': 0.8, 'love': 1.0,
    'excited': 1.0, 'historic': 1.2, 'unbelievable': 1.0, 'phenomenal': 1.3,
    'good': 0.5, 'nice': 0.5, 'win': 1.5, 'proud': 1.0, 'celebrate': 1.2
}

NEGATIVE_WORDS = {
    'hell': -2.5, 'disaster': -2.0, 'terrible': -1.5, 'horrible': -1.8,
    'failed': -1.5, 'failing': -1.5, 'loser': -2.5, 'losers': -2.5,
    'fake': -1.0, 'corrupt': -1.8, 'crooked': -2.0, 'weak': -1.2,
    'stupid': -2.0, 'dumb': -1.8, 'pathetic': -2.0, 'sad': -1.0,
    'disgrace': -2.0, 'shame': -1.5, 'disgusting': -2.0, 'dangerous': -1.5,
    'threat': -1.5, 'destroy': -2.5, 'destroyed': -2.5, 'attack': -2.0,
    'defeat': -1.8, 'surrender': -2.0, 'pay the price': -3.0,
    'catastrophe': -2.5, 'mess': -1.5, 'worst': -2.0, 'bad': -1.0,
    'nasty': -1.8, 'evil': -2.0, 'radical': -1.0, 'crazy': -1.5,
    'insane': -1.8, 'reign down': -3.0, 'enemy': -1.5, 'war': -2.0,
    'welfare': -1.5
}

# ========== T-Index 市场敏感度系统 V2.0 ==========
# 病理学关联：区分"市场毒性"与"叙事噪音"

# 市场毒性词 (Market Toxic) - 直接影响现金流和贴现率
# 权重: 2.0x + 强制加分
MARKET_TOXINS = {
    'TARIFFS': 30, 'TARIFF': 30,
    'CHINA': 20, 'CHINESE': 20,
    'FED': 25, 'POWELL': 25,
    'INTEREST': 25, 'RATES': 20,
    'SANCTIONS': 30, 'SANCTION': 30,
    'TRADE WAR': 40, 'DEVALUATION': 30,
    'DEPORT': 25, 'DEPORTATION': 30,
    'DOGE': 20, 'BUDGET': 20,
    'RECESSION': 30, 'DEPRESSION': 35,
    'CRASH': 35, 'COLLAPSE': 35,
    'DEFAULTS': 30, 'DEBT CEILING': 30,
    'WELFARE': 15
}

# 叙事噪音词 (Narrative Noise) - 影响情绪但不影响EPS
# 权重: 0.5x - 抑制噪音
NARRATIVE_NOISE = {
    'FAKE NEWS': 5, 'WITCH HUNT': 5,
    'LOSER': 3, 'LOSERS': 3,
    'SAD': 2, 'CORRUPT': 5,
    'CROOKED': 5, 'RIGGED': 5,
    'EVIL': 5, 'NASTY': 3,
    'PATHETIC': 3, 'DUMB': 3,
    'STUPID': 3
}

# 中等影响词
MEDIUM_IMPACT = {
    'MICRON': 20, 'NVIDIA': 15, 'APPLE': 15, 'TESLA': 15,
    'TSMC': 20, 'SEMICONDUCTOR': 20, 'CHIPS': 15,
    'OIL': 15, 'GAS': 10, 'ENERGY': 10,
    'GOLD': 10, 'SILVER': 10, 'STOCK': 10, 'MARKET': 10, 'MARKETS': 10,
    'BITCOIN': 15, 'CRYPTO': 15
}

# 地缘政治词
GEOPOLITICAL = {
    'IRAN': 20, 'RUSSIA': 15, 'UKRAINE': 15,
    'ISRAEL': 15, 'WAR': 20, 'MILITARY': 15,
    'STRAIT': 25, 'NUCLEAR': 20, 'HEZBOLLAH': 15
}


def calculate_mood_score(text: str) -> float:
    """计算情绪指数 (-10 到 +10)"""
    text_lower = text.lower()
    score = 0
    
    for word, weight in POSITIVE_WORDS.items():
        if word in text_lower:
            score += weight
    
    for word, weight in NEGATIVE_WORDS.items():
        if word in text_lower:
            score += weight
    
    caps_words = re.findall(r'\b[A-Z]{4,}\b', text)
    score += len(caps_words) * 0.4
    
    exclamation_count = text.count('!')
    if exclamation_count >= 2:
        score += exclamation_count * 0.25
    
    geo_count = sum(1 for word in GEOPOLITICAL if word in text.lower())
    if geo_count > 0:
        score *= (1 + geo_count * 0.2)
    
    return max(-10, min(10, round(score, 1)))


def get_mood_label(score: float) -> str:
    if score <= -7: return "🔴 暴怒"
    elif score <= -4: return "🟠 愤怒"
    elif score <= -1: return "🟡 不满"
    elif score <= 1: return "⚪ 中性"
    elif score <= 4: return "🟢 自信"
    elif score <= 7: return "🔵 亢奋"
    else: return "🟣 狂喜"


def calculate_t_back(text: str) -> float:
    """
    计算T-Back市场敏感度 V3.0 (-100 到 +100)
    
    极性判定逻辑：
    - 负轴 (Predator/掠食者): 威胁、攻击性内容 → 市场恐慌
    - 正轴 (Missionary/传教士): 成就、宣传内容 → 市场亢奋
    - 0轴 (Mask/面具): 中性内容
    """
    text_upper = text.upper()
    text_lower = text.lower()
    score = 0
    
    # ==================== 强度计算 ====================
    # 1. 大写字母比例 (情绪强度)
    alpha_chars = [c for c in text if c.isalpha()]
    if alpha_chars:
        caps_count = sum(1 for c in text if c.isupper())
        intensity = (caps_count / len(alpha_chars)) * 40
    else:
        intensity = 0
    
    # 2. 感叹号强度
    intensity += min(text.count('!'), 5) * 4
    
    # 3. 市场毒性词 (Market Toxic) - 核心加权
    for word, weight in MARKET_TOXINS.items():
        if word in text_upper:
            intensity += weight * 2.0
    
    # 4. 叙事噪音词 (Narrative Noise) - 抑制
    noise_count = 0
    for word, weight in NARRATIVE_NOISE.items():
        if word in text_upper:
            intensity += weight * 0.5
            noise_count += 1
    
    # 5. 中等影响词
    for word, weight in MEDIUM_IMPACT.items():
        if word in text_upper:
            intensity += weight
    
    # 6. 地缘政治 (放大器)
    geo_count = 0
    for word, weight in GEOPOLITICAL.items():
        if word in text_upper:
            intensity += weight * 0.8
            geo_count += 1
    
    # 7. 病理学关联：如果市场毒性+地缘政治同时出现，额外加成
    has_toxin = any(w in text_upper for w in MARKET_TOXINS)
    if has_toxin and geo_count > 0:
        intensity *= 1.3
    
    # ==================== 极性判定 ====================
    # 负面/攻击性关键词 (进入负轴)
    AGGRESSIVE_KEYWORDS = [
        'THREAT', 'DESTROY', 'DESTRUCTION', 'WAR', 'ATTACK', 'KILL',
        'HELL', 'DISASTER', 'TERRIBLE', 'HORRIBLE', 'DANGER', 'WARNING',
        'FAIL', 'LOSER', 'ENEMY', 'CRIMINAL', 'TRAITOR', 'SURRENDER',
        'REVENGE', 'PAY THE PRICE', 'DESTROYED', 'WRECK', 'CRUSH',
        'ANNIHILATE', 'WIPE OUT', 'FINISH', 'END IT', 'DEVASTATE',
        'WELFARE'
    ]
    
    # 正面/成就关键词 (进入正轴)
    BOASTING_KEYWORDS = [
        'GREAT', 'AMAZING', 'BEST', 'WINNING', 'SUCCESS', 'VICTORY',
        'TREMENDOUS', 'HISTORIC', 'PHENOMENAL', 'INcredible', 'BRILLIANT',
        'STRONG', 'POWERFUL', 'PROUD', 'CELEBRATE', 'BIGGEST', 'FIRST',
        'UNBELIEVABLE', 'MASSIVE', 'BIG', 'HUGE', 'SUCCESSFUL', 'WIN'
    ]
    
    # 检测极性
    is_aggressive = any(kw in text_upper for kw in AGGRESSIVE_KEYWORDS)
    is_boasting = any(kw in text_upper for kw in BOASTING_KEYWORDS)
    
    # 特殊判断：关税/制裁/威胁 = 强制负轴
    forced_negative = any(w in text_upper for w in ['TARIFFS', 'SANCTIONS', 'DEPORT', 'WAR', 'TARIFF'])
    
    # 极性赋值
    if forced_negative:
        # 关税/制裁 = 强制负轴，忽略其他
        polarity = -1
    elif is_aggressive and not is_boasting:
        # 负轴：掠食者模式
        polarity = -1
    elif is_boasting and not is_aggressive:
        # 正轴：传教士模式
        polarity = 1
    elif is_aggressive and is_boasting:
        # 混合：看哪个权重更高
        aggressive_count = sum(1 for kw in AGGRESSIVE_KEYWORDS if kw in text_upper)
        boasting_count = sum(1 for kw in BOASTING_KEYWORDS if kw in text_upper)
        polarity = 1 if boasting_count > aggressive_count else -1
    else:
        # 中性：0轴
        polarity = 0
    
    # 计算最终分数
    final_score = intensity * polarity
    
    return max(-100, min(100, round(final_score, 1)))


def get_t_back_level(score: float) -> Tuple[str, str]:
    """获取T-Back等级 (支持负轴)"""
    abs_score = abs(score)
    
    if score > 0:
        # 正轴：传教士模式
        if abs_score >= 80: return "🔴 CRITICAL", "传教士模式-极端亢奋"
        elif abs_score >= 60: return "🟠 HIGH", "传教士模式-高度自信"
        elif abs_score >= 40: return "🟡 ELEVATED", "传教士模式-成就宣传"
        elif abs_score >= 20: return "🟢 WATCH", "传教士模式-轻微乐观"
        else: return "⚪ MASK", "面具模式-中性"
    elif score < 0:
        # 负轴：掠食者模式
        if abs_score >= 80: return "🔴 CRITICAL", "掠食者模式-极端威胁"
        elif abs_score >= 60: return "🟠 HIGH", "掠食者模式-高度攻击"
        elif abs_score >= 40: return "🟡 ELEVATED", "掠食者模式-负面施压"
        elif abs_score >= 20: return "🟢 WATCH", "掠食者模式-轻微不安"
        else: return "⚪ MASK", "面具模式-中性"
    else:
        return "⚪ MASK", "面具模式-中性"


def analyze_post(text: str, timestamp: str = None) -> Dict:
    """分析单条帖子"""
    mood = calculate_mood_score(text)
    t_back = calculate_t_back(text)
    mood_label = get_mood_label(mood)
    t_level, t_desc = get_t_back_level(t_back)
    keywords = extract_keywords(text)
    
    return {
        'text': text[:100] + '...' if len(text) > 100 else text,
        'timestamp': timestamp or datetime.now().isoformat(),
        'mood_score': mood,
        'mood_label': mood_label,
        't_back': t_back,
        't_level': t_level,
        't_desc': t_desc,
        'keywords': keywords,
        'toxicity_type': 'MARKET_TOXIN' if keywords['toxic'] else 'NARRATIVE_NOISE' if keywords['noise'] else 'NEUTRAL'
    }


def extract_keywords(text: str) -> Dict:
    """提取帖子中的关键词及类型"""
    text_upper = text.upper()
    result = {
        'toxic': [],      # 市场毒性词
        'noise': [],     # 叙事噪音词  
        'medium': [],    # 中等影响词
        'geo': []        # 地缘政治词
    }
    
    for word in MARKET_TOXINS:
        if word in text_upper:
            result['toxic'].append(word)
    
    for word in NARRATIVE_NOISE:
        if word in text_upper:
            result['noise'].append(word)
    
    for word in MEDIUM_IMPACT:
        if word in text_upper:
            result['medium'].append(word)
    
    for word in GEOPOLITICAL:
        if word in text_upper:
            result['geo'].append(word)
    
    return result


# ========== 市场数据模块 ==========
def get_market_data():
    """获取市场数据（需要yfinance）"""
    try:
        import yfinance as yf
        
        # 获取SPX和VIX
        spx = yf.download("^GSPC", period="1d", interval="1m")
        vix = yf.download("^VIX", period="1d", interval="1m")
        
        return {
            'spx_current': spx['Close'].iloc[-1] if len(spx) > 0 else None,
            'spx_change': ((spx['Close'].iloc[-1] - spx['Open'].iloc[0]) / spx['Open'].iloc[0] * 100) if len(spx) > 0 else None,
            'vix_current': vix['Close'].iloc[-1] if len(vix) > 0 else None,
            'vix_change': ((vix['Close'].iloc[-1] - vix['Open'].iloc[0]) / vix['Open'].iloc[0] * 100) if len(vix) > 0 else None,
        }
    except Exception as e:
        return {'error': str(e)}


if __name__ == "__main__":
    # 测试
    test = "TARIFFS ON CHINA! BIGGEST EVER! IRAN WILL BE DESTROYED!"
    result = analyze_post(test)
    print(result)


# ========== 每日聚合器 (Ray提供) ==========
class Post:
    """帖子对象"""
    def __init__(self, text: str, score: float = 0, engagement: int = 1):
        self.text = text
        self.score = score
        self.engagement = engagement

def daily_aggregator(posts_today: list) -> dict:
    """
    每日帖子聚合器 (Ray版)
    
    输出:
    - peak: 最极端的T-Back值
    - range: (最负面, 最正面)
    - status: Rapid Cycling / Stable
    - dominant_score: 情感重心(加权)
    """
    if not posts_today:
        return {"peak": 0, "range": (0, 0), "status": "Stable", "dominant_score": 0}
    
    # 确保是Post对象
    posts = []
    for p in posts_today:
        if isinstance(p, dict):
            posts.append(Post(p.get('text', ''), p.get('t_back', 0), p.get('engagement', 1)))
        elif isinstance(p, Post):
            posts.append(p)
        else:
            posts.append(Post(str(p), 0, 1))
    
    # 最凶/最亢奋
    scores = [p.score for p in posts]
    peak_negative = min(scores)  # 最负面
    peak_positive = max(scores)  # 最正面
    
    # 振幅
    volatility = peak_positive - peak_negative
    
    # 情感重心 (加权平均)
    total_engagement = sum(p.engagement for p in posts)
    if total_engagement > 0:
        dominant_score = sum(p.score * p.engagement for p in posts) / total_engagement
    else:
        dominant_score = sum(scores) / len(scores)
    
    # 判断主导模式
    if dominant_score > 20:
        mode = "传教士"
    elif dominant_score < -20:
        mode = "掠食者"
    else:
        mode = "面具"
    
    return {
        "peak": peak_negative if abs(peak_negative) > peak_positive else peak_positive,
        "range": (peak_negative, peak_positive),
        "volatility": volatility,
        "status": "Rapid Cycling" if volatility > 120 else "Stable",
        "dominant_score": round(dominant_score, 1),
        "mode": mode,
        "post_count": len(posts)
    }


# ========== 传播动量量化模型 (Ray提供) ==========
class ViralPost:
    """带传播数据的帖子"""
    def __init__(self, text: str, score: float = 0, 
                 reposts: int = 0, comments: int = 0, likes: int = 0):
        self.text = text
        self.score = score  # T_base 势能
        self.reposts = reposts
        self.comments = comments
        self.likes = likes
    
    @property
    def engagement(self) -> int:
        return self.reposts + self.comments + self.likes
    
    @property
    def viral_momentum(self) -> float:
        """
        计算传播动量 V_m
        V_m = log10(Reposts + Comments×0.7 + Likes×0.3)
        """
        weighted = self.reposts + self.comments * 0.7 + self.likes * 0.3
        if weighted <= 0:
            return 0
        return (weighted - 1) / 6  # 归一化到0-1区间，假设10万是max
    
    def final_t_back(self) -> float:
        """
        T_final = T_base × (1 + log10(weighted_engagement) / 3)
        
        流量放大效应（修正版）:
        - 1000互动: ~1.3倍
        - 10000互动: ~1.7倍
        - 100000互动: ~2.0倍
        - 1000000互动: ~2.3倍
        """
        if self.engagement <= 1:
            return self.score
        
        # 对数增长，最大1.5倍放大
        weighted = self.reposts + self.comments * 0.7 + self.likes * 0.3
        multiplier = 1 + min(1.5, (weighted ** 0.15 - 1) / 2)
        
        final_score = self.score * multiplier
        return max(-120, min(120, round(final_score, 1)))


def viral_validator(posts: list) -> dict:
    """
    传播验证器 - 结合势能与动能
    
    输入: [{"text": "...", "t_base": -95, "reposts": 10000, "comments": 5000, "likes": 50000}, ...]
    输出: {
        "high_impact_posts": [...],  # 病毒式传播帖子
        "dud_posts": [...],         # 无效咆哮
        "supernova_posts": [...],   # 超新星爆发 (RPS > 500)
        "total_viral_momentum": float,
    }
    """
    high_impact = []
    duds = []
    supernovas = []
    momentum_sum = 0
    
    for p in posts:
        # 创建ViralPost对象
        if isinstance(p, dict):
            vp = ViralPost(
                p.get('text', ''),
                p.get('t_base', 0),
                p.get('reposts', 0),
                p.get('comments', 0),
                p.get('likes', 0)
            )
        else:
            continue
        
        t_final = vp.final_t_back()
        momentum = vp.viral_momentum
        momentum_sum += momentum
        
        post_data = {
            "text": vp.text[:50] + "...",
            "t_base": vp.score,
            "t_final": t_final,
            "engagement": vp.engagement,
            "momentum": momentum,
            "reposts": vp.reposts,
            "comments": vp.comments,
            "likes": vp.likes
        }
        
        # 分类
        if vp.engagement > 50000 and abs(t_final) > 80:
            high_impact.append(post_data)
        
        if vp.engagement < 100 and abs(vp.score) > 50:
            duds.append(post_data)
            
        # 超新星检测 (假设5分钟内10000转 = RPS > 33)
        if vp.reposts > 10000:
            supernovas.append(post_data)
    
    return {
        "high_impact_posts": high_impact,
        "dud_posts": duds,
        "supernova_posts": supernovas,
        "total_viral_momentum": round(momentum_sum / len(posts), 2) if posts else 0,
        "post_count": len(posts)
    }
