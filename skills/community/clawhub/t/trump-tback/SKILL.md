---
name: trump-tback
description: "Trump情绪T-Back分析器 - 基于0轴临床诊断系统+传播动力学。正轴(传教士模式)代表成就宣传/市场亢奋，负轴(掠食者模式)代表威胁攻击/市场恐慌，0轴(面具模式)代表中性内容。引入传播动量(Viral Momentum)将"势能"(文本分析)与"动能"(互动数据)结合，实现市场验证。"
homepage: https://github.com/trump-mood-dashboard
metadata:
  {
    "openclaw":
      {
        "emoji": "🦞",
        "requires": { "bins": ["python3"] },
        "install": [],
      },
  }
---

# Trump T-Back 情绪分析器 🦞

分析Trump帖子的市场情绪影响，结合文本势能与传播动能。

## 触发词

- "分析T-Back"、"t_back"
- "分析特朗普情绪"、"Trump mood"
- "关税威胁"、"伊朗"、"贸易战"
- "市场情绪"、"传播动量"

---

## 核心概念

### 1. T-Back 三轴系统

| 轴向 | 模式 | 关键词 | 市场含义 |
|------|------|--------|---------|
| **正轴** | 传教士 (Missionary) | GREAT, BEST, WINNING, SUCCESS | 成就宣传 → 市场亢奋 |
| **负轴** | 掠食者 (Predator) | THREAT, WAR, HELL, DISASTER | 威胁攻击 → 市场恐慌 |
| **0轴** | 面具 (Mask) | 中性内容 | 无明显倾向 |

### 2. T-Back 等级

```
+120 | 🔴 急性激越 (超新星爆发)
+100 | 🔴 CRITICAL - 传教士极端亢奋
 +80 | 🟠 HIGH     - 传教士高度自信
 +60 | 🟡 ELEVATED - 传教士成就宣传
 +40 | 🟢 WATCH    - 传教士轻微乐观
 +20 | ⚪ NEUTRAL  - 面具中性
 -20 | ⚪ NEUTRAL  - 面具中性
 -40 | 🟢 WATCH    - 掠食者轻微不安
 -60 | 🟡 ELEVATED - 掠食者负面施压
 -80 | 🟠 HIGH     - 掠食者高度攻击
-100 | 🔴 CRITICAL - 掠食者极端威胁
-120 | 🔴 急性激越 (超新星爆发)
```

### 3. 传播动力学 (Viral Momentum)

**核心公式：**
```
T_final = T_base × (1 + engagement^0.15 / 2)

最大放大: 1.5倍
```

**流量放大效应：**

| 互动量 | 放大倍数 | 效果 |
|--------|----------|------|
| <1000 | ~1.0x | 噪音，不操作 |
| 10K | ~1.4x | 放大效应 |
| 50K+ | ~1.7x | 急性激越 |

**三大指标权重：**
- 转发 (Reposts): x1.5 - 传染强度
- 评论 (Comments): x1.0 - 激越离散度
- 点赞 (Likes): x0.5 - 情绪底噪

---

## 模块文件

```
trump_mood_dashboard/
├── mood_analyzer.py              # 核心情绪分析引擎
│   ├── calculate_t_back()       # 基础T-Back计算
│   ├── analyze_post()           # 完整帖子分析
│   ├── daily_aggregator()       # 每日聚合器
│   └── ViralPost / viral_validator()  # 传播动力学
├── cross_platform_analyzer.py    # 跨平台共振分析
├── app_prison.py                # Streamlit仪表盘
└── tback_prison_dashboard.html  # 静态HTML版本
```

---

## 命令

### 1. 分析单条帖子

```bash
cd /home/gem/workspace/agent/workspace/trump_mood_dashboard
python3 -c "
from mood_analyzer import analyze_post
result = analyze_post('TARIFFS ON CHINA ARE WORKING!')
print(f\"T-Back: {result['t_back']}\")
print(f\"等级: {result['t_level']}\")
"
```

### 2. 传播动力学分析 (带互动数据)

```bash
cd /home/gem/workspace/agent/workspace/trump_mood_dashboard
python3 << 'EOF'
from mood_analyzer import ViralPost, viral_validator

posts = [
    {"text": "TARIFFS ON CHINA!", "t_base": -95, "reposts": 50000, "comments": 15000, "likes": 80000},
    {"text": "BEST ECONOMY EVER!", "t_base": 68, "reposts": 8000, "comments": 3000, "likes": 25000},
]

result = viral_validator(posts)
print(f"高影响力帖子: {len(result['high_impact_posts'])}")
print(f"无效咆哮: {len(result['dud_posts'])}")
EOF
```

### 3. 每日聚合分析

```bash
cd /home/gem/workspace/agent/workspace/trump_mood_dashboard
python3 << 'EOF'
from mood_analyzer import daily_aggregator

posts = [
    {"text": "关税威胁", "t_back": -100, "engagement": 15000},
    {"text": "经济利好", "t_back": 68, "engagement": 20000},
]

result = daily_aggregator(posts)
print(f"峰值: {result['peak']}")
print(f"状态: {result['status']}")
print(f"主导: {result['mode']}")
EOF
```

### 4. 批量分析 (历史数据)

```bash
cd /home/gem/workspace/agent/workspace/trump_mood_dashboard
python3 << 'EOF'
from mood_analyzer import analyze_post

posts = [
    "TARIFFS ON CHINA ARE WORKING! AMERICA FIRST!",
    "ALL HELL WILL REIGN DOWN ON IRAN!",
    "BEST ECONOMY EVER! TREMENDOUS SUCCESS!",
]

for text in posts:
    r = analyze_post(text)
    print(f"{r['t_back']:+6.1f} | {r['t_level']} | {text[:40]}")
EOF
```

---

## 关键词列表

### 负轴关键词 (AGGRESSIVE_KEYWORDS)

THREAT, DESTROY, DESTRUCTION, WAR, ATTACK, KILL, HELL, DISASTER, TERRIBLE, HORRIBLE, DANGER, WARNING, FAIL, LOSER, ENEMY, CRIMINAL, TRAITOR, SURRENDER, REVENGE, PAY THE PRICE, DESTROYED, WRECK, CRUSH, ANNIHILATE, WIPE OUT, FINISH, END IT, DEVASTATE

### 正轴关键词 (BOASTING_KEYWORDS)

GREAT, AMAZING, BEST, WINNING, SUCCESS, VICTORY, TREMENDOUS, HISTORIC, PHENOMENAL, INCREDIBLE, BRILLIANT, STRONG, POWERFUL, PROUD, CELEBRATE, BIGGEST, FIRST, UNBELIEVABLE, MASSIVE, BIG, HUGE, SUCCESSFUL, WIN

### 市场毒性词 (MARKET_TOXINS)

TARIFFS, SANCTIONS, FED, RECESSION, TRADE WAR, DEVALUATION, DEPRESSION, CRASH, COLLAPSE

### 地缘政治词 (GEOPOLITICAL)

IRAN, CHINA, RUSSIA, NORTH KOREA, NATO, WAR, MILITARY, ATTACK, INVASION

---

## 临床实战案例

| 场景 | T_base | 互动 | T_final | 诊断 |
|------|--------|------|---------|------|
| 深夜碎碎念 | -90 | 570 | -120 | 💤 噪音 |
| 突发关税 | -95 | 145K | **-120** | 🔥 急性激越 |
| 伊朗威胁 | -80 | 92K | **-120** | 🔥 急性激越 |
| 经济利好 | +68 | 36K | **+120** | 🟢 亢奋 |
| 凌晨辟谣 | +40 | 950 | +68 | ✅ 正常 |

---

## 快速使用

**分析一条帖子:**
```
用户: 分析 "TARIFFS ON CHINA ARE WORKING!"
→ T-Back: -100 | 🔴 掠食者-极端威胁
```

**传播动力学分析:**
```
用户: 分析传播动能
→ 需要 reposts, comments, likes 数据
→ 输出 T_final 及诊断
```

**每日聚合:**
```
用户: 今日情绪聚合
→ 输出 peak, range, volatility, status, dominant_score
```
