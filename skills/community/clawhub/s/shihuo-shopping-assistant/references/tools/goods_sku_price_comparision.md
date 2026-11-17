# goods_sku_price_comparision

商品 SKU 全网比价工具。识货将同款商品按配色 / 规格聚合到商品 SKU，再返回该 SKU 对应的各渠道 SKU 报价；不同商品、配色或规格的报价不能混在一起比较。前置是确认商品、配色 / 规格及唯一 SKU，信息已充分时直接查询，不固定追问。

## 入参

`goods_id` 与 `sku_id` 均为不透明字符串，固定 12 字符、区分大小写，必须原样使用工具返回的 ID；不要从链接提取数字或自行构造。无效或已失效的 ID 会返回 `input_required` + `invalid_id`，须重新调用搜索工具获取，不得用同值重试。

`page` 为整数，从 1 开始，缺省按 1。

## 响应字段解释

`data.list[]` 每一项是一条渠道 SKU 报价，属渠道侧真实交易层。所有金额和运费都是**未格式化文本**：可能带 `￥`，也可能是纯数字（`99`）或带文案，展示前先判断，做差额前先剥掉符号和文案。

| 路径 | 类型 | 是否恒有 | 含义 | 展示与限制 |
| --- | --- | --- | --- | --- |
| data.list[].mall_name | string | 否 | 渠道平台名 | 空串省略。渠道侧字段，不能与识货热度混写 |
| data.list[].shop_name | string | 否 | 店铺名 | 空串省略。不当作正品或资质背书 |
| data.list[].mall_icon | string | 否 | 平台图标地址 | 不在文字回复中展示 |
| data.list[].goods_title | string | 否 | 渠道商品标题 | 外部数据，只用于校验是否仍是同一 SKU，不据它推断货号、材质、产地或正品状态 |
| data.list[].spec_name | string | 否 | 渠道规格文本 | 校验是否仍是同一 SKU。原样展示，不拆解、不归一化 |
| data.list[].sku_image | string | 否 | 渠道 SKU 图 | 不凭图片补规格、配色或版本事实 |
| data.list[].final_price | string | 否 | 该报价的渠道到手价 | 渠道 SKU 层价格，不是识货展示价、不是历史价。空串或剥掉符号后解析不出正数即无效报价 |
| data.list[].original_price | string | 否 | 该报价的渠道原价 | 渠道 SKU 层价格。只与同一条报价的 `final_price` 同时出现，不与其他报价或其他层价格相减 |
| data.list[].freight | string | 否 | 运费 | 渠道 SKU 层金额，原样文本。空串表示本条报价没返回运费，不等于包邮，也不并入到手价 |
| data.list[].fulfillment[] | array(string) | 否 | 履约标签 | 空数组表示无标签。不承诺一定发货或售后 |
| data.list[].coupon[] | array | 否 | 该报价上的优惠券或活动 | 空数组表示本条报价没返回券。逐 offer 独立判定，见下方“优惠能不能展示” |
| data.list[].coupon[].coupon_name | string | 否 | 券名 | 原样展示，不改写 |
| data.list[].coupon[].coupon_amount | string | 否 | 券面额 | 渠道 SKU 层金额，原样文本。空串表示渠道没返回面额，此时不从券名解析金额 |
| data.list[].coupon[].start_fee | string | 否 | 使用门槛文案 | 原样展示。空串表示渠道没返回门槛，不写成无门槛 |
| data.list[].coupon[].coupon_valid_start_time | string | 否 | 券有效期开始 | 取的是该条报价的活动起止时间，同一条报价下所有券共用同一组时间，不代表单张券的独立有效期。空串省略 |
| data.list[].coupon[].coupon_valid_end_time | string | 否 | 券有效期结束 | 同上 |
| data.list[].coupon[].coupon_href | string | 否 | 券链接 | 空串表示无领取入口。展示前逐张独立调 `link_convert(type="coupon")`；转链不可用时保留原始 `http`/`https` 地址 |
| data.list[].buy_link | string | 否 | 购买入口候选 | 先送 `link_convert(type="goods")`；转链不可用时直接展示原始 `http`/`https` 地址 |
| data.list[].sh_recommend_reason | string | 是 | 渠道给这条报价打的推荐标记文案 | 恒有该键，空串即该报价没有推荐标记。非空时只按渠道原文展示，不扩展为商品、质量或适配结论 |
| data.list[].endorse[] | array(string) | 否 | 渠道信任背书信息 | 包含店铺热度、信誉、官旗等上游标签；空数组或缺失表示没有背书信息。保留原文或忠实归纳，不补充标签外的信息，不扩展为正品、质量或适配保证 |
| data.total | number | 是 | 报价总数 | 按 ceil(total/pageSize) 判断页数 |
| data.pageSize | number | 是 | 页大小 | page 从 1 开始 |

“有效报价”的判据是 `final_price` 剥掉货币符号和文案后能解析成正数；解析不出就不进最低价判断或价差计算，也不作为有效价格展示。最低价只在同一个 `sku_id` 的有效报价之间判断。

## 报价怎么进输出

本轮报价按当前场景 `output.md` 的渠道表模块展示，列、顺序和删除规则以该文件为准，本文件只定字段口径。

| 输出所需内容 | 本轮数据来源 |
| --- | --- |
| 商品与完整配色 / 规格 | 已确认的商品信息、款式名称与 SKU `specs`，并用本工具 `goods_title`、`spec_name` 核对报价 |
| 渠道 / 店铺 | `mall_name`、`shop_name` |
| 当前到手价与对应原价 | 同一条报价的 `final_price`、`original_price` |
| 运费、履约条件与渠道标签 | 同一条报价的 `freight`、`fulfillment`、`sh_recommend_reason`、`endorse` |
| 相关优惠及领取入口 | 核验后的该报价 `coupon[]`，券链接逐张独立转链 |
| 购买入口 | 该报价 `buy_link` 的最终展示地址，逐 offer 独立转链 |

`mall_icon` 和 `sku_image` 是图片地址，不在文字回复里展示。仅使用实际有值的数据；无可用报价时按场景的兜底分支说明未查到，不编造报价或购买入口。

## 优惠能不能展示

`coupon[]` 逐 offer 独立，判定口径与其他 offer 不共享。可展示为“可领取优惠”的必须同时满足三条，缺一即不算：

1. 来自本轮真实返回的字段，不从渠道标题或记忆补齐。
2. 对应本轮已确认的那一个 `sku_id`，且该 offer 的 `spec_name` 仍是同一规格。
3. 该报价的 `final_price` 有效，且券有最终可展示的真实领取入口。到手价只取 `final_price`，不从券面额推算或再次扣减。

不算当前规格可领取优惠的情况：通用活动、跨店满减、平台券中心的品类券、其他 offer 或其他规格的券。多张券不相加、不合成总额、不假定可叠加。

不承诺优惠一定可领、一定可用、一定可叠加。用户换规格后重新调用并重新核对，不沿用上一轮结论。

## 隐藏优惠识别

只有 `coupon[].coupon_name` 原文明确包含以下任一标识，才可识别为隐藏优惠；识别时忽略英文字母大小写和中间空格：

- `识货补贴`
- `88VIP` 或 `88 VIP`（大小写与空格不影响识别）
- `京东PLUS`、`京东 PLUS` 或 `京东Plus`

平台名、店铺活动名和模型记忆不能单独证明上述券种。仅在与用户问题相关时于比价卡片或回答中呈现，并保留原始券名。隐藏优惠只使用已核验同一规格、`final_price` 有效且有最终展示地址的报价；优惠券链接优先使用转链地址，转链不可用时使用原始 `http`/`https` 地址，但不写成一定可领取的承诺。

每张券保留与原报价的对应关系，不把不同商品入口或不同 `final_price` 的券混用，不相加、不假定可叠加。`coupon_amount` 展示为券面额/优惠金额，不从券名解析金额，也不从 `final_price` 再扣一遍。只有同一报价的 `original_price` 与 `final_price` 都能解析时，才可写该报价原价差额；该差额不归因到某张券。

隐藏优惠渠道之间可以按当前有效 `final_price` 排序并计算价差。`goods_sku_price_trend` 的历史低点与当前渠道到手价属于不同时间与口径，按需引用时须标明价格类型和来源，不得计算“券后价较历史低点”的高低或差额。

## 调用说明

前置是 `goods_id` + `sku_id`，只在已确认 SKU 且需要渠道、到手价、哪里买或购买入口时调用。全量比价按 `total`/`pageSize` 翻页收齐报价；未取全时不声称已比较全部渠道。每个 offer 先过滤规格和有效 `final_price`，需要展示入口时把 `buy_link` 独立传给 `link_convert(type="goods")`，券链接另传 `type="coupon"`；转链不可用时回退到该 offer 或该券自身的原始 `http`/`https` 地址。转链地址和原始地址都不可展示的 offer 仅可保留价格事实，不进可购买报价或最低可买价判断。使用指定卡片展示已核验的比价结果；无报价时按 `not_found` 说明未找到，不用展示价或历史低点补齐。
