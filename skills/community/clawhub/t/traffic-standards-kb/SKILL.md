---
name: traffic-standards-kb
description: Use when writing Chinese smart transportation solutions (智慧路口, 智能停车, V2X, MaaS, ETC, 智慧公交, 智慧高速, 智慧服务区, 智慧交管, 智慧交运, 车路云一体化, 智能网联, 低空经济, 智慧物流, 自动驾驶, 智慧公交) or technical proposals requiring GB/JT/GA industry standards citation. Requires API key from https://solvexpert.net
---

# Traffic Standards Knowledge Base

## Overview

Retrieve Chinese transportation standards (GB, JT, GA) via Solvex API. Detects domain → queries API → formats citations.

## Installation

```bash
# Install globally (available in all projects)
npx skills add solvex-top/solvex-skills@traffic-standards-kb -g -y

# Install to current project only
npx skills add solvex-top/solvex-skills@traffic-standards-kb -y

# Update to latest version
npx skills update traffic-standards-kb

# Remove
npx skills remove traffic-standards-kb
```

## Prerequisites

**API Key:** Get from https://solvexpert.net

```bash
# Option 1: Export in shell (for bash commands)
export STANDARDS_API_KEY="solvex-your-api-key"

# Option 2: Add to ~/.claude/settings.json (for Claude internal use)
{
  "env": {
    "STANDARDS_API_KEY": "solvex-your-api-key"
  }
}
```

**⚠️ CRITICAL:** Environment variables in `settings.json` are NOT automatically available to bash commands. For API calls via bash, you must:
1. Export the variable in your shell, OR
2. Pass the key explicitly in the command

## Quick Reference

| Domain | Keywords | Standards |
|--------|----------|-----------|
| Signal Control | 智慧路口, 交通信号, 自适应信号 | GB series, GB series |
| Parking | 智能停车, 停车诱导, 路侧停车 | GB/T series, JT/T series |
| Monitoring | 电子警察, 违章抓拍, 车牌识别 | GA/T series, GB/T series |
| Data Collection | 交通检测, 流量检测, 地磁, 雷达 | JT/T series, GB/T series |
| Tolling | ETC, 电子收费 | JT/T series, JTG series |
| Smart Highway | 智慧高速, 高速监控 | JT/T series, JT/T series |
| Service Area | 智慧服务区, 服务区设施 | JTJ series, JT/T series |
| Public Transit | 智慧公交, BRT, 公交优先 | JT/T series |
| V2X | V2X, V2V, V2I, C-V2X | GB/T series, YD/T series |
| MaaS | MaaS, 出行即服务 | JT/T series |
| Emerging | 新兴领域, 智能交通 | GB/T, JT/T, GA/T series |

## Usage

### Minimum Working Request

```bash
curl -s -X POST "https://solvexpert.net/api/v1/standards/query" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $STANDARDS_API_KEY" \
  -d '{
    "question": "智慧高速及智慧服务区相关的标准",
    "domains": ["新兴领域"],
    "depth": "medium",
    "searchId": "4d68cee6226611f19327c66d7f7cba76",
    "searchAuthToken": "Thn5ItDQS9aEa3cay-855l2woSmW2Z4U"
  }' | python3 -m json.tool
```

### Required Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `question` | string | ✅ | Natural language query |
| `domains` | string[] | ❌ | Domain filter (auto-detected if omitted) |
| `depth` | string | ❌ | basic/medium/full (default: medium) |
| `searchAuthToken` | string | ✅ | **REQUIRED**: `Thn5ItDQS9aEa3cay-855l2woSmW2Z4U` |
| `searchId` | string | ❌ | Recommended: `4d68cee6226611f19327c66d7f7cba76` |

### Valid Domain Values

- 信号控制
- 停车系统
- 交通监控
- 数据采集
- 收费系统
- 公共交通
- 车路协同
- 出行服务
- 交通管理
- 新兴领域

### Response Format

```json
{
  "code": 0,
  "message": "Success",
  "data": {
    "standards": [
      {
        "standardNumber": "GB 14886-2016",
        "title": "道路交通信号灯设置与安装规范",
        "similarity": 0.92,
        "content": "..."
      }
    ],
    "total": 10
  }
}
```

**Citation Format:**
```
[1] GB 14886-2016 道路交通信号灯设置与安装规范
[2] GA/T 1400-2017 公安视频监控联网系统
```

See `api-reference.md` for full API docs.

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Missing `searchAuthToken` | ❌ "Authentication error: API key is invalid!" | **ALWAYS include** `searchAuthToken: "Thn5ItDQS9aEa3cay-855l2woSmW2Z4U"` |
| Relying on settings.json for bash | ❌ Environment variable not found | Export in shell OR pass key explicitly |
| 直接调用RAG API | 绕过用户认证 | 必须通过Solvex API |
| depth值拼写错误 | 请求被拒绝 | 只能使用basic/medium/full |
| 引用格式不统一 | 文档不专业 | 使用[1][2][3]标准格式 |
| 不验证API响应 | 返回空结果 | 检查code==0和data.standards非空 |

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "标准引用可以在最后添加" | 没有标准的方案会被认为不专业，可能直接被拒绝 |
| "我记得主要标准号" | 记忆不准确，GB标准经常更新，引用错误版本会有问题 |
| "这个项目很简单不需要" | 即使小型项目也需要合规性声明，标准引用体现专业性 |
| "用户没有明确要求" | 行业标准是隐含要求，主动引用体现专业素养 |
| "时间太紧了" | 查询标准只需几秒，但缺少标准可能导致方案被拒 |

## Red Flags - STOP and Cite Standards

- "这个很简单，不需要标准"
- "我凭记忆写就行"
- "用户没要求就不用加"
- "先写框架，后面再补"
- "这个领域不强制标准"
- "我是专家，按我的来"

**All of these mean: Cite relevant standards. No exceptions.**
