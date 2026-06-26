# 各识别类型的字段说明（elements 内容）

根据 ocrType 不同，返回的 `elements` 对象包含以下字段：

## TELEGRAPHIC_TRANSFER_VOUCHER (电汇凭证)
- `title`: 标题
- `currency`: 币别
- `fillDate`: 填单日期
- `voucherNo`: 凭证编号
- `remitterName`: 汇款人名称
- `remitterAccount`: 汇款人账号
- `remitterBank`: 汇款人汇出行名称
- `payeeName`: 收款人名称
- `payeeAccount`: 收款人账号
- `payeeBank`: 收款人汇入行名称
- `amountUpper`: 大写金额
- `amountLower`: 小写金额
- `password`: 支付密码
- `usage`: 附加信息及用途