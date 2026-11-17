# link_convert

转链工具。把第三方商品链接或优惠券链接转成识货可跟单的地址。展示第三方链接前优先调用，不查商品、不查价格。

## 入参

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| type | string | 是 | 枚举，只能是 `goods` 或 `coupon`。商品入口传 `goods`，优惠券入口传 `coupon`；其他值非法 |
| link | string | 是 | 待转链的原始第三方 `http`/`https` 地址。非 `http`/`https`（含 `shihuo://`）不要传 |

一次调用只处理一个链接。**每个 offer 的商品入口、每张券的券链接都各自独立调用**，不把一次转链结果套用到其他 offer 或其他券。

## 响应字段解释

| 路径 | 类型 | 是否恒有 | 含义 | 展示与限制 |
| --- | --- | --- | --- | --- |
| data.link | string | 是 | 转链后的地址 | 非空且以 `http://` 或 `https://` 开头时优先展示；空串或非法值视为转链失败，改用本次入参中的原始 `http`/`https` 地址 |

每次调用都生成一个最终展示地址：`data.link` 有效时取 `data.link`；否则，入参 `link` 本身是完整的 `http`/`https` 地址时取入参 `link`；两者都无效时不展示。不要对转链地址或原始地址做拼接、改写、删参或补参，不展示 `shihuo://`。

## 什么时候调用

| 链接来源 | 是否需要转链 |
| --- | --- |
| `goods_sku_price_comparision.list[].buy_link` | 需要，`type=goods`，逐 offer 独立调用 |
| `goods_sku_price_comparision.list[].coupon[].coupon_href` | 需要，`type=coupon`，逐券独立调用 |
| `goods_link_query.extra_coupons[].link` | 需要，`type=coupon`，逐券独立调用 |
| `goods_link_query.coupons[].link` | 需要，`type=coupon`，逐券独立调用 |
| `href`（识货站内入口，`https://m.shihuo.` 开头） | 不需要，直接展示 |
| 任何 `shihuo://` 开头的原始值 | 不传、不展示，改用对应的 `buy_link` 或 `supplier_buy_link` |

只在**已经决定要展示**某个第三方链接时才调用，不预先给所有候选批量转链。

## 失败处理

转链失败有三种：调用返回非成功状态、`data.link` 为空串、`data.link` 不是 `http`/`https` 地址。三种统一处理：

1. 入参 `link` 是完整的 `http`/`https` 地址时，直接把它作为最终展示地址；`shihuo://` 或其他非网页地址不回退展示。
2. 商品入口回退成功后，该报价照常进入渠道表和最低可买价判断；转链失败本身不构成报价不可展示的条件。
3. 券入口回退成功后，券名可链接到原始券地址，但仍不承诺一定可领、可用或可叠加。
4. 只有转链地址和原始地址都不可展示时，才省略这个入口；商品报价保留价格事实但不作为可购买报价，券保留来源工具真实返回的文本字段。
5. 同一参数不反复重试，也不把一次调用的转链结果或原始地址套给其他 offer 或其他券。

## 调用说明

前置条件是已有一个原始第三方 `http`/`https` 链接，且当前回复确实要展示它。

不适用：识货站内链接（直接展示）、非 `http`/`https` 链接、把链接解析成识货 ID（用 `link_parse`）、下单加购订单类请求。本工具不校验链接是否仍然有效、不返回价格、不代表库存或可购买状态。

`type` 不是 `goods` 或 `coupon` 时修正后重试。只要本次入参 `link` 是完整的 `http`/`https` 地址，`input_required`、`not_found`、`failed`、空结果或非法 `data.link` 都按上面的回退规则直接使用原始地址，不用同参数反复重试；原始地址本身也不可展示时才省略入口。
