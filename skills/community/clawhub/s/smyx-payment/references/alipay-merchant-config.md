# 支付安全配置说明

## privateKey 处理规则

- 支付宝 privateKey 不允许明文写死在代码、文档或配置中。
- 支付宝 privateKey 不允许保存到本地文件、环境变量、YAML、JSON、日志或临时文件。
- 支付宝 privateKey 只能来自云端 `create_order` 创单接口返回字段 `privateKey`。
- H5/网页支付生成签名时，只能以内存参数传入 `create_payment_with_cloud_order(..., private_key_string=...)`。
- 查询支付宝订单状态时，只能以内存参数传入 `query_alipay_trade_status(..., private_key_string=...)`。
- 旧版本地密钥文件、密钥生成脚本、独立支付脚本、后台跨进程轮询均已禁用。

## 标准链路

1. 调用云端 `create_order` 创建订单。
2. 从返回对象读取 `orderNo` 和 `privateKey`。
3. `orderNo` 作为支付宝 `out_trade_no`。
4. `privateKey` 仅在当前进程内存中用于签名。
5. 不打印、不保存、不回显 `privateKey`。
