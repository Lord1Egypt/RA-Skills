---
name: tencentcloud-faceid-compareface
description: 腾讯云人脸比对(CompareFace)接口调用技能。当用户需要对两张人脸图片进行相似度比对时，应使用此技能。基于腾讯云人脸识别服务，对两张图片中的人脸进行相似度比较，返回人脸相似度分数。支持图片Base64和图片URL两种输入方式，可用于判断两张人脸是否为同一人。
---

# 腾讯云人脸比对 (CompareFace)

## 用途

调用腾讯云人脸识别 CompareFace 接口，对两张图片中的人脸进行相似度比较，返回人脸相似度分数。

核心能力：
- **人脸相似度比对**：对两张图片中的人脸进行相似度打分（0~100分）
- **同一人判断**：根据相似度分数判断两张人脸是否为同一人
- **多输入方式**：支持图片 Base64 和图片 URL 两种输入方式，传入本地文件时可自动转为 Base64
- **质量控制**：可选图片质量控制，过滤低质量图片
- **算法版本**：支持 2.0 和 3.0 两个算法版本，默认使用 3.0

官方文档：https://cloud.tencent.com/document/product/867/44987

## 使用时机

当用户提出以下需求时触发此技能：
- 需要比对两张人脸图片的相似度
- 需要判断两张照片中的人是否为同一人
- 需要对人脸进行1:1验证
- 涉及人脸比对、人脸相似度计算的任何场景

## 环境要求

- Python 3.6+
- 依赖：`tencentcloud-sdk-python`（通过 `pip install tencentcloud-sdk-python` 安装）
- 环境变量：
  - `TENCENTCLOUD_SECRET_ID`：腾讯云API密钥ID
  - `TENCENTCLOUD_SECRET_KEY`：腾讯云API密钥Key

## 使用方式

运行 `scripts/main.py` 脚本完成人脸比对。

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| --image-a | str | 是（与url-a二选一）| A图片本地文件路径（自动转Base64）或Base64字符串 |
| --url-a | str | 是（与image-a二选一）| A图片URL地址，优先级高于image-a |
| --image-b | str | 是（与url-b二选一）| B图片本地文件路径（自动转Base64）或Base64字符串 |
| --url-b | str | 是（与image-b二选一）| B图片URL地址，优先级高于image-b |
| --face-model-version | str | 否 | 算法版本："2.0" 或 "3.0"，默认 "3.0" |
| --quality-control | int | 否 | 图片质量控制：0(不控制)/1(低)/2(一般)/3(较高)/4(很高)，默认0 |
| --need-rotate-detection | int | 否 | 是否开启旋转识别：0(不开启)/1(开启)，默认0 |

### 图片输入规格

- **格式**：支持 PNG、JPG、JPEG、BMP，不支持 GIF
- **大小**：Base64 编码后不可超过 5MB
- **分辨率**：jpg格式长边不可超过4000像素，其他格式长边不可超过2000像素，短边不小于64像素
- **人脸要求**：若图片中包含多张人脸，默认选取置信度最高的人脸

### 输出格式

检测成功后返回 JSON 格式结果：

```json
{
  "Score": 87.5,
  "ScoreDesc": "高度相似，可认定为同一人（3.0版本）",
  "IsSamePerson": true,
  "FaceModelVersion": "3.0",
  "RequestId": "xxx"
}
```

### 相似度分数说明（3.0版本）

| 分数范围 | 误识率 | 建议判断 |
|----------|--------|----------|
| ≥ 40分 | 千分之一 | 疑似同一人 |
| ≥ 50分 | 万分之一 | 可认定为同一人（推荐阈值） |
| ≥ 60分 | 十万分之一 | 高度确信为同一人 |

### 相似度分数说明（2.0版本）

| 分数范围 | 误识率 | 建议判断 |
|----------|--------|----------|
| ≥ 70分 | 千分之一 | 疑似同一人 |
| ≥ 80分 | 万分之一 | 可认定为同一人（推荐阈值） |
| ≥ 90分 | 十万分之一 | 高度确信为同一人 |

### 调用示例

```bash
# 传入两张本地图片文件（自动转Base64）
python scripts/main.py --image-a ./face_a.jpg --image-b ./face_b.jpg

# 传入图片URL
python scripts/main.py --url-a "https://example.com/face_a.jpg" --url-b "https://example.com/face_b.jpg"

# 混合使用（A用本地文件，B用URL）
python scripts/main.py --image-a ./face_a.jpg --url-b "https://example.com/face_b.jpg"

# 指定算法版本和质量控制
python scripts/main.py --image-a ./face_a.jpg --image-b ./face_b.jpg --face-model-version 3.0 --quality-control 2

# 传入Base64字符串
python scripts/main.py --image-a "<base64_string_a>" --image-b "<base64_string_b>"
```
