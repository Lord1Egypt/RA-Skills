---
name: ss-requirements-to-teambition
description: 从 SaleSmartly 客服会话中自动采集带标签的对话，经 AI 分析提取需求，创建 Teambition 任务。用于客服反馈→需求管理自动化。触发词：SS需求采集、客服需求整理、SaleSmartly会话转任务、聊天记录转需求、客户反馈建任务、采集会话创建TB任务。当用户想把 SaleSmartly 中的客户会话整理成 Teambition 需求任务时使用。
---

# SS Requirements → Teambition

从 SaleSmartly 客服会话中采集对话 → AI 分析提取需求 → 自动创建 Teambition 任务。

## 前置条件

1. **SaleSmartly API Key** — SS 后台 → 设置 → API 管理
2. **Teambition MCP** — 见 [tb_mcp_setup.md](references/tb_mcp_setup.md)

## 快速开始

### 1. 配置

```bash
cp scripts/config.example.json scripts/config.json
```

编辑 `scripts/config.json`，填入你的配置。各字段含义和获取方式见 [config_fields.md](references/config_fields.md)。

### 2. 采集数据（纯脚本，0 token）

```bash
cd scripts && python3 collect.py
```

输出：`scripts/data/ss_sessions_YYYY-MM-DD.json`

### 3. AI 分析 + 创建任务

对 AI 说：「读取 `scripts/data/` 下最新的 JSON，分析会话内容，按 config.json 配置创建 TB 任务」

AI 会按 [analysis_template.md](references/analysis_template.md) 中的规则执行。

## 定时自动化（可选）

在 OpenClaw 中配置 cron：

```json
{
  "schedule": { "kind": "cron", "expr": "0 10 * * *", "tz": "Asia/Shanghai" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "执行 SS 需求采集：1) cd scripts && python3 collect.py 2) 读取 data/ 下最新 JSON 3) 按 config.json 配置分析并创建 TB 任务"
  }
}
```

## 文件结构

```
scripts/
├── collect.py              # 数据采集（0 token）
├── config.example.json     # 配置模板
└── config.json             # 你的配置（不入库）
references/
├── tb_mcp_setup.md         # TB MCP 配置指南
├── config_fields.md        # 配置项获取指南
└── analysis_template.md    # AI 分析 + 任务创建模板
```

## 关键约束

- SS API 限流 10 QPS，脚本内置 200ms 间隔
- 增量采集：`state.json` 记录上次时间戳，下次从该点开始
- 创建任务前先查重，避免同一会话重复建任务
- 数据文件保留 7 天自动清理