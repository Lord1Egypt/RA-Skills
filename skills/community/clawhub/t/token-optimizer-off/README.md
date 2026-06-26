# Token Optimizer

> 🚀 将 AI 对话上下文从 10万+ tokens 压缩至 8,000 以内的完整解决方案

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 核心特性

- **92% Token 节省** - 从 100K+ 压缩到 8K
- **三层索引体系** - 任务层/记忆层/内容层
- **自动压缩** - 智能判断何时需要压缩
- **任务隔离** - 避免上下文污染
- **开箱即用** - 自动使用 OpenClaw AI 配置

## 快速开始

### 安装

**从 ClawHub 安装（推荐）：**

```bash
# 使用 ClawHub 安装
claw install token-optimizer
```

**手动安装：**

```bash
# 克隆到 skills 目录
cd ~/.openclaw/workspace/skills
git clone https://github.com/thanksandyou/token-optimizer.git

# 安装依赖
pip install -r token-optimizer/requirements.txt
```

### 配置

**无需配置！** 🎉

本工具自动使用 OpenClaw 的 AI 配置，开箱即用。

### 使用

```bash
# 1. 检查会话状态
python3 scripts/session_guard.py check --message "用户消息"

# 2. 预览压缩效果（不保存）
python3 scripts/compress_session.py --dry-run

# 3. 压缩会话（实际保存）
python3 scripts/compress_session.py

# 4. 查看状态
python3 scripts/status.py
```

## 工作原理

### Token 来源分析

```
优化前：
  系统提示    ~2,000  （固定）
  会话历史   ~90,000  ← 主要问题
  记忆文件    ~5,000  ← 可优化
  当前消息      ~500  （正常）
  ─────────────────
  总计      ~97,500

优化后：
  系统提示    ~2,000
  latest-summary  ~1,500  ← 替代完整历史
  任务记忆    ~1,000  ← 按需加载
  近5轮对话   ~3,000  ← 滑动窗口
  当前消息      ~500
  ─────────────────
  总计        ~8,000  ✅ 节省 92%
```

### 三层索引体系

**层1：任务层（TaskID）**
```
格式：{类型}-{日期}-{序号}
示例：STOCK-20260227-001 / DEPLOY-20260227-002
```

**层2：记忆层（按需加载）**
```
~/.openclaw/memory/          # OpenClaw 全局记忆目录
├── index/
│   └── INDEX.md            # 必读，<1KB
├── sessions/
│   ├── latest-summary.md   # 最新压缩摘要
│   └── {日期}-summary.md   # 历史归档
└── {domain}/               # 领域专属记忆
    └── {domain}.md
```

**注意：** 记忆文件存储在 `~/.openclaw/memory/`，不在技能目录内。详见 [MEMORY_STRUCTURE.md](MEMORY_STRUCTURE.md)

**层3：内容层（关键词匹配）**
- 匹配度 ≥ 0.8 才纳入上下文
- 自动识别任务类型
- 动态加载相关记忆

## 自动判断机制

| 条件 | 触发动作 |
|------|---------|
| 上下文 < 4万 token | ✅ 正常，无操作 |
| 上下文 4~7万 token | ⚠️ 自动压缩 |
| 上下文 > 7万 token | 🔄 建议新开会话 |
| 会话轮数 > 25 轮 | 🔄 建议新开会话 |

## 脚本说明

| 脚本 | 功能 |
|------|------|
| `session_guard.py` | ⭐ 核心：自动判断是否需要压缩/新开会话 |
| `compress_session.py` | 压缩当前会话摘要 |
| `new_session.py` | 初始化新会话 |
| `status.py` | 显示当前 token 使用情况 |

## 效果对比

| 场景 | 优化前 | 优化后 | 节省 |
|------|--------|--------|------|
| 长会话（50轮） | ~100,000 | ~8,000 | 92% |
| 中等会话（20轮） | ~40,000 | ~6,000 | 85% |
| 新会话 | ~5,000 | ~4,000 | 20% |

## 高级配置（可选）

如果需要自定义配置，可以设置环境变量：

```bash
# 自定义 API Key（覆盖 OpenClaw 配置）
export TOKEN_OPTIMIZER_API_KEY="your-key"

# 自定义模型
export TOKEN_OPTIMIZER_MODEL="gpt-4"

# 自定义 API URL
export TOKEN_OPTIMIZER_API_URL="https://api.openai.com/v1"

# 自定义阈值
export TOKEN_OPTIMIZER_WARN_TOKENS="40000"
export TOKEN_OPTIMIZER_CRITICAL_TOKENS="70000"
export TOKEN_OPTIMIZER_MAX_ROUNDS="25"
```

## 自定义任务类型

编辑 `scripts/session_guard.py`：

```python
DEFAULT_TASK_KEYWORDS = {
    'STOCK':  ['股票','行情','持仓'],
    'DEPLOY': ['部署','安装','服务'],
    'YOUR_TASK': ['关键词1', '关键词2'],  # 添加你的任务类型
}
```

或使用环境变量：

```bash
export TOKEN_OPTIMIZER_TASK_KEYWORDS='{"MYTASK": ["关键词1", "关键词2"]}'
```

## 集成到 Agent

在你的 Agent 代码中：

```python
import subprocess
import json

# 每次对话前检查
result = subprocess.run(
    ['python3', 'scripts/session_guard.py', 'check',
     '--message', user_message,
     '--context-size', str(current_tokens)],
    capture_output=True,
    text=True
)

# 根据结果采取行动
if 'compress' in result.stdout:
    # 执行压缩
    subprocess.run(['python3', 'scripts/compress_session.py'])
elif 'new_session' in result.stdout:
    # 提示用户新开会话
    print("建议新开会话以获得最佳体验")
```

## 故障排查

### 问题 1：找不到 openai 模块

```bash
pip install openai
```

### 问题 2：未找到 AI 配置

确保 OpenClaw 已正确配置：
```bash
cat ~/.openclaw/config.json
```

应包含 `ai` 或 `llm` 配置段。

### 问题 3：压缩失败

检查 OpenClaw AI 配置是否正确：
```bash
# 测试 AI 连接
python3 -c "from compress_session import load_openclaw_config; print(load_openclaw_config())"
```

## 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md)

## 许可证

[MIT License](LICENSE)

## 致谢

- OpenClaw 社区
- 所有贡献者和使用者

## 联系方式

- Issues: [GitHub Issues](https://github.com/thanksandyou/token-optimizer/issues)
- ClawHub: [token-optimizer](https://clawhub.com/skills/token-optimizer)

---

**⭐ 如果这个项目对你有帮助，请给个 Star！**
