# 🧤 Self-Improver

**OpenClaw 技能 - 自改进智能体系统**

一个为 OpenClaw 设计的持续学习智能体技能，从交互中学习并持续改进性能。

**[🇺🇸 English](README.md)** | **[🇨🇳 中文文档](README-CN.md)**

---

## ✨ 功能特性

- 🧠 **持续学习** - 从每次交互中学习
- 🔄 **自动改进** - 自动应用改进
- 📚 **记忆系统** - 存储和检索学习成果
- 🔌 **钩子系统** - 可扩展的钩子系统
- 📊 **进度追踪** - 追踪改进进度
- 🐍 **Python CLI** - 易用的命令行界面

---

## 🚀 快速开始

### 前置条件

- Python 3.10+
- 已安装 OpenClaw
- pip 或 uv 包管理器

### 安装

```bash
# 克隆仓库
git clone https://github.com/leohuang8688/self-improve-claw.git
cd self-improve-claw

# 使用 pip 安装
pip install -e .

# 或使用 uv 安装
uv pip install -e .
```

### 基本使用

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

---

## 📖 命令

### `run` - 运行智能体

执行带有所有已应用改进的自改进智能体。

```bash
python -m self_improving_agent run --workspace /path/to/workspace
```

### `learn` - 从会话学习

分析上次会话并提取学习成果。

```bash
python -m self_improving_agent learn --verbose
```

### `review` - 回顾学习成果

回顾所有存储的学习成果。

```bash
python -m self_improving_agent review --verbose
```

### `export` - 导出学习成果

将所有学习成果导出到 markdown 文件。

```bash
python -m self_improving_agent export
```

---

## 🏗️ 架构

```
┌─────────────────┐
│  OpenClaw       │
│  智能体          │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ 自改进智能体     │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ↓         ↓
┌──────┐  ┌──────┐
│钩子  │  │记忆  │
└──────┘  └──────┘
```

### 组件

- **Agent** - 主要智能体逻辑
- **Hooks** - 改进钩子
- **Memory** - 学习存储和检索

---

## 📁 项目结构

```
self-improve-claw/
├── main.py              # CLI 入口
├── src/
│   ├── agent.py         # 核心智能体逻辑
│   ├── hooks.py         # 钩子管理器
│   └── memory.py        # 记忆系统
├── hooks/               # 自定义钩子
├── learnings/           # 存储的学习成果
├── scripts/             # 工具脚本
├── tests/               # 测试用例
├── pyproject.toml       # 项目配置
├── README.md            # 英文文档
└── README-CN.md         # 中文文档
```

---

## 🔧 配置

在工作区创建 `.env` 文件：

```bash
# 工作区配置
WORKSPACE_PATH=~/.openclaw/workspace

# 学习配置
LEARNING_ENABLED=true
AUTO_APPLY=true

# 钩子配置
HOOKS_ENABLED=true
```

---

## 📚 学习分类

学习成果分为：

- **skill_improvement** - 技能改进
- **error_prevention** - 错误预防模式
- **optimization** - 性能优化
- **best_practice** - 最佳实践
- **lesson_learned** - 失败教训

---

## 🔌 钩子系统

在 `hooks/` 目录创建自定义钩子：

```python
# hooks/my_hook.py

def apply():
    """应用此钩子的改进。"""
    print("应用我的改进...")
    # 你的改进逻辑在这里
```

---

## 📊 进度追踪

查看你的改进进度：

```bash
# 回顾所有学习成果
self-improve-claw review

# 导出到 markdown
self-improve-claw export > progress.md
```

---

## 🧪 测试

```bash
# 运行测试
pytest

# 运行带覆盖率
pytest --cov=src

# 格式化代码
black src/ tests/

# 检查代码
ruff check src/ tests/
```

---

## 🤝 贡献

1. Fork 仓库
2. 创建功能分支
3. 进行修改
4. 运行测试
5. 提交拉取请求

---

## 📝 许可证

MIT License

---

## 👨‍💻 作者

PocketAI for Leo - OpenClaw Community

---

## 🙏 致谢

- OpenClaw 团队
- 自改进智能体概念
- Python 社区
