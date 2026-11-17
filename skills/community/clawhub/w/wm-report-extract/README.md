# 财报提取 Financial Report Extractor

> 财报 PDF（年报/半年报/季报，A 股 + 港股 IFRS）内容理解与按需可溯源提取。

版本 `0.6.1` · 独立运行（standalone）· 每个数值带页码 + 原文 quote 溯源

## 它做什么 / What it does

对财报 PDF（年报/半年报/季报；A 股 + 港股 IFRS）做**内容理解与按需提取**：先产出可提取性地图
（这份财报有什么、在哪、质量如何），再按需求提取特定内容或全量数据。七步流水线全部本地运行，
产物落缓存可审计；质量门（勾稽校验 / 数值存在性 / quote 回验）与独立审核（review-extract）不过，
不得把结果交给下游分析。

## 安装 / Install

复制本目录到你的 skills 根（如 `~/.agents/skills/`、`~/.openclaw/skills/`、
`~/.claude/skills/`、`~/.cursor/skills/`），然后安装转换依赖：

```bash
pip install docling pymupdf  # Python 3.10+，约 1-2GB；scan/locate/records 子命令无需安装
```

OpenClaw 用户（ClawHub 已收录后）：

```bash
openclaw skills install @open-winmale/wm-report-extract
```

## 快速开始 / Quickstart

```bash
S=<skills_root>/wm-report-extract/scripts/wm_report.py
python3 $S fetch --pdf-url https://…/annual-report.pdf   # 或本地 PDF 路径；无需任何 API key
python3 $S convert <cache_id>        # 双轨转换，300 页年报约 6-12 分钟，建议后台
python3 $S scan <cache_id> --summary # 可提取性地图（行业画像/章节树/全表 schema）
python3 $S adapt-plan <cache_id>     # 提取剧本（正文信号优先、行业组先验）
python3 $S extract-tables <cache_id> # 全表行级 records 预提取（秒级）
python3 $S materialize-tables <cache_id>  # 分表：result-{ts}/tables/*.json + gaps
python3 $S qa-tables <cache_id>      # 质量门：quality.json（给下游前必跑）
python3 $S review-extract <cache_id> # 独立审核：review.json
python3 $S resolve <cache_id> --need "合同负债" --need "存货" --write-fields  # 按需字段
```

完整契约（定型晋升、异常处置、禁止事项）见 [SKILL.md](SKILL.md)；
操作细节见 [references/workflow.md](references/workflow.md)。

## 纯函数单测 / Tests

```bash
python3 wm-report-extract/scripts/test_wm_report.py  # 不依赖 docling/pymupdf
```

## 可选：接入 WinMale 平台

`fetch --symbol <A股代码>` 可经 [WinMale 开放平台](https://open.winmale.com) 自动查询并下载
财报（需安装 wm-skillhub 生态）。未接入平台时 `--pdf-url` / 本地路径全链路可用，二者产物一致。

## 许可 / License

按分发平台条款（ClawHub 平台统一 MIT-0）。© WinMale。
