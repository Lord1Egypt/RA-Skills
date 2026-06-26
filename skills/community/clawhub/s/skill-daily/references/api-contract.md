# ClawHub Convex API 契约

> 真实可用的 API 端点和参数，基于对 ClawHub 主 JS bundle（v6）的分析

## 端点

```
POST https://wry-manatee-359.convex.cloud/api/query
Content-Type: application/json
```

## 函数签名

### `skills:listPublicPageV4`

抓取 Skill 列表（分页）

#### 请求参数

| 参数 | 类型 | 必填 | 默认 | 说明 |
|------|------|------|------|------|
| `numItems` | int | ✅ | 25 | 每页数量，1-200 稳定支持 |
| `cursor` | str | ❌ | null | 翻页游标（首次为空） |
| `sort` | str | ❌ | - | 排序字段 |
| `dir` | str | ❌ | "desc" | `asc` / `desc` |
| `highlightedOnly` | bool | ❌ | false | 仅精选 |
| `capabilityTag` | str | ❌ | - | 能力标签筛选 |
| `categorySlug` | str | ❌ | - | 分类筛选 |
| `categoryKeywords` | str | ❌ | - | 分类关键词 |
| `excludeCategoryKeywords` | str | ❌ | - | 排除关键词 |

#### 排序字段 `sort` 取值

| 值 | 含义 | 备注 |
|---|---|---|
| `"downloads"` | 按总下载量 | 主流榜单 |
| `"installs"` | 按总安装量 | - |
| `"stars"` | 按星标数 | - |
| `"updated"` | 按更新时间 | 新近更新 |
| `"recommended"` | 推荐排序 | ClawHub 算法 |
| `"relevance"` | 相关性 | 仅搜索时有效 |

#### 请求示例

```json
{
  "path": "skills:listPublicPageV4",
  "args": {
    "numItems": 100,
    "sort": "downloads",
    "dir": "desc",
    "highlightedOnly": false
  },
  "format": "json"
}
```

#### 响应格式

```json
{
  "status": "success",
  "value": {
    "page": [Skill, Skill, ...],
    "hasMore": true,
    "nextCursor": "{\"v\":1,\"index\":\"by_active_stats_downloads\",...}"
  }
}
```

#### 翻页机制

- `nextCursor` 是 JSON 字符串，作为下次请求的 `cursor` 参数
- 当 `hasMore: false` 时停止翻页
- 推荐每次 `numItems=50`，翻 4 次 = 200 个

### 完整翻页示例

```python
def fetch_all_skills(num_target=200, sort="downloads"):
    """翻页抓取所有 Skill"""
    page_size = 50
    all_skills = []
    cursor = None

    for i in range(0, num_target, page_size):
        resp = requests.post(
            "https://wry-manatee-359.convex.cloud/api/query",
            json={
                "path": "skills:listPublicPageV4",
                "args": {
                    "numItems": page_size,
                    "cursor": cursor,
                    "sort": sort,
                    "dir": "desc"
                },
                "format": "json"
            },
            headers={
                "Content-Type": "application/json",
                "Origin": "https://clawhub.ai",
                "Referer": "https://clawhub.ai/"
            },
            timeout=20
        )
        data = resp.json()
        if data.get('status') != 'success':
            break
        value = data['value']
        all_skills.extend(value['page'])
        if not value.get('hasMore') or not value.get('nextCursor'):
            break
        cursor = value['nextCursor']

    return all_skills
```

## 错误码

| 错误 | 含义 | 处理 |
|------|------|------|
| `DEPLOYMENT_NOT_FOUND` | 端点 URL 错 | 检查 `wry-manatee-359.convex.cloud` |
| `[Request ID: xxx] Server Error` | 服务端异常 | 重试 3 次，仍失败则跳过 |
| `status != 'success'` | 函数报错 | 检查参数名/类型 |
| HTTP 429 | 限流 | 退避 5 秒后重试 |
| HTTP 5xx | 服务端故障 | 退避 10 秒后重试 |

## 已知限制

1. **无认证**：当前接口公开，无需 token
2. **限流**：单 IP 短时间内大量请求可能被限（建议 ≥ 1 秒间隔）
3. **稳定性**：Convex 服务本身可能有抖动，建议脚本内置重试

## 版本说明

- API 端点版本：Convex Cloud（v1 协议）
- 端点部署：`wry-manatee-359`（2026 年 6 月确认有效）
- 函数版本：`listPublicPageV4`（v4 协议）
