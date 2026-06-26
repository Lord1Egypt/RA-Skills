# OCR发票解析指南

## 调用方式（批量模式）

步骤4使用以下方式**一次性完成所有PDF的OCR**，不逐张调用：

```python
import sys, os, glob, json
sys.path.insert(0, '/app/skills/pdf-ocr-skill/scripts')
from pdf_ocr_processor import PDFOCRProcessor

inbox_dir = '/tmp/openclaw/uploads/{session_id}/inbox/'
pdf_files = sorted(glob.glob(os.path.join(inbox_dir, '*.pdf')))

processor = PDFOCRProcessor(engine='rapid')
results = []
for pdf_path in pdf_files:
    result = processor.ocr_pdf(pdf_path)
    results.append({'pdf_path': pdf_path, 'filename': os.path.basename(pdf_path), 'text': result['text'], 'page_count': result['page_count']})

print(json.dumps(results, ensure_ascii=False, indent=2))
```

返回结构示例：
```json
[
  {
    "pdf_path": "/tmp/openclaw/uploads/.../invoice.pdf",
    "filename": "invoice.pdf",
    "text": "发票全文...",
    "page_count": 1
  }
]
```

## 12306火车票字段提取

从OCR结果中提取：
- 发票号码（右上方）
- 开票日期
- 出发站、到达站
- 车次
- 乘车日期、发车时间
- 座位信息（车厢、座位号、席别）
- 票价金额
- 乘客姓名、身份证号（脱敏）
- 购买方名称、统一社会信用代码

输出格式：
```json
{
  "type": "railway",
  "invoice_number": "26329116804005647551",
  "issue_date": "2026-05-26",
  "departure": "南京南",
  "arrival": "北京南",
  "transport_number": "G50",
  "travel_date": "2026-04-01",
  "departure_time": "20:06",
  "seat_info": "02车05A号 二等座",
  "amount": 464.00,
  "passenger_name": "马天澍",
  "passenger_id": "3212011996****0216",
  "buyer_name": "浩鲸云计算科技股份有限公司",
  "buyer_tax_id": "91320100745379000T",
  "pdf_path": "inbox/railway/xxx.pdf"
}
```

## 美团发票字段提取

从OCR结果中提取：
- 发票号码
- 开票日期
- 服务类型（如"经纪代理服务"→代订房费）
- 商家/酒店名称（从备注中提取）
- 金额（价税合计）
- 入住日期、离店日期、晚数（从备注中提取）
- 购买方名称、统一社会信用代码

输出格式：
```json
{
  "type": "meituan",
  "invoice_number": "26352000001272859066",
  "issue_date": "2026-05-26",
  "service_type": "代订房费",
  "merchant_name": "全季酒店（XXX店）",
  "check_in": "2026-04-02",
  "check_out": "2026-04-04",
  "nights": 2,
  "amount": 1144.85,
  "buyer_name": "浩鲸云计算科技股份有限公司",
  "buyer_tax_id": "91320100745379000T",
  "pdf_path": "inbox/meituan/xxx.pdf"
}
```

## 其他发票类型参照处理

- 携程机票：提取航班号、出发/到达城市、日期、金额、乘客姓名
- 携程酒店/华住会酒店：提取酒店名、入住/离店日期、金额、入住人

## 发票类型识别特征

| 类型 | 识别特征 |
|------|---------|
| 12306火车票 | 包含"中国铁路"/"电子客票"/"国家税务总局" |
| 携程机票 | 包含"携程"/"航空运输电子客票行程单" |
| 携程酒店 | 包含"携程"/"住宿服务" |
| 华住会酒店 | 包含"华住"/"汉庭"/"全季"/"桔子"等 |
| 美团发票 | 包含"美团"/"美团外卖"/"大众点评" |
