---
name: report-search
description: 搜索和提取发现报告(fxbaogao.com)中的研究报告、行业报告、公司研究、宏观策略、财报和招股书内容。当用户需要按关键词、机构、作者或时间范围查找研究报告，或进一步查看某篇研究报告的摘要和正文时使用。
argument-hint: [关键词] [--org 机构] [--author 作者] [--time last1mon|last3mon] [--start-date YYYY-MM-DD] [--end-date YYYY-MM-DD]
---

# 研报搜索 Skill

这个 skill 面向 Claude Code 和 OpenClaw，默认使用本 skill 自带脚本。

运行脚本时，脚本路径要相对当前 `SKILL.md` 所在目录解析，不要假设当前工作目录正好在 skill 目录内。

## 何时使用

- 用户要搜索券商研报、行业报告、公司深度、宏观策略、财报、招股书
- 用户给了关键词、作者、机构、时间范围等过滤条件
- 用户已经选中某篇研报，想看摘要、正文、结论或风险提示

## 运行方式

### 1. 搜索研报

优先运行：

```bash
python3 scripts/search_reports.py "人工智能" --json
```

常见参数：

- `--author 张三`，可重复传多次
- `--org 中信证券`，可重复传多次
- `--time last7day|last1mon|last3mon|last1year`
- `--start-date 2025-01-01 --end-date 2025-03-31`
- `--size 10`

不要把相对时间自行换算后塞进 `end_time`；脚本会按 `fxbaogao_mcp` 的方式把 `last1mon` 这类值原样传给接口。

### 2. 获取研报详情

当用户指定序号或 `doc_id` 后，运行：

```bash
python3 scripts/get_report_content.py 5288801 --json
```

## 工作流

1. 解析用户条件，只提取用户明确表达的关键词、机构、作者、时间范围。
2. 先运行 `scripts/search_reports.py ... --json`。
3. 向用户展示最相关的 5 到 10 条结果，必须保留 `doc_id`、机构、日期和链接。
4. 用户要求深入某篇时，再运行 `scripts/get_report_content.py DOC_ID --json`。
5. 详情回答时优先使用 `summary_sections`，再按需引用 `content` 中的正文段落。

## JSON 输出字段

### 搜索结果

`search_reports.py --json` 返回：

- `total`
- `reports[]`
- 每个 `report` 含 `doc_id`、`title`、`org_name`、`authors`、`publish_date`
- `report_url`、`detail_url`
- `snippets`

### 详情结果

`get_report_content.py --json` 返回：

- `doc_id`、`title`、`org_name`、`authors`、`publish_date`
- `report_url`、`detail_url`
- `summary_sections`
- `summary`
- `content`
- `raw_content`

## 回复约定

- 搜索结果先给列表，再等用户选择具体报告
- 不要伪造不存在的作者、机构、日期或摘要
- 引用详情时优先总结 `summary_sections`，不要直接整段倾倒长正文
- 如果结果很多，先展示前几条，并告知用户可以继续筛选机构、作者或时间
- 用户如果想打开 PDF，统一引导到 `https://www.fxbaogao.com/view?id=DOC_ID`，不要返回 `public.fxbaogao.com` 直链
- 如果运行时出现网络或 DNS 错误，明确告诉用户当前环境需要放行外网访问 `api.fxbaogao.com` 和 `www.fxbaogao.com`
- 如果运行时出现本机 Python 证书链错误，可提示用户临时加上 `FXBAOGAO_SSL_NO_VERIFY=1` 重试，但不要默认关闭 SSL 校验

## 常用命令示例

```bash
python3 scripts/search_reports.py "人工智能" --time last1mon --json
python3 scripts/search_reports.py "半导体" --org "中信证券" --org "华泰证券" --size 20 --json
python3 scripts/search_reports.py "新能源" --start-date 2025-01-01 --end-date 2025-03-31 --json
python3 scripts/get_report_content.py 5288801 --json
```

更多示例见 [examples/sample.md](examples/sample.md)。
