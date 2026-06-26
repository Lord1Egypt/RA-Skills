# 🤖 极简万能 Agent (Minimal Universal Agent)

> **作者：王教成（波动几何）** | **LLM（大脑）+ 命令执行器（手脚） = 万能通用AI Agent**

## 核心理念

```
用户自然语言输入
       ↓
  ┌─────────┐
  │   LLM   │ ← 理解意图，生成命令/脚本代码
  │  (大脑)  │
  └────┬────┘
       │ 自动生成
       ↓
  ┌─────────────┐
  │execute_     │ ← 执行任何命令，控制所有软件和硬件
  │command(手脚)│
  └──────┬──────┘
         │ 实际执行
         ↓
    任务完成 ✅
```

## 为什么这是"万能"的？

| 能力层 | 说明 |
|--------|------|
| **Shell命令** | 操作文件、管理进程、系统运维 |
| **Python脚本** | 数据处理、网络爬虫、机器学习 |
| **调用任何CLI** | git, docker, ffmpeg, aws... |
| **控制硬件** | 通过软件间接控制：屏幕、音频、串口... |
| **网络连接** | API调用、SSH远程、IoT设备 |

**execute_command 能运行 Python 脚本 → Python 能做任何事 → Agent 就能做任何事**

## 快速开始

### 🏔️ 模式一：独立运行（需要 API Key）

脚本自力更生，自己调用 LLM API + 自己执行命令。

```bash
# 交互式启动（推荐）
python scripts/universal_agent.py

# 单次任务
python scripts/universal_agent.py --run "列出当前目录的所有文件"

# 使用环境变量
set LLM_API_KEY=sk-xxx
python scripts/universal_agent.py --run "分析数据"
```

### 🌉 模式二：桥接执行（不需要 API Key，推荐用于 Skill 集成）

脚本由外部 Agent 驱动。外部 Agent 提供"大脑"（LLM能力），脚本负责"手脚"（执行+安全+重试+记忆）。任何有 LLM + 命令执行能力的工具都可使用：WorkBuddy、Cursor、Continue.dev、Aider、Cline 等。

```bash
# 查看完整协议说明
python scripts/universal_agent.py --bridge-info

# 桥接模式执行任务
set UA_THINK={"type":"command","content":"dir /b","explanation":""}
python scripts/universal_agent.py --backend bridge --run "列出当前目录的文件"

# 作为模块导入使用
from universal_agent import UniversalAgent, AgentBridge

bridge = AgentBridge()
bridge.set_response('think', '{"type":"command","content":"dir /b"}')
bridge.set_response('summarize', '已完成：列出了当前目录的15个文件')

agent = UniversalAgent(api_key="bridge", backend="bridge")
agent.run("列出当前目录的文件")
```

**通信方式（环境变量）：**

| 环境变量 | 用途 | 格式 |
|----------|------|------|
| `UA_THINK` | 任务决策结果 | `{"type":"command\|script","content":"...","explanation":"..."}` |
| `UA_GENERATE_SCRIPT` | 生成的 Python 脚本 | 完整代码 |
| `UA_SUMMARIZE` | 执行结果总结 | 自然语言文本 |
| `UA_DEBUG_AND_FIX` | 修复后的代码 | 修复后代码 |

### 📖 模式三：Skill 模拟（不需要运行脚本）

加载此 Skill 的 Agent 阅读 SKILL.md 后，用自身能力模拟整个工作流程。无需配置，但不会启用脚本内置的安全/重试/记忆功能。

### 方式四：作为模块导入（独立模式）

```python
from universal_agent import UniversalAgent

agent = UniversalAgent(
    api_key="your-key",
    model="gpt-4o",
    base_url="https://api.openai.com/v1"
)

# 单次执行
agent.run("帮我把当前目录的文件按类型整理")

# 交互模式
agent.chat()
```

### 方式四：使用环境变量（适合服务器）

```bash
export LLM_API_KEY="sk-xxx"
export LLM_MODEL="gpt-4o"
export LLM_BASE_URL="https://api.openai.com/v1"

python universal_agent.py --run "分析数据"
```

## 支持的LLM提供商

| 提供商 | 模型 | base_url |
|--------|------|----------|
| OpenAI | gpt-4o, gpt-4o-mini | https://api.openai.com/v1 |
| DeepSeek | deepseek-chat, deepseek-reasoner | https://api.deepseek.com |
| 通义千问 | qwen-max, qwen-turbo | https://dashscope.aliyuncs.com/compatible-mode/v1 |
| 智谱GLM | glm-4-plus | https://open.bigmodel.cn/api/paas/v4 |
| 本地Ollama | llama3, qwen2, any-model | http://localhost:11434/v1 |
| Groq | llama-3.1-70b-versatile | https://api.groq.com/openai/v1 |
| 其他 | 任何OpenAI兼容API | - |

## 使用示例

### 简单任务（自动生成shell命令）

```
你: 列出当前目录的文件
Agent: $ dir /b
      (显示结果)
✅ 已完成：当前目录包含15个文件和3个文件夹...
```

### 复杂任务（自动生成Python脚本）

```
你: 分析sales.csv的销售趋势并生成图表
Agent: (自动生成并执行约50行Python代码)
      - 导入pandas、matplotlib
      - 读取CSV数据
      - 计算统计指标
      - 绑制趋势图
      - 保存为图片
✅ 任务完成！已生成销售趋势图 trend.png...
```

### 开发任务

```
你: 写一个快速排序算法并测试性能
Agent: (生成完整Python脚本)
      ✅ 快速排序实现完成
      - 随机数组10000个元素: 排序耗时0.012秒
      - 与内置sorted对比验证: 结果一致
```

### 系统运维

```
你: 检查哪些端口被占用
Agent: $ netstat -ano | findstr LISTENING
      (展示端口占用情况)
✅ 已发现5个活跃端口...
```

## 项目结构

```
scripts/
├── universal_agent.py        # 主程序（单文件，约900行）
├── config.json               # 配置文件（填入API Key即可使用）
references/
└── README.md                 # 本文档
```

## 功能特性

### ✅ 全流程自动化
- 用户只需说一句话
- 自动理解 → 规划 → 生成代码 → 执行 → 总结
- 无需人工干预

### 🔒 安全机制
- 高危命令检测（rm -rf /, format C:, etc.）
- 危险操作强制确认
- 中危操作警告提示
- 可选的危险模式（跳过确认）

### 🧠 智能决策
- 自动判断任务复杂度
- 简单任务 → 生成shell命令
- 复杂任务 → 生成Python脚本
- 多步任务 → 生成命令序列

### 🔄 自我修复
- 执行出错时自动分析原因
- LLM修复代码后重新执行
- 默认最多重试2次

### 💾 持久记忆
- 跨会话保留执行历史
- 存储学到的知识
- 变量持久化存储
- 下次启动自动加载

### 🌐 跨平台支持
- Windows (cmd.exe)
- macOS (bash/zsh)
- Linux (bash)

### 📊 执行历史
- 实时查看最近执行记录
- 包含成功/失败状态
- 显示耗时信息

## 依赖要求

**零外部依赖**（使用标准库）：
- `os`, `sys` — 系统操作
- `subprocess` — 命令执行
- `json` — JSON解析
- `re` — 正则表达式
- `time/datetime` — 时间处理
- `urllib` — HTTP请求（备选）

**可选依赖**：
- `requests` — 更好的HTTP支持（推荐安装）
  ```bash
  pip install requests
  ```

## 免费方案推荐

### 1️⃣ Ollama + 本地模型（完全免费）

```bash
# 安装 Ollama
# Windows: https://ollama.ai/download
# Mac: brew install ollama
# Linux: curl -fsSL https://ollama.ai/install.sh | sh

# 运行本地模型
ollama run llama3    # 推荐，7B参数
# 或
ollama run qwen2     # 通义千问2代
ollama run codellama # 代码专用

# 启动Agent时选择 Ollama 配置即可
```

**优点**: 免费、无限用、隐私安全
**缺点**: 需要较好的电脑配置（建议8GB+显存）

### 2️⃣ DeepSeek（性价比极高）

- 注册: https://platform.deepseek.com
- 价格: 约 ¥1/百万token
- 性能: 接近GPT-4水平

### 3️⃣ Groq Cloud（有免费额度）

- 注册: https://console.groq.com
- 特点: 超快推理速度
- 免费额度: 每月一定量免费API调用

## 配置说明

### config.json 格式

```json
{
  "api_key": "sk-your-api-key",
  "model": "gpt-4o",
  "base_url": "https://api.openai.com/v1",
  "dangerous_mode": false,
  "auto_save_memory": true,
  "memory_file": "universal_agent_memory.json",
  "command_timeout": 300,
  "script_timeout": 600
}
```

### 环境变量

```bash
export LLM_API_KEY="sk-xxx"
export LLM_MODEL="gpt-4o"
export LLM_BASE_URL="https://api.openai.com/v1"
```

## 交互命令

在交互模式中可使用以下特殊命令：

| 命令 | 功能 |
|------|------|
| `help` | 显示帮助 |
| `history` | 查看执行历史 |
| `context` | 查看上下文 |
| `stats` | 统计信息 |
| `clear` | 清理临时文件 |
| `var X Y` | 设置变量 |
| `remember X` | 记住信息 |
| `exit` | 退出 |

## 安全注意事项

⚠️ **重要提醒**

1. 不要在公共环境开启危险模式
2. 定期清理临时生成的脚本文件 (`_agent_task_*.py`)
3. 敏感信息不要放在任务描述中
4. API Key 要妥善保管，不要提交到Git
5. 对于删除操作，务必仔细检查

## 技术架构

```
universal_agent.py (~1000+ 行)
│
├── class AgentBridge        (外部Agent桥接接口 — Mode 2)
│   ├── think()             # 从外部Agent接收决策结果
│   ├── generate_script()   # 接收生成的Python脚本
│   ├── summarize()         # 接收总结文本
│   ├── debug_and_fix()     # 接收修复后代码
│   └── set_response()      # 程序化设置响应内容
│
├── class LLMBrain          (大语言模型HTTP接口 — Mode 1)
│   ├── think()             # 核心：理解意图，生成命令/脚本
│   ├── generate_script()   # 专门生成Python脚本
│   ├── summarize()         # 将结果翻译成人类语言
│   └── debug_and_fix()     # 出错时自我修复
│
├── class UniversalExecutor  (通用命令执行器 — 所有模式共用)
│   ├── execute()           # 主入口：执行命令或脚本
│   ├── _execute_command()  # Shell命令执行
│   ├── _execute_script()   # Python脚本执行
│   └── _check_danger()     # 危险等级检查
│
├── class ContextManager     (上下文/记忆管理 — 所有模式共用)
│   ├── add_task_record()   # 记录任务
│   ├── get_context_string()# 供LLM/Agent使用的上下文
│   ├── save() / load()     # 持久化
│   └── get_stats()         # 统计信息
│
└── class UniversalAgent     (主类，组合以上三者)
    ├── run()               # 单次任务（全流程自动化）
    ├── chat()              # 交互模式
    ├── batch_run()         # 批量任务
    └── backend="llm|bridge" # 后端选择
```

## License

MIT License - 自由使用、修改、分发

---

**Made with ❤️ by 极简万能 Agent**
