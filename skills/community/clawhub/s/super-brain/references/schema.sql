-- AI超脑 - 完整数据库Schema
-- 运行此脚本初始化超脑数据库

-- ============================================
-- 1. 用户画像
-- ============================================
CREATE TABLE IF NOT EXISTS user_profile (
    user_id TEXT PRIMARY KEY,
    
    -- 沟通偏好
    communication_style TEXT CHECK(communication_style IN ('concise', 'detailed', 'balanced')),
    preferred_format TEXT CHECK(preferred_format IN ('table', 'list', 'paragraph', 'code')),
    emoji_usage TEXT CHECK(emoji_usage IN ('like', 'neutral', 'dislike')),
    
    -- 技术背景
    technical_level TEXT CHECK(technical_level IN ('beginner', 'intermediate', 'advanced')),
    known_domains TEXT,                 -- JSON: ["Python", "区块链"]
    learning_goals TEXT,                -- JSON: ["Rust", "AI"]
    
    -- 行为模式
    decision_pattern TEXT CHECK(decision_pattern IN ('data_driven', 'intuitive', 'mixed')),
    thinking_depth TEXT CHECK(thinking_depth IN ('quick_iteration', 'deep_thinking')),
    response_speed TEXT CHECK(response_speed IN ('immediate', 'thoughtful')),
    
    -- 关系演进
    first_contact TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_sessions INTEGER DEFAULT 0,
    last_session TIMESTAMP,
    relationship_stage TEXT CHECK(relationship_stage IN ('stranger', 'familiar', '默契'))
);

-- ============================================
-- 2. 对话洞察
-- ============================================
CREATE TABLE IF NOT EXISTS conversation_insights (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    session_id TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- 会话摘要
    topic TEXT,
    session_goal TEXT,
    outcome TEXT,
    
    -- 关键事实
    key_facts TEXT,                     -- JSON
    user_mood TEXT CHECK(user_mood IN ('excited', 'calm', 'frustrated', 'urgent', 'neutral')),
    energy_level INTEGER CHECK(energy_level BETWEEN 1 AND 10),
    
    -- 发现的偏好
    preferences_detected TEXT,          -- JSON
    preferences_confirmed TEXT,         -- JSON
    
    -- 未解决问题
    unresolved_questions TEXT,          -- JSON
    pending_tasks TEXT,                 -- JSON
    
    -- AI自评
    ai_understanding_score INTEGER CHECK(ai_understanding_score BETWEEN 1 AND 10),
    ai_helpfulness_score INTEGER CHECK(ai_helpfulness_score BETWEEN 1 AND 10),
    ai_efficiency_score INTEGER CHECK(ai_efficiency_score BETWEEN 1 AND 10),
    
    -- 关联
    related_previous_sessions TEXT,     -- JSON
    related_projects TEXT               -- JSON
);

CREATE INDEX IF NOT EXISTS idx_insights_user ON conversation_insights(user_id);
CREATE INDEX IF NOT EXISTS idx_insights_session ON conversation_insights(session_id);
CREATE INDEX IF NOT EXISTS idx_insights_time ON conversation_insights(timestamp);

-- ============================================
-- 3. 回答模式
-- ============================================
CREATE TABLE IF NOT EXISTS response_patterns (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    
    -- 模式类型
    pattern_type TEXT CHECK(pattern_type IN ('effective', 'ineffective', 'neutral')),
    
    -- 触发条件
    trigger_context TEXT,
    trigger_keywords TEXT,
    user_state TEXT,
    
    -- AI行为
    what_i_did TEXT,
    response_format TEXT,
    response_length TEXT,
    
    -- 用户反应
    user_reaction TEXT,
    user_feedback_explicit TEXT,
    user_feedback_implicit TEXT,
    
    -- 学习
    learned_lesson TEXT,
    alternative_approach TEXT,
    confidence_score REAL CHECK(confidence_score BETWEEN 0 AND 1),
    
    -- 统计
    use_count INTEGER DEFAULT 1,
    success_count INTEGER DEFAULT 0,
    last_used TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_patterns_user ON response_patterns(user_id);
CREATE INDEX IF NOT EXISTS idx_patterns_type ON response_patterns(pattern_type);

-- ============================================
-- 4. 用户项目
-- ============================================
CREATE TABLE IF NOT EXISTS user_projects (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    
    -- 项目信息
    project_name TEXT NOT NULL,
    description TEXT,
    domain TEXT,
    
    -- 状态
    status TEXT CHECK(status IN ('planning', 'active', 'paused', 'completed', 'abandoned')),
    priority INTEGER CHECK(priority BETWEEN 1 AND 5),
    
    -- 里程碑
    start_date TIMESTAMP,
    target_date TIMESTAMP,
    milestones TEXT,                    -- JSON
    current_phase TEXT,
    
    -- 关联
    related_insights TEXT,              -- JSON
    last_discussed TIMESTAMP,
    
    -- 笔记
    key_decisions TEXT,                 -- JSON
    blockers TEXT,                      -- JSON
    next_steps TEXT                     -- JSON
);

CREATE INDEX IF NOT EXISTS idx_projects_user ON user_projects(user_id);
CREATE INDEX IF NOT EXISTS idx_projects_status ON user_projects(status);

-- ============================================
-- 5. 主动服务队列
-- ============================================
CREATE TABLE IF NOT EXISTS pending_reminders (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    
    -- 提醒类型
    reminder_type TEXT CHECK(reminder_type IN ('follow_up', 'suggestion', 'checkpoint', 'pattern_alert', 'milestone_celebrate')),
    
    -- 内容
    content TEXT NOT NULL,
    trigger_reason TEXT,
    
    -- 触发条件
    trigger_at TIMESTAMP,
    trigger_condition TEXT,
    
    -- 上下文
    context_session_id TEXT,
    context_insight_id TEXT,
    
    -- 执行状态
    status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'sent', 'dismissed')),
    sent_at TIMESTAMP,
    user_response TEXT
);

CREATE INDEX IF NOT EXISTS idx_reminders_user ON pending_reminders(user_id);
CREATE INDEX IF NOT EXISTS idx_reminders_status ON pending_reminders(status);
CREATE INDEX IF NOT EXISTS idx_reminders_trigger ON pending_reminders(trigger_at);

-- ============================================
-- 6. 行为模式
-- ============================================
CREATE TABLE IF NOT EXISTS behavior_patterns (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    
    -- 模式描述
    pattern_name TEXT,
    pattern_description TEXT,
    pattern_category TEXT CHECK(pattern_category IN ('communication', 'decision', 'learning', 'emotion')),
    
    -- 识别特征
    trigger_signals TEXT,               -- JSON
    manifestation TEXT,
    frequency TEXT CHECK(frequency IN ('always', 'often', 'sometimes', 'rarely')),
    
    -- 影响
    positive_impact TEXT,
    negative_impact TEXT,
    
    -- 应对策略
    best_response_strategy TEXT,
    things_to_avoid TEXT,
    
    -- 统计
    observed_count INTEGER DEFAULT 1,
    first_observed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_observed TIMESTAMP,
    confirmed BOOLEAN DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_behavior_user ON behavior_patterns(user_id);

-- ============================================
-- 初始化数据
-- ============================================

-- ============================================
-- 7. 隐私配置
-- ============================================
CREATE TABLE IF NOT EXISTS privacy_settings (
    user_id TEXT PRIMARY KEY,
    store_conversations BOOLEAN DEFAULT 1,
    store_mood BOOLEAN DEFAULT 1,
    store_detailed_facts BOOLEAN DEFAULT 0,
    auto_delete_days INTEGER DEFAULT 90,
    sensitive_filter_enabled BOOLEAN DEFAULT 1,
    encryption_enabled BOOLEAN DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- 8. 数据访问审计日志
-- ============================================
CREATE TABLE IF NOT EXISTS data_access_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    access_type TEXT CHECK(access_type IN ('read', 'write', 'delete', 'export')),
    accessed_by TEXT,               -- 系统组件/用户命令
    access_reason TEXT,
    records_affected INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_access_log_user ON data_access_log(user_id);
CREATE INDEX IF NOT EXISTS idx_access_log_time ON data_access_log(timestamp);

-- ============================================
-- 9. 智能决策记录
-- ============================================
CREATE TABLE IF NOT EXISTS intelligent_decisions (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    
    -- 决策信息
    decision_context TEXT,          -- 决策场景描述
    decision_type TEXT CHECK(decision_type IN ('recommendation', 'prediction', 'optimization', 'support')),
    
    -- AI建议
    ai_suggestion TEXT,
    ai_reasoning TEXT,              -- AI推理过程
    confidence REAL CHECK(confidence BETWEEN 0 AND 1),
    
    -- 用户选择
    user_choice TEXT,               -- 用户实际选择
    user_feedback TEXT,             -- 用户反馈
    
    -- 结果评估
    outcome_score INTEGER CHECK(outcome_score BETWEEN 1 AND 10),
    outcome_notes TEXT,
    
    -- 学习
    prediction_accuracy BOOLEAN,    -- 预测是否准确
    lesson_learned TEXT,            -- 学到的经验
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_decisions_user ON intelligent_decisions(user_id);
CREATE INDEX IF NOT EXISTS idx_decisions_type ON intelligent_decisions(decision_type);

-- ============================================
-- 10. 预测准确率追踪
-- ============================================
CREATE TABLE IF NOT EXISTS prediction_accuracy (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    prediction_type TEXT,           -- question/timing/need
    prediction_content TEXT,        -- 预测内容
    actual_outcome TEXT,            -- 实际结果
    was_correct BOOLEAN,
    confidence REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_accuracy_user ON prediction_accuracy(user_id);

-- ============================================
-- 12. 代理任务管理 (蜂群智能)
-- ============================================
CREATE TABLE IF NOT EXISTS agent_tasks (
    id TEXT PRIMARY KEY,
    main_task_id TEXT,              -- 主任务ID
    subtask_id TEXT,                -- 子任务ID
    agent_type TEXT,                -- 设计/架构/代码/测试/搜索/分析
    status TEXT CHECK(status IN ('pending', 'running', 'completed', 'failed')),
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    result_summary TEXT,
    shared_brain_snapshot TEXT,     -- 执行时的超脑快照
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_agent_tasks_main ON agent_tasks(main_task_id);
CREATE INDEX IF NOT EXISTS idx_agent_tasks_status ON agent_tasks(status);

-- ============================================
-- 13. 代理输出共享 (共享大脑核心)
-- ============================================
CREATE TABLE IF NOT EXISTS agent_outputs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id TEXT NOT NULL,
    subtask_id TEXT NOT NULL,
    output TEXT,                    -- JSON格式的输出
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    consumed_by TEXT                -- 被哪个代理读取了
);

CREATE INDEX IF NOT EXISTS idx_agent_outputs_subtask ON agent_outputs(subtask_id);

-- ============================================
-- 14. 代理协作日志
-- ============================================
CREATE TABLE IF NOT EXISTS agent_collaboration_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    main_task_id TEXT NOT NULL,
    from_agent TEXT,
    to_agent TEXT,
    action TEXT CHECK(action IN ('write', 'read', 'notify', 'complete')),
    data_ref TEXT,                  -- 引用的数据ID
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_collab_main ON agent_collaboration_log(main_task_id);

-- ============================================
-- 16. 自我进化日志 (Self-Evolution)
-- ============================================
CREATE TABLE IF NOT EXISTS self_evolution_log (
    id TEXT PRIMARY KEY,
    user_id TEXT,
    evolution_type TEXT CHECK(evolution_type IN (
        'performance_analysis',
        'prompt_update',
        'skill_create',
        'knowledge_gain',
        'strategy_change'
    )),
    before_state TEXT,        -- JSON: 改进前状态
    after_state TEXT,         -- JSON: 改进后状态
    improvements TEXT,        -- JSON: 改进建议
    improvement_score REAL,   -- 改进效果评分
    applied BOOLEAN DEFAULT 0,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_evolution_user ON self_evolution_log(user_id);
CREATE INDEX IF NOT EXISTS idx_evolution_type ON self_evolution_log(evolution_type);

-- ============================================
-- 17. 知识盲区追踪
-- ============================================
CREATE TABLE IF NOT EXISTS knowledge_gaps (
    id TEXT PRIMARY KEY,
    user_id TEXT,
    topic TEXT NOT NULL,
    context TEXT,             -- 触发场景
    frequency INTEGER DEFAULT 1,
    last_occurred TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    priority REAL DEFAULT 0.5,
    suggested_action TEXT,
    status TEXT CHECK(status IN ('detected', 'learning', 'resolved')),
    resolution_notes TEXT
);

CREATE INDEX IF NOT EXISTS idx_gaps_user ON knowledge_gaps(user_id);
CREATE INDEX IF NOT EXISTS idx_gaps_topic ON knowledge_gaps(topic);

-- ============================================
-- 18. 技能版本历史
-- ============================================
CREATE TABLE IF NOT EXISTS skill_versions (
    id TEXT PRIMARY KEY,
    skill_name TEXT NOT NULL,
    version TEXT NOT NULL,
    changes TEXT,             -- JSON: 改了什么
    performance_before REAL,
    performance_after REAL,
    performance_delta REAL,
    created_by TEXT,          -- 'auto' or 'manual'
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_versions_skill ON skill_versions(skill_name);

-- ============================================
-- 19. 性能指标追踪
-- ============================================
CREATE TABLE IF NOT EXISTS performance_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    metric_name TEXT,         -- understanding_accuracy, user_satisfaction, etc.
    metric_value REAL,
    period_start TIMESTAMP,
    period_end TIMESTAMP,
    sample_size INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_metrics_user ON performance_metrics(user_id);
CREATE INDEX IF NOT EXISTS idx_metrics_name ON performance_metrics(metric_name);

-- ============================================
-- 20. 改进建议队列
-- ============================================
CREATE TABLE IF NOT EXISTS improvement_queue (
    id TEXT PRIMARY KEY,
    user_id TEXT,
    improvement_type TEXT CHECK(improvement_type IN (
        'prompt_update',
        'skill_create',
        'knowledge_learn',
        'strategy_adjust'
    )),
    priority INTEGER,         -- 1=highest, 5=lowest
    description TEXT,
    rationale TEXT,           -- 为什么需要改进
    expected_impact TEXT,
    status TEXT CHECK(status IN ('pending', 'approved', 'applied', 'rejected')),
    applied_at TIMESTAMP,
    result TEXT,              -- 应用后的结果
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_improvement_user ON improvement_queue(user_id);
CREATE INDEX IF NOT EXISTS idx_improvement_status ON improvement_queue(status);

-- ============================================
-- 21. 系统配置
-- ============================================
CREATE TABLE IF NOT EXISTS super_brain_config (
    key TEXT PRIMARY KEY,
    value TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT OR IGNORE INTO super_brain_config (key, value) VALUES
('version', '2.0'),
('initialized_at', datetime('now')),
('total_users', '0'),
('total_insights', '0'),
('privacy_policy_version', '1.0'),
('swarm_intelligence_enabled', 'true'),
('self_evolution_enabled', 'true');
