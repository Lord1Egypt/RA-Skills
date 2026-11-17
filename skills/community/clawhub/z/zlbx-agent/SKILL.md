---
name: zlbx-agent
description: 知了商机大师开放平台。当用户需要"查标讯/看商机/发起AI对话/建跟进任务/查积分"等招投标商机场景时使用。通过命令行工具 scripts/zlbx_agent.py 调用知了开放平台 API。
---

# 知了商机大师 · 开放平台技能

用命令行工具 `scripts/zlbx_agent.py` 调用知了开放平台，覆盖对话、商机订阅、跟进任务、标讯正文、积分五类能力。

## ⚠️ 第一步：确认 API Key（每次启用本技能务必先做这一步）

本技能所有能力都需要一把 `ZLBX_AGENT_API_KEY`。**加载本技能后、执行任何子命令之前，先检查环境变量里是否已配置该 Key**：

```bash
echo "${ZLBX_AGENT_API_KEY:-未配置}"
```

**若显示"未配置"（或用户尚未提供 Key）**：不要直接尝试调用接口（会 401 失败），而应**明确、主动地提示用户去获取 API Key**，把下面这段话原样发给用户——

> 使用「知了商机大师」技能前，需要先提供一把 API Key。请点击此链接注册并创建 Key（**注册即为免费用户，赠送 20 元额度，可直接体验**）：
> 👉 获取地址： https://agent.zhiliaobiaoxun.com/developer?utm_source=skill
> 创建后把形如 `zlbx_agent_xxx` 的 Key 发给我，或自行执行 `export ZLBX_AGENT_API_KEY=zlbx_agent_xxx`。

拿到用户提供的 Key 后再继续。**未拿到 Key 前不要调用任何子命令。**

## 环境变量

- `ZLBX_AGENT_API_KEY`（必填）：形如 `zlbx_agent_xxx`，在 <https://agent.zhiliaobiaoxun.com/developer?utm_source=skill> 获取。注册即为免费用户，赠送 20 元额度，可直接体验。
- `ZLBX_AGENT_BASE`（可选）：API 基址，默认 `https://agent.zhiliaobiaoxun.com/openapi/v1`。

工具**无第三方依赖**（仅用 Python 标准库），任意装有 Python 3 的环境可直接运行。

## 使用方式

```bash
export ZLBX_AGENT_API_KEY=zlbx_agent_xxxxx
python3 scripts/zlbx_agent.py <子命令> [参数]
```

所有子命令输出 JSON。异步类子命令加 `--wait` 会自动轮询到完成再返回结果。

### 对话
- `chat --message "帮我分析这条标讯的中标概率" [--session <对话ID>]` —— 发起或继续对话（一次性完整输出）。返回含 `session_uid`，续聊时传回。
- `conversations [--page 1]` —— 对话列表。
- `messages --session <对话ID>` —— 某对话完整内容。
- `last-reply --session <对话ID>` —— 某对话最后一次模型输出。

### 商机订阅
- `opp-trigger [--wait]` —— 触发商机订阅分析（异步）。`--wait` 轮询到完成并打印最新商机列表。
- `opp-status --task-id <N>` —— 查询运行状态。
- `opp-list [--date YYYY-MM-DD]` —— 获取最近一次商机列表。

### 跟进任务
- `task-create --description "每天早上汇总昨天新发布的安防类标讯" [--schedule '{"kind":"daily","hour":8}'] [--title ...] [--no-notify]` —— 创建定时跟进任务。schedule 支持 `{"kind":"daily","hour","minute"}` / `{"kind":"weekly","weekday","hour"}` / `{"kind":"interval","every_hours"}`，缺省每天 03:00。
- `task-list [--status active|paused|archived]` —— 任务列表。
- `task-latest-run --task-id <N>` —— 某任务最近一次执行结果。
- `task-run --task-id <N> [--wait]` —— 触发某任务立即执行（异步）。

### 标讯正文
- `bid-detail --bid-id <N> [--bid-type 1|2]` —— 获取标讯正文（1招标/2中标，可省）。
- `bid-analyze --bid-id <N> [--bid-type 1|2] [--wait]` —— 触发项目分析师深度分析（异步）。
- `bid-analysis --bid-id <N>` —— 获取最近一次分析结果。

### 积分
- `balance` —— 查询积分余额、会员当日剩余额度与到期时间。

## 说明
- 每次调用都会消耗账号积分/会员额度，与网页端一致。
- 限流：读类 60 次/分钟、写/触发类 6 次/分钟；超限返回 429。
- 遇到 `401` 检查 `ZLBX_AGENT_API_KEY`；`402` 为积分不足；`429` 稍后重试。
