# 5工具路由 + 兜底搜索机制

## 工具路由器

根据素材的核查类型，自动选择最佳搜索工具：

| 核查类型 | 路由目标 | 数据源 |
|---------|---------|--------|
| 金融硬数据（股价/市值/财报/CapEx/目标价） | 妙想 mx-data / mx-search | 东方财富实时行情、研报、财务数据 |
| AI行业动态/模型发布/产品发布/论文 | aihot | aihot.virxact.com 公开API，实时AI资讯，无需API Key |
| 行业背景/趋势/技术概念/竞品数据 | cn-web-search | 28引擎聚合（财经/美股/学术/技术） |
| 近期动态/舆论/热点/行业讨论 | last30days-cn | 8大平台近30天（百度/微博/知乎/小红书/B站/微信/抖音/头条） |
| 事实核查流程/谣言辨别 | news-fact-check | 核查方法论+多源验证框架 |

### 路由规则

1. 含具体股票/市值/CapEx/EPS等金融指标 → 妙想优先
2. **AI领域关键词（AI/大模型/LLM/OpenAI/Anthropic/Google AI等）→ aihot优先**，比通用搜索更精准更实时
3. 含行业/技术/学术关键词（非AI领域）→ cn-web-search 优先
4. 含"最新"/"近期"/"舆论"等时间敏感词 → last30days 优先
5. 含"真假"/"辟谣"/"核实"等核查词 → news-fact-check
6. 可组合：AI领域先查aihot，再用cn-web-search交叉验证
7. 降级：妙想不可用→cn-web-search财经引擎；aihot不可用→cn-web-search技术引擎；last30days不可用→cn-web-search中文引擎

### 通用降级：WebSearch 兜底

当上述专用工具（妙想/aihot/last30days-cn/news-fact-check）在当前环境不可用时，**统一使用 `WebSearch` 工具替代**：

| 原始路由 | WebSearch 替代查询策略 |
|---------|----------------------|
| 妙想 mx-data/mx-search | `WebSearch` + 金融关键词（如"XX公司 2026 财报 营收"） |
| aihot | `WebSearch` + AI领域关键词（如"XX模型 发布 性能"） |
| cn-web-search | `WebSearch` 直接使用（功能等价） |
| last30days-cn | `WebSearch` + 时间限定词（如"XX 最新 2026"） |
| news-fact-check | `WebSearch` + 核查关键词（如"XX 辟谣 真假"） |

**降级优先级**：专用工具 → WebSearch → Agent已知信息[AI推断]

### 各工具查询策略

**妙想 mx-data / mx-search**：
- 股价/市值 → mx-data 查实时行情和历史数据
- 财报指标 → mx-data 查财务数据（收入/CapEx/EPS/毛利率等）
- 研报/目标价 → mx-search 搜索分析师研报
- 行业对比 → mx-data 查同业数据

**aihot（AI行业动态）**：
- 调用方式：curl aihot.virxact.com 公开API，无需API Key
- 必须带浏览器User-Agent（否则403）
- AI模型发布/更新 → `GET /api/public/items?mode=selected&category=ai-models`
- AI产品发布 → `GET /api/public/items?mode=selected&category=ai-products`
- AI行业动态 → `GET /api/public/items?mode=selected&category=industry`
- AI论文 → `GET /api/public/items?mode=selected&category=paper`
- 关键词搜索 → `GET /api/public/items?q=关键词`（如q=OpenAI、q=RAG）
- 时间窗口 → `since=ISO-8601`（最近7天内）
- 日报 → `GET /api/public/daily`（用户明确说"日报"时才用）
- 适用场景：访谈涉及AI/大模型/LLM/OpenAI/Anthropic等关键词时优先使用
- 不适用：非AI领域（金融/医疗/教育等通用行业）

**cn-web-search**：
- 行业背景数据 → 财经引擎（东方财富/集思录/财新）+ 美股引擎（Seeking Alpha/Finviz）
- 技术概念注释 → 知识引擎（Wikipedia中英文）+ 技术引擎（Stack Overflow/GitHub）
- 竞品/市场数据 → 中文综合引擎 + 美股深度引擎
- 公众号文章查重 → 搜狗微信引擎

**last30days-cn**：
- 近期热点 → 百度/微博/头条（新闻类）
- 行业讨论 → 知乎/B站（深度内容类）
- 用户口碑 → 小红书/抖音（消费端）
- 专业分析 → 微信公众号（深度文章）

**news-fact-check**：
1. 识别关键声明 → 从素材中提取可验证的核心事实主张
2. 多源验证 → 权威新闻源比对 + 官方信息核查 + 专业核查网站
3. 评估来源可靠性 → 媒体声誉/消息源明确性/多方观点/时效性
4. 给出结论 → 已证实为真/已证实为假/部分属实/无法核实/误导性

---

## 兜底搜索机制（零空缺保证）

**核心原则：每个干货信息点的补充信息不能空缺。**

当首选工具搜索无结果或结果不足以形成有效补充时，必须按以下顺序逐个尝试其他工具：

```
首选工具搜索
    ↓
有有效结果？ ──是──→ 记录结果，标记核查状态
    │
    否
    ↓
工具2搜索（调整查询词：放宽条件）
    ↓
有有效结果？ ──是──→ 记录结果，标记 [PARTIAL] 或 [相关]
    │
    否
    ↓
工具3搜索（换角度/换语言）
    ↓
有有效结果？ ──是──→ 记录结果，标记 [相关]
    │
    否
    ↓
工具4搜索（换领域引擎）
    ↓
有有效结果？ ──是──→ 记录结果，标记 [间接相关]
    │
    否
    ↓
工具5搜索（最宽泛查询）
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
| 第1轮（首选工具） | 精确查询 | "美光 FY2027 CapEx 440亿美元 大摩" |
| 第2轮（换工具） | 放宽条件 | "Micron capital expenditure 2027 forecast" |
| 第3轮（换角度） | 查相关主题 | "存储行业 资本开支 2026 2027 趋势" |
| 第4轮（换领域引擎） | 换数据源 | "MU capital expenditure analyst estimate" |
| 第5轮（最宽泛） | 查大类背景 | "美光 投资 扩产 计划" |

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
- 例如：无法验证"美光FY27 CapEx 440亿"，但可以补充"存储行业整体CapEx趋势"和"美光历史CapEx数据"作为参照系

---

## 来源可信度分级体系

搜索工具只是通道，可信度取决于搜索结果的**实际来源**。所有补充信息必须标注来源分级，决定链接策略和文章写法。

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

### 各工具搜索结果的典型分级

| 工具 | 高概率产出级别 | 说明 |
|------|--------------|------|
| 妙想 mx-data/mx-search | Tier 1-2 | SEC文件、研报、官方行情 |
| aihot | Tier 3-4 | 聚合AI行业新闻，需追溯原始报道判断分级 |
| cn-web-search | Tier 2-5 | 跨度大，需按URL域名判断 |
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
- **文章写法**: {在文章中的具体写法，含链接或标注}
- **链接位置**: 正文行内 / 文末参考来源 / 无链接
```

**示例**：
```markdown
### [DATA]-3: HBM 2026产能售罄

- **核查结果**: [VERIFIED]
- **来源分级**: Tier 3
- **来源标注**: TrendForce 2026年HBM供需报告
- **来源URL**: https://www.trendforce.com/xxx
- **文章写法**: 2026年HBM产能已售罄（据TrendForce 2026年HBM供需报告）
- **链接位置**: 文末参考来源
```
