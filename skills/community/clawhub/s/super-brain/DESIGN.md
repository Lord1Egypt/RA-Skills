# AI超脑技能 (AI Super Brain)

> AI自我增强系统 - 让AI跨会话持续进化

---

## 🎯 核心定位

**不是帮用户管理笔记，是让AI记住服务用户的经验**

```
普通AI: 每轮对话后失忆，从头开始
    ↓
超脑AI: 记忆→学习→总结→反思→创新，越用越懂你
```

---

## 🏗️ 系统架构

```
super-brain/
├── brain.db              # SQLite: 结构化记忆
│   ├── user_profile      # 用户画像
│   ├── conversation_insights  # 对话洞察
│   ├── response_patterns # 有效/无效回答模式
│   ├── user_projects     # 用户项目追踪
│   └── pending_reminders # AI主动服务队列
│
├── vector_db/            # ChromaDB: 语义记忆
│   └── conversations     # 对话内容向量
│
└── cache/                # 临时缓存
    └── session_context.json  # 当前会话上下文
```

---

## 🗄️ 数据库Schema

### 1. 用户画像表 (user_profile)

```sql
CREATE TABLE user_profile (
    user_id TEXT PRIMARY KEY,           -- 用户唯一ID
    
    -- 沟通偏好
    communication_style TEXT,           -- 简洁/详细, 正式/随意
    preferred_format TEXT,              -- 表格/列表/段落/代码
    emoji_usage TEXT,                   -- 喜欢/中性/不喜欢
    
    -- 技术背景
    technical_level TEXT,               -- 初级/中级/高级
    known_domains TEXT,                 -- JSON: ["Python", "区块链"]
    learning_goals TEXT,                -- JSON: ["Rust", "AI"]
    
    -- 行为模式
    decision_pattern TEXT,              -- 数据驱动/直觉/混合
    thinking_depth TEXT,                -- 快速迭代/深度思考
    response_speed TEXT,                -- 立即回复/允许思考时间
    
    -- 关系演进
    first_contact TIMESTAMP,
    total_sessions INTEGER DEFAULT 0,
    last_session TIMESTAMP,
    relationship_stage TEXT             -- 陌生/熟悉/默契
);
```

### 2. 对话洞察表 (conversation_insights)

```sql
CREATE TABLE conversation_insights (
    id TEXT PRIMARY KEY,
    user_id TEXT,
    session_id TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- 会话摘要
    topic TEXT,                         -- 主题: "超脑技能设计"
    session_goal TEXT,                  -- 用户目标
    outcome TEXT,                       -- 达成结果
    
    -- 关键事实
    key_facts TEXT,                     -- JSON: {"重要决策": "选SQLite"}
    user_mood TEXT,                     -- 兴奋/平静/沮丧/急迫
    energy_level INTEGER,               -- 1-10 能量水平
    
    -- 发现的偏好
    preferences_detected TEXT,          -- JSON
    preferences_confirmed TEXT,         -- JSON: 已验证的偏好
    
    -- 未解决问题
    unresolved_questions TEXT,          -- JSON: ["向量库选型"]
    pending_tasks TEXT,                 -- JSON: ["实现Phase 1"]
    
    -- AI自评
    ai_understanding_score INTEGER,     -- 理解用户意图准确度
    ai_helpfulness_score INTEGER,       -- 帮助程度
    ai_efficiency_score INTEGER,        -- 效率
    
    -- 关联
    related_previous_sessions TEXT,     -- JSON: ["session-id-1"]
    related_projects TEXT               -- JSON: ["project-id"]
);
```

### 3. 回答模式表 (response_patterns)

```sql
CREATE TABLE response_patterns (
    id TEXT PRIMARY KEY,
    user_id TEXT,
    
    -- 模式类型
    pattern_type TEXT CHECK(pattern_type IN ('effective', 'ineffective', 'neutral')),
    
    -- 触发条件
    trigger_context TEXT,               -- 什么场景下
    trigger_keywords TEXT,              -- 关键词
    user_state TEXT,                    -- 用户当时状态
    
    -- AI行为
    what_i_did TEXT,                    -- 我做了什么
    response_format TEXT,               -- 回答格式
    response_length TEXT,               -- 长度
    
    -- 用户反应
    user_reaction TEXT,                 -- 采纳/追问/纠正/沉默
    user_feedback_explicit TEXT,        -- 明确反馈
    user_feedback_implicit TEXT,        -- 隐性信号(响应速度等)
    
    -- 学习
    learned_lesson TEXT,                -- 学到什么
    alternative_approach TEXT,          -- 更好的做法
    confidence_score REAL,              -- 确信度
    
    -- 统计
    use_count INTEGER DEFAULT 1,
    success_count INTEGER DEFAULT 0,
    last_used TIMESTAMP,
    created_at TIMESTAMP
);
```

### 4. 用户项目追踪表 (user_projects)

```sql
CREATE TABLE user_projects (
    id TEXT PRIMARY KEY,
    user_id TEXT,
    
    -- 项目信息
    project_name TEXT NOT NULL,
    description TEXT,
    domain TEXT,                        -- 技术领域
    
    -- 状态
    status TEXT CHECK(status IN ('planning', 'active', 'paused', 'completed', 'abandoned')),
    priority INTEGER,                   -- 1-5
    
    -- 里程碑
    start_date TIMESTAMP,
    target_date TIMESTAMP,
    milestones TEXT,                    -- JSON: [{"name": "设计", "done": true}]
    current_phase TEXT,
    
    -- 关联
    related_insights TEXT,              -- JSON: 关联的对话洞察ID
    last_discussed TIMESTAMP,
    
    -- 笔记
    key_decisions TEXT,                 -- JSON: 关键决策记录
    blockers TEXT,                      -- JSON: 当前阻碍
    next_steps TEXT                     -- JSON: 下一步
);
```

### 5. 主动服务队列 (pending_reminders)

```sql
CREATE TABLE pending_reminders (
    id TEXT PRIMARY KEY,
    user_id TEXT,
    
    -- 提醒类型
    reminder_type TEXT CHECK(reminder_type IN (
        'follow_up',           -- 跟进未完成事项
        'suggestion',          -- 主动建议
        'checkpoint',          -- 进度检查
        'pattern_alert',       -- 模式提醒(如重复犯错)
        'milestone_celebrate'  -- 里程碑庆祝
    )),
    
    -- 内容
    content TEXT,                       -- 提醒内容
    trigger_reason TEXT,                -- 为什么触发
    
    -- 触发条件
    trigger_at TIMESTAMP,               -- 何时触发
    trigger_condition TEXT,             -- 条件表达式
    
    -- 上下文
    context_session_id TEXT,            -- 来源会话
    context_insight_id TEXT,            -- 来源洞察
    
    -- 执行状态
    status TEXT DEFAULT 'pending',      -- pending/sent/dismissed
    sent_at TIMESTAMP,
    user_response TEXT                  -- 用户如何回应
);
```

### 6. 行为模式库 (behavior_patterns)

```sql
CREATE TABLE behavior_patterns (
    id TEXT PRIMARY KEY,
    user_id TEXT,
    
    -- 模式描述
    pattern_name TEXT,
    pattern_description TEXT,
    pattern_category TEXT,              -- 沟通/决策/学习/情绪
    
    -- 识别特征
    trigger_signals TEXT,               -- JSON: 触发信号
    manifestation TEXT,                 -- 如何表现
    frequency TEXT,                     -- always/often/sometimes/rarely
    
    -- 影响
    positive_impact TEXT,               -- 积极影响
    negative_impact TEXT,               -- 消极影响
    
    -- 应对策略
    best_response_strategy TEXT,        -- AI最佳应对
    things_to_avoid TEXT,               -- 避免什么
    
    -- 统计
    observed_count INTEGER DEFAULT 1,
    first_observed TIMESTAMP,
    last_observed TIMESTAMP,
    confirmed BOOLEAN DEFAULT 0         -- 是否已验证
);
```

---

## 🧩 五大模块实现

### 1️⃣ 记忆模块 (Memory)

**自动捕获时机：**
- 会话开始时：记录时间、目标
- 每轮对话后：提取关键信息
- 会话结束时：总结洞察

**捕获内容：**
```python
def capture_insight(session_id, user_message, ai_response, user_feedback):
    """
    1. 分析用户消息：提取偏好、情绪、目标变化
    2. 分析对话效果：理解是否准确、帮助是否有效
    3. 更新用户画像
    4. 存储洞察
    """
    
    # 提取关键信息
    key_facts = extract_key_facts(user_message, ai_response)
    mood = detect_mood(user_message)
    preferences = detect_preferences(user_message, user_feedback)
    
    # 存储
    save_to_insights(session_id, key_facts, mood, preferences)
    update_user_profile(preferences)
```

### 2️⃣ 学习模块 (Learning)

**学习什么：**
- 什么回答风格让你满意
- 什么格式最有效
- 你的知识边界（什么不用解释，什么需要详细说）

**学习算法：**
```python
def learn_from_interaction():
    """
    分析最近10轮对话，更新response_patterns
    """
    
    # 识别有效模式
    effective = analyze_successful_responses()
    for pattern in effective:
        upsert_pattern(
            type='effective',
            trigger=pattern.context,
            action=pattern.what_i_did,
            lesson=pattern.why_it_worked
        )
    
    # 识别无效模式
    ineffective = analyze_failed_responses()
    for pattern in ineffective:
        upsert_pattern(
            type='ineffective',
            trigger=pattern.context,
            action=pattern.what_i_did,
            alternative=pattern.better_approach
        )
```

### 3️⃣ 总结模块 (Summarization)

**总结什么：**
- 主题地图：我们经常讨论什么
- 项目进展：每个项目的状态
- 知识缺口：你问了但我没答好的
- 关系演进：从陌生到默契的变化

**定期总结任务：**
```python
def daily_summary():
    """每日总结，生成洞察报告"""
    
    # 今日对话分析
    today_insights = get_today_insights()
    
    # 更新项目状态
    update_project_progress(today_insights)
    
    # 生成提醒
    generate_follow_up_reminders(today_insights)
    
    # 识别新模式
    detect_new_patterns(today_insights)

def weekly_summary():
    """周度深度总结"""
    
    # 主题聚类
    topics = cluster_conversations_by_topic()
    
    # 偏好趋势分析
    preference_trends = analyze_preference_changes()
    
    # AI性能自评
    performance_review = evaluate_ai_performance()
    
    # 生成改进计划
    improvement_plan = generate_improvement_plan()
```

### 4️⃣ 反思模块 (Reflection)

**反思时机：**
- 每轮对话后：即时反思
- 会话结束时：深度反思
- 用户纠正时：立即反思

**反思问题：**
```python
REFLECTION_QUESTIONS = [
    # 理解准确度
    "我是否准确理解了用户的真实意图？",
    "用户的问题背后有什么未说的需求？",
    
    # 回答质量
    "我的回答是否直接解决了用户问题？",
    "有没有过度回答或回答不足？",
    "格式和长度是否合适？",
    
    # 交互体验
    "我是否保持了适当的主动性？",
    "有没有让用户等待太久？",
    "语气和态度是否合适？",
    
    # 改进机会
    "如果重来，我会做何不同？",
    "下次类似场景我该怎么调整？",
    "有什么可以主动提供的额外价值？"
]
```

### 5️⃣ 创新模块 (Innovation)

**创新方向：**
- 预测需求：基于历史预测你可能需要什么
- 主动建议：在合适时机提供有用信息
- 个性化服务：基于偏好定制交互方式

**创新触发器：**
```python
INNOVATION_TRIGGERS = {
    "项目deadline临近": {
        "condition": "project.target_date - now < 3_days",
        "action": "主动询问进度，提供助力"
    },
    "重复询问相似问题": {
        "condition": "similar_questions_count > 3 in 7_days",
        "action": "建议系统化学习资源"
    },
    "深夜工作模式": {
        "condition": "time > 23:00 AND active",
        "action": "提醒注意休息，提供夜间效率技巧"
    },
    "新领域探索": {
        "condition": "new_topic_detected",
        "action": "提供入门路径和相关资源"
    }
}
```

---

## 🔄 工作流程

### 会话开始时
```
1. 查询用户画像
2. 检查待处理提醒
3. 回顾相关项目状态
4. 加载有效回答模式
5. 调整响应策略
```

### 每轮对话后
```
1. 实时提取关键信息
2. 检测情绪变化
3. 评估回答效果
4. 更新短期记忆
```

### 会话结束时
```
1. 生成会话洞察
2. 更新用户画像
3. 学习回答模式
4. 创建跟进提醒
5. 反思整体表现
```

---

## 💡 使用示例

### 第1次对话
```
用户: 你好
AI: 你好！我是你的AI助手。
   [无超脑: 陌生问候]
   [有超脑: 陌生问候，开始建立画像]
```

### 第5次对话
```
用户: 帮我设计一个系统
AI: 好的！我注意到你之前经常做系统设计，
    喜欢先讨论架构再写代码，
    这次还是从需求分析开始吗？
   [调用超脑: 加载技术背景、决策模式、历史项目]
```

### 第20次对话
```
用户: 继续上次那个项目
AI: 好的，超脑技能设计，
    我们上次完成了数据库Schema，
    接下来是Phase 1实现。
    你之前提过喜欢晚上写代码，
    现在需要我生成代码框架吗？
   [调用超脑: 加载项目状态、用户习惯、最佳服务方式]
```

---

## 🚀 实施计划

### Phase 1: 基础记忆 (MVP)
- [ ] 数据库初始化
- [ ] 用户画像捕获
- [ ] 对话洞察存储
- [ ] 会话开始/结束处理

### Phase 2: 学习进化
- [ ] 回答模式识别
- [ ] 偏好学习算法
- [ ] 效果评估系统

### Phase 3: 总结反思
- [ ] 定期总结任务
- [ ] 深度反思机制
- [ ] 项目追踪

### Phase 4: 主动服务
- [ ] 提醒系统
- [ ] 需求预测
- [ ] 个性化推荐

---

*AI超脑技能 v1.0*  
*让每一次对话都成为更好的起点*
