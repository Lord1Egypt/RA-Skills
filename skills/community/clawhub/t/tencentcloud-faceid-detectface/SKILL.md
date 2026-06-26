---
name: tencentcloud-faceid-detectface
description: 腾讯云人脸检测(DetectFace)接口调用技能。当用户需要对图片进行人脸检测时，应使用此技能。可检测图片中的人脸位置（坐标、宽高），并可选返回人脸属性（性别、年龄、表情、魅力、眼镜、口罩、头发、姿态）和人脸质量信息（质量分、模糊分、光照分、遮挡分）。支持图片Base64和图片URL两种输入方式，支持同时检测多张人脸。
---

# 腾讯云人脸检测 (DetectFace)

## 用途

调用腾讯云人脸识别（IAI）DetectFace 接口，对请求图片进行人脸检测，获取人脸坐标、属性信息及质量信息。

核心能力：
- **人脸定位**：返回人脸框的坐标（X、Y）及宽高（Width、Height）
- **多人脸检测**：支持同时检测多张人脸，最多 120 张
- **人脸属性**（可选）：性别、年龄、表情、魅力、眼镜、口罩、头发、姿态（pitch/roll/yaw）
- **质量检测**（可选）：质量分（score）、模糊分（sharpness）、光照分（brightness）、遮挡分（completeness）
- **多输入方式**：支持图片 Base64 和图片 URL 两种输入方式，传入本地文件时自动转 Base64

官方文档：https://cloud.tencent.com/document/product/867/44989

## 使用时机

当用户提出以下需求时触发此技能：
- 需要检测图片中是否有人脸
- 需要获取人脸在图片中的位置（坐标）
- 需要获取人脸属性信息（年龄、性别、表情等）
- 需要评估人脸图片质量
- 需要统计图片中的人脸数量

## 环境要求

- Python 3.6+
- 依赖：`tencentcloud-sdk-python`（通过 `pip install tencentcloud-sdk-python` 安装）
- 环境变量：
  - `TENCENTCLOUD_SECRET_ID`：腾讯云API密钥ID
  - `TENCENTCLOUD_SECRET_KEY`：腾讯云API密钥Key

## 使用方式

运行 `scripts/main.py` 脚本完成人脸检测。

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| --image | str | 与 --url 二选一 | 本地图片文件路径（自动转 Base64）或 Base64 字符串 |
| --url | str | 与 --image 二选一 | 图片的 URL 地址，优先级高于 --image |
| --max-face-num | int | 否 | 最多检测人脸数，默认 1，最大 120 |
| --min-face-size | int | 否 | 人脸最小尺寸（像素），只支持 34 和 20，默认 34 |
| --need-face-attributes | int | 否 | 是否返回人脸属性：0(不返回)/1(返回)，默认 0 |
| --need-quality-detection | int | 否 | 是否开启质量检测：0(关闭)/1(开启)，默认 0 |
| --face-model-version | str | 否 | 算法模型版本：2.0/3.0，默认 3.0 |
| --need-rotate-detection | int | 否 | 是否开启旋转识别：0(关闭)/1(开启)，默认 0 |
| --region | str | 否 | 腾讯云地域，默认 ap-guangzhou |

### 图片输入规格

- **格式**：支持 PNG、JPG、JPEG、BMP，不支持 GIF
- **大小**：Base64 编码后不可超过 5MB
- **分辨率**：jpg 格式长边像素不可超过 4000，其他格式不可超 2000；短边不小于 64px

### 输出格式

检测成功后返回 JSON 格式结果：

```json
{
  "ImageWidth": 640,
  "ImageHeight": 480,
  "FaceModelVersion": "3.0",
  "FaceCount": 1,
  "FaceInfos": [
    {
      "X": 100,
      "Y": 80,
      "Width": 200,
      "Height": 220,
      "FaceAttributesInfo": {
        "Gender": 99,
        "Age": 28,
        "Expression": 0,
        "Beauty": 60,
        "Glass": false,
        "Pitch": 2,
        "Yaw": -5,
        "Roll": 1,
        "Mask": 0,
        "Hair": {"Length": 1, "Bang": 0, "Color": 0}
      },
      "FaceQualityInfo": {
        "Score": 88,
        "Sharpness": 90,
        "Brightness": 85,
        "Completeness": {...}
      }
    }
  ],
  "RequestId": "xxx"
}
```

### 属性字段说明

| 字段 | 说明 |
|------|------|
| Gender | 性别：0(女性) ~ 100(男性)，大于 50 为男性 |
| Age | 年龄：0~100 |
| Expression | 笑容：0(严肃) ~ 100(大笑) |
| Beauty | 魅力：0~100 |
| Glass | 是否戴眼镜：true/false |
| Mask | 口罩：0(无口罩) |
| Pitch | 俯仰角：上下点头，-30°~30° |
| Yaw | 偏航角：左右摇头，-30°~30° |
| Roll | 翻滚角：歪头，-180°~180° |

### 质量字段说明

| 字段 | 说明 |
|------|------|
| Score | 质量分：0~100，越高越好，建议 > 80 用于人脸入库 |
| Sharpness | 清晰分：0~100，越高越清晰 |
| Brightness | 光照分：0~100，越高光照越好 |
| Completeness | 遮挡分：包含眉毛、眼睛、鼻子、脸颊、嘴巴、下巴遮挡情况 |

### 调用示例

```bash
# 传入本地图片文件（仅检测人脸位置）
python scripts/main.py --image ./face.jpg

# 传入图片 URL
python scripts/main.py --url "https://example.com/face.jpg"

# 开启属性检测 + 质量检测，最多检测 5 张人脸
python scripts/main.py --image ./face.jpg --need-face-attributes 1 --need-quality-detection 1 --max-face-num 5

# 传入 Base64 字符串
python scripts/main.py --image "<base64_string>"
```
