# search_sku

款式下的 SKU 列表。按 `goods_id` + `style_id` 一次返回该款式下全部 SKU，含完整规格组成、SKU 展示价和 30 日销量；用于将已确认配色 / 规格匹配到商品 SKU。链接工具也可直接提供真实 SKU ID。

## 入参

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| goods_id | string | 是 | 识货商品 ID，不透明字符串，固定 12 字符、区分大小写，原样取自工具返回值 |
| style_id | string | 是 | 款式/配色 ID，不透明字符串，固定 12 字符、区分大小写，原样取自工具返回值，来自 `goods_styles.styles[].style_id` 或 `link_parse.results[].goods_style_id` |

两个都必填，缺任一个返回 `input_required` + `missing_param`；无效或已失效 ID 返回 `input_required` + `invalid_id`，须重新调用搜索工具获取，不得用同值重试。无分页参数，一次返回全部 SKU。

## 响应字段解释

| 路径 | 类型 | 是否恒有 | 含义 | 展示与限制 |
| --- | --- | --- | --- | --- |
| data.goods_id | string | 是 | 回显的商品 ID，不透明字符串，固定 12 字符、区分大小写 | 与请求核对 |
| data.style_id | string | 是 | 回显的款式 ID，不透明字符串，固定 12 字符、区分大小写 | 与请求核对，确认规格属于用户选的配色 |
| data.skus | array | 是 | SKU 列表 | 可能为空数组，表示该款式下无可用 SKU |
| data.skus[].goods_sku_id | string | 是 | SKU ID，不透明字符串，固定 12 字符、区分大小写 | 传给 `goods_sku_price_trend` 和 `goods_sku_price_comparision` 时，**参数名必须写 `sku_id`** |
| data.skus[].specs | array | 否 | 规格维度列表 | 整块可能缺失。维度名和取值都不固定，以返回值为准，不假定一定有“尺码” |
| data.skus[].specs[].name | string | 是 | 规格维度名，如“尺码”“容量”“版本” | 原样展示 |
| data.skus[].specs[].values | array(string) | 是 | 该维度取值 | 匹配用户指定规格的实际含义与完整组合，见下方匹配规则 |
| data.skus[].sale_price | string | 否 | SKU 券后/售卖展示价，格式 `￥550` | 空串时省略。固定称“SKU 展示价”，不是渠道到手价 |
| data.skus[].origin_price | string | 否 | SKU 原价 | 同上格式。只与同一 SKU 的 `sale_price` 做同口径差额 |
| data.skus[].sales_30_days | number | 否 | 近 30 日销量 | 缺失或 0 时省略。只作 SKU 信息陈述，不改写成排名，不当作质量或适配证据 |
| data.skus[].image_url | string | 否 | SKU 图 | 不凭图片补规格、颜色或版本事实 |

`SKUCard` 只有以上 6 个字段，没有库存、发货地、渠道或链接字段。

## 规格匹配规则

1. 用户明确说了规格（如“42 码”“512G”）时，只保留 `specs[].values` 的实际含义和完整规格组合均匹配的 SKU。可识别“42 码”与尺码维度下“42”这类清晰等价写法，不要求字面逐字一致；近似值（41.5 与 42、256G 与 512G）及不同版本一律不算匹配，不擅自换规格。
2. 精确匹配为空时不替换、不就近取值，说明未找到指定规格，并按需提供真实可选值；只有用户选择了其它规格才继续查询该规格。
3. 精确匹配唯一时直接收口到该 SKU，可继续调用 SKU 趋势或比价。
4. 信息足够时结合已有条件与真实结果直接匹配；用户要帮选或允许参考规格时，可根据需求选择并说明完整参考规格；只有无法依据现有条件确定、且会影响结论的歧义才展示真实选项并追问，不设固定排序选择规则。只问可选规格时直接回答规格，无需先选定 SKU。
5. 确认 SKU 时核对全部规格维度，不仅匹配单个尺码或容量；继续查询历史或全网比价时使用同一个已确认的 SKU，不跨规格复用数据。

## 调用说明

前置条件是已确认 `goods_id` + `style_id`。用户问某个配色有哪些尺码/容量/版本，或需要收口到唯一 SKU 才能继续查价时调用。

不适用：找商品（用搜索工具）、配色列表（用 `goods_styles`）、商品参数与热度（用 `goods_detail`）、当前渠道价（用 `goods_sku_price_comparision`）、历史价（用趋势工具）。本工具的 `sale_price` 不作到手价回答“多少钱能买到”。

链接直达 SKU 时：`link_parse` 已给出 `goods_id` + `goods_sku_id` 可直接调 SKU 价格工具，不为了凑 `style_id` 猜测款式，按 `index.md` 的“ID 使用约定”处理。

结果处理按 `index.md` 的“失败与异常处理”：`not_found` 或空 `skus` 说明该款式无 SKU，改为确认款式或商品，不用同参数重试；`failed` 最多重试一次，仍失败时保留已确认的商品和款式信息进入兜底。
