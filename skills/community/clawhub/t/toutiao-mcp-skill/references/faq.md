# 常见问题 (FAQ)

## 安装相关

### Q: 如何安装 toutiao-mcp？

A: 使用 npm 全局安装：
```bash
npm install -g toutiao-mcp
npx playwright install chromium
```

### Q: 支持哪些 Node.js 版本？

A: Node.js >= 18.0.0

### Q: 需要安装哪些浏览器？

A: 只需要 Chromium：
```bash
npx playwright install chromium
```

## 登录相关

### Q: 如何登录今日头条？

A: 在 OpenClaw 中说"帮我登录今日头条"，AI 会调用 `login_with_credentials` 工具打开浏览器，你在浏览器中完成登录即可。

### Q: Cookie 保存在哪里？

A: 默认保存在 `COOKIES_FILE` 环境变量指定的位置，通常是 `~/.openclaw/data/toutiao-cookies.json`

### Q: Cookie 会过期吗？

A: 会的。如果提示未登录，重新调用登录工具即可。

### Q: 可以使用账号密码自动登录吗？

A: 目前需要手动在浏览器中完成登录，这样更安全。

## 发布相关

### Q: 文章标题有什么限制？

A: 标题长度为 2-30 个字。

### Q: 支持哪些图片格式？

A: JPG, PNG, GIF, WEBP

### Q: 图片大小有限制吗？

A: 建议单张图片不超过 10MB。

### Q: 可以发布视频吗？

A: 目前不支持视频发布，只支持图文文章和微头条。

### Q: 微头条和文章有什么区别？

A: 
- 文章：长内容，有标题和正文，适合深度内容
- 微头条：短内容，类似微博，适合快速分享

### Q: 如何批量发布小红书数据？

A: 使用 `publish_xiaohongshu_data` 工具，提供 JSON 格式的数据数组：
```json
[
  {
    "小红书标题": "标题",
    "仿写小红书文案": "正文",
    "配图": "https://example.com/image.jpg"
  }
]
```

## 错误处理

### Q: 提示"未登录"怎么办？

A: 调用 `login_with_credentials` 重新登录。

### Q: 发布失败怎么办？

A: 
1. 检查是否已登录
2. 检查内容格式是否符合要求
3. 查看详细错误信息
4. 如果问题持续，提交 GitHub Issue

### Q: 图片上传失败怎么办？

A: 
1. 检查图片路径是否正确
2. 确认图片格式是否支持
3. 检查图片大小是否超限
4. 检查网络连接

### Q: 浏览器自动化失败怎么办？

A: 
1. 更新 toutiao-mcp 到最新版本
2. 重新安装浏览器：`npx playwright install chromium`
3. 如果问题持续，报告到 GitHub Issues

## 配置相关

### Q: 如何配置无头模式？

A: 在 MCP 配置中设置环境变量：
```json
{
  "env": {
    "PLAYWRIGHT_HEADLESS": "true"
  }
}
```

### Q: 如何查看详细日志？

A: 设置日志级别：
```json
{
  "env": {
    "LOG_LEVEL": "debug"
  }
}
```

### Q: 数据保存在哪里？

A: 保存在 `DATA_DIR` 环境变量指定的目录，默认是 `~/.openclaw/data`

## 性能相关

### Q: 发布一篇文章需要多长时间？

A: 通常 30-60 秒，取决于网络速度和图片数量。

### Q: 可以并发发布吗？

A: 不建议并发，建议按顺序发布以避免被平台限制。

### Q: 批量发布会被限制吗？

A: 建议控制发布频率，避免短时间内大量发布。

## 其他问题

### Q: 支持哪些平台？

A: macOS, Linux, Windows（需要 WSL）

### Q: 是否开源？

A: 是的，Apache-2.0 许可证。

### Q: 如何贡献代码？

A: 欢迎提交 Pull Request 到 GitHub 仓库。

### Q: 如何报告 Bug？

A: 在 GitHub 提交 Issue，请包含：
- 错误信息
- 操作步骤
- 环境信息（Node.js 版本、操作系统等）

### Q: 数据安全吗？

A: 
- ✅ Cookie 仅存储在本地
- ✅ 不上传数据到第三方
- ✅ 所有通信仅限今日头条官方网站
- ✅ 开源代码，可审计

## 获取更多帮助

- GitHub: https://github.com/sipingme/toutiao-mcp-skill
- Email: sipingme@gmail.com
- 文档: [SKILL.md](../SKILL.md)
