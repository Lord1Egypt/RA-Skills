# 最美证件照 API 详细文档

## 基础信息

- **Base URL**: `https://idphoto.huipai.vip`
- **协议**: HTTPS
- **编码**: UTF-8
- **认证**: v2 签名认证

## 请求头

| 头部 | 必填 | 说明 |
|------|------|------|
| X-API-Key | 是 | API Key ID |
| X-Timestamp | 是 | Unix 时间戳（秒） |
| X-Nonce | 是 | 随机字符串（建议 32 位 hex） |
| X-Signature | 是 | HMAC-SHA256 签名 |
| X-Content-SHA256 | 是 | 请求内容 SHA256 摘要 |
| X-Sign-Version | 是 | 签名版本，固定为 `v2` |

## 响应格式

```json
{
  "code": 0,
  "message": "success",
  "data": { }
}
```

## 错误码

| 错误码 | 说明 |
|--------|------|
| 0 | 成功 |
| 20001 | **余额不足，请充值后继续使用** |
| 40001 | 参数格式错误 |
| 40002 | 参数值无效 |
| 40024 | 缺少图片源参数 |
| 40025 | 图片格式不支持 |
| 40101 | 签名验证失败 |
| 40102 | 时间戳过期 |
| 40103 | 请求重复提交 |
| 40104 | API Key 无效 |
| 50001 | 系统内部错误 |
| 50003 | 服务繁忙 |

---

## 1. 一键证件照

**POST** `/api/v1/photo/id-photo`

完整的证件照制作流程：人脸检测 → 人像分割 → 智能裁剪 → 美颜（可选）→ 换底色。

### 请求参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| image | file | 否* | - | 图片文件 |
| image_base64 | string | 否* | - | Base64 编码图片 |
| width | int | 否 | 295 | 目标宽度（50-2000） |
| height | int | 否 | 413 | 目标高度（50-2000） |
| background_color | string | 否 | #FFFFFF | 背景颜色 |
| dpi | int | 否 | 300 | 图片 DPI（72-1200） |
| max_size_kb | int | 否 | - | 文件大小限制（KB） |
| return_hd_transparent | bool | 否 | false | 是否返回高清透明 PNG |
| beautify_flag | bool | 否 | false | 是否启用美颜 |
| verify | bool | 否 | false | 是否启用完整照片校验 |
| subject_mode | string | 否 | single | single=单人，couple=双人结婚照 |
| output_format | string | 否 | jpeg | 输出格式（jpeg/png/webp） |

*image 和 image_base64 二选一

### 常见证件照尺寸

| 规格 | 宽 x 高 (px) | 毫米 |
|------|-------------|------|
| 一寸 | 295 x 413 | 25mm x 35mm |
| 二寸 | 413 x 579 | 35mm x 49mm |
| 小二寸 | 413 x 531 | 35mm x 45mm |
| 护照 | 390 x 567 | 33mm x 48mm |

### 背景色格式

- 纯色：`#FFFFFF`（白）、`#438EDB`（蓝）、`#FF0000`（红）
- 上下渐变：`#438EDB,updown`
- 中心渐变：`#438EDB,center`
- 多背景色：`#FFFFFF;#438EDB;#FF0000`（最多5个，用分号分隔）

### 响应示例

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "image_url": "https://cdn.example.com/result.jpg",
    "hd_transparent_url": "https://cdn.example.com/transparent.png",
    "width": 295,
    "height": 413,
    "dpi": 300,
    "size_kb": 45,
    "output_format": "jpeg"
  }
}
```

### 计费

- 基础费用：抠图 + 人脸检测
- 启用美颜（beautify_flag=true）：额外收取美颜费用

---

## 2. 智能抠图

**POST** `/api/v1/segment/portrait`

将图片中的人像抠出，生成透明背景 PNG。

### 请求参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| image | file | 否* | - | 图片文件（JPG/PNG/WebP/HEIC） |
| image_base64 | string | 否* | - | Base64 编码图片 |
| quality | string | 否 | hd-pro | 分割质量 |

*image 和 image_base64 二选一

### 响应示例

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "image_url": "https://cdn.example.com/result.png"
  }
}
```

### 计费

按抠图单价扣费。

---

## 3. 换背景色

**POST** `/api/v1/segment/background`

将图片的背景替换为指定颜色，支持纯色和渐变色。

### 请求参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| image | file | 否* | - | 图片文件 |
| image_base64 | string | 否* | - | Base64 编码图片 |
| background_color | string | 否 | #FFFFFF | 背景颜色 |
| quality | string | 否 | - | 分割质量（传值则扣费） |
| dpi | int | 否 | 300 | 输出 DPI（72-1200） |
| max_size_kb | int | 否 | - | 文件大小限制（KB） |
| output_format | string | 否 | jpeg | 输出格式（jpeg/png/webp） |

### 工作模式

- **传入 quality 参数**：使用人像分割，然后换底色（扣费）
- **不传 quality 参数**：仅支持透明背景 PNG，直接换底色（免费）

### 背景色格式

| 格式 | 示例 | 说明 |
|------|------|------|
| 纯色 | `#FFFFFF` | 白色背景 |
| 纯色 | `#438EDB` | 蓝色背景 |
| 上下渐变 | `#438EDB,updown` | 从蓝色渐变到白色 |
| 中心渐变 | `#438EDB,center` | 从蓝色向四周渐变到白色 |
| 多背景色 | `#FFFFFF;#438EDB;#FF0000` | 生成多个不同背景色的图片（最多5个） |

### 响应示例

单背景色：
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "image_url": "https://cdn.example.com/result.jpg",
    "dpi": 300,
    "output_format": "jpeg"
  }
}
```

多背景色：
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "images": [
      {"background_color": "#FFFFFF", "image_url": "..."},
      {"background_color": "#438EDB", "image_url": "..."}
    ],
    "dpi": 300
  }
}
```

### 计费

- 传入 `quality` 参数：按抠图单价扣费
- 不传 `quality` 参数：免费（仅支持透明背景 PNG）

---

## 4. 人脸增强

**POST** `/api/v1/photo/enhance`

使用 AI 进行人脸增强、去模糊、修复，可选超分辨率。

### 请求参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| image | file | 否* | - | 图片文件 |
| image_base64 | string | 否* | - | Base64 编码图片 |
| fidelity | float | 否 | 0.3 | 保真度（0.0-1.0） |
| use_sr | bool | 否 | false | 是否使用超分辨率 |
| sr_scale | int | 否 | 2 | 放大倍数（2 或 4） |
| restore_size | bool | 否 | true | 是否恢复原始尺寸 |

### 参数说明

- **fidelity**: 保真度，值越小增强越强，但可能失真
- **use_sr**: 启用 Real-ESRGAN 超分辨率
- **sr_scale**: 放大倍数
- **restore_size**: 放大后缩小回原尺寸，提升清晰度但保持大小

### 响应示例

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "original_url": "https://cdn.example.com/original.jpg",
    "enhanced_url": "https://cdn.example.com/enhanced.jpg",
    "width": 800,
    "height": 600,
    "dpi": 300,
    "enhance_time": 2.5,
    "face_count": 1
  }
}
```

### 计费

按增强单价扣费。

---

## 5. 排版照

**POST** `/api/v1/photo/layout`

将证件照排列在一张纸上，方便打印。

### 请求参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| image | file | 否* | - | 证件照图片 |
| image_base64 | string | 否* | - | Base64 编码图片 |
| crop_line | bool | 否 | false | 是否添加裁剪线 |
| layout_type | string | 否 | 6inch | 排版类型 |
| watermark | string | 否 | - | 自定义水印（最多6字符） |

### layout_type 可选值

| 值 | 画布尺寸 (px) | 毫米 |
|----|--------------|------|
| 6inch | 1795 x 1205 | 152mm x 102mm |
| 5inch | 1500 x 1051 | 127mm x 89mm |
| A4 | 3508 x 2479 | 297mm x 210mm |
| 3R | 1500 x 1051 | 127mm x 89mm |
| 4R | 1795 x 1205 | 152mm x 102mm |

### 响应示例

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "image_url": "https://cdn.example.com/layout.jpg",
    "width": 1795,
    "height": 1205,
    "dpi": 300,
    "photo_count": 8,
    "layout_type": "6inch"
  }
}
```

### 计费

免费。

---

## 6. 图片编辑

**POST** `/api/v1/photo/edit`

对图片进行尺寸调整、DPI 设置、格式转换和压缩。

### 请求参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| image | file | 否* | - | 图片文件 |
| image_base64 | string | 否* | - | Base64 编码图片 |
| width | int | 否 | 原图宽度 | 目标宽度 |
| height | int | 否 | 原图高度 | 目标高度 |
| dpi | int | 否 | 300 | 图片 DPI |
| max_size_kb | int | 否 | - | 文件大小限制（KB） |
| output_format | string | 否 | jpeg | 输出格式（jpeg/png/webp） |

### 响应示例

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "image_url": "https://cdn.example.com/result.jpg",
    "width": 800,
    "height": 600,
    "dpi": 300,
    "size_kb": 150,
    "output_format": "jpeg"
  }
}
```

### 计费

免费。
