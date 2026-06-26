# Sugon-Scnet OCR API 文档摘要

## 接口地址
`POST https://api.scnet.cn/api/llm/v1/ocr/recognize`

## 请求头
- `Content-Type: multipart/form-data`
- `Authorization: Bearer <你的 API Key>`

## 请求参数（表单）
| 参数名  | 类型 | 必填 | 描述                                   |
| ------- | ---- | ---- | -------------------------------------- |
| file    | File | 是   | 需要识别的图片文件                     |
| ocrType | str  | 是   | 识别类型枚举，详见 SKILL.md 参数说明   |

## 响应结构
```json
{
    "code": "0",
    "msg": "success",
    "data": [
        {
            "traceId": "202604010000019",
            "originalFilename": "火车票示例.jpg",
            "cosPath": "/ocr/202604/01/火车票示例.jpg",
            "result": [
                {
                    "status": 200,
                    "originFilename": "火车票示例.jpg",
                    "cosPath": "/ocr/202604/01/火车票示例.jpg",
                    "fileIndex": 1,
                    "cutIndex": 0,
                    "coordinate": [],
                    "classifyCode": "TRAIN_TICKET",
                    "confidence": 0.997,
                    "elements": {
                      "title": "电子发票(铁路电子客票)",
                      "ticketNo": "03C027012",
                      "departStation": "南京",
                      "destinationStation": "上海虹桥",
                      "trainNo": "D1021",
                      "departDate": "20220120",
                      "departTime": "0.265972222222222",
                      "seatPostion": "03车01F号",
                      "seatNo": "一等座",
                      "ticketPrice": "48",
                      "passengerName": "梁某某",
                      "identifyId": "3422011966****1111",
                      "invoiceNo": "22119230671000000011",
                      "invoiceDate": "20220317",
                      "preTaxAmount": "45.28",
                      "taxRate": "0.06",
                      "taxAmount": "2.72",
                      "elecTicketNo": "306712A086012090014312022",
                      "originInvoiceNo": "22119230671000000010",
                      "buyerName": "铁路客票电子发票测试单位",
                      "socialCreditCode": "91110001110AE35858",
                      "refundTag": "Y",
                      "replaceTag": "Y",
                      "otherInfo": ""
                    },
                    "stamps": []
                }
            ]
        }
    ]
}
```
## 错误码
- `401 / 403: Token 无效或过期`
- `其他 4xx/5xx: 请检查请求参数或联系服务商`
- `业务错误码（如 code 非 0）：见返回的 msg 字段`

## 注意事项
- `支持单张图片、PDF 或多页压缩包（自动解压识别）`
- `识别结果位于 data[0].result[0].elements 中`
- `不同 ocrType 返回的 elements 字段不同，详见 assets/templates/fields-summary.md`
