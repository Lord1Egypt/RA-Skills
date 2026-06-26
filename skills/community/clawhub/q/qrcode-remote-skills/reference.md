# QR Code API Reference

草料二维码开放 API 完整参考文档。

官方文档：https://cli.im/open-api/qrcode-api/quick-start.html

## 生成二维码 API

**端点：** `GET https://api.2dcode.biz/v1/create-qr-code`

直接返回二维码图片（非 JSON），可嵌入 `<img>` 标签或 Markdown 图片语法中。

### 参数详情

#### data（必选）

二维码中存储的文本内容，需 URL 编码。

- 最小字符数：1
- 建议不超过 900 字符
- 实际容量取决于纠错级别，纠错越高容量越小

#### size

图片尺寸（仅对 PNG 格式有效）。

- 格式：`WxH`（如 `256x256`）或单个整数（如 `256`，生成正方形）
- 默认值：`256x256`
- 最小不限，但至少需要 `41x41` 像素才能满足二维码矩阵

#### format

输出格式。

| 值 | 类型 |
|----|------|
| png | 位图（默认） |
| svg | 矢量 |

#### error_correction

纠错级别。

| 值 | 说明 |
|----|------|
| L | 低级别（7%） |
| M | 中级别（15%，默认） |
| Q | 较高级别（25%） |
| H | 最高级别（30%） |

#### border

边框宽度（码点为单位）。

- 默认值：2
- 最小值：0

### 完整 URL 示例

```
https://api.2dcode.biz/v1/create-qr-code?data=https%3A%2F%2Fexample.com&size=400x400&format=png&error_correction=H&border=2
```

---

## 解码二维码 API

**端点：** `https://api.2dcode.biz/v1/read-qr-code`

### GET 方式

通过图片 URL 解码。

```
GET https://api.2dcode.biz/v1/read-qr-code?file_url=<URL编码的图片地址>
```

**参数：**

| 参数 | 必选 | 说明 |
|------|------|------|
| file_url | 是 | 二维码图片的 URL（需 URL 编码） |

### POST 方式

通过上传文件解码。

```
POST https://api.2dcode.biz/v1/read-qr-code
Content-Type: multipart/form-data
```

**参数：**

| 参数 | 必选 | 说明 |
|------|------|------|
| file | 是 | 二维码图片文件（form-data） |

### 响应

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "contents": ["Example"]
  }
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| code | number | 0 表示成功，其他表示失败 |
| message | string | 返回信息 |
| data.contents | array | 二维码内容数组，支持多码识别，无码时为空数组 |
