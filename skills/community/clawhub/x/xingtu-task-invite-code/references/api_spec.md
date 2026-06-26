# XingTu API Reference

## provider_get_task_order_list

获取星图招募任务订单列表。

### Request

```
POST https://www.xingtu.cn/gw/api/task/provider_get_task_order_list
```

### Headers

| Header | Value |
|--------|-------|
| Accept | application/json, text/plain, */* |
| Content-Type | application/json |
| agw-js-conv | str |
| Cookie | {{session_cookie}} |
| User-Agent | Apifox/1.0.0 (https://apifox.com) |
| Host | www.xingtu.cn |
| Accept-Charset | UTF-8 |
| Accept-Encoding | gzip, deflate |

### Request Body

```json
{
    "page": 1,
    "limit": 10,
    "query": {
        "order_status": [2],
        "task_category_list": [133],
        "pay_type_list": [3, 4, 12]
    }
}
```

| Field | Type | Description |
|-------|------|-------------|
| page | int | Page number, starting from 1 |
| limit | int | Items per page (fixed at 10) |
| query.order_status | int[] | Order status filter. `[2]` = 已发布/进行中 |
| query.task_category_list | int[] | Task category. `[133]` = 招募任务 |
| query.pay_type_list | int[] | Payment type filter. `[3, 4, 12]` covers common pay types |

### Response

Expected successful response (HTTP 200):

```json
{
    "code": 0,
    "data": {
        "list": [
            {
                "task_id": "7644105920513261594",
                "task_name": "...",
                ...
            }
        ],
        "total": 25,
        "page": 1,
        "limit": 10
    }
}
```

| Field | Type | Description |
|-------|------|-------------|
| code | int | 0 = success |
| data.list | array | Array of task objects |
| data.total | int | Total number of matching tasks |
| data.page | int | Current page number |

### Error Responses

| Status | Meaning | Action |
|--------|---------|--------|
| 302 | Redirect to login | Cookie expired, re-authenticate |
| 401 | Unauthorized | Cookie invalid, re-authenticate |
| 200 + code != 0 | Business error | Check error message, may need different query params |

---

## Task Detail Page

URL pattern: `https://www.xingtu.cn/provider/pages/recruit/management/{{task_id}}`

### Required Browser Interactions

The detail page requires three sequential clicks:

1. **邀约达人** — Button/link on the task detail page. Triggers the invitation flow.
2. **二维码邀请** — Option within the invitation modal. Opens the QR code generation dialog.
3. **下载图片** — Download button within the QR code modal. Triggers browser download of the QR code PNG image.

### Cookie Format

Cookies from XingTu typically include these keys:
- `sessionid`
- `sso_uid_tt`
- `sso_uid_tt_ss`
- `sid_guard`
- `uid_tt`
- `uid_tt_ss`
- `sid_tt`

Format for storage: `key1=value1; key2=value2; key3=value3`

Format for HTTP Cookie header: same as above.

---

## Login Flow

Login URL: `https://sso.oceanengine.com/xingtu/login?role=7`

After successful login, the browser is redirected to the XingTu main site (`www.xingtu.cn`). All authentication cookies are set on the `.xingtu.cn` domain.

### Cookie File Location

```
C:\Users\majin\.xingtuCookie.txt
```

Plain text file containing the full Cookie header string on a single line.
