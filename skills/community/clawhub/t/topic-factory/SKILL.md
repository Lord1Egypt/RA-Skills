---
name: topic-factory
version: 1.0.0
description: |
  跨平台自媒体选题日报系统 — 每天自动从 6 大数据源（头条/微博/B站/抖音/知乎/36氪）
  抓取热点新闻，按 6 大类 119 词关键词库筛选，LLM 生成抖音钩子和公众号标题，
  输出 Markdown 选题日报，推送到飞书 webhook。
  
  适用场景：
  - 自媒体运营：每天 10 个候选选题，⭐ 优先 3 个
  - 双平台发布：抖音 60s 口播 + 公众号 2000-3000 字图文
  - "只看数据说话"人设：严格禁词清单 + 数据点必填
  - 跨平台热点捕获：6 大数据源 + 36h 时间窗口过滤
  
  本 skill 含完整工作流：4 个脚本 + 4 个 cron 配置 + 飞书 webhook 推送 + 限流 fallback。
---

# 跨平台自媒体选题日报系统 (topic-factory)

每天凌晨自动从 6 大公开数据源抓取热点，按关键词库筛选行业新闻，LLM 生成抖音钩子 + 公众号标题 + 数据点，输出 Markdown 选题日报，飞书推送 ⭐ 优先选题。

## 核心特性

- **6 大数据源**：头条 / 微博 / B站 / 抖音 / 知乎 / 36氪（公开 JSON / RSS API）
- **6 大类 119 词关键词库**：财经投资 / 房产 / 政策 / AI科技 / 中国大模型公司
- **LLM 钩子**：60s 口播钩子（≤30 字，含数字+时间戳）+ 公众号标题（≤25 字，无句末标点）
- **36h 时间窗口**：36氪 RSS 编辑推荐段旧文章过滤（防止"京东方 IPO"等 8/14 旧数据霸占选题）
- **禁用词后处理**：6 个常见违规词 → 同义中性词（"背后" → "原因"）
- **飞书 webhook 推送**：支持限流 fallback（输出 markers 给 cron agent 推私聊）
- **3 次重试机制**：shell wrapper 自动重试 + send_alert 告警
- **2 个 cron 推荐**：04:00 主任务 + 08:00 兜底（处理 LLM api 过载）

## 系统架构

```
┌─────────────────────────────────────────────────┐
│                 每日工作流                         │
├─────────────────────────────────────────────────┤
│                                                  │
│  [04:00 cron] → run_daily.sh                    │
│                  ↓                                │
│                  generate_topics.js              │
│                    ├─ 6 数据源并发抓取              │
│                    ├─ 关键词匹配 + 流量分排序         │
│                    ├─ LLM 钩子 + 标题 + 数据点        │
│                    └─ 输出 YYYYMMDD_topics.md      │
│                                                  │
│  [08:00 cron] → 兜底重试（若 04:00 失败）         │
│                                                  │
│  [09:00 cron] → notify_feishu.js                │
│                  ├─ 解析 ⭐ 选题                  │
│                  ├─ 飞书 webhook 推送              │
│                  └─ 失败时输出 fallback markers    │
│                                                  │
│  [23:55 cron] → archive_unused.js              │
│                  ├─ 扫未标注 ADOPTED 选题          │
│                  └─ 移到 history/                │
│                                                  │
└─────────────────────────────────────────────────┘
```

## 快速开始

### 1. 依赖安装

```bash
# Node.js 16+（推荐 18 LTS）
node --version

# 无需 npm 依赖（纯 Node 标准库 + 内置 fetch）
```

### 2. 部署脚本

```bash
# 推荐：~/.openclaw/workspace/.analysis/topic_factory/
mkdir -p ~/.openclaw/workspace/.analysis/topic_factory
mkdir -p ~/.openclaw/workspace/claude-hub/topics

cp scripts/*.js scripts/*.sh ~/.openclaw/workspace/.analysis/topic_factory/
chmod +x ~/.openclaw/workspace/.analysis/topic_factory/run_daily.sh
```

### 3. 配置环境变量

```bash
# LLM API（如使用 Anthropic Claude）
export ANTHROPIC_AUTH_TOKEN="sk-ant-..."
export ANTHROPIC_BASE_URL="https://api.anthropic.com"  # 默认
export LLM_MODEL="claude-3-5-sonnet-20241022"          # 默认

# 写入 ~/.zshrc 或 ~/.bashrc 永久生效
echo 'export ANTHROPIC_AUTH_TOKEN="sk-ant-..."' >> ~/.zshrc
```

### 4. 配置飞书 webhook（可选）

如果不用推送，可跳过；用的话：

```bash
# 编辑 notify_feishu.js 第 32 行
const FEISHU_WEBHOOK = 'https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_TOKEN';
```

获取方式：飞书群 → 群设置 → 群机器人 → 添加机器人 → 自定义机器人 → 复制 webhook URL

### 5. 第一次运行

```bash
cd ~/.openclaw/workspace/.analysis/topic_factory
bash run_daily.sh

# 验证
ls -la ~/.openclaw/workspace/claude-hub/topics/  # 应有 YYYYMMDD_topics.md
cat ~/.openclaw/workspace/claude-hub/topics/$(date +%Y%m%d)_topics.md
```

### 6. 配置定时任务（推荐）

```bash
# 04:00 每日生成（主任务）
# 08:00 兜底重试（防 LLM 过载）
# 09:00 飞书推送
# 23:55 归档未选用

# OpenClaw cron 配置示例
openclaw cron add "04:00 topic-factory main" \
  --schedule "0 4 * * *" \
  --tz "Asia/Shanghai" \
  --command "bash ~/.openclaw/workspace/.analysis/topic_factory/run_daily.sh"

openclaw cron add "08:00 topic-factory fallback" \
  --schedule "0 8 * * *" \
  --tz "Asia/Shanghai" \
  --command "bash ~/.openclaw/workspace/.analysis/topic_factory/run_daily.sh"

openclaw cron add "09:00 topic-factory feishu" \
  --schedule "0 9 * * *" \
  --tz "Asia/Shanghai" \
  --command "node ~/.openclaw/workspace/.analysis/topic_factory/notify_feishu.js"
```

## 6 大数据源说明

| 数据源 | 抓取方式 | API 类型 | 特殊处理 |
|---|---|---|---|
| 头条 | HTTP JSON | 公开榜单 API | Top 50，按热度排序 |
| 微博 | HTTP JSON | 公开热搜 API | Top 50 |
| B站 | HTTP JSON | 公开热搜 API | Top 50 |
| 抖音 | HTTP JSON | 公开榜单 API | Top 50 |
| 知乎 | HTTP JSON | 公开热榜 API | Top 50 |
| 36氪 | RSS XML | 公开 RSS feed | **36h 时间窗口过滤** |

### 36氪特别说明

36氪 RSS feed 结构：
- 第 1-10 条 = "编辑推荐"（混合多日数据，不按时间排序）
- 第 11-30 条 = 按时间倒序的快讯（最新在前）

不加时间窗口会导致 8/14、8/15 的旧文章命中关键词后霸占选题。`fetch36krRSS` 内置 36h 时间过滤：

```javascript
const TIME_WINDOW_HOURS = 36;
const cutoffMs = Date.now() - TIME_WINDOW_HOURS * 60 * 60 * 1000;
// 时间窗口过滤：跳过 36h 之前的文章
```

## 6 大类 119 词关键词库

| 类目 | 名称 | 词数 | 典型词 |
|---|---|---|---|
| A | 财经投资 | 31 | 半导体 / 存储 / 新质生产力 / 医疗 / A股 / 财报 |
| B | 房产 | 28 | 城市更新 / 乡村振兴 / REITs / 楼市 / 保障房 |
| C | 政策类 | 9 | 楼市新政 / 公积金 / 降息 / 央行 / 证监会 |
| D | AI 科技 | 30 | AI / 大模型 / GPT / Claude / Gemini / 算力 / GPU |
| E | 中国大模型公司 | 16 | 智谱 / Kimi / 百川 / DeepSeek / Qwen / 豆包 |

**优先级排序**（流量分）：D > A > B > C > E

可在 `generate_topics.js` 第 46-100 行自定义关键词库。

## LLM 集成

### 3 个 LLM 调用点

1. **钩子文案（60s 口播）**：20-30 字，含数字+时间戳
2. **公众号标题候选**：2 个，15-25 字，无句末标点
3. **数据点补充**：3 个，含数字 + 时间戳 + 权威来源

### Prompt 模板

```javascript
// generate_topics.js 第 661 行 generateHookCopy()
const prompt = `你是一个抖音/公众号自媒体运营专家，只看数据说话。
【约束清单】
1. 禁止词：颠覆 / 沉默 / 真相 / 背后 / 答案 / 原来如此 / 万万没想到
2. 禁止句末标点：！? 
3. 禁止主观判断
【输出】JSON: { hook, gzhTitles: [t1, t2] }`;
```

### 环境变量

| 变量 | 必填 | 默认值 | 说明 |
|---|---|---|---|
| `ANTHROPIC_AUTH_TOKEN` | ✅ | - | API key |
| `ANTHROPIC_BASE_URL` | - | `https://api.anthropic.com` | API endpoint |
| `LLM_MODEL` | - | `claude-3-5-sonnet-20241022` | 模型名 |

### 限流处理

LLM API 有限流，重试 2 次（间隔 3 秒），仍失败则用模板兜底。

## 飞书 webhook 推送

### 推送内容

从每天的 `YYY主题_topics.md` 提取 ⭐ 推送选题（前 10 个），拼接后发到飞书：

```
📋 自媒体选题日报
日期：2026-08-17 周日

#1 抖音「60岁AI动画赛道新人」7655448热度
钩子：60岁零基础入局AI动画，2026年8月单条视频播放破百万

#2 抖音「一条AI短片演绎时间焦虑」8856859热度
钩子：2026年8月，885万热度，一条AI短片呈现时间焦虑

#3 头条「问界儿童车即将上市」546.0万热度
钩子：546万人热议，问界儿童车8月正式上市，价格区间曝光
...
```

### 限流 fallback

飞书 webhook 偶发限流（`code=11232`，`psm=lark.oapi.app_platform_runtime`），脚本检测后输出 fallback markers：

```
=== FALLBACK_MESSAGE_START ===
📋 自媒体选题日报
...
=== FALLBACK_MESSAGE_END ===
```

cron agent 检测到 markers 时，把内容直接推用户私聊（plain text，不加表格）。

## 4 个 cron 推荐配置

| 时间 | 任务 | cron 表达式 | 备注 |
|---|---|---|---|
| 04:00 | 主任务生成 | `0 4 * * *` | LLM 偶发过载 |
| 08:00 | 兜底重试 | `0 8 * * *` | 处理 04:00 失败 |
| 09:00 | 飞书推送 | `0 9 * * *` | 早上查看 |
| 23:55 | 归档未选用 | `55 23 * * *` | 每日清理 |

**时区：Asia/Shanghai**（避免 UTC 算日期错位）

## 输出文件结构

```
~/.openclaw/workspace/claude-hub/topics/
├── YYYYMMDD_topics.md      # 每日选题日报（当天）
└── history/
    └── YYYYMMDD_unused.md  # 未选用归档（每天 23:55 生成）
```

### Markdown 选题日报结构

```markdown
# 自媒体选题日报 · 2026-08-17 周日
文件路径：~/.openclaw/workspace/claude-hub/topics/20260817_topics.md

## 今日总览
- 选题数量：10 个（推送 10 个）
- 分布：A 财经 5 / B 房产 0 / C 政策 0 / D AI 5

---

## 选题 1 · ⭐推送
**抖音「60岁AI动画赛道新人」7655448热度**

- **原始命中**：D AI科技(命中词：AI)
- **延伸方向**：A 财经投资、B 房产、C 政策类
- **目标平台**：抖音短视频 + 公众号图文

**钩子文案（用户可直接用）**
- 60岁零基础入局AI动画，2026年8月单条视频播放破百万

**3 个数据点（必填）**
1. 2025年全球AI内容创作工具市场规模达XX亿元（来源：IDC）
...

**来源链接**
- https://...

**用户操作**
- 想采用本选题：把注释改为 `<!-- __ADOPTED__: 选题 1 ✓ -->`
- 不采用：保持注释不变，编辑 .md 文件加备注

<!-- __ADOPTED__: 选题 1 -->
- [ ] 备注修改意见
- [ ] 触发 LLM 写完整公众号长文
```

## 故障排查

### Q1: 36氪数据总是 8/14、8/15 旧数据

**根因**：36氪 RSS feed 前 10 条是"编辑推荐"，混合多日数据，不按时间排序。

**修复**：`fetch36krRSS` 加 36h 时间窗口（已内置）。验证日志：
```
[36氪] 获取 10 条（过滤 1 条 36h 之前旧文章）
```

### Q2: LLM API 频繁 429 / overloaded

**修复**：
- 04:00 + 08:00 双 cron 兜底
- 单次失败重试 2 次（间隔 3 秒）
- 最终失败用模板兜底（钩子函数 `fallbackHookCopy`）

### Q3: 飞书 webhook 限流 code=11232

**修复**：脚本输出 fallback markers，cron agent 推用户私聊（plain text）。

### Q4: 钩子 / 公众号标题含禁用词

**修复**：内置 `sanitizeForbiddenWords` 后处理：
- `背后` → `原因`
- `真相` → `事实`
- `答案` → `回复`
- `原来如此` → `原来这样`
- `万万没想到` → `没想到`
- `太可怕了` → `值得关注`

### Q5: 04:00 cron 频繁失败

**根因**：minimax 私有 API 偶发 rate_limit / overloaded。

**修复**：08:00 兜底 cron 是关键。即使 04:00 失败，08:00 重生成。

### Q6: 钩子超 30 字

**修复**：`truncateHook(text, 30)` 智能截断到最近标点。

## 隐私与免责声明

### 数据源合规性

- 所有数据源（头条/微博/B站/抖音/知乎/36氪）均为公开 API / RSS
- 仅抓取公开热榜，不抓取用户隐私数据
- 关键词匹配完全本地，无第三方数据上报

### 飞书 webhook

- 推送内容由用户配置（公开 webhook URL）
- 推送内容含钩子文案（用户生成或 LLM 增强）
- 用户负责确保 webhook 群组合规

### LLM 使用

- 默认调用 Anthropic Claude API
- 选题内容（公开新闻）发送至 LLM
- LLM 返回钩子/标题/数据点（可能含虚构，需用户核实）

### 免责声明

本 skill 生成的选题内容仅供参考，不构成投资建议。发布前请用户核实数据真实性。

## 性能指标

| 操作 | 耗时 |
|---|---|
| 6 数据源并发抓取 | ~3-5 秒 |
| 关键词匹配 + 流量分排序 | < 1 秒 |
| LLM 钩子 / 标题生成（10 个） | ~20-30 秒 |
| 数据点生成（10 个 × 3） | ~30-60 秒 |
| 整体生成 | ~60-90 秒 |
| 飞书 webhook 推送 | < 1 秒 |

## 许可

MIT License
