# 🧠 Self-Improving Agent - 完整使用指南

**持续学习和自动改进的终极指南**

**[🇺🇸 English Guide](USAGE.md)** | **[🇨🇳 中文指南](USAGE-CN.md)**

---

## 📖 目录

1. [简介](#简介)
2. [工作原理](#工作原理)
3. [安装](#安装)
4. [基本使用](#基本使用)
5. [高级使用](#高级使用)
6. [配置](#配置)
7. [学习分类](#学习分类)
8. [钩子系统](#钩子系统)
9. [记忆系统](#记忆系统)
10. [实际示例](#实际示例)
11. [故障排除](#故障排除)
12. [常见问题](#常见问题)

---

## 🎯 简介

**Self-Improving Agent** 是一个为 OpenClaw 设计的持续学习系统，从每次交互中学习并自动改进性能。

### 核心特性

- 🧠 **持续学习** - 从每次交互中学习
- 🔄 **自动改进** - 自动应用改进
- 📚 **记忆系统** - 存储和检索学习成果
- 🔌 **钩子系统** - 可扩展的钩子系统
- 📊 **进度追踪** - 追踪改进进度
- ⚡ **完全自动化** - 与 OpenClaw 自动协作

### 优势

- ✅ **越来越聪明** - 每次使用都在改进
- ✅ **无需手动配置** - 完全自动化
- ✅ **透明可见** - 所有学习成果可见可审查
- ✅ **可定制** - 创建自定义钩子和分类
- ✅ **可分享** - 导出并与团队分享学习成果

---

## 🔧 工作原理

### 架构概览

```
┌─────────────────────────────────────┐
│      OpenClaw 智能体会话             │
│         (用户交互)                  │
└──────────────┬──────────────────────┘
               │
               ↓ 会话结束
┌─────────────────────────────────────┐
│     Self-Improving Agent            │
│  ┌─────────────┐  ┌──────────────┐  │
│  │   提取      │→ │   分析       │  │
│  │  学习成果   │  │   模式       │  │
│  └─────────────┘  └──────────────┘  │
└──────────────┬──────────────────────┘
               │
               ↓ 学习成果
┌─────────────────────────────────────┐
│        记忆系统                      │
│  ┌─────────────┐  ┌──────────────┐  │
│  │   存储      │→ │   检索       │  │
│  │  学习成果   │  │  学习成果    │  │
│  └─────────────┘  └──────────────┘  │
└──────────────┬──────────────────────┘
               │
               ↓ 应用改进
┌─────────────────────────────────────┐
│         钩子系统                     │
│  ┌─────────────┐  ┌──────────────┐  │
│  │   应用      │→ │   改进       │  │
│  │   钩子      │  │   性能       │  │
│  └─────────────┘  └──────────────┘  │
└─────────────────────────────────────┘
```

### 工作流程

#### **阶段 1: 运行会话**
```bash
python -m self_improving_agent run
```

**发生了什么：**
1. 加载之前存储的学习成果
2. 应用所有改进钩子
3. 以改进后的状态运行 OpenClaw Agent
4. 记录新的交互数据

#### **阶段 2: 学习与提取**
```bash
python -m self_improving_agent learn
```

**发生了什么：**
1. **分析会话日志**
   - 读取 OpenClaw 会话记录
   - 识别成功和失败模式

2. **提取学习成果**
   ```json
   {
       "title": "避免重复搜索",
       "category": "optimization",
       "content": "查询相似问题前先检查缓存",
       "trigger": "用户连续提问",
       "action": "先检查缓存"
   }
   ```

3. **存储到记忆系统**
   - 保存到 `learnings/active_learnings.json`
   - 生成唯一 ID 和时间戳

#### **阶段 3: 回顾学习成果**
```bash
python -m self_improving_agent review --verbose
```

**输出示例：**
```
📖 Reviewing learnings...

1. 避免重复搜索
   Category: optimization
   Date: 2026-03-14T10:30:00
   Content: 查询相似问题前先检查缓存

2. 错误预防模式
   Category: error_prevention
   Date: 2026-03-14T09:15:00
   Content: 调用外部 API 前先检查网络连接

✅ Total: 2 learnings
```

#### **阶段 4: 导出学习成果**
```bash
python -m self_improving_agent export
```

**生成文件：** `learnings_export.md`

```markdown
# Self-Improving Agent - Learnings Export

Exported: 2026-03-14T11:00:00
Total Learnings: 2

---

## 1. 避免重复搜索

**Category:** optimization

**Date:** 2026-03-14T10:30:00

**Content:**
查询相似问题前先检查缓存

---
```

---

## 🚀 安装

### 前置条件

- Python 3.10+
- 已安装 OpenClaw
- pip 或 uv 包管理器

### 步骤 1: 克隆仓库

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/leohuang8688/self-improving-agent.git
cd self-improving-agent
```

### 步骤 2: 安装依赖

```bash
# 使用 pip
pip install -e .

# 使用 uv
uv pip install -e .
```

### 步骤 3: 在 OpenClaw 中启用

添加到 OpenClaw 配置文件：

```json
{
  "skills": {
    "self-improving-agent": {
      "enabled": true,
      "auto_learn": true,
      "auto_apply": true
    }
  }
}
```

### 步骤 4: 重启 OpenClaw

```bash
openclaw gateway restart
```

---

## 💻 基本使用

### 快速开始

```bash
# 运行自改进智能体
python -m self_improving_agent run

# 从上次会话学习
python -m self_improving_agent learn

# 查看所有学习成果
python -m self_improving_agent review

# 导出学习成果到文件
python -m self_improving_agent export
```

### 命令参考

#### `run` - 运行智能体

执行带有所有已应用改进的自改进智能体。

```bash
python -m self_improving_agent run --workspace /path/to/workspace
```

**选项：**
- `--workspace` - OpenClaw 工作区路径（默认：`~/.openclaw/workspace`）
- `--verbose` - 启用详细输出

#### `learn` - 从会话学习

分析上次会话并提取学习成果。

```bash
python -m self_improving_agent learn --verbose
```

**选项：**
- `--verbose` - 显示详细分析
- `--session` - 指定要分析的会话文件

#### `review` - 回顾学习成果

回顾所有存储的学习成果。

```bash
python -m self_improving_agent review --verbose
```

**选项：**
- `--verbose` - 显示每个学习成果的完整内容
- `--category` - 按分类筛选（如 `optimization`）
- `--limit` - 限制结果数量（如 `--limit 10`）

#### `export` - 导出学习成果

将所有学习成果导出到 markdown 文件。

```bash
python -m self_improving_agent export
```

**选项：**
- `--output` - 输出文件路径（默认：`learnings_export.md`）
- `--format` - 导出格式（`markdown` 或 `json`）

---

## ⚙️ 高级使用

### 自动化工作流

设置自动学习和应用：

```json
{
  "skills": {
    "self-improving-agent": {
      "enabled": true,
      "auto_learn": true,
      "auto_apply": true,
      "learn_after_session": true,
      "apply_on_startup": true,
      "review_frequency": "weekly"
    }
  }
}
```

### 自定义钩子

在 `hooks/` 目录创建自定义钩子：

```python
# hooks/cache_hook.py
"""
缓存优化钩子
"""

def apply():
    """应用缓存优化"""
    print("📦 应用缓存优化钩子...")
    
    # 启用结果缓存
    enable_cache(ttl=300)  # 5 分钟缓存
    
    print("✅ 缓存优化已应用")
```

### 自定义分类

添加自定义学习分类：

```python
# 在学习提取代码中
learning = {
    "type": "custom_category",
    "title": "我的自定义学习",
    "content": "学习成果描述"
}
```

---

## 🔧 配置

### 环境变量

在工作区创建 `.env` 文件：

```bash
# 工作区配置
WORKSPACE_PATH=~/.openclaw/workspace

# 学习配置
LEARNING_ENABLED=true
AUTO_APPLY=true

# 钩子配置
HOOKS_ENABLED=true

# 记忆配置
MEMORY_PATH=~/.openclaw/workspace/self-improving-agent/learnings
MAX_LEARNINGS=1000
ARCHIVE_AFTER_DAYS=30
```

### 配置文件

在工作区创建 `config.json`：

```json
{
  "learning": {
    "enabled": true,
    "auto_apply": true,
    "min_confidence": 0.7
  },
  "memory": {
    "max_learnings": 1000,
    "archive_after_days": 30,
    "export_format": "markdown"
  },
  "hooks": {
    "enabled": true,
    "auto_load": true,
    "custom_hooks_path": "./hooks"
  }
}
```

---

## 📚 学习分类

### 内置分类

#### 1. **skill_improvement（技能改进）**
特定技能或能力的改进。

```json
{
    "type": "skill_improvement",
    "title": "改进股票分析",
    "content": "使用 5 日、20 日、60 日均线进行技术分析"
}
```

#### 2. **error_prevention（错误预防）**
预防常见错误的模式。

```json
{
    "type": "error_prevention",
    "title": "API 调用检查",
    "content": "调用外部 API 前先检查网络连接和 API Key"
}
```

#### 3. **optimization（性能优化）**
性能优化。

```json
{
    "type": "optimization",
    "title": "缓存策略",
    "content": "对于相同查询，缓存结果 5 分钟"
}
```

#### 4. **best_practice（最佳实践）**
最佳实践和指南。

```json
{
    "type": "best_practice",
    "title": "错误处理",
    "content": "所有外部调用都使用 try-except 包裹"
}
```

#### 5. **lesson_learned（失败教训）**
从失败或错误中吸取的教训。

```json
{
    "type": "lesson_learned",
    "title": "Git 推送失败",
    "content": "推送前先拉取最新代码，避免冲突"
}
```

---

## 🔌 钩子系统

### 钩子是什么？

钩子是自动应用学习成果作为改进的机制。

### 钩子如何工作

```python
# 当智能体运行时
agent.run()
  ↓
hooks.apply_all()  # 应用所有钩子
  ↓
# 所有学习到的改进自动生效
```

### 创建自定义钩子

**示例：** `hooks/cache_hook.py`

```python
"""
缓存优化钩子
"""

def apply():
    """应用缓存优化"""
    print("📦 应用缓存优化钩子...")
    
    # 启用结果缓存
    enable_cache(ttl=300)  # 5 分钟缓存
    
    print("✅ 缓存优化已应用")
```

**示例：** `hooks/error_prevention_hook.py`

```python
"""
错误预防钩子
"""

def apply():
    """应用错误预防改进"""
    print("🛡️  应用错误预防钩子...")
    
    # 启用网络检查
    enable_network_check()
    
    # 启用 API 验证
    enable_api_validation()
    
    print("✅ 错误预防已应用")
```

---

## 💾 记忆系统

### 存储位置

```
~/.openclaw/workspace/self-improving-agent/learnings/
├── active_learnings.json    # 当前活跃学习
├── archive.json             # 归档学习
└── learnings_export.md      # 导出的文档
```

### active_learnings.json 结构

```json
[
    {
        "id": "a1b2c3d4",
        "type": "optimization",
        "title": "缓存优化",
        "content": "对于相同查询，缓存结果 5 分钟",
        "date": "2026-03-14T10:30:00",
        "applied": true
    }
]
```

### 记忆生命周期

1. **新学习** → 存储在 `active_learnings.json`
2. **30 天后** → 移动到 `archive.json`
3. **导出时** → 生成为 `learnings_export.md`

---

## 🌟 实际示例

### 示例 1: 日常使用

```bash
# 早上：开始工作
python -m self_improving_agent run

# 一天结束：从今天学习
python -m self_improving_agent learn

# 周末：回顾学习成果
python -m self_improving_agent review --verbose
```

### 示例 2: 性能调优

```bash
# 运行性能分析
python -m self_improving_agent run --verbose

# 分析瓶颈
python -m self_improving_agent learn

# 应用优化
python -m self_improving_agent run  # 自动应用优化钩子
```

### 示例 3: 团队协作

```bash
# 导出学习成果
python -m self_improving_agent export

# 分享给团队
cat learnings_export.md | mail team@company.com
```

---

## 🐛 故障排除

### 没有找到学习成果

**问题：** `No learnings extracted`

**解决方案：**
1. 确保配置中启用了学习
2. 检查是否发生了交互
3. 验证工作区路径正确
4. 检查会话日志是否存在

### 导入错误

**问题：** `ModuleNotFoundError: No module named 'self_improving_agent'`

**解决方案：**
1. 安装包：`pip install -e .`
2. 检查 Python 版本：需要 Python 3.10+
3. 验证安装：`python -m self_improving_agent --help`

### 钩子未应用

**问题：** `Hooks not being applied`

**解决方案：**
1. 检查 `hooks/` 目录是否存在
2. 验证钩子有 `apply()` 函数
3. 检查钩子中的 Python 语法错误
4. 在配置中启用钩子

### 记忆系统问题

**问题：** `Memory system not working`

**解决方案：**
1. 检查 `learnings/` 目录是否存在
2. 验证写入权限
3. 检查磁盘空间
4. 检查记忆配置

---

## ❓ 常见问题

### Q: 应该多久运行一次 learn？

**A:** 推荐频率：
- **每天：** 重度使用
- **每周：** 中度使用
- **每月：** 轻度使用

### Q: 可以不用 OpenClaw 使用这个吗？

**A:** 可以！虽然是为 OpenClaw 设计的，但你可以通过提供自己的会话日志将其作为独立学习系统使用。

### Q: 可以存储多少学习成果？

**A:** 默认限制是 1000 个活跃学习成果。你可以在 `config.json` 中配置。

### Q: 可以和团队分享学习成果吗？

**A:** 可以！使用 `export` 命令生成可分享的 markdown 或 JSON 文件。

### Q: 学习成果是持久的吗？

**A:** 是的！学习成果存储在 JSON 文件中，在会话之间持久保存。

### Q: 可以删除特定的学习成果吗？

**A:** 可以！手动编辑 `active_learnings.json` 或使用 `review` 命令的删除选项（即将推出）。

### Q: 如何备份学习成果？

**A:** 备份整个 `learnings/` 目录：

```bash
cp -r ~/.openclaw/workspace/self-improving-agent/learnings/ /backup/location/
```

---

## 📝 许可证

MIT License

---

## 👨‍💻 作者

PocketAI for Leo - OpenClaw Community

---

## 🙏 致谢

- OpenClaw Team
- Self-Improving Agent Concept
- Python Community

---

**快乐学习！🚀**
