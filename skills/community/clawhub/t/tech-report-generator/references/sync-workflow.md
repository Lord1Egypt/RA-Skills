# 同步分发流程参考

## IMA 知识库同步

### 目标知识库

- 名称：「龙虾-模型ScalingUp」
- kb_id: `6peD1tTQj2UYi41MTaDgLpfVnbCegcA-sjzZLJ0zVPA=`

### 完整流程

```bash
# Step 1: 获取 IMA 凭证
CLIENT_ID=$(cat ~/.config/ima/client_id)
API_KEY=$(cat ~/.config/ima/api_key)

# Step 2: Preflight Check（验证连接）
curl -s "https://api.ima.qq.com/open/knowledge/check" \
  -H "client_id: $CLIENT_ID" \
  -H "api_key: $API_KEY"

# Step 3: 检查重名（避免重复上传）
curl -s "https://api.ima.qq.com/open/knowledge/check_repeated_names" \
  -H "client_id: $CLIENT_ID" \
  -H "api_key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"kb_id": "KB_ID", "names": ["文件名.md"]}'

# Step 4: 创建媒体（获取上传凭证）
curl -s "https://api.ima.qq.com/open/knowledge/create_media" \
  -H "client_id: $CLIENT_ID" \
  -H "api_key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"kb_id": "KB_ID", "file_name": "文件名.md", "file_size": FILE_SIZE}'
# 返回: upload_url, media_key

# Step 5: 上传文件到 COS
curl -s -X PUT "$UPLOAD_URL" \
  -H "Content-Type: text/markdown" \
  --data-binary @文件路径.md

# Step 6: 完成入库
curl -s "https://api.ima.qq.com/open/knowledge/add_knowledge" \
  -H "client_id: $CLIENT_ID" \
  -H "api_key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"kb_id": "KB_ID", "media_key": "MEDIA_KEY", "file_name": "文件名.md"}'
```

### 注意事项

- 上传文件使用 **Markdown 版本**（便于知识库索引和检索）
- 文件名建议包含日期：`{技术名称}技术报告_{YYYY-MM-DD}.md`
- 若 check_repeated_names 返回有重复，先确认是否需要更新版本

## 腾讯文档同步

### 方式一：智能文档（推荐）

使用 MCP 工具 `mcp__tencent-docs__create_smartcanvas_by_mdx`：

```json
{
  "title": "报告标题",
  "mdx": "Markdown 正文内容",
  "content_format": "markdown"
}
```

优点：
- 自动格式化，支持标题/表格/列表
- 文档可在线协作编辑

限制：
- SVG 图示无法直接渲染（建议在文档中添加 HTML 版本链接）
- 超大表格可能需要调整

### 方式二：HTML 导入（保留图示）

流程：
1. `mcp__tencent-docs__manage.pre_import` — 预导入获取上传 URL
2. `curl -X PUT` 上传 HTML 文件到 COS
3. `mcp__tencent-docs__manage.async_import` — 触发异步导入
4. 轮询 `mcp__tencent-docs__manage.import_progress` 直到完成

优点：
- 保留 HTML 排版和 SVG 图示

限制：
- 编辑能力受限（导入后为文档格式）
- 复杂 CSS 可能丢失

### 输出提示

同步完成后，输出格式：

```
✅ 已同步至 IMA 知识库「龙虾-模型ScalingUp」
✅ 已同步至腾讯文档：https://docs.qq.com/xxx?_fid=YYY
```

注意：腾讯文档链接必须追加 `?_fid=<file_id>` 参数。
