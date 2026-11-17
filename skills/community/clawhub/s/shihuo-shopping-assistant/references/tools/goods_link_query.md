# goods_link_query

链接对应渠道的详情工具。根据电商平台商品链接、口令或分享文本返回平台、店铺、渠道规格、当前到手价、额外优惠券、普通优惠券、渠道侧历史低点和渠道购买入口，同时给出识货商品绑定信息。

与 `link_parse` 的分工：`link_parse` 只做识货三层 ID 绑定，判定链接已定位到商品层、款式层还是 SKU 层，不返回标准链接或渠道快照；本工具只返回一条渠道快照、不含 `goods_style_id`，用于取价格与优惠事实。两者按用户问题所需调用，职责互不替代。

## 入参

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| link | string | 是 | 用户给出的**完整原文**：渠道商品链接、短链、淘口令或整段分享文本。空串或纯空白返回 `input_required` |

必须传用户原话，不截断、不只截取其中的 URL、不删掉前后中文和符号。口令和分享文本的识别依赖这些上下文。无分页参数。

## 响应字段解释

`data` 为对象，只描述一条渠道商品快照。所有金额都是**未格式化文本**：可能带 `￥`，也可能是纯数字（`3600`）或带文案，展示前先判断，做差额前先剥掉符号和文案。

| 路径 | 类型 | 是否恒有 | 含义      | 展示与限制 |
| --- | --- | --- |---------| --- |
| data.mall_name | string | 否 | 渠道平台名   | 空串省略。渠道侧字段，不与识货站内热度混写 |
| data.shop_name | string | 否 | 店铺名     | 空串省略。不当作正品或资质背书 |
| data.mall_icon | string | 否 | 平台图标地址  | 不在文字回复中展示 |
| data.product_title | string | 否 | 渠道商品标题  | 外部数据。只作兜底检索的输入，不据它推断货号、配色、尺码、容量、版本、材质和正品状态 |
| data.supplier_sku_info | object | 是 | 渠道 SKU 信息 | 整块可能为空值 |
| data.supplier_sku_info.attrs | array(string) | 否 | 渠道规格文本，如颜色、尺码、容量、版本 | 唯一可用的链接侧规格来源。原样展示，不拆解、不归一化、不补维度名 |
| data.supplier_sku_info.supplier_id | string | 否 | 渠道 ID   | 不展示 |
| data.supplier_sku_info.stock | number | 否 | 渠道库存    | 只陈述当前快照，不承诺可购买 |
| data.supplier_sku_info.image | string | 否 | 渠道 SKU 图 | 不凭图片补规格、配色或版本事实 |
| data.supplier_sku_info.url | string | 否 | 渠道原始商品地址 | 展示前优先走 `link_convert`；转链不可用时可直接展示原始 `http`/`https` 地址 |
| data.current_final_price | string | 否 | 该链接当前到手价 | 链接侧到手价的唯一来源。空串表示无有效到手价 |
| data.price_before_coupon | string | 否 | 券前价     | 只与同一条快照的 `current_final_price` 做差额。空串表示无券前价，此时不算整体节省额 |
| data.extra_coupons | array | 否 | 额外优惠券列表 | `coupon_type` 为 6、74、90、91、94、95 的券；空数组表示无此类券 |
| data.extra_coupons[].name | string | 否 | 券名 | 工具已按券名与券描述生成，原样展示 |
| data.extra_coupons[].link | string | 否 | 券链接 | 来自券搜索接口的 `coupon_url`，展示前逐张独立调 `link_convert(type="coupon")`；转链不可用时保留原始 `http`/`https` 地址 |
| data.coupons | array | 否 | 普通优惠券列表 | 其他 `coupon_type` 的券；空数组表示无此类券 |
| data.coupons[].name | string | 否 | 券名 | 工具已按券名与券描述生成，原样展示 |
| data.coupons[].link | string | 否 | 券链接 | 来自券搜索接口的 `coupon_url`，展示前逐张独立调 `link_convert(type="coupon")`；转链不可用时保留原始 `http`/`https` 地址 |
| data.history_low_price | string | 否 | 渠道侧近 180 天历史低点 | 固定称“该链接渠道近 180 天最低价”。不是识货 SKU 层历史低点，不是全网历史最低。空串表示该渠道没返回历史低点，不用当前到手价顶替 |
| data.price_trends | array | 否 | 渠道侧历史价格点 | 与 `history_low_price` 同口径 |
| data.price_trends[].timestamp | string | 否 | 价格点时间戳，秒级字符串 | 展示前转成日期 |
| data.price_trends[].price | string | 否 | 该时间点价格  | 同金额格式约定 |
| data.promotion_price | string | 否 | 活动价     | 有值才展示，且要说明是活动价不是当前到手价。是渠道促销，不改写成隐藏券或识货补贴 |
| data.promotion_name | string | 否 | 活动名     | 原样展示，不改写成保证、承诺、隐藏券或识货补贴 |
| data.promotion_time | number | 否 | 活动时间戳   | 0 或缺失时省略 |
| data.supplier_buy_link | string | 否 | 渠道购买入口  | 展示前优先调 `link_convert(type="goods")`；转链不可用时直接展示原始 `http`/`https` 地址 |
| data.sh_goods_id | string | 否 | 绑定的识货商品 ID | 不透明字符串，固定 12 字符、区分大小写；非空才算绑定，仅用于工具调用 |
| data.sh_sku_id | string | 否 | 绑定的识货 SKU ID | 不透明字符串，固定 12 字符、区分大小写；非空才算绑定，传价格工具时参数名写 `sku_id` |
| data.sh_goods_name | string | 否 | 识货商品名   | 可展示 |
| data.sh_min_price | string | 否 | 识货站内最低展示价 | 识货侧价格，固定称“识货站内展示价”，不得当作渠道到手价或最低价。空串表示识货侧没返回展示价 |

本工具不返回 `goods_style_id`、货号和识货站内 `href`。需要款式层或货号走 `goods_styles`、`goods_detail`；需要识货商品入口用 `goods_styles` 返回的识货 `href`。

## 优惠能不能展示

`extra_coupons[]`、`coupons[]`、`promotion_*` 三块字段各自独立，判定口径不同。两组券都来自本轮券搜索结果：`coupon_type` 为 6、74、90、91、94、95 时进入 `extra_coupons[]`，其余进入 `coupons[]`。可展示为“可领取优惠”的必须同时满足三条，缺一即不算：

1. 来自本轮真实返回的字段，不从标题、活动文案或记忆补齐。
2. 对应本轮已确认的那一个规格，即 `supplier_sku_info.attrs[]` 指向的规格。
3. 券链接有最终展示地址：优先取 `link_convert(type="coupon")` 的有效结果，转链不可用时取该券原始 `http`/`https` 地址；两者都不可展示时只保留券名事实，不声称存在可用领取入口。

券对象不返回面额，不从券名或描述中解析金额。当前到手价只取 `current_final_price`，不再扣除任何券金额；需要表达相对券前价的整体节省额时，只能用同一快照中可解析的 `price_before_coupon - current_final_price`，不得把差额归因或拆分到某一张券，也不得声称多张券可叠加。

不算当前规格可领取优惠的情况：通用活动、跨店满减、平台券中心的品类券、其他规格的券、`promotion_*` 这类渠道促销。它们只能按渠道促销原样陈述。

不承诺优惠一定可领、一定可用、一定可叠加。用户换规格后所有优惠字段重新核对，不沿用上一轮结论。

返回 `partial_success` 且 issue 表示优惠券查询失败时，平台、店铺、价格和历史信息仍可使用，但 `extra_coupons[]`、`coupons[]` 不能用于得出“无券”结论，应说明券信息暂未取全。

## 两个历史低点不能混用

| 来源 | 口径 | 表述 |
| --- | --- | --- |
| `goods_link_query.history_low_price` | 该渠道链接近 180 天 | “该链接渠道近 180 天最低价” |
| `goods_sku_price_trend` | 识货同一 SKU 的历史价格 | “识货同一规格历史低点” |

两者实体和时间窗都不同，不做差额、不取更低值当结论、不互相替代。同时展示时必须各自标注来源。

## 与其他工具的关系

| 目标 | 用哪个 |
| --- | --- |
| 判断链接落在商品层、款式层还是 SKU 层 | `link_parse` |
| 取链接当前到手价、额外优惠券、普通优惠券、渠道入口 | 本工具 |
| 取同规格其他渠道报价 | `goods_sku_price_comparision`（需 `goods_id` + `sku_id`） |
| 取识货同一 SKU 历史价 | `goods_sku_price_trend` |
| 取货号、配色、款式、识货商品入口 | `goods_detail`、`goods_styles` |

## 调用说明

前置条件是用户消息里出现渠道商品链接、口令或分享文本，且问题需要该链接的价格、优惠或渠道事实。需要继续做同规格全网比价时，核对真实商品与 SKU 绑定，必要时配合 `link_parse`、`goods_styles`、`search_sku` 补齐定位，再调用 `goods_sku_price_comparision`，结果按所在场景 `output.md` 的模块骨架展示。

不适用：识货站内关键词或图片搜索、识货商品详情与 SKU 查询、下单加购订单类请求。本工具不校验链接是否仍然有效、不承诺库存与可购买状态。

结果处理按 `index.md` 的“通用响应约定”：`input_required` 说明没传到有效 `link`，补齐原文重试；`not_found` 表示这条链接无法解析成渠道商品（含被屏蔽域名、二手平台链接），说明未能取得渠道信息，不把链接标题或渠道商品名当作识货实体，也不用同参数反复重试。
