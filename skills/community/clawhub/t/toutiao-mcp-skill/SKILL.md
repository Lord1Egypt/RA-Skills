---
name: toutiao-mcp
description: 通过 MCP 协议操作今日头条平台，支持内容发布、账号管理等功能
version: 1.0.0
author: Ping Si <sipingme@gmail.com>
type: mcp-server
requires:
  - mcpServer: toutiao-mcp
  - node: ">=18.0.0"
  - browser: chromium
tags:
  - toutiao
  - mcp
  - content-publishing
  - automation
repository: https://github.com/sipingme/toutiao-mcp-skill
mcpServer: https://github.com/sipingme/toutiao-mcp
---

# 今日头条 MCP Skill

通过 Model Context Protocol 让 AI 能够操作今日头条平台。

## 🏗️ 架构说明

本 Skill 是一个 MCP Server 集成配置，实际功能由 [toutiao-mcp](https://github.com/sipingme/toutiao-mcp) MCP Server 提供。

```
OpenClaw/AI Agent
    ↓ (读取 Skill 配置)
toutiao-mcp-skill
    ↓ (启动 MCP Server)
toutiao-mcp
    ↓ (MCP Protocol - 6 Tools)
今日头条平台
```

## 🎯 何时使用此 Skill

当用户需要操作今日头条平台时，AI 会自动调用相应的 MCP 工具：

### 账号管理
- ✅ 登录今日头条账号
- ✅ 检查登录状态
- ✅ 登出账号

### 内容发布
- ✅ 发布图文文章（支持多图、标签）
- ✅ 发布微头条（短内容快速分享）
- ✅ 批量发布小红书数据到今日头条

### 典型使用场景

1. **内容创作者**：将创作的文章、教程发布到今日头条
2. **知识分享者**：分享学习笔记、技术心得
3. **多平台运营**：将小红书内容同步到今日头条
4. **自媒体工作者**：批量管理和发布内容

**触发关键词**：
- "发布到今日头条"、"今日头条发布"、"头条发文"
- "发布文章到头条"、"在头条发表文章"
- "发布微头条"、"发微头条"、"头条动态"
- "把小红书数据发到头条"、"同步到今日头条"
- "批量发布到头条"、"头条批量发文"

## 📋 前置要求

### 1. 安装 toutiao-mcp MCP Server

```bash
# 方式 1：从 npm 安装（推荐）
npm install -g toutiao-mcp

# 安装浏览器
npx playwright install chromium

# 方式 2：从源码构建
git clone https://github.com/sipingme/toutiao-mcp.git
cd toutiao-mcp
npm install
npx playwright install chromium
npm run build
```

### 2. 配置 OpenClaw

在 OpenClaw 的 MCP 配置中添加：

```json
{
  "mcpServers": {
    "toutiao": {
      "command": "node",
      "args": ["/path/to/toutiao-mcp/dist/index.js"],
      "env": {
        "PLAYWRIGHT_HEADLESS": "true",
        "COOKIES_FILE": "/path/to/data/cookies.json",
        "DATA_DIR": "/path/to/data"
      }
    }
  }
}
```

### 3. 安装 Skill 文档

```bash
# 克隆 Skill 配置和文档
git clone https://github.com/sipingme/toutiao-mcp-skill.git
cp -r toutiao-mcp-skill ~/.openclaw/skills/toutiao/
```

## 🚀 标准操作流程 (SOP)

### 操作 1：检查登录状态

**场景**：在执行任何操作前，先确认登录状态

**MCP 工具**：`check_login_status`

**步骤**：

1. AI 调用 `check_login_status` 工具
2. 解析返回结果
3. 如果未登录，引导用户登录

**输出示例**：
```json
{
  "isLoggedIn": true,
  "message": "已登录"
}
```

**异常处理**：
- 如果 `isLoggedIn: false`，执行操作 2（登录流程）
- 如果 Cookie 过期，提示用户重新登录

---

### 操作 2：登录今日头条

**场景**：首次使用或 Cookie 过期

**MCP 工具**：`login_with_credentials`

**步骤**：

1. AI 调用 `login_with_credentials` 工具
2. 系统会打开浏览器窗口
3. 用户在浏览器中完成登录（扫码或账号密码）
4. 登录成功后，Cookie 自动保存

**输入参数**：
```json
{
  "headless": false
}
```

**输出示例**：
```json
{
  "success": true,
  "message": "登录成功"
}
```

**异常处理**：
- 登录超时：重新调用工具
- 登录失败：检查网络连接或账号状态

---

### 操作 3：发布图文文章

**场景**：用户提供标题、正文和图片，发布到今日头条

**MCP 工具**：`publish_article`

**前置条件**：
- ✅ 用户已登录
- ✅ 标题符合规范（2-30字）
- ✅ 正文内容充实（建议300字以上）
- ✅ 图片格式正确（可选）

**步骤**：

1. **验证登录状态**
   ```
   调用 check_login_status
   如果未登录 → 执行操作 2（登录流程）
   ```

2. **收集发布信息**
   - 标题（必需，2-30字）
   - 正文内容（必需，建议300字以上）
   - 图片路径列表（可选，支持本地路径和 URL）
   - 标签（可选，建议3-5个）

3. **验证内容格式**
   - 检查标题长度
   - 验证图片路径（如果有）
   - 确认正文不为空

4. **调用发布工具**

```json
{
  "title": "Node.js 开发技巧分享",
  "content": "本文分享几个实用的 Node.js 开发技巧...\n\n## 1. 使用 async/await\n\n异步编程是 Node.js 的核心...\n\n## 2. 错误处理最佳实践\n\n正确的错误处理能提高应用稳定性...\n\n## 3. 性能优化技巧\n\n...",
  "images": ["/path/to/image1.jpg", "/path/to/image2.jpg"],
  "tags": ["Node.js", "编程", "技术分享"]
}
```

5. **等待发布完成**
   - 预计时间：30-60秒
   - 显示进度提示
   - 处理可能的错误

6. **向用户报告结果**

**输出示例**：
```json
{
  "success": true,
  "articleId": "7123456789",
  "url": "https://www.toutiao.com/article/7123456789/",
  "message": "文章发布成功"
}
```

**成功标准**：
- ✅ 返回 `success: true`
- ✅ 获得文章 ID
- ✅ 可以在今日头条查看文章

**异常处理**：

| 错误类型 | 症状 | 解决方案 |
|---------|------|----------|
| 未登录 | `isLoggedIn: false` | 执行操作 2（登录流程） |
| 标题超长 | "标题长度不符" | 缩短标题到30字以内 |
| 标题过短 | "标题太短" | 扩充标题到2字以上 |
| 图片路径错误 | "图片不存在" | 检查路径，使用绝对路径 |
| 图片格式错误 | "不支持的格式" | 转换为 JPG/PNG/GIF/WEBP |
| 网络超时 | "请求超时" | 重试或检查网络连接 |
| 内容违规 | "内容审核失败" | 修改内容后重新发布 |

**最佳实践**：
- 📝 标题简洁有力，突出核心价值
- 📝 正文结构清晰，使用标题分段
- 📝 添加相关标签，提高曝光率
- 📝 配图质量高，与内容相关
- 📝 发布前预览，确保格式正确

---

### 操作 4：发布微头条

**场景**：用户想发布短内容到微头条（类似微博）

**MCP 工具**：`publish_micro_post`

**适用场景**：
- 💬 日常想法、心得分享
- 💬 学习笔记、技术片段
- 💬 快速资讯、动态更新
- 💬 图片配文、截图分享

**前置条件**：
- ✅ 用户已登录
- ✅ 内容不为空
- ✅ 内容长度适中（建议2000字以内）

**步骤**：

1. **验证登录状态**
   ```
   调用 check_login_status
   ```

2. **收集发布信息**
   - 内容（必需，建议2000字以内）
   - 图片（可选，最多9张）
   - 话题标签（可选，使用 #话题 格式）

3. **调用发布工具**

```json
{
  "content": "今天学习了 TypeScript 的高级类型，收获满满！\n\n主要学习了：\n• 条件类型\n• 映射类型\n• 工具类型\n\n#TypeScript #学习笔记 #前端开发",
  "images": ["/path/to/screenshot1.jpg", "/path/to/screenshot2.jpg"]
}
```

4. **等待发布完成**（通常10-20秒）

5. **向用户报告结果**

**输出示例**：
```json
{
  "success": true,
  "postId": "7123456789",
  "url": "https://www.toutiao.com/w/7123456789/",
  "message": "微头条发布成功"
}
```

**微头条 vs 文章对比**：

| 特性 | 微头条 | 文章 |
|------|--------|------|
| 内容长度 | 短（建议2000字内） | 长（建议300字以上） |
| 发布速度 | 快（10-20秒） | 慢（30-60秒） |
| 适用场景 | 碎片化分享 | 深度内容 |
| 标题要求 | 无标题 | 必需标题 |
| 话题标签 | 支持 #话题 | 支持标签 |

**内容建议**：
- 💡 使用话题标签增加曝光（#话题）
- 💡 配图提高吸引力
- 💡 内容简洁明了，突出重点
- 💡 适当使用 emoji 增加趣味性
- 💡 互动性强的内容更容易传播

**异常处理**：
- 未登录：执行登录流程
- 内容为空：提示用户输入内容
- 图片过多：限制在9张以内
- 内容过长：建议发布为文章

---

### 操作 5：批量发布小红书数据

**场景**：用户有小红书格式的数据，想批量发布到今日头条

**MCP 工具**：`publish_xiaohongshu_data`

**步骤**：

1. 验证用户已登录
2. 准备小红书数据（JSON 数组格式）
3. 指定下载目录（用于保存图片）

4. 调用 `publish_xiaohongshu_data` 工具：

```json
{
  "data": [
    {
      "小红书标题": "TypeScript 开发技巧",
      "仿写小红书文案": "分享几个 TypeScript 实用技巧...",
      "配图": "https://example.com/image1.jpg"
    },
    {
      "小红书标题": "React 性能优化",
      "仿写小红书文案": "React 性能优化的几个要点...",
      "配图": "https://example.com/image2.jpg"
    }
  ],
  "downloadDir": "/path/to/downloads"
}
```

**输出示例**：
```json
{
  "success": true,
  "total": 2,
  "succeeded": 2,
  "failed": 0,
  "results": [
    {
      "title": "TypeScript 开发技巧",
      "success": true,
      "articleId": "7123456789"
    },
    {
      "title": "React 性能优化",
      "success": true,
      "articleId": "7123456790"
    }
  ],
  "message": "批量发布完成，成功 2 条"
}
```

**数据格式要求**：
- `小红书标题`：文章标题
- `仿写小红书文案`：文章正文
- `配图`：图片 URL（自动下载）

**异常处理**：
- 部分失败：继续处理其他数据，最后汇总结果
- 图片下载失败：跳过该图片或整条数据
- 网络问题：重试机制

---

### 操作 6：登出账号

**场景**：用户想退出登录

**MCP 工具**：`logout`

**步骤**：

```json
{}
```

**输出示例**：
```json
{
  "success": true,
  "message": "已登出"
}
```

---

## 📊 输入输出规范

### MCP 工具输出格式

所有工具统一使用 JSON 格式输出：

**成功响应**：
```json
{
  "success": true,
  "message": "操作成功",
  "data": {
    "id": "7123456789",
    "url": "https://www.toutiao.com/..."
  }
}
```

**错误响应**：
```json
{
  "success": false,
  "error": "错误信息",
  "code": "ERROR_CODE"
}
```

### 内容规范

#### 文章标题
- **长度限制**：2-30个字
- **计算规则**：
  - 中文字符：1个字
  - 英文字母/数字：0.5个字
  - 标点符号：1个字
- **建议**：
  - ✅ 简洁有力，突出核心
  - ✅ 包含关键词，便于搜索
  - ❌ 避免标题党
  - ❌ 避免特殊符号过多

**标题示例**：
```
✅ 好标题：
- "Node.js 性能优化实战指南"
- "TypeScript 高级类型详解"
- "前端开发必备的10个工具"

❌ 差标题：
- "震惊！！！这个技巧让我..."（标题党）
- "a"（太短）
- "这是一篇关于 Node.js 性能优化的非常详细的实战指南文章"（太长）
```

#### 图片要求

| 项目 | 要求 | 说明 |
|------|------|------|
| **格式** | JPG, PNG, GIF, WEBP | 推荐 JPG（体积小） |
| **大小** | 单张 ≤ 10MB | 建议压缩到 2MB 以内 |
| **尺寸** | 建议 1920x1080 | 保持清晰度 |
| **数量** | 文章：不限；微头条：≤9张 | 建议3-5张 |
| **来源** | 本地路径或 URL | URL 会自动下载 |

**图片路径示例**：
```json
{
  "images": [
    "/Users/username/Pictures/image1.jpg",
    "https://example.com/image2.jpg",
    "./relative/path/image3.png"
  ]
}
```

#### 内容要求

| 内容类型 | 长度建议 | 质量要求 |
|---------|---------|----------|
| **文章正文** | ≥ 300字 | 结构清晰，内容充实 |
| **微头条** | ≤ 2000字 | 简洁明了，重点突出 |
| **标签** | 3-5个 | 相关性强，覆盖主题 |

**内容格式建议**：
```markdown
# 使用 Markdown 格式

## 二级标题

正文内容...

- 列表项 1
- 列表项 2

**加粗重点**

> 引用内容
```

#### 标签规范

- **数量**：建议 3-5 个
- **选择原则**：
  - ✅ 与内容高度相关
  - ✅ 热门标签优先
  - ✅ 覆盖不同维度
- **示例**：
  ```json
  {
    "tags": ["Node.js", "性能优化", "后端开发", "技术分享"]
  }
  ```

---

## ⚠️ 常见问题和解决方案

### 问题 1：未登录或 Cookie 过期

**症状**：提示"未登录"或操作失败

**解决**：
调用 `login_with_credentials` 工具重新登录

### 问题 2：标题长度不符合要求

**症状**：提示"标题长度不符合要求"

**解决**：
- 检查标题长度（2-30字）
- 修改标题使其符合要求

### 问题 3：图片上传失败

**症状**：提示"图片上传失败"

**原因**：
- 图片路径错误
- 图片格式不支持
- 图片大小超限
- 网络问题

**解决**：
- 检查图片路径是否正确
- 确认图片格式（JPG/PNG/GIF/WEBP）
- 压缩图片到合适大小
- 检查网络连接

### 问题 4：浏览器自动化失败

**症状**：提示"页面元素未找到"

**原因**：今日头条页面结构变化

**解决**：
- 更新 toutiao-mcp 到最新版本
- 报告问题到 GitHub Issues

### 问题 5：批量发布部分失败

**症状**：批量发布时部分数据失败

**解决**：
- 查看详细错误信息
- 检查失败数据的格式
- 单独重试失败的数据

---

## 🔒 安全性说明

### 敏感信息处理

- Cookie 存储在本地文件中（默认 `./data/cookies.json`）
- 不会上传任何数据到第三方服务器
- 所有通信仅限于今日头条官方网站

### 权限要求

- 读取本地文件（图片、文本）
- 网络访问（今日头条网站）
- 写入 Cookie 文件
- 浏览器控制（Playwright）

### 数据隐私

- ❌ 不会收集用户信息
- ❌ 不会上传到第三方服务器
- ✅ 所有操作仅在本地执行
- ✅ Cookie 仅存储在本地

---

## 🎓 示例对话

### 场景 1：发布文章

**用户**：帮我把这篇文章发布到今日头条

**AI**：好的，我来帮你发布。请提供以下信息：
1. 文章标题（2-30字）
2. 文章正文
3. 配图（可选）
4. 标签（可选）

**用户**：
标题：Node.js 性能优化实战
正文：[提供详细内容]
图片：/Users/me/article-cover.jpg
标签：Node.js、性能优化、后端开发

**AI**：收到！我将为你发布到今日头条。

[内部流程]
1. 检查登录状态 ✓
2. 验证标题长度 ✓
3. 处理图片 ✓
4. 调用 publish_article

```json
{
  "title": "Node.js 性能优化实战",
  "content": "...",
  "images": ["/Users/me/article-cover.jpg"],
  "tags": ["Node.js", "性能优化", "后端开发"]
}
```

**AI**：✅ 文章已成功发布到今日头条！

📊 发布详情：
- 标题：Node.js 性能优化实战
- 文章ID：7123456789
- 链接：https://www.toutiao.com/article/7123456789/
- 状态：✅ 发布成功
- 用时：45秒

你可以在今日头条 App 或网站查看文章。

---

### 场景 2：发布微头条

**用户**：发布一条微头条："今天学习了 TypeScript 的高级类型，终于搞懂了条件类型和映射类型的区别！#TypeScript #学习笔记"

**AI**：好的，我来帮你发布微头条。

[调用 publish_micro_post]

```json
{
  "content": "今天学习了 TypeScript 的高级类型，终于搞懂了条件类型和映射类型的区别！#TypeScript #学习笔记"
}
```

**AI**：✅ 微头条发布成功！

📊 发布详情：
- 动态ID：7123456790
- 链接：https://www.toutiao.com/w/7123456790/
- 话题：#TypeScript #学习笔记
- 用时：12秒

---

### 场景 3：批量发布小红书数据

**用户**：把这些小红书数据批量发布到今日头条

**AI**：好的，我来批量发布。请提供小红书数据文件或数据内容。

**用户**：[提供包含5条数据的 JSON 文件]

**AI**：收到 5 条数据，开始批量发布...

[内部流程]
1. 检查登录状态 ✓
2. 验证数据格式 ✓
3. 下载图片 ✓
4. 逐条发布...

进度：
- [1/5] TypeScript 开发技巧 ✅
- [2/5] React 性能优化 ✅
- [3/5] 前端工程化实践 ✅
- [4/5] Vue3 新特性解析 ✅
- [5/5] Webpack 配置指南 ✅

**AI**：✅ 批量发布完成！

📊 发布统计：
- 总数：5 条
- 成功：5 条 ✅
- 失败：0 条
- 总用时：3分45秒

📝 发布详情：
1. TypeScript 开发技巧 - ID: 7123456791
2. React 性能优化 - ID: 7123456792
3. 前端工程化实践 - ID: 7123456793
4. Vue3 新特性解析 - ID: 7123456794
5. Webpack 配置指南 - ID: 7123456795

所有文章已成功发布到今日头条！

---

### 场景 4：处理错误情况

**用户**：发布文章，标题：这是一篇非常非常非常详细的关于 Node.js 性能优化的完整实战指南

**AI**：抱歉，标题长度超出限制。

❌ 错误：标题长度为 35 字，超过最大限制 30 字

💡 建议修改为：
- "Node.js 性能优化完整实战指南"（14字）✅
- "Node.js 性能优化实战"（11字）✅

请提供修改后的标题。

**用户**：好的，用第一个

**AI**：收到！使用标题"Node.js 性能优化完整实战指南"继续发布...

[继续发布流程]

---

## 📚 参考资料

- [项目 GitHub](https://github.com/sipingme/toutiao-mcp-skill)
- [toutiao-mcp 核心库](https://github.com/sipingme/toutiao-mcp)
- [快速开始指南](./references/quick-start.md)
- [常见问题 FAQ](./references/faq.md)

---

## 📝 维护说明

- **版本**: 1.0.0
- **最后更新**: 2026-03-20
- **维护者**: Ping Si <sipingme@gmail.com>
- **许可证**: Apache-2.0

---

## ✅ 首次成功检查清单

新用户应该能在 5 分钟内完成：

- [ ] 安装工具：`npm install -g toutiao-mcp`
- [ ] 安装浏览器：`npx playwright install chromium`
- [ ] 配置 OpenClaw MCP Server
- [ ] 登录账号：调用 `login_with_credentials`
- [ ] 检查登录：调用 `check_login_status`
- [ ] 测试发布：准备内容，调用 `publish_article` 或 `publish_micro_post`
- [ ] 在今日头条网站或 App 中看到发布的内容

如果以上步骤都能顺利完成，说明 Skill 已正确配置！
