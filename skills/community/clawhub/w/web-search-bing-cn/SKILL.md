# Web Search Bing CN Skill

使用无头浏览器自动访问 Bing CN（必应中国版）进行搜索，并在访问需要登录的网站时打开 host 浏览器让用户登录的技能。

## 功能

- 支持中文搜索，返回纯净搜索结果
- 仅在网站明确要求登录时（检测到登录弹窗/按钮），才打开 host 浏览器
- 不预先判断哪些网站需要登录，而是实时检测页面状态
- 可获取搜索结果页面内容供后续解析
- 基于 OpenClaw 内置浏览器工具，无需额外依赖

### 浏览器设置

如需自定义浏览器行为，可在 `openclaw.json` 中配置 `browser` 字段（可选）：

```json
{
  "browser": {
    "headless": true,
    "noSandbox": true
  }
}
```

详细配置选项请参阅官方文档：https://docs.openclaw.ai/zh-CN/tools/browser

## 故障排除

- **"浏览器启动失败"**：检查 OpenClaw 浏览器工具是否正常配置
- **"登录检测不准确"**：某些网站可能使用动态加载，需要更复杂的检测逻辑
- **"host 浏览器无法打开"**：确保系统默认浏览器可用

## 依赖

- OpenClaw 内置浏览器工具（browser）
- 系统安装浏览器
