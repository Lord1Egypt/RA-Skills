# 引擎级路由 + 兜底搜索机制

## 总览：37通道引擎级路由

可用搜索通道共37个，分属5个工具：

| 工具 | 通道数 | 通道明细 |
|------|-------|---------|
| cn-web-search | 17引擎 | 公众号2(搜狗微信/必应索引) + 中文综合5(360/搜狗/必应中文/百度/头条) + 英文综合7(DDG/Qwant/Startpage/必应英文/Yahoo/Brave/Mojeek) + 技术2(SO/GitHub) + 财经3(东方财富/集思录/财新) + 百科2(Wiki中英文) |
| 妙想5件套 | 5工具 | mx-data(行情/财务/关联) + mx-search(新闻/研报/政策/公告) + mx-xuangu(选股/行业筛选) + mx-zixuan(自选) + mx-moni(模拟) |
| aihot | 6通道 | 5个category(ai-models/ai-products/industry/paper/tip) + 关键词搜索(q=) |
| last30days-cn | 8平台 | 百度/微博/知乎/小红书/B站/微信/抖音/头条 |
| news-fact-check | 1通道 | 核查方法论+多源验证框架 |

---

## 话题领域→引擎级路由矩阵

根据素材的话题领域，精准路由到最合适的引擎通道：

| 话题领域 | 第1优先通道 | 第2优先通道 | 第3优先通道 |
|---------|-----------|-----------|-----------|
| **财经/金融/投资/上市** | mx-data(硬数据) + mx-search(资讯/研报/政策) | cn-web-search: 东方财富+集思录+财新 + **港交所披露易(港股/H股)** | mx-xuangu(行业/板块对比) |
| **AI/大模型/LLM** | aihot: 对应category(ai-models/industry/paper等) | cn-web-search: Brave+DDG+必应英文(英文一手) | mx-search(如涉及上市公司) |
| **科技/互联网/产品** | cn-web-search: Brave+DDG+必应英文(英文一手) + SO+GitHub(技术) | aihot(如涉及AI) | last30days-cn: 知乎+B站(深度讨论) |
| **医疗/教育/政策** | cn-web-search: Wikipedia+Brave(权威一手) | cn-web-search: 财新(政策解读) | last30days-cn: 微信+知乎(深度) |
| **近期舆论/热点** | last30days-cn: 微博+百度+抖音(热点) | cn-web-search: 搜狗微信(公众号) | cn-web-search: 必应中文(综合) |
| **知识/概念/定义** | cn-web-search: Wikipedia中英文 | cn-web-search: Brave+DDG | cn-web-search: SO+GitHub(技术概念) |
| **学术/研究/论文** | **arXiv REST API**(同行评审论文，Tier 1) | cn-web-search: Brave+DDG+必应英文(英文一手) | cn-web-search: Wikipedia中英文(概念背景) |
| **公众号深度文章** | cn-web-search: 搜狗微信+必应索引 | last30days-cn: 微信 | — |

### 路由规则（优先级从高到低）

1. **话题领域匹配** → 按上方矩阵选择第1优先通道
2. 含具体股票/市值/CapEx/EPS等金融指标 → 妙想mx-data优先
3. **AI领域关键词**（AI/大模型/LLM/OpenAI/Anthropic/Google AI等）→ aihot优先
4. 含行业/技术/学术关键词（非AI领域）→ cn-web-search对应引擎优先
5. 含"最新"/"近期"/"舆论"等时间敏感词 → last30days-cn优先
6. 含"真假"/"辟谣"/"核实"等核查词 → news-fact-check
7. 可组合：AI领域先查aihot，再用cn-web-search英文引擎交叉验证
8. 降级：妙想不可用→cn-web-search财经引擎；aihot不可用→cn-web-search英文引擎；last30days不可用→cn-web-search中文引擎
9. **学术关键词**（论文/research/arXiv/DOI/Paper/Transformer/attention 等学术术语）→ arXiv REST API 优先（详见"学术信源专用通道"小节）

---

## cn-web-search 引擎选择规则

cn-web-search有17个引擎，**必须根据场景选择引擎，不能默认走百度/360/头条**：

| 搜索场景 | 优先引擎 | 避开引擎 | WebFetch URL模板 |
|---------|---------|---------|----------------|
| 财经深度 | 东方财富 + 集思录 + 财新 + 港交所披露易 | 百度/360/头条 | `https://search.eastmoney.com/search?keyword={Q}` / `https://www.jisilu.cn/explore/?keyword={Q}` / `https://search.caixin.com/search/?keyword={Q}` / `https://www1.hkexnews.hk/search/searchtitleweb.xhtml?lang=zh`（港股财报/公告） |
| 英文一手信源 | Brave + DDG + Startpage + 必应英文 + Yahoo + Mojeek + Qwant | 中文通用引擎 | `https://search.brave.com/search?q={Q}` / `https://lite.duckduckgo.com/lite/?q={Q}` / `https://www.startpage.com/do/search?q={Q}&cluster=web` / `https://www.bing.com/search?q={Q}` / `https://search.yahoo.com/search?p={Q}` / `https://www.mojeek.com/search?q={Q}` / `https://www.qwant.com/?q={Q}&t=web` |
| 知识/概念/定义 | Wikipedia中文 + Wikipedia英文 | 百度/360 | `https://zh.wikipedia.org/w/index.php?search={Q}&title=Special:Search` / `https://en.wikipedia.org/w/index.php?search={Q}&title=Special:Search` |
| 公众号文章 | 搜狗微信 + 必应索引 | 头条 | `https://weixin.sogou.com/weixin?type=2&query={Q}&page=1` / `https://cn.bing.com/search?q=site:mp.weixin.qq.com+{Q}` |
| 技术概念 | Stack Overflow + GitHub | 百度/360 | `https://stackoverflow.com/search?q={Q}` / `https://github.com/trending?since=weekly` |
| 中文通用（兜底） | 百度 + 360 | — | `https://www.baidu.com/s?wd={Q}` / `https://m.so.com/s?q={Q}` |
| 最新资讯（最后兜底） | 头条搜索 | — | `https://so.toutiao.com/search?keyword={Q}` |

**关键约束：头条搜索仅作为最后兜底，不得作为默认引擎。**

---

## 学术信源专用通道（arXiv REST API）

涉及学术论文/研究/模型架构等学术话题时，优先使用 arXiv REST API 获取一手论文信息（Tier 1 同行评审信源）。

**调用方式**（WebFetch）：
```
http://export.arxiv.org/api/query?search_query=all:{关键词}&max_results=5&sortBy=relevance
```

**适用场景**：
- 实录中引用了具体论文（如"Transformer 论文""attention is all you need"）
- 涉及模型架构/算法原理（如 Diffusion/Mamba/MoE）
- 学术人物访谈（论文作者/研究者）

**信源分级**：arXiv 论文 = **Tier 1**（同行评审/官方预印本），必附 URL（`arxiv.org/abs/{id}`）

**降级**：arXiv 无结果 → cn-web-search 英文引擎（Brave/DDG）→ Wikipedia（概念背景）→ Agent 已知信息[AI推断]

**与 aihot 的区别**：aihot 覆盖 AI 行业新闻/产品发布，arXiv 覆盖学术论文本身。AI 领域访谈应 aihot + arXiv 双查。

---

## 妙想5件套路由详情

| 工具 | 路由场景 | 调用方式 |
|------|---------|---------|
| **mx-data** | 金融硬数据：股价/市值/财报/CapEx/EPS/毛利率/股东/行业对比/板块数据 | `python ./mx_data.py "{自然语言查询}"` |
| **mx-search** | 财经全场景：公司动态/行业分析/政策解读/研报/估值讨论/交易规则/事件解读/公告 | `python ./mx_search.py "{自然语言查询}"` |
| **mx-xuangu** | 行业/板块筛选："XX行业有哪些公司"/"XX板块市盈率分布"等横向对比 | `python ./mx_xuangu.py "{自然语言条件}"` |
| mx-zixuan | 自选股管理（非搜索用途，不纳入路由） | — |
| mx-moni | 模拟交易（非搜索用途，不纳入路由） | — |

**注意**：mx-search不限于"研报/目标价"，它的核心能力是**金融场景信源智能筛选**，覆盖新闻/公告/研报/政策/交易规则/具体事件/影响分析等全场景。财经话题的搜索补充应优先走mx-search。

---

## aihot 路由详情

| 场景 | 端点 | 说明 |
|------|------|------|
| AI模型发布/更新 | `GET /api/public/items?mode=selected&category=ai-models` | 新模型、模型更新 |
| AI产品发布 | `GET /api/public/items?mode=selected&category=ai-products` | 产品上线、功能更新 |
| AI行业动态 | `GET /api/public/items?mode=selected&category=industry` | 融资、收购、人事变动 |
| AI论文 | `GET /api/public/items?mode=selected&category=paper` | 重要论文 |
| AI技巧与观点 | `GET /api/public/items?mode=selected&category=tip` | 观点文章 |
| 关键词搜索 | `GET /api/public/items?q={关键词}` | 公司/技术/产品名搜索 |
| 时间窗口 | `since=ISO-8601` | 限最近7天 |

- 调用方式：通过 HTTP 请求 aihot.virxact.com 公开 API，无需 API Key
- **必须带浏览器User-Agent**（否则403）：`UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"`
- 不适用：非AI领域（金融/医疗/教育等通用行业）

---

## last30days-cn 路由详情

| 平台 | 适用场景 | 内容类型 |
|------|---------|---------|
| 微信公众号 | 专业分析/深度文章 | Tier 3-4 |
| 知乎 | 行业讨论/专业问答 | Tier 4-5 |
| B站 | 深度视频内容/行业解读 | Tier 4-5 |
| 微博 | 热点/舆论/快讯 | Tier 4-5 |
| 百度 | 新闻聚合 | Tier 4-5 |
| 小红书 | 用户口碑/消费端 | Tier 5 |
| 抖音 | 短视频/热点 | Tier 5 |
| 头条 | 资讯聚合 | Tier 4-5 |

- 调用方式：`python {SKILL_DIR}/scripts/last30days.py "{主题}" --emit compact`
- 可指定平台：`--search weibo,zhihu,bilibili`
- 深度模式：`--deep --emit md`

---

## news-fact-check 路由详情

1. 识别关键声明 → 从素材中提取可验证的核心事实主张
2. 多源验证 → 权威新闻源比对 + 官方信息核查 + 专业核查网站
3. 评估来源可靠性 → 媒体声誉/消息源明确性/多方观点/时效性
4. 给出结论 → 已证实为真/已证实为假/部分属实/无法核实/误导性

---

## 通用降级：WebSearch 兜底

当上述专用工具在当前环境不可用时，**统一使用 `WebSearch` 工具替代**：

| 原始路由 | WebSearch 替代查询策略 |
|---------|----------------------|
| 妙想 mx-data/mx-search | `WebSearch` + 金融关键词（如"XX公司 2026 财报 营收"） |
| aihot | `WebSearch` + AI领域关键词（如"XX模型 发布 性能"） |
| cn-web-search | `WebSearch` 直接使用（功能等价） |
| last30days-cn | `WebSearch` + 时间限定词（如"XX 最新 2026"） |
| news-fact-check | `WebSearch` + 核查关键词（如"XX 辟谣 真假"） |

**降级优先级**：专用工具 → WebSearch → Agent已知信息[AI推断]

---

## 信源多样性门控（v1.1.0 升级，详见 source-quality-gate.md）

**Step 5 搜索完成后必须执行**，3 项硬阻断，任一不通过→换通道重搜。完整规范见 `source-quality-gate.md`。

1. **信源多样性**：单一域名≤30% + 聚合平台（头条/百家号/UC大鱼号/企鹅号等）≤20% + 独立信源≥6个
2. **信源分级覆盖**：Tier 1 官方≥1 + Tier 2 权威媒体≥2 + Tier 3 行业研究≥1 + Tier 4-5 占比≤50%
3. **始发信源追溯**：聚合平台内容必须追溯始发信源，追溯不到→降级 Tier 5 或弃用

未通过时换通道优先级：妙想mx-search → cn-web-search财经引擎 → cn-web-search英文引擎（Brave/DDG）→ arXiv（学术话题）→ Wikipedia

---

## 兜底搜索机制（零空缺保证）

**核心原则：每个干货信息点的补充信息不能空缺。**

当首选通道搜索无结果或结果不足以形成有效补充时，按话题领域矩阵逐级降级：

```
第1优先通道搜索
    ↓
有有效结果？ ──是──→ 记录结果，标记核查状态
    │
    否
    ↓
第2优先通道搜索（调整查询词：放宽条件）
    ↓
有有效结果？ ──是──→ 记录结果，标记 [PARTIAL] 或 [相关]
    │
    否
    ↓
第3优先通道搜索（换角度/换语言）
    ↓
有有效结果？ ──是──→ 记录结果，标记 [相关]
    │
    否
    ↓
cn-web-search 英文引擎（Brave/DDG等）
    ↓
有有效结果？ ──是──→ 记录结果，标记 [间接相关]
    │
    否
    ↓
cn-web-search 中文通用（百度/360，最后兜底）
    ↓
有有效结果？ ──是──→ 记录结果，标记 [间接相关]
    │
    否
    ↓
使用 Agent 已知信息填充，标记 [AI推断]（绝不留空）
```

### 查询词调整策略

| 尝试轮次 | 查询词调整 | 示例 |
|---------|----------|------|
| 第1轮（首选通道） | 精确查询 | "SpaceX Starlink ARPU 2026" |
| 第2轮（第2优先通道） | 放宽条件 | "Starlink revenue per user decline" |
| 第3轮（第3优先通道） | 查相关主题 | "SpaceX 营收 星链 用户数 趋势" |
| 第4轮（英文引擎） | 换数据源 | "SpaceX Starlink financial metrics" |
| 第5轮（中文通用兜底） | 查大类背景 | "SpaceX 星链 商业模式" |

### 核查状态标记

| 标记 | 含义 | 文章中的处理 |
|------|------|------------|
| `[VERIFIED]` | 多源确认，准确 | 直接使用 |
| `[PARTIAL]` | 部分准确或需更新 | 标注"截至XX时间"或补充说明 |
| `[UNVERIFIED]` | 无法验证 | 加注"据XX表示"或降级为观点 |
| `[INCORRECT]` | 与事实不符 | 不使用，或标注差异 |
| `[相关]` | 兜底搜索找到的相关信息 | 作为背景补充，标注"相关数据显示" |
| `[间接相关]` | 仅找到间接关联信息 | 作为行业背景，不作为佐证 |
| `[AI推断]` | 所有工具均无结果 | 标注"据行业常识"，明确为推断 |

### 兜底底线

- 绝不允许任何干货信息点的补充信息为空
- 即使无法验证具体数字，也要提供该领域的背景趋势、行业共识或相关案例

---

## 来源可信度分级体系

搜索工具只是通道，可信度取决于搜索结果的**实际来源**。所有补充信息必须标注来源分级。

### 5级采信标准

| 级别 | 来源类型 | 链接策略 | 文章标注方式 | 示例 |
|------|---------|---------|------------|------|
| **Tier 1 官方** | SEC/交易所/公司官网/政府文件/同行评审论文 | **必附URL** | `数据（[来源名](URL)）` | 营收186.74亿（[S-1/A招股书](https://sec.gov/xxx)） |
| **Tier 2 权威媒体** | 路透/彭博/财新/WSJ/Nature/Science/新华社 | **必附URL** | `数据（[媒体名](URL)）` | 估值1.75万亿（[路透社](https://reuters.com/xxx)） |
| **Tier 3 行业研究** | TrendForce/Gartner/McKinsey/IDC/行业白皮书 | **尽量附URL**，无URL标机构+报告名 | `数据（据{机构}{报告名}）` | HBM产能售罄（据TrendForce 2026年HBM供需报告） |
| **Tier 4 聚合/二手** | aihot聚合/36kr/虎嗅/TheVerge/科技博客 | **选择性附URL** | `数据（据{来源}报道）` | Terafab投资1190亿（据[华尔街日报](https://wsj.com/xxx)报道） |
| **Tier 5 社区/推断** | 知乎/微博/小红书/Agent推断 | **不附URL** | `数据（行业观点认为）` 或 `[AI推断]` | DRAM紧缺将延续（行业观点认为） |

### 分级判断流程

```
搜索结果 → 识别来源类型
    │
    ├─ URL域名含 sec.gov / gov.cn / 官方域名 → Tier 1
    ├─ URL域名含 reuters.com / bloomberg.com / caixin.com / nature.com → Tier 2
    ├─ 来源含机构名(TrendForce/Gartner/McKinsey等) → Tier 3
    ├─ 来源为科技媒体/聚合平台 → Tier 4
    └─ 来源为UGC平台/无明确来源/Agent推断 → Tier 5
```

### 各通道搜索结果的典型分级

| 通道 | 高概率产出级别 | 说明 |
|------|--------------|------|
| 妙想 mx-data/mx-search | Tier 1-2 | SEC文件、研报、官方行情 |
| aihot | Tier 3-4 | 聚合AI行业新闻，需追溯原始报道判断分级 |
| cn-web-search 财经引擎 | Tier 2-3 | 东方财富/集思录/财新 |
| cn-web-search 英文引擎 | Tier 2-3 | Brave/DDG/Bing等，一手信源多 |
| cn-web-search 百科引擎 | Tier 2-3 | Wikipedia |
| cn-web-search 中文通用 | Tier 4-5 | 百度/360/头条，聚合内容多 |
| last30days-cn | Tier 4-5 | UGC为主，极少Tier 2 |
| news-fact-check | Tier 1-2 | 专业核查机构结论 |

### 补充信息标准化格式（Step 5→Step 6 传递）

每条补充信息必须携带以下字段：

```markdown
### [维度标记]-N: {补充信息摘要}

- **核查结果**: [VERIFIED / PARTIAL / UNVERIFIED / INCORRECT / 相关 / 间接相关 / AI推断]
- **来源分级**: Tier {1-5}
- **来源标注**: {来源名称}（如：S-1/A招股书 / 路透社 / TrendForce 2026年HBM报告）
- **来源URL**: {URL}（Tier 1-3必填，Tier 4选填，Tier 5填"无"）
- **搜索通道**: {使用的具体通道}（如：mx-search / cn-web-search:Brave / aihot:industry）
- **文章写法**: {在文章中的具体写法，含链接或标注}
- **链接位置**: 正文行内 / 文末参考来源 / 无链接
```

**示例**：
```markdown
### [DATA]-3: SpaceX估值从1750亿增至1.77万亿

- **核查结果**: [VERIFIED]
- **来源分级**: Tier 2
- **来源标注**: 路透社
- **来源URL**: https://www.reuters.com/xxx
- **搜索通道**: cn-web-search:Brave
- **文章写法**: 不到三年估值从1750亿飙升至1.77万亿（[路透社](https://www.reuters.com/xxx)）
- **链接位置**: 正文行内
```
