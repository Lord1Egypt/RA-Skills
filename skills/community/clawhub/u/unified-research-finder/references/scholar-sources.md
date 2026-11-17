# Scholar 数据源技术参考

本文件供 WorkBuddy 在执行 `scholar_search.py` 时参考，说明四个数据源的
请求方式、字段结构与兜底逻辑。**所有内容必须来自脚本真实返回，不得编造。**

## 数据源与优先级

`--source auto`（默认）按以下顺序依次尝试，取第一个返回可用结果的源：

| 优先级 | key         | 名称                | 类型 | 检索地址                                      |
|--------|-------------|---------------------|------|-----------------------------------------------|
| 1      | kiphub      | KipHub学术          | HTML | `https://www.kiphub.com/search?wd=...`        |
| 2      | lanfanshu   | 烂番薯学术搜索      | HTML | `https://scholar.lanfanshu.cn/scholar?hl=zh-CN&as_sdt=0,5&q=...&btnG=` |
| 3      | scholar_pro | 学术搜索Pro         | HTML | `https://www.googlescholar.pro/search_results.php?q=...` |
| 4      | dotaindex   | 灯塔学术搜索        | JSON | `https://www.dotaindex.com/api/scholar/search?q=...` |
| 5      | hk          | Google Scholar 香港镜像 | HTML | `https://scholar.google.com.hk/scholar?q=...` |
| 6      | google      | Google Scholar 官方站   | HTML | `https://scholar.google.com/scholar?q=...`    |

> 注意：kiphub 使用 `wd`（而非 `q`）作为查询参数名；烂番薯需携带 `hl=zh-CN&as_sdt=0,5&btnG=` 以绕过反爬墙。

用户也可用 `--source lanfanshu|dotaindex|hk|google` 强制指定单一源。

## 公共检索参数

脚本统一将以下参数拼入 URL：

- `q` — 检索词（必填）
- `start` — 起始偏移，分页步长 10
- `hl` — 界面语言，默认 `zh-CN`
- `as_ylo` — 起始年份下限（`--ylo 2020`）
- `scisbd=1` — 当 `--sort date` 时附加，表示按日期排序（相关性排序不加）

## 灯塔（dotaindex）JSON API

最稳、最快、内存占用最低，**优先使用**。

- 端点：`GET https://www.dotaindex.com/api/scholar/search`
- 请求头需带 `Referer: https://www.dotaindex.com/scholar` 与 `Accept: application/json`
- 响应（顶层字典）：
  - `total` — 命中总数（用于 `count`）
  - `results[]` — 每篇文献，关键字段：
    - `titleHtml` — 含 `<a href="...">` 的标题，解析出 `url` 与标题文本
    - `author` — 作者串，如 `"K Han, A Xiao, E Wu…"`
    - `year` / `journal` / `publisher`
    - `abstractHtml` — 摘要片段（去标签）
    - `citationCount` — 被引次数（字符串数字）
    - `openAccessUrl` / `accessLinks[].url` — PDF 全文链接
- 限流表现：被限流时返回 `results: []` 且 `total: 0`（而非报错）。脚本在首页空结果时退避 1.5s 重试一次。

## KipHub 学术（kiphub）

自定义 Bootstrap 结构的 Scholar 镜像：

- 检索地址：`https://www.kiphub.com/search?wd=QUERY`（注意查询参数名是 `wd` 而非 `q`）
- 结果容器：`<div class="paper-summary-wrapper">`
- 标题/链接：`<div class="pp-title">` 内的第一个 `<a href="...">`
- 作者·期刊·年份：`<div class="author">` 内的文本（格式：`作者, 作者... -期刊, 年份`）
- 当前不支持摘要片段与被引次数

## 学术搜索Pro（scholar_pro）

自定义 card 布局的 Scholar 镜像：

- 检索地址：`https://www.googlescholar.pro/search_results.php?q=QUERY`
- 结果容器：`<div class="card">`
- 标题/链接：`<h3 class="card-title">` 内的 `<a href="...">`
- 元信息：`<div class="card-meta">` 内的文本
- 摘要：`<div class="card-text">` 内的文本
- 被引次数：card 文本中 `被引用次数 N` / `Cited by N` 模式
- PDF 链接：`[PDF]` 后的 `<a>` 或 `card-side-links` 内的第一个 `<a>`

## 烂番薯 / 香港镜像 / 官方（经典 Scholar HTML）

三者均为服务端渲染的经典 Google Scholar 结构，由同一个 HTML 解析器处理：

- 结果容器：`<div class="gs_r ...">`（顺序无关，模糊匹配）
- 标题/链接：`<h3 class="gs_rt"><a href="URL">标题</a></h3>`
- 作者·来源·年份：`<div class="gs_a">作者 - 期刊, 年份 - 出版方</div>`
- 摘要片段：`<div class="gs_rs">`（若该 class 缺失，则取 `gs_a` 与 `gs_fl` 之间的文本兜底）
- 被引次数：`gs_fl` 内 `被引用次数 N` / `Cited by N` 等写法
- PDF 链接：`[PDF]` 之后的 href，或 `gs_ggs` 区域内的 href

**烂番薯特别说明**：需带 `Referer: https://scholar.lanfanshu.cn/`，否则返回 403。
该站对高频请求会限流（403），脚本会自动回退到下一源。

**香港镜像 / 官方站特别说明**：在中国大陆常被网络阻断（连接超时 / SSL 异常）。
若 HTTP 方式失败，可让用户安装 Playwright 后以 `--browser` 模式用无头浏览器兜底。

## 拦截 / 验证码检测

- HTTP 403 / 429 → 记为「被拦截」，自动尝试下一源。
- HTML 中出现 `unusual traffic` / `我们的系统检测到` / `captcha` / `why did this happen` 等标记 → 记为「被拦截」。
- 全部源均无结果时，`ok` 置为 false（或 results 为空），并在 `note` 中说明原因，**绝不返回虚构文献**。

## 性能与依赖

- 默认纯标准库（`urllib`），**无需安装任何第三方包**，内存占用低、启动快。
- `--browser` 模式依赖 Playwright（`pip install playwright && playwright install chromium`），
  仅在 HTTP 被拦截且用户确认启用时作为兜底，避免常驻重进程。
