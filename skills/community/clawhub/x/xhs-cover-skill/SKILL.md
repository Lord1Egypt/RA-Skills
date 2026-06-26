---
name: xhs-cover
version: 3.0.0
description: 生成小红书风格封面图片。使用场景：(1) 用户要求生成小红书封面 (2) 用户要求生成社交媒体封面图 (3) 用户为笔记/文章生成配图 (4) 用户询问 credit 余额或生成历史。首次使用会自动引导注册。
requires:
  binaries:
    - npx
sendsDataTo:
  - https://api.xhscover.cn
---

# 小红书封面生成器

通过 `npx xhscover` 生成小红书风格封面图片。首次使用自动引导注册，跨平台支持。

> **注意**：本技能需要将您的 API Key 和封面文案发送到 xhscover.cn 服务。请确保您信任该服务后再使用。

## 环境要求

- Node.js >= 18（用于 npx）

## 首次使用

如果未配置 API Key，运行以下命令注册并自动配置：

```bash
npx xhscover setup
```

注册即获 10 个免费积分。

## 快速使用

```bash
# 生成封面（默认 3:4 竖版）
npx xhscover generate "5个习惯让你越来越自律"

# 指定宽高比
npx xhscover generate "今日份好心情" 1:1

# 查询余额
npx xhscover balance

# 查看历史
npx xhscover history
```

## 宽高比选项

| 比例 | 说明 |
|------|------|
| `3:4` | 小红书标准竖版（默认） |
| `9:16` | 超长竖版 |
| `1:1` | 正方形 |
| `16:9` | 横版 |

## 数据流向

本技能通过 `npx xhscover` 调用 `api.xhscover.cn` REST API，将封面文案和 API Key 发送到服务端进行处理。

## 相关链接

- 官网：https://xhscover.cn
- CLI 工具：https://github.com/xwchris/xhscover-cli
- npm 包：https://www.npmjs.com/package/xhscover
