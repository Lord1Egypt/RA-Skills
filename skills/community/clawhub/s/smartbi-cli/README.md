# Smartbi CLI Skill

让**任意 AI agent**（Cursor、Claude Code、Copilot 等）通过 `@smartbi/cli` npm 工具发现并调用 Smartbi 全部 OpenAPI 能力。

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
│   Smartbi OpenAPI             │
│   (datamodel / scheduletask   │
│    tabularmodel / aichat ...) │
└───────────────────────────────┘
```

**一句话**：一个 skill 文件 + 一个 npm 包 = 任意 agent 获得 Smartbi 全平台能力。

## 架构

```
SKILL.md                         ← 入口（agent 加载）
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
│   └─ schedule-task.md          S1 定时计划任务
│
└─ references/                   ← 参考手册（按需加载）
    ├─ init.md                   安装与配置
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
| **通用 OpenAPI 调用** | `smartbi list` → `describe` → `call` 全流程，覆盖任意 `domain.operationId` | 完整 |
| **S1 定时计划任务** | 创建调度计划 + Rhino JS 脚本任务 + 邮件/消息推送（API schema + Rhino 模板已确认） | 完整 |

> 新场景须经过端到端验证后才可入库。

## 依赖

- **npm 包**：`@smartbi/cli >= 1.1.0`（`npm install -g @smartbi/cli@latest`）
- **外部 skill**：**零**。本 skill 自闭环，不依赖任何其他 skill。

## 使用说明

### 安装

```bash
npm install -g @smartbi/cli@latest
smartbi --version   # 确认 >= 1.1.0
smartbi init        # 生成 ~/.smartbi/config.yaml，按提示填入 baseUrl + token
```

### 在 Agent 中使用

1. 将本目录放到 agent 的 skills 路径下（如 Cursor 的 `.cursor/skills/`、Claude Code 的配置的 skills 目录等）
2. Agent 加载 `SKILL.md` 后自动获得以下能力：
   - 发现接口：用户描述需求 → `smartbi list --agent` 语义匹配 → 得到 `operationKey`
   - 理解契约：`smartbi describe <key> --agent` → 加载文档 → 理解参数
   - 执行调用：`smartbi call <key> -d @body.json --agent` → 返回结果
   - 定时任务：识别定时意图 → 生成 Rhino JS → 创建 task + schedule → 启用

### 场景路由

Agent 根据用户问句自动选择场景：

```
用户问句
  ├─ 有「每天/每周/定时/几点」? 
  │   └─ 是 → S1 定时计划任务（生成 task + schedule；是否推送由语义决定）
  └─ 否 → 走 Part 1 通用流程
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
> Agent：找到 `datamodel.queryDataByMql`，确认模型字段后执行查询，返回 s3Url + rowCount

**定时计划任务**：
> 用户：每天 9:00 发送保额大于 20 万的保单数据到邮箱
> Agent：创建 Rhino JS 脚本（MQL 取数 + 过滤 + HTML 格式化）→ 创建任务 → 创建计划（DAY, 9:00, MAIL）→ 启用

## 文件清单

```
smartbi-cli/
├── README.md                    ← 本文件
├── SKILL.md                     ← skill 入口（agent 加载）
├── scenarios/                   ← 已验证场景
│   └── schedule-task.md         S1 定时计划任务
└── references/                  ← 参考手册
    ├── init.md
    ├── discovery.md
    ├── describe.md
    ├── call.md
    ├── strategy.md
    ├── rhino-template.md        MQL 取数 Rhino JS 模板（共用）
    └── doc-index.md
```
