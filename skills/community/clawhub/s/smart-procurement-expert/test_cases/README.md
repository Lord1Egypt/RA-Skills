# 回归测试用例（test_cases）

本目录固化「智慧招采专家」关键能力的最小回归集。每次改动 `scripts/` 或 `references/` 后，至少跑通以下用例，防止分叉与回归。

## 运行方式

```bash
# 环境（托管运行时）
VENV=".../e2e-run/venv/Scripts/python.exe"
NODE=".../node/versions/22.22.2/node.exe"
DOCX=".../node/workspace/node_modules"

# 用例 A：解析→生成（骨架模式）
$VENV scripts/parse_bidding_docx.py <招标文件.docx> --output parsed.json
$NODE --eval ... # 注入项目信息
NODE_PATH=$DOCX $NODE scripts/generate_bid_template.js --config bid_config.json --out out.docx

# 用例 B：章节初稿模式（直接用 demo/sample_config.json）
NODE_PATH=$DOCX $NODE scripts/generate_bid_template.js --config demo/sample_config.json --out demo/out.docx

# 校验（python-docx）
$VENV -c "from docx import Document; d=Document('out.docx'); print([p.text for p in d.paragraphs if p.style and p.style.name.startswith('Heading')])"
```

## 用例清单（见 cases.md）

- A · scheme4 全角 H4 无双重前缀（防回归）
- B · 章节初稿 body 渲染（字符串 / 数组）
- C · 图表占位 chart 渲染（对象 / 字符串）
- D · 页边距透传（非默认 1.5cm）
- E · 价格分异常检测（评分建模）
- F · 双信封第一信封无价格信息
- G · ESG 加分项识别与佐证
- H · 一致性实质背离拦截
- I · 价格分自动算分（深度节点 C，benchmark/低价优先/区间三类）
- J · 内容自动填充（autofill 端到端：解析→content→章节初稿）
- K · 价格分规则半自动抽取（深度节点 C 上游：评标办法→price_config.json 草稿）

### 新增用例运行命令（v1.0.3）
```bash
# 用例 I：价格分算分（可用 --config 或 CLI 快速模式）
$VENV scripts/price_score.py --config demo/price_config.json
$VENV scripts/price_score.py --method low_price_first --quotes 980,1000,1020,950 --names A,B,C,D --full-score 30

# 用例 J：autofill 端到端
$VENV scripts/parse_bidding_docx.py <招标文件.docx> --output parsed.json
$VENV scripts/autofill_prepare.py --parsed parsed.json --content demo/content_sample.json --out bid_config.json
NODE_PATH=$DOCX $NODE scripts/generate_bid_template.js --config bid_config.json --out out.docx

# 用例 K：价格分规则抽取（v1.0.4，txt 零依赖 / PDF 需 pypdf）
$VENV scripts/extract_price_rules.py demo/bid_eval_benchmark.txt --out demo/extracted/benchmark
$VENV scripts/extract_price_rules.py demo/bid_eval_low_price.txt --out demo/extracted/low_price
$VENV scripts/extract_price_rules.py demo/bid_eval_interval.txt --out demo/extracted/interval
# 校验：抽取配置(去quotes) == demo/price_config.json(去quotes)
$VENV -c "import json;a=json.load(open('demo/extracted/benchmark/price_config.json'));b=json.load(open('demo/price_config.json'));a.pop('quotes',None);b.pop('quotes',None);print('OK' if a==b else 'MISMATCH')"
```

> 印记约束：包内任何文件不得出现第三方原作者的姓名、邮箱与源技能包名等印记；打包后须做字节级扫描确认无残留。

> 印记约束：包内任何文件不得出现第三方原作者的姓名、邮箱与源技能包名等印记；打包后须做字节级扫描确认无残留。
