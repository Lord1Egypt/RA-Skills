---
name: tb-opportunity-radar
slug: tb-opportunity-radar
version: 1.0.2
displayName: 淘宝竞品分析选品雷达 · 新品卖点拆解
summary: 新品还没上，先知道同行评价里藏着哪些没人做的点。给 1 个淘宝/天猫商品链接，自动配 2 个不同店铺的竞品一起比：主图卖点、价格销量、买家评价（刷单自动剔除）全采齐，再对照 xhs 同类需求，产出一份 HTML 报告——别人已经做了什么、买家还在抱怨什么、哪些点没人做，新品上架前就找准差异化机会。不需要任何 API key，用你 Chrome 里已登录的淘宝账号跑。当用户想做竞品分析、选品、差评分析、找新品机会时唤起。
description: 输入 1 个淘宝/天猫商品链接，自动做类目级竞品分析：起点商品加 2 个不同店铺竞品，三品一起采主图、详情长图、SKU、价格销量和买家评价，刷单评价自动剔除，再对照 xhs 同词需求，产出面向电商运营的 HTML 报告——同行已经做了什么、买家还在抱怨什么、哪些点没人做，新品上架前就找准差异化机会。当用户给出淘宝/天猫商品链接，想做竞品分析、选品参考、差评分析、买家需求缺口、找新品机会时唤起；只需采集评价做参考用同系列 taobao-review-export。
---

# tb-opportunity-radar（新品机会雷达）

一句话：给一个淘宝/天猫商品链接，自动跑完「三品采集 → 图片卖点打标 → 评价分层 → xhs需求源 → HTML 报告」这条类目级竞品分析流水线。

## 前置条件

- 本机 Chrome 装了浏览器扩展，并且**已在 Chrome 登录淘宝/天猫**（未登录会被登录墙拦截，skill 会明确报错并提示登录）；xhs侧需要能正常浏览
- 浏览器中继服务运行中（HTTP API `http://127.0.0.1:3459`）
- 需要判断/归纳的环节走 LLM 子会话，经本地 pipeline 服务（`:3460`）代跑，因此**本地 pipeline 服务需处于运行状态**
- macOS：图片文案由 LLM 子会话多模态直接读图提取（pipeline :3460 后端模型支持图片；不使用本地 OCR）

## 使用方式

```bash
node skill.mjs input.json
# 或：cat input.json | node skill.mjs
```

`input.json`：

```json
{
  "productUrl": "https://detail.tmall.com/item.htm?id=1053286842802",
  "searchTerm": "",
  "seed": 20261016,
  "outputDir": "/abs/path/to/output"
}
```

| 入参 | 必填 | 说明 |
|---|---|---|
| `productUrl` | 是 | 淘宝 `item.taobao.com/item.htm?id=...` 或天猫 `detail.tmall.com/item.htm?id=...`，纯链接即可 |
| `searchTerm` | 否 | 聚焦搜索词覆盖。不传则从商品标题/类目自动猜（规则：聚焦、不泛，优先「品类词+关键规格」） |
| `seed` | 否 | 随机选品种子（前 5 选 1 的可复现性），默认当天 `yyyymmdd` |
| `outputDir` | 否 | 输出目录，默认 `.workbuddy/output/tb-opportunity-radar-run/` |

## 流程

1. 建独立 tab 分组 → 打开起点商品（A），采集标题/店铺（shopName 选择器 + 店铺链接 shopId）/到手价/销量/评价数/SKU/主图
2. 点「图文详情」→ 步进滚动懒加载 → 收详情长图 → 真实点击「查看全部评价」（page.search 取 ref + page.click，合成事件无效）→ 内联卡片边滚边采评价（8 字段）
3. 自动猜聚焦搜索词（子会话；`searchTerm` 非空时跳过）
4. 淘宝站内搜索（taobao 域 tab 内 `location.assign` 直达 `s.taobao.com/search?q=`）→ 取前 5 商品卡片（id 取最长数字串且 ≥11 位滤假 id，店名取卡片 `shopNameText--`）→ `mulberry32(seed)` 随机定起点后顺延扫描：**同店（卡片店名先比，详情页 shopId 再核实）、失效商品（详情页核实为宝贝不存在/缺价格销量）、重复候选都跳过并记录**，直到选出 B、C
5. B、C 各走一遍第 1~2 步的同管线采集
6. 图片下载 → 转换 → LLM 子会话读图提取文案 + 七维打标（人群/环境/作用/形态/成分/保障/体验，子会话）→ 频次 × 销量加权
7. 评价三层分层（规则化跑真实数字）：① 无效忽略不计分母 ② 跨用户公共子串 ≥18 字剔除 ③ 其余视为真实
8. xhs：聚焦词 + 1 个变体词检索 → 选帖（子会话，词命中 + 评论密度）→ 深挖 ≥2 篇评论区
9. 需求点归纳 + 结论表（子会话，措辞平实、禁浮夸词）→ 拼装 HTML 报告

## 输出

`outputDir/` 下：

- `report.html` — 报告（关键图 base64 内嵌），板块：判定口径 / 样本构成含种子与前 5 明细 / 频次×销量加权表 / 评价分层结果 / 真实评价满足度表 / xhs需求原话 / 结论表（证据→运营含义→可做的事）/ 边界说明
- `data/item-{A,B,C}.json` — 三品元数据、图片 URL、评价、LLM 提取的图片文案、标签
- `data/reviews/{A,B,C}/reviews.md` — 每品评价明细（含分层标注）
- `data/review-classify.json` — 分层规则与全量明细（含 why）
- `data/selection.json` — 选品记录：种子、聚焦词、搜索 URL、前 5 明细、选中结果与全部顺延跳过原因（同店/失效/重复）
- `data/tag-matrix.json` — 三品标签矩阵 + 加权结果
- `data/xhs-demand.jsonl` — xhs检索/笔记/评论/需求点，一行一条

stdout 只输出一行 JSON：`{"status":"success|partial|failed","summary":"...","output_dir":"..."}`，其余日志走 stderr。

## 已知边界

- 评价内联展开区块上限约 22 条；展开不足 20 条会重取 ref 再点一次，仍不足且页面评价总数更大的记「未到底」并在运行摘要标注（每品 ≥20 条是验收底线，页面总数本身不足的算到底）
- 同店排除：搜索卡片店名（`shopNameText--`）先比一轮，详情页 shopId（店铺链接 href）再核实一轮，命中顺延并记录在 skips
- 候选商品已下架（跳转「宝贝不存在」错误页）或缺价格销量字段时，会自动顺延到下一个候选并记录在 skips；前 5 全部不可用时该样本缺失，status 只能到 partial（不足三个有效样本不会报 success）
- 销量口径统一取商品页「已售 N+」（「万」按 ×10000 折算）；价格取页面「￥N 起」结构
- 三品只是类目里的 3 个样本，结论是这三个样本之间的比较，不代表整个类目
- 全程操作间隔 ≥1.8s、串行采集；商品页或搜索页被登录墙/访问限制拦截时直接报错，提示在 Chrome 登录淘宝后重试
