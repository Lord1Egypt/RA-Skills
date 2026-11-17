# SmartBI CLI Skill

Skill 版本：**2.1.0**。运行时依赖的 `@smartbi/cli` 版本独立管理，最低要求为 2.0.0。

保留标准 Skill 的业务路由，为数据类请求采用基于模型的直接取数路径：用户问句 → 读取必要模型信息 → 根据模型与 SDK 能力选择 MQL 或只读 SQL → CLI 调用 SDK → 校验数据 → 桌面智能体分析/展示。直接取数不依赖模型训练或 AI 问数，无需额外查询框架。详见 `references/query-routing.md`。

在原版场景索引中新增数据查询与洞察，入口为 `scenarios/data-query.md`；原有通用 API、定时任务和推送保留。外部智能体通过接口定位资源，不依赖 SmartBI 页面预选信息。模型取数按语义选择 MQL/只读 SQL，已有报表按定义与参数查询/导出；正式报告、归因、预测和综合大屏按路由默认白泽，用户指定直接取数或本地分析时遵循其选择。已有数据制图和文件转换继续本地处理；创建或修改 SmartBI 报表仍走资源操作接口。

普通取数依赖 Node/npm 全局安装的 SmartBI CLI（>=2.0.0）。Python 仅用于可选辅助脚本/文件读取，不是 MQL 前置条件。跨桌面客户端需具备命令执行和文件读写能力；不能把单一客户端的实测视为所有客户端已验证。

支持具备命令执行和文件读写能力的桌面智能体，通过 `@smartbi/cli` 发现并调用当前环境开放且有权限的 SmartBI API。

## 目标

```
          ┌──────────┐
          │ 任意 Agent │
          └─────┬────┘
                │ 自然语言意图
                ▼
┌───────────────────────────────┐
│   smartbi-cli skill           │
│                               │
│  意图 → operationKey → call   │
│                               │
│  定时计划任务 / ...           │
└───────────────┬───────────────┘
                │ smartbi call
                ▼
┌───────────────────────────────┐
│   SmartBI OpenAPI             │
│   (datamodel / scheduletask   │
│    tabularmodel / aichat ...) │
└───────────────────────────────┘
```

Skill 提供业务路由与调用规则，实际能力取决于当前 SDK、模型定义和账号权限。

普通“查询XXX数据”默认取齐指定条件和粒度下的结果；`limit`控制单次批量，满批且无结束证据时继续分页。明确TopN/前N条/样本时按指定范围停止。数据默认直接展示，文件按需交付；不能将首批或预览称为全部，执行受容量或耗时限制时明确说明未完成范围。

## 架构

```
SKILL.md                         ← 入口（agent 加载）
│
├─ 直接取数                       ← 必要元数据 → MQL/SQL → 校验 → 本地分析/交付
│   query-routing.md / data-model-query.md
│
├─ Part 1: Core CLI Workflow     ← 骨架，所有 OpenAPI 调用通用
│   Phase 0  惰性预检
│   Phase 1  Discover  (smartbi list)
│   Phase 2  Contract  (smartbi describe + doc)
│   Phase 3  Execute   (smartbi call)
│   Phase 4  Diagnose  (失败诊断)
│
├─ Part 2: Scenario Guides（索引）  ← 按意图路由，命中后加载对应文件
│
├─ scenarios/                    ← 场景文件（每个独立验证）
│   ├─ schedule-task.md          S1 定时计划任务
│   ├─ push-message.md           S2 消息推送
│   └─ data-query.md             数据查询与洞察
│
└─ references/                   ← 参考手册（按需加载）
    ├─ init.md                   安装与配置
    ├─ profiles.md               多环境（profile）规范
    ├─ discovery.md              Phase 1 详细流程
    ├─ describe.md               Phase 2 详细流程
    ├─ call.md                   Phase 3 详细流程
    ├─ strategy.md               策略与常见模式
    ├─ rhino-template.md         MQL 取数 Rhino JS 模板（共用）
    └─ doc-index.md              domain → 文档路径索引
```

## 当前能力

| 场景 | 能力 | 状态 |
|------|------|------|
| **直接 MQL 取数** | 字段发现、过滤、聚合、排序、分页及按需计算，本地分析与文件交付 | 按目标环境契约、模型字段和查询结果逐次校验 |
| **通用 OpenAPI 调用** | `smartbi list` → `describe` → `call`，按当前注册接口执行 | 保留原标准流程 |
| **S1 定时计划任务 / S2 推送** | 定时任务、脚本及消息推送指南 | 保留原场景，本轮只读验收不代表写操作已复测 |
| **已有报表取数** | 资源发现、元数据、参数、导出与文件校验 | 按报表类型、有效参数和业务结果逐次校验 |
| **SmartBI AI / Baize** | 按数据查询与洞察场景处理显式请求或复杂洞察 | 按需分支，不是普通直接取数前置 |

> 新场景按具体类型和路径完成端到端验收后才声明支持；已加入的扩展说明须保留未验证边界。

## 依赖

- **npm 包**：`@smartbi/cli >= 2.0.0`（`npm install -g @smartbi/cli@latest`）
- **外部 skill**：**零**。本 skill 自闭环，不依赖任何其他 skill。

## 使用说明

### 安装

```bash
npm install -g @smartbi/cli@latest
smartbi --version   # 确认 >= 2.0.0
smartbi init --server-type <sdk-server|smartbi> --base-url <url> --token <token>
                    # 全参数生成 ~/.smartbi/config.yaml
```

### 在 Agent 中使用

1. 将本目录放到 agent 的 skills 路径下（如 Cursor 的 `.cursor/skills/`、Claude Code 的配置的 skills 目录等）
2. Agent 加载 `SKILL.md` 后自动获得以下能力：
   - 发现接口：未知操作时由 `smartbi list --profile <name> --agent` 语义匹配 → 得到 `operationKey`
   - 查询快速路径：已知并核实 operationKey 时直接调用；尚未核实时 `describe → call`；只有契约不足才读取 doc
   - 理解契约：`smartbi describe <key> --profile <name> --agent` → 加载文档 → 理解参数
   - 执行调用：`smartbi call <key> --profile <name> -d @body.json --agent` → 返回结果
   - 定时任务：识别定时意图 → 生成 Rhino JS → 创建 task + schedule → 启用

### 场景路由

Agent 根据用户问句自动选择场景：

```
用户问句
  ├─ 明确要求定时、推送或资源操作 → 原场景 / 通用 API 流程
  ├─ 普通模型问数 → 模型元数据 → MQL/只读 SQL → 校验结果
  ├─ 已有报表问数 → 报表定义与参数 → 只读查询/导出 → 校验结果
  ├─ 明确白泽或默认复杂洞察 → 会话流程（用户指定直接/本地优先）
  └─ 已有数据的本地报告、图表或文件转换 → 桌面智能体本地处理
```

## 如何新增 Scenario

1. 新建 `scenarios/<name>.md` — 自描述文件：触发条件 + 请求体模板 + 注意事项
2. 通过实际 API 调用端到端验证（Python 脚本或 smartbi call）
3. `SKILL.md` Part 2 索引表加一行
4. 如有新的共享代码模板 → `references/` 下新增

每个新场景必须经过端到端验证后才可入库，不添加未验证的 placeholder。

## 示例对话

**即时查询**：
> 用户：帮我查一下上个月各分支行的贷款余额
> Agent：复用或定位模型，核实余额口径后直接MQL查询，返回各分支行余额、日期范围和必要说明；需要文件时下载校验后给本地文件，不暴露签名地址。

**定时计划任务**：
> 用户：每天 9:00 发送保额大于 20 万的保单数据到邮箱
> Agent：创建 Rhino JS 脚本（MQL 取数 + 过滤 + HTML 格式化）→ 创建任务 → 创建计划（DAY, 9:00, MAIL）→ 启用

## 文件清单

```
smartbi-cli/
├── README.md                    ← 本文件
├── SKILL.md                     ← skill 入口（agent 加载）
├── agents/                      ← Agent入口提示
│   └── openai.yaml
├── scripts/                     ← 按需辅助工具，不是普通查询前置
│   ├── artifact_io.py           文件识别、下载与读取
│   ├── baize_session.py         白泽路径的会话工具
│   ├── smartbi_internal.py      会话工具共用模块
│   └── inject-script.mjs        脚本参数注入
├── scenarios/                   ← 保留标准业务场景
│   ├── schedule-task.md         S1 定时计划任务
│   ├── push-message.md          S2 消息推送
│   └── data-query.md            数据查询与洞察（扩展）
└── references/                  ← 参考手册
    ├── query-routing.md         直接取数范围、最小路径及校验
    ├── data-model-query.md      MQL/SQL接口契约与示例
    ├── report-query.md          已有报表定位、参数、导出与校验
    ├── artifact-handling.md     文件值保真及格式处理
    ├── sessions-and-logs.md     白泽会话与执行校验
    ├── agent-workflows.md / custom-tools.md / insight-agent-behavior.md
    ├── troubleshooting.md      按失败层级排错
    ├── init.md
    ├── profiles.md
    ├── discovery.md
    ├── describe.md
    ├── call.md
    ├── strategy.md
    ├── rhino-template.md        MQL 取数 Rhino JS 模板（共用）
    └── doc-index.md
```
