---
name: social-media-marketing-hub
description: "🎯 社交媒体营销中心 — 抖音爆款分析 + AI标题/脚本生成 + 选品分析 + 竞品账号分析。输入关键词，AI自动分析爆款规律，生成可用的标题和口播脚本。微信: without-dream"
---

# Social Hub · 社交媒体营销中心

## 安装配置

```bash
git clone https://github.com/0xbigbig/social-media-marketing-hub.git
cd social-media-marketing-hub/scripts

# 推荐：环境变量配置（安全）
export TIKHUB_TOKEN=你的Token
export DEEPSEEK_KEY=你的Key

# 或者配置文件（兼容旧版）
node marketing_hub.js config <TikHubToken> <DeepSeekKey>
```

**获取 API：**
- TikHub Token → [tikhub.io/register](https://user.tikhub.io/register?ref=teKGFLs1)
- DeepSeek Key → [platform.deepseek.com](https://platform.deepseek.com/)

> ⚠️ API Key 推荐通过环境变量配置，避免明文存储。

---

## 命令参考

### 抖音分析

| 命令 | 说明 |
|------|------|
| `analyze <词>` | 深度分析 + AI 学习爆款规律 |
| `analyze <词> --days=7` | 只看7天内数据 |
| `analyze <词> --has-product` | 只看带货视频 |
| `analyze <词> --browser` | 用真实浏览器搜索 |
| `a <词>` | 快速查看数据（免费） |

### 爆款标题

| 命令 | 说明 |
|------|------|
| `titles <词>` | 生成10条爆款标题 |
| `titles <词> -n=20` | 生成20条 |

### 口播脚本

| 命令 | 说明 |
|------|------|
| `script <词> sales [产品] [价格]` | 带货脚本（60秒+） |
| `script <词> seed` | 种草脚本（30-60秒） |
| `script <词> traffic` | 引流脚本（15-30秒） |

例：`node marketing_hub.js script 咖啡 sales 挂件 39`

### 商品分析

| 命令 | 说明 |
|------|------|
| `product <词>` | AI 选品分析 + 带货机会识别 |

### 竞品账号分析

| 命令 | 说明 |
|------|------|
| `author <博主名>` | 账号数据 + 视频风格 + 带货能力 + AI深度分析 |

例：`node marketing_hub.js author 李子柒`

### 记忆系统

| 命令 | 说明 |
|------|------|
| `memory` | 查看所有赛道记忆 |
| `memory <词>` | 查看某赛道详细记忆 |
| `dashboard <词>` | 可视化分析面板 |

### 一键全套

```bash
full <词> [产品] [价格]
# 等于：analyze + titles + script
```

### 自然语言

支持直接说人话，AI 自动识别命令和关键词：

```bash
用浏览器分析咖啡
```

---

## 数据输出说明

- `analyze / a / product / author` 结果存入 `scripts/memory/<词>.json`
- `author` 分析完整报告存入 `author_<博主名>.json`
- 所有分析结果均可叠加，越分析 AI 越懂你的赛道
