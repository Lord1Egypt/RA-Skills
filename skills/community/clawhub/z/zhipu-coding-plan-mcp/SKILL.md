---
name: zhipu-coding-plan-mcp
description: 智谱 AI 视觉、搜索与生图工具集 — 图像分析、OCR 文字提取、错误截图诊断、UI 截图转代码、技术图表解读、数据可视化分析、视频理解、UI 差异对比、联网搜索、网页读取、GitHub 仓库检索、AI 生图（CogView）、AI 生视频（CogVideoX）。共 4 个 MCP Server、13 个工具 + CogView-3-Plus 生图 API + CogVideoX 视频生成 API。
version: 1.3.0
read_when:
  - 智谱
  - MCP
  - 图像分析
  - 图片识别
  - 截图
  - OCR
  - 文字提取
  - 错误诊断
  - UI 转代码
  - 视频分析
  - 视频理解
  - 技术图表
  - 架构图
  - 流程图
  - UML
  - 数据可视化
  - 图表分析
  - UI 对比
  - UI 差异
  - 联网搜索
  - 网络搜索
  - 网页读取
  - 网页抓取
  - GitHub 仓库
  - 仓库检索
  - 代码搜索
  - 生图
  - 画图
  - AI生图
  - CogView
  - 生成图片
  - 生视频
  - 视频生成
  - AI视频
  - CogVideoX
metadata:
  openclaw:
    requires:
      bins:
        - npx
    emoji: "🔮"
    homepage: https://open.bigmodel.cn
---

# 智谱 MCP 工具集

## API Key 与调用方式

所有工具共用同一个 API Key，从 `~/.openclaw/agents/main/agent/auth-profiles.json` 的 `profiles."zai:default".key` 动态读取。绝对不要硬编码 API Key。

调用统一通过 `scripts/zai-mcp.js`，它会自动读取 API Key 并设置环境变量：

```bash
ZAI=~/.openclaw/workspace/skills/zhipu-coding-plan-mcp/scripts/zai-mcp.js
node $ZAI call <server>.<tool> --args '{...}'
```

CogView 等直接 HTTP 调用场景，动态获取 Key：
```bash
API_KEY=$(jq -r '.profiles."zai:default".key' ~/.openclaw/agents/main/agent/auth-profiles.json)
```

---

## 工具概览

| Server | 工具 | 说明 |
|--------|------|------|
| zai-mcp-server | analyze_image | 通用图像分析与理解 |
| | analyze_video | 视频内容分析（MP4/MOV/M4V，≤8MB） |
| | ui_to_artifact | UI 截图转代码/提示词/设计规范/描述 |
| | extract_text_from_screenshot | 截图 OCR 文字提取 |
| | diagnose_error_screenshot | 错误截图诊断与修复建议 |
| | understand_technical_diagram | 技术图表理解（架构图/流程图/UML/ER 图） |
| | analyze_data_visualization | 数据可视化图表分析与洞察 |
| | ui_diff_check | 两张 UI 截图差异对比 |
| web-search-prime | web_search_prime | 全网搜索，支持域名过滤、时间范围 |
| web-reader | webReader | 网页抓取转 Markdown/Text |
| zread | search_doc | 搜索 GitHub 仓库文档/Issue/Commit |
| | read_file | 读取仓库中指定文件 |
| | get_repo_structure | 获取仓库目录结构 |


> ⚠️ `analyze_image` 和 `analyze_video` 响应较慢（30-120s），调用时 timeout 建议 ≥180s，视频 ≥300s。

---

## 调用示例

以下示例中 `$ZAI` 代表脚本完整路径，实际使用时替换为：
`~/.openclaw/workspace/skills/zhipu-coding-plan-mcp/scripts/zai-mcp.js`

### 视觉理解（zai-mcp-server）

```bash
# 通用图像分析
node $ZAI call zai-mcp-server.analyze_image \
  --args '{"image_source": "https://example.com/image.png", "prompt": "描述图片内容"}'

# 视频理解
node $ZAI call zai-mcp-server.analyze_video \
  --args '{"video_source": "https://example.com/video.mp4", "prompt": "描述视频中发生了什么"}'

# UI 截图转代码
node $ZAI call zai-mcp-server.ui_to_artifact \
  --args '{"image_source": "./screenshot.png", "output_type": "code", "prompt": "用 React 实现这个界面"}'

# OCR 文字提取
node $ZAI call zai-mcp-server.extract_text_from_screenshot \
  --args '{"image_source": "./code_screenshot.png", "prompt": "提取截图中的代码", "programming_language": "python"}'

# 错误截图诊断
node $ZAI call zai-mcp-server.diagnose_error_screenshot \
  --args '{"image_source": "./error.png", "prompt": "帮我分析这个报错", "context": "执行 npm install 时出现"}'

# 技术图表理解
node $ZAI call zai-mcp-server.understand_technical_diagram \
  --args '{"image_source": "./architecture.png", "prompt": "解释这个架构图的组件关系", "diagram_type": "architecture"}'

# 数据可视化分析
node $ZAI call zai-mcp-server.analyze_data_visualization \
  --args '{"image_source": "./chart.png", "prompt": "分析这个图表的趋势", "analysis_focus": "trends"}'

# UI 差异对比
node $ZAI call zai-mcp-server.ui_diff_check \
  --args '{"expected_image_source": "./design.png", "actual_image_source": "./implementation.png", "prompt": "找出设计稿和实现的差异"}'
```

### 联网搜索与网页读取

```bash
# 网络搜索
node $ZAI call web-search-prime.web_search_prime \
  --args '{"search_query": "最新 Node.js 版本", "search_recency_filter": "oneWeek", "content_size": "high", "location": "cn"}'

# 网页内容抓取
node $ZAI call web-reader.webReader \
  --args '{"url": "https://example.com", "return_format": "markdown", "timeout": 30, "retain_images": true}'
```

### GitHub 仓库检索（zread）

```bash
# 文档搜索
node $ZAI call zread.search_doc --args '{"repo_name": "vitejs/vite", "query": "如何配置代理"}'

# 读取文件
node $ZAI call zread.read_file --args '{"repo_name": "vitejs/vite", "file_path": "src/index.ts"}'

# 仓库结构
node $ZAI call zread.get_repo_structure --args '{"repo_name": "vitejs/vite"}'
```

### AI 生图（CogView-3-Plus，HTTP API）

不走 MCP，直接 HTTP 调用：

```bash
API_KEY=$(jq -r '.profiles."zai:default".key' ~/.openclaw/agents/main/agent/auth-profiles.json)
curl -s https://open.bigmodel.cn/api/paas/v4/images/generations \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "cogview-3-plus", "prompt": "一只在草地上晒太阳的小猫，水彩画风格"}' \
  | jq -r '.data[0].url'
```

支持尺寸：1024x1024（默认）、768x1344、864x1152、1344x768、1152x864、1440x720、720x1440。返回 URL 有效期约 1 小时。

### AI 生视频（CogVideoX，HTTP API，异步）

不走 MCP，直接 HTTP 异步调用，分两步：

**Step 1 — 提交生成任务：**

```bash
API_KEY=$(jq -r '.profiles."zai:default".key' ~/.openclaw/agents/main/agent/auth-profiles.json)

# 文本生成视频
curl -s https://open.bigmodel.cn/api/paas/v4/videos/generations \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "cogvideox-flash",
    "prompt": "一只可爱的小猫在草地上追蝴蝶，阳光明媚，卡通风格",
    "size": "1280x720",
    "fps": 30
  }' | jq .
# 返回 {"id": "...", "task_status": "PROCESSING"}

# 图像生成视频（image_url + prompt 至少传一个）
curl -s https://open.bigmodel.cn/api/paas/v4/videos/generations \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "cogvideox-flash",
    "image_url": "https://example.com/photo.jpg",
    "prompt": "让画面动起来",
    "size": "1280x720"
  }' | jq .
```

**Step 2 — 轮询查询结果：**

```bash
TASK_ID="<上一步返回的 id>"
curl -s "https://open.bigmodel.cn/api/paas/v4/async-result/$TASK_ID" \
  -H "Authorization: Bearer $API_KEY" | jq .
# task_status: "PROCESSING" → 继续等待（约 1-3 分钟）
# task_status: "SUCCESS"  → video_result[0].url 为视频地址，video_result[0].cover_image_url 为封面
# task_status: "FAIL"     → 生成失败
```

**可用模型：** `cogvideox-flash`（免费）

**参数说明：**

- `prompt`：视频描述，≤512 字符（`image_url` 和 `prompt` 不能同时为空）
- `image_url`：可选，图片 URL 或 Base64（支持 png/jpeg/jpg，≤5MB）
- `size`：720x480、960x1280、1024x1024、1280x720、1280x960、720x1280、1920x1080、1080x1920、2048x1080
- `fps`：30（默认）

**一键脚本（提交 + 轮询 + 下载）：**

```bash
API_KEY=$(jq -r '.profiles."zai:default".key' ~/.openclaw/agents/main/agent/auth-profiles.json)
PROMPT="一只可爱的小猫在草地上追蝴蝶，阳光明媚"
MODEL="cogvideox-flash"
SIZE="1280x720"
OUT="/root/.openclaw/workspace/downloads/video.mp4"

# 提交任务
TASK_ID=$(curl -s https://open.bigmodel.cn/api/paas/v4/videos/generations \
  -H "Authorization: Bearer $API_KEY" -H "Content-Type: application/json" \
  -d "{\"model\":\"$MODEL\",\"prompt\":\"$PROMPT\",\"size\":\"$SIZE\"}" | jq -r '.id')
echo "Task: $TASK_ID"

# 轮询等待（间隔20秒，最多30次=10分钟）
for i in $(seq 1 30); do
  STATUS=$(curl -s "https://open.bigmodel.cn/api/paas/v4/async-result/$TASK_ID" \
    -H "Authorization: Bearer $API_KEY" | jq -r '.task_status')
  echo "[$i] $STATUS"
  if [ "$STATUS" = "SUCCESS" ]; then
    VIDEO_URL=$(curl -s "https://open.bigmodel.cn/api/paas/v4/async-result/$TASK_ID" \
      -H "Authorization: Bearer $API_KEY" | jq -r '.video_result[0].url')
    curl -sL -o "$OUT" "$VIDEO_URL"
    echo "Done: $OUT ($(du -h $OUT | cut -f1))"
    break
  elif [ "$STATUS" = "FAIL" ]; then
    echo "Failed!"; break
  fi
  sleep 20
done
```

---

## 常见问题

- **连接失败**：检查 API Key 配置、网络连接、工具名称拼写
- **参数错误**：`node $ZAI list <工具名称> --schema` 查看支持的参数
- **视觉/视频超时**：加大 timeout（≥180s，视频 ≥300s）重试即可
- **权限问题**：确认 `mcporter.json` 存在、auth-profiles.json 中有有效 Key、当前用户有读写权限
- **视频生成查询路径**：异步查询用 `/paas/v4/async-result/{id}`，不是 `/paas/v4/videos/generations/{id}`
- **视频 URL 有效期**：返回的视频/封面 URL 有效期约 24 小时，请及时下载

_最后更新: 2026-04-03_
