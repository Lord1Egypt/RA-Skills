# 翔云通用文档/表格识别 API 文档

> 官网产品页：https://www.netocr.com/table.html

> ⚠️ **重要说明**：本 API 为**通用文档识别**接口，不仅支持表格识别，也支持纯文字文档、多语言文档、多栏排版文档等。表格识别只是其中一个典型场景。

---

## 一、接口总览

| 接口 | 说明 |
|:---|:---|
| `POST https://netocr.com/api/recog_table_base64` | 文档识别（Base64 图片），支持文字+表格+版面分析 |
| `POST https://netocr.com/api/recog_table_file` | 文档识别（File 上传），支持文字+表格+版面分析 |
| `POST https://netocr.com/api/download_file` | 导出识别结果为文件 |

---

## 二、表格识别接口

### 2.1 Base64 方式

**请求**

```
POST https://netocr.com/api/recog_table_base64
Content-Type: application/x-www-form-urlencoded
```

**必填参数**

| 参数 | 类型 | 说明 |
|:---|:---|:---|
| `img` | String | 图片 Base64 字符串（建议 300KB，最大 3M） |
| `key` | String | 用户 OCR Key（个人中心获取） |
| `secret` | String | 用户 OCR Secret（个人中心获取） |
| `typeId` | Integer | 固定值：**3050**（通用文档识别，支持文字+表格+版面分析） |
| `format` | String | 固定值：**json** |

**可选参数**

| 参数 | 类型 | 默认 | 可选值 | 说明 |
|:---|:---|:---:|:---|:---|
| `nLanguage` | Integer | 0 | 0-15 | 识别语言（见语言对照表） |
| `autoRotation` | Integer | 0 | 0/1 | 自动旋转：0=关，1=开 |
| `inclineCorrect` | Integer | 0 | 0/1/2 | 图像校正：0=无，1=透视畸变，2=弯曲畸变 |
| `filterColor` | Integer | 0 | 0-4 | 颜色过滤：0=无，1=弱滤红，2=强滤红，3=弱滤蓝，4=强滤蓝 |
| `backgroundFilter` | Integer | 0 | 0/1 | 去背景：0=关，1=开 |
| `removeWaterMark` | Integer | 0 | 0/1 | 去水印：0=关，1=开 |
| `refactoring` | Integer | 0 | 0/1/2/3 | 表格重构：0=少补线，1=不补线，2=多补线，3=全补线 |
| `layout` | Integer | 0 | 0/1 | 版面分析：0=关，1=开 |
| `subscript` | Integer | 0 | 0/1 | 角标识别：0=关，1=开 |
| `lineProcess` | Integer | 0 | 0/1 | 逐行校正：0=关，1=开 |
| `imageSegmentation` | Integer | 0 | 0/1 | 超大图切分：0=关，1=开 |

### 2.2 File 上传方式

```
POST https://netocr.com/api/recog_table_file
Content-Type: multipart/form-data
```

参数与 Base64 方式一致，但图片字段名为 `file`（MultipartFile 类型），其余参数同上。

> ⚠️ 上传文件字段名必须是 `file`，否则接口报错。

### 2.3 Python 调用示例

```python
import base64
import requests

# Base64 方式
def recognize_table_base64(image_path, key, secret, **options):
    with open(image_path, 'rb') as f:
        img_b64 = base64.b64encode(f.read()).decode('utf-8')

    payload = {
        'img': img_b64,
        'key': key,
        'secret': secret,
        'typeId': 3050,
        'format': 'json',
        **options  # 可选参数透传
    }
    resp = requests.post('https://netocr.com/api/recog_table_base64',
                         data=payload, timeout=60)
    return resp.json()


# File 方式
def recognize_table_file(image_path, key, secret, **options):
    with open(image_path, 'rb') as f:
        files = {'file': f}
        data = {
            'key': key,
            'secret': secret,
            'typeId': 3050,
            'format': 'json',
            **options
        }
        resp = requests.post('https://netocr.com/api/recog_table_file',
                             files=files, data=data, timeout=60)
    return resp.json()
```

### 2.4 返回结果示例

```json
{
  "message": {
    "status": 0,
    "value": {
      "consumeId": "1776397426889281",
      "num": "1-1",
      "info": {
        "result": [
          {
            "path": "",
            "parags": [...]
          }
        ]
      }
    }
  }
}
```

> ⚠️ **重要**：
> - `consumeId` 是导出文件的凭证，必须保存，识别完成后立即记录
> - 响应结构为 `message.value.xxx`，非 `code + data` 结构

---

## 三、文件导出接口

### 3.1 接口信息

```
POST https://netocr.com/api/download_file
Content-Type: application/x-www-form-urlencoded
```

> ⚠️ **注意**：此接口**不需要 key 和 secret**。

### 3.2 请求参数

| 参数 | 类型 | 必填 | 说明 |
|:---|:---|:---:|:---|
| `consumeId` | String | ✅ | 识别阶段返回的唯一 ID |
| `num` | String | ✅ | 页范围：`1-1`（第1页）、`1-10`（全部10页）、`2-5`（第2到5页） |
| `type` | String | ✅ | 导出格式（见下表） |

### 3.3 返回值：OSS 预签名 URL

此接口**不直接返回文件**，而是返回一个阿里云 OSS 预签名 URL（有效期约15分钟），需要用该 URL 再发起 GET 请求下载实际文件。

**响应格式**：
```json
{
  "message": {
    "status": 0,
    "value": "http://product.netocr.com/xxx.xls?Expires=1776435094&OSSAccessKeyId=...&Signature=..."
  }
}
```

**下载流程**：
1. 调用 `/api/download_file` 获取 OSS URL
2. 用返回的 URL 发起 GET 请求下载文件

### 3.4 支持的导出格式

| type 值 | 说明 | 文件后缀 |
|:---|:---|:---|
| `xls` | Excel 表格文件 | `.xls` |
| `flowWord` | Word 文字流文档 | `.docx` |
| `boxWord` | Word 文本框文档 | `.docx` |
| `md` | Markdown 文件 | `.md` |
| `pdf` | 双层 PDF（可搜索） | `.pdf` |
| `txt` | 纯文本文件 | `.txt` |
| `ofd` | OFD 格式文件 | `.ofd` |

### 3.4 Python 调用示例

```python
import requests

def download_result(consume_id, num, file_type, save_path):
    """下载识别结果到本地文件"""
    payload = {
        'consumeId': consume_id,
        'num': num,         # 如 "1-1" 或 "1-5"
        'type': file_type   # 如 "xls", "md", "flowWord"
    }
    resp = requests.post('https://netocr.com/api/download_file',
                         data=payload, timeout=60)

    if resp.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(resp.content)
        return True, save_path
    else:
        return False, resp.text
```

---

## 四、nLanguage 语言对照表

| 值 | 语言 | 值 | 语言 |
|:---:|:---|:---:|:---|
| 0 | 简体中文（印刷）| 8 | 西里尔文 |
| 1 | 繁体中文（印刷）| 9 | 法文 |
| 2 | 英文 | 10 | 西班牙文 |
| 3 | 简体中文（印刷+手写）| 11 | 日文 |
| 4 | 繁体中文（印刷+手写）| 12 | 韩文 |
| 5 | 阿拉伯文 | 13 | 葡萄牙文 |
| 6 | 乌尔都文 | 14 | 越南文 |
| 7 | 格鲁吉亚文 | 15 | 孟加拉文 |

---

## 五、图片/文件要求

| 类型 | 要求 |
|:---|:---|
| 支持格式 | PNG、JPG、JPEG、WEBP、TIF、OFD、PDF |
| 普通图像大小 | 约 200KB，位深度 24 以上 |
| 扫描件 | 分辨率 300DPI，小于 3M |
| 推荐大小 | 200KB - 500KB |

---

## 六、本地配置文件

将凭据保存到 `./config.json`（Skill 包同目录下），避免每次重复输入：

```json
// config.json（与 recognize_table.py 同目录）
{
  "key": "你的OCRKey",
  "secret": "你的OCRSecret"
}
```

脚本启动时自动读取此文件，无需每次传入参数。
也支持环境变量 `NETOCR_KEY` / `NETOCR_SECRET` 作为备选。

| 错误码 | 含义 | 建议处理 |
|:---:|:---|:---|
| 0 | 成功 | — |
| 10001 | 缺少必要参数 | 检查 typeId/format 是否正确填写 |
| 10002 | 识别失败 | 改善图片质量，开启 autoRotation |
| 10003 | 账户额度不足 | 充值或更换账号 |
| 10004 | 图片格式错误 | 转为 JPG/PNG 后重试 |
| 20001 | Key/Secret 错误 | 重新配置凭据 |
| 20002 | 签名验证失败 | 检查 key/secret 是否含多余空格 |
| 20003 | 服务超时 | 稍后重试，或缩小图片尺寸 |
