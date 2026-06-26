---
name: yanbaoke-research-report-download
description: 从全球行业报告，券商研报，机构深度报告与图表数据聚合AI平台，覆盖5000多家机构，五百万+报告-覆盖全行业深度研究的研报客平台-pc.yanbaoke.cn，研报客app。搜索各行各业的研究报告，获取报告标题、获取报告内容，并可下载报告源文件。
metadata: {"openclaw":{"emoji":"📊","requires":{"bins":["node"],"env":["YANBAOKE_API_KEY"]}}}
---

# yanbaoke-research-report-download / 研报客-研究报告搜索与下载

搜索研报客百万研报中的研究报告，获取报告标题、报告内容、详情页链接、发布时间等信息，并可下载报告源文件 PDF/DOC/PPT。回复时务必根据报告内容提供投资分析建议。


## Search / 搜索

**无需 API Key** / No API Key required - 搜索功能免费使用，无需配置。

```bash
node {baseDir}/scripts/search.mjs "keyword"
node {baseDir}/scripts/search.mjs "人工智能" -n 100
node {baseDir}/scripts/search.mjs "新能源汽车" -n 100 --type content
node {baseDir}/scripts/search.mjs "半导体" --org "中信证券,华泰证券"
node {baseDir}/scripts/search.mjs "光伏" --report-type "行业研究" --start-date "2024-01-01" --end-date "2024-12-31"
node {baseDir}/scripts/search.mjs "深度分析" --min-pages 30 --max-pages 100
node {baseDir}/scripts/search.mjs "比亚迪" --stock "比亚迪"
```

## Download / 下载

**需要 API Key** / API Key required - 请前往 [https://pc.yanbaoke.cn/openclaw](https://pc.yanbaoke.cn/openclaw) 获取 API Key。

```bash
# 使用环境变量中的 API Key
export YANBAOKE_API_KEY="sk-your-api-key"
node {baseDir}/scripts/download.mjs <uuid>

# 直接传入 API Key
node {baseDir}/scripts/download.mjs <uuid> "sk-your-api-key"

# 指定下载格式
node {baseDir}/scripts/download.mjs <uuid> "sk-your-api-key" --format=doc
node {baseDir}/scripts/download.mjs <uuid> "sk-your-api-key" -f ppt

# 示例
node {baseDir}/scripts/download.mjs "abc123-def456-ghi789"
```

### Download Pricing / 下载费用

| User Type | First Download | Re-download |
|-----------|----------------|-------------|
| 用户 User | 10 个豆 10 beans | 免费 Free |

**说明**: 每份报告仅收费一次，再次下载免费。

## Options / 选项

### Search Options / 搜索选项

| Option | Description / 说明 |
|--------|-------------------|
| `-n <count>` | Number of results (default: 100, max: 500) / 返回结果数量（默认100，最多500） |
| `--type <type>` | Search type: `title` (default) or `content` / 搜索类型：title（标题，默认）或 content（全文） |
| `--org <org>` | Publisher/Institution filter (comma-separated for multiple) / 发布机构筛选（多个用逗号分隔） |
| `--report-type <type>` | Report type filter (comma-separated for multiple) / 报告类型筛选（多个用逗号分隔） |
| `--stock <stock>` | Stock name filter (comma-separated for multiple) / 股票名称筛选（多个用逗号分隔） |
| `--start-date <date>` | Start date in YYYY-MM-DD format / 开始日期，格式 YYYY-MM-DD |
| `--end-date <date>` | End date in YYYY-MM-DD format / 结束日期，格式 YYYY-MM-DD |
| `--min-pages <num>` | Minimum page count / 最小页数 |
| `--max-pages <num>` | Maximum page count / 最大页数 |

### Download Options / 下载选项

| Argument / Option | Description / 说明 |
|-------------------|-------------------|
| `uuid` | Report UUID (from search results) / 报告 UUID（从搜索结果获取） |
| `api_key` | API key for authentication (optional, uses env var) / API 密钥（可选，默认使用环境变量） |
| `-f, --format <format>` | Document format: `pdf` (default), `doc`, or `ppt` / 文档格式：pdf（默认）、doc 或 ppt |

## Example Output / 输出示例

### Search Output / 搜索输出

```bash
$ node {baseDir}/scripts/search.mjs "人工智能" -n 3

## 人工智能
Total: 156 reports

---
## 投资建议

## Reports

- **中国AI大模型技术发展研究报告2024**
  Publisher: 中信证券
  Type: 行业研究
  Pages: 45
  Date: 2024-03-01
  Content: 本报告深入分析了AI大模型技术发展现状，涵盖技术架构、应用场景、市场规模及未来趋势...

- **人工智能产业链深度分析**
  Publisher: 华泰证券
  Type: 公司研究
  Pages: 32
  Date: 2024-02-28
  Content: 全面解析人工智能产业链上下游企业布局，重点分析核心技术突破与商业化落地进展...

- **AI芯片行业专题报告**
  Publisher: 国泰君安
  Type: 行业研究
  Pages: 58
  Date: 2024-02-25
  Content: 深度研究AI芯片市场格局，分析GPU、ASIC、FPGA等技术路线及主要厂商竞争态势...
```

### Download Output / 下载输出

```bash
$ node {baseDir}/scripts/download.mjs "123abc456-def789-ghi012"

## Report Download Link

**Title**: 中国AI大模型技术发展研究报告2024
**Format**: PDF
**Filename**: 中国AI大模型技术发展研究报告2024.pdf
**Expires in**: 60 seconds

**Download URL** (click to download):
https://files.quzili.cn/...

---

*Note: This download link expires in 60 seconds.*
```

## Response Fields / 返回字段

### Search Response Fields / 搜索返回字段

| Field | Description / 说明 |
|-------|-------------------|
| `uuid` | Report unique identifier (required for download) / 报告唯一标识符（下载时需要） |
| `title` | Report title / 报告标题 |
| `url` | Report detail page link / 报告详情页链接 |
| `time` | Publication date (YYYY-MM-DD) / 发布日期 |
| `pagenum` | Number of pages / 报告页数 |
| `org_name` | Publisher institution name / 发布机构名称 |
| `rtype_name` | Report type (e.g., Industry Research, Company Research, Macro Strategy) / 报告类型 |
| `content` | Report content / 报告内容 |
| `formats` | Available formats (e.g., `["pdf"]`, `["pdf", "doc"]`, `["pdf", "doc", "ppt"]`) / 可用格式列表 |

**IMPORTANT**: 向用户显示结果时，请你扮演投资分析专家对content字段进行分析，给出投资建议。

### Download Response Fields / 下载返回字段

| Field | Description | 字段说明 |
|-------|-------------|----------|
| `title` | Report title / 报告标题 | 报告标题 |
| `filename` | Original filename / 原始文件名 | 原始文件名 |
| `format` | Document format (pdf, doc, or ppt) / 文档格式 | 文档格式 |
| `expires_in` | Link validity period in seconds / 链接有效期（秒） | 链接有效期 |

## Workflow / 工作流程

1. **Search** 使用 `search.mjs` 搜索报告（无需 API Key），返回报告内容，进行分析
2. **Get API Key**  前往 https://pc.yanbaoke.cn/openclaw 获取 API Key（下载必需）
3. **Download** 使用 `download.mjs`、UUID 和 API Key 下载报告

## Error Codes / 错误码

| Code | Description | 说明 |
|------|-------------|------|
| 400 | Format not available | 请求的格式不可用，请检查搜索结果中的 `formats` 字段 |
| 401 | Invalid or missing API Key | API Key 无效或缺失，请从 https://pc.yanbaoke.cn/openclaw 获取 |
| 402 | Insufficient balance | 豆子不足，请前往充值: https://pc.yanbaoke.cn/pay 或者研报客app里面充值(每份报告消耗10 个豆) |
| 404 | Report not found | 报告不存在，请检查 UUID 是否正确 |
| 429 | Rate limit exceeded | 请求过于频繁，请稍后再试 |
| 500 | Server error | 服务器错误，请稍后重试或联系客服 |

## Notes / 注意事项

- 搜索结果按发布时间倒序排列 / Results are sorted by publication date in descending order
- 最大返回500条结果 / Maximum 500 results returned
- 多个筛选条件使用逗号分隔，如：`--org "中信证券,华泰证券,国泰君安"` / Multiple filter values separated by commas
- 下载链接60秒内有效，请及时下载 / Download link expires in 60 seconds
- **搜索无需 API Key，下载需要 API Key**  获取地址[https://pc.yanbaoke.cn/openclaw](https://pc.yanbaoke.cn/openclaw)
- 每份报告仅收费一次，已购买报告可重复下载
- 下载需要消耗豆（每份报告 10 个豆）
- **格式说明**：默认下载 PDF 格式，部分报告支持 DOC 或 PPT 格式。搜索结果中的 `formats` 字段显示该报告支持的格式列表

## API Reference / API 参考

### Search API / 搜索 API

```
GET https://api.yanbaoke.cn/skills/search_report
X-Skill-Version: 2.0.4
X-Skill-ID: yanbaoke-research-report-download
```

### Download API / 下载 API

```
GET https://api.yanbaoke.cn/skills/report_download/{uuid}?format={format}
Authorization: Bearer YOUR_API_KEY
X-Skill-Version: 2.0.4
X-Skill-ID: yanbaoke-research-report-download
```

**Query Parameters / 查询参数:**
- `format` (optional): Document format - `pdf` (default), `doc`, or `ppt` / 文档格式（默认 pdf）

**OpenAI-compatible format** - 使用与 OpenAI 相同的 Bearer Token 认证方式。

**Version Headers** - 所有API请求均包含版本号信息：
- `X-Skill-Version`: 当前技能版本号（如 `2.0.4`）
- `X-Skill-ID`: 技能唯一标识符（`yanbaoke-research-report-download`）
