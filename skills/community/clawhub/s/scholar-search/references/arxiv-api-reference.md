# arXiv API 参数与接口全量说明（Legacy API）

文档日期：2026-03-06  
适用范围：arXiv 官方 `legacy arXiv API`（Metadata API）  
官方文档入口：<https://info.arxiv.org/help/api/user-manual.html>

---

## 1. 接口总览

arXiv 的 Legacy API 在官方手册中只有一个查询接口（`method_name=query`），通过不同参数组合覆盖“关键词检索 + 指定 ID 获取 + 分页 + 排序”。

| 接口名 | method_name | HTTP 方法 | 基础 URL | 返回格式 | 主要用途 |
| --- | --- | --- | --- | --- | --- |
| 查询接口 | `query` | `GET` / `POST` | `https://export.arxiv.org/api/query` | Atom XML (`application/atom+xml`) | 按条件检索论文元数据或按 arXiv ID 批量拉取 |

说明：
- 官方示例里多数是 `http://export.arxiv.org/...`，实际可使用 `https://export.arxiv.org/...`。
- 返回是 Atom XML，不是 JSON。

---

## 2. 查询参数（全量）

> 官方“参数表”列出 4 个核心参数；`sortBy`、`sortOrder` 在排序小节单独给出，属于同一查询接口可用参数。

| 参数名 | 类型 | 默认值 | 是否必填 | 可选值/约束 | 作用 | 示例 |
| --- | --- | --- | --- | --- | --- | --- |
| `search_query` | string | 无 | 否 | 使用 arXiv 查询语法（见第 4 节） | 按字段检索（标题、作者、摘要、分类等） | `search_query=all:electron` |
| `id_list` | comma-delimited string | 无 | 否 | 逗号分隔的 arXiv ID 列表；可带版本号 `vN` | 按指定论文 ID 获取 | `id_list=cond-mat/0207270,hep-ex/0307015v1` |
| `start` | int | `0` | 否 | `>= 0` | 分页起始偏移（0-based） | `start=20` |
| `max_results` | int | `10` | 否 | `>= 0`；单次请求最多 `30000`；单片建议不超过 `2000` | 每次返回条数 | `max_results=100` |
| `sortBy` | string | （未显式写默认值） | 否 | `relevance` / `lastUpdatedDate` / `submittedDate` | 结果排序字段 | `sortBy=lastUpdatedDate` |
| `sortOrder` | string | （未显式写默认值） | 否 | `ascending` / `descending` | 升降序 | `sortOrder=descending` |

补充限制（官方明确）：

| 规则 | 说明 |
| --- | --- |
| `max_results > 30000` | 返回 HTTP `400` |
| 大结果集建议 | 官方建议：若结果数 > 1000，尽量细化查询或分片拉取 |
| 大规模元数据收割 | 官方建议改用 OAI-PMH，而不是一次性大分页拉取 |

---

## 3. `search_query` 与 `id_list` 联动逻辑

| `search_query` | `id_list` | 返回行为 |
| --- | --- | --- |
| 有 | 无 | 返回匹配 `search_query` 的论文 |
| 无 | 有 | 返回 `id_list` 中对应论文 |
| 有 | 有 | 返回 `id_list` 中且同时匹配 `search_query` 的论文（可当作过滤器） |

实用建议：
- 如果你只想“按 ID 精确拿数据”，优先用 `id_list`，不要把 ID 放进 `search_query=id:...`。
- 需要拿某论文最新版本时，用不带版本号的 ID；需要指定版本时，ID 后附 `vN`。

---

## 4. `search_query` 语法参数表

### 4.1 字段前缀（field prefixes）

| 前缀 | 检索字段 | 示例 |
| --- | --- | --- |
| `ti` | 标题 | `ti:transformer` |
| `au` | 作者 | `au:del_maestro` |
| `abs` | 摘要 | `abs:graph` |
| `co` | 作者备注（comment） | `co:"survey"` |
| `jr` | 期刊引用（journal reference） | `jr:"Phys. Rev."` |
| `cat` | 学科分类 | `cat:cs.CL` |
| `rn` | 报告号（report number） | `rn:FERMILAB` |
| `id` | arXiv ID 字段（官方建议改用 `id_list`） | `id:0704.0001` |
| `all` | 全字段联合检索 | `all:multimodal` |

### 4.2 日期过滤（提交日期）

| 语法项 | 格式 | 含义 | 示例 |
| --- | --- | --- | --- |
| `submittedDate` | `[YYYYMMDDTTTT TO YYYYMMDDTTTT]` | 过滤提交时间区间（GMT，24 小时制到分钟） | `submittedDate:[202301010600 TO 202401010600]` |

### 4.3 布尔与分组

| 类型 | 可用值/符号 | 说明 | 示例 |
| --- | --- | --- | --- |
| 布尔运算符 | `AND` | 与 | `au:foo AND ti:bar` |
| 布尔运算符 | `OR` | 或 | `cat:cs.CL OR cat:cs.AI` |
| 布尔运算符 | `ANDNOT` | 排除 | `au:foo ANDNOT ti:survey` |
| 分组 | `(` `)`（URL 编码 `%28` `%29`） | 控制优先级 | `au:x ANDNOT %28ti:a OR ti:b%29` |
| 短语 | `"`（URL 编码 `%22`） | 多词短语匹配 | `ti:%22quantum+criticality%22` |
| 空格 | `+` | URL 中空格编码 | `au:foo+AND+ti:bar` |

---

## 5. 分页与排序参数使用说明

| 场景 | 参数组合 | 说明 |
| --- | --- | --- |
| 普通分页 | `start=0&max_results=10` | 取第 1 页（0-9） |
| 翻页 | `start=10&max_results=10` | 取第 2 页（10-19） |
| 大批拉取 | `max_results<=2000` 分片 + 累加 `start` | 官方建议按片拉取，避免超大响应 |
| 按提交时间排序 | `sortBy=submittedDate&sortOrder=descending` | 新提交优先 |
| 按最后更新时间排序 | `sortBy=lastUpdatedDate&sortOrder=ascending` | 旧更新在前 |
| 按相关性排序 | `sortBy=relevance` | 与查询相关性排序 |

---

## 6. 返回结构字段（Atom XML）

### 6.1 Feed 级字段

| 元素 | 说明 | 是否稳定出现 |
| --- | --- | --- |
| `<title>` | 规范化后的查询串 | 是 |
| `<id>` | 该查询对应的唯一 ID | 是 |
| `<updated>` | 该查询结果最近更新时间（手册说明为当天 00:00） | 是 |
| `<link rel="self">` | 可复用的查询 URL | 是 |
| `<opensearch:totalResults>` | 匹配总数 | 是 |
| `<opensearch:startIndex>` | 本次返回首项索引 | 是 |
| `<opensearch:itemsPerPage>` | 本次返回条数 | 是 |

### 6.2 Entry 级字段

| 元素 | 说明 | 是否稳定出现 |
| --- | --- | --- |
| `<title>` | 论文标题 | 是 |
| `<id>` | 论文 URL（`http://arxiv.org/abs/...`） | 是 |
| `<published>` | 论文 `v1` 提交时间 | 是 |
| `<updated>` | 当前返回版本提交时间 | 是 |
| `<summary>` | 摘要 | 是 |
| `<author><name>` | 作者名（可多个） | 是 |
| `<category>` | 分类标签（可多个） | 常见 |
| `<arxiv:primary_category>` | 主分类 | 常见 |
| `<arxiv:comment>` | 作者备注 | 可选 |
| `<arxiv:affiliation>` | 作者机构（在 `<author>` 下） | 可选 |
| `<arxiv:journal_ref>` | 期刊信息 | 可选 |
| `<arxiv:doi>` | DOI | 可选 |

### 6.3 `<link>` 子类型（Entry 内）

| `rel` | `title` | 指向 | 一般是否有 |
| --- | --- | --- | --- |
| `alternate` | - | 摘要页 | 是 |
| `related` | `pdf` | PDF 链接 | 是 |
| `related` | `doi` | DOI 解析链接 | 否（有 DOI 才有） |

---

## 7. 错误返回与常见报错参数

官方错误同样返回 Atom feed（通常包含单个错误 entry）。

| 项 | 说明 |
| --- | --- |
| 错误消息位置 | `<entry><summary>` |
| 详细说明链接 | `<entry><link>` |
| 典型 HTTP 状态 | 参数非法时常见 `400`（例如 `max_results > 30000`） |

常见参数错误（官方示例）：

| 示例请求片段 | 典型错误 |
| --- | --- |
| `start=not_an_int` | `start` 必须是整数 |
| `start=-1` | `start` 必须 `>= 0` |
| `max_results=not_an_int` | `max_results` 必须是整数 |
| `max_results=-1` | `max_results` 必须 `>= 0` |
| `id_list=1234.1234` | ID 格式错误 |

---

## 8. 限流与使用规范（必须遵守）

> 以下来自 arXiv API Terms of Use（适用于 legacy API，包括本接口）。

| 规则 | 要求 |
| --- | --- |
| 频率限制 | 整体不超过“每 3 秒 1 次请求” |
| 并发连接 | 同时仅 1 个连接 |
| 禁止行为 | 不要通过多机并发等方式规避限流 |

---

## 9. 使用示例（可直接复制）
- 统一脚本路径写法：`scripts/scholar-search.py`。

### 9.1 基础关键词检索

```bash
python scripts/scholar-search.py --source arxiv --params '{"search_query":"all:electron","start":0,"max_results":10}'
```

### 9.2 分类 + 布尔检索 + 按提交时间倒序

```bash
python scripts/scholar-search.py --source arxiv --params '{"search_query":"cat:cs.CL AND all:multimodal","start":0,"max_results":20,"sortBy":"submittedDate","sortOrder":"descending"}'
```

### 9.3 指定作者 + 时间区间过滤

```bash
python scripts/scholar-search.py --source arxiv --params '{"search_query":"au:del_maestro AND submittedDate:[202301010600 TO 202401010600]","start":0,"max_results":50}'
```

### 9.4 精确 ID 拉取（最新版本）

```bash
python scripts/scholar-search.py --source arxiv --params '{"id_list":"cond-mat/0207270"}'
```

### 9.5 精确 ID 拉取（指定版本）

```bash
python scripts/scholar-search.py --source arxiv --params '{"id_list":"cond-mat/0207270v1"}'
```

### 9.6 `id_list` + `search_query` 组合过滤

```bash
python scripts/scholar-search.py --source arxiv --params '{"id_list":"cond-mat/0207270,hep-ex/0307015v1","search_query":"cat:hep-ex"}'
```

### 9.7 在本仓库脚本中调用（`scripts/scholar-search.py`）

```bash
python scripts/scholar-search.py --source arxiv --params '{"search_query":"cat:cs.CL AND all:multimodal","start":0,"max_results":10,"sortBy":"submittedDate","sortOrder":"descending"}'
```


