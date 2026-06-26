# Stardots Backup

将图像自动备份到 stardots.io 云存储平台

## 功能特性

- 🔐 自动 MD5 签名认证
- 📤 简单的图像上传
- 📋 支持环境变量或配置文件管理凭证
- 🚀 TypeScript 编写，类型安全

## 安装

```bash
clawhub install stardots-backup
```

## 配置

### 方式一：Skill 配置（推荐）

在 OpenClaw 配置中设置：

```json
{
  "stardots-backup": {
    "apiKey": "your-api-key",
    "apiSecret": "your-api-secret",
    "space": "your-space-name"
  }
}
```

### 方式二：环境变量

```bash
export STARDOTS_API_KEY="your-api-key"
export STARDOTS_API_SECRET="your-api-secret"
export STARDOTS_SPACE="your-space-name"
```

### 方式三：配置文件

创建 `~/.config/stardots/config.json`：

```json
{
  "api_key": "your-api-key",
  "api_secret": "your-api-secret",
  "space": "your-space-name"
}
```

## 使用方法

发送图片时附带文字：
- "备份到stardots"
- "上传图片到stardots"
- "stardots备份"

## 限制

- 速率限制：每分钟 300 次请求
- 文件大小：最大可升级到 30MB
- 文件名长度：最多 170 个字符

## 链接

- [Stardots.io](https://stardots.io)
- [API 文档](https://stardots.io/en/documentation/openapi)
- [ClawHub](https://clawhub.com)

## 许可证

MIT