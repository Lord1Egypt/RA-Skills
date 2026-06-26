# `/api/cli` 接口契约

CLI 所有远程请求必须统一访问 `/api/cli/*`。后端可以复用现有服务，但 CLI 不直接访问 `/canvas`、`/run`、`/toolbar-image`。

## 认证

所有需要用户上下文的接口使用：

```http
Authorization: Bearer <ACCESS_KEY>
```

Access Key 由用户在 Web 头像菜单中的 `Access Key` 弹窗创建并复制。

## 接口列表

| 接口 | 说明 |
|------|------|
| `GET /api/cli/models/image?project_id=<id>` | 获取 CLI 可用生图模型 |
| `GET /api/cli/models/video?project_id=<id>` | 获取 CLI 可用视频模型 |
| `POST /api/cli/images/generate` | 提交生图/图生图任务 |
| `POST /api/cli/videos/generate` | 提交视频生成任务 |
| `POST /api/cli/upload` | 上传本地文件获取公开 URL |
| `GET /api/cli/tasks/{task_id}` | 查询标准化任务状态 |
| `POST /api/cli/tasks/{task_id}/settle` | 结算任务 |
| `POST /api/cli/markdown/images/plan` | 生成 Markdown 图片提示词计划 |

## POST /api/cli/upload

上传本地文件到平台 OSS，返回可公开访问的 URL。

- 请求格式：`multipart/form-data`
- 字段：`file`（必填）
- 认证：`Authorization: Bearer <ACCESS_KEY>`
- 文件限制：
  - 图片（`.png`, `.jpg`, `.jpeg`, `.webp`, `.gif`）：最大 20MB
  - 视频（`.mp4`, `.mov`, `.webm`）：最大 100MB
  - 音频（`.mp3`, `.wav`, `.m4a`, `.flac`, `.aac`）：最大 50MB

响应：

```json
{"success": true, "url": "https://xianchou.com/users/cli-uploads/..."}
```

## POST /api/cli/images/generate

提交生图任务。当 `image_urls` 非空时自动切换为图生图模式。

请求体新增字段：

```json
{
  "image_urls": ["https://..."]
}
```

## 错误格式

后端错误应返回 `success: false` 和 `message`。CLI 会优先展示 `message`，其次展示 `detail`。

## 稳定性规则

- 不暴露 Web 前端内部字段作为 CLI 必填字段。
- 任务结果统一输出 `image_urls`，不要让 CLI 解析多种内部结构。
- 模型字段使用 snake_case，便于公开文档保持稳定。
- 新增 CLI 能力时优先扩展 `/api/cli`，不要让 CLI 绕过契约层。
