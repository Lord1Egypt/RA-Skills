---
name: taobao-shop-price
slug: taobao-shop-price
version: 1.0.3
description: |
  全网电商商品检索与比价工具（China E-commerce Price Comparison）。
  支持淘宝/天猫、京东、拼多多、抖音、快手、1688 等主流电商平台。
  根据商品名称跨平台搜索、智能过滤、生成比价表格、推荐优选商品并获取购买链接。
  China e-commerce product search and price comparison tool. Search and compare prices across Taobao, Tmall, JD.com (Jingdong), Pinduoduo (PDD), Douyin Shop, Kuaishou Shop, 1688 (Alibaba wholesale), Suning, Vipshop. Find the cheapest price, best deals, discounts, coupons, and get purchase links. Supports cross-platform product search, smart filtering, recommendation ranking, and price table generation.
  Use when user asks to: compare prices across platforms, find the lowest price, search products on Taobao/JD/Pinduoduo, find deals or coupons, check where to buy cheap, get purchase links, do shopping research, or find the best value product.
triggers:
  - 比价
  - 帮我比价
  - 帮我检索
  - 帮我搜索
  - 帮我购买
  - 帮我找
  - 最低价
  - 哪里买便宜
  - 价格对比
  - 帮我从淘宝检索
  - 帮我从天猫检索
  - 帮我从京东检索
  - 帮我从拼多多检索
  - 淘宝搜索
  - 京东搜索
  - 拼多多搜索
  - 帮我查一下
  - 找优惠
  - 找购买链接
  - compare prices
  - find cheapest
  - where to buy
  - best deal
  - price check
  - search product
  - search on taobao
  - search on jd
  - search on pinduoduo
metadata: {"clawdbot":{"emoji":"📦"}}
---

# 全网电商比价 / E-commerce Price Comparison

基于 price.py 脚本，实现"搜索 → 表格+推荐 → 用户选品 → 获取链接 → 汇总输出"的完整比价流程。

**支持平台：** 淘宝/天猫、京东、拼多多、抖音、快手、1688

**Supported platforms:** Taobao/Tmall, JD.com, Pinduoduo, Douyin, Kuaishou, 1688

## 平台编码 (sourceType)

| sourceType | 平台 |
|---|---|
| 0 | 全部 |
| 1 | 淘宝/天猫 |
| 2 | 京东 |
| 3 | 拼多多 |
| 4 | 苏宁 |
| 5 | 唯品会 |
| 7 | 抖音 |
| 8 | 快手 |
| 22 | 1688 |

## 工作流程

### 第一步：构造关键字并检索

从用户输入的商品名中提取核心关键字，调用 search 命令：

```bash
python3 scripts/price.py search --keyword "关键字" --sourceType 0 --pages 1 --format csv
```

- 默认 `--sourceType 0`（全部平台）、`--pages 1`（第1页）、`--format csv`（CSV 格式便于解析）
- 如果用户指定了平台或需要更多结果，调整对应参数

### 第二步：过滤无关商品 + 输出推荐表格

从 search 返回的 CSV 结果中，逐条检查商品名称（`商品` 列）：
- **保留**：名称与用户搜索的商品明确相关的条目
- **排除**：名称明显不相关、品类不符的条目
- 过滤时注意同义词、别名、不同叫法（如"纸尿裤"vs"拉拉裤"）

过滤完成后，**立即**输出 Markdown 表格，列名：

| ID | 名称 | 平台 | 商铺 | 价格 | 原价 | 优惠 | 月销 | 推荐度 | 推荐理由 |

**各列说明：**

- **ID**：序号（从1开始），用于后续用户选品引用
- **名称**：商品标题（过长时截取关键部分，保留核心信息）
- **平台**：根据 sourceType 映射平台名称（如 1→淘宝，2→京东，3→拼多多 等）
- **商铺**：shopName
- **价格**：actualPrice
- **原价**：originalPrice（如与现价相同可标 `-`）
- **优惠**：couponPrice（无优惠标 `-`）
- **月销**：monthSales
- **推荐度**：综合评估该商品，使用 ⭐ 1-5 星评级（⭐ 最低，⭐⭐⭐⭐⭐ 最高）
- **推荐理由**：一句话说明推荐/不推荐的关键原因（如"最低价+高销量"、"名称匹配但价格偏高"、"月销过少需谨慎"等）

**推荐度评估标准（综合三项因素）：**

1. **相关性**（权重最高）：商品名称与用户搜索意图的匹配程度
2. **价格**：在同类商品中的价格竞争力（越低越好）
3. **月销量**：反映市场认可度（越高越好）

评估示例：
- 名称高度匹配 + 价格最低/较低 + 月销高 → ⭐⭐⭐⭐⭐ → 理由："高度匹配+最低价+销量领先"
- 名称匹配 + 价格适中 + 月销中等 → ⭐⭐⭐ → 理由："名称匹配，价格适中"
- 名称勉强相关 + 价格偏高 + 月销低 → ⭐ → 理由："相关度低，价格偏高"

**按推荐度从高到低排列表格。推荐度相同时按价格升序。**

> ⚠️ **必须记住每个商品的 goodsId 和 sourceType**（从 search 结果中获取），后续步骤需要用到。不要在表格中展示这两列，但必须内部保留映射关系：ID → {goodsId, sourceType}。

### 第三步：输出检索说明 + 等待用户选品

表格输出后，紧接着输出检索说明，包含以下内容：

#### 检索概况
- 搜索关键字
- 覆盖平台
- 检索结果总数 / 过滤后保留数量

#### 推荐排序
- 无序列表列出推荐度 ⭐⭐⭐⭐ 及以上的商品，格式：`ID. 商品名称 - 平台 - ¥价格 (推荐度: ⭐⭐⭐⭐⭐) — 理由`
- 理由为简短一句话，说明为何推荐该商品（如"最低价+高销量"、"性价比最优"等）
- 方便用户快速定位优质商品

#### 注意事项
- 价格为检索时点价格，可能随时间变动
- 部分商品有优惠券，下单前确认优惠是否可用
- 月销数据仅供参考，不代表绝对品质
- 建议综合推荐度、价格、销量做决策

#### 汇总结论
- 简要总结本次检索的关键发现（如：最低价商品、性价比最高、销量冠军等）

#### 互动提示

在检索说明末尾输出：

> 📌 **请输入您关注的商品序号（可多选，用逗号或空格分隔），我将为您获取购买链接。**
> 例如：`1, 3, 5` 或 `1 3 5`
> 💡 **推荐选择：`{推荐ID列表}`**（推荐度 ⭐⭐⭐⭐ 及以上的商品）

其中 `{推荐ID列表}` 为推荐度 ⭐⭐⭐⭐ 及以上商品的 ID，用逗号分隔（如 `1, 3, 5`）。如果推荐度均低于 ⭐⭐⭐⭐，则不显示推荐选择行。

然后 **停止并等待用户输入**，不要自动进入下一步。

### 第四步：根据用户选择的 ID 获取链接

用户输入商品序号后：

1. 根据用户输入的 ID，从内部映射中找到对应的 `goodsId` 和 `sourceType`
2. 逐个调用 link 命令获取购买链接：

```bash
python3 scripts/price.py link --goodsId "{goodsId}" --sourceType {sourceType}
```

3. 每次调用间隔 0.5 秒，避免请求过快
4. 记录每个商品的链接（优先 appUrl，次选 schemaUrl，最后用口令）

### 第五步：汇总输出带链接的最终结果

将用户关注的商品整理为最终表格，列名：

| ID | 名称 | 平台 | 商铺 | 价格 | 链接 |

- **链接**：直接展示链接 URL 纯文本（优先 appUrl，次选 schemaUrl），**不要使用 `[购买链接](URL)` 格式**；如有口令也一并附上
- 按价格升序排列

表格后附汇总结论，帮助用户快速决策。

## 关于脚本

脚本路径：`scripts/price.py`
- 脚本无第三方依赖，仅使用 Python 标准库
- 脚本仅作为客户端请求 maishou88.com，不会读写本地文件

## 使用说明 / Usage Guide

当用户问"你能干什么"、"这个技能有什么用"、"你能帮我买什么"时，输出以下说明：

> 🔍 **全网电商比价工具**
>
> 我可以帮你在淘宝/天猫、京东、拼多多、抖音、快手、1688 等平台搜索商品、对比价格、找到最优购买方案。
>
> **你可以这样问我：**
> - `帮我比价 iPhone 16 Pro` — 全网检索对比各平台价格
> - `帮我从京东检索 AirPods Pro` — 指定平台搜索
> - `帮我找最便宜的纸尿裤` — 找最低价商品
> - `帮我搜索戴森吹风机` — 全平台商品搜索
> - `哪里买小米手环便宜` — 价格对比
>
> **完整流程：** 搜索商品 → 过滤推荐 → 你选商品 → 我给购买链接
>
> I can search and compare product prices across major Chinese e-commerce platforms (Taobao, JD.com, Pinduoduo, etc.), and provide you with the best deals and purchase links.
