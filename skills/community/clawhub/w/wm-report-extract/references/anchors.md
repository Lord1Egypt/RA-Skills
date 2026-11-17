# 锚点与表格签名模式库

`scan`/`extract-tables` 阶段的定位知识。**实现位置（0.5.x+）**：声明式常量在 `scripts/domain/`（`signatures.py` / `industry.py` / `catalogs.py`），行业冲突仲裁在 `domain/policy.py`；`wm_report.py` 只编排流水线。改 domain 即改库；本文件解释语义与扩展法。

## 章节锚点（CHAPTER_RE）

`^#{1,3} 第([一二…十\d]+)[节章] 、? (标题)$`——兼容 A 股格式准则「第X节」与银行/部分公司「第X章」；节序非标（如长城第三节=董事长致辞）照样工作；只认正文标题行。正文无章标题 → 目录行解析回退（`source:"toc"`，印刷页码）。

## 子节锚点（SUBSECTION_ANCHORS）

`(key, 显示名, 正则)`，匹配优先正文行，目录命中标 `from_toc`。key 与 coverage-checklist 分组对应。

MD&A 相关键（`mda_overview` / `mda_business` / `mda_industry` / `mda_outlook` / `risk_factors`）：

- 跳过前瞻性免责声明（「不构成实质承诺」「展望性陈述」等）。
- 若章节树能定「管理层讨论与分析」页区间，优先取区间内命中。
- `mda_outlook` 优先「公司未来发展的讨论与分析」/「前景展望」，再才是「未来展望」标题；不要用「未来计划」以免命中重要提示。
- `risk_factors` 优先「可能面对的风险」，不要把「前瞻性陈述的风险声明」当风险清单。

Python 层只认章节标题与表结构，**不出现任何公司名或品牌名**。

## 表格类型判定（Python 高置信 + Agent 晋升）

1. **判定输入**：近标题 + `headers` + 样本行标签。**禁止用表体全文关键词定型**（议案里出现「限制性股票」不得整表变成激励表）。
2. **高置信签名**（写入 `type`）：摘要/股东/分红/分部/产销量/变动原因/费率/质押；`executives` 须表头同时有姓名+职务且有报酬或持股列。
3. **结构性三表**：资产/利润/现金流科目结构；标题或表头像子公司持股表（持股比例/注册资本/业务性质）不定 `income_stmt`。
4. **type_hint**（不写入 type）：员工/研发/关联交易/担保/股权激励/新能源/产能/海外——留给 Agent `type_promote`。
5. Agent 按 coverage-checklist 分析意图从 generic 晋升；混两类或低置信保持 generic。质量门后再给下游。

## 跨页续表合并

相邻、同列数、页距≤1，且满足：间距文本含「续」/ 表头相同 / 表头空壳 / 前表长表(≥15行)且间距≤12。**间距出现新报表标题（合并/母公司XX表、## 标题）则阻断**——合并利润表后紧跟母公司利润表不是续表。定型在合并跨度上做（银行资产负债表的资产合计与负债合计分居两片）。

## 行业特征（INDUSTRY_HINTS）

特征词计数打分：bank、insurance、broker、real_estate、automobile、energy、manufacturing、nonferrous，以及 **pharma**（药品注册/一致性评价/集采/临床试验…，不收单独「医药」泛词作正文唯一证据）、**consumer**（经销商/同店/坪效/基酒…，不收单独「零售/食品」）、**transport_infrastructure**（通行量/通行费/吞吐量/TEU/泊位…）、**fossil_energy**（原煤产量/商品煤/油气当量/证实储量…，不收泛「能源」）。**标题加权**：制药/药业→pharma；酒业/乳业/超市→consumer；高速公路/港口→transport；煤业/石油/海油→fossil；电力→energy；矿业→nonferrous 等。短文档（<50 页）降低 bank 权重，且无保险/证券标题时清除 insurance/broker；bank 需 ≥2 个独立命中才可压过标题 automobile；nonferrous/real_estate/energy/**pharma/consumer/fossil** 正文充分时压制 manufacturing；**nonferrous 正文 ≥2 时压制 energy**；**fossil 高信号 ≥2 时压制 energy**，金属词充分时 **nonferrous > fossil**；insurance/broker 正文充分或标题命中时压制 bank；**无保险标题且保险强信号（保费/偿付/NBV 等）不足时**，消费/制药/交运等 rival 可压制准则附注污染的 insurance（综合金融如平安保留）；**交运运营词/标题充分时压制地产与偶发装机 energy**；快递/EPC/航司负向词在交运证据不足时清除或降权；珠宝黄金标题压低 consumer；器械标题在制药高信号不足时压低 pharma。交运命中时额外输出 `transport_segment=highway|port|mixed`。输出 `{industry, confidence, matched[, transport_segment]}`，驱动 coverage-checklist 行业扩展组与 priority 指引。**公司名、产品名、矿山名不得进入 schema/清单**，仅运行时从原文抽取。

## NFKC 与断词归一

- 文本 NFKC：康熙部首兼容字符（⼈民币→人民币）、全角数字/标点→半角。
- `label_norm`：record 行科目去全部空白——docling 把跨行科目断成「归属于上市公司股 东的净资产」，检索必须用 norm 匹配。

## 页码体系

`<!-- page:N -->` = PDF 物理页（1-based）。`chapters.source:"toc"` 的 page 为印刷页码（与物理页常有 2-4 页偏移），定位一律以 `sections`/`tables`/records 的物理页为准。
