# Sugon-Scnet OCR API 文档摘要

> **⚠️ 隐私提示**：调用本接口时，您上传的文件内容将离开本地环境并传输至 SCNET 服务器进行处理。请确保您有权共享该文件，并了解 SCNET 的数据处理与保留策略。

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
      "traceId": "202604010000016",
      "originalFilename": "税务登记证示例.jpg",
      "cosPath": "scnetAPIService/20260101/3f7af0ad3ee44374a9cc4afd7d3ff152.jpg",
      "result": [
        {
          "status": 200,
          "originFilename": "税务登记证示例.jpg",
          "cosPath": "scnetAPIService/20260101/3f7af0ad3ee44374a9cc4afd7d3ff152.jpg",
          "fileIndex": 1,
          "cutIndex": 0,
          "coordinate": [],
          "classifyCode": "",
          "confidence": 0.9099,
          "elements": {
            "title": "税务登记证",
            "copyFlag": "副本",
            "certificateNumber": "国地税湘字16873471907431号",
            "taxpayerName": "湖南亮晶晶酒店用品有限责任公司",
            "legalRepresentative": "陈用民",
            "address": "湖南省长沙市昌北经济技术开发区第十三大街星火仓库、第1002仓库、第2002商务楼",
            "registrationType": "有限责任公司",
            "businessScope": "酒店设备、酒店用品、消防设备、公共服务设备；酒店商务，酒店管理服务，酒店培训；餐具制品；灯具制品；一次性用品**",
            "approvingAuthority": "湖南省长沙市工商行政管理局",
            "withholdingObligation": "依法确定",
            "issueDate": "2021年04月22日"
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
- `识别结果位于 data[0].result[0].stamps 中`
- `不同 ocrType 返回的 stamps 字段不同，详见 assets/templates/fields-summary.md`
