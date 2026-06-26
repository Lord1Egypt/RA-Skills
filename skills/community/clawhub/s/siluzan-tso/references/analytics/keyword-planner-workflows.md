# 关键词规划师工作流

> **拓词命令**读本文；**建户 JSON + validate + create** 读 `references/google-ads/google-ads-campaign-plan.md`。关键词数量规则：`google-ads/rules/google-ads-keyword-taxonomy.md`。
>
> **数据口径**：`siluzan-tso keyword` 默认走 `keywordidea/google`（共享 MCC，出价 **USD**）；传 **`-a <mediaCustomerId>`** 时走 `keywordrecommendation/recommend/{id}/google`，出价币种为 `list-accounts` 的 **`currencyCode`**（如 CNY）。可选 `--url` 叠加 **网址拓词**（`websitereco`）。与 **`google-analysis` 投放表现**不是同一套数据。

---

## 路径选择（拓词前先定分支）

关键词列表可能来自 **三类来源**，交付前须在说明中标注来源，勿混为一谈：

| 来源                | 典型做法                                                                                                         | 是否含 `montlySearch` / CPC 等 Google 指标             |
| ------------------- | ---------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| **A. 宿主联网搜索** | 助手用 WebSearch / 公开网页归纳行业词、竞品词、长尾变体，再写入词包                                              | ❌ 无，须再调 `keyword` 补指标或单独标注「无市场数据」 |
| **B. Google API**   | `siluzan-tso keyword -k "种子,..."`（无 `-a`：`keywordidea/google`/USD；有 `-a`：账户接口/账户币；可选 `--geo`） | ✅ 有                                                  |
| **C. 网址拓词**     | `keyword` 带 `--url`（`websitereco` 轮询）                                                                       | 通常仅词面，**无**完整 Planner 指标                    |

### 分支 A — 混合拓词

**适用**：用户要「全面拓词」「行业/竞品词一起出」，且**未**要求只要 Google 数据。

1. （可选）宿主 **联网搜索** 或 `rag query` 归纳 **2–8 个英文种子词**（RAG 见 §0，联网搜索勿与 Google 指标混写在同一列）。
2. `siluzan-tso keyword -k "种子1,种子2,..." [--url "<落地页或竞品站>"] --json-out ./snap-kw`
3. 对落盘 `items`：以 **`keyword` 返回行为准**（有 `montlySearch` / `averageCpc` 等，币种见 `bidAmountCurrency`）；联网搜索得到的词若无对应行，可并入词包但须标注 **「无 Google 市场数据」**，或丢弃。

### 分支 B — 仅 Google 市场数据（默认）

**适用**：用户明确「只要 Google 关键词规划师 / Keyword Planner 数据」「不要联网搜索」「不要网络拓词」；或只需带搜索量、CPC、竞争度的官方建议列表。

**禁止**：

- 为补词而做 **WebSearch / webfetch 联网归纳**（落地页 PDP 推断等 **投放方案** 流程除外，且不得把联网词当作 Planner 结果）。
- CLI 使用 **`--url`**（会叠加网址拓词，非纯 Google API）。

**执行**：

1. 种子词仅来自：**用户已给出的词**、账户内 `google-analysis` 抽词、或（可选）**RAG 知识库**片段——**不要**再联网搜索补种子。
2. ```bash
   siluzan-tso keyword -k "种子1,种子2,..." --google-only --json-out ./snap-kw
   ```
   （`--google-only` 即使误传 `--url` 也会忽略网址拓词。）
3. 词包说明首行标注：**数据来源：Google Keyword Planner（`keywordidea/google`）**；表格只列落盘 JSON 中有 `montlySearch` 等字段的词。
4. 若 `source` 为 `"Cgy"` 的条目仍存在，须在说明中单独标注，勿称为 Google Planner 原生建议。

---

## 九类场景索引

洗词、分组、否词表、匹配策略等多依赖对 **`--json-out` 落盘 JSON** 的解析或 Agent 归纳；逐步命令见「场景编排」。

| #   | 场景                                                                            | 编排                            |
| --- | ------------------------------------------------------------------------------- | ------------------------------- |
| —   | **仅 Google Planner 数据**（不联网搜索、不用 `--url`）                          | 上文「分支 B」                  |
| 0   | **先 RAG 再拓词**：客户产品/行业背景 → 种子词与 `--url`                         | §0                              |
| 1   | 竞品网址 + 种子拓词：至少一个 `-k` + `--url`，落盘后去重/排序/截 Top N          | §1                              |
| 2   | 多种子长尾：`-k "种子1,种子2,..."`                                              | §2                              |
| 3   | 按规则洗词：月搜索量阈值、排除词根、排除类意图等                                | §2（JSON）                      |
| 4   | 账户关键词表现 + 市场侧指标：`google-analysis` keywords → 抽词 → 分批 `keyword` | §3                              |
| 5   | 搜索词 + 拓词：浪费流量 / 否词线索                                              | §4                              |
| 6   | 高商业意图粗筛：CPC、竞争度、搜索量                                             | §5                              |
| 7   | 否词或否词根落地：`ad keyword-negative-create` 等                               | §4 + `google-ads/google-ads.md` |
| 8   | Campaign → AdGroup → JSON：`ad campaign-validate` → `ad campaign-create`        | §6                              |
| 9   | 拓词结果导出：`keyword … --json-out`，供脚本消费                                | §7                              |

---

## 指定拓词市场地区（geoTargetConstant）

Google Keyword Planner 的搜索量/CPC 与**目标国家/地区**相关。指定地区：

1. **查国家 ID**：
   ```bash
   siluzan-tso keyword geo-list --json-out ./snap-geo
   # 或按代码过滤：--country-code US,CN
   ```
2. **带地区拓词**（单次只传 **一个** ID 时，指标对应该市场）：
   ```bash
   siluzan-tso keyword -k "pipe" --geo 2840 --json-out ./snap-kw-us
   ```

常见 ID（与 `ad campaign-create --location-ids` 同源）：美国 `2840`，中国 `2826`。

### 多地区 `--geo`：返回汇总数据，无法按地区拆分

`--geo` 可传多个 ID（逗号分隔，如 `--geo 2840,2826`），网关会把它们一并传给 `keywordidea/google?geoTargetConstantIds=...`。此时 Google Keyword Planner 返回的 `montlySearch`、CPC、竞争度等是**跨所传地区的汇总/合并口径**，**不是**「每个国家各一行」或 JSON 里带 `geoTargetConstantId` 分字段。

| 需求                                | 做法                                                                                                          |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| 只要「美国+中国合在一起」的市场参考 | 一次调用：`--geo 2840,2826`                                                                                   |
| 要对比美国 vs 中国各自搜索量/CPC    | **多次调用**，每次 `--geo` **只传一个** ID，分别 `--json-out` 到不同目录（如 `./snap-kw-us`、`./snap-kw-cn`） |

**禁止**把 `--geo 2840,2826` 的单次落盘结果当成「美国一套、中国一套」两张表；报告里若写多市场对比，须注明数据来源为分次 `keyword` 调用。

```bash
# 正确：分市场各查一次
siluzan-tso keyword -k "pipe" --geo 2840 --json-out ./snap-kw-us
siluzan-tso keyword -k "pipe" --geo 2826 --json-out ./snap-kw-cn

# 易误解：单次多 geo 只有汇总指标，无法在 items[] 内按国家拆开
siluzan-tso keyword -k "pipe" --geo 2840,2826 --json-out ./snap-kw-merged
```

---

## 无接口能力（勿过度承诺）

| 能力                                                                                  | CLI 现状                                                                                          |
| ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| 种子词 / 多种子、可选竞品站 URL、本地 `--include` / `--exclude`、搜索量与 CPC、竞争度 | ✅ `keyword`                                                                                      |
| 按国家/地区限定 Keyword Planner 市场指标                                              | ✅ `keyword geo-list` + `keyword --geo`                                                           |
| 账户内关键词/搜索词表现 + 再对重点词拉市场侧指标                                      | ✅ 多命令编排（见下）                                                                             |
| 词包数值过滤、意图分类、语义 AdGroup、否词清单、匹配策略表                            | ✅ **由 AI 消费 `--json-out` 落盘结果后产出**；无单独算法命令                                     |
| Google Ads 内「过去 12 个月按月」搜索量趋势曲线                                       | ❌ **无接口**，勿用本 CLI 假装产出                                                                |
| Keyword Planner **Forecast**（官方点击/展示/成本预估）                                | ❌ **无接口**；若用户要官方 Forecast，引导至 Google Ads 界面或接受「仅粗算说明」并标注非 Forecast |

---

## 通用执行规范

- **一律**对可复用中间结果使用 `--json-out <目录>`（或等价快照参数），再读 `cli-manifest*.json` / 各 section 的 `*.outline.txt` 了解字段；详见 **`references/core/tips.md`**。
- **写账户**（新建系列/加词/加否词）：新建系列走 **`references/google-ads/google-ads-campaign-plan.md`**（含 `campaign-validate`）；其余写操作先与用户确认，写后用成对读命令复核（命令见 `google-ads/google-ads.md`）。

---

## 场景编排

### 0）先知识库、再市场侧拓词（推荐）

当用户给出**客户/品牌**或需要**产品型号、英文类目、应用场景**才能写出靠谱种子词时，**先**走 `references/analytics/rag.md`，**再**调用 `keyword`（市场侧指标与账户内表现仍须区分，见文首「数据口径」）。

1. 选定客户知识库：  
   `siluzan-tso rag list --rag-only --json-out ./snap`
2. 检索产品/行业背景（锁定 `--folder-id`，长正文优先 `--partition wiki`）：  
   `siluzan-tso rag query -q "产品型号 英文类目 应用场景 认证" --folder-id <id> --partition wiki --top-k 12 --json-out ./snap`
3. 从 RAG 片段归纳 **2–8 个种子词**（含官网/画册中的英文写法），再拓词：  
   `siluzan-tso keyword -k "种子1,种子2,..." [--url "<落地页>"] --json-out ./snap-kw`
4. 报告/词包说明中标注：**卖点与术语来自知识库片段**；搜索量/CPC/竞争度来自 `keyword`（市场参考）。

```bash
siluzan-tso rag list --rag-only --json-out ./snap
siluzan-tso rag query -q "结构胶 型号 SG 建筑幕墙" --folder-id <id> --partition wiki --top-k 12 --json-out ./snap
siluzan-tso keyword -k "structural adhesive,SG-200,curtain wall bonding" --url "https://example.com/products" --json-out ./snap-kw
```

### 1）竞品网址 + 种子拓词

1. 选定至少 **1 个种子词** `-k`（品类、品牌或竞品站上的核心产品词均可）；**不可**仅传 URL。
2. ```bash
   siluzan-tso keyword -k "<种子>" --url "<竞品或落地页 URL>" --json-out ./snap-kw
   ```
3. 合并去重、按搜索量/CPC/竞争度排序、截断 Top N、写「词包说明」（注意通过 google-analysis --sections keywords 获取的账号关键词数据禁止参与合并，因为包含同关键词多个广告系列的表现，一旦合并会导致数据错乱）

### 2）核心词长尾裂变 + 自定义过滤

1. ```bash
   siluzan-tso keyword -k "种子1,种子2,..." [--include "<须含片段>"] [--exclude "<排除片段>"] --json-out ./snap-kw
   ```
2. 月搜索量阈值、排除求职/零售等意图：**对 JSON 中 `montlySearch`（字段名与网关一致）等做程序或 AI 过滤**；`--exclude` 仅做子串级粗滤。

### 3）旧账户关键词 + 叠市场侧 CPC/热度

可选前置：若账户所属客户有知识库，先 `rag query` 核对产品表述，避免对账户内高花费词做错误英文拓词。

1. 拉账户表现：  
   `siluzan-tso google-analysis -a <mediaCustomerId> --sections keywords --start <S> --end <E> --json-out ./snap-ga`
2. 从落盘 JSON 抽取关键词文案（字段路径以该次 **`keywords-*.outline.txt`** 为准）。
3. 分批调用（避免单次 body 过大）：  
   `siluzan-tso keyword -k "词A,词B,..." --json-out ./snap-kw-batchN`
4. 报告中**分栏说明**：左列为账户内指标（花费/转化等），右列为 `keyword` 返回的搜索量/CPC/竞争度（市场参考）。

### 4）搜索词辅助（浪费流量 / 否词线索）

1. `siluzan-tso google-analysis -a <id> --sections search-terms --start <S> --end <E> --json-out ./snap-st`
2. 与 `keyword` 拓词结果对照，由 AI 列否词根或精确否词；落地执行：  
   `siluzan-tso ad keyword-negative-create …`（见 `references/google-ads/google-ads.md`）。

### 5）高商业意图粗筛（出价 + 竞争度 + 搜索量）

1. `siluzan-tso keyword -k "..." --json-out ./snap-kw`
2. 对落盘 `items` 按 `averageCpc`（CLI 出口已 ÷1,000,000，货币见 **`bidAmountCurrency`**）、`competition` / `competitionV2`、`montlySearch` 综合排序截断；此外 `lowTopOfPageBid` / `highTopOfPageBid`（页首出价 20/80 分位，与 `bidAmountCurrency` 一致）可用于评估合理出价区间。

### 6）词包 → campaign-create JSON

拓词落盘结果 + `google-ads-keyword-taxonomy.md` 分层建议 → 填 JSON（`KeywordsForBatchJob`、`campaign-validate`、`campaign-create`）见 **`references/google-ads/google-ads-campaign-plan.md`** § 标准流水线 **步 3–7**。

### 7）拓词结果标准化导出

1. ```bash
   siluzan-tso keyword -k "..." [--url ...] [--include ...] [--exclude ...] --json-out ./snap-kw
   ```
2. 消费顺序：**先**读该目录下 `cli-manifest*.json` 与 **`*.outline.txt`（字段结构）**，**再**用脚本 `require()` 或聚合逻辑读真实数据 JSON；禁止跳过 outline 猜字段。总约定见 **`references/core/tips.md`**。

---

## 单命令速查

```bash
siluzan-tso keyword -k "<必填，逗号分隔多词>" [-a <mediaCustomerId>] [--geo <id[,id...]>] [--url <url>] [--google-only] [--include <words>] [--exclude <words>] [--json-out ./snap] [--json-out <dir>] [--verbose]
siluzan-tso keyword geo-list [--country-code <codes>] [--name-contains <text>] [--json-out ./snap] [--json-out <dir>]
```

`-a`：走 `keywordrecommendation/recommend/{id}/google`；先 `list-accounts -m Google -k <id>` 确认账户与 **`currencyCode`**；出价金额字段为 `averageCpc` / `lowTopOfPageBid` / `highTopOfPageBid`（**账户币种「元」**，非汇率换算）。CLI 会再调 `keywordmanagement/v2/list`（约 10 年区间）拉账户正向词，对每条推荐写 **`alreadyInAccount`**：`1`=词干已存在，`0`=否（匹配时忽略 broad/phrase/exact 的 `""`/`[]` 包裹，大小写不敏感）。该列表为报表口径，非 Google 后台 criterion 全量；区间内从未出报表行的词可能标 `0`。

`--google-only`：只调 Google 推荐主接口（有 `-a` 为账户接口，无 `-a` 为 `keywordidea/google`），不叠加 `--url` 的网址拓词；**分支 B（仅 Google）必加**。

**返回字段**（与后端 `Samm.Core.Service.KeywordRecommendation` 对齐）：根级与每条 **`bidAmountCurrency`**（无账户=`USD`；有账户=`list-accounts` 的 `currencyCode`）；`averageCpc` / `lowTopOfPageBid` / `highTopOfPageBid`（微元 ÷1,000,000，**与 `bidAmountCurrency` 一致**）。另有 `keyword` / `montlySearch` / `monthlySearchVolumes` / `competition` / `competitionV2` / `source` 等；**有 `-a` 时**每条多 **`alreadyInAccount`**（`0` | `1`）。

与只读账户关键词列表、否词 CRUD 的对照仍归 **`references/google-ads/google-ads.md`** 中 `ad keywords` / `ad keyword-*` 各节。
