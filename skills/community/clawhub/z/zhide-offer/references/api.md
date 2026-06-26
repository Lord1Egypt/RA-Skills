# 职得Offer MCP API 文档

## 接口列表

| 工具名 | 说明 |
|--------|------|
| account.entitlements | 查询账户权益和每日调用配额 |
| jobs.search | 搜索岗位列表 |
| jobs.get | 获取岗位详情 |
| jobs.facets | 获取账户权益+筛选项（同 entitlements） |
| interviews.search | 搜索面经列表 |
| interviews.get | 获取面经详情 |

---

## account.entitlements

**参数**：无

**返回**：
```json
{
  "userId": "...",
  "userLevel": 2,
  "userLevelDesc": "大会员",
  "expirationTime": "2027-04-10",
  "mcpDailyLimit": 200,
  "mcpUsedToday": 5
}
```

---

## jobs.search

**参数**：
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| keyword | string | 否 | 搜索关键词 |
| company | string | 否 | 公司名 |
| city | string | 否 | 城市 |
| pageSize | integer | 否 | 返回数量，默认10 |

**结果路径**：`result.structuredContent.data.items[]`

**item 字段**：
| 字段 | 说明 |
|------|------|
| id | 岗位ID（用于 jobs.get） |
| company | 公司名 |
| city | 城市 |
| （title 字段在列表中可能为空，详情用 jobs.get） |

---

## jobs.get

**参数**：
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | string | ✅ | 岗位ID |

**结果路径**：`result.structuredContent.data`

**data 字段**：
| 字段 | 说明 |
|------|------|
| title | 岗位名称 |
| company | 公司名 |
| city | 城市 |
| description | 岗位描述（JD） |

---

## interviews.search

**参数**：
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| position_query | string | 建议 | 岗位检索词（推荐，精准） |
| query | string | - | 等价于 position_query |
| positionQuery | string | - | 等价于 position_query（camelCase） |
| job_id | string | 否 | 单个岗位ID过滤 |
| job_ids | string | 否 | 多个岗位ID，逗号分隔 |
| company | string | 否 | 公司名过滤 |
| city | string | 否 | 城市过滤 |
| recruitment_tag | string | 否 | 招聘类型：校招/实习/社招 |
| industry | string | 否 | 行业 |
| limit | integer | 否 | 返回数量，1-20，默认10 |

**⚠️ 注意**：position_query 用单一精准词组，多词组合可能返回0条。

**结果路径**：`result.structuredContent.data.items[]`

**item 字段**：
| 字段 | 说明 |
|------|------|
| id | 面经ID（用于 interviews.get） |
| title | 标题（格式："公司的岗位名的面经"） |
| company | 公司名 |
| position | 岗位方向 |
| city | 城市 |
| difficulty | 招聘类型（校招/实习/社招） |
| tags | 标签数组 |
| summary | 面经摘要 |

---

## interviews.get

**参数**：
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | string | ✅ | 面经ID |

**结果路径**：`result.structuredContent.data`

**data 结构**：
```
data
├── title
├── company
├── position
├── city
├── summary
└── content
    ├── background    # 面试者背景介绍
    ├── outcome       # 结果（如"结果待更新"）
    ├── takeaways[]   # 关键要点列表
    └── rounds[]      # 面试轮次
        ├── key       # round1/round2/round3
        ├── title     # 轮次名称（如"一面"）
        ├── duration  # 时长
        ├── tags[]    # 考察重点标签
        ├── characteristics  # 面试官风格描述
        └── questionAnswers[]
            ├── question  # 面试题
            └── answer    # 回答
```

---

## MCP 请求格式

```http
POST https://offer.yxzrkj.cn/mcp
Content-Type: application/json
Accept: application/json, text/event-stream
Authorization: Bearer <KEY>

{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "<工具名>",
    "arguments": { ...参数 }
  }
}
```

initialize 握手（每次调用前需先发送）：
```json
{
  "jsonrpc": "2.0",
  "id": 0,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": { "name": "client", "version": "1.0" }
  }
}
```
