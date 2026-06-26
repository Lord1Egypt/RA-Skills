---
name: tencentcloud-faceid-detectaifakefaces
description: 腾讯云AI人脸防护盾(DetectAIFakeFaces)接口调用技能。当用户需要对人脸图片或视频进行防攻击检测时,应使用此技能。可针对性有效识别高仿真的AIGC换脸、高清翻拍、批量黑产攻击、水印等攻击痕迹,增强对图片和视频的防伪安全能力。支持图片Base64和视频Base64两种输入方式。
---

# 腾讯云 AI 人脸防护盾 (DetectAIFakeFaces)

## 用途
调用腾讯云人脸核身 AI 人脸防护盾接口，基于多模态的 AI 大模型算法，提供对人脸图片、视频的防攻击检测能力。

## 注意事项
请确保您委托本服务处理人脸等个人信息已获得个人信息主体合法、有效的同意或具备其他的合法性基础，本服务的相关具体事项以本服务官网所载服务协议约定为准。

核心能力：
- **AIGC换脸检测**：识别高仿真的 AI 生成/合成换脸攻击
- **翻拍检测**：识别高清翻拍攻击痕迹
- **黑产攻击检测**：识别批量黑产攻击行为
- **水印检测**：识别图片/视频中的水印等攻击痕迹
- **多输入类型**：支持图片 Base64、视频 Base64 两种输入方式，传入本地文件时可自动识别类型并转为 Base64（图片仅支持 jpg/png，视频仅支持 mp4/avi/flv）

官方文档：https://cloud.tencent.com/document/product/1007/101561

## 使用时机

当用户提出以下需求时触发此技能：
- 需要检测人脸图片是否为 AI 合成/换脸
- 需要检测人脸图片是否为翻拍照片
- 需要检测人脸视频是否存在攻击痕迹
- 需要对人脸图片/视频进行防伪安全检测
- 涉及人脸防攻击、防伪检测的任何场景

## 环境要求

- Python 3.6+
- 依赖：`tencentcloud-sdk-python`（通过 `pip install tencentcloud-sdk-python` 安装）
- 环境变量：
  - `TENCENTCLOUD_SECRET_ID`：腾讯云API密钥ID
  - `TENCENTCLOUD_SECRET_KEY`：腾讯云API密钥Key

## 使用方式

运行 `scripts/main.py` 脚本完成 AI 人脸防护盾检测。

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| FaceInput | str | 是 | 本地图片/视频文件路径（自动转 Base64）或 Base64 字符串 |
| FaceInputType | int | 否 | 输入类型：`1`(图片) / `2`(视频)。传入本地文件时可省略，自动根据扩展名识别 |

### 图片输入规格

- **格式**：仅支持 jpg、png 格式
- **分辨率**：建议整体图像 480×640，脸部大小在 100×100 以上
- **拍摄要求**：由手机前置摄像头拍摄
- **大小限制**：Base64 编码后的图片数据大小建议不超过 3MB，最大不可超过 10MB
- **编码规范**：请使用标准的 Base64 编码方式（带=补位），编码规范参考 RFC4648

### 视频输入规格

- **格式**：仅支持 mp4、avi、flv 格式
- **时长**：建议 2～5 秒，最大不可超过 20 秒
- **分辨率**：建议 480×640（最大支持 720p）
- **帧率**：建议 25fps～30fps
- **拍摄要求**：由手机前置摄像头拍摄
- **大小限制**：Base64 编码后的大小建议在 8MB 以内，最大不可超过 10MB
- **编码规范**：请使用标准的 Base64 编码方式（带=补位），编码规范参考 RFC4648

### 输出格式

检测成功后返回 JSON 格式结果：

```json
{
  "AttackRiskLevel": "Low",
  "AttackRiskDetailInfos": [
    {
      "Type": "换脸攻击",
      "RiskLevel": "Low"
    }
  ],
  "RequestId": "xxx"
}
```

### 风险等级说明

| 风险等级 | 含义 |
|----------|------|
| Low | 低风险，图片/视频为正常人脸 |
| Mid | 中风险，存在一定攻击嫌疑 |
| High | 高风险，极有可能为攻击行为 |

### 攻击类型说明

| 攻击类型 | 含义 |
|----------|------|
| 换脸攻击 | 检测到 AI 换脸/合成痕迹 |
| 翻拍攻击 | 检测到屏幕翻拍痕迹 |
| 活体伪造 | 检测到活体伪造痕迹 |
| 黑产攻击 | 检测到批量黑产攻击痕迹 |
| 水印攻击 | 检测到水印攻击痕迹 |

### 调用示例

```bash
# 传入本地图片文件(自动识别类型并Base64编码)
python scripts/main.py --face-input ./face.jpg

# 传入本地视频文件(自动识别类型并Base64编码)
python scripts/main.py --face-input ./face_video.mp4

# 手动指定类型 + Base64字符串
python scripts/main.py --face-input-type 1 --face-input "<base64_string>"

# 手动指定类型 + 视频Base64字符串
python scripts/main.py --face-input-type 2 --face-input "<base64_string>"
```
