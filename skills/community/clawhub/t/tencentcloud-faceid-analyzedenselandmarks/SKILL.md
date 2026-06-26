---
name: tencentcloud-faceid-analyzedenselandmarks
description: 腾讯云稠密人脸关键点(AnalyzeDenseLandmarks)接口调用技能。当用户需要对人脸图片进行稠密关键点定位时，应使用此技能。可返回人脸框坐标，以及人脸各部位（眼睛、眉毛、嘴巴、鼻子、瞳孔、中轴线、下巴、眼袋、额头）的稠密轮廓关键点坐标。支持图片Base64和图片URL两种输入方式。
---

# 腾讯云稠密人脸关键点 (AnalyzeDenseLandmarks)

## 用途

调用腾讯云人脸识别（IAI）稠密人脸关键点接口，对请求图片进行五官定位，计算构成人脸轮廓的关键点，包括眉毛、眼睛、鼻子、嘴巴、下巴、脸型轮廓、中轴线等。

核心能力：
- **稠密关键点定位**：返回人脸各部位的高密度轮廓点坐标
- **多部位覆盖**：眼睛、眉毛、嘴巴（内/外）、鼻子、瞳孔、中轴线、下巴、眼袋、额头
- **多人脸支持**：最多返回 5 张人脸的关键点信息
- **多输入方式**：支持图片 Base64 和图片 URL 两种输入方式，传入本地文件时可自动转为 Base64

官方文档：https://cloud.tencent.com/document/product/867/47397

## 使用时机

当用户提出以下需求时触发此技能：
- 需要对人脸图片进行稠密关键点定位
- 需要获取人脸各部位（眼睛、眉毛、嘴巴、鼻子等）的轮廓坐标
- 需要进行人脸轮廓分析或人脸对齐
- 涉及人脸关键点提取、人脸形状分析的任何场景

## 环境要求

- Python 3.6+
- 依赖：`tencentcloud-sdk-python`（通过 `pip install tencentcloud-sdk-python` 安装）
- 环境变量：
  - `TENCENTCLOUD_SECRET_ID`：腾讯云API密钥ID
  - `TENCENTCLOUD_SECRET_KEY`：腾讯云API密钥Key

## 使用方式

运行 `scripts/main.py` 脚本完成稠密人脸关键点检测。

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| --image | str | 否 | 本地图片文件路径（自动转 Base64）或 Base64 字符串，与 --url 二选一 |
| --url | str | 否 | 图片 URL，与 --image 二选一（都提供时优先使用 URL）|
| --mode | int | 否 | 检测模式：`0`(检测所有人脸) / `1`(仅检测面积最大的人脸)，默认 `0` |
| --need-rotate-detection | int | 否 | 是否开启图片旋转识别：`0`(不开启) / `1`(开启)，默认 `0` |
| --region | str | 否 | 腾讯云地域，默认 `ap-guangzhou` |

### 图片输入规格

- **格式**：支持 PNG、JPG、JPEG、BMP，不支持 GIF
- **大小**：Base64 编码后不超过 5MB
- **分辨率**：jpg 格式长边不超过 4000px，其他格式长边不超过 2000px，短边不小于 64px
- **算法版本**：仅支持 3.0

### 输出格式

检测成功后返回 JSON 格式结果：

```json
{
  "ImageWidth": 480,
  "ImageHeight": 640,
  "FaceModelVersion": "3.0",
  "FaceCount": 1,
  "DenseFaceShapeSet": [
    {
      "FaceRect": {"X": 100, "Y": 80, "Width": 200, "Height": 250},
      "LeftEye": [{"X": 150, "Y": 180}, ...],
      "RightEye": [...],
      "LeftEyeBrow": [...],
      "RightEyeBrow": [...],
      "MouthOutside": [...],
      "MouthInside": [...],
      "Nose": [...],
      "LeftPupil": [...],
      "RightPupil": [...],
      "CentralAxis": [...],
      "Chin": [...],
      "LeftEyeBags": [...],
      "RightEyeBags": [...],
      "Forehead": [...]
    }
  ],
  "RequestId": "xxx"
}
```

### 各部位关键点说明

| 部位字段 | 说明 |
|----------|------|
| LeftEye / RightEye | 左/右眼睛轮廓点 |
| LeftEyeBrow / RightEyeBrow | 左/右眉毛轮廓点 |
| MouthOutside | 外嘴巴轮廓点（从左侧开始逆时针） |
| MouthInside | 内嘴巴轮廓点（从左侧开始逆时针） |
| Nose | 鼻子轮廓点 |
| LeftPupil / RightPupil | 左/右瞳孔轮廓点 |
| CentralAxis | 中轴线轮廓点 |
| Chin | 下巴轮廓点 |
| LeftEyeBags / RightEyeBags | 左/右眼袋轮廓点 |
| Forehead | 额头轮廓点 |

### 调用示例

```bash
# 传入本地图片文件（自动转 Base64）
python scripts/main.py --image ./face.jpg

# 传入图片 URL
python scripts/main.py --url "https://example.com/face.jpg"

# 只检测面积最大的人脸
python scripts/main.py --image ./face.jpg --mode 1

# 开启旋转识别
python scripts/main.py --image ./face.jpg --need-rotate-detection 1
```
