# 各识别类型的字段说明（elements 内容）

根据 ocrType 不同，返回的 `elements` 对象包含以下字段：

## TRAIN_TICKET (火车票)
- `title`: 标题
- `ticketNo`: 车票编号
- `departStation`: 起始站
- `destinationStation`: 终止站
- `trainNo`: 车次
- `departDate`: 发车日期
- `departTime`: 发车时间
- `seatPostion`: 座位号
- `seatNo`: 座次
- `ticketPrice`: 票价
- `passengerName`: 旅客姓名
- `identifyId`: 身份证号
- `invoiceNo`: 发票号码
- `invoiceDate`: 开票日期
- `preTaxAmount`: 税前金额
- `taxRate`: 税率
- `taxAmount`: 税额
- `elecTicketNo`: 电子客票号
- `originInvoiceNo`: 原发票号码
- `buyerName`: 购买方名称
- `socialCreditCode`: 统一社会信用代码
- `refundTag`: 退票标识
- `replaceTag`: 换开标识
- `otherInfo`: 其他信息

