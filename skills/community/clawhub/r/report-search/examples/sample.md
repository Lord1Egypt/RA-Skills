# 研报搜索示例

本文件展示这个 skill 在 Claude Code / OpenClaw 中应如何调用本地脚本。

## 基础搜索

用户输入：

```text
搜索最近一个月关于人工智能的研报
```

执行：

```bash
python3 scripts/search_reports.py "人工智能" --time last1mon --json
```

向用户展示时至少保留：

- 标题
- 机构
- 作者
- 日期
- `doc_id`
- `report_url`

如果用户要打开 PDF，直接引导：

```text
请打开 https://www.fxbaogao.com/view?id=DOC_ID
```

## 机构筛选

用户输入：

```text
找中信证券和华泰证券关于半导体的研报
```

执行：

```bash
python3 scripts/search_reports.py "半导体" --org "中信证券" --org "华泰证券" --size 20 --json
```

## 作者筛选

用户输入：

```text
看看王磊最近一周写的研报
```

执行：

```bash
python3 scripts/search_reports.py --author "王磊" --time last7day --json
```

## 显式时间范围

用户输入：

```text
查 2025 年一季度的新能源研报
```

执行：

```bash
python3 scripts/search_reports.py "新能源" --start-date 2025-01-01 --end-date 2025-03-31 --json
```

## 获取详情

用户输入：

```text
看第一篇的内容
```

前提：搜索结果里第一篇的 `doc_id` 为 `5288801`

执行：

```bash
python3 scripts/get_report_content.py 5288801 --json
```

优先使用返回中的这些字段组织回答：

- `summary_sections`
- `summary`
- `content`

## 推荐回答方式

搜索阶段：

```text
找到 10 条相关研报，先给你看最相关的 5 条：

1. 人工智能行业专题（15）：从全球模型巨头的发展历程，思考模型企业的壁垒与空间
   机构：国信证券
   作者：张伦可、张昊晨、刘子谭
   日期：2026-03-07
   doc_id：5288801
   链接：https://www.fxbaogao.com/view?id=5288801
```

详情阶段：

```text
这篇报告的核心观点主要有三组：
1. Anthropic 依靠编程场景和高毛利 API 建立壁垒。
2. 谷歌在多模态与生态协同上优势明显。
3. OpenAI 仍是 C 端领导者，但开始强化企业业务。

如果你需要，我可以继续按“投资建议 / 风险提示 / 正文摘录”展开。
```
