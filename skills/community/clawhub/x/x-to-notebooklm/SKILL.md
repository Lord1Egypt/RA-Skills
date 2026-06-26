---
name: x-to-notebooklm
description: |
  中文：将 X (Twitter) 文章解析并上传到 NotebookLM。使用 r.jina.ai 抓取内容，自动创建 Notebook 并上传文章。
  English: Parse X (Twitter) articles and upload to NotebookLM. Uses r.jina.ai to fetch content, automatically creates notebooks and uploads articles.
---

# X to NotebookLM / X 文章转 NotebookLM

## Overview / 概述

**English:** Quickly parse X (Twitter) articles and upload to Google NotebookLM for deep reading and analysis.

**中文：** 快速解析 X (Twitter) 文章并上传到 Google NotebookLM，便于深度阅读和分析。

---

## Dependencies / 依赖项

**English:**
- **r.jina.ai** - Free web content extraction service (no API key required)
- **NotebookLM CLI** - Installed and authenticated (run `notebooklm login` to authenticate)
- **Node.js** - Script runtime environment

**中文：**
- **r.jina.ai** - 免费的网页内容提取服务（无需 API Key）
- **NotebookLM CLI** - 已安装并认证（运行 `notebooklm login` 完成认证）
- **Node.js** - 运行脚本环境

---

## Usage / 使用方法

### Basic Usage / 基本用法

**English:**
```bash
# Run from workspace root
node ~/.openclaw/workspace/skills/x-to-notebooklm/scripts/x-to-notebooklm.mjs <X_Article_URL>

# Example
node ~/.openclaw/workspace/skills/x-to-notebooklm/scripts/x-to-notebooklm.mjs "https://x.com/elonmusk/status/1234567890"
```

**中文：**
```bash
# 从工作区根目录运行
node ~/.openclaw/workspace/skills/x-to-notebooklm/scripts/x-to-notebooklm.mjs <X 文章 URL>

# 示例
node ~/.openclaw/workspace/skills/x-to-notebooklm/scripts/x-to-notebooklm.mjs "https://x.com/elonmusk/status/1234567890"
```

### Advanced Usage / 高级用法

**English:**
```bash
# Specify notebook name
node ~/.openclaw/workspace/skills/x-to-notebooklm/scripts/x-to-notebooklm.mjs <URL> --notebook-name "X Articles"

# Use existing notebook
node ~/.openclaw/workspace/skills/x-to-notebooklm/scripts/x-to-notebooklm.mjs <URL> --notebook-id <existing_notebook_id>

# Verbose output mode
node ~/.openclaw/workspace/skills/x-to-notebooklm/scripts/x-to-notebooklm.mjs <URL> --verbose
```

**中文：**
```bash
# 指定 Notebook 名称
node ~/.openclaw/workspace/skills/x-to-notebooklm/scripts/x-to-notebooklm.mjs <URL> --notebook-name "X Articles"

# 使用现有 Notebook
node ~/.openclaw/workspace/skills/x-to-notebooklm/scripts/x-to-notebooklm.mjs <URL> --notebook-id <existing_notebook_id>

# 详细输出模式
node ~/.openclaw/workspace/skills/x-to-notebooklm/scripts/x-to-notebooklm.mjs <URL> --verbose
```

---

## Workflow / 工作流程

**English:**
1. **Fetch Content** - Use `curl + r.jina.ai` to extract plain text from X articles
2. **Create Notebook** - Automatically create a new NotebookLM Notebook (or reuse existing)
3. **Upload Article** - Upload parsed content as Source to Notebook
4. **Verify** - Check upload status and return Notebook ID and Source ID

**中文：**
1. **抓取内容** - 使用 `curl + r.jina.ai` 提取 X 文章的纯文本内容
2. **创建 Notebook** - 自动创建新的 NotebookLM Notebook（或复用现有的）
3. **上传文章** - 将解析后的内容作为 Source 上传到 Notebook
4. **验证效果** - 检查上传状态并返回 Notebook ID 和 Source ID

---

## Output Example / 输出示例

**English:**
```
✅ X article parsed and uploaded successfully

📄 Title: Elon Musk on X: "..."
🔗 URL: https://x.com/elonmusk/status/1234567890
📓 Notebook ID: notebook_abc123
📝 Source ID: source_xyz789
📊 Status: Processing complete
```

**中文：**
```
✅ X 文章解析上传成功

📄 文章标题：Elon Musk on X: "..."
🔗 原始链接：https://x.com/elonmusk/status/1234567890
📓 Notebook ID: notebook_abc123
📝 Source ID: source_xyz789
📊 解析状态：已处理完成
```

---

## Configuration / 配置要求

### Environment Variables / 环境变量（可选）

**English:**
```bash
# Default notebook name (if --notebook-name not specified)
export NOTEBOOKLM_DEFAULT_NOTEBOOK="X Articles"

# Verbose mode
export X_TO_NOTEBOOKLM_VERBOSE=true
```

**中文：**
```bash
# 默认 Notebook 名称（如不指定 --notebook-name）
export NOTEBOOKLM_DEFAULT_NOTEBOOK="X Articles"

# 详细模式
export X_TO_NOTEBOOKLM_VERBOSE=true
```

### NotebookLM Authentication / NotebookLM 认证

**English:**
Authenticate before first use:
```bash
# Login using NotebookLM CLI
node ~/.openclaw/skills/tiangong-notebooklm-cli/scripts/notebooklm.mjs login
```

**中文：**
首次使用前需要认证：
```bash
# 使用 NotebookLM CLI 登录
node ~/.openclaw/skills/tiangong-notebooklm-cli/scripts/notebooklm.mjs login
```

---

## Troubleshooting / 故障排除

### Common Issues / 常见问题

**Q: "NotebookLM CLI not authenticated" error / 提示 "NotebookLM CLI not authenticated"**

**English:**
```bash
# Run login command
node ~/.openclaw/skills/tiangong-notebooklm-cli/scripts/notebooklm.mjs login
```

**中文：**
```bash
# 运行登录命令
node ~/.openclaw/skills/tiangong-notebooklm-cli/scripts/notebooklm.mjs login
```

---

**Q: r.jina.ai cannot access X article / r.jina.ai 无法访问 X 文章**

**English:**
- Check if URL is correct
- X articles may require login to access
- Try using a logged-in browser session
- **Note**: Most X (Twitter) content now requires login; r.jina.ai may not be able to fetch content requiring login
- **Alternative**: Use browser tool with logged-in browser session

**中文：**
- 检查 URL 是否正确
- X 文章可能需要登录才能访问
- 尝试使用已登录的浏览器会话
- **注意**：X (Twitter) 大部分内容现在需要登录，r.jina.ai 可能无法抓取需要登录的内容
- **替代方案**：使用 browser 工具配合已登录的浏览器会话

---

**Q: Script execution timeout / 脚本执行超时**

**English:**
- Increase timeout: add `--timeout 60` parameter
- Check network connection

**中文：**
- 增加超时时间：添加 `--timeout 60` 参数
- 检查网络连接

---

**Q: Source ID shows "pending" / Source ID 显示为 "pending"**

**English:**
- This is normal; NotebookLM is processing the uploaded content
- Wait a few minutes and check in NotebookLM interface

**中文：**
- 这是正常现象，NotebookLM 正在处理上传的内容
- 等待几分钟后在 NotebookLM 界面中查看

---

## X Article Fetching Limitations / X 文章抓取限制

**English:**
Due to stricter access restrictions implemented by X (Twitter) after 2023:

- ✅ **Public articles** - r.jina.ai can fetch
- ⚠️ **Articles requiring login** - r.jina.ai cannot fetch
- 💡 **Solution** - Use browser tool with logged-in browser session, or manually copy content

**中文：**
由于 X (Twitter) 在 2023 年后实施了更严格的访问限制：

- ✅ **公开文章** - r.jina.ai 可以抓取
- ⚠️ **需要登录的文章** - r.jina.ai 无法抓取
- 💡 **解决方案** - 使用 browser 工具配合已登录的浏览器会话，或手动复制内容

---

## Test Results / 测试结果

**English:**
- **Test Time**: 2026-03-07 23:46 (Beijing Time)
- **Test URL**: https://github.com/openclaw/openclaw
- **Result**: ✅ Success

```
📓 Notebook ID: 6367c115-bcfa-42f3-b174-456df3537122
📝 Source ID: 658c3733-a02f-4b08-ae16-fc06475d1c19
📊 Status: processed
```

**中文：**
- **测试时间**: 2026-03-07 23:46 (北京时间)
- **测试 URL**: https://github.com/openclaw/openclaw
- **测试结果**: ✅ 成功

```
📓 Notebook ID: 6367c115-bcfa-42f3-b174-456df3537122
📝 Source ID: 658c3733-a02f-4b08-ae16-fc06475d1c19
📊 解析状态：processed
```

---

## Related Files / 相关文件

**English:**
- Main script: `scripts/x-to-notebooklm.mjs`
- Metadata: `_meta.json`
- NotebookLM CLI docs: `~/.openclaw/skills/tiangong-notebooklm-cli/references/cli-commands.md`

**中文：**
- 主脚本：`scripts/x-to-notebooklm.mjs`
- 元数据：`_meta.json`
- NotebookLM CLI 文档：`~/.openclaw/skills/tiangong-notebooklm-cli/references/cli-commands.md`

---

## Version History / 版本历史

**English:**
- **v1.1.0** (2026-03-12) - Add Chinese-English bilingual support
- **v1.0.0** (2026-03-07) - Initial release
  - Support X article fetching
  - Automatic notebook creation
  - Upload and verify

**中文：**
- **v1.1.0** (2026-03-12) - 添加中英双语支持
- **v1.0.0** (2026-03-07) - 初始版本
  - 支持 X 文章抓取
  - 自动创建 Notebook
  - 上传并验证

---

*Version 1.1.0 / 版本 1.1.0*
