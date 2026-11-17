# 回归用例明细

## 用例 A · scheme4 全角 H4 无双重前缀（防回归，P0 修复）
- **输入**：工程类招标文件（scheme4，H4 原文「（一） 资质与业绩」全角括号）
- **预期**：解析后标题剥离为「资质与业绩」，生成后 H4 渲染为「（一） 资质与业绩」，不出现「（一）（一）」。
- **校验**：`len(re.findall(r'（[一二三四五六七八九十百零]+）', t)) == 1`

## 用例 B · 章节初稿 body 渲染
- **输入**：`demo/sample_config.json` 中 chapters 含 `body`（字符串与字符串数组两种）
- **预期**：生成 docx 在对应标题下渲染起草正文段落；未提供 body 的章节保留「（此处填写具体内容）」占位。
- **校验**：docx 段落中出现 body 文本。

## 用例 C · 图表占位 chart 渲染
- **输入**：chapters 含 `chart`（对象 `{title,hint}` 与字符串两种）
- **预期**：渲染为灰色底纹居中提示段落 `【图表占位 · <title>】（<hint>）`。
- **校验**：段落文本含「图表占位」。

## 用例 D · 页边距透传（非默认）
- **输入**：招标文件页边距 1.5cm（EMU 539750）
- **预期**：生成 docx 正文节 margin_top ≈ 850 twip，非写死的 1440（2.54cm）。
- **校验**：`round(sec.top_margin.emu/635) == 850`

## 用例 E · 价格分异常检测（评分建模）
- **输入**：综合评分法，我方报价显著偏离均值
- **预期**：评分建模表「价格分异常检测」输出独立重算结果 + 偏离研判 + 临界提示（⚠️ 需用户确认）。
- **依据**：`references/scoring-model.md` 第六节。

## 用例 F · 双信封第一信封无价格信息
- **输入**：双信封制招标文件
- **预期**：技术标第一信封内容规划不含任何报价/折扣/价格；规划说明标注该红线。
- **依据**：`references/frontier-adaptation.md` 第三节。

## 用例 G · ESG 加分项识别与佐证
- **输入**：评分办法含绿色认证/碳足迹评分项
- **预期**：识别加分项并规划佐证（认证/报告/承诺函），明确「无认证不得声明加分」。
- **依据**：`references/frontier-adaptation.md` 第四节。

## 用例 H · 一致性实质背离拦截
- **输入**：投标承诺工期 500 天 vs 招标 540 天
- **预期**：一致性审查报告标红（🔴），定位招标条款 + 投标位置 + 修复建议（须与招标实质一致或依法声明偏离）。
- **依据**：`references/consistency-check.md` TC 系列。

## 用例 I · 价格分自动算分（深度节点 C）
- **输入**：`demo/price_config.json`（benchmark 法，报价 980/1000/1020/950，满分 60，基准价=均值下浮 2%）
- **预期**：输出报价得分表，含评标基准价、各报价偏差率与得分、排名；末尾标注「⚠️ 需人工复核」。
- **校验**：得分随报价贴近基准价递增；最低报价若高于基准价则得分 < 满分；结果可机读（--format json）。
- **依据**：`scripts/price_score.py` + `references/scoring-model.md` 第六节。

## 用例 J · 内容自动填充（autofill 端到端）
- **输入**：① `parse_bidding_docx.py` 解析真实招标文件 → `parsed_config.json`；② `content.json` 含若干 `match` 章节正文与图表占位。
- **预期**：`autofill_prepare.py` 把 content 按章节标题注入 `bid_config.json`（含 body/chart）；未命中章节保留占位；终端打印「已填充/未填充」清单。
- **校验**：`generate_bid_template.js` 渲染的 docx 在对应标题下出现 content 正文与「图表占位」块；未命中章节仍为占位。
- **依据**：`scripts/autofill_prepare.py` + `references/response-autofill.md` + `templates/autofill-map.md`。

## 用例 K · 价格分规则半自动抽取（深度节点 C 上游，v1.0.4）
- **输入**：`demo/bid_eval_benchmark.txt`（基准价法描述：价格分 60 分、有效报价算术平均下浮 2%、每高于基准价 1% 扣 0.5 分、每低于 1% 扣 0.3 分）
- **预期**：`extract_price_rules.py` 抽取出 `method=benchmark, full_score=60, base={mode:average_k, k:0.98}, deduction={above:0.5, below:0.3}`；与 `demo/price_config.json` 规则段完全一致；同时产出 `price_config.review.md`（含 `quotes` 留空等需人工确认项）。
- **校验**：抽取配置（去 `quotes`）与 `demo/price_config.json`（去 `quotes`）JSON 相等；审阅报告存在「需人工确认项」清单。
- **扩展复验**：`demo/bid_eval_low_price.txt` → `low_price_first / full_score=30`；`demo/bid_eval_interval.txt` → `interval / full_score=40 / low=500 / high=600 / unit=万元`。
- **PDF 路径**：将 benchmark 文本生成 PDF 后抽取，结果须与 TXT 路径逐项一致。
- **依据**：`scripts/extract_price_rules.py` + `references/price-rule-extraction.md`。
