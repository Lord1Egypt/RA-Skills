# 用户偏好追踪系统

## 📋 系统概述

本系统用于记录和追踪用户对助眠故事的偏好，实现**个性化适配**和**持续优化**。

**核心目标**：
- 记录用户对每个故事的反馈
- 自动识别偏好模式
- 动态调整后续故事风格
- 追踪助眠效果

---

## 🗂️ 数据结构

### 用户偏好档案 (`memory/user-preferences.json`)

```json
{
  "version": "1.0",
  "lastUpdated": "2026-04-05",
  "totalStories": 0,
  
  "storyTypePreferences": {
    "自然风景类": {
      "count": 0,
      "avgRating": 0,
      "lastUsed": null,
      "favoriteElements": []
    },
    "温馨日常类": {
      "count": 0,
      "avgRating": 0,
      "lastUsed": null,
      "favoriteElements": []
    },
    "动物伙伴类": {
      "count": 0,
      "avgRating": 0,
      "lastUsed": null,
      "favoriteElements": []
    },
    "童年回忆类": {
      "count": 0,
      "avgRating": 0,
      "lastUsed": null,
      "favoriteElements": []
    },
    "奇幻治愈类": {
      "count": 0,
      "avgRating": 0,
      "lastUsed": null,
      "favoriteElements": []
    },
    "季节限定类": {
      "count": 0,
      "avgRating": 0,
      "lastUsed": null,
      "favoriteElements": []
    }
  },
  
  "elementPreferences": {
    "scenes": {},
    "characters": {},
    "journeys": {},
    "discoveries": {},
    "sensoryFocus": {}
  },
  
  "stylePreferences": {
    "length": {
      "preferred": "1500-2000",
      "options": ["1000-1500", "1500-2000", "2000-2500", "2500+"]
    },
    "pace": {
      "preferred": "slow",
      "options": ["very-slow", "slow", "medium", "fast"]
    },
    "hypnosisDepth": {
      "preferred": "medium",
      "options": ["light", "medium", "deep"]
    },
    "dialogueRatio": {
      "preferred": "low",
      "options": ["none", "low", "medium", "high"]
    }
  },
  
  "psychologyTechniquePreferences": {
    "正念呼吸": { "effectiveness": 0, "count": 0 },
    "渐进式肌肉放松": { "effectiveness": 0, "count": 0 },
    "可视化想象": { "effectiveness": 0, "count": 0 },
    "安全基地构建": { "effectiveness": 0, "count": 0 },
    "感恩回忆": { "effectiveness": 0, "count": 0 },
    "催眠暗示": { "effectiveness": 0, "count": 0 },
    "呼吸绑定": { "effectiveness": 0, "count": 0 },
    "意识模糊化": { "effectiveness": 0, "count": 0 }
  },
  
  "sleepEffectiveness": {
    "avgSleepTime": null,
    "avgSleepQuality": null,
    "improvementTrend": []
  },
  
  "avoidElements": {
    "scenes": [],
    "characters": [],
    "themes": []
  },
  
  "notes": []
}
```

---

## 📝 反馈收集机制

### 反馈收集时机

| 时机 | 收集方式 | 收集内容 |
|------|----------|----------|
| **故事结束后** | 简单评分 | 1-5 星评分 |
| **次日早晨** | 效果问询 | 入睡时间、睡眠质量 |
| **每周总结** | 深度反馈 | 偏好变化、新需求 |
| **主动反馈** | 随时接收 | 喜好、建议、问题 |

### 反馈问题模板

#### 简单反馈（故事结束后）

```
昨晚的故事还喜欢吗？
⭐⭐⭐⭐⭐ (1-5 星)

哪个部分最喜欢？
A. 场景描写  B. 角色互动  C. 放松引导  D. 整体氛围

还想听类似的故事吗？
A. 很想  B. 可以  C. 不用了
```

#### 效果反馈（次日早晨）

```
昨晚睡得怎么样？
A. 很快就睡着了 (10 分钟内)
B. 比较快 (10-20 分钟)
C. 一般 (20-30 分钟)
D. 比较难 (30 分钟以上)

睡眠质量如何？
A. 深沉无梦  B. 有梦但安稳  C. 浅睡多梦  D. 易醒

今天精神状态？
A. 精力充沛  B. 正常  C. 有点累  D. 很疲惫
```

#### 偏好反馈（主动询问）

```
最近想听什么类型的故事？
A. 自然风景（森林、湖泊、星空）
B. 温馨日常（小屋、书店、咖啡馆）
C. 动物伙伴（小猫、小鹿、鲸鱼）
D. 童年回忆（外婆家、老街道）
E. 奇幻治愈（魔法、星星、梦境）
F. 都可以，听你安排

喜欢什么样的节奏？
A. 很慢很缓  B. 适中  C. 稍微快一点

偏好哪种感官描写？
A. 视觉（月光、星光、色彩）
B. 听觉（雨声、风声、音乐）
C. 触觉（温暖、柔软、拥抱）
D. 嗅觉（花香、书香、食物香）
```

---

## 🤖 个性化适配规则

### 规则引擎 (`memory/adaptation-rules.md`)

#### 基于评分的适配

| 条件 | 动作 |
|------|------|
| 评分 ≥ 4 星 | 记录喜欢的元素，7 天内可重复使用 |
| 评分 = 3 星 | 中性，保持观察 |
| 评分 ≤ 2 星 | 记录不喜欢的元素，30 天内避免 |
| 连续 3 次 ≥ 4 星 | 提升该类型优先级 |
| 连续 3 次 ≤ 2 星 | 降低该类型优先级，询问用户 |

#### 基于入睡时间的适配

| 入睡时间 | 调整策略 |
|----------|----------|
| < 10 分钟 | 保持当前风格，强化有效元素 |
| 10-20 分钟 | 微调，增加催眠暗示强度 |
| 20-30 分钟 | 调整故事类型，尝试新元素 |
| > 30 分钟 | 显著调整，询问用户偏好 |

#### 基于睡眠质量的适配

| 睡眠质量 | 调整策略 |
|----------|----------|
| 深沉无梦 | 保持当前配方 |
| 有梦但安稳 | 轻微调整，观察变化 |
| 浅睡多梦 | 减少刺激元素，增加安全感 |
| 易醒 | 增强安全基地构建，减少转折 |

#### 基于时间的适配

| 时间维度 | 适配策略 |
|----------|----------|
| **季节** | 使用当季场景和意象 |
| **星期** | 工作日偏安静，周末偏轻松 |
| **月相** | 满月用月光主题，新月用星空主题 |
| **特殊日期** | 生日、节日使用应景故事 |

---

## 📊 偏好学习算法

### 元素偏好计算

```python
# 伪代码示例
def calculate_element_preference(element_id, ratings):
    """
    计算元素偏好分数
    :param element_id: 元素 ID（如场景 N01）
    :param ratings: 使用该元素的评分列表
    :return: 偏好分数 (0-100)
    """
    if not ratings:
        return 50  # 中性
    
    # 加权平均（最近评分权重更高）
    weights = [1.0, 0.8, 0.6, 0.4, 0.2]  # 最近 5 次
    weighted_sum = sum(r * w for r, w in zip(ratings[-5:], weights[-len(ratings):]))
    weight_total = sum(weights[-len(ratings):])
    
    base_score = (weighted_sum / weight_total) * 20  # 转为 0-100
    
    # 使用频率惩罚（避免过度使用）
    usage_count = len(ratings)
    frequency_penalty = min(usage_count * 2, 20)  # 最多减 20 分
    
    # 新鲜度奖励（长时间未用）
    days_since_last_use = 7  # 示例
    freshness_bonus = min(days_since_last_use * 3, 15)  # 最多加 15 分
    
    final_score = base_score - frequency_penalty + freshness_bonus
    
    return max(0, min(100, final_score))
```

### 类型推荐逻辑

```python
def recommend_story_type(preferences, recent_history):
    """
    推荐故事类型
    :param preferences: 用户偏好档案
    :param recent_history: 最近使用的故事类型
    :return: 推荐类型
    """
    # 获取各类型分数
    type_scores = {}
    for story_type, data in preferences['storyTypePreferences'].items():
        if story_type in recent_history:
            continue  # 跳过最近用过的
        
        base_score = data['avgRating'] * 20
        count_bonus = min(data['count'] * 2, 10)  # 成功经验奖励
        recency_penalty = 10 if data['lastUsed'] else 0  # 久未使用奖励
        
        type_scores[story_type] = base_score + count_bonus + recency_penalty
    
    # 返回最高分类型
    return max(type_scores, key=type_scores.get)
```

---

## 🔄 自适应调整流程

### 创作前检查流程

```
1. 读取用户偏好档案
   ↓
2. 检查最近 3 篇故事历史
   ↓
3. 计算各元素偏好分数
   ↓
4. 排除低分元素（< 40 分）
   ↓
5. 选择高分元素（> 70 分优先）
   ↓
6. 组合生成故事大纲
   ↓
7. 检查去重规则
   ↓
8. 开始创作
```

### 创作中调整

| 检测点 | 调整项 |
|--------|--------|
| 开场后 | 根据用户反应调整节奏 |
| 放松阶段 | 根据呼吸反馈调整深度 |
| 高潮前 | 根据注意力调整情感强度 |
| 结尾前 | 根据困倦程度调整暗示强度 |

### 创作后优化

1. **收集反馈** - 评分 + 文字评价
2. **更新档案** - 记录元素效果
3. **分析模式** - 识别偏好趋势
4. **调整规则** - 优化推荐算法
5. **生成报告** - 每周总结

---

## 📈 效果追踪指标

### 核心指标

| 指标 | 计算方式 | 目标值 |
|------|----------|--------|
| **平均入睡时间** | 总和/故事数 | < 20 分钟 |
| **平均睡眠质量** | 评分平均 | > 4 星 |
| **用户满意度** | 故事评分平均 | > 4.2 星 |
| **偏好匹配度** | 推荐接受率 | > 70% |
| **元素多样性** | 不重复元素占比 | > 80% |

### 趋势分析

```
每周生成趋势报告：
- 入睡时间变化曲线
- 睡眠质量变化曲线
- 偏好类型分布
- 有效元素 TOP10
- 需要调整的元素
```

---

## 💡 智能推荐示例

### 场景 1：新用户体验优化

```
用户：第一次使用
策略：
1. 使用通用型故事（温馨日常类）
2. 中等长度（1500-2000 字）
3. 基础放松技术（呼吸 + 肌肉放松）
4. 收集详细反馈
5. 建立初始偏好档案
```

### 场景 2：失眠严重用户

```
用户：连续 3 天入睡>30 分钟
策略：
1. 增加催眠暗示强度
2. 使用深度放松技术
3. 缩短故事长度（减少刺激）
4. 增加安全基地构建
5. 次日跟进效果
```

### 场景 3：偏好明显用户

```
用户：明确喜欢自然风景类（4.8 星平均）
策略：
1. 优先推荐自然风景类
2. 轮换使用不同自然场景
3. 强化用户喜欢的元素（如月光、湖水）
4. 尝试自然 + 动物混合类型
5. 季度性引入新元素防腻
```

### 场景 4：审美疲劳用户

```
用户：最近评分下降（4.5→3.2 星）
策略：
1. 显著调整故事类型
2. 引入新场景和新角色
3. 减少过度使用元素
4. 询问用户新需求
5. 尝试系列故事增加期待感
```

---

## 🔧 实施建议

### 第一阶段（基础）
- [ ] 创建用户偏好档案模板
- [ ] 实现基础反馈收集
- [ ] 建立简单推荐规则
- [ ] 手动更新偏好档案

### 第二阶段（自动化）
- [ ] 自动化评分记录
- [ ] 实现元素偏好计算
- [ ] 自动推荐故事类型
- [ ] 生成周度报告

### 第三阶段（智能化）
- [ ] 机器学习优化推荐
- [ ] 实时反馈调整
- [ ] 预测性偏好识别
- [ ] 跨用户模式学习

### 第四阶段（生态化）
- [ ] 系列故事自动生成
- [ ] 用户社区分享
- [ ] A/B 测试优化
- [ ] 多模态反馈（语音、生理）

---

## 📋 快速启动指南

### Step 1: 创建偏好档案

```bash
# 复制模板
cp memory/user-preferences.json.template memory/user-preferences.json
```

### Step 2: 首次使用记录

```json
{
  "totalStories": 1,
  "lastStory": {
    "date": "2026-04-05",
    "type": "温馨日常类",
    "scene": "D01 深夜书店",
    "rating": 5,
    "sleepTime": 15,
    "sleepQuality": 4
  }
}
```

### Step 3: 根据反馈调整

```
如果评分 ≥ 4 星：
→ 记录喜欢的元素
→ 7 天内可再次使用

如果评分 ≤ 2 星：
→ 记录不喜欢的元素
→ 30 天内避免使用
```

### Step 4: 持续优化

- 每周回顾偏好变化
- 每月总结效果趋势
- 每季度调整推荐策略

---

**最后更新**：2026-04-05
**版本**：1.0
**维护**：定期根据用户反馈更新规则
