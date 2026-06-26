# 🧠 Fluid Memory

> 基于艾宾浩斯遗忘曲线和访问频率的衰减模型设计的遗忘和归档机制，完全依赖 OpenClaw 原生记忆系统的拟人化流体记忆系统

---

## 特性

- **🤝 原生联动**: 依赖 OpenClaw 原生 memory flush 触发
- **🔄 动态遗忘**: 权重低的记忆会被自动淡化
- **⚡ 语义理解**: 基于 ChromaDB 向量检索
- **💪 强化机制**: 被检索次数越多的记忆，越难被遗忘
- **🔌 OpenClaw Ready**: 开箱即用的 OpenClaw Skill

---

## 工作原理

### 架构

```
用户对话 → Hook 记录到临时文件 → OpenClaw 触发 flush → AI 调用 fluid_increment_summarize → 写入向量库
```

### 触发流程

1. **Hook 记录**: 每次 AI 回复时，对话记录到 `conversation_log.txt`
2. **原生 flush**: 当 OpenClaw 上下文快满时，触发 memory flush
3. **AI 响应**: AI 收到提醒，同步调用 `fluid_increment_summarize`
4. **向量存储**: 对话摘要写入 ChromaDB 向量库

---

## 与 OpenClaw 原生系统互补

| 维度 | 原生 Memory | Fluid Memory |
|------|-------------|--------------|
| **存储格式** | 文本 (Markdown) | 向量 (Embedding) |
| **检索方式** | 关键词匹配 | 语义理解 |
| **遗忘机制** | 永不清除 | 动态权重衰减 |

---

## 安装

### 1. 安装 Skill

```bash
clawhub install fluid-memory
```

### 2. 安装 Hook

```bash
cp -r hooks/fluid-memory-sync ~/.openclaw/hooks/
```

### 3. 配置 OpenClaw

在 `openclaw.json` 中启用 Hook 和调整触发频率：

```json5
{
  "hooks": {
    "internal": {
      "entries": {
        "fluid-memory-sync": { "enabled": true }
      }
    }
  },
  "agents": {
    "defaults": {
      "compaction": {
        "memoryFlush": {
          "enabled": true,
          "softThresholdTokens": 50000
        }
      }
    }
  }
}
```

### 触发时机

> 触发 = contextWindow - reserveTokensFloor (20000) - softThresholdTokens

例如 Minimax 195K：195K - 20K - 50K = 125K（约 64% 满时触发）

---

## 使用

### 手动记录

```bash
python fluid_skill.py remember --content "用户喜欢喝可乐"
python fluid_skill.py recall --query "用户喝什么"
python fluid_skill.py forget --content "青椒肉丝"
python fluid_skill.py status
```

---

## 遗忘机制

### 1. 动态遗忘（检索时过滤）

```
Score = (相似度 × e^(-λt)) + α × log(1+N)
```

- λ = 遗忘速度 (0.05)
- t = 距离上次访问的天数
- α = 强化力度 (0.2)
- N = 被访问次数

分数 < 0.05 的记忆不返回。

### 2. 主动遗忘

调用 `forget` 命令归档记忆。

### 3. 梦境守护

运行 `maintenance.py`，归档超过 120 天的低权重记忆。

---

## 文件结构

```
fluid-memory/
├── SKILL.md                    # OpenClaw Skill 定义
├── fluid_skill.py              # 核心引擎
├── maintenance.py              # 梦境整理脚本
├── dream_daemon.py            # 定时守护进程
├── wrapper.py                 # CLI 封装
├── config.yaml                # 配置文件
├── LICENSE                    # MIT 许可证
├── README.md                  # 本文件
└── hooks/
    └── fluid-memory-sync/     # 自动同步 Hook
        ├── HOOK.md
        └── handler.js
```

---

## ⚠️ 隐私声明

- **存储位置**: 所有数据存储在本地 `~/.openclaw/workspace/database/`
- **存储格式**: 明文存储（无加密）
- **文件列表**:
  - `chroma_store/` - 向量数据库
  - `conversation_log.txt` - 对话缓存
  - `summary_buffer.json` - 摘要缓存

**风险**: 如果多人共用一台电脑，建议加密磁盘或定期清理。数据无云端同步，安全性取决于本地系统。

---

## 许可证

MIT License
