# 引擎清单与接入规范（Signal-Search）

> **单真相源 = `config.json`**；本文档是其人类可读展开，也是 §13 **M02 验收对照源**（每个 `id` 必须在此有对应 URL）。
> 通用 17 引擎 = `cn`(8) + `global`(9)；`academic`(2) 与 `vertical`（按 domain）为附加免费源，不计入"通用 17"但同样免费无 Key。
> 所有 URL 经 `scrape.py` 反爬层发出（`search.py` / `connector.py` 不裸发 HTTP）。`{q}` 占位符由 `urllib.parse.quote` 编码。

---

## 1. 通用 17 引擎（M02 计数对象）

| id | name | region | 最佳场景 | 时效 | search_url 模板 | 关键参数 |
|----|------|--------|----------|------|-----------------|----------|
| Baidu | 百度 | CN | 通用/中文网页 | 中 | `https://www.baidu.com/s?wd={q}` | `wd` |
| BingCN | 必应中国 | CN | 通用/学术 | 中 | `https://cn.bing.com/search?q={q}` | `q` |
| BingINT | 必应国际 | INT | 英文/学术 | 中 | `https://www.bing.com/search?q={q}` | `q` |
| 360 | 360搜索 | CN | 通用 | 低 | `https://www.so.com/s?q={q}` | `q` |
| Sogou | 搜狗 | CN | 通用/微信外链 | 中 | `https://www.sogou.com/web?query={q}` | `query` |
| WeChat | 微信 | CN | 公众号/中文深度 | 高 | `https://weixin.sogou.com/weixin?type=2&query={q}` | `query` |
| Toutiao | 头条 | CN | 资讯/时效 | 高 | `https://so.toutiao.com/search?keyword={q}` | `keyword` |
| Jisilu | 集思录 | CN | 金融数据/固收 | 高 | `https://www.jisilu.cn/search?q={q}` | `q` |
| Google | Google | INT | 通用/英文 | 中 | `https://www.google.com/search?q={q}` | `q` |
| GoogleHK | Google香港 | INT | 通用/中文国际 | 中 | `https://www.google.com.hk/search?q={q}` | `q` |
| DuckDuckGo | DuckDuckGo | INT | 隐私/通用 | 中 | `https://html.duckduckgo.com/html/?q={q}` | `q`（用 html 端点避 JS） |
| Yahoo | Yahoo | INT | 通用 | 低 | `https://search.yahoo.com/search?p={q}` | `p` |
| Startpage | Startpage | INT | 隐私/Google结果 | 中 | `https://www.startpage.com/sp/search?query={q}` | `query` |
| Brave | Brave | INT | 隐私/通用 | 中 | `https://search.brave.com/search?q={q}` | `q` |
| Ecosia | Ecosia | INT | 通用/环保 | 低 | `https://www.ecosia.org/search?q={q}` | `q` |
| Qwant | Qwant | INT | 隐私/欧洲 | 中 | `https://www.qwant.com/?q={q}` | `q` |
| WolframAlpha | WolframAlpha | INT | 计算/事实/数据 | 高 | `https://www.wolframalpha.com/input?i={q}` | `i`（URL 编码整句） |

> **时效友好度**：`高`=优先用于 latest/realtime 类 query；`低`=结果偏陈旧，仅作补充源。

---

## 2. 学术源（2，免费无 Key）

| id | name | search_url | 说明 |
|----|------|-----------|------|
| arXiv | arXiv | `https://arxiv.org/search/?searchtype=all&query={q}` | 预印本，覆盖 CS/物理/数学 |
| SemanticScholar | Semantic Scholar | `https://www.semanticscholar.org/search?q={q}&sort=relevance` | 论文+引用图谱，可补 `&year=` 限域 |

> 学术源默认在 L2/L3 且 `intent∈{research}` 时启用；`arXiv` 也可直接命中 `/abs/` JSON。

---

## 3. 垂直源（按 `constraints.domain` 路由，全部 `access:free`）

| domain | 源 id（name） | search_url / api |
|--------|---------------|------------------|
| academic-cn | BaiduScholar(百度学术) / CNKI(知网) / WanFang(万方) | `xueshu.baidu.com/s?wd=` · `kns.cnki.net/...` · `wanfangdata.com.cn/search?q=` |
| tech-cn | CSDN / Juejin(掘金) / cnblogs(博客园) / Gitee | `so.csdn.net/so/search?q=` · `juejin.cn/search?query=` · `cnblogs.com/search?q=` · `search.gitee.com/?q=` |
| code | GitHub / StackOverflow / HackerNews | `github.com/search?q=` · `stackoverflow.com/search?q=` · `hn.algolia.com/api/v1/search?query=`（**免费 API**，优先） |
| finance-cn | Xueqiu(雪球) / Eastmoney(东方财富) / SinaFin(新浪财经) | `xueqiu.com/search?q=` · 东财行情走 `push2.eastmoney.com` JSON（见 `eastmoney-example.md`）· `search.sina.com.cn/?q=` |
| social-cn | Zhihu(知乎) / Weibo(微博) / Bilibili | `zhihu.com/search?type=content&q=` · `s.weibo.com/weibo?q=` · `search.bilibili.com/all?keyword=` |
| knowledge | Wikipedia / BaiduBaike / Wikidata | `en.wikipedia.org/wiki/Special:Search?search=` · `baike.baidu.com/item/` · `wikidata.org/w/index.php?search=` |
| news-cn | Xinhua(新华网) / People(人民网) / Kr36(36氪) | `so.news.cn/search?keyword=` · `search.people.com.cn/...` · `36kr.com/search/articles/` |
| legal-cn | GovCN(中国政府网) / PKULaw(北大法宝) | `sousuo.www.gov.cn/...` · `pkulaw.com` |
| medical | PubMed | `pubmed.ncbi.nlm.nih.gov/?term=` |
| regional | Yandex / Naver / Mojeek / Marginalia | `yandex.com/search/?text=` · `search.naver.com/...` · `mojeek.com/search?q=` · `search.marginalia.nu/search?query=` |

> 垂直源仅在 `constraints.domain` 命中时加入候选池，保持通用档位精简（避免工具描述预算爆炸）。全部 `free`，开箱即跑，无 API Key。

---

## 4. 接入注意事项

- **JSON API 优先**：如 `HackerNews`(Algolia)、东财 `push2`、Wikipedia `api.php`、`Wikidata` SPARQL——命中即结构化、零浏览器挑战、最省 token。
- **source_type 映射**（供 SBA 打分，见 §5.9 / §7）：
  - `gov`：`.gov` / 人民网 / 新华网 / 中国政府网
  - `academic`：arxiv/semanticscholar/知网/万方/百度学术/PubMed
  - `media`：新华/人民/36氪/新浪/澎湃类
  - `forum`：贴吧/论坛/Stack Overflow（技术问答按场景可升 media）
  - `selfmedia`：公众号/头条/知乎专栏/百家号
  - `vendor`：厂商官方文档/东财研报类
  - 其余 `unknown`
- **失败隔离**：单引擎抓取失败（403/429/超时）由 `connector.py` try 包裹并换同组源，不中断整次检索（M22）。
- **D3 铁律**：本表无任何 `type:"api"` 或付费 Key 字段；`api-extra`(Tavily/Exa/Perplexity/Kagi/Firecrawl/SerpApi/SearXNG 公共实例) 一律不在列。
