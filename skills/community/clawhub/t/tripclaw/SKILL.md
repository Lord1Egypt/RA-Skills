---
name: tripclaw
description: 将 OpenClaw 生成的自驾行程导入到 TripClaw 应用。当用户说"导入行程到 TripClaw"、"同步到 TripClaw"、"发送到 TripClaw"、"推送到 TripClaw" 或提及 TripClaw 行程同步时触发。支持将行程数据（途经点、住宿、活动、预算等）通过 API 同步到用户的 TripClaw 账户。
---

# TripClaw 行程导入

将 OpenClaw 生成的自驾行程同步到 TripClaw 应用。

## 快速开始

### 1. 配置 API Key

用户需要先配置 TripClaw API Key：

```bash
# 设置环境变量（推荐）
export TRIPCLAW_API_KEY="your-api-key-here"

# 或在 OpenClaw 配置中添加
```

⚠️ **安全提醒**：API Key 是敏感信息，请勿分享、勿提交到公开仓库、勿在截图或录屏中暴露。

### 2. 触发方式

用户说以下任一指令时触发：
- "导入行程到 TripClaw"
- "同步到 TripClaw"
- "发送到 TripClaw"
- "把行程推送到 TripClaw"

## 行程数据结构

TripClaw 接受以下 JSON 格式的行程数据：

```json
{
  "name": "行程名称",
  "description": "行程描述（可选）",
  "startDate": "2024-01-15",
  "endDate": "2024-01-22",
  "travelers": 2,
  "waypoints": [
    {
      "order": 1,
      "name": "地点名称",
      "type": "start|waypoint|destination",
      "location": {
        "address": "详细地址",
        "coordinates": {
          "lat": 25.0389,
          "lng": 102.7183
        }
      },
      "arrivalDate": "2024-01-15",
      "stay": {
        "accommodation": "住宿名称",
        "nights": 1,
        "bookingUrl": "预订链接（可选）"
      }
    }
  ],
  "activities": [
    {
      "date": "2024-01-16",
      "name": "活动名称",
      "description": "活动描述",
      "location": {
        "address": "活动地点",
        "coordinates": { "lat": 0, "lng": 0 }
      },
      "duration": "2小时",
      "cost": 100
    }
  ],
  "budget": {
    "total": 15000,
    "currency": "CNY"
  }
}
```

### 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| name | ✅ | 行程名称 |
| description | ❌ | 行程描述 |
| startDate | ✅ | 开始日期 (YYYY-MM-DD) |
| endDate | ✅ | 结束日期 (YYYY-MM-DD) |
| travelers | ❌ | 出行人数，默认 1 |
| waypoints | ✅ | 途经点数组，至少 1 个 |
| activities | ❌ | 活动安排数组 |
| budget | ❌ | 预算信息 |

### Waypoint 类型

- `start` - 出发点
- `waypoint` - 中途经停点
- `destination` - 最终目的地

## 使用流程

1. **检测意图**：用户表达导入/同步行程到 TripClaw 的意图
2. **收集数据**：从当前对话或用户提供的行程信息中提取数据
3. **构建结构**：按照上述 JSON 结构组织行程数据
4. **调用 API**：使用 `scripts/import_trip.py` 发送到 TripClaw
5. **反馈结果**：告知用户导入成功或失败原因

## 执行导入

使用脚本执行实际导入：

```bash
python3 scripts/import_trip.py --api-key "$TRIPCLAW_API_KEY" --data '<trip-json-data>'
```

或传入文件：

```bash
python3 scripts/import_trip.py --api-key "$TRIPCLAW_API_KEY" --file trip.json
```

## API 参考

详细的 API 文档请参阅 [references/api.md](references/api.md)。

## 错误处理

| 错误码 | 说明 | 处理建议 |
|--------|------|----------|
| 401 | API Key 无效或过期 | 检查 TRIPCLAW_API_KEY 配置 |
| 400 | 数据格式错误 | 检查 JSON 结构是否符合规范 |
| 404 | 用户不存在 | 确认 API Key 对应的账户状态 |
| 429 | 请求过于频繁 | 稍后重试 |
| 500 | 服务器错误 | 联系 TripClaw 支持 |

## 隐私与安全

- API Key 仅存储在用户本地环境
- 行程数据通过 HTTPS 加密传输
- 不会记录或缓存敏感数据