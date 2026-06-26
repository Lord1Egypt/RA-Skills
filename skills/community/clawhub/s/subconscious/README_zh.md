# Subconscious — 有界限的自我改进Agent

持久化、自我进化的行为偏见层。跨会话保持，重启不丢失。在严格约束下安静地塑造Agent行为。为OpenClaw Agent设计。

**版本 1.5** — 生产就绪

## 包含集成

内置与 **self-improving-agent** (v3.0.10) 的连接，该技能由 **[@pskoett](https://clawhub.ai/u/pskoett)** 开发。subconscious 消费该技能产生的学习记录，并将其进化为持久的行为偏见。

```
self-improving-agent (by @pskoett)  →  .learnings/  →  subconscious  →  live/bias
(从错误、纠正和洞察中                  (消费 +
 产生学习记录)                          进化)
```

self-improving-agent 技能文件包含在本包 `self-improving-agent/` 目录下。完整版权归 [@pskoett](https://clawhub.ai/u/pskoett) 所有。

## 快速开始

```bash
# 安装（自动检测OpenClaw workspace）
git clone <repo> ~/.openclaw/skills/subconscious
cd ~/.openclaw/skills/subconscious/scripts
chmod +x install.sh
./install.sh

# 检查状态
SUBCONSCIOUS_WORKSPACE=~/.openclaw/workspace-alfred python3 subconscious_metabolism.py status
python3 subconscious_cli.py verify
python3 subconscious_cli.py bias
```

## 工作原理

```
Learnings Bridge          Pending Queue           Live Store           Session Context
.self-improving/ ────────► tick ───────────────► rotate ───────────► bias inject
                           (reinforce,           (promote eligible,
                            dedupe)               archive stale)
```

- **Learnings Bridge**：每5分钟扫描 `.learnings/`，将新条目加入 pending
- **有界晋升**：item 必须达到阈值才能晋升到 live（confidence≥0.75, reinforcement≥3）
- **治理保护**：所有变更都有类型限制，有日志，可追溯
- **不可变核心**：身份/价值观不能被篡改
- **临时偏见**：每会话最多5条，不污染上下文

## 三层架构

| 层级 | 用途 | 治理规则 |
|------|------|----------|
| `core/` | 不可变身份 | 禁止变更 — 仅手动 |
| `live/` | 活跃学习 | 仅允许有界变更 |
| `pending/` | 新条目队列 | 强化 → 晋升 |

**Item 类型**: `VALUE`, `LESSON`, `PRIORITY`, `PATTERN`, `CONSTRAINT`

## 代谢周期

| 周期 | 频率 | 用途 |
|------|------|------|
| `tick` | 每5分钟 | 扫描 learnings，强化 pending |
| `rotate` | 每小时 | 全面维护，晋升 eligible items |
| `review` | 每天6点 | 健康检查，快照完整性 |

## 文件结构

```
subconscious/
├── SKILL.md                          # OpenClaw 技能定义
├── README.md                         # 英文说明
├── README_zh.md                      # 中文说明
├── CLAUDE.md                         # Claude Code 工作指南
├── .gitignore
├── self-improving-agent/             # 内置集成 (by @pskoett)
│   ├── SKILL.md
│   ├── assets/LEARNINGS.md
│   ├── hooks/openclaw/
│   └── scripts/
├── scripts/
│   ├── install.sh                    # 安装脚本
│   ├── subconscious_metabolism.py   # 代谢 CLI
│   └── subconscious_cli.py          # 管理 CLI
└── subconscious/                     # 核心包
    ├── schema.py                    # Item 数据类
    ├── store.py                    # JSON 文件操作
    ├── retrieve.py                  # 相关性评分
    ├── influence.py                # 偏见格式化
    ├── governance.py                # 变更规则
    ├── evolution.py                 # 晋升管道
    ├── maintenance.py               # 维护
    ├── intake.py                    # 输入提取
    ├── flush.py                     # 快照连续性
    └── learnings_bridge.py          # self-improving-agent 桥接
```

## 环境要求

- Python 3.8+
- OpenClaw workspace
- self-improving-agent（内置，无需单独安装）

## 自定义 Workspace

```bash
# 覆盖 workspace 路径
export SUBCONSCIOUS_WORKSPACE=/path/to/workspace

# 或每次命令指定
SUBCONSCIOUS_WORKSPACE=/path/to/workspace python3 scripts/subconscious_metabolism.py status
```

支持任意 OpenClaw workspace 目录名称。

## 上传到 ClawHub

```bash
cd ~/.openclaw/skills/subconscious

# 登录（首次需要）
clawhub login

# 发布
clawhub publish .

# 查看状态
clawhub inspect <your-handle>/subconscious
```

## 设计原则

1. **有界** — 硬限制：50 core / 100 live / 500 pending
2. **治理** — 类型化变更，有界，无未限制操作
3. **代谢而非守护进程** — 一次性 cron 任务，非持久进程
4. **核心不可变** — 价值观不经人工授权不能变更
5. **会话隔离** — 偏见临时，不污染上下文
