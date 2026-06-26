# xiaohongshu-mcp 配置详解

## 安装

从 GitHub 获取：[xpzouying/xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp)

## 可执行文件

| 文件 | 用途 |
|------|------|
| `xiaohongshu-mcp-{platform}` | MCP 服务端 |
| `xiaohongshu-login-{platform}` | 登录工具（扫码） |

## 启动参数

### MCP 服务端

```bash
./xiaohongshu-mcp-{platform} [-headless] [-port :18060]
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-headless` | 无头模式 | true |
| `-port` | HTTP 服务端口 | :18060 |

### 登录工具

```bash
./xiaohongshu-login-{platform}
```

无参数时自动打开浏览器显示小红书登录页，扫码即可。

## Cookie 存储

登录后 cookie 存储在临时文件，MCP 服务自动加载。

**注意**: 不要在其他浏览器登录同一小红书账号，会失效。

## API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/v1/login/status` | GET | 检查登录状态 |
| `/api/v1/publish` | POST | 发布笔记 |
| `/api/v1/search` | POST | 搜索笔记 |
| `/api/v1/feeds` | GET | 获取推荐流 |

## 发布参数

```json
{
  "title": "笔记标题",
  "content": "正文内容",
  "images": ["绝对路径"],
  "tags": ["标签"]
}
```

## 故障排查

### 服务未启动

解决：启动 MCP 服务

### 未登录

解决：运行登录工具扫码

### 图片路径错误

解决：使用绝对路径，不带 `file://` 协议

### 发布超时

发布需要 1-2 分钟，设置 timeout >= 180 秒。