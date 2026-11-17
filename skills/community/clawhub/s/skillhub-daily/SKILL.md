---
name: "skillhub-daily"
slug: "skillhub-daily"
displayName: "SkillHub Daily"
version: "7.0.1"
summary: "每日扫描 SkillHub.cn 7 大排行榜 + 11 分类搜索 + 关键词搜索（7.5 万+ 技能），7 维度推荐 8 个技能，聚焦国内适配与活跃开发者"
license: MIT-0
description: |
  SkillHub Daily — 与 ClawHub Daily（口碑精品/趋势洞察）互补的每日推荐引擎。

  本技能的行为范围（用户须知）：
  - 读取本地记忆文件（TRAE memory 目录）提取关键词用于个性化推荐，仅使用关键词匹配，不传输原始记忆内容
  - 调用 skillhub CLI 获取 SkillHub.cn 排行榜和搜索数据（网络请求）
  - 调用 skillhub skill evaluation/reports 获取深度评估（网络请求，可选）
  - 将推荐简报写入本地文件和外部服务（Obsidian/IMA/飞书），需用户配置对应凭证
  - 推荐结果中不包含原始记忆内容，仅记录关键词匹配数量

  差异化特色：
  - 国内优先：重点推荐适配国内生态的技能（飞书/微信/钉钉/小红书/抖音等）
  - 活跃开发者：发现高产开发者及其代表作，追踪值得关注的技能作者
  - 双实验室安全审计：调用 skillhub skill reports 获取安全评估
  - AI 6维质量评估：调用 skillhub skill evaluation 获取可用性/安全性/文档等评分
  - 3级权重记忆碰撞：project_memory×3 / topics×2 / user_profile×1

  数据源：SkillHub.cn API（via skillhub CLI，结构化 JSON，0 token 消耗）
  扫描规模：7 排行榜 × 100 + 11 分类 × 20 搜索 + 6 关键词 × 20 搜索 ≈ 1000+ 候选
  推荐维度：趋势飙升 / 新星上线 / 国内优先 / 活跃开发者 / 记忆碰撞 / 痛点匹配 / 官方认证
  去重机制：7 天跨维度去重
  三处存放：Obsidian inbox / IMA FIM 知识库 / 飞书云文档

  权限声明：需要网络访问（skillhub CLI）、本地文件读写（data 目录）、环境变量（IMA_OPENAPI_CLIENTID/IMA_OPENAPI_APIKEY/OBSIDIAN_VAULT_PATH/TRAE_MEMORY_PATH）

  触发场景：
  - 用户希望每日收到 SkillHub 国内技能推荐
  - 用户希望发现适配国内的 AI 技能
  - 用户希望追踪活跃开发者
  - 用户说"SkillHub 日报"、"国内技能推荐"、"有什么新 Skill"

  Do NOT use for ClawHub 平台推荐（用 clawhub-daily）、通用代码开发、非 Skill 项目。
---

# SkillHub Daily 国内技能洞察 v7.0

> 每日扫描 SkillHub.cn 7.5 万+ 技能生态 | 与 ClawHub Daily 互补：聚焦**国内适配**、**活跃开发者**、**双实验室安全审计**

## 数据源

### skillhub CLI 排行榜 + 搜索 API

```bash
# 7 种排行榜，每种 100 条
skillhub skill rankings --type hot         # 热门榜
skillhub skill rankings --type newest      # 最新上线
skillhub skill rankings --type trending    # 趋势飙升
skillhub skill rankings --type featured    # 编辑精选
skillhub skill rankings --type recommended # 平台推荐

# 11 分类搜索，每种 20 条
skillhub search "知识管理" --json --search-limit 20
skillhub search "办公效率" --json --search-limit 20
skillhub search "内容创作" --json --search-limit 20
# ... 共 11 个分类

# 6 个记忆关键词搜索，每种 20 条
skillhub search "飞书" --json --search-limit 20
skillhub search "Python" --json --search-limit 20
skillhub search "审计" --json --search-limit 20
# ... 共 6 个关键词

# 深度评估（对最终 8 个推荐调用）
skillhub skill evaluation <slug> --json    # AI 6维质量评估
skillhub skill reports <slug> --json       # 双实验室安全审计
```

### 返回数据结构（每个技能）

```json
{
  "slug": "self-improving-agent-cn",
  "name": "Self Improving Agent CN",
  "ownerName": "zhengxinjipai",
  "version": "1.0.0",
  "source": "clawhub",
  "category": "ai-agent",
  "subCategories": [{"key": "agent-memory", "name": "记忆增强"}],
  "description": "AI自我改进与记忆系统...",
  "description_zh": "AI自我改进与记忆系统...",
  "downloads": 37072,
  "installs": 9905,
  "stars": 49,
  "score": 3621.57,
  "labels": {"requires_api_key": "false"},
  "verified": false,
  "claimable": false,
  "created_at": 1773023560715,
  "updated_at": 1783822732293,
  "homepage": "https://api.skillhub.cn/zhengxinjipai/self-improving-agent-cn"
}
```

### 分类体系

| category | 中文名 |
|----------|--------|
| knowledge-management | 知识管理 |
| office-efficiency | 办公效率 |
| content-creation | 内容创作 |
| data-analysis | 数据分析 |
| ai-agent | AI Agent |
| design-media | 设计多媒体 |
| professional | 行业专业 |
| dev-programming | 开发编程 |
| life-service | 生活服务 |
| it-ops-security | IT运维安全 |
| business-ops | 商业运营 |

## 每日扫描策略

### 扫描覆盖

| 来源 | 数量 | 用途 |
|------|------|------|
| 7 排行榜 × 100 | 700 | 热门/趋势/精选/推荐 |
| 11 分类 × 20 搜索 | 220 | 长尾覆盖 |
| 6 关键词 × 20 搜索 | 120 | 记忆碰撞精准补充 |
| **合并去重后** | **~550** | 独立技能候选池 |

### 量化指标

| 指标 | 来源 | 用途 |
|------|------|------|
| downloads | API 字段 | 热度排序 |
| installs | API 字段 | 实际使用量 |
| stars | API 字段 | 用户口碑 |
| score | API 字段 | 平台综合评分 |
| installs/downloads | 计算 | 安装转化率 |
| created_at | API 字段 | 新鲜度 |
| updated_at | API 字段 | 活跃度 |

## 7 维度推荐算法

### D1: trending_surge × 2 — 趋势飙升

同时登上 hot + trending 双榜的技能，score 降序取 Top 2

### D2: newcomers × 1 — 新星上线

newest 榜 + created_at 在 30 天内 + installs > 100，installs 降序取 Top 1

### D3: scene_match × 2 — 痛点场景匹配

7 大痛点场景库匹配，不同场景各取 Top 1

### D4: memory_collision × 1 — 记忆碰撞

3 级权重关键词碰撞：project_memory×3 / topics×2 / user_profile×1

### D5: china_first × 1 — 国内优先（最低门槛：50 安装或 10 星）

国内适配信号检测（飞书/微信/钉钉/小红书/抖音等 25 个关键词），候选不足时降级

### D6: active_developer × 1 — 活跃开发者

按 ownerName 聚合，活跃度 = 技能数 + 总安装/1000 + 上榜次数×5，推荐最活跃开发者的代表作

### D7: tencent_official × 1(可选) — 官方认证

verified=true，候选为 0 时名额分给 D3

## 7 天去重机制

加载过去 7 天 `data/recommended/*.json` 中的 slug 集合，推荐时过滤已推荐的技能。

## 记忆碰撞实现

3 级权重关键词提取：
- project_memory.md (weight=3) — 项目约束、技术决策
- topics.md (weight=2) — 近期任务关键词
- user_profile.md (weight=1) — 用户偏好、技术栈

碰撞算法：对每个技能在 description_zh + name + category + subCategories 中搜索关键词，累加权重。

## 活跃开发者发现

按 ownerName 聚合所有扫描到的技能，计算活跃度分数，在简报中展示 Top 5 开发者速览（技能数/总安装/上榜次数/代表作）。

## 使用模式

### Interactive 模式

触发词："SkillHub 日报"、"国内技能推荐"、"有什么新 Skill"

### Cron 定时任务

每天北京时间 06:50 执行，TRAE Schedule ID: be17fc27

```
执行步骤：
1. python scripts/fetch_skillhub_cn.py --output data/snapshots
2. python scripts/daily_recommend.py --data-dir data --skip-eval
3. 三处存放：Obsidian inbox / IMA FIM 知识库 / 飞书云文档
```

## 三处存放

| 目的地 | 方式 | 配置 |
|--------|------|------|
| Obsidian inbox | 写 Markdown + frontmatter | OBSIDIAN_VAULT_PATH 环境变量（默认 E:\Obsidian\md\inbox） |
| IMA FIM 知识库 | 两步流程（create_note + add_knowledge） | IMA_OPENAPI_CLIENTID / IMA_OPENAPI_APIKEY 环境变量 |
| 飞书云文档 | lark-cli 或 lark-doc skill | 飞书授权 |

三处存放各自独立 try/except，一处失败不阻断其他。

## 输出物

- `data/snapshots/YYYY-MM-DD.json` — 扫描快照（550+ 独立技能）
- `data/recommended/YYYY-MM-DD.json` — 8 个推荐 + 元数据
- `data/recommended/YYYY-MM-DD.md` — 中文结构化简报
- `E:\Obsidian\md\inbox\SkillHub-Daily-YYYY-MM-DD.md` — Obsidian 本地
- IMA FIM 知识库笔记
- 飞书云文档

## 依赖

- skillhub CLI（`npm i -g skillhub`，已全局安装并认证）
- Python 3.8+
- 已登录 skillhub auth（`skillhub auth login`）

## 与 ClawHub Daily 互补

| | SkillHub Daily | ClawHub Daily |
|---|---|---|
| 平台 | SkillHub.cn（7.5 万+） | ClawHub.ai（500） |
| 特色 | 🇨🇳 国内优先 / 👤 开发者 / 🔬 安全审计 | 🦞 口碑精品 / 趋势洞察 |
| 评估 | AI 6维评分 + 双实验室审计 | 口碑率 + 活跃度 |
