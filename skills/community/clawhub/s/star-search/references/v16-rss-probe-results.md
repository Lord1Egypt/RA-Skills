# v16.1 RSS 引擎 — 20 无效域的替代抓取策略

**测试时间**: 2026-06-02
**目标**: v15.1 探针确认 site:bing 0 命中的 20 个域，逐个找替代抓取方案
**方法**: aiohttp + RSS XML 正则解析（无 feedparser 依赖，< 1s/请求）

## 探针结果：5/20 域 RSS 有效（v16.1 已接）

| 域 | RSS endpoint | items | sample | 状态 |
|----|-------------|-------|--------|------|
| **ithome** | https://www.ithome.com/rss/ | 60 | "华硕推出 ASUS Pad 平板" | ✅ v16.1 接 |
| **36kr** | https://36kr.com/feed-newsflash | 20 | "恒生指数涨超1%" | ✅ v16.1 接 |
| **sspai** | https://sspai.com/feed | 10 | "派早报：英伟达..." | ✅ v16.1 接 |
| **oschina** | https://www.oschina.net/news/rss | 50 | "Surface Laptop Ultra" | ✅ v16.1 接 |
| **woshipm** | https://www.woshipm.com/feed | 15 | "AI Agent 产品化瓶颈" | ✅ v16.1 接 |

## 8 域：feed 链接已失效（404 / 0 items / DNS 失败）

| 域 | 原因 | 备注 |
|----|------|------|
| jianshu | 404 | 简书 RSS endpoint 已下线（短链 service） |
| segmentfault | 0 items | 改版后无 feed |
| jiqizhixin | 0 items | 机器之心 RSS endpoint 失效 |
| yicai | 404 | 第一财经 feed 需登录 |
| caixin | 0 items | 财经 RSS 需订阅 |
| netease_news | 0 items | 网易 news feed 死链 |
| people | DNS 失败 | feedx.info 第三方聚合被墙 |
| xinhuanet | DNS 失败 | 同上 |
| ifeng | DNS 失败 | 同上 |
| chinanews | DNS 失败 | 同上 |

## 5 域：第三方 RSSHub/feedx.info 兜底（本机不可用）

| 域 | 候选 endpoint | 状态 |
|----|---------------|------|
| juejin | rsshub.app/juejin/category/frontend | ❌ DNS 失败（rsshub.app 在国内被墙） |
| huxiu | huxiu.com/rss/0.xml | ❌ timeout（huxiu 反爬严格） |
| lieyunwang | lieyunwang.com/rss | ❌ DNS 失败 |
| geekpark | geekpark.net/rss | ❌ Server disconnected（feed 关闭） |
| infoq | feedx.info/rss/infoq.xml | ❌ DNS 失败 |

**结论**：这 5 域需部署 RSSHub 自建实例（国外机器可达 feedx.info / rsshub.app），本机网络受限于 GFW。**token-star.cn 腾讯云服务器可考虑部署**。

## 6 域：强反爬 / 商业数据 — RSS/聚合均不可行

| 域 | 性质 | 替代方案 |
|----|------|---------|
| **bilibili** | 视频内容 | 走移动端 API（`api.bilibili.com/x/web-interface/search`）+ UA 模拟（**未实测**） |
| **抖音** | 视频内容 | 走 tiktok.com 跨域爬（**未实测**） |
| **小红书** | UGC 笔记 | 移动端 API（**未实测**） |
| **雪球 xueqiu** | 财经数据 | 官方 API 付费 |
| **华尔街见闻 wallstreetcn** | 财经数据 | RSS endpoint 已下线 |
| **天眼查 tianyancha / 企查查 qichacha** | 企业征信 | 官方 API 付费 |
| **yicai / caixin** | 财经新闻 | 需付费订阅 |

**结论**：这 7 域短期不接，留待 token-star.cn 上部署 RSSHub + 反向代理后再说。

## v16.1 RSS 引擎技术要点

### 无 feedparser 依赖
直接用 `re.findall(r'<item[\s>](.*?)</item>', xml, re.DOTALL)` 解析，省去 1 个第三方库。

### RSS endpoint 固定 → 客户端按 query 过滤
- endpoint 不带 query（RSS 订阅语义就是全量）
- `_filter_by_query(results, query, engine)` 客户端按 query 关键词命中过滤
- 兜底：关键词全不命中时取前 5 条（保证 RSS 引擎总能返回结果）

### HTML 实体转义
RSS description 里 `&lt;` / `&gt;` / `&amp;` / `&quot;` / `&#34;` / `&nbsp;` / `&#39;` 在 `_parse_rss` 里手工替换。

### 性能
- 单 RSS 引擎请求 < 0.7s（带 UA，session 复用）
- 5 个 RSS 引擎并联 ~1.5s（和 deep mode 其他引擎叠加）
- 缓存友好：同一个 query 走 RSS 不同次时间相近，命中率 50%+

## 后续建议（v16.2 候选）

1. **部署 RSSHub 自建**（token-star.cn 腾讯云）：解锁 juejin/huxiu/lieyunwang/infoq + 央媒聚合
2. **bilibili/抖音/小红书走移动端 API**（UA 模拟 + graphql query）：v15 探针未做
3. **付费源兜底**：雪球/华尔街/天眼查等强反爬，可对接百度千帆/天眼 API（用户决定）
4. **RSS 引擎 health-check**：定期探测 RSS endpoint 死活，死了自动禁用
