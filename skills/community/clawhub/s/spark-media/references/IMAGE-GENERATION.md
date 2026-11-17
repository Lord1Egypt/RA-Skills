# 图片生成与编辑

## 文生图

`POST /api/v1/spark-media/image`

| 字段 | 约束 |
|---|---|
| `prompt` | 必填，最多 8000 字符 |
| `width`、`height` | 可选，各 512–4096 |
| `count` | 可选，1–4 |

## 图生图

`POST /api/v1/spark-media/image/edit`

除 `prompt`、`width`、`height` 外，必须提供 JSON `image`（兼容单图）或 `images`（1–5 张有序参考图数组），两者二选一，不可同时提供。每项必须是完整的 PNG、JPEG 或 WebP `data:` URL，例如 `data:image/png;base64,...`；不是 multipart 文件或公网 URL。

每张解码后最大 5 MB（5242880 bytes）、16777216 像素，全部参考图解码后总计最大 20 MB（20971520 bytes）。多图共同参考生成同一个作品，不会逐张创建任务；可在提示词中写“保留图 1 主体，使用图 2 场景”。模型支持范围须与平台部署配置匹配。

异步图生图使用 `POST /api/v1/spark-media/image/edit/async`，接受相同图片输入；HTTP 202 返回 `id`、`status`、`billing`，使用原 Key 查询 `GET /api/v1/spark-media/image/edit/async/{id}`。异步图生图不接收 `count`。

图片费用按生成张数计算，与输入参考图张数无关。重试须保留全部图片内容、顺序和生成参数；更换或重排图片不能复用同一幂等键。

两个接口都要求：

```text
Authorization: Bearer ...
Idempotency-Key: 每个新逻辑请求的唯一值
Content-Type: application/json
```

保持用户要求的主体、构图、文字和风格。编辑图片时以用户提供的原图为事实来源；不要为了
下载、改名、移动或再次展示结果而重新调用生成接口。响应中的媒体字段由上游模型决定，
应解析并持久化实际返回内容；不要假设始终是某一种 URL 结构，也不要在聊天中输出完整
base64。
