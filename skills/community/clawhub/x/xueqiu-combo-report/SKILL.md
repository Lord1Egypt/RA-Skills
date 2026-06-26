---
name: xueqiu-combo-report
description: "End-to-end workflow for Xueqiu self-selected combo analysis from scraped or self-selected combo holdings batches through final ranking and PDF export. Use when the user wants one complete skill covering: (1) collecting Xueqiu self-selected combo holdings in batches from a logged-in browser session, (2) merging and patching those combo results, (3) ranking all stocks by how many combos hold them, and (4) generating JSON, Markdown, HTML, and PDF summary files. 雪球自选组合端到端分析技能，适用于：在已登录雪球浏览器会话中分批抓取自选组合持仓、合并和修补批次结果、按股票被多少组合持有进行统计排序，并生成 JSON、Markdown、HTML、PDF 汇总文件。"
---

# Xueqiu Combo Report
# 雪球组合完整报告

Use this skill when the user wants one complete workflow from Xueqiu combo holdings collection through final PDF delivery.
当用户希望把“雪球组合持仓采集 → 汇总统计 → 生成 PDF”做成一条完整流程时，使用这个技能。

Keep the workflow honest: upstream Xueqiu collection depends on an already logged-in browser session and often needs interactive browser evaluation. Do not claim this skill can always scrape Xueqiu headlessly without that session.
要如实说明流程边界：上游雪球采集依赖一个**已经登录**的浏览器会话，而且通常需要交互式浏览器 evaluate。不要把这个技能描述成“完全不依赖登录态、可稳定无头抓取”的工具。

## Workflow | 工作流程

1. Collect combo holdings in browser-sized batches from a logged-in Xueqiu session.
   在已登录雪球的浏览器会话中，按小批次采集组合持仓。
2. Save each batch as JSON.
   把每一批结果保存成 JSON。
3. Merge batch JSON files into one normalized combo-holdings file.
   将多个批次 JSON 合并成统一结构的组合持仓文件。
4. Apply any verified manual patches.
   对已确认的数据做人工 patch 修补。
5. Build ranked stock summaries.
   生成股票排名汇总。
6. Export JSON, Markdown, HTML, and PDF.
   导出 JSON、Markdown、HTML、PDF。
7. Call out assumptions, failures, and data-source limits.
   明确披露假设、失败项和数据源限制。
8. Commit workspace changes.
   提交工作区变更。

## Step 1, Collect batch results in a logged-in browser session | 第一步，在已登录浏览器里分批抓取

Use the browser tool on an already logged-in Xueqiu page.
在已经登录雪球的页面里使用 browser 工具。

Prefer small batches, usually 5 to 10 combos per run, to avoid browser-tool timeout.
优先使用小批次，通常每批 5 到 10 个组合，避免 browser tool 超时。

Read `references/end-to-end.md` for the browser-side fetch template and caveats.
需要浏览器侧 fetch 模板和注意事项时，读取 `references/end-to-end.md`。

Key rule: if the environment blocks browser navigation or long-running evaluate calls, keep the fetches short and save batch results incrementally.
关键规则：如果环境会拦截浏览器导航，或者长时间 evaluate 容易超时，就把抓取拆短，并且每批及时落盘。

## Step 2, Merge batches | 第二步，合并批次

Run:

```bash
python3 skills/xueqiu-combo-report/scripts/merge_batches.py <batch1.json> <batch2.json> ... --output <merged.json>
```

Example | 示例：

```bash
python3 skills/xueqiu-combo-report/scripts/merge_batches.py \
  output/batch1.json output/batch2.json output/batch3.json \
  --output output/xueqiu_combo_holdings_merged.json
```

## Step 3, Apply patch data when needed | 第三步，需要时应用 patch

If one or more combos need a verified correction, prepare a patch JSON and pass it to the report builder.
如果一个或多个组合需要用已确认的数据纠正，就准备 patch JSON，并传给报表脚本。

Read `references/data-format.md` for the exact structure.
具体格式见 `references/data-format.md`。

## Step 4, Build the final report | 第四步，生成最终报告

Run:

```bash
python3 skills/xueqiu-combo-report/scripts/build_report.py <merged.json> --output-prefix <prefix>
```

Example | 示例：

```bash
python3 skills/xueqiu-combo-report/scripts/build_report.py \
  output/xueqiu_combo_holdings_merged.json \
  --patch-json output/xueqiu_patch.json \
  --output-prefix output/xueqiu_combo_holdings_rank_complete \
  --title "雪球38个组合股票持仓完整汇总" \
  --note "按被持仓组合数量从高到低排序，仅统计权重大于0的持仓。"
```

Outputs | 输出：
- `<prefix>.json`
- `<prefix>.md`
- `<prefix>.html`
- `<prefix>.pdf` when Chrome/Chromium is available
- 若本机有 Chrome/Chromium，则额外输出 `<prefix>.pdf`

## Ranking rules | 排名规则

Only count `weight > 0`.
只统计 `weight > 0` 的持仓。

Sort stocks by:
股票排序规则：
1. number of combos holding the stock, descending
   被持仓组合数量降序
2. summed holding percentage across combos, descending
   跨组合合计持仓比例降序
3. stock symbol, ascending
   股票代码升序

Include for each stock:
每只股票需要包含：
- stock name / 股票名称
- stock symbol / 股票代码
- combo count / 被持仓组合数量
- total holding percentage / 合计持仓比例
- every combo holding it and the corresponding percentage / 所在组合及对应持仓比例

## Quality checks | 质量检查

Before final delivery:
交付前检查：

- Verify every expected combo is present in merged data.
  确认每个目标组合都已经出现在合并结果里。
- Verify any remaining failures are explicitly disclosed.
  确认剩余失败项被明确写出。
- Watch for combos dominated by zero-weight rows.
  注意那些主要由零权重条目构成的组合。
- Distinguish clearly between verified patches and heuristic upstream selection.
  明确区分“人工确认 patch”和“启发式选取的上游记录”。
- Prefer the PDF when the user asks for a final deliverable.
  如果用户要最终交付件，优先给 PDF。

## Example scenarios | 触发示例

- “把我这批雪球组合持仓 JSON 合并，生成完整 PDF。”
- “Merge these Xueqiu batch files and give me a final ranked PDF.”
- “我已经抓完 38 个组合，帮我做最终统计并导出表格。”
- “Patch one failed combo, then rebuild the complete stock ranking report.”

## Notes | 说明

- This skill replaces a report-only workflow by bundling both upstream collection guidance and downstream report generation.
  这个技能不再只是“出 PDF”，而是把上游抓取指导和下游报告生成合并到了一个流程里。
- Keep the browser-dependent collection step lightweight and incremental.
  浏览器依赖的抓取步骤要尽量轻量、分批、可中断续跑。
- If the user later wants a more deterministic upstream collector, split that into a dedicated scraping skill rather than over-promising in this one.
  如果以后用户要更确定性的上游采集器，建议单独拆成 scraping skill，不要在这个技能里过度承诺。
