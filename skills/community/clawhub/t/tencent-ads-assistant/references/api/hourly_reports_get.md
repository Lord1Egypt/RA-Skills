# hourly_reports/get — 小时粒度报表

## 功能说明

获取**指定某一天**的腾讯广告账户小时粒度报表数据，适合分析当天或指定日期的小时级别数据波动。

## 适用场景

- 分析当天各小时的消耗变化趋势
- 查看指定日期小时粒度的投放效果
- 按小时粒度分析广告/创意的表现
- 对比不同时段的投放效果

## 请求参数 Schema

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `date` | string | ✅ | 查询日期，格式：`yyyy-MM-dd`，最小值为一年前的今天 |
| `group_by_type` | string | ✅ | 聚合维度（每次仅支持一个），可选值见下表 |
| `fields` | list | ✅ | 要获取的指标列表（可多个），可选值见下表 |
| `page_size` | number | ✅ | 返回数据条数上限，最大 100 |
| `account_id_list` | list[number] | ✅ | 账户 ID 列表，最多 100 个。用户未指定时需先通过 Chat 模式 `DATA_QUERY` 查询用户账户列表后填入 |
| `adgroup_id` | number | 否 | 指定广告 ID，查询单个广告的报表时传 |
| `order_by` | object | 否 | 排序配置，含 `field`（排序字段，默认 cost）和 `type`（`DESC` 降序 / `ASC` 升序） |

### group_by_type 可选值

| 值 | 说明 |
|----|------|
| `SUM` | 汇总加和 |
| `HOUR` | 按小时 |
| `ACCOUNT_ID` | 按账户 ID |
| `ADGROUP_ID` | 按广告 ID |
| `ADGROUP_ID_AND_HOUR` | 按广告 ID + 小时 |
| `CREATIVE_ID` | 按创意 ID |
| `CREATIVE_ID_AND_HOUR` | 按创意 ID + 小时 |

### fields 可选值

以下为**常用高频指标**，按场景分类列出：

#### 基础效果指标

| 值 | 说明 |
|----|------|
| `hour` | 小时 |
| `account_id` | 账号ID |
| `cost` | 花费/消耗费用（元） |
| `view_count` | 曝光次数 |
| `view_user_count` | 曝光人数 |
| `valid_click_count` | 点击次数 |
| `click_user_count` | 点击人数 |
| `ctr` | 点击率 |
| `cpc` | 点击均价 |
| `thousand_display_price` | 千次展现均价（CPM） |
| `valuable_click_count` | 可转化点击次数 |
| `valuable_click_cost` | 可转化点击成本 |
| `valuable_click_rate` | 可转化点击率 |
| `acquisition_cost` | 一键起量消耗 |
| `conversions_count` | 目标转化量 |
| `conversions_rate` | 目标转化率 |
| `conversions_cost` | 目标转化成本（元） |
| `deep_conversions_count` | 深度目标转化量 |
| `deep_conversions_rate` | 深度目标转化率 |
| `deep_conversions_cost` | 深度转化成本 |

#### 落地页相关

| 值 | 说明 |
|----|------|
| `platform_page_view_count` | 落地页曝光次数 |
| `platform_page_view_rate` | 落地页曝光率 |
| `lan_button_click_count` | 落地页组件点击次数 |
| `lan_button_click_cost` | 落地页点击成本 |
| `key_page_view_count` | 关键页面访问次数 |
| `key_page_view_cost` | 关键页面访问成本 |

#### 下单/付费核心指标

| 值 | 说明 |
|----|------|
| `order_pv` | 下单次数 |
| `order_amount` | 下单金额 |
| `order_cost` | 下单成本 |
| `order_roi` | 下单ROI |
| `order_rate` | 下单率 |
| `purchase_pv` | 付费次数 |
| `purchase_amount` | 付费金额 |
| `purchase_cost` | 付费成本 |
| `purchase_roi` | 付费ROI |
| `purchase_clk_rate` | 付费率 |

#### 线索/咨询类

| 值 | 说明 |
|----|------|
| `page_consult_count` | 在线咨询次数 |
| `page_consult_cost` | 在线咨询成本 |
| `page_reservation_count` | 表单预约次数 |
| `page_reservation_cost` | 表单预约成本 |
| `page_phone_call_direct_count` | 电话直拨次数 |
| `page_phone_call_direct_cost` | 电话直拨成本 |
| `overall_leads_purchase_count` | 综合销售线索人数 |
| `effective_leads_count` | 有效线索次数 |
| `effective_cost` | 有效线索成本 |

#### 加粉/企微

| 值 | 说明 |
|----|------|
| `scan_follow_user_count` | 加企业微信客服人数 |
| `scan_follow_user_cost` | 加企业微信客服成本 |
| `scan_follow_user_rate` | 加企业微信客服率 |
| `from_follow_uv` | 公众号关注人数 |
| `from_follow_cost` | 公众号关注成本 |

#### APP下载/激活/注册

| 值 | 说明 |
|----|------|
| `download_count` | APP下载完成次数 |
| `download_cost` | APP下载成本 |
| `activated_count` | APP激活次数 |
| `activated_cost` | APP激活成本 |
| `reg_pv` | 注册次数 |
| `reg_cost` | 注册次数成本 |
| `retention_count` | 次日留存次数 |
| `retention_cost` | 次日留存成本 |

#### 视频播放指标

| 值 | 说明 |
|----|------|
| `video_outer_play_count` | 视频有效播放次数 |
| `video_outer_play_cost` | 有效播放成本 |
| `video_outer_play_rate` | 有效播放率 |
| `video_outer_play_time_count` | 平均有效播放时长 |
| `video_outer_play100_count` | 100%进度播放次数 |
| `video_outer_play3s_count` | 3s播放完成次数 |

#### 互动指标

| 值 | 说明 |
|----|------|
| `praise_count` | 点赞次数 |
| `forward_count` | 分享次数 |
| `comment_count` | 评论次数 |
| `read_count` | 阅读次数 |

#### 综合归因付费（高频使用）

| 值 | 说明 |
|----|------|
| `first_day_pay_count` | 综合归因首日付费次数 |
| `first_day_pay_amount` | 综合归因首日付费金额 |
| `roi_activated_d1` | 综合归因首日付费ROI |
| `purchase_pla_active_1d_roi` | 综合归因首日付费ROI（平台上报，优先推荐） |
| `roi_activated_d7` | 综合归因7日付费ROI |
| `purchase_pla_active_7d_roi` | 综合归因7日付费ROI（平台上报，优先推荐） |

#### 视频号直播

| 值 | 说明 |
|----|------|
| `video_live_exp_count` | 视频号直播观看次数 |
| `live_stream_exp_uv` | 视频号直播观看人数 |
| `video_follow_count` | 视频号关注人数 |
| `video_live_cick_commodity_count` | 视频号直播商品点击次数 |

> 以上为常用高频指标，接口支持的**全量指标共 867 个**（还涵盖曝光归因/点击归因、多日窗口期ROI、广告变现、混合变现、回流、搜一搜品专等更多细分场景指标）。完整字段列表请查阅 [`references/api/report_fields.md`](./report_fields.md)。

## 示例

**查询今天各小时的消耗趋势：**

```bash
node scripts/api_tool_call.js '{"method":"GET","path":"hourly_reports/get","params":{"date":"2025-04-08","group_by_type":"HOUR","fields":["cost","hour","valid_click_count"],"page_size":24,"account_id_list":[2345678]}}'
```

**查询指定日期某广告的小时粒度数据：**

```bash
node scripts/api_tool_call.js '{"method":"GET","path":"hourly_reports/get","params":{"date":"2025-04-08","group_by_type":"ADGROUP_ID_AND_HOUR","fields":["cost","hour"],"page_size":24,"adgroup_id":123456,"account_id_list":[2345678]}}'
```

## 注意事项

- 仅查询单天数据，`date` 参数为必填
- 当天数据为实时数据，可能尚未完整
- 如需跨天数据，请使用 `daily_reports/get`
