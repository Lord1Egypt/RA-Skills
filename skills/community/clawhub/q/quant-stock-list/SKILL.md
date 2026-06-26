---
name: quant-stock-list
description: 从图片自动识别股票并加入股票池。触发条件：用户发送股票截图/图片并要求加入股票池。功能：(1) 使用RapidOCR识别图片中的股票代码、名称、涨幅、价格 (2) 自动去重 (3) FIFO原则管理30只股票上限 (4) 保存到manual_stock_list.json。
---

# quant-stock-list

从图片识别股票代码并自动加入股票池。

## 工作流程

1. 读取图片：`/Users/wy/.openclaw/media/inbound/{uuid}.jpg`
2. RapidOCR识别
3. 解析股票代码（6位数字）
4. 去重 + FIFO（上限30只）
5. 保存到 `stone_quant/manual_stock_list.json`

## OCR脚本

```python
from rapidocr_onnxruntime import RapidOCR
import cv2

ocr = RapidOCR()
img = cv2.imread(img_path)
result, _ = ocr(img)

stocks = []
for bbox, text, conf in result:
    if text.isdigit() and len(text) == 6:
        code = text
        # 下一条通常是名称
        stocks.append(code)
```

## 自动加入规则

- 读取现有股票列表
- 新股票加入（去重）
- 超过30只按FIFO移除最旧的
- 记录加入时间和来源

## 保存格式

```json
{
  "stocks": [
    {"code": "600010", "name": "包钢股份", "add_time": "22:30", "source": "图片识别"}
  ]
}
```
