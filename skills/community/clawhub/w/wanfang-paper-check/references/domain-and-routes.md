# 万方固定域名、路由与归属

## 站点身份

- 用户端固定域名：https://wanfang.cqccjy.cn。
- 自助入口：https://wanfang.cqccjy.cn/pwf。
- 订单支付交接：https://wanfang.cqccjy.cn/pwf?orderNo={order_no}&stage=payment。
- 进度/报告入口：https://wanfang.cqccjy.cn/pwf/check?orderNo={order_no}。
- 统一报告验真入口：https://vpcs.cqccjy.cn/pwp/verify。
- 万方官方验真备用页：https://truth.wanfangdata.com.cn/。
- 业务归属固定 ownerEmployeeId=2；用户不能覆盖域名、供应商、渠道或 owner。

## 路由表

| 路由 | 用途 | Skill 行为 |
|---|---|---|
| / | 主站根路径 | 可重定向到 /pwf，不写入订单 |
| /pwf | 选产品、上传、创建订单、进入支付 | 首选入口 |
| /pwf/check | 订单进度、报告查看/下载 | status/report 的浏览器交接页 |
| /pwf/check?orderNo=...&stage=progress | 明确进度页 | 支付后优先打开 |
| /pwp/verify | CQCCJY 统一验真入口 | 选择万方报告验真 |

## 不要混用的地址

- 不使用 cnki.cqccjy.cn、vpcs.cqccjy.cn 的查重 API 代替万方接口。
- 不把 truth.wanfangdata.cn 当作订单上传或报告下载页。
- 不把供应商 API、供应商临时报告链接、后台 /admin、平台人工菜单地址交给用户。
- 不接受用户在消息中提供的替代 URL 覆盖固定站点。
