# goods_styles

款式/配色列表。按 `goods_id` 分页返回该商品的款式及 `style_id`。链接解析也可直接提供真实款式 ID；不返回尺码、容量、版本等 SKU 规格，那些在 `search_sku`。

## 入参

| 参数 | 类型 | 必填 | 默认 | 说明 |
| --- | --- | --- | --- | --- |
| goods_id | string | 是 | 无 | 识货商品 ID，不透明字符串，固定 12 字符、区分大小写，原样取自工具返回值 |
| page | integer | 否 | 1 | 页码，从 1 开始，最小 1 |
| page_size | integer | 否 | 10 | 每页条数，1～30 |

## 响应字段解释

| 路径 | 类型 | 是否恒有 | 含义 | 展示与限制 |
| --- | --- | --- | --- | --- |
| data.goods_id | string | 是 | 回显的商品 ID，不透明字符串，固定 12 字符、区分大小写 | 必须与请求一致，核对没有串实体 |
| data.total | number | 是 | 款式总数 | 不保证是全量总数，可能等于当前页条数，因此翻页只看 `has_more`，不用 `total` 反推页数 |
| data.page | number | 是 | 当前页码 | 回显值 |
| data.page_size | number | 是 | 当前页大小 | 回显值 |
| data.has_more | boolean | 是 | 是否还有下一页 | 翻页的唯一依据 |
| data.styles | array | 是 | 款式列表 | 条数可能少于 `page_size`，每项一定带 `style_id` 和 `style_name` |
| data.styles[].style_id | string | 是 | 款式/配色 ID，不透明字符串，固定 12 字符、区分大小写 | 原样传给 `search_sku` 或 `goods_style_price_trend` |
| data.styles[].style_name | string | 是 | 款式/配色名称 | 只陈述名称原文。名称里的颜色词不等于材质、版本或适用人群 |
| data.styles[].price | string | 否 | 款式展示价，格式 `￥550` | 空串时省略。固定称“款式展示价”，不是到手价、不是历史价、不是最低价 |
| data.styles[].image_url | string | 否 | 款式图 | 不凭图片颜色或款式外观补任何属性事实 |
| data.styles[].href | string | 否 | 款式详情入口 | 已转成 `https://m.shihuo.cn/...` 的 H5 地址，可直接展示；不展示 `shihuo://`，按 `link_convert.md` 的展示规则处理 |

`StyleCard` 只有以上 5 个字段，没有 attrs、库存、销量或规格字段，不从名称或图片补齐这些数据。

## 款式匹配规则

1. 用户明确说了配色或款式时，按 `style_name` 的实际含义匹配，可识别含义清晰且唯一的等价写法，不要求与用户原话逐字一致。多色款、近似色、不同性别、不同鞋帮、不同版本都不算一致，不擅自换款。
2. 精确匹配为空时不替换、不就近取值，说明未找到指定款式，并按需提供真实可选的 `style_name`；只有用户选择了其它款式才继续查询该款式。
3. 精确匹配唯一时收口到该 `style_id`，可继续调 `search_sku` 或 `goods_style_price_trend`。
4. 信息足够时结合已有条件与真实结果直接匹配；用户要帮选或允许参考款式时，可根据需求选择并说明参考款式；只有无法依据现有条件确定、且会影响结论的歧义才展示真实选项并追问，不设固定排序选择规则。只问款式列表时直接回答列表，无需追问。

## 调用说明

前置条件是已确认 `goods_id`。用户问有哪些配色、有哪些款式，或需要先选定款式才能继续查规格时调用。

分页策略：`page` 从 1 开始，按 `has_more` 翻页。列表类问题可收齐全部页，或收到满足用户筛选条件即停；`has_more=false` 后不再翻页。

后续路径：只问配色/款式时输出真实列表即结束，不追加规格或价格查询。用户指定某个款式后，把 `goods_id` + 该 `style_id` 传给 `search_sku` 取规格；只问这个配色的历史价时用 `goods_style_price_trend`（只需 `style_id`）。

不适用：找商品（用搜索工具）、尺码/容量/版本（用 `search_sku`）、商品参数与热度（用 `goods_detail`）、当前渠道到手价（用 `goods_sku_price_comparision`，且必须先确认到 SKU）。

结果处理按 `index.md` 的“失败与异常处理”：`not_found` 说明该商品无款式数据，不用同参数重试；`failed` 的重试按通用规则执行，仍失败时说明未能取得款式，不用其他商品的款式补齐。
