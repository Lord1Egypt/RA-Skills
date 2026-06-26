-- agent-memory SQLite Schema
-- 所有结构化维度 + 关联关系存储

-- 主表：记忆记录
CREATE TABLE IF NOT EXISTS memories (
    memory_id       TEXT PRIMARY KEY,
    time_id         TEXT NOT NULL,
    time_ts         INTEGER NOT NULL,
    person_id       TEXT NOT NULL,
    nature_id       TEXT NOT NULL,
    content         TEXT NOT NULL,
    content_hash    TEXT NOT NULL,
    importance      TEXT DEFAULT 'medium',
    is_aggregated   INTEGER DEFAULT 0,
    source_count    INTEGER DEFAULT 1,
    -- 多 Agent 扩展
    owner_agent_id  TEXT DEFAULT '_system',     -- 创建者 Agent ID
    visibility      TEXT DEFAULT 'team',        -- private / team / public
    -- 多租户隔离
    tenant_id       TEXT NOT NULL DEFAULT 'default',  -- 租户 ID（SHARED_DB 模式行级隔离）
    -- Phase 1: 情感编码
    valence         REAL DEFAULT 0.0,           -- 效价 [-1.0, 1.0]
    arousal         REAL DEFAULT 0.2,           -- 唤醒度 [0.0, 1.0]
    dominance       REAL DEFAULT 0.5,           -- 支配度 [0.0, 1.0]
    significance    TEXT DEFAULT 'notable',      -- trivial/notable/important/breakthrough/crisis/milestone
    confidence      REAL DEFAULT 0.5,           -- 内容质量置信度 [0.0, 1.0]
    primary_emotions TEXT DEFAULT '{}',          -- JSON: Plutchik 8-vector
    compound_emotions TEXT DEFAULT '[]',         -- JSON: detected dyads
    source          TEXT DEFAULT 'agent_memory', -- 来源: agent_memory/openclaw/hermes
    source_id       TEXT DEFAULT '',             -- 来源系统中的 ID（防重复同步）
    deleted         INTEGER DEFAULT 0,           -- 软删除标记（0=正常, 1=已删除）
    deleted_at      REAL DEFAULT NULL,           -- 软删除时间戳（Unix epoch）
    custom_ttl      INTEGER DEFAULT NULL,        -- 自定义 TTL（秒），NULL=使用默认策略
    -- Phase 2.1: 双时间线事实管理
    valid_from      REAL DEFAULT NULL,           -- 事实开始有效的时间戳（Unix epoch）
    valid_until     REAL DEFAULT NULL,           -- 事实失效的时间戳（NULL=仍然有效）
    occurrence_time REAL DEFAULT NULL,           -- 事件实际发生的时间（区别于写入时间 time_ts）
    mention_time    REAL DEFAULT NULL,           -- 用户首次提及此事实的时间
    last_accessed_ts REAL DEFAULT NULL,          -- 最近访问时间戳（用于 recency bias 和淘汰排序）
    bookmarked      INTEGER DEFAULT 0,           -- 书签标记（0=未收藏, 1=已收藏）
    created_at      INTEGER NOT NULL DEFAULT (strftime('%s','now'))
);

-- Agent 注册表
CREATE TABLE IF NOT EXISTS agents (
    agent_id        TEXT PRIMARY KEY,           -- Agent 唯一标识
    agent_name      TEXT NOT NULL,              -- 显示名
    team_id         TEXT DEFAULT 'default',     -- 所属团队
    capabilities    TEXT DEFAULT '[]',          -- JSON: 能力标签 ["coding", "writing"]
    status          TEXT DEFAULT 'active',      -- active / inactive
    created_at      INTEGER NOT NULL DEFAULT (strftime('%s','now'))
);

-- 记忆访问权限（细粒度控制）
CREATE TABLE IF NOT EXISTS memory_permissions (
    memory_id       TEXT NOT NULL,
    agent_id        TEXT NOT NULL,              -- 被授权的 Agent
    permission      TEXT DEFAULT 'read',        -- read / write / admin
    granted_by      TEXT NOT NULL,              -- 授权者 Agent ID
    granted_at      INTEGER NOT NULL DEFAULT (strftime('%s','now')),
    expires_at      INTEGER,                   -- 过期时间（NULL=永久）
    FOREIGN KEY (memory_id) REFERENCES memories(memory_id),
    PRIMARY KEY (memory_id, agent_id)
);

-- Agent 间的知识关联（跨 Agent 联想）
CREATE TABLE IF NOT EXISTS agent_associations (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    source_agent    TEXT NOT NULL,
    target_agent    TEXT NOT NULL,
    memory_id       TEXT NOT NULL,
    association_type TEXT NOT NULL,             -- shares_knowledge / depends_on / contradicts
    reason          TEXT,
    created_at      INTEGER NOT NULL DEFAULT (strftime('%s','now')),
    FOREIGN KEY (memory_id) REFERENCES memories(memory_id)
);

CREATE INDEX IF NOT EXISTS idx_mem_owner ON memories(owner_agent_id);
CREATE INDEX IF NOT EXISTS idx_mem_visibility ON memories(visibility);
CREATE INDEX IF NOT EXISTS idx_mem_owner_vis ON memories(owner_agent_id, visibility);
CREATE INDEX IF NOT EXISTS idx_mem_tenant_id ON memories(tenant_id);
CREATE INDEX IF NOT EXISTS idx_memories_deleted ON memories(deleted);
CREATE INDEX IF NOT EXISTS idx_perm_agent ON memory_permissions(agent_id);
CREATE INDEX IF NOT EXISTS idx_perm_memory ON memory_permissions(memory_id);
CREATE INDEX IF NOT EXISTS idx_agent_team ON agents(team_id);
CREATE INDEX IF NOT EXISTS idx_assoc_source ON agent_associations(source_agent);
CREATE INDEX IF NOT EXISTS idx_assoc_target ON agent_associations(target_agent);

-- 主题关联
CREATE TABLE IF NOT EXISTS memory_topics (
    memory_id       TEXT NOT NULL,
    topic_code      TEXT NOT NULL,
    is_primary      INTEGER DEFAULT 1,
    FOREIGN KEY (memory_id) REFERENCES memories(memory_id),
    PRIMARY KEY (memory_id, topic_code)
);

-- 知识类型关联
CREATE TABLE IF NOT EXISTS memory_knowledge (
    memory_id       TEXT NOT NULL,
    knowledge_id    TEXT NOT NULL,
    FOREIGN KEY (memory_id) REFERENCES memories(memory_id),
    PRIMARY KEY (memory_id, knowledge_id)
);

-- 工具关联
CREATE TABLE IF NOT EXISTS memory_tools (
    memory_id       TEXT NOT NULL,
    tool_id         TEXT NOT NULL,
    FOREIGN KEY (memory_id) REFERENCES memories(memory_id),
    PRIMARY KEY (memory_id, tool_id)
);

-- 关联关系
CREATE TABLE IF NOT EXISTS memory_links (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id       TEXT NOT NULL,
    target_id       TEXT NOT NULL,
    link_type       TEXT NOT NULL,
    weight          REAL DEFAULT 1.0,
    reason          TEXT,
    created_at      INTEGER NOT NULL DEFAULT (strftime('%s','now')),
    FOREIGN KEY (source_id) REFERENCES memories(memory_id),
    FOREIGN KEY (target_id) REFERENCES memories(memory_id)
);

-- 对话窗口
CREATE TABLE IF NOT EXISTS windows (
    window_id       TEXT PRIMARY KEY,
    start_time      INTEGER NOT NULL,
    end_time        INTEGER,
    person_id       TEXT NOT NULL,
    message_count   INTEGER DEFAULT 0,
    topic_dominant  TEXT
);

-- 窗口-记录映射
CREATE TABLE IF NOT EXISTS window_memories (
    window_id       TEXT NOT NULL,
    memory_id       TEXT NOT NULL,
    seq_order       INTEGER NOT NULL,
    FOREIGN KEY (window_id) REFERENCES windows(window_id),
    FOREIGN KEY (memory_id) REFERENCES memories(memory_id),
    PRIMARY KEY (window_id, memory_id)
);

-- ═══════════════════════════════════════════════════════
-- 索引策略
-- ═══════════════════════════════════════════════════════

-- 单列索引
CREATE INDEX IF NOT EXISTS idx_mem_time ON memories(time_ts);
CREATE INDEX IF NOT EXISTS idx_mem_person ON memories(person_id);
CREATE INDEX IF NOT EXISTS idx_mem_nature ON memories(nature_id);
CREATE INDEX IF NOT EXISTS idx_mem_importance ON memories(importance);
CREATE INDEX IF NOT EXISTS idx_mem_hash ON memories(content_hash);
CREATE INDEX IF NOT EXISTS idx_mem_aggregated ON memories(is_aggregated);

-- 复合索引：覆盖最常见的查询模式
-- "按时间范围 + 重要度过滤" — 最高频组合
CREATE INDEX IF NOT EXISTS idx_mem_time_importance ON memories(time_ts, importance);
-- "按时间范围 + 人物"
CREATE INDEX IF NOT EXISTS idx_mem_time_person ON memories(time_ts, person_id);
-- "按人物 + 性质"
CREATE INDEX IF NOT EXISTS idx_mem_person_nature ON memories(person_id, nature_id);
-- "按重要度 + 时间倒序" — 高优先记忆快速检索
CREATE INDEX IF NOT EXISTS idx_mem_importance_time ON memories(importance, time_ts DESC);
-- "按性质 + 聚合标记" — 查找可压缩的非聚合记忆
CREATE INDEX IF NOT EXISTS idx_mem_nature_aggregated ON memories(nature_id, is_aggregated);
-- "按创建时间" — 归档/清理查询
CREATE INDEX IF NOT EXISTS idx_mem_created ON memories(created_at);
-- Phase 1: 情感索引
CREATE INDEX IF NOT EXISTS idx_mem_significance ON memories(significance);
CREATE INDEX IF NOT EXISTS idx_mem_valence ON memories(valence);
CREATE INDEX IF NOT EXISTS idx_mem_arousal ON memories(arousal);
CREATE INDEX IF NOT EXISTS idx_mem_dominance ON memories(dominance);
-- Phase 2.1: 双时间线索引
CREATE INDEX IF NOT EXISTS idx_memories_valid_until ON memories(valid_until);
CREATE INDEX IF NOT EXISTS idx_memories_valid_from ON memories(valid_from);
CREATE INDEX IF NOT EXISTS idx_memories_occurrence ON memories(occurrence_time);

-- ═══════════════════════════════════════════════════════
-- Phase 2.2: 实体消解引擎 — 实体/关系/记忆-实体关联
-- ═══════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS entities (
    entity_id       TEXT PRIMARY KEY,
    canonical_name  TEXT NOT NULL,
    entity_type     TEXT NOT NULL DEFAULT 'person',  -- person/org/location/concept/other
    aliases         TEXT DEFAULT '[]',               -- JSON array of alternative names
    first_seen      REAL NOT NULL,
    last_seen       REAL NOT NULL,
    mention_count   INTEGER DEFAULT 1,
    metadata        TEXT DEFAULT '{}',               -- JSON
    created_at      REAL NOT NULL DEFAULT (strftime('%s','now'))
);

CREATE TABLE IF NOT EXISTS relations (
    relation_id         TEXT PRIMARY KEY,
    subject_entity_id   TEXT NOT NULL,
    predicate           TEXT NOT NULL,
    object_entity_id    TEXT NOT NULL,
    source_memory_id    TEXT,
    confidence          REAL DEFAULT 1.0,
    valid_from          REAL,
    valid_until         REAL,
    created_at          REAL NOT NULL DEFAULT (strftime('%s','now')),
    FOREIGN KEY (subject_entity_id) REFERENCES entities(entity_id),
    FOREIGN KEY (object_entity_id) REFERENCES entities(entity_id)
);

CREATE TABLE IF NOT EXISTS memory_entities (
    memory_id   TEXT NOT NULL,
    entity_id   TEXT NOT NULL,
    role        TEXT DEFAULT 'subject',  -- subject/object/mentioned
    FOREIGN KEY (memory_id) REFERENCES memories(memory_id),
    FOREIGN KEY (entity_id) REFERENCES entities(entity_id),
    PRIMARY KEY (memory_id, entity_id)
);

CREATE INDEX IF NOT EXISTS idx_entities_type ON entities(entity_type);
CREATE INDEX IF NOT EXISTS idx_entities_canonical ON entities(canonical_name);
CREATE INDEX IF NOT EXISTS idx_entities_canonical_type ON entities(canonical_name, entity_type);
CREATE INDEX IF NOT EXISTS idx_relations_subject ON relations(subject_entity_id);
CREATE INDEX IF NOT EXISTS idx_relations_object ON relations(object_entity_id);
CREATE INDEX IF NOT EXISTS idx_memory_entities_entity ON memory_entities(entity_id);

-- 新增复合索引：优化常见查询模式
-- "按时间范围 + 主题" — 时间和主题的组合查询
CREATE INDEX IF NOT EXISTS idx_mem_time_topic ON memories(time_ts, person_id, nature_id);
-- "按主题 + 重要度" — 主题和重要度的组合查询
CREATE INDEX IF NOT EXISTS idx_mem_topic_importance ON memory_topics(topic_code, memory_id);
-- "按工具 + 时间" — 工具和时间的组合查询
CREATE INDEX IF NOT EXISTS idx_mem_tool_time ON memory_tools(tool_id, memory_id);
-- "按知识类型 + 时间" — 知识类型和时间的组合查询
CREATE INDEX IF NOT EXISTS idx_mem_knowledge_time ON memory_knowledge(knowledge_id, memory_id);
-- "按可见性 + 所有者" — 权限过滤查询
CREATE INDEX IF NOT EXISTS idx_mem_visibility_owner ON memories(visibility, owner_agent_id);

-- 关联表索引
CREATE INDEX IF NOT EXISTS idx_link_source ON memory_links(source_id);
CREATE INDEX IF NOT EXISTS idx_link_target ON memory_links(target_id);
CREATE INDEX IF NOT EXISTS idx_link_type ON memory_links(link_type);
CREATE INDEX IF NOT EXISTS idx_link_source_type ON memory_links(source_id, link_type);
CREATE INDEX IF NOT EXISTS idx_link_target_type ON memory_links(target_id, link_type);
-- S9: 缺失的复合索引
CREATE INDEX IF NOT EXISTS idx_link_type_target ON memory_links(link_type, target_id);
CREATE INDEX IF NOT EXISTS idx_mem_deleted_importance_time ON memories(deleted, importance, time_ts);
CREATE INDEX IF NOT EXISTS idx_mem_deleted_tenant ON memories(deleted, tenant_id);

-- Missing indexes for last_accessed_ts and bookmarked
CREATE INDEX IF NOT EXISTS idx_mem_last_accessed ON memories(last_accessed_ts);
CREATE INDEX IF NOT EXISTS idx_mem_bookmarked ON memories(bookmarked);

-- 主题索引
CREATE INDEX IF NOT EXISTS idx_topic_code ON memory_topics(topic_code);
CREATE INDEX IF NOT EXISTS idx_topic_memory ON memory_topics(memory_id, is_primary);

-- 待办任务
CREATE TABLE IF NOT EXISTS tasks (
    task_id         TEXT PRIMARY KEY,
    memory_id       TEXT NOT NULL,
    title           TEXT NOT NULL,
    status          TEXT DEFAULT 'pending',
    assignee        TEXT DEFAULT 'ai',
    deadline        INTEGER,
    created_at      INTEGER NOT NULL DEFAULT (strftime('%s','now')),
    updated_at      INTEGER NOT NULL DEFAULT (strftime('%s','now')),
    completed_at    INTEGER,
    topic_code      TEXT,
    FOREIGN KEY (memory_id) REFERENCES memories(memory_id)
);

CREATE INDEX IF NOT EXISTS idx_task_status ON tasks(status);
-- "按任务状态 + 截止时间" — 任务管理查询
CREATE INDEX IF NOT EXISTS idx_task_status_deadline ON tasks(status, deadline);
-- "按任务分配 + 状态" — 任务分配查询
CREATE INDEX IF NOT EXISTS idx_task_assignee_status ON tasks(assignee, status, deadline);
CREATE INDEX IF NOT EXISTS idx_task_memory ON tasks(memory_id);
CREATE INDEX IF NOT EXISTS idx_task_deadline ON tasks(deadline);

-- ═══════════════════════════════════════════════════════
-- 记忆版本化（流式更新）
-- ═══════════════════════════════════════════════════════

-- 每条记忆的版本历史
-- 主表 memories 存储最新版本，此表存储完整版本链
CREATE TABLE IF NOT EXISTS memory_versions (
    version_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    memory_id       TEXT NOT NULL,
    content         TEXT NOT NULL,
    content_hash    TEXT NOT NULL,
    importance      TEXT DEFAULT 'medium',
    topics_json     TEXT DEFAULT '[]',          -- JSON: 当时的主题列表
    change_reason   TEXT,                        -- 变更原因
    created_at      INTEGER NOT NULL DEFAULT (strftime('%s','now')),
    FOREIGN KEY (memory_id) REFERENCES memories(memory_id)
);

CREATE INDEX IF NOT EXISTS idx_mv_memory ON memory_versions(memory_id);
CREATE INDEX IF NOT EXISTS idx_mv_created ON memory_versions(memory_id, created_at DESC);

-- ═══════════════════════════════════════════════════════
-- Phase 2: 自我指涉 — 推理追踪 + 反思
-- ═══════════════════════════════════════════════════════

-- 推理追踪：记录每次检索/决策的推理过程
CREATE TABLE IF NOT EXISTS reasoning_traces (
    trace_id        TEXT PRIMARY KEY,
    query           TEXT NOT NULL,              -- 检索/决策的查询
    result_summary  TEXT,                        -- 结果摘要
    confidence      REAL DEFAULT 0.0,           -- 最终置信度 [0.0, 1.0]
    sources_used    TEXT DEFAULT '[]',           -- JSON: 用到的 memory_id 列表
    steps           TEXT DEFAULT '[]',           -- JSON: 推理步骤 [{step_type, detail, timestamp}]
    uncertainty     TEXT DEFAULT '[]',           -- JSON: 不确定因素列表
    created_at      INTEGER NOT NULL DEFAULT (strftime('%s','now'))
);

-- 自我反思：基于低置信度推理生成的反思记录
CREATE TABLE IF NOT EXISTS self_reflections (
    reflection_id   TEXT PRIMARY KEY,
    trace_id        TEXT,                        -- 关联的推理追踪
    insight         TEXT NOT NULL,               -- 反思内容
    action_taken    TEXT,                        -- 采取的修正行动
    created_at      INTEGER NOT NULL DEFAULT (strftime('%s','now')),
    FOREIGN KEY (trace_id) REFERENCES reasoning_traces(trace_id)
);

CREATE INDEX IF NOT EXISTS idx_trace_query ON reasoning_traces(query);
CREATE INDEX IF NOT EXISTS idx_trace_confidence ON reasoning_traces(confidence);
CREATE INDEX IF NOT EXISTS idx_trace_created ON reasoning_traces(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_reflection_trace ON self_reflections(trace_id);
CREATE INDEX IF NOT EXISTS idx_reflection_created ON self_reflections(created_at DESC);

-- ═══════════════════════════════════════════════════════
-- Phase 4: 内在动机 — Agent 内在状态
-- ═══════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS internal_state (
    state_id        TEXT PRIMARY KEY,           -- 'current' 固定值
    curiosity       REAL DEFAULT 0.3,           -- 好奇心 [0, 1]
    boredom         REAL DEFAULT 0.0,           -- 无聊度 [0, 1]
    confidence      REAL DEFAULT 0.5,           -- 自信度 [0, 1]
    satisfaction    REAL DEFAULT 0.5,           -- 满足感 [0, 1]
    urgency         REAL DEFAULT 0.0,           -- 紧迫感 [0, 1]
    dominant_drive  TEXT DEFAULT 'none',         -- 当前主导动机
    updated_at      INTEGER NOT NULL DEFAULT (strftime('%s','now'))
);

-- ═══════════════════════════════════════════════════════
-- Phase 5: 叙事自我 — 身份模型 + 生命叙事
-- ═══════════════════════════════════════════════════════

-- 身份模型：动态更新的自我认知
CREATE TABLE IF NOT EXISTS identity_model (
    key             TEXT PRIMARY KEY,           -- core_values / preferences / expertise / personality_traits / interests / _meta
    value           TEXT NOT NULL,              -- JSON
    confidence      REAL DEFAULT 0.5,
    evidence_count  INTEGER DEFAULT 0,
    updated_at      INTEGER NOT NULL DEFAULT (strftime('%s','now'))
);

-- 生命叙事：从记忆构建的叙事记录
CREATE TABLE IF NOT EXISTS life_narratives (
    narrative_id        TEXT PRIMARY KEY,
    narrative_type      TEXT NOT NULL,           -- daily / topic / milestone / identity
    title               TEXT NOT NULL,
    content             TEXT NOT NULL,            -- Markdown 叙事
    period_start        INTEGER,
    period_end          INTEGER,
    source_memory_count INTEGER DEFAULT 0,
    created_at          INTEGER NOT NULL DEFAULT (strftime('%s','now'))
);

CREATE INDEX IF NOT EXISTS idx_identity_key ON identity_model(key);
CREATE INDEX IF NOT EXISTS idx_narrative_type ON life_narratives(narrative_type);
CREATE INDEX IF NOT EXISTS idx_narrative_created ON life_narratives(created_at DESC);

-- ═══════════════════════════════════════════════════════
-- V9.2.0: 文档分段索引
-- ═══════════════════════════════════════════════════════

-- 文档级元数据
CREATE TABLE IF NOT EXISTS document_meta (
    doc_id          TEXT PRIMARY KEY,
    title           TEXT NOT NULL,
    author          TEXT DEFAULT '',
    source_path     TEXT NOT NULL,
    source_type     TEXT DEFAULT 'text',
    total_chunks    INTEGER DEFAULT 0,
    total_chars     INTEGER DEFAULT 0,
    created_at      INTEGER NOT NULL,
    updated_at      INTEGER NOT NULL
);

-- 分段级元数据
CREATE TABLE IF NOT EXISTS chunk_meta (
    chunk_id        TEXT PRIMARY KEY,
    memory_id       TEXT NOT NULL,
    doc_id          TEXT NOT NULL,
    chapter         TEXT DEFAULT '',
    section         TEXT DEFAULT '',
    page_num        INTEGER DEFAULT 0,
    position        INTEGER DEFAULT 0,
    prev_chunk_id   TEXT DEFAULT '',
    next_chunk_id   TEXT DEFAULT '',
    char_offset     INTEGER DEFAULT 0,
    char_length     INTEGER DEFAULT 0,
    FOREIGN KEY (memory_id) REFERENCES memories(memory_id),
    FOREIGN KEY (doc_id) REFERENCES document_meta(doc_id)
);

CREATE INDEX IF NOT EXISTS idx_chunk_doc ON chunk_meta(doc_id);
CREATE INDEX IF NOT EXISTS idx_chunk_memory ON chunk_meta(memory_id);
CREATE INDEX IF NOT EXISTS idx_chunk_position ON chunk_meta(doc_id, position);
CREATE INDEX IF NOT EXISTS idx_chunk_chapter ON chunk_meta(doc_id, chapter);
CREATE INDEX IF NOT EXISTS idx_doc_source ON document_meta(source_path);
CREATE INDEX IF NOT EXISTS idx_doc_type ON document_meta(source_type);

-- ═══════════════════════════════════════════════════════
-- Phase 2.1: 双时间线事实管理 — Schema 迁移
-- 为已有数据库添加新字段（IF NOT EXISTS 模式，幂等安全）
-- ═══════════════════════════════════════════════════════

-- SQLite 不支持 ALTER TABLE ADD COLUMN IF NOT EXISTS，
-- 使用 pragma_table_info 检测列是否存在，在 Python 层执行迁移。
-- 迁移逻辑见 store.py _ensure_schema() 中的 _migrate_temporal_columns()
