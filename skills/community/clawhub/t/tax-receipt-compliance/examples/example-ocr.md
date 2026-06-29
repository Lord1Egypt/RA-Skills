# 示例1：单张发票OCR识别

## 场景
用户有一张增值税专用发票，需要识别并提取结构化数据。

## 输入
```
识别发票 D:\invoices\20260628_001.png
```

## 处理步骤
1. `ocr_engine.py` 读取图片
2. 图像预处理（灰度化 → 去噪 → 二值化 → 纠偏）
3. Tesseract OCR 提取文字
4. 正则匹配提取关键字段
5. 输出结构化JSON

## 预期输出
```json
{
  "success": true,
  "invoice_type": "增值税专用发票",
  "invoice_code": "3100204130",
  "invoice_number": "00564189",
  "invoice_date": "2026-06-28",
  "seller_name": "上海某某科技有限公司",
  "buyer_name": "北京某某信息技术有限公司",
  "amount": 10000.00,
  "tax_rate": 0.13,
  "tax_amount": 1300.00,
  "total": 11300.00,
  "remark": "*信息技术服务费*",
  "confidence": 0.96,
  "timestamp": "2026-06-29T00:15:41"
}
```

## 命令
```bash
python scripts/ocr_engine.py --input D:\invoices\20260628_001.png --output D:\invoices\receipt_001.json
```

## 注意事项
- 图片需清晰、完整、无遮挡
- 建议使用300DPI以上扫描件
- 若 `confidence < 0.8`，建议重新拍摄或手动输入
- 支持的发票类型：增值税专用发票、电子发票、普通发票
- 暂不支持：手写发票、定额发票

## 常见错误

| 错误 | 解决 |
|------|------|
| `Tesseract not found` | 运行 `.\scripts\install_tesseract.ps1` 并重启终端 |
| `empty result` | 检查图片质量，确保光线均匀、平整 |
| `chi_sim not found` | 重新安装Tesseract，勾选中文语言包 |
| 识别率低 | 提高DPI（建议≥300），重新拍摄 |