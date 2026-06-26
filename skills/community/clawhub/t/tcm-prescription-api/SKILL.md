---
name: tcm-prescription-api
version: 1.0.1
license: MIT-0
description: "中医药方剂API查询技能。通过HTTP API查询中医药方剂数据库中的方剂资料。支持方剂搜索、方剂详情查看、分类浏览、症状推荐等功能。This skill should be used when the user mentions: 查方剂、搜索方剂、方剂详情、中药方、方剂分类、症状推荐方剂、中医药方查询、方剂数据、prescription search、herb formula、TCM prescription、查询中药、方剂API、方剂数据库。"
metadata:
  openclaw:
    emoji: "\U0001F9E8"
    category: api
  clawdbot:
    emoji: "\U0001F9E8"
    requires:
      bins: ["curl", "python3"]
      envs: ["TCM_API_KEY"]
    install: []
---

# 中医药方剂 API 查询技能

## 用途

通过中医药方剂数据库的 REST API 接口，查询方剂名称、组成、功用、主治、方解、方歌、用法、禁忌、加减变化等完整资料。支持模糊搜索、分类浏览和基于症状的方剂推荐。

## 触发条件

当用户的请求涉及以下任一场景时，加载此技能：

- **方剂搜索**：用户想查找某个方剂（如"查一下桂枝汤"、"搜索麻黄汤"、"find Guizhi Tang"）
- **方剂详情**：用户想了解某个方剂的完整资料（如"桂枝汤的组成是什么"、"桂枝汤的功用"、"tell me about Mahuang Tang"）
- **分类浏览**：用户想浏览某类方剂（如"解表剂有哪些"、"清热剂的方剂"、"show me diaphoretic formulas"）
- **症状推荐**：用户描述症状并希望推荐方剂（如"头痛发热怎么办"、"推荐治感冒的方剂"、"what formula for headache and fever"）
- **方剂数据查询**：泛化的中医药方数据需求（如"方剂数据库"、"中药方资料"、"TCM formula database"）

## 前置条件

### API Key 配置（推荐通过环境变量）

API Key 用于访问完整功能（如症状推荐）。推荐通过环境变量安全配置：

1. 访问网站 https://119.91.226.122 注册账号并生成 API Key
2. 将 API Key 配置为环境变量：`export TCM_API_KEY=<your_key>`
3. 技能将自动从环境变量读取，无需在对话中输入

无 API Key 也可使用基本功能（搜索、分类浏览、方剂详情）。

## API 服务地址

- **API 基础地址**：`https://119.91.226.122/api`
- **网站首页**：`https://119.91.226.122`
- **健康检查**：`https://119.91.226.122/health`

## API 接口说明

详细的 API 接口文档请查阅 `references/api-reference.md`。以下是核心接口概览：

### 1. 搜索方剂

```bash
curl -s "https://119.91.226.122/api/prescriptions/search?q=桂枝&page=1&limit=20"
```

参数说明：
- `q` 或 `keyword`：搜索关键词（方剂名称、药物组成等）
- `category`：按分类筛选（如"解表剂"、"清热剂"）
- `page`：页码，默认 1
- `limit` 或 `pageSize`：每页条数，默认 20

### 2. 获取方剂详情

```bash
curl -s "https://119.91.226.122/api/prescriptions/PRESCRIPTION_ID"
```

返回方剂的完整信息：名称、别名、组成、功用、主治、方解、方歌、用法、禁忌、加减变化、来源等。

### 3. 获取方剂分类

```bash
curl -s "https://119.91.226.122/api/prescriptions/categories"
```

返回所有方剂分类列表（如解表剂、泻下剂、和解剂、清热剂等）。

### 4. 症状推荐方剂（需要 API Key）

系统同时对 `indications`（主治）和 `description`（功用）字段进行关键词匹配，按匹配症状数量排序返回。

```bash
curl -s -X POST "https://119.91.226.122/api/prescriptions/recommend" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $TCM_API_KEY" \
  -d '{"symptoms": ["头痛", "发热", "恶风", "汗出"]}'
```

返回的每条推荐结果包含 `matchScore`（匹配症状数），分数越高越相关。

### 5. 健康检查

```bash
curl -s "https://119.91.226.122/health"
```

## 执行流程

当用户触发此技能时，按以下流程执行：

### Step 0：检查 API Key 状态

在执行任何查询之前，先检查环境变量中是否配置了 API Key：

1. 检查环境变量 `TCM_API_KEY` 是否已设置
2. 如果已设置 → 在需要认证的请求中自动附加
3. 如果未设置 → 提示用户配置环境变量，或使用无认证模式继续

**重要**：不要要求用户在对话中直接粘贴 API Key。始终引导用户通过环境变量配置。

### Step 1：识别用户意图

分析用户请求，判断属于以下哪种类型：

| 意图 | 关键词示例 | 对应接口 |
|------|-----------|---------|
| 搜索方剂 | "查"、"搜索"、"找" + 方剂名 | `GET /api/prescriptions/search` |
| 方剂详情 | "组成"、"功用"、"主治"、"详情" + 方剂名 | 先搜索获取 ID，再 `GET /api/prescriptions/:id` |
| 分类浏览 | "分类"、"有哪些" + 分类名 | `GET /api/prescriptions/categories` 然后按分类搜索 |
| 症状推荐 | "症状"、"推荐"、"治什么" + 症状描述 | `POST /api/prescriptions/recommend` |

### Step 2：构建 API 请求

根据识别的意图，构建对应的 API 请求。参考 `scripts/query_prescriptions.sh` 脚本中的实现方式。

如果环境变量 `TCM_API_KEY` 已设置，将其加入 `X-API-Key` 请求头。如果未设置，则尝试无认证访问。

### Step 3：执行查询

使用 `execute_command` 工具执行 `curl` 命令调用 API。使用 `python3 -m json.tool` 格式化 JSON 输出以便阅读。

### Step 4：解析与呈现结果

将 API 返回的 JSON 数据解析后，以清晰的中文格式呈现给用户：

- **搜索结果**：列出匹配的方剂名称、分类、简要功用，提示用户可以选择查看详情
- **方剂详情**：展示完整方剂资料，按"组成 → 功用 → 主治 → 方解 → 用法 → 禁忌 → 加减变化"的顺序组织
- **分类列表**：以表格形式展示所有分类及各方剂数量
- **症状推荐**：列出推荐的方剂及其推荐理由

### Step 5：追问与深入

查询完成后，询问用户是否需要：
- 查看某个方剂的详细信息
- 查看其他分类的方剂
- 调整搜索条件

## 辅助脚本

`scripts/query_prescriptions.sh` 提供了封装好的命令行工具，可用于快速查询。用法：

```bash
bash scripts/query_prescriptions.sh search "桂枝"              # 搜索方剂
bash scripts/query_prescriptions.sh detail PRESCRIPTION_ID     # 查看详情
bash scripts/query_prescriptions.sh categories                   # 获取分类
bash scripts/query_prescriptions.sh recommend "头痛,发热,恶风"  # 症状推荐
bash scripts/query_prescriptions.sh health                       # 健康检查
```

脚本通过环境变量 `TCM_API_KEY` 读取 API Key，无需在命令行参数中传递。

## 注意事项

1. API 有速率限制（每分钟 100 次请求），避免短时间内大量调用
2. 症状推荐接口需要有效的 API Key（通过环境变量 `TCM_API_KEY` 配置）
3. 方剂 ID 为系统内部标识，可通过搜索接口获取
4. 搜索支持中文方剂名、药物名等多种关键词，中文搜索时需进行 URL 编码
5. 公开接口可返回完整方剂信息（组成、用法、适应症、禁忌、注意事项）

## 关于

- **技能名称**：tcm-prescription-api
- **开发者**：Phal Studio
- **客服邮箱**：guest@phalstudio.tech
