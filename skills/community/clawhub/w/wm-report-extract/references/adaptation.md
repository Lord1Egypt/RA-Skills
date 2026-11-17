# 规则演进流程（adaptation）

把「适配新公司/新行业/新签名」从一次性手工动作变成可复制的 Agent 过程。review 的
`evolution_proposal` 只产提案（validate + 样本 + 批准后才写回），本文件是落地纪律。

## 触发信号

- review warning `annual_industry_weak`：年报行业置信 weak/none → 行业目录可能未适配
- review warning `unpromoted_type_hints` / `missing_type_signatures`：表签名缺口
- `statement_signature_gap` hard fail：三表定型失败（新版式）
- narrative-scan 某行业 needle 长期不命中（多公司）：needles 形态偏差

## 提案模板（改动 PR 描述必含）

```yaml
kind: industry | table_signature | narrative_needles | cross_industry_allowlist
industry: <industry key>            # kind=industry 时
files:                              # 触及的声明式文件
  - scripts/domain/industry.py      # INDUSTRY_HINTS / TITLE_INDUSTRY_HINTS
  - scripts/domain/catalogs.py      # INDUSTRY_EXT_GROUPS / TABLE_CATALOG
  - scripts/domain/narratives.py    # NARRATIVE / GAP needles
  - scripts/domain/signatures.py    # TYPE_HINT_SIGNATURES / STRUCTURAL_RULES
  - scripts/domain/policy.py        # 行业仲裁 / CROSS_INDUSTRY_TABLE_ALLOWLIST
keywords: [词1, 词2, ...]            # 新增词 + 设计说明（与哪些行业错开）
samples:                            # 实证来源（>=1 个真实缓存）
  - cache_id: <sha12>
    company: <名称>
    expected: 行业=X 置信>=0.5 / type_hint=Y
expected_meta_change: detect_industry(s) 或 find_tables 的预期 diff
tests: 新增/修改的单测与 eval 用例 id
approval: <谁> <日期>               # 批准记录
```

## 纪律

1. **不写死公司词**：品牌/公司名禁止进关键词表（现有测试约束）；样本只作实证来源。
2. **错开原则**：新词须与相邻行业词表刻意错开（如 化工 vs manufacturing 的 产量泛词），
   冲突靠 `apply_industry_arbitration` 显式规则，不靠词频硬顶。
3. **样本验证**：`detect_industry`/`find_tables` 在 >=1 个真实缓存上跑出预期结果才可合并；
   同 batch 内既有行业不得翻转（跑 `eval/run_eval.py` required cases）。
4. **单测**：每个新词表/签名配 fixture 用例（test_wm_report.py / cases.json）。
5. **批准**：规则库改动（signatures/policy/catalogs/industry）需人工批准记录；
   needles 微调（narratives.py）豁免，但须附样本命中证据。
6. **版本**：触及 convert 无关的规则仍建议递增 `PIPELINE_VERSION` 尾号——
   stale-cache 警告会提示旧 QA 结论过期。

## 已落地范例（0.6.1）

- `fossil_energy` 词表增补（神华 7068df123192：0.33→0.60，eval 不翻转）
- 6 新行业：steel / chemicals / telecom / internet_consumer_electronics /
  agriculture / semiconductor（cases.json 新增 6 用例，小米样本实证互联网行业）
- 保险口径三表签名（平安 860c455bbad9：`保险业务收入` 进 STRUCTURAL_RULES）
- 跨业态邻接白名单（神华 fossil+电力 4 表晋升）
- 三表科目词校验扫整行文本列（盾安 2025 b8dd4f1f0f15：BS 节标签前置列版式恢复定型）

## 待批准提案

```yaml
kind: table_signature
proposal_id: sparse-col-income-statement
issue: 盾安环境 2025 年报利润表被 docling 拆为三种列布局碎片（p78 九列稀疏头段
  i100/34 行、p79 两列中段 i102、p80 九列尾段 i103/104），跨页续链因列形态不一致
  断裂，income_stmt 无法定型。
proposal: 续链判定允许「剔除全空列后列形态一致」的跨页片合并（限定在续链判定，
  不改已抽行数据，避免神华 164 案例否决的全局列归一风险）；IS 签名对表头
  重复同名列（项目×N 稀疏布局）按首非空列判。
files:
  - scripts/wm_report.py   # merge_continued_tables 列一致性 / 定型签名
samples:
  - cache_id: b8dd4f1f0f15
    company: 盾安环境 2025 年度报告
    expected: income_stmt 定型（三片并链），review 不再 statement_signature_gap
expected_meta_change: find_tables 三片链合为单一 income_stmt 候选
tests: 待补（并链 fixture + 签名 fixture）
approval: 待人工批准
```

```yaml
kind: table_signature
proposal_id: hk-borderless-income-statement
issue: 吉利汽车 2025 年报（港股繁体）合并损益表被 docling 碎片化——科目与数值
  分离成多个物理行（「收入 6 銷售成本」粘连、L3650-3663 同一巨型单元格重复 14 次），
  p124 fitz 仅有 bbox 骨架无文本。income_stmt 无法定型（叙述层与 BS/CF 均已闭环，
  review 仅剩 statement_signature_gap[income_stmt]）。
proposal: 港股无边框报表的 convert 通道改造（docling 表格模式参数或 fitz 文本+
  bbox 重建），不在规则层硬修。
files:
  - scripts/wm_report.py   # convert 通道选择（仅提案，未动）
samples:
  - cache_id: e7dbbb39bea7
    company: 吉利汽车 2025 年度报告
    expected: income_stmt 定型（损益表 p123-124 可读行结构）
expected_meta_change: report.md 損益表段落行结构重建
tests: 待补
approval: 待人工批准
```

```yaml
kind: convert_channel
proposal_id: garbled-embedded-font-ocr
issue: 小米集团 2025 年报（ffd733761633，港股 415 页）PDF 字体嵌入损坏——
  docling 输出为伪字形乱码（cmap 缺失，如「⸶灱㇓ΐ」形态），章节锚点全未命中、
  行业置信 0.1、三表无法定型、MD&A 不可读（4 叙述已按 not_found 终态留档）。
proposal: 对 kangxi/garbled 异常码命中的缓存走 OCR 通道重转（或重取源文件），
  转换健康检查已有 anomaly 检测，缺的是降级通道。
files:
  - scripts/wm_report.py   # convert 通道（仅提案，未动）
samples:
  - cache_id: ffd733761633
    company: 小米集团 2025 年度报告
    expected: report.md 可读，行业 internet_consumer_electronics，三表定型
tests: 待补
approval: 待人工批准
```
