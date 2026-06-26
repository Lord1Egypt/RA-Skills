---
name: wechat-content-studio
description: 微信公众号内容工作室 — 支持多来源权威搜索、多站点文章抓取、AI 改写、封面生成、智能排版发布的一站式工具
author: 模型猎人
version: 2.2.0
allowed-tools: Bash,Read,Write
---

# 微信公众号内容工作室 (WeChat Content Studio)

一站式公众号内容创作工具，支持**多来源权威搜索**（10 大分类 50+ 来源）和**多站点文章抓取**，自动合并、**AI 改写**、**封面生成**、**智能排版发布**。

默认产出根目录为 **`~/WorkBuddy/<技能文件夹名>/`**（与 `~/.workbuddy/skills` 下本技能目录名一致）。**搜索 / 链接抓取 / workflow**（`search`、`links`、`workflow`）在根目录下再建一层：**合并**时为 `sanitize(合并后标题)/`，**不合并**时为 `1_标题/`、`2_标题/` 子目录，其内为 `article.md`；其它命令（如 `generate-cover`、`extract` 调用多站点抓取）仍按各子命令参数或默认根目录行为。

## 核心工作流

```bash
# 最简用法：多来源搜索 → 抓取 → 合并 → 改写 → 封面 → 排版 → 发布
node {baseDir}/scripts/main.js search "RAG 幻觉治理" --merge
```

## 命令一览

### 1. 多来源搜索（推荐）

```bash
# 默认搜索（高质量渠道：微信全网 + 知乎 + 少数派等 + 开发者社区）
node {baseDir}/scripts/main.js search "人工智能" --merge

# 叠加微信公众号头部号定向搜索
node {baseDir}/scripts/main.js search "大模型" --sources high_quality_channels,wechat_top --merge

# 指定搜索分类
node {baseDir}/scripts/main.js search "大模型" --sources wechat_top,intl_ai_official,academic --merge

# 搜索所有 10 大分类
node {baseDir}/scripts/main.js search "AI Agent" --all-sources --merge

# 列出所有可用搜索分类
node {baseDir}/scripts/main.js search "any" --list-sources

# 仅搜索微信公众号头部号（Brave site:mp.weixin.qq.com + 各账号名）
node {baseDir}/scripts/main.js search "RAG" --wechat-only --merge

# 搜索不发布
node {baseDir}/scripts/main.js search "大模型" --merge --no-auto

# 调整每源抓取数和总上限
node {baseDir}/scripts/main.js search "LLM" --count 5 --total-max 30 --merge
```

#### 搜索分类

| 分类 Key | 分类名称 | 包含来源 |
|----------|---------|----------|
| `high_quality_channels` | 高质量内容渠道 | 微信公众号 (全网)、知乎、少数派、掘金、InfoQ、极客公园、虎嗅、36 氪 |
| `wechat_top` | 微信公众号头部账号 | 机器之心、量子位、AI 科技评论、新智元、DataFunTalk、PaperWeekly、深度学习自然语言处理 |
| `cn_tech_blog` | 中文技术博客 | CSDN、博客园、掘金、知乎专栏、SegmentFault、简书、少数派 |
| `cn_bigtech` | 国内大厂官方号 | 阿里达摩院、腾讯 AI Lab、百度 AI、字节 AILab、华为诺亚方舟、智谱 AI |
| `intl_ai_official` | 国际头部 AI 公司 | OpenAI Blog、Google AI Blog、Meta AI、Anthropic Blog、Stability AI |
| `intl_media` | 国际权威媒体 | TechCrunch、MIT Technology Review、The Verge、Reuters 中文、Bloomberg 中文、FT 中文、财新 |
| `cn_tech_media` | 国内科技媒体 | 36 氪、品玩、极客公园、虎嗅、钛媒体、InfoQ |
| `dev_community` | 开发者社区 | Hacker News (score≥100)、GitHub Trending、Product Hunt、V2EX |
| `platform_blogs` | 平台官方 Blog | GitHub Blog、Hugging Face Blog |
| `academic` | 学术/研究 | arXiv、Papers With Code |
| `investment` | 投资/商业 | 投中网、IT 桔子 |
| `cn_tech_other` | 其他中文科技媒体 | 雷锋网、亿欧、CSDN AI 专栏 |

默认分类：`high_quality_channels` + `dev_community`（含微信公众号全网与知乎等；可加 `--sources wechat_top` 定向头部号）

#### 搜索引擎

**默认推荐：WorkBuddy WebSearch（开箱即用）**

| 来源类型 | 搜索方式 |
|---------|---------|
| 微信公众号（定向头部号） | WorkBuddy：`"公众号名" 关键词 site:mp.weixin.qq.com` |
| 微信公众号（全网） | WorkBuddy：`关键词 site:mp.weixin.qq.com` |
| 知乎（专栏 + 问答等） | WorkBuddy：`关键词 site:zhihu.com` |
| CSDN、博客园、掘金等 | WorkBuddy：`关键词 site:domain` |
| Hacker News | Algolia HN Search API |
| GitHub Trending | HTML 抓取 + 关键词过滤 |
| Product Hunt | WorkBuddy：`关键词 site:producthunt.com` |
| arXiv | OpenSearch API |

**优势**：
- ✅ 开箱即用，无需代理配置
- ✅ 无 Brave 限流风险（429 错误）
- ✅ 中文搜索结果更优
- ✅ 与 `keyword-search` 技能共享搜索逻辑

**备选方案：Brave Search**

如 WorkBuddy 搜索效果不理想，可切换回 Brave Search：

```bash
export USE_BRAVE_SEARCH=true
node {baseDir}/scripts/main.js search "关键词" --engine brave
```

Brave 需配置代理（默认 `http://127.0.0.1:7890`），遇 429 限流时会自动退避重试。

### 2. 链接抓取

```bash
node {baseDir}/scripts/main.js links "URL" --merge
node {baseDir}/scripts/main.js links "URL1,URL2" --merge
node {baseDir}/scripts/main.js links --file urls.txt --merge
node {baseDir}/scripts/main.js links "URL" --merge --no-auto
```

### 3. 多站点抓取

```bash
node {baseDir}/scripts/main.js extract "URL"
node {baseDir}/scripts/main.js extract "URL" --publish --theme github
node {baseDir}/scripts/main.js extract "URL" --json
```

支持站点：微信公众号、CSDN、博客园、掘金、知乎、简书、思否、少数派，及通用网页。

### 4. AI 改写

```bash
node {baseDir}/scripts/main.js rewrite ./path/to/article.md
```

### 5. 封面生成

```bash
node {baseDir}/scripts/main.js generate-cover --title "文章标题" --content "内容摘要"
node {baseDir}/scripts/main.js generate-tech --description "RAG 系统架构"
```

### 6. 发布

```bash
node {baseDir}/scripts/main.js publish ./path/to/article.md
node {baseDir}/scripts/main.js publish-browser ./path/to/article.md
```

### 7. 一键工作流

```bash
node {baseDir}/scripts/main.js workflow search \
  --keyword "人工智能" --count 5 --merge --rewrite --generate-cover --publish

node {baseDir}/scripts/main.js workflow links \
  --urls "URL1,URL2" --merge --rewrite --generate-cover --publish
```

## 输出结构

**搜索 / 链接抓取 / workflow**（`--merge`）：默认 `--output` 为 `~/WorkBuddy/<技能文件夹名>/`，其下再建 **`文章标题/`**（文件名经 `sanitize`），例如：

```
~/WorkBuddy/wechat-content-studio/
└── <文章标题>/
    ├── article.md              # 合并后的正文（含 frontmatter）
    ├── article_rewritten.md    # AI 改写版
    ├── merged_articles.json    # 合并的原始数据
    ├── images/
    │   └── cover.jpg           # 封面图（若生成）
    └── metadata.json           # 若某流程写出
```

**`--no-merge`**：在同一根目录下建 **`1_标题/`、`2_标题/`** 各含 `article.md`，避免多篇混在同一目录。

## 模块说明

| 模块 | 目录 | 功能 |
|------|------|------|
| 多来源搜索 | `search/multi_source_search.js` | Brave Search（site:）、HN/GitHub/arXiv API |
| 搜索来源配置 | `search/search_sources.json` | 多分类来源（含中文技术博客 CSDN/博客园等） |
| 微信搜索 | — | 已并入 `multi_source_search`（Brave） |
| 文章合并 | `search/merge_articles.js` | 多篇文章智能合并 |
| 抓取 | `extractor/` | 多站点文章提取（通过 multi-site-extractor） |
| 改写 | `rewriter/` | AI 改写、去 AI 味 |
| 配图 | `image/` | 万象 2.6 封面生成（含复用逻辑） |
| 发布 | `publisher/` | wenyan-cli / browser-use 发布 |
| 排版 | 外部依赖 | `wechat-typeset-pro` 排版技能 |

## 环境变量

启动时自动从 `~/.openclaw/.env` 加载，无需手动 export。

| 用途 | 变量名 | 说明 |
|------|--------|------|
| 微信 AppID | `WECHAT_APP_ID` | 发布必须 |
| 微信 AppSecret | `WECHAT_APP_SECRET` | 发布必须 |
| 阿里云 DashScope | `DASHSCOPE_API_KEY` | 封面生成必须 |
| LLM API Key | `OPENAI_API_KEY` | AI 改写必须 |
| LLM Base URL | `OPENAI_BASE_URL` | 默认 `https://api.openai.com/v1` |
| LLM 模型名 | `OPENAI_MODEL` | 默认 `gpt-4o` |
| 联网搜索代理 | `HTTPS_PROXY` / `HTTP_PROXY` | 访问 Brave/GitHub 等；未设时默认 `http://127.0.0.1:7890` |
| Brave 请求间隔 | `BRAVE_SEARCH_MIN_INTERVAL_MS` | 两次 Brave 请求最小间隔（毫秒），默认 `3200`，遇 429 可调大 |

**.env 查找顺序：**
1. `OPENCLAW_ENV_FILE`（若设置）
2. 技能根目录 `.env`
3. `~/.openclaw/.env`
4. `~/.workbuddy/.env`

## 依赖安装

```bash
# Node.js 依赖
cd {baseDir} && npm install

# wenyan-cli（发布功能）
npm install -g @wenyan-md/cli

# Python 依赖（多站点抓取）
pip install requests beautifulsoup4 lxml markdownify readability-lxml

# 浏览器自动化（可选）
uvx browser-use install
```

## 注意事项

1. **发布凭证**：首次使用需配置微信公众号 API 凭证
2. **IP 白名单**：发布功能需将服务器 IP 添加到微信公众号后台白名单
3. **封面复用**：封面生成失败时自动复用上次已上传的封面图
4. **Brave 限流**：短时间大量搜索可能返回 HTTP 429，脚本会退避重试；请降低 `--count`、少用 `--all-sources`，或隔一段时间再搜
5. **版权合规**：生成的文章请确保符合版权法规，建议深度改写
6. **搜索引擎选择**：默认使用 WorkBuddy WebSearch（无需配置），如需切换回 Brave Search，设置 `USE_BRAVE_SEARCH=true`

## 技能依赖

- `multi-site-extractor` — 多站点文章提取
- `wechat-typeset-pro` — 专业排版（多主题）
- 阿里云万象 2.6 — 封面图生成
- wenyan-cli / browser-use — 发布到公众号

## 推荐工作流

### 方案 A：使用 keyword-search 技能（推荐）

```bash
# 1. 使用 keyword-search 搜索文章 URL
keyword-search 搜索 "RAG 幻觉治理" --limit 10

# 2. 使用 wechat-content-studio 处理搜索到的 URL
node {baseDir}/scripts/main.js links "URL1,URL2,URL3" --merge

# 3. 后续流程（改写、封面、发布）
node {baseDir}/scripts/main.js rewrite ./wechat-content-studio/文章标题/article.md
node {baseDir}/scripts/main.js generate-cover --title "文章标题"
```

### 方案 B：Agent 直接使用 web_search 工具

Agent 在执行 `wechat-content-studio` 的搜索任务时：

1. **不调用** `node scripts/main.js search` 命令
2. **直接使用** `web_search` 工具搜索：
   ```
   query: "RAG 幻觉治理" site:mp.weixin.qq.com OR site:zhihu.com OR site:juejin.cn
   ```
3. **提取** 搜索结果中的 URL 列表
4. **调用** `wechat-content-studio links` 命令处理这些 URL

详见 `scripts/search/workbuddy_search_workflow.md`
