# 星辰 AI 顾客生图 API

## 环境变量

```text
XINGCHEN_API_BASE_URL=https://your-xingchen-domain.example
XINGCHEN_API_KEY=xk_live_...
```

本地开发可以把 `XINGCHEN_API_BASE_URL` 指向 `http://127.0.0.1:8000`。生产环境必须使用 HTTPS。API 密钥只对 `/api/generate` 和 `/api/jobs/*` 生效；`/api/assets/upload` 仍需要网站登录会话，因此 OpenClaw skill 不负责上传本地文件。

## 提交生成任务

`POST /api/generate`

请求头：

```http
Content-Type: application/json
X-Xingchen-API-Key: xk_live_...
X-Xingchen-Response-Mode: compact
```

### curl

```bash
curl -sS -X POST "$XINGCHEN_API_BASE_URL/api/generate" \
  -H "Content-Type: application/json" \
  -H "X-Xingchen-API-Key: $XINGCHEN_API_KEY" \
  -H "X-Xingchen-Response-Mode: compact" \
  --data @request.json
```

### PowerShell

```powershell
$headers = @{
  "X-Xingchen-API-Key" = $env:XINGCHEN_API_KEY
  "X-Xingchen-Response-Mode" = "compact"
}
$body = Get-Content .\request.json -Raw
Invoke-RestMethod -Uri "$env:XINGCHEN_API_BASE_URL/api/generate" -Method Post -Headers $headers -ContentType "application/json" -Body $body
```

最小文字生图请求：

```json
{
  "clientRequestId": "oclaw-20261006-001",
  "cost": 5,
  "record": {
    "id": "oclaw-20261006-001",
    "title": "红色连衣裙商品图",
    "toolPath": "/studio/image",
    "prompt": "一件红色连衣裙，纯净浅色背景，电商商品主图，柔和棚拍光线",
    "count": 1,
    "ratio": "1:1",
    "quality": "1K"
  }
}
```

`cost` 仅是客户端报价字段，服务端会按账户、工作流、质量和数量重新计算，不能用它绕过扣点。对不确定价格的调用可以省略该字段。

字段约定：`clientRequestId` 用于幂等重试；`record.id` 是客户端记录标识；`record.toolPath` 选择网站工作流；`record.prompt` 是用户需求；`record.count` 是生成数量；`record.ratio` 是画面比例；`record.quality` 是质量档位。除这些字段外，不要凭空添加未在当前契约中说明的 provider 专用字段。

参考图字段应使用已经在网站上传并已得到可访问 URL 的素材，例如：

```json
{
  "record": {
    "toolPath": "/studio/image",
    "prompt": "保留商品外观，生成高级电商场景图",
    "count": 1,
    "primaryAssets": [
      { "url": "https://cdn.example.com/reference/product.jpg" }
    ]
  }
}
```

实际可用的素材字段以站点当前生成契约为准；不要在请求中发送 `data:image/...;base64`。顾客 API skill 当前不能自行上传本地文件。

## 网站工作流映射

| 用户意图 | `record.toolPath` | 素材要求 |
| --- | --- | --- |
| 普通商品图、场景图、海报 | `/studio/image` 或 `/studio/ai-poster` | 可无素材 |
| 爆款构图复用 | `/studio/hot-remake` | 需要参考设计图，通常还需要商品图 |
| 局部替换、扩图、去水印、高清修复 | 对应 `/studio/local-crop` 或 `/studio/retouch/*` | 需要原图，局部编辑还需要明确目标 |
| AI 试衣、换装、背景、姿势 | 对应 `/studio/ai-model/*` | 需要与该工作流匹配的服装/模特素材 |

提示词只描述当前任务和用户要求。参考图的角色通过 `primaryAssets`、`secondaryAssets` 和 `role` 表达，不要把上传图 URL 拼进 prompt。

## 响应与轮询

成功响应通常包含 `ok: true`、`points`、`job` 和 `record`。优先使用 `job.id` 或 `job.jobId`：

```http
GET /api/jobs/{jobId}
X-Xingchen-API-Key: xk_live_...
X-Xingchen-Response-Mode: compact
```

终态包括 `succeeded`、`done`、`failed`、`partial`。成功结果通常位于：

```text
record.outputs[].preview
record.outputs[].url
record.assets.outputs[].preview
record.assets.outputs[].url
```

展示时优先 `preview` 或 `thumbnailUrl`，下载时再使用 `url`。

### curl

```bash
curl -sS "$XINGCHEN_API_BASE_URL/api/jobs/$JOB_ID" \
  -H "X-Xingchen-API-Key: $XINGCHEN_API_KEY" \
  -H "X-Xingchen-Response-Mode: compact"
```

### PowerShell

```powershell
$headers = @{
  "X-Xingchen-API-Key" = $env:XINGCHEN_API_KEY
  "X-Xingchen-Response-Mode" = "compact"
}
Invoke-RestMethod -Uri "$env:XINGCHEN_API_BASE_URL/api/jobs/$env:JOB_ID" -Method Get -Headers $headers
```

## 常见错误

| HTTP / error | 处理 |
| --- | --- |
| 401 / `unauthenticated` | 检查密钥是否配置、是否已撤销；不要重试提交，也不要把密钥放进错误消息 |
| 400 / `payload_too_large` | 减少参考图或先压缩上传；任务未创建 |
| 400 / `generation_contract_failed` | 修正 prompt、比例、数量或素材字段 |
| 402 / 点数不足 | 告知用户充值或减少数量；不要自动扣款 |
| 404 / `job_not_found` | 检查任务 ID；不要换 ID 重提 |
| 502/503 | 保留原 `clientRequestId`，等待后查询原任务状态 |

## 安全与权限边界

- 只从环境变量读取 `XINGCHEN_API_KEY`；不要把它写入 prompt、请求体、日志、截图、生成记录或公开链接。
- 顾客密钥只用于本文件列出的生成提交和任务查询；不要尝试用它访问账户、充值、支付、推广或后台接口。
- `cost` 不是授权凭证，也不是最终价格；服务端重新计算扣点，客户端不得借此降低费用。
- 网络失败时用相同的 `clientRequestId` 查询原任务，避免重复提交和重复扣点。
- 401、密钥撤销、权限不足时停止调用并提示用户到账户中心重新生成密钥；不要反复重试。
- 只展示缩略图或预览字段，原图 URL 仅用于用户明确要求的查看或下载。
