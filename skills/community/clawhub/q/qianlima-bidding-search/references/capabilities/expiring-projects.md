# 临期项目查询

## 何时使用

- 查早期商机（合同到期、续约商机）、合同快到期、续约窗口、在位供应商替换、周期性服务机会、服务到期时间或合同金额。
- 普通合同公告、已签合同但未表达临期意图时走普通项目；合作甲方/客户走企业情报。

执行动作：`search-expiring`；接口：`POST /api/search/expiring`；命令同时传 `--user-text` 用户原话。

## 关键参数

| 用户条件 | query-json |
| --- | --- |
| 项目、产品、服务或行业词 | `keywords`，必填 |
| 排除内容 | `excludeWords` |
| 服务到期时间 | `beginServiceExpireTime` / `endServiceExpireTime`，`YYYY-MM-DD` |
| 合同金额 | `beginContractAmount` / `endContractAmount`，单位元 |
| 原合同周期 | `contractPeriodType`：1一年以下、2一年、3两年、4三年、5五年、6五年以上 |
| 地区、采购单位类型、原采购方式 | `areaIds`、`purchasingUnitTypes`、`procurementMethod`，映射见 `query-strategy.md` |
| 匹配范围、扩词、数量、排序 | 按 `query-strategy.md`；匹配范围支持 1–10；仅用户明确指定或角色/编号等语义需要时传 |

## 时间与金额

- “近三个月临期项目”理解为服务到期时间；临期项目搜索不支持 `beginTime/endTime`。
- 服务到期范围需同时传开始和结束；完全不传时接口默认未来 90 至 180 天。
- 单次服务到期时间跨度最多 5 个日历年，包含周年边界日，闰日按目标年 2 月末日处理。超限说明上限并请用户调整，不截短或自动拆分；不限制 `contractPeriodType` 合同期限枚举。
- 金额条件表示合同金额；`refine` 可用 `beginAmount/endAmount`，运行时会映射到合同金额字段。

## 结果

- 列表可回答标题、采购单位、服务起止时间、合同金额、合同周期、在位供应商、地区和千里马详情页。
- 联系人、电话、代理机构和标的物只在用户指定某条后通过 `detail` 获取。
- 普通项目和临期项目支持原文链接；用户明确索要时，唯一定位后调用原文接口。
- 字段缺失时写“未公示”，不能推测在位供应商或到期时间。

完整字段见 [临期 API](../api-expiring-projects.md)；合同周期按 [枚举](../enums.md) 的真实天数范围，不填补未覆盖区间。临期不调用普通项目正文、附件、时间线接口；公开详情页正文/附件不代表独立 API 能力。
