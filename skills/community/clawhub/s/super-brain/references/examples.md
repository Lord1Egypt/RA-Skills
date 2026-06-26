# AI超脑 - 使用示例

## 示例1：新用户首次对话

**用户:** 你好，帮我写个Python脚本

**AI内部流程:**
```python
# 1. 检查用户画像
profile = query("SELECT * FROM user_profile WHERE user_id = ?", [user_id])
# 结果: None (新用户)

# 2. 创建画像
create_profile(user_id)

# 3. 开始对话（无历史偏好）
# ... 提供Python帮助 ...

# 4. 对话中检测偏好
# 用户说: "给我完整代码" → technical_level='intermediate'
# 用户说: "简单点说" → communication_style='concise'

# 5. 会话结束存储洞察
insert_insight(
    user_id=user_id,
    topic="Python脚本编写",
    key_facts={"需求": "自动化脚本", "语言": "Python"},
    preferences_detected={"communication_style": "concise"}
)
```

**AI回复:**
> 你好！我来帮你写Python脚本。
> 需要什么功能的脚本？数据处理、自动化任务还是其他？

---

## 示例2：老用户继续项目

**用户:** 继续上次的项目

**AI内部流程:**
```python
# 1. 加载画像
profile = query("SELECT * FROM user_profile WHERE user_id = ?", [user_id])
# 结果: 存在，communication_style='concise', known_domains=["Python", "数据库"]

# 2. 检查项目
projects = query("SELECT * FROM user_projects WHERE user_id = ? AND status = 'active'", [user_id])
# 结果: project_name='超脑技能设计', current_phase='数据库Schema'

# 3. 检查提醒
reminders = query("SELECT * FROM pending_reminders WHERE user_id = ? AND status = 'pending'", [user_id])
# 结果: content='跟进超脑实现进度', trigger_at='3天前'

# 4. 应用偏好
set_response_style(brief=True)  # 因为用户喜欢简洁

# 5. 构建上下文回复
```

**AI回复:**
> 好，继续**超脑技能设计**项目。
>
> 我们上次完成了数据库Schema，接下来是Phase 1实现。
>
> 对了，3天前你说要实现，后来进展如何？
> 需要我从初始化脚本开始吗？

---

## 示例3：学习用户偏好

**对话1:**
- AI: [长段回答]
- 用户: "简单说"
- AI: [检测到偏好变化，存储 communication_style='concise']

**对话2:**
- AI: [简洁回答]
- 用户: "明白了，谢谢！"
- AI: [检测到积极反馈，确认偏好有效]

**对话3:**
- AI: [自动使用简洁风格]
- 用户: [正常继续，无纠正]
- AI: [偏好已稳定，存入 confirmed_preferences]

---

## 示例4：主动服务

**场景:** 用户3天前说要完成一个任务

**AI检测:**
```python
# 会话开始时
reminder = query("""
    SELECT * FROM pending_reminders 
    WHERE user_id = ? 
    AND reminder_type = 'follow_up'
    AND trigger_at < now()
    AND status = 'pending'
""")

if reminder:
    raise_reminder(reminder.content)
    update_reminder_status(reminder.id, 'sent')
```

**AI主动说:**
> 对了，3天前你说要完成XX，后来做了吗？
> 有什么需要帮忙的？

---

## 示例5：项目追踪

**用户:** 我想做个新APP

**AI流程:**
```python
# 创建项目
create_project(
    user_id=user_id,
    project_name="新APP",
    description="用户想做的APP",
    status="planning",
    milestones=[
        {"name": "需求分析", "done": False},
        {"name": "原型设计", "done": False},
        {"name": "开发", "done": False}
    ]
)

# 后续对话中更新
update_project_milestone(project_id, "需求分析", done=True)
add_project_decision(project_id, "选择React Native跨平台")
```

---

## 示例6：反思与改进

**失败场景:**
- AI: [详细技术解释]
- 用户: "我听不懂，说人话"
- AI: 
```python
# 存储无效模式
insert_pattern(
    pattern_type='ineffective',
    trigger_context='技术问题',
    what_i_did='详细技术解释',
    user_reaction='纠正',
    learned_lesson='先确认用户技术水平',
    alternative_approach='先用通俗比喻，再深入'
)

# 更新画像
update_profile(user_id, {'technical_level': 'beginner'})
```

**下次:**
- AI: [先用通俗语言解释，确认理解后再深入]
- 用户: "明白了！"
- AI: [模式有效，success_count + 1]

---

## 示例7：跨会话记忆

**上周:**
- 用户: "我在学Rust"
- AI: [存储 learning_goals=["Rust"]]

**这周:**
- 用户: "帮我看个代码"
- AI: 
```python
profile = load_profile(user_id)
if "Rust" in profile['learning_goals']:
    # 默认提供Rust示例
    response = generate_response(language_hint='Rust')
```

**AI回复:**
> 好，这个逻辑用Rust可以这样写...
> （我知道你最近在学Rust）
