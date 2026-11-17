# PubMed 检索语法速查

构造 `--query` 参数时使用。PubMed 支持完整的布尔检索与字段限定。

## 布尔运算

- `AND`、`OR`、`NOT` 必须**大写**
- 默认多个词之间按 `AND` 处理（自动术语映射可能介入）
- 括号控制优先级：`(a OR b) AND c`

## 常用字段标签

| 标签 | 含义 | 示例 |
|------|------|------|
| `[MeSH Terms]` / `[mh]` | MeSH 主题词 | `"Diabetes Mellitus, Type 2"[MeSH Terms]` |
| `[Title]` / `[ti]` | 标题 | `metformin[Title]` |
| `[Title/Abstract]` / `[tiab]` | 标题或摘要 | `semaglutide[tiab]` |
| `[Author]` / `[au]` | 作者 | `Smith J[Author]` |
| `[Journal]` / `[jour]` | 期刊 | `"N Engl J Med"[Journal]` |
| `[pdat]` | 发表日期 | `2023:2025[pdat]` |
| `[Publication Type]` / `[pt]` | 文献类型 | `randomized controlled trial[pt]` |
| `[la]` | 语言 | `english[la]` |
| `[free full text]` | 免费全文过滤 | `... AND free full text[Filter]` |

## 常用文献类型 `[pt]`

- `randomized controlled trial[pt]` — RCT
- `systematic review[pt]` — 系统综述
- `meta-analysis[pt]` — Meta 分析
- `review[pt]` — 综述
- `clinical trial[pt]` — 临床试验
- `case reports[pt]` — 病例报告

## 日期限定（两种方式）

1. 查询内：`"covid-19"[mh] AND 2022:2025[pdat]`
2. 脚本参数（更推荐）：`--mindate 2022/01/01 --maxdate 2025/12/31`

## 短语检索

- 双引号锁定短语，禁用自动术语映射：`"blood pressure"` 
- 截词：`*`（至少 4 个字符后），如 `diabet*`

## 典型查询示例

```
# 某药治疗某病的 RCT
semaglutide[tiab] AND "Obesity"[MeSH Terms] AND randomized controlled trial[pt]

# 某作者在某期刊的文章
Wang Y[Author] AND "Lancet"[Journal]

# 近 5 年系统综述
"Alzheimer Disease"[MeSH Terms] AND systematic review[pt] AND 2020:2025[pdat]

# 标题含某关键词、英文、有免费全文
metformin[Title] AND english[la] AND free full text[Filter]
```

## 排序说明

- `--sort relevance`（默认）：相关性，适合"最重要的几篇"
- `--sort pub_date`：按发表日期倒序，适合"最新的几篇"
