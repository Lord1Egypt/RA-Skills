---
name: skillforge-discovery
description: SkillForge API 服务发现 - 自动发现和调用付费 AI 服务。当 OpenClaw Agent 需要某个能力但本地没有时，自动查找并推荐可用服务。
homepage: https://github.com/skillforge/skillforge-skill
metadata: {"openclaw":{"emoji":"🔍","requires":{"bins":["node"],"env":["SKILLFORGE_API_URL","SKILLFORGE_API_KEY"]},"primaryEnv":"SKILLFORGE_API_KEY"}}
---

# SkillForge 服务发现

自动发现和调用付费 AI 服务。当需要某个能力但本地没有时，自动查找并推荐可用服务。

## 功能

1. **自动检测能力缺口** - 当 Agent 遇到需要外部 API 支持的任务时，自动识别
2. **发现匹配服务** - 从 SkillForge 平台发现付费 API 服务
3. **调用服务** - 用户确认后调用服务并返回结果

## 触发词

- 服务发现、发现服务、找 API
- 能力缺口、缺少能力、需要能力
- SkillForge、技能市场、API 市场
- 调用外部服务、付费 API

## 使用方式

### 1. 手动触发发现

```
用户: 帮我找一个能生成图片的 API
Agent: [触发 skillforge discover]
```

### 2. 自动能力检测

当 Agent 识别到以下场景时，自动触发服务发现：

- 用户请求的功能需要外部 API
- 当前环境缺少某项能力
- 任务涉及特定领域（图像、语音、视频等）

## 配置

```yaml
# ~/.openclaw/config.yaml
skills:
  skillforge:
    platform_url: "https://skillforge.example.com"
    api_key: "sk_xxxx"
    auto_discover: true
    discover_limit: 3
    max_cost_per_call: 1.00
```

## API 接口

### 发现服务

```http
GET /v1/discover?capability={capability}&limit={limit}
Authorization: Bearer {api_key}
```

### 调用服务

```http
POST /v1/services/{id}/invoke
Authorization: Bearer {api_key}
Content-Type: application/json

{
  "input": {
    "prompt": "a cat in space"
  }
}
```

## 错误处理

| 错误码 | 说明 | 处理方式 |
|--------|------|----------|
| SERVICE_NOT_FOUND | 服务不存在 | 重新发现服务 |
| SERVICE_OFFLINE | 服务离线 | 选择其他服务 |
| INSUFFICIENT_BALANCE | 余额不足 | 提示用户充值 |
| INVOCATION_ERROR | 调用失败 | 重试或换服务 |

## 费用说明

- 所有服务调用都会从账户余额扣除费用
- 服务价格由开发者设定
- 平台收取 20% 手续费，开发者获得 80%
- 部分服务提供免费额度