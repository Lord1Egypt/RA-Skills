# 越南发票字段提取参考

## 需要提取的字段

### 1. 卖家税号 (nbmst / MST người bán)
- 越南语标签: "Mã số thuế" 或 "MST"
- 格式: 10位数字（有时带横杠如 0101234567-001，只取前10位）
- 位置: 通常在发票顶部卖家信息区域

### 2. 发票符号 (khhdon / Ký hiệu hóa đơn)
- 越南语标签: "Ký hiệu hóa đơn" 或 "Ký hiệu"
- 格式: 字母和数字的组合，如 "AB/25E"、"C23TAA"
- 位置: 通常在发票编号附近

### 3. 发票号码 (shdon / Số hóa đơn)
- 越南语标签: "Số hóa đơn" 或 "Số"
- 格式: 1-8位数字，可能有前导零，如 "00000001"
- 位置: 发票编号区域

### 4. 发票类型 (khmshdon + hdon)
发票类型由两个字段组合确定:

| khmshdon | hdon | 中文含义 | 越南语 |
|----------|------|---------|--------|
| 1 | 01 | 增值税电子发票 | Hóa đơn điện tử giá trị gia tăng |
| 2 | 02 | 销售发票 | Hóa đơn bán hàng |
| 3 | 03 | 公共资产销售发票 | Hóa đơn bán tài sản công |
| 4 | 04 | 国家储备销售发票 | Hóa đơn bán hàng dự trữ quốc gia |
| 5 | 05 | 其他发票 | Hóa đơn khác |
| 6 | 06_01 | 内部调拨出库单 | Phiếu xuất kho kiêm vận chuyển nội bộ |
| 6 | 06_02 | 寄售代销出库单 | Phiếu xuất kho gửi bán hàng đại lý |
| 7 | 07 | 商业发票 | Hoá đơn thương mại |
| 8 | 08 | 增值税发票(含税费收据) | Hóa đơn GTGT tích hợp biên lai |
| 9 | 09 | 销售发票(含税费收据) | Hóa đơn bán hàng tích hợp biên lai |

判断方法:
- 发票上通常标注类型名称，如 "HÓA ĐƠN GIÁ TRỊ GIA TĂNG" → khmshdon=1, hdon=01
- "HÓA ĐƠN BÁN HÀNG" → khmshdon=2, hdon=02
- 也可以从 "Mẫu số" 字段推断: 如 "1C20TAA" 中第一个数字就是 khmshdon

### 5. 总金额 (tgtttbso / Tổng tiền thanh toán) - 可选
- 越南语标签: "Tổng tiền thanh toán" 或 "Tổng cộng"
- 格式: 纯数字（不带千位分隔符）
- 注意: 此字段可以留空，API 不强制要求

## 提取示例

一张典型越南发票的关键区域:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
...
Mã số thuế (MST): 0101234567
Ký hiệu: AB/25E
Số: 00000001
HÓA ĐƠN GIÁ TRỊ GIA TĂNG
...
```

对应参数:
- nbmst = "0101234567"
- khhdon = "AB/25E"
- shdon = "00000001"
- khmshdon = "1" (从 "HÓA ĐƠN GIÁ TRỊ GIA TĂNG" 或 "Mẫu số" 判断)
- hdon = "01"
