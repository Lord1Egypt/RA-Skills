# MCP API - fetch-asset Endpoint Examples

## Endpoint
```
POST https://kansas3.8glabs.com/mcp
```

## Headers
```
X-API-Key: YOUR_API_KEY
Content-Type: application/json
Accept: application/json, text/event-stream
```

---

## Example 1: Fetch a Completed Video Job

### Request
```bash
curl -s -X POST \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "fetch-asset",
      "arguments": {
        "id": "1f8ef5cf-44f1-47f1-abd5-cf9d360304a9",
        "type": "create-video"
      }
    }
  }' \
  https://kansas3.8glabs.com/mcp
```

### Expected Response (Working)
```json
{
  "result": {
    "content": [
      {
        "type": "text",
        "text": "{\"data\":{\"job_status\":\"JOB_STATUS_DONE\",\"url\":\"https://storage.googleapis.com/imagineapp-dev-web/media/5/infinitetalk/....mp4\"},\"status\":\"success\"}"
      }
    ],
    "structuredContent": {
      "data": {
        "job_status": "JOB_STATUS_DONE",
        "url": "https://storage.googleapis.com/imagineapp-dev-web/media/5/infinitetalk/....mp4"
      },
      "status": "success"
    }
  },
  "jsonrpc": "2.0",
  "id": 1
}
```

### Current Response (Broken - Missing URL)
```json
{
  "result": {
    "content": [
      {
        "type": "text",
        "text": "{\"data\":{\"job_status\":\"JOB_STATUS_DONE\",\"message\":\"\"},\"status\":\"success\"}"
      }
    ],
    "structuredContent": {
      "data": {
        "job_status": "JOB_STATUS_DONE",
        "message": ""
      },
      "status": "success"
    }
  },
  "jsonrpc": "2.0",
  "id": 1
}
```

---

## Example 2: Fetch a Job That's Still Processing

### Request
```bash
curl -s -X POST \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "fetch-asset",
      "arguments": {
        "id": "YOUR_JOB_ID",
        "type": "create-video"
      }
    }
  }' \
  https://kansas3.8glabs.com/mcp
```

### Response (Processing)
```json
{
  "result": {
    "structuredContent": {
      "data": {
        "job_status": "JOB_STATUS_PROCESSING",
        "progress": 0.45
      },
      "status": "success"
    }
  },
  "jsonrpc": "2.0",
  "id": 1
}
```

---

## Example 3: Pretty Print with jq

```bash
curl -s -X POST \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "fetch-asset",
      "arguments": {
        "id": "1f8ef5cf-44f1-47f1-abd5-cf9d360304a9",
        "type": "create-video"
      }
    }
  }' \
  https://kansas3.8glabs.com/mcp | python3 -m json.tool
```

---

## Example 4: Extract URL Only (if present)

```bash
curl -s -X POST \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "fetch-asset",
      "arguments": {
        "id": "YOUR_JOB_ID",
        "type": "create-video"
      }
    }
  }' \
  https://kansas3.8glabs.com/mcp | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('result',{}).get('structuredContent',{}).get('data',{}).get('url','URL NOT FOUND'))"
```

---

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | Job ID returned from `create-video` call |
| `type` | string | Yes | Asset type: `create-video` |

## Job Status Values

| Status | Description |
|--------|-------------|
| `JOB_STATUS_PENDING` | Job queued, waiting to start |
| `JOB_STATUS_PROCESSING` | Job in progress |
| `JOB_STATUS_DONE` | Job completed successfully |
| `JOB_STATUS_FAILED` | Job failed |

## Notes

⚠️ **Current Issue (2026-03-07):** 
When `job_status` is `JOB_STATUS_DONE`, the response should include a `url` field with the video URL, but recent responses are missing this field.

**Expected:**
```json
{
  "data": {
    "job_status": "JOB_STATUS_DONE",
    "url": "https://storage.googleapis.com/..."
  }
}
```

**Actual (Broken):**
```json
{
  "data": {
    "job_status": "JOB_STATUS_DONE",
    "message": ""
  }
}
```

---

## Test Job IDs (from current batch run)

These jobs show `JOB_STATUS_DONE` but are missing the URL:

```
1f8ef5cf-44f1-47f1-abd5-cf9d360304a9
37b6ac5e-94bc-414b-b4f7-01feec7c2c2f
c8bd9780-5a13-44a9-9c65-2866257458f2
deb53198-bb0c-4029-a542-ca2c113a198f
1884c1fa-ba49-48c7-a5c7-35e53a351531
```
