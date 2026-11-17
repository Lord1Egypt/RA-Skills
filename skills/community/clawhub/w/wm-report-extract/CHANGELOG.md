# Changelog — wm-report-extract

## 0.6.1

- 跨行业结构修复 + Agent 闭环（auto-heal 落地）：close 编排命令（auto-promote→narrative-scan→agent-apply→qa→review）；叙述层证据扫描与 agent_tasks 协议（quote 逐字+页码机器校验、勾稽仲裁、行业确认）；跨页续链条件增补与勾稽自和解；canonical 选主合并优先+多年摘要惩罚，typed 表 variant 标注；分析类标题否决与保险口径三表签名；新增 6 行业（钢铁/化工/通信运营/互联网与消费电子/农业/半导体）；短文档行业按发行人继承；规则演进流程 adaptation.md。
- Cross-industry structural fixes + agent-in-the-loop closure (auto-heal): close orchestrator (auto-promote, narrative-scan, agent-apply, qa, review); narrative evidence scan with agent_tasks protocol (verbatim quote + page machine validation, QA adjudication, industry confirm); extra continued-table chaining conditions and crossfoot self-reconciliation; canonical selection prefers consolidated statements and penalizes multi-year summaries, typed tables carry variant labels; analysis-title veto and insurance-statement signatures; 6 new industries; issuer-based industry inheritance for short filings; adaptation.md rule-evolution process.

## 0.6.0

- 港股披露适配（招股书 filing_kind=prospectus、繁体中期报告、三大报表简繁签名）+ 智驾行业（auto_electronics）+ adapt-plan / review-extract 提取-审核双环。
- HK disclosure support (prospectus kind, traditional-Chinese interims, bilingual statement signatures) + auto-electronics industry + adapt-plan/review-extract loops.

## 0.5.0

- 有色金属行业接入；领域常量拆分至 scripts/domain/；eval 金标准 + Agent schema 检查进 CI。
- Nonferrous-metals industry; domain constants split into scripts/domain/; golden eval + agent schema checks wired into CI.

## 0.4.0

- convert 双轨混合（PyMuPDF 有框线表格接管，数值幻觉率 0.2-0.4% vs Docling FAST 7.8%）+ qa-tables v2 质量门（勾稽/数值存在性/quote 回验）。
- Dual-track conversion (PyMuPDF takes over ruled tables; numeric hallucination 0.2-0.4% vs 7.8%) + qa-tables v2 quality gates.

## 0.2.0

- meta v2（行业探测/全表 schema/优先指引）+ extract-tables 全表 records 确定性预提取（行级溯源）。
- meta v2 (industry hint, full-table schema, priority guide) + deterministic per-row records pre-extraction with provenance.

## 0.1.0

- 首版四步流水线（Docling 页标记/NFKC/FAST 表格/CPU 默认 + fetch/scan/locate/cache）。
- Initial four-step pipeline (Docling page markers, NFKC, FAST tables, CPU default; fetch/scan/locate/cache).
