# 演示（demo）

最小可运行示例集，覆盖 v1.0.2（章节初稿 + 图表占位）与 v1.0.3（价格分引擎 + 内容自动填充）新能力。

## 1. 章节初稿 + 图表占位（深度节点 B）
```bash
NODE_PATH=$DOCX $NODE scripts/generate_bid_template.js --config demo/sample_config.json --out demo/out.docx
```
打开 `demo/out.docx` 可见：封面【正本】与目录；各章节按 scheme3 重新编号；「投标函」「技术方案」等章节已渲染起草正文（body）；「技术方案」「项目实施计划」下出现灰色图表占位段落（chart）。

## 2. 价格分算分（深度节点 C）
```bash
$VENV scripts/price_score.py --config demo/price_config.json
```
输出 benchmark 法报价得分表（评标基准价=均值下浮2%，满分60，偏离1%分别扣0.5/0.3分），含排名与「⚠️ 需人工复核」提示。

## 3. 内容自动填充（autofill 端到端）
```bash
$VENV scripts/parse_bidding_docx.py <招标文件.docx> --output parsed.json
$VENV scripts/autofill_prepare.py --parsed parsed.json --content demo/content_sample.json --out bid_config.json
NODE_PATH=$DOCX $NODE scripts/generate_bid_template.js --config bid_config.json --out out.docx
```
`demo/content_sample.json` 提供若干章节（`match` 锚点须与解析出的章节标题一致）的起草正文与图表占位，`autofill_prepare.py` 将其注入骨架，渲染出带章节初稿的 docx；未命中章节保留占位，终端打印「已填充/未填充」清单。

> 真实项目中：先解析招标文件得到 `config.json`，再依 `templates/response-draft.md` 与 `templates/autofill-map.md` 为每章写 body、规划 chart，最后经节点 6 润色、节点 9 一致性审查定稿。

