---
name: tencentcloud-faceid-detectlivefaceaccurate
description: 腾讯云人脸静态活体检测高精度版(DetectLiveFaceAccurate)接口调用技能。当用户需要对人脸图片进行防翻拍活体检测时，应使用此技能。相比普通静态活体检测，高精度版增强了对高清屏幕、裁剪纸片、3D面具等攻击的防御能力，适用于移动端、PC端各类型场景的图片活体检验。支持图片Base64和图片URL两种输入方式。
---

# 腾讯云人脸静态活体检测（高精度版）(DetectLiveFaceAccurate)

## 用途

调用腾讯云人脸识别静态活体检测（高精度版）接口，对用户上传的静态图片进行防翻拍活体检测，以判断是否是翻拍图片。

核心能力：
- **高清屏幕攻击防御**：识别通过高清屏幕翻拍的图片
- **裁剪纸片攻击防御**：识别纸质打印照片翻拍
- **3D面具攻击防御**：识别3D面具等高级攻击手段
- **多场景支持**：满足移动端、PC端各类型场景的图片活体检验需求
- **多输入类型**：支持图片Base64和图片URL两种输入方式（传入本地文件时可自动识别并转为Base64）

官方文档：https://cloud.tencent.com/document/product/867/48501

## 使用时机

当用户提出以下需求时触发此技能：
- 需要检测人脸图片是否为翻拍照片
- 需要对用户上传的静态图片进行活体检测
- 需要判断图片是否来自真实人脸（非翻拍、非合成）
- 需要高精度的静态活体检测（相比普通静态活体检测精度更高）
- 涉及人脸防翻拍、静态活体检验的任何场景

## 环境要求

- Python 3.6+
- 依赖：`tencentcloud-sdk-python`（通过 `pip install tencentcloud-sdk-python` 安装）
- 环境变量：
  - `TENCENTCLOUD_SECRET_ID`：腾讯云API密钥ID
  - `TENCENTCLOUD_SECRET_KEY`：腾讯云API密钥Key

## 使用方式

运行 `scripts/main.py` 脚本完成人脸静态活体检测。

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| --image | str | 否 | 本地图片文件路径（自动转Base64）或Base64字符串，与 --url 二选一 |
| --url | str | 否 | 图片的URL地址，与 --image 二选一；若同时提供，优先使用URL |
| --face-model-version | str | 否 | 算法模型版本，目前支持"3.0"，默认"3.0" |
| --region | str | 否 | 腾讯云地域，默认为空 |

### 图片输入规格

- **格式**：支持PNG、JPG、JPEG、BMP，不支持GIF
- **分辨率**：jpg格式长边像素不可超过4000，其他格式长边像素不可超过2000
- **宽高比**：建议接近3:4，手机拍摄比例最佳
- **人脸尺寸**：人脸尺寸大于100×100像素
- **大小限制**：Base64编码后大小不可超过5MB

### 输出格式

检测成功后返回 JSON 格式结果：

```json
{
  "Score": 99,
  "ScoreDesc": "活体分数99，高于推荐阈值40，判断为真实人脸",
  "IsLive": true,
  "FaceModelVersion": "3.0",
  "RequestId": "xxx"
}
```

### 活体分数说明

| 分数范围 | 推荐阈值 | 判断结论 |
|----------|----------|----------|
| [0, 100] | 40（推荐） | Score ≥ 40 为真实人脸，Score < 40 为翻拍 |
| - | 可选阈值 | 5 / 10 / 40 / 70 / 90，根据业务安全需求选择 |

> 推荐阈值为40，分数越高代表越可能为真实人脸。

### 调用示例

```bash
# 传入本地图片文件（自动Base64编码）
python scripts/main.py --image ./face.jpg

# 传入图片URL
python scripts/main.py --url "http://example.com/face.jpg"

# 传入Base64字符串
python scripts/main.py --image "<base64_string>"

# 指定算法模型版本
python scripts/main.py --image ./face.jpg --face-model-version 3.0
```
