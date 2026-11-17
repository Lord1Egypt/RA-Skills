# 支付、状态与停止条件

## 当前支付方式

2026-10-02 快照显示检测卡号、微信、支付宝均 enabled。微信当前 mobilePayMode=SCAN，支付宝当前 mobilePayMode=DIRECT。页面显示可能随配置变化，Skill 只读取并交接，不主动调用支付或卡结算。

## 状态映射

| 服务端状态 | 建议话术 | 停止/继续 |
|---|---|---|
| PENDING_UPLOAD | 等待上传 | 回同一订单页面上传 |
| WAIT_PAY/UNPAID | 已建单待支付 | 用户本人支付 |
| PAYING | 支付处理中 | 等待原订单刷新 |
| PAID/SUBMITTING | 已支付待提交 | 查询原订单 |
| DETECTING/PROCESSING | 检测中 | 等待异步完成 |
| COMPLETED/SUCCESS | 检测完成 | 打开报告页 |
| FAIL/FAILED | 处理失败 | 保留 failReason，联系客服 |

payStatus=PAID 才能说已支付；打开支付页、生成二维码或用户口头说“已付”都不是订单事实。

## 补差价

supplementPayEnabled 表示页面可能在平台解析字数高于预估时要求补款。Skill 不自动计算补款、不自动扣款、不重复创建支付单；让用户在原订单页面确认最终金额。

## 轮询

status 是幂等查询。短时间内连续查询不改变履约状态，也不能替代供应商处理。出现失败原因、服务端明确错误或报告完成后停止轮询。
