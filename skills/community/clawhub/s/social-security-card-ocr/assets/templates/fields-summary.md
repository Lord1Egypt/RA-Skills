# 各识别类型的字段说明（elements 内容）

根据 ocrType 不同，返回的 `elements` 对象包含以下字段：

## SOCIAL_SECURITY_CARD (社保卡)
- `name`: 姓名
- `gender`: 性别
- `nation`: 民族
- `bornDate`: 出生日期
- `socialSecurityNumber`: 社会保障号码
- `cardNumber`: 社会保障卡号
- `issueDate`: 发卡日期
- `bankCardNumber`: 银行卡号
- `validityPeriod`: 有效期限
- `issueInstitution`: 发卡机关
