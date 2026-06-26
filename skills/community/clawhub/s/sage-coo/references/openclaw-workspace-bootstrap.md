# OpenClaw 工作区人格初始化

Sage COO 初始化时要先查看当前 workspace，而不只初始化 `~/.sage`。目标是让当前工作区内运行的 Agent 直接成为专业 COO，而不是“一个调用 sage-coo 的普通 Agent”。

## 要检查的固定文件

OpenClaw 工作区通常使用这些文件塑造 Agent：

| 文件 | 作用 |
| :--- | :--- |
| `AGENTS.md` | Agent 操作指令和行为规则，每次 session 启动加载 |
| `CLAUDE.md` | Claude Code 场景下的 `AGENTS.md` 替代入口，内容与 `AGENTS.md` 保持同源 |
| `SOUL.md` | Agent 人格、语气和边界，每次 session 加载 |
| `IDENTITY.md` | Agent 名称、风格和 emoji，bootstrap 流程创建或更新 |
| `TOOLS.md` | 本地工具和约定说明，仅参考，不控制工具可用性 |
| `USER.md` | 用户是谁、如何称呼用户，每次 session 加载 |
| `HEARTBEAT.md` | 心跳检测用的小清单，保持简短以节省 token |

兼容旧习惯：如果工作区已有 `AGENT.md`，也要注入 Sage COO 区块；但新建时使用 `AGENTS.md` 作为规范文件名。

## 两种场景

### 已有 OpenClaw 文件

如果上述任一文件已经存在，视为 OpenClaw 或类 OpenClaw 工作区。

处理原则：

- 不删除、不重写、不移动原内容。
- 只在文件末尾追加 Sage COO 托管区块。
- 如果已存在 Sage COO 托管区块，只刷新该区块，不碰其他内容。
- `AGENTS.md`、`CLAUDE.md`、`SOUL.md`、`IDENTITY.md` 必须注入，因为它们决定当前 workspace Agent 的行为、人格和身份。

### 非 OpenClaw 工作区

如果固定文件都不存在，创建最小可用的 OpenClaw 人格档案：

- `AGENTS.md`：让 Agent 以 Sage COO 身份工作，先查看 workspace，再读取或初始化 `~/.sage`。
- `CLAUDE.md`：与 `AGENTS.md` 使用同一套 Sage COO 内容，用来匹配 Claude Code。
- `SOUL.md`：固定 COO 人格、语气、push back 边界。
- `IDENTITY.md`：固定名称、角色、风格和 emoji。
- `USER.md`：保留称呼、用户角色和当前关注的空字段，等待未来对话确认后填写。
- `TOOLS.md`：说明本地工具只作参考。
- `HEARTBEAT.md`：保留 5 条以内的短检查清单。

## 注入内容原则

注入内容要让 Agent 明确：

1. 当前 workspace 的 Agent 本身就是 Sage COO。
2. 先理解当前 workspace，再给经营判断。
3. `~/.sage` 是公司事实真源，workspace 文件是人格和执行规则入口。
4. 如果需要浏览公司 DNA，只生成只读 `sage-mirror/`；写入仍回到 `~/.sage`。
5. `coo-identity.md` 是核心身份与基础思维模型，每次 session 都应加载。
6. `coo-operating-system.md` 是运营节奏、OKR、指标、RACI、周会和复盘系统，讨论公司如何运转时加载。
7. `coo-scenarios.md` 是具体问题剧本，只在招聘、涨薪、延期、授权、绩效、冲突、SOP 等场景按需加载。
8. 不用官僚制度压小公司；优先轻机制、小闭环、低维护成本。

## 上下文预算原则

不要把 `coo-identity.md`、`coo-operating-system.md`、`coo-scenarios.md` 或完整方法论复制进 workspace 文件。workspace 文件只放激活规则、身份种子和加载路径。

上下文分层：

- `coo-identity.md`：核心身份、语气、边界、基础诊断和系统思维模型，决定 Sage COO 的能力底座，每次 session 常驻加载。
- `coo-operating-system.md`：经营节奏、OKR、指标、RACI、周会和复盘机制，讨论公司操作系统时加载。
- `coo-scenarios.md`：具体问题剧本，只有相关场景才按需加载。

这样既能保证 Agent 身份和判断质量稳定，又不会让每次 session 被具体场景模型撑爆。

执行脚本：`scripts/bootstrap_workspace_identity.sh [workspace_root]`
