# RapidDNS API Reference

Base URL: `https://rapiddns.io`

## Authentication

Header: `X-API-KEY: rdns_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

Get key at: https://rapiddns.io/user/profile (Pro/Max required)

## Endpoints

### GET /api/search/{keyword}

Keyword search (domain, IP, or CIDR).

**Params:** `page`, `pagesize`, `search_type` (subdomain|same_domain|ip|ip_segment)

**Response:**
```json
{
  "status": "ok",
  "data": {
    "total": 45,
    "data": [
      {"type":"A","value":"1.2.3.4","subdomain":"www.example.com","timestamp":"...","date":"..."}
    ]
  }
}
```

### GET /api/search/query/{query}

Advanced query (Elasticsearch query_string syntax).

**Fields:** domain (2nd-level only, e.g. "baidu" NOT "baidu.com"), tld, subdomain, value, type, is_root

### POST /api/export-data

Create export task. Params: `query_type`, `query_input`, `max_results`, `compress`

### GET /api/export-data/{task_id}

Check export status (pending → processing → completed → failed).

### GET /api/export-data/{task_id}/download

Get temporary download URL.

### GET /api/fdns/list

List FDNS datasets (Max only).

### POST /api/fdns/download

Generate FDNS dataset download link (Max only).

## Error Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad parameters |
| 401 | Invalid/expired token |
| 403 | Insufficient permissions |
| 404 | Not found |
| 429 | Rate limit |
| 5xx | Server error |
