# 699pic OpenAPI MCP

本 Skill 对接本地已注册的 `st-mcp` MCP server。

使用前先确认你自己的本地环境，而不是复用其他用户目录或预配置：

- `mcporter` 是否已安装并可执行
- `st-mcp` 是否已经在本机注册
- MCP 注册配置里的命令、参数、环境变量、权限是否经过审核
- `SERVICE_API_KEY` / `SERVICE_API_BASE_URL` 是否来自你的环境配置
- `scripts/openapi.js` 是否已审阅，且你确认它会向目标服务发送带 `x-api-key` 头的 `POST` 请求
- 不要使用来源不明或共享的 API key

服务通过 `mcporter` 注册名：

- `st-mcp`

可用 tools：

- `search_photos`
- `search_videos`
- `download_asset`
- `get_download_records`
- `check_downloaded`

## 建议用法

- 先搜索，再给出候选结果
- 搜索结果默认输出为 Markdown 图片文档，不要只给裸链接
- 如果 `preview_url` / `thumbnail_url` 以 `//` 开头，补成 `https://` 后再用于 Markdown 图片
- 下载前确认 `asset_type` 与 `id`
- 若要判断企业是否已下载，先调用 `check_downloaded`
- 若用户要查历史下载记录，调用 `get_download_records`

## 常用 mcporter 示例

```bash
mcporter list st-mcp --schema
mcporter call st-mcp.search_photos keywords=春节 limit=10 --output json
mcporter call st-mcp.search_videos keywords=城市航拍 limit=10 --output json
mcporter call st-mcp.check_downloaded content_id=123456 type=1 --output json
```
