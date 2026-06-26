# 附件控件详解

## 附件控件 (attachmentWidget)

### 数据结构

```json
{
  "codeId": "At_0",
  "type": "attachmentWidget",
  "title": "附件",
  "maximum": 200,
  "allowDocDispatch": true,
  "extendFieldMap": {
    "docOnly": false,
    "pdfOnly": false
  },
  "value": [
    {
      "fileId": "69f06679d0c3b700014ec175",
      "fileName": "document.pdf",
      "fileSize": "482",
      "fileExt": "pdf",
      "fileType": "application/pdf",
      "fileMime": "null",
      "pdfFileSize": "null",
      "ofdFileSize": "null"
    }
  ]
}
```

### value 字段说明

| 字段 | 类型 | 说明 |
|-----|------|------|
| `fileId` | String | 云之家文件ID，用于下载文件 |
| `fileName` | String | 文件名 |
| `fileSize` | String | 文件大小（字节） |
| `fileExt` | String | 文件扩展名 |
| `fileType` | String | MIME类型 |

---

## 图片控件 (imageWidget)

### 数据结构

```json
{
  "codeId": "Im_0",
  "type": "imageWidget",
  "title": "图片",
  "maximum": 12,
  "value": ["fileId1", "fileId2"]
}
```

**注意**: 图片控件的 `value` 是文件ID数组，比附件控件简单。

---

## 文件下载接口

通过 fileId 下载文件：

```bash
curl -X GET \
  'https://www.yunzhijia.com/docrest/doc/user/downloadfile?fileId=5b860345b6238e3d9e9e1973' \
  -H 'Cache-Control: no-cache' \
  -H 'x-accessToken: iq0lfXAJCu2GlxxxxdZpLxxxx3ihC590'
```

**接口说明**:
- 请求方式: GET
- 接口地址: `https://www.yunzhijia.com/docrest/doc/user/downloadfile`
- 参数: `fileId` - 文件ID
- Header: `x-accessToken` - 访问令牌