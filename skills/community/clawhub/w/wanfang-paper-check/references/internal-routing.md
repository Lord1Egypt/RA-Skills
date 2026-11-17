# 内部履约与供应商边界

公共用户端背后可能按时间窗、余额、产品、供应商可用性和人工队列选择 AUTO 或 MANUAL 路由。以上属于平台内部实现，不是用户可配置项。

## 公共请求禁止字段

不要向 public config/presign/create/order 请求传递 processMode、fulfillmentMode、channelCode、externalProductId、supplierCode、supplier callback、人工操作人或内部 owner 字段。externalProductId 只在公共目录中作为展示事实存在，不用于替代 productCode。

## 对用户的统一表现

无论内部走自动渠道还是平台人工，用户只看到待提交、检测中、完成或失败，以及可操作的原订单页面。不要暴露供应商名称、余额、人工下载/上传动作、回调 URL、内部时区窗口或路由切换。

## 失败归因

公共接口失败时按服务端 status/failReason 解释；不能通过修改内部字段“强行切供应商”，也不能伪造一个完成状态。若平台要求客服介入，保留 orderNo 并交给官方支持。
