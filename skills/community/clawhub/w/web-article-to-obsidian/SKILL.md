---
name: web-article-to-obsidian
version: 2.0.0
description: 网页文章一体化抓取存入Obsidian知识库。集成Playwright/Tavily/Firecrawl/Browser四种提取引擎，支持微信公众号/富途牛牛/雪球/通用网页，自动行业分类、导航清理、双层存储。统一替代wechat-article-extractor、wechat-mp-reader、article-to-obsidian三个技能。
category: data-science
author: apollo
created: 2026-04-28
updated: 2026-04-28
supersedes:
  - wechat-article-extractor
  - wechat-mp-reader
  - article-to-obsidian
---

# 网页文章一体化抓取 → Obsidian

集成三套提取方案，按优先级自动回退，一键完成「URL → 提取 → 清洗 → 行业分类 → Obsidian存储」全流程。

## 触发条件

- 用户发送文章链接（URL）
- 提及"存obsidian"、"保存文章"、"抓取文章"、"放入知识库"等
- 提及"微信公众号"文章读取需求

## 支持的平台

| 平台 | 识别关键词 | 内容选择器 | 特殊处理 |
|------|-----------|-----------|---------|
| 微信公众号 | `mp.weixin.qq.com` | `#js_content` | URL追加`?scene=1` |
| 富途牛牛 | `news.futunn.com` | `.inner.origin_content` | URL清理跟踪参数；分离作者/时间；行情组件移除 |
| 雪球 | `xueqiu.com` | `.article__bd__detail` | 登录墙绕过 |
| 东方财富 | `eastmoney.com` | `.txtinfos` / `.newsContent` | 广告清理 |
| 通用网页 | 其他 | `article` / `main` / `body` | 智能正文识别 |

## 提取引擎优先级链（核心创新）

**按成功率和速度排序，自动回退**：

```
方法1: Hermes browser_navigate (最快，内置工具，无需外部依赖)
  ↓ 失败
方法2: Playwright headless (反检测能力强，支持JS渲染)
  ↓ 失败
方法3: Tavily API (住宅IP池，绕过反爬，需API Key)
  ↓ 失败
方法4: Firecrawl CLI (浏览器渲染引擎，需已安装)
  ↓ 失败
方法5: web_extract (纯HTTP提取，最后兜底)
```

### 方法详解

#### 方法1: Hermes browser_navigate（首选）
- 使用 Hermes 内置 `browser_navigate` → `browser_snapshot` 工具链
- 速度最快，零外部依赖
- 适合：微信、富途、雪球等JS渲染页面
- 调用方式：直接使用 Hermes 工具，无需Python脚本

#### 方法2: Playwright headless
- 完整浏览器环境，反自动化检测绕过
- 支持自定义等待策略和选择器
- 适合：方法1被反爬拦截时

#### 方法3: Tavily API
- 住宅IP池，模拟真实用户
- 无需浏览器，API直取
- 需要 `TAVILY_API_KEY` 环境变量
- 适合：微信验证码拦截、IP被封时

#### 方法4: Firecrawl CLI
- 云端浏览器渲染+JS执行
- `firecrawl scrape "<url>?scene=1" --only-main-content -o <output>.md`
- 需要 firecrawl 已安装并配置

#### 方法5: web_extract
- Hermes 内置 `web_extract` 工具
- 纯HTTP抓取，不支持JS渲染
- 仅适合静态页面，最后兜底

## 微信文章URL规范化规则

**铁律**：URL必须带 `?scene=1` 参数，否则触发验证码。

| 原始URL | 修正后 | 规则 |
|---------|--------|------|
| `.../s/abc123` | `.../s/abc123?scene=1` | 无参数→追加`?scene=1` |
| `.../s/abc123?chksm=xxx` | `.../s/abc123?chksm=xxx&scene=1` | 已有`?`→追加`&scene=1` |
| `.../s/abc123?scene=1` | 不变 | 已包含→跳过 |

## 智能行业分类

基于标题+前1000字符关键词匹配，自动归类到Obsidian对应目录：

| 行业 | 识别关键词 | Obsidian路径 |
|------|-----------|-------------|
| AI芯片 | AI芯片、GPU、GPGPU、寒武纪、壁仞、海光、摩尔线程、半导体 | `sources/AI芯片/` |
| AI大模型 | 大模型、LLM、GPT、Claude、通义、文心、DeepSeek、AGI | `sources/AI大模型/` |
| 新能源 | 新能源、宁德时代、动力电池、锂电池、光伏、风电、储能、比亚迪 | `sources/新能源/` |
| 消费 | 消费、白酒、茅台、啤酒、食品饮料、调味品、零售 | `sources/消费/` |
| 医药 | 医药、创新药、医疗器械、CXO、生物科技、疫苗、中药 | `sources/医药/` |
| 金融 | 金融、银行、保险、证券、券商、投行、资管 | `sources/金融/` |
| 互联网 | 互联网、电商、腾讯、阿里、字节、美团、拼多多、SaaS | `sources/互联网/` |
| 军工 | 军工、国防、航天、航空、导弹、雷达 | `sources/军工/` |
| 汽车 | 汽车、整车、乘用车、车企、吉利、长城 | `sources/汽车/` |
| 能源 | 能源、电力、煤炭、石油、天然气、华能、三峡 | `sources/能源/` |
| 原材料 | 化工、钢铁、有色、水泥、万华、MDI | `sources/原材料/` |
| 地产 | 地产、房地产、保利、万科、碧桂园 | `sources/地产/` |
| 宏观经济 | 宏观、GDP、CPI、PMI、央行、货币政策、财政政策 | `sources/宏观经济/` |

## Obsidian 双层存储结构

```
~/Documents/Obsidian Vault/llm-wiki/
├── raw/                         # 原始文本归档（不丢失任何内容）
│   ├── wechat/{行业}/           # 微信文章原文
│   ├── futu/{行业}/             # 富途文章原文
│   ├── xueqiu/{行业}/           # 雪球文章原文
│   └── general/{行业}/          # 通用网页原文
└── sources/                     # 结构化Markdown（含frontmatter）
    ├── AI芯片/
    ├── 新能源/
    ├── 消费/
    └── ...（按行业分类）
```

### 结构化来源页格式

```markdown
---
source_type: wechat_article|futu_article|xueqiu_article|web_article
url: https://...
title: 文章标题
source: 微信公众号|富途牛牛|雪球|...
industry: AI芯片
author: 作者/公众号名
publish_date: YYYY-MM-DD
fetched_date: YYYY-MM-DD
content_length: 字符数
fetch_method: browser_navigate|playwright|tavily|firecrawl|web_extract
---

# 文章标题

## 基本信息

| 字段 | 内容 |
|------|------|
| 来源 | 微信公众号 |
| 行业 | AI芯片 |
| 作者 | ... |
| 发布时间 | ... |
| 原文链接 | [链接](url) |
| 抓取方法 | browser_navigate |

## 文章内容

（清理后的正文）

## 关键词

#wechat #AI芯片 #文章 #知识库
```

## 导航冗余内容自动清理

内置关键词列表，自动移除导航菜单、登录提示、广告等：

```
行情工具, 报价, 股票报价, 投资工具, 模拟交易, 选股器,
资讯及牛牛圈, 新闻, 焦点新闻, 7×24快讯, 牛牛圈,
关于我们, 帮助, English, 繁體中文, 注册/登入,
新客限时, 立即领取, 刷新, 加载中, 热门资讯,
行情, 资讯, 课堂, 港股, 美股, 沪深, 公告, 研报
```

## 执行流程（面向Apollo的标准操作）

当用户发送文章URL时，按以下步骤执行：

### Step 1: URL规范化 + 平台识别

```
1. 检查URL是否包含 mp.weixin.qq.com → 追加 ?scene=1
2. 富途URL (news.futunn.com) → 清理跟踪参数，只保留 https://news.futunn.com/post/{ID}
3. 识别平台类型（wechat/futu/xueqiu/eastmoney/general）
4. 选择对应的提取策略（见下方 Step 2 各平台指令）
```

### Step 2: 提取内容（按优先级回退）

#### 方法1: Hermes browser_navigate（首选，速度快）

**通用流程**：
```
1. browser_navigate(url) → 打开URL
2. browser_snapshot(full=true) → 获取页面完整可访问性树
3. 从snapshot中按平台规则提取标题/作者/正文
4. 如内容为空或检测到验证码 → 回退方法2
```

**⚠️ 各平台从 browser_snapshot 提取规则（关键！）**：

##### 富途牛牛 (news.futunn.com)
snapshot结构特征：
```
heading: "报道称OpenAI未达销售目标，相关股票大跌"     ← 标题：取第一个 heading 节点
link: "环球市场播报"                                   ← 作者：标题后第一个 link（来源站名）
text: "43分钟前"                                       ← 时间：作者后含数字+时间单位的 text
text: "OpenAI的合作伙伴..."                            ← 正文：从第一个长 text 开始
text: "编辑/lambor"                                    ← 正文结束标志
link: "CRWV CoreWeave 106.210 -5.850..."              ← 行情组件：跳过
```
提取规则：
- **标题**：取 `heading` 角色节点的 name 值
- **作者**：取标题后第一个 `link` 角色节点（是来源站名如"环球市场播报"）
- **时间**：取作者后含"分钟前/小时前/天前/前天"的 `text` 节点
- **正文**：从第一个长 `text` 节点（>30字符）开始，到"编辑/"行结束
- **跳过**：股票行情组件（含价格+涨跌幅的 link 节点）、热点推荐、免责声明、"赞/评论/浏览"、页脚

##### 微信公众号 (mp.weixin.qq.com)
snapshot结构特征：
```
heading: "文章标题"                                    ← 标题
text: "公众号名称"                                     ← 作者（公众号名）
text: "2026-04-28 18:30"                              ← 时间（标准日期格式）
text: "正文第一段..."                                  ← 正文
```
提取规则：
- **标题**：取 `heading` 角色节点
- **作者**：取标题后第一个非链接的 text 节点（公众号名）
- **时间**：取含 YYYY-MM-DD 格式的 text 节点
- **正文**：从时间后第一个长 text 开始到文末
- **⚠️ 验证码**：snapshot 中出现"Access Verification"/"请完成验证"→ 立即回退方法2

##### 雪球 (xueqiu.com)
- **标题**：取 `heading` 角色节点
- **作者**：取 class 含 "user" 的元素或作者名 text
- **正文**：从"正文内容"区域提取
- **⚠️ 验证码**：雪球常见 WAF 拦截→回退方法2（Tavily）

##### 通用网页
- **标题**：取第一个 `heading` 节点，或 WebArea 的 name
- **正文**：取 `main` 或 `article` 角色节点下的所有 `text` 节点，拼接
- **跳过**：`navigation`/`banner`/`footer`/`complementary` 角色节点

#### 方法2-5: 回退到 Python 脚本

```bash
python3 ~/.hermes/skills/web-article-to-obsidian/scripts/unified_fetch.py <URL>
```

脚本自动按 Playwright → Tavily → Firecrawl → HTTP 顺序回退。
脚本内已集成各平台选择器、URL清理、行情组件清理逻辑。

### Step 3: 内容清理

**从 browser_snapshot 提取的文本需额外清理**：
```
1. 移除股票行情组件（如 "CRWV CoreWeave 106.210 -5.850 -5.22% 盘前时段 04/28 06:20"）
2. 移除"编辑/lambor"之后的免责声明、赞/评论/浏览、热点推荐、页脚
3. 移除导航项（行情工具、资讯及牛牛圈、关于我们、帮助、注册/登入）
4. 清理空行和重复段落
5. 验证内容长度（<200字符标记警告）
```

**从 Python 脚本提取的内容已自动清理**，直接进入 Step 4。

### Step 4: 行业分类 + 存储

```
1. 基于标题+前1000字符匹配行业关键词
2. 保存原始文本到 raw/{平台}/{行业}/
3. 生成结构化Markdown到 sources/{行业}/
4. 验证文件存在性
```

### Step 5: 返回结果

```
✅ 文章标题: XXX
📂 行业分类: AI芯片
📄 内容长度: 3,542 字符
🔧 提取方法: browser_navigate
💾 存储路径: sources/AI芯片/微信公众号_XXX.md
```

## 故障排除

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 验证码页面 | URL缺少`?scene=1` | 规范化URL |
| 内容为空 | 页面未加载完成 | 增加等待时间 / 切换提取方法 |
| 导航菜单污染 | 选择器未命中正文 | 使用平台专用选择器 |
| Tavily失败 | API额度用完 | 切换其他方法 |
| 网络超时 | 服务器响应慢 | 缩短timeout + 重试 |
| 内容过短(<200字) | 反爬拦截 | 按优先级回退到下一方法 |

## 命令行脚本

```bash
# 完整提取流程
python3 ~/.hermes/skills/web-article-to-obsidian/scripts/unified_fetch.py <URL>

# 指定行业分类
python3 ~/.hermes/skills/web-article-to-obsidian/scripts/unified_fetch.py <URL> --industry AI芯片

# 指定提取方法
python3 ~/.hermes/skills/web-article-to-obsidian/scripts/unified_fetch.py <URL> --method playwright

# 仅提取不存储（调试用）
python3 ~/.hermes/skills/web-article-to-obsidian/scripts/unified_fetch.py <URL> --dry-run
```

## 版本历史

- **v2.0.0** (2026-04-28) - 集成版本，合并三个技能，统一五级提取引擎+回退机制
- 原始版本：
  - article-to-obsidian v1.1.0 - Playwright+行业分类
  - wechat-article-extractor v1.0.0 - Tavily+Firecrawl
  - wechat-mp-reader v1.0.0 - Hermes browser工具
