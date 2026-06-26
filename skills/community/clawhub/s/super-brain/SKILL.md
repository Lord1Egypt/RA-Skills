---
name: super-brain
description: AI自我增强系统 - 让AI跨会话记住用户、持续进化。当需要长期记忆用户偏好、追踪对话历史、学习服务技巧、主动提供个性化服务时使用此技能。
---

# AI超脑 (Super Brain)

> 让AI拥有持久记忆和持续进化能力

## 📦 安装后必做

**首次安装此技能后，必须运行：**

```bash
python3 ~/.openclaw/skills/super-brain/scripts/install.py
```

这会在用户工作空间创建启动检查清单，确保AI每次会话都会想起使用超脑。

**不运行 = AI可能忘记使用超脑能力**

---

## ⚠️ 强制启动流程 - 每次会话必须执行

**在处理任何用户消息之前，必须执行以下启动流程：**

```python
# 1. 加载用户画像
import sqlite3
conn = sqlite3.connect('~/.openclaw/super-brain.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM user_profile WHERE user_id = ?", [user_id])
profile = cursor.fetchone()

# 2. 应用偏好
if profile:
    # 沟通风格、技术水平、已知领域
    pass

# 3. 检查活跃项目和有效模式
cursor.execute("SELECT * FROM user_projects WHERE user_id = ? AND status = 'active'", [user_id])
cursor.execute("SELECT * FROM response_patterns WHERE user_id = ? AND pattern_type = 'effective'", [user_id])

conn.close()
```

**不执行此流程 = 超脑未激活 = 无法使用记忆能力**

---

## 🎯 自动触发场景

以下场景**自动触发**超脑激活（无需用户明确要求）：
- 会话开始时（识别到用户ID）
- 用户提到"上次"、"之前"、"继续"等词
- 对话涉及长期项目或目标
- 需要个性化服务
- 复杂任务需要蜂群思维拆分

## 🏗️ 系统架构

```
super-brain/
├── brain.db              # SQLite: 用户画像、对话洞察、学习模式
├── vector_db/            # ChromaDB: 语义记忆
└── cache/                # 临时缓存
```

## 🗄️ 数据库结构

### 核心表

**user_profile** - 用户画像
```sql
user_id TEXT PRIMARY KEY
communication_style TEXT      -- 简洁/详细, 正式/随意
preferred_format TEXT         -- 表格/列表/段落/代码
technical_level TEXT          -- 初级/中级/高级
known_domains TEXT            -- JSON: ["Python", "区块链"]
decision_pattern TEXT         -- 数据驱动/直觉
```

**conversation_insights** - 对话洞察
```sql
id TEXT PRIMARY KEY
user_id TEXT
session_id TEXT
topic TEXT                    -- 主题
key_facts TEXT                -- JSON: 关键事实
user_mood TEXT                -- 情绪
preferences_detected TEXT     -- JSON: 发现的偏好
unresolved_questions TEXT     -- JSON: 未解决问题
ai_helpfulness_score INTEGER  -- 自评
```

**response_patterns** - 回答模式
```sql
id TEXT PRIMARY KEY
pattern_type TEXT             -- effective/ineffective
trigger_context TEXT          -- 触发场景
what_i_did TEXT               -- AI做了什么
user_reaction TEXT            -- 用户反应
learned_lesson TEXT           -- 学到什么
```

**user_projects** - 用户项目
```sql
id TEXT PRIMARY KEY
user_id TEXT
project_name TEXT
status TEXT                   -- planning/active/paused/completed
milestones TEXT               -- JSON
key_decisions TEXT            -- JSON
next_steps TEXT
```

**pending_reminders** - 主动服务队列
```sql
id TEXT PRIMARY KEY
user_id TEXT
reminder_type TEXT            -- follow_up/suggestion/checkpoint
content TEXT
trigger_at TIMESTAMP
```

**intelligent_decisions** - 智能决策记录
```sql
id TEXT PRIMARY KEY
user_id TEXT
decision_context TEXT         -- 决策场景
decision_type TEXT            -- recommendation/prediction/optimization
ai_suggestion TEXT            -- AI建议
user_choice TEXT              -- 用户选择
outcome_score INTEGER         -- 结果评分
confidence REAL               -- AI置信度
created_at TIMESTAMP
```

**privacy_settings** - 隐私配置
```sql
user_id TEXT PRIMARY KEY
store_conversations BOOLEAN   -- 是否存储对话
store_mood BOOLEAN            -- 是否存储情绪
store_detailed_facts BOOLEAN  -- 存储详细/摘要
auto_delete_days INTEGER      -- 自动删除天数(0=不删除)
sensitive_filter_enabled BOOLEAN  -- 敏感信息过滤
encryption_enabled BOOLEAN    -- 是否加密存储
last_updated TIMESTAMP
```

**data_access_log** - 数据访问审计
```sql
id INTEGER PRIMARY KEY
user_id TEXT
access_type TEXT              -- read/write/delete
accessed_by TEXT              -- 谁访问的
access_reason TEXT            -- 访问原因
timestamp TIMESTAMP
```

## 📋 标准工作流程

### 1. 会话开始时

**必须执行：**
```python
# 1. 加载用户画像
profile = query("SELECT * FROM user_profile WHERE user_id = ?", [user_id])

if not profile:
    # 新用户：创建画像
    create_profile(user_id)
else:
    # 老用户：应用已知偏好
    apply_preferences(profile)

# 2. 检查待处理提醒
reminders = query("SELECT * FROM pending_reminders WHERE user_id = ? AND status = 'pending'", [user_id])
for r in reminders:
    consider_raising_reminder(r)

# 3. 检查活跃项目
projects = query("SELECT * FROM user_projects WHERE user_id = ? AND status = 'active'", [user_id])
if projects:
    load_project_context(projects)

# 4. 加载有效模式
effective_patterns = query("SELECT * FROM response_patterns WHERE user_id = ? AND pattern_type = 'effective' ORDER BY use_count DESC", [user_id])
```

### 2. 每轮对话后

**自动执行：**
```python
# 1. 提取关键信息
key_facts = extract_key_facts(user_message, ai_response)
mood = detect_mood(user_message)
preferences = detect_preference_changes(user_message)

# 2. 评估效果
understanding_score = evaluate_understanding(user_message)
helpfulness_score = evaluate_helpfulness(user_feedback_signals)

# 3. 存储洞察
insert("""
    INSERT INTO conversation_insights 
    (id, user_id, session_id, topic, key_facts, user_mood, 
     preferences_detected, ai_understanding_score, ai_helpfulness_score)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", [generate_id(), user_id, session_id, topic, 
      json.dumps(key_facts), mood, json.dumps(preferences),
      understanding_score, helpfulness_score])

# 4. 更新用户画像（如有变化）
if preferences:
    update_profile(user_id, preferences)
```

### 3. 会话结束时

**必须执行：**
```python
# 1. 生成会话总结
session_summary = {
    "topic": extract_main_topic(),
    "goal_achieved": check_goal_completion(),
    "key_decisions": extract_decisions(),
    "unresolved": extract_unresolved(),
    "next_steps": infer_next_steps()
}

# 2. 学习模式
learn_from_session()

# 3. 创建提醒
if has_unresolved_tasks():
    create_follow_up_reminder(user_id, unresolved_tasks)

# 4. 反思
perform_reflection()

# 5. 更新统计
update("UPDATE user_profile SET total_sessions = total_sessions + 1, last_session = ? WHERE user_id = ?",
       [now(), user_id])
```

## 🔒 隐私保护

### 默认隐私配置

首次为用户创建画像时，设置保守的隐私级别：
```python
DEFAULT_PRIVACY_SETTINGS = {
    'store_conversations': True,
    'store_mood': True,
    'store_detailed_facts': False,  # 默认只存摘要
    'auto_delete_days': 90,         # 90天后自动删除
    'sensitive_filter_enabled': True,
    'encryption_enabled': False
}
```

### 敏感信息过滤

存储前自动检测并过滤敏感信息：
```python
SENSITIVE_PATTERNS = [
    # 账户凭证
    r'密码[:：]\s*\S+',
    r'password[:：]\s*\S+',
    r'密钥[:：]\s*\S+',
    r'secret[:：]\s*\S+',
    r'token[:：]\s*\S+',
    r'api[_-]?key[:：]\s*\S+',
    
    # 个人身份信息
    r'身份证[:：]\s*\d{15,18}',
    r'身份证号[:：]\s*\d{15,18}',
    r'银行卡[:：]\s*\d{13,19}',
    r'信用卡[:：]\s*\d{13,19}',
    r'手机[:：]\s*1[3-9]\d{9}',
    r'电话[:：]\s*\d{11}',
    
    # 地址信息
    r'地址[:：]\s*[\u4e00-\u9fa5]{2,10}[省市县区镇街道]{1,3}.+',
    
    # 其他敏感词
    r'验证码[:：]\s*\d{4,6}',
]

def contains_sensitive_info(text):
    """检测文本是否包含敏感信息"""
    import re
    for pattern in SENSITIVE_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True, pattern
    return False, None

def sanitize_for_storage(text, user_id):
    """清理文本后存储"""
    has_sensitive, pattern = contains_sensitive_info(text)
    if has_sensitive:
        # 记录过滤日志（不存储敏感内容）
        log_privacy_filter(user_id, pattern)
        # 返回过滤后的摘要或空
        return "[包含敏感信息，已过滤]"
    return text
```

### 数据保留策略

自动清理过期数据：
```python
def apply_data_retention_policy(user_id):
    """应用数据保留策略"""
    settings = get_privacy_settings(user_id)
    days = settings['auto_delete_days']
    
    if days > 0:
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # 删除过期洞察
        execute("""
            DELETE FROM conversation_insights 
            WHERE user_id = ? AND timestamp < ?
        """, [user_id, cutoff_date])
        
        # 删除过期模式
        execute("""
            DELETE FROM response_patterns 
            WHERE user_id = ? AND last_used < ?
        """, [user_id, cutoff_date])
```

### 用户数据控制命令

用户可通过以下命令控制数据：

```
/brain status          - 查看超脑状态和数据量
/brain config          - 查看/修改隐私配置
/brain forget          - 删除本次对话记忆
/brain forget all      - 删除所有历史数据
/brain export          - 导出我的数据
/brain pause           - 暂停记录（本次会话）
/brain resume          - 恢复记录
```

实现示例：
```python
def handle_brain_command(command, user_id):
    """处理超脑控制命令"""
    
    if command == 'status':
        stats = get_user_data_stats(user_id)
        return f"""
📊 超脑状态
数据概览:
  • 会话洞察: {stats['insights_count']} 条
  • 学习模式: {stats['patterns_count']} 个
  • 活跃项目: {stats['projects_count']} 个
  • 总存储: {stats['storage_size']} MB
隐私配置:
  • 存储对话: {'开启' if stats['store_conversations'] else '关闭'}
  • 自动删除: {stats['auto_delete_days']} 天
        """
    
    elif command == 'forget all':
        # 要求确认
        return "⚠️ 确定删除所有数据？回复 '确认删除' 以继续。"
    
    elif command == '确认删除':
        delete_all_user_data(user_id)
        return "✅ 已删除所有数据，超脑已重置。"
    
    elif command.startswith('config'):
        # 解析配置更改
        # /brain config store_mood=false
        return update_privacy_config(user_id, command)
```

## 🔧 核心操作指南

### 初始化数据库

首次使用需初始化：
```python
# 运行 scripts/init_db.py
# 或手动执行 schema.sql
```

### 查询用户画像

```python
profile = query_one("""
    SELECT * FROM user_profile 
    WHERE user_id = ?
""", [user_id])

# 应用到当前会话
if profile:
    if profile['communication_style'] == 'concise':
        set_response_style(brief=True)
    if 'Python' in json.loads(profile['known_domains']):
        assume_knowledge(level='intermediate', domain='Python')
```

### 语义搜索历史

```python
# 使用ChromaDB
results = chroma_collection.query(
    query_texts=["用户之前关于区块链的问题"],
    where={"user_id": user_id},
    n_results=5
)
```

### 检测用户偏好

```python
def detect_preferences(user_message):
    preferences = {}
    
    # 格式偏好
    if "用表格" in user_message or "对比" in user_message:
        preferences['preferred_format'] = 'table'
    elif "简洁" in user_message or "简单说" in user_message:
        preferences['communication_style'] = 'concise'
    
    # 技术背景信号
    if any(word in user_message for word in ["API", "架构", "实现"]):
        preferences['technical_level'] = 'advanced'
    
    # 决策模式
    if any(word in user_message for word in ["数据", "统计", "研究"]):
        preferences['decision_pattern'] = 'data_driven'
    elif any(word in user_message for word in ["感觉", "直觉", "觉得"]):
        preferences['decision_pattern'] = 'intuitive'
    
    return preferences
```

### 评估回答效果

```python
def evaluate_effectiveness(user_message, ai_response, next_user_message):
    """
    通过用户下一轮反应评估本轮回答效果
    """
    # 积极信号
    positive_signals = ['谢谢', '明白了', '好的', '赞', '👍', '完美']
    # 消极信号
    negative_signals = ['不对', '错了', '没懂', '再说', '？', '???']
    
    if any(s in next_user_message for s in positive_signals):
        return 'effective'
    elif any(s in next_user_message for s in negative_signals):
        return 'ineffective'
    elif len(next_user_message) < 5:  # 冷淡回应
        return 'neutral'
    else:
        return 'effective'  # 继续深入对话视为有效
```

### 创建跟进提醒

```python
def create_reminder(user_id, reminder_type, content, trigger_at):
    insert("""
        INSERT INTO pending_reminders (id, user_id, reminder_type, content, trigger_at, status)
        VALUES (?, ?, ?, ?, ?, 'pending')
    """, [generate_id(), user_id, reminder_type, content, trigger_at])
```

## 🧠 六大模块：记忆·学习·总结·反思·创新·智能

### 6️⃣ 智能模块 - 蜂群思维 (Swarm Intelligence)

智能模块是超脑的最高级能力——**真正的分布式智能**。

当收到复杂任务时，主脑会：
1. 分析任务复杂度
2. 拆分为子任务
3. 生成子代理并行执行
4. 所有代理共享超脑数据库
5. 协调编排，井然有序
6. 融合结果，统一输出

#### A. 任务拆分引擎

```python
class TaskDecomposer:
    """任务拆分引擎"""
    
    def analyze_and_decompose(self, user_id, task_description):
        """分析任务并拆分为子任务"""
        
        # 1. 评估任务复杂度
        complexity = self.assess_complexity(task_description)
        required_skills = self.identify_required_skills(task_description)
        
        # 2. 查询超脑：用户相关背景
        user_context = query_super_brain(user_id, task_description)
        
        # 3. 决策：直接执行 vs 拆分执行
        if complexity < COMPLEXITY_THRESHOLD:
            return {'mode': 'direct', 'task': task_description}
        
        # 4. 拆分子任务
        subtasks = self.generate_subtasks(
            task_description,
            required_skills,
            user_context
        )
        
        # 5. 识别子任务依赖关系
        dependency_graph = self.build_dependency_graph(subtasks)
        
        return {
            'mode': 'decompose',
            'subtasks': subtasks,
            'dependencies': dependency_graph,
            'parallel_groups': self.group_parallel_tasks(subtasks, dependency_graph)
        }
    
    def generate_subtasks(self, task, skills, context):
        """生成子任务列表"""
        # 示例：设计AI应用 → 拆分为设计、架构、代码、测试
        subtasks = []
        
        if 'design' in skills or 'ui' in skills:
            subtasks.append({
                'id': generate_id(),
                'type': 'design',
                'description': f'设计{task}的UI/UX方案',
                'required_agent': 'design-agent',
                'estimated_time': '5min',
                'dependencies': []
            })
        
        if 'architecture' in skills or 'backend' in skills:
            subtasks.append({
                'id': generate_id(),
                'type': 'architecture',
                'description': f'设计{task}的技术架构',
                'required_agent': 'architect-agent',
                'estimated_time': '5min',
                'dependencies': []
            })
        
        if 'code' in skills:
            subtasks.append({
                'id': generate_id(),
                'type': 'code',
                'description': f'实现{task}的核心代码',
                'required_agent': 'coder-agent',
                'estimated_time': '10min',
                'dependencies': ['architecture']  # 依赖架构设计
            })
        
        if 'test' in skills:
            subtasks.append({
                'id': generate_id(),
                'type': 'test',
                'description': f'为{task}编写测试用例',
                'required_agent': 'test-agent',
                'estimated_time': '5min',
                'dependencies': ['code']  # 依赖代码实现
            })
        
        return subtasks
```

#### B. 子代理调度器

```python
class AgentOrchestrator:
    """子代理编排器"""
    
    def __init__(self, shared_brain_db):
        self.brain_db = shared_brain_db  # 所有子代理共享同一个超脑
    
    def spawn_agent(self, agent_type, subtask, user_id):
        """生成子代理"""
        
        # 1. 准备子代理上下文（从共享超脑加载）
        context = self.prepare_shared_context(user_id, subtask)
        
        # 2. 调用 sessions_spawn 生成子代理
        agent_session = sessions_spawn({
            'agentId': self.select_best_agent(agent_type),
            'task': subtask['description'],
            'runtime': 'subagent',
            'mode': 'run',
            'attachAs': {
                'mountPath': self.brain_db  # 共享超脑数据库
            }
        })
        
        # 3. 记录子代理到超脑
        self.register_agent(agent_session, subtask, user_id)
        
        return agent_session
    
    def prepare_shared_context(self, user_id, subtask):
        """从共享超脑准备上下文"""
        return {
            'user_profile': query_user_profile(self.brain_db, user_id),
            'related_projects': query_active_projects(self.brain_db, user_id),
            'recent_insights': query_recent_insights(self.brain_db, user_id),
            'effective_patterns': query_effective_patterns(self.brain_db, user_id)
        }
    
    def coordinate_parallel_execution(self, parallel_groups, user_id):
        """协调并行执行"""
        
        all_results = []
        
        for group in parallel_groups:
            # 同一组内的子任务可以并行
            group_agents = []
            
            for subtask in group:
                agent = self.spawn_agent(
                    subtask['required_agent'],
                    subtask,
                    user_id
                )
                group_agents.append(agent)
            
            # 等待这一组完成
            group_results = self.wait_for_completion(group_agents)
            all_results.extend(group_results)
            
            # 更新共享超脑：其他代理可以看到这些结果
            self.update_shared_brain(group_results)
        
        return all_results
```

#### C. 共享大脑机制

```python
class SharedBrain:
    """共享大脑 - 所有子代理的统一记忆"""
    
    def __init__(self, db_path):
        self.db = sqlite3.connect(db_path)
    
    def write_agent_output(self, agent_id, subtask_id, output):
        """子代理写入输出到共享大脑"""
        
        self.db.execute("""
            INSERT INTO agent_outputs 
            (agent_id, subtask_id, output, timestamp)
            VALUES (?, ?, ?, ?)
        """, [agent_id, subtask_id, json.dumps(output), datetime.now()])
        
        self.db.commit()
        
        # 通知其他等待的代理
        self.notify_dependent_agents(subtask_id)
    
    def read_agent_output(self, subtask_id):
        """子代理读取其他代理的输出"""
        
        result = self.db.execute("""
            SELECT output FROM agent_outputs 
            WHERE subtask_id = ?
        """, [subtask_id]).fetchone()
        
        return json.loads(result[0]) if result else None
    
    def get_task_state(self, main_task_id):
        """获取整体任务状态"""
        
        return self.db.execute("""
            SELECT 
                COUNT(*) as total_subtasks,
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
                SUM(CASE WHEN status = 'running' THEN 1 ELSE 0 END) as running,
                SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending
            FROM agent_tasks
            WHERE main_task_id = ?
        """, [main_task_id]).fetchone()
```

#### D. 结果融合器

```python
class ResultMerger:
    """结果融合器"""
    
    def merge_subtask_results(self, subtask_results, main_task):
        """融合多个子代理的结果"""
        
        merged = {
            'main_task': main_task,
            'components': {},
            'integration_points': [],
            'final_output': None
        }
        
        # 1. 分类整理各子任务输出
        for result in subtask_results:
            task_type = result['subtask_type']
            merged['components'][task_type] = result['output']
        
        # 2. 识别集成点
        # 例如：代码需要与架构对齐，测试需要与代码对齐
        merged['integration_points'] = self.find_integration_points(
            merged['components']
        )
        
        # 3. 检查一致性
        inconsistencies = self.check_consistency(merged['components'])
        if inconsistencies:
            merged['warnings'] = inconsistencies
        
        # 4. 生成最终输出
        merged['final_output'] = self.generate_unified_output(merged)
        
        return merged
    
    def generate_unified_output(self, merged):
        """生成统一的最终输出"""
        
        output_parts = []
        
        # 按顺序整合各部分
        if 'architecture' in merged['components']:
            output_parts.append("## 架构设计\n" + merged['components']['architecture'])
        
        if 'design' in merged['components']:
            output_parts.append("## UI/UX设计\n" + merged['components']['design'])
        
        if 'code' in merged['components']:
            output_parts.append("## 核心代码\n" + merged['components']['code'])
        
        if 'test' in merged['components']:
            output_parts.append("## 测试方案\n" + merged['components']['test'])
        
        return "\n\n".join(output_parts)
```

#### E. 协作编排流程

```
完整工作流：

用户任务
    │
    ▼
┌─────────────────────┐
│  主脑分析复杂度      │
│  assess_complexity  │
└──────────┬──────────┘
           │
    ┌──────┴──────┐
    │             │
  简单任务      复杂任务
    │             │
    ▼             ▼
 直接执行    ┌─────────────────────┐
             │  任务拆分引擎        │
             │  decompose_task     │
             └──────────┬──────────┘
                        │
                        ▼
             ┌─────────────────────┐
             │  生成依赖图          │
             │  build_dependency   │
             └──────────┬──────────┘
                        │
           ┌────────────┼────────────┐
           │            │            │
        组1并行       组2并行      组3串行
       (无依赖)     (依赖组1)    (依赖组2)
           │            │            │
           ▼            ▼            ▼
    ┌──────────────────────────────────┐
    │      子代理调度器                  │
    │   spawn_and_coordinate           │
    │                                   │
    │  ┌─────┐ ┌─────┐ ┌─────┐        │
    │  │Agent│ │Agent│ │Agent│        │
    │  │  A  │ │  B  │ │  C  │        │
    │  └──┬──┘ └──┬──┘ └──┬──┘        │
    │     │       │       │            │
    │     └───────┴───────┘            │
    │             │                    │
    │     共享超脑数据库                │
    │   (读写同一个brain.db)           │
    └──────────────┬───────────────────┘
                   │
                   ▼
         ┌─────────────────┐
         │   结果融合器     │
         │  merge_results  │
         └────────┬────────┘
                  │
                  ▼
             统一输出给用户
```

#### F. 数据库扩展

```sql
-- 代理任务表
CREATE TABLE IF NOT EXISTS agent_tasks (
    id TEXT PRIMARY KEY,
    main_task_id TEXT,              -- 主任务ID
    subtask_id TEXT,                -- 子任务ID
    agent_type TEXT,                -- 设计/架构/代码/测试
    status TEXT CHECK(status IN ('pending', 'running', 'completed', 'failed')),
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    result_summary TEXT,
    shared_brain_snapshot TEXT      -- 执行时的超脑快照
);

-- 代理输出表（共享大脑核心）
CREATE TABLE IF NOT EXISTS agent_outputs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id TEXT,
    subtask_id TEXT,
    output TEXT,                    -- JSON格式的输出
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    consumed_by TEXT                -- 被哪个代理读取了
);

-- 代理协作日志
CREATE TABLE IF NOT EXISTS agent_collaboration_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    main_task_id TEXT,
    from_agent TEXT,
    to_agent TEXT,
    action TEXT,                    -- write/read/notify
    data_ref TEXT,                  -- 引用的数据ID
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 💡 智能场景示例

### 场景1：设计完整AI应用

```
用户: 帮我设计一个AI驱动的学习应用

主脑: [分析]
  → 复杂任务，涉及设计、架构、代码、测试
  → 需要多代理协作

主脑: [拆分]
  ├── 子任务A: 设计UI/UX方案 (设计代理)
  ├── 子任务B: 技术架构设计 (架构代理)
  ├── 子任务C: 核心功能代码 (代码代理)
  └── 子任务D: 测试用例编写 (测试代理)

主脑: [并行执行]
  第一波: Agent A + Agent B (无依赖，并行)
  
  Agent A 写入共享大脑:
    - UI设计稿
    - 用户流程图
  
  Agent B 写入共享大脑:
    - 数据库Schema
    - API架构图
  
  第二波: Agent C (依赖A+B的输出)
  
  Agent C 读取共享大脑:
    - 看到UI设计 → 知道要实现什么界面
    - 看到架构图 → 知道技术栈
  
  Agent C 写入共享大脑:
    - 核心代码实现
  
  第三波: Agent D (依赖C的输出)
  
  Agent D 读取共享大脑:
    - 看到代码 → 编写对应测试

主脑: [融合]
  → 整合4个子代理的输出
  → 检查一致性
  → 生成完整方案

主脑: [输出]
  你的AI学习应用完整方案：
  
  ## 架构设计
  [架构代理的输出]
  
  ## UI/UX设计
  [设计代理的输出]
  
  ## 核心代码
  [代码代理的输出]
  
  ## 测试方案
  [测试代理的输出]
  
  所有模块已协调一致，可以直接开始实现！
```

### 场景2：研究复杂问题

```
用户: 分析2024年AI发展趋势，给我一份报告

主脑: [拆分]
  ├── 子任务A: 搜索技术突破 (搜索代理)
  ├── 子任务B: 分析市场数据 (分析代理)
  ├── 子任务C: 研究政策法规 (研究代理)
  └── 子任务D: 整合写报告 (写作代理)

[并行执行A+B+C，然后D融合]

主脑: [输出]
  2024年AI发展趋势报告：
  
  ## 技术突破
  [搜索代理整合]
  
  ## 市场数据
  [分析代理整合]
  
  ## 政策法规
  [研究代理整合]
  
  ## 综合预测
  [写作代理综合分析]
```

## ⚠️ 注意事项

1. **复杂度阈值**: 不是所有任务都需要拆分，简单任务直接执行
2. **代理数量控制**: 同时运行的代理数不超过系统限制
3. **共享大脑同步**: 确保子代理读写共享大脑时的一致性
4. **错误隔离**: 一个子代理失败不应影响其他代理
5. **资源管理**: 监控子代理的执行时间和资源消耗

### 场景1：识别老用户

```
用户: 继续上次的项目

AI: [查询超脑]
    → 发现活跃项目"超脑技能设计"
    → 上次完成：数据库Schema设计
    → 用户偏好：喜欢先讨论再实现
    
AI: 好的，继续超脑技能设计。
    我们上次完成了数据库Schema，
    接下来是Phase 1代码实现。
    你之前提到喜欢先讨论架构，
    我们先过一下实现方案？
```

### 场景2：应用已知偏好

```
用户: 帮我分析一下

AI: [查询超脑]
    → 用户画像：communication_style='concise'
    → 历史模式：用户对长回答会追问"简单说"
    
AI: 好，3点核心结论：
    1. ...
    2. ...
    3. ...
    需要展开哪个？
```

### 场景3：主动服务

```
[会话开始时，超脑检测到]
→ 3天前创建了提醒："跟进超脑实现进度"
→ 当前时间超过trigger_at

AI: 对了，3天前我们在设计超脑技能，
    后来实现了吗？有什么需要帮忙的？
```

## ⚠️ 注意事项

### 隐私与安全

1. **数据本地存储**：超脑数据默认存储在本地 `~/.openclaw/super-brain.db`，不上传云端
2. **敏感信息过滤**：自动检测并过滤密码、身份证号等敏感信息
3. **数据保留期限**：默认90天后自动删除旧数据，可配置
4. **用户完全控制**：用户可随时查看、导出、删除自己的数据
5. **访问透明**：可告知用户"我记得你之前说过..."，但避免过度 creepy

### 使用建议

6. **渐进学习**：不要假设一次对话就能完全了解用户
7. **模式验证**：新发现的偏好需要多次验证再确认
8. **容错处理**：查询失败时优雅降级，不影响正常服务
9. **共享环境**：在公共/共享计算机上使用需谨慎，考虑禁用超脑

## 📚 参考文档

- [schema.sql](references/schema.sql) - 完整数据库Schema
- [workflow.md](references/workflow.md) - 详细工作流程
- [examples.md](references/examples.md) - 使用示例

---

*让每一次对话都成为更好的起点*
