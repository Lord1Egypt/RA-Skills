# SoulForge 中文文档

**SoulForge** — AI 智能体记忆进化系统。自动分析记忆文件，发现反复出现的模式，并将结果写入智能体的工作区身份文件（SOUL.md、USER.md、IDENTITY.md 等）。

SoulForge 利用你已有的 MiniMax API 进行模式检测和内容生成，让你的 AI 智能体越用越聪明。

---

## 核心特性

- **🧠 自动记忆分析** — 读取 `memory/*.md` 每日日志、hawk-bridge 向量库、`.learnings/` 记录
- **⚡ MiniMax 驱动** — 使用已有的 MiniMax API 进行模式检测
- **📝 多文件进化** — 自动更新 SOUL.md、USER.md、IDENTITY.md、MEMORY.md、AGENTS.md、TOOLS.md
- **🔒 安全设计** — 增量更新，写前备份，来源追踪
- **⏰ 定时或手动** — 支持 cron 调度或手动触发
- **🌍 中英双语** — 完整的英文和中文文档

---

## 工作原理

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  记忆源     │ ──▶ │   分析器      │ ──▶ │  进化器     │
│  Memory     │     │  (MiniMax)   │     │  (写入器)   │
└─────────────┘     └──────────────┘     └─────────────┘
     │                    │                    │
     ▼                    ▼                    ▼
memory/*.md         模式检测              SOUL.md
hawk-bridge         反复规则              USER.md
.learnings/         决策挖掘              IDENTITY.md
                                          MEMORY.md
```

**触发条件**（何时更新）：
- 同一行为模式出现 3 次以上
- 用户在同一主题上纠正智能体 2 次以上
- 发现新的偏好或决策
- 项目里程碑达成

---

## 快速开始

### 1. 安装

```bash
# 通过 clawhub（推荐）
clawhub install soul-evolver

# 或手动克隆
git clone https://github.com/relunctance/soul-evolver.git ~/.openclaw/skills/soul-evolver
```

### 2. 配置 API Key

SoulForge 使用 MiniMax API 进行模式分析。需要设置环境变量：

```bash
export MINIMAX_API_KEY="your-minimax-api-key"
```

**OpenClaw 用户注意：** 如果通过 OpenClaw cron 运行，API Key 由 OpenClaw 自动注入。独立 CLI 使用时需手动设置环境变量。

### 3. 运行

```bash
# 手动触发
python3 scripts/soulforge.py run

# 指定工作区
python3 scripts/soulforge.py run --workspace /path/to/workspace

# 预览模式（只查看，不写入）
python3 scripts/soulforge.py run --dry-run

# 查看状态
python3 scripts/soulforge.py status
```

### 4. 设置定时任务（可选）

```bash
# 每 2 小时运行
python3 scripts/soulforge.py cron --every 120

# 或通过 OpenClaw cron
openclaw cron add --name soulforge-evolve --every 120m \
  --message "exec python3 ~/.openclaw/skills/soul-evolver/scripts/soulforge.py run"
```

---

## 配置说明

通过 `soulforge/config.json` 配置：

```json
{
  "workspace": "~/.openclaw/workspace",
  "memory_paths": [
    "memory/",
    ".learnings/"
  ],
  "target_files": [
    "SOUL.md",
    "USER.md",
    "IDENTITY.md",
    "MEMORY.md",
    "AGENTS.md",
    "TOOLS.md"
  ],
  "trigger_threshold": 3,
  "backup_enabled": true,
  "backup_dir": ".soulforge-backups/",
  "minimax_api_key_env": "MINIMAX_API_KEY",
  "model": "MiniMax-M2.7",
  "log_level": "INFO"
}
```

---

## 记忆来源

| 来源 | 说明 | 优先级 |
|------|------|--------|
| `memory/YYYY-MM-DD.md` | 每日对话日志 | 高 |
| `.learnings/LEARNINGS.md` | 智能体纠正和洞察 | 高 |
| `.learnings/ERRORS.md` | 命令失败和错误记录 | 中 |
| hawk-bridge 向量库 | 语义记忆搜索 | 中 |
| `.learnings/FEATURE_REQUESTS.md` | 用户请求记录 | 中 |

---

## 更新逻辑

### SOUL.md — 行为身份
触发条件：
- 同一沟通模式出现 3 次以上
- 用户在同一行为上纠正智能体 2 次以上
- 发现新的行为原则

### USER.md — 用户画像
触发条件：
- 用户提供了新的偏好信息
- 产生了新的项目或决策
- 用户工作风格发生变化

### IDENTITY.md — 角色定义
触发条件：
- 智能体的角色或职责发生变化
- 新团队成员加入
- 项目范围变化

### MEMORY.md — 长期记忆
触发条件：
- 做出重要决策
- 项目里程碑达成
- 从错误中学到新教训

### AGENTS.md — 工作流模式
触发条件：
- 发现新的团队协作模式
- 找到工作流改进方法
- 建立新的委托模式

### TOOLS.md — 工具知识
触发条件：
- 发现新的工具使用模式
- 找到集成解决方案
- 遇到工具限制

---

## 安全特性

1. **增量更新** — 从不覆盖，只追加新的内容块
2. **写前备份** — 每次更新前在 `.soulforge-backups/` 创建时间戳备份
3. **来源追踪** — 每个更新块包含源文件和原因
4. **预览模式** — 写入前预览所有变更
5. **阈值门控** — 模式必须出现多次才升级

---

## 文件格式

更新以结构化块的形式追加：

```markdown
<!-- SoulForge Update | 2026-04-05T12:00:00+08:00 -->
## 发现：新的沟通模式

**来源**: memory/2026-04-05.md
**模式**: 用户喜欢用编号列表选择选项
**置信度**: 高（观察4次）

**内容**:
用户不喜欢看长文本选项，给选项时列序号让直接挑。

<!-- /SoulForge Update -->
```

---

## 项目结构

```
soul-evolver/
├── SKILL.md                    # Skill 定义文件
├── README.md                   # 英文说明
├── README.zh-CN.md             # 中文说明
├── LICENSE                     # MIT 许可证
├── soulforge/
│   ├── __init__.py
│   ├── config.py               # 配置管理
│   ├── memory_reader.py        # 读取记忆源
│   ├── analyzer.py             # 模式检测（MiniMax）
│   └── evolver.py              # 更新目标文件
├── scripts/
│   └── soulforge.py            # CLI 入口
├── references/
│   └── ARCHITECTURE.md         # 技术架构
└── tests/
    └── test_soulforge.py       # 单元测试
```

---

## 环境要求

- Python 3.10+
- MiniMax API Key
- OpenClaw（可选，用于 cron 集成）
- hawk-bridge（可选，用于向量记忆）

---

## 许可证

MIT License - 参见 [LICENSE](LICENSE)

---

## 贡献指南

欢迎贡献！提交 PR 前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

**SoulForge**：让 AI 智能体的灵魂在每次对话中进化。
