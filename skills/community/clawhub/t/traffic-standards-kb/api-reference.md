# API Reference - Traffic Standards Knowledge Base

> Detailed API documentation for the Solvex Standards API. See SKILL.md for usage overview.

## Authentication

The Standards API uses **API Key Authentication only**:

**Header:** `X-API-Key: $STANDARDS_API_KEY`

```bash
curl -X POST "https://solvexpert.net/api/v1/standards/query" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $STANDARDS_API_KEY" \
  -d '{...}'
```

Get API Key from: https://solvexpert.net

## Configuration

### API Key Priority

| Priority | Source | Method |
|----------|--------|--------|
| 1 | Environment Variable | `export STANDARDS_API_KEY="solvex-your-api-key"` |
| 2 | settings.json | `{"env": {"STANDARDS_API_KEY": "solvex-your-api-key"}}` |
| 3 | Request Header | Manual `X-API-Key` header per request |

**⚠️ Important:**
- Don't hardcode API keys in code
- Use environment variables or settings.json
- Replace `solvex-your-api-key` placeholders with actual configured values

## API Endpoint

**POST** `/api/v1/standards/query`

### ⚠️ CRITICAL Authentication Requirements

**TWO authentication methods are BOTH required:**

1. **Header:** `X-API-Key: $STANDARDS_API_KEY`
2. **Request Body Parameter:** `searchAuthToken: "Thn5ItDQS9aEa3cay-855l2woSmW2Z4U"` **(MANDATORY)**

**Missing `searchAuthToken` will cause:** `"Authentication error: API key is invalid!"` even with valid API key.

### Request Parameters

| Field | Type | Required | Description | Default |
|-------|------|----------|-------------|---------|
| question | string | ✅ | Natural language query | - |
| domains | string[] | ❌ | Domain filters | Auto-detected |
| depth | string | ❌ | basic/medium/full | medium |
| searchId | string | ❌ | Search application ID (推荐) | 4d68cee6226611f19327c66d7f7cba76 |
| searchAuthToken | string | ✅ | **MANDATORY** SearchBots auth token | Thn5ItDQS9aEa3cay-855l2woSmW2Z4U |
| pageSize | int | ❌ | 1-100 | 10 (mapped from depth) |
| similarityThreshold | double | ❌ | 0.0-1.0 | 0.5 |

### Example Request

```bash
export STANDARDS_API_KEY="your-actual-api-key"

curl -X POST "https://solvexpert.net/api/v1/standards/query" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $STANDARDS_API_KEY" \
  -d '{
    "question": "智慧高速相关的标准",
    "domains": ["新兴领域"],
    "depth": "medium",
    "searchId": "4d68cee6226611f19327c66d7f7cba76",
    "searchAuthToken": "Thn5ItDQS9aEa3cay-855l2woSmW2Z4U"
  }'
```

### Response Format

```json
{
  "code": 0,
  "data": {
    "standards": [{
      "standardNumber": "GB 14886-2016",
      "title": "道路交通信号灯设置与安装规范",
      "executingUnit": "中华人民共和国公安部",
      "scope": "本标准规定了道路交通信号灯的设置条件...",
      "similarity": 0.92,
      "keyPoints": ["信号灯设置应满足交通安全要求"]
    }],
    "total": 10,
    "aggregations": {"信号控制": 8}
  }
}
```

## Depth Levels

| depth | pageSize | Content |
|-------|----------|---------|
| basic | 5 | 标准号 + 标题 + 执行单位 + 适用范围 |
| medium | 10 | + 归口单位 + 发布/实施日期 + 关键条款 |
| full | 30 | + 完整元数据 + AI要点总结 + 条文索引 |

## Error Handling

### 401 Unauthorized
- **Cause:** Missing or invalid API Key
- **Fix:**
  - Set `X-API-Key` header with valid API Key
  - Get API Key from: https://solvexpert.net

### 504 Gateway Timeout
- **Cause:** Request taking longer than Nginx timeout (RAG API slow)
- **Fix:** Timeout increased to 600s. If still timing out, reduce `depth` parameter.

### Empty Standards Array
- **Cause:** No matching documents in knowledge base
- **Fix:** Verify RAG dataset has documents with proper metadata

### 400 Bad Request
- **Cause:** Invalid depth value or pageSize out of range
- **Fix:** Use basic/medium/full, pageSize between 1-100

### "Authentication error: API key is invalid!"
- **Cause:** Missing or invalid `searchAuthToken` parameter
- **Fix:** Always include `searchAuthToken: "Thn5ItDQS9aEa3cay-855l2woSmW2Z4U"` in request body

## Architecture

```
User Task (智慧路口解决方案)
    ↓
Skill (Parse task → Extract domain)
    ↓
Solvex API /api/v1/standards/query (User API KEY auth)
    ↓
RAG SearchBots API (Two-Step Process)
    ├─ Step 1: /api/v1/searchbots/detail?search_id={search_id}
    │           → Get kb_ids from search configuration
    └─ Step 2: /api/v1/searchbots/retrieval_test
                → Retrieve with kb_ids and search_id
    ↓
Return Standards → Format citations
```

## Domain Values

Valid `domains` array values:
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

## Standard Metadata Fields

When adding PDF documents to RAG:

| Field | Example |
|-------|---------|
| standard_number | GB 14886-2016 |
| title | 道路交通信号灯设置与安装规范 |
| executing_unit | 中华人民共和国公安部 |
| committee | 全国交通工程设施（公路）标准化技术委员会 |
| drafting_unit | 公安部交通管理科学研究所 |
| drafters | ["张三", "李四"] |
| publish_date | 2016-12-13 |
| implement_date | 2017-07-01 |
| replaces | GB 14886-2006 |
| scope | 本标准规定了... |
| category | 信号控制 |
| level | 国家标准/行业标准/地方标准/国际标准 |
