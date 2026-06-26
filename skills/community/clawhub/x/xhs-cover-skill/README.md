# xhs-cover-skill

<div align="center">

**小红书封面生成器** - OpenClaw AI Agent 技能

一句话生成精美的小红书风格封面图

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://openclaw.ai)
[![npm version](https://img.shields.io/npm/v/xhscover.svg)](https://www.npmjs.com/package/xhscover)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

---

## 功能特性

- **AI 自动设计** - 输入文案，自动生成小红书风格封面
- **多种比例** - 支持 3:4、9:16、1:1、16:9 等常用比例
- **余额查询** - 随时查看剩余生成次数
- **历史记录** - 查看之前生成的封面
- **一键注册** - `npx xhscover setup` 即可开始使用

## 快速开始

### 1. 安装技能

```bash
# 方法 1：从 GitHub 安装
cd ~/.openclaw/workspace
git clone https://github.com/xwchris/xhs-cover-skill.git skills/xhs-cover

# 方法 2：通过 ClawHub 安装
clawhub install xhs-cover
```

### 2. 配置（自动引导）

首次使用时自动引导注册：

```bash
npx xhscover setup
```

注册即获 10 个免费积分，API Key 自动保存到 `~/.xhscover`，无需手动配置。

## 使用示例

### 在 OpenClaw 中使用

| 你说 | AI 会做的 |
|------|-----------|
| "帮我生成一个小红书封面：5个习惯让你越来越自律" | 生成默认 3:4 竖版封面 |
| "生成一张 1:1 的封面，文案是今日份好心情" | 生成正方形封面 |
| "查询我的 xhscover 余额" | 显示剩余生成次数 |
| "看看我最近生成的封面" | 显示历史记录 |

### 命令行直接使用

```bash
# 生成封面（默认 3:4 竖版）
npx xhscover generate "5个习惯让你越来越自律"

# 指定宽高比
npx xhscover generate "今日份好心情" 1:1

# 查询余额
npx xhscover balance

# 查看历史
npx xhscover history 20
```

## 支持的尺寸

| 比例 | 用途 | 效果 |
|------|------|------|
| `3:4` | 小红书标准竖版（默认） | 适合图文笔记 |
| `9:16` | 超长竖版 | 适合长图笔记 |
| `1:1` | 正方形 | 适合 Instagram/微博 |
| `16:9` | 横版 | 适合 B站/视频封面 |

## 架构

```
OpenClaw Agent
    ↓  读取 SKILL.md，识别意图
npx xhscover（npm 包，Node.js）
    ↓
api.xhscover.cn REST API
    ↓
Gemini AI → 生成封面图片
```

跨平台支持，Node.js >= 18 即可。

## 数据安全

> **重要提示**：本技能需要将您的 API Key 和封面文案发送到 xhscover.cn 服务进行处理。

- 仅在使用时发送必要数据
- 不会存储或分享您的 API Key
- 请确保您信任 xhscover.cn 服务后再使用

## 相关链接

- 官网：[xhscover.cn](https://xhscover.cn)
- CLI 工具：[github.com/xwchris/xhscover-cli](https://github.com/xwchris/xhscover-cli)
- npm 包：[npmjs.com/package/xhscover](https://www.npmjs.com/package/xhscover)
- MCP Server：[github.com/xwchris/xhs-cover-mcp](https://github.com/xwchris/xhs-cover-mcp)
- OpenClaw：[openclaw.ai](https://openclaw.ai)

## License

MIT
