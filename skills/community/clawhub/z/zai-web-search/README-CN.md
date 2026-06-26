# Z.AI Web Search API - 中文说明

使用智谱 AI (Z.AI) 的网络搜索 API 进行智能搜索，支持多种搜索引擎和高级筛选。

## 功能概述

本技能提供 AI 驱动的网页搜索，支持多个中文搜索引擎，特别优化了中文内容的处理和 LLM 解析。

### 支持的搜索引擎

| 引擎 | 提供商 | 说明 |
|------|--------|------|
| `search_std` | 智谱 AI | 基础版，快速响应 |
| `search_pro` | 智谱 AI | 高阶版，最佳质量 |
| `search_pro_sogou` | 搜狗 | 搜狗搜索结果 |
| `search_pro_quark` | 夸克 | 夸克搜索结果 |

### 价格说明

官方定价页面：[https://open.bigmodel.cn/pricing](https://open.bigmodel.cn/pricing)

- Web Search API 使用 token 计费
- 不同引擎计费标准不同
- 请访问官方页面查看最新费率

### 与其他搜索工具对比

| 功能 | 本技能 (Z.AI) | Brave Search |
|------|--------------|--------------|
| 中文支持 | ✅ 优秀 | ⚠️ 有限 |
| 意图识别 | ✅ 支持 | ❌ 不支持 |
| 多引擎 | ✅ 4 个引擎 | ❌ 单引擎 |
| 时间过滤 | ✅ 支持 | ✅ 支持 |
| 域名过滤 | ✅ 支持 | ❌ 不支持 |

## 首次使用指南

当你第一次在 OpenClaw 中使用这个技能时，系统会引导你完成配置。

### 配置步骤

1. **获取 API Key**：访问 [https://open.bigmodel.cn](https://open.bigmodel.cn) 注册并获取 API Key

2. **选择配置方式**：
   - 在本技能文件夹创建 `config.json`（推荐）
   - 设置 `ZAI_API_KEY` 环境变量
   - 使用用户配置 `~/.config/zai-web-search/config.json`

3. **替换其他搜索技能**（可选）

   本技能可以替换其他搜索相关技能：
   - **Brave Search**（OpenClaw 内置）：替换以获得更好的中文搜索体验
   - 其他网页搜索技能：请比较功能后决定是否替换

   当被询问时，请说明是否要将此技能设为你的主要搜索工具。

### 默认行为

配置完成后，本技能将：
- 默认使用 `search_std` 引擎
- 返回 10 条结果
- 不应用时间过滤
- 使用中等长度摘要

你可以通过命令行参数或配置文件覆盖这些默认值。

## 功能特点

- 🚀 **多种搜索引擎**：智谱基础版/高阶版、搜狗搜索、夸克搜索
- 🎯 **智能意图识别**：自动理解查询意图，优化搜索结果
- ⏰ **时间过滤**：支持按天、周、月、年筛选最新内容
- 🎨 **多种输出格式**：Markdown、JSON、紧凑模式

## 快速开始

### 第一步：获取 API Key

1. 访问 [智谱 AI 开放平台](https://open.bigmodel.cn)
2. 注册/登录账号
3. 在控制台创建 API Key
4. 复制你的 API Key（格式类似：`xxxx.xxxxx.xxxxx`）

### 第二步：创建配置文件

在 skill 文件夹中创建 `config.json` 文件：

```bash
# 进入 skill 文件夹
cd ~/.openclaw/skills/zai-web-search

# 复制示例配置文件
cp config.json.example config.json

# 编辑配置文件（用你喜欢的编辑器）
# 比如: vim config.json, nano config.json, 或用 VS Code 打开
```

**⚠️ 重要提示**：
- `config.json.example` 是**示例文件**，里面有注释帮助理解
- 你创建的 `config.json` 才是实际使用的配置，必须是标准 JSON 格式
- 复制后请**删除所有注释**，否则会导致解析失败

### 第三步：填写配置

打开 `config.json`，填写你的 API Key（删除所有注释后）：

```json
{
  "apiKey": "把你的API Key粘贴到这里",
  "engine": "search_std",
  "intent": false,
  "count": 10,
  "recency": "noLimit",
  "content": "medium",
  "domain": ""
}
```

> 💡 **参数说明**：查看 [config.json.example](config.json.example) 了解每个参数的含义和可选值

**保存文件后，配置就完成了！** 🎉

## 配置参数说明

### 必填参数

| 参数 | 说明 |
|------|------|
| `apiKey` | 你的智谱 AI API Key |

### 可选参数

| 参数 | 说明 | 可选值 |
|------|------|--------|
| `engine` | 搜索引擎 | `search_std`(基础版), `search_pro`(高阶版), `search_pro_sogou`(搜狗), `search_pro_quark`(夸克) |
| `intent` | 启用智能意图识别 | `true`/`false` |
| `count` | 返回结果数量 | 1-50 |
| `recency` | 时间过滤 | `oneDay`, `oneWeek`, `oneMonth`, `oneYear`, `noLimit` |
| `content` | 内容长度 | `medium`(中等), `high`(详细) |
| `domain` | 域名过滤 | 域名，如 `"docs.openclaw.ai"` |

## 使用方法

### 基础搜索

```bash
# 使用默认配置搜索
zai-search "哈尔滨冰雪大世界 2026"

# 切换到高阶版搜索引擎
zai-search "人工智能最新进展" --engine search_pro

# 查询更多结果
zai-search "React 教程" --count 20
```

### 模糊查询（推荐启用意图识别）

当你不确定要搜索什么时，启用意图识别会有更好的结果：

```bash
# 询问式查询
zai-search "今天吃什么" --intent

zai-search "最近有什么好看的电影" --intent
```

### 按时间筛选

```bash
# 最近一周的新闻
zai-search "科技新闻" --recency oneWeek

# 最近一天的热点
zai-search "今日热点" --recency oneDay

# 最近一年的研究进展
zai-search "量子计算进展" --recency oneYear
```

### 限定搜索域名

```bash
# 只搜索某个网站
zai-search "OpenClaw 文档" --domain docs.openclaw.ai

# 搜索 React 官方文档
zai-search "React Hooks" --domain react.dev
```

### 获取详细内容

```bash
# 使用 high 模式获取更完整的内容摘要
zai-search "React 19 新特性" --content high
```

### 输出格式

```bash
# JSON 格式（方便脚本处理）
zai-search "查询内容" --json

# 紧凑模式（只显示标题和链接）
zai-search "查询内容" --compact

# 默认 Markdown 格式（易读）
zai-search "查询内容"
```

## 配置优先级

当同时存在多个配置来源时，优先级从高到低：

1. **命令行参数**（最高优先级）
   ```bash
   zai-search "查询" --engine search_pro  # 覆盖配置文件
   ```

2. **环境变量**（仅影响 apiKey）
   ```bash
   export ZAI_API_KEY="你的API Key"
   ```

3. **用户配置文件**
   ```bash
   ~/.config/zai-web-search/config.json
   ```

4. **Skill 文件夹配置文件**（最低优先级）
   ```bash
   config.json（在 skill 文件夹内）
   ```

## 示例场景

### 场景 1：日常搜索中文内容

```json
{
  "apiKey": "你的API Key",
  "engine": "search_std",
  "intent": true,
  "count": 10
}
```

### 场景 2：获取最新科技资讯

```json
{
  "apiKey": "你的API Key",
  "engine": "search_pro",
  "recency": "oneWeek",
  "content": "high"
}
```

### 场景 3：只搜索特定网站

```json
{
  "apiKey": "你的API Key",
  "engine": "search_std",
  "domain": "docs.python.org"
}
```

## 常见问题

### Q: 配置文件放哪里？

A: 建议放在 skill 文件夹内：`~/.openclaw/skills/zai-web-search/config.json`

### Q: 为什么复制示例文件后报错？

A: `config.json.example` 包含注释，JSON 标准不支持注释。请复制后删除所有 `//` 注释再保存。

### Q: API Key 哪里获取？

A: 访问 https://open.bigmodel.cn 注册后，在控制台创建 API Key

### Q: 搜索无结果怎么办？

A: 检查以下几点：
1. API Key 是否正确填写
2. 配置文件是否是标准 JSON（没有注释）
3. 查询词是否过长（建议 70 字符以内）
4. 是否触发了限流（稍等片刻再试）

### Q: 哪个搜索引擎最好？

A:
- `search_std`：速度快，适合日常搜索
- `search_pro`：质量最高，适合专业搜索
- `search_pro_sogou`：使用搜狗搜索结果
- `search_pro_quark`：使用夸克搜索结果

## 文件结构

```
zai-web-search/
├── README.md              # 本文件（中文说明）
├── SKILL.md               # 英文使用文档
├── config.json            # 你的配置文件（创建它）
├── config.json.example    # 配置示例
├── scripts/
│   └── zai-search.js      # CLI 脚本
└── .gitignore             # 忽略敏感文件
```

## 技术支持

如有问题，请参考：
- [智谱 AI 官方文档](https://open.bigmodel.cn)
- [API 文档](https://open.bigmodel.cn/dev/api#web_search)
