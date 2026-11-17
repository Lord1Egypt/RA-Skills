# 省 Token 七法 + Signal-Search 实操清单

> 本文档是 §9 / §5.11 的实现依据，也是所有模块"每多花一批 token 前问'会改变结论/动作吗'"原则的操作手册。蓝图 §9 引用本文件。
> 读者：构建者（落实各模块 token 策略）+ 验收人（对照 M28 软上限早停、全局 token 比 0.6–1.0）。

---

## 0. 总原则

每多花一批 token 前问自己：**"这会改变结论/动作吗？"** 答否即停。这是 token 预算的灵魂，比任何具体技巧都重要。

---

## 1. 七法（按落地优先级）

### 1. prompt 裁剪（固定前缀冻结、复用缓存）
- SKILL.md 调度逻辑精简；相同系统前缀在多次调用间保持一致，命中 KV 缓存。
- 不把"引擎 URL 表 / 五维公式数值 / HTML 解析细节"塞进 SKILL.md（放 config/references/scripts，渐进式披露）。

### 2. 上下文剪枝（长文外置 / 检索型 fan-out）
- 抓取到的网页原始 HTML（~90% 噪声）**绝不进上下文**；先抽正文→Markdown 砍 80–95%（§3 抽取归一化）。
- 长文外置：只把 snippet（默认 ≤800 字）与引用元信息喂给综合模型，原文留本地按需回查。

### 3. 预检索过滤（先路由再抓）
- 先 `classify_tier` + `classify_intent` 定档位/意图，再决定用哪些源、抓多少——避免"全源盲抓"。
- `constraints.domain` 命中才把垂直源加入候选池，通用档位保持精简（生产环境 3–5 源足够，>6 触发工具描述预算爆炸）。

### 4. 工具输出压缩（search.py 截断去噪）
- `extract.py` 截断 `truncate_chars`（默认 800）；`dedup.py` 合并近重复页后再进打分；`cache.py` 复用"查询→结论"短路重抓取。

### 5. prompt caching（稳定前缀命中 KV 缓存）
- 稳定前缀（系统指令、可信度表、档位规则）固定不变，跨调用复用缓存；变体只在尾部。

### 6. 输出长度控制（结构化 JSON 而非长文）
- 子查询/规划输出结构化 JSON（`plan_queries` 返回 `[{q, depends_on, rewrite}]`），便于程序解析、减少自然语言冗余。
- 综合 `findings` 先答后源、按主题聚，避免堆叠无关细节。

### 7. 模型路由（规划/综合用强模型、摘要抽取用弱模型）
- 拆解/重写/抽取用弱模型（快、省）；综合/研判/冲突定夺用强模型。实测降本 35–50% 且不损关键质量。
- 子 agent（L3 leaf）各自封顶 token 预算，避免单 leaf 失控拖垮总账。

---

## 2. Signal-Search 实操清单（checklist）

- [ ] 抓取层：`extract.prefer_json_api=true`，优先命中隐藏 JSON 接口（结构化、零挑战、最省 token）。
- [ ] 抽取层：`trafilatura` 整页抽正文→Markdown；`markdownify` 处理已选片段；JS 渲染才回退 `playwright`。
- [ ] 截断：`snippet > truncate_chars` 必截断；残留导航/广告 < 5%。
- [ ] 缓存：命中 L1（hash）/L2（语义）直接返结论，token 记 ~0。
- [ ] 预算：`budget.monitor(used, budget)` 软上限；到顶标 `exhausted`，不硬截断半成品。
- [ ] 重试：反爬重试/换源在 scrape 层闭环，不把整段失败上下文回灌 LLM。

---

## 3. 抽取归一化要点（D9，省 token 核心）

- **绝不把原始 HTML 直接进上下文**：原始 HTML ≈ 90% 噪声，转干净 Markdown 砍 80–95% token。
- **优先探测隐藏 JSON API**：结构化优于 prose，且无浏览器挑战（东财 push2 系典型）。
- 工具选型：整页 `trafilatura`（F1 0.958，无 GPU，毫秒级）；已选片段 `markdownify`；JS 渲染回退 `playwright`；文档类（PDF/DOCX/PPTX/XLSX/图片）用 `MarkItDown`。
- Markdown 仅比纯文本多 ~10% 开销却保留标题/列表，是 LLM 上下文最佳载体。

---

## 4. 测量与告警

- `eval.py` 输出 `token_used / budget` 比：健康区间 **0.6–1.0**；<0.3 判过度保守（可降预算），>1 判预算失准（需上调或拆子查询）。
- 缓存命中率目标 >30–40%；命中率骤降告警（可能语义阈值漂移或语料版本变）。
