# 万方公共 API 契约

脚本 scripts/wanfang_client.py 只访问 domains/cqccjy.json 中的 HTTPS 公共地址。字段以当前用户端前端和实时响应为准；本文件解释已确认的公共调用，不承诺后台或供应商接口。

## 1. config

    GET https://wanfang.cqccjy.cn/api/paper/wanfang/public/config

返回 ownerEmployeeId、channelCode、enabled、客服配置、paymentChannels、products。channelCode 仅用于服务端展示/路由事实，脚本读取后不回传给公共写接口。products 的执行字段包括 productCode、productName、unit、pricingMode、unitWordCount、fileType、minCount、hintMinCount、hintMaxCount、acceptTimeRequired、salePrice、priceLabel 和 supplementPayEnabled。

## 2. presign 与文件上传

    POST /api/paper/wanfang/public/upload/presign
    { fileName, productCode }

响应包含 uploadUrl、objectKey 和可选 headers。客户端必须用响应给出的 HTTPS uploadUrl 做一次 PUT，保持原 host、路径、query 和签名 header，不得把票据传到其他域名或记录到用户回答。

## 3. create 建单

    POST /api/paper/wanfang/public/order/create
    {
      title, author, productCode, fileName, objectKey,
      contentType, fileSize, acceptTime?, checkDbs?
    }

只有真实有值时才发送 acceptTime 和 checkDbs。不要传 processMode、fulfillmentMode、channelCode、externalProductId、supplier callback 或内部 owner 字段。成功返回应包含 orderNo；没有 orderNo 不能说“已下单”。

## 4. order 状态

    GET /api/paper/wanfang/public/order/{orderNo}

只对用户提供或本次创建的原订单号查询。返回可包含 productCode/productName、status/statusLabel、payStatus/payStatusLabel、payAmount、wordCount、failReason、reportUrl/reportNum 等字段；缺失字段保持 null，不猜测。

## 5. 报告下载地址

    GET /api/paper/wanfang/public/order/{orderNo}/report-download-url

只有订单已完成或服务端明确报告可用时才调用。脚本仅输出 HTTPS 地址，并始终保留本站 /pwf/check 页面；供应商临时 HTTP 地址和签名参数不对用户公开。

## 6. 未声明接口

当前域名配置没有 order/query、pay、pay/qr、settlement/card、delete 或供应商回调接口。不要自行拼接这些路径，也不要用其他品牌的 CNKI/VPCS 接口替代万方接口。支付、补差价、卡号核销由用户在原页面完成。

## 7. 输出安全

uploadUrl、签名 header、STS、objectKey、token、供应商字段、客服 secret 和文件正文只用于当前执行；统一输出会过滤这些字段。报告与订单字段按真实返回输出，不把本地快照或价格当成订单事实。
