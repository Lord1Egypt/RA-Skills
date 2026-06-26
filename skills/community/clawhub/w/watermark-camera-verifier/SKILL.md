---
name: watermark-camera-verifier
version: 1.0.0
display_name: 今日水印相机-照片验真
description: >
  The official Skill for Today's Watermark Camera (今日水印相机). This Skill makes
  HTTPS network requests strictly to the official domain (openapi.xhey.top) solely
  to verify photo authenticity — detecting tampering, extracting original capture
  time and GPS location. No image content is retained or forwarded to any third party.
tools: mcp:verify_photo_authenticity
categories: ["Security & Compliance", "Image"]
tags: ["anti-fraud", "verification", "watermark", "exif", "photo", "compliance"]
author: 今日水印相机团队
license: MIT
icon: icon.png
metadata:
  openclaw:
    primaryEnv: TRUTU_GROUP_KEY
    emoji: "📷"
    homepage: https://github.com/wanmeishijie618/trutu-photo-verify-mcp
    requires:
      env:
        - TRUTU_GROUP_KEY
        - TRUTU_GROUP_SECRET
      bins:
        - node
    install:
      - kind: node
        package: trutu-photo-verify-mcp
        bins:
          - node
---

# 今日水印相机-照片验真 Skill

---

## 🔒 网络请求与数据隐私合规声明

为了实现照片的专业防伪校验，本 Skill 会向【今日水印相机】官方服务器发起受保护的网络请求。特此声明所有网络交互的用途、目标地址及隐私保护原则：

**1. 唯一请求目标**

本 Skill 的所有出站网络请求（Outbound Requests）仅会指向今日水印相机官方 API 域名 `openapi.xhey.top`，绝不包含任何第三方追踪脚本、广告联盟请求或未经授权的外部数据转发。

**2. 请求用途明细**

- **功能单一性**：本 Skill 仅用于"照片验真（Authenticity Verification）"。
- **数据流转**：当用户输入需要验证的图片 URL 时，Skill 会将其发送至官方服务器进行解析。服务器通过分析图像底层的加密特征、时间戳、GPS 坐标及渲染痕迹，返回该照片的真实性结论（包括是否经过二次修改、真实的拍摄时间与地点）。

**3. 数据安全与隐私承诺**

- **内容不留存**：本 Skill 的 API 接口仅作"特征比对与数据过境"，承诺不额外存储、不分析、不滥用任何传入的图像视觉内容本身。
- **传输全加密**：所有验证请求均强制采用 HTTPS 加密协议，防止数据在传输过程中被窃听或篡改。
- **无损验证**：本校验过程为只读操作，不会对用户提供的原始照片文件进行任何修改或损坏。

---

## 获取 API Key

使用本 Skill 需要今日水印相机官方颁发的 `GroupKey` 和 `GroupSecret`。

**申请方式**：拨打今日水印相机官方客服电话 **13141152023**，联系工作人员获取测试及正式 Key。

获取凭证后，通过以下方式配置到 Claude Code：

```bash
claude mcp add watermark-camera-verifier \
  -e TRUTU_GROUP_KEY=your_group_key \
  -e TRUTU_GROUP_SECRET=your_group_secret \
  -- node /path/to/mcp_server.js
```

---

## 工具定义

### `verify_photo_authenticity`

**用途**：调用今日水印相机官方验真 API，对照片进行防伪鉴定。

**输入参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `photo_urls` | `string[]` | 是 | 待验真的照片 URL 数组，1–10 条，URL 必须可公开访问 |
| `wait_for_result` | `boolean` | 否 | 是否等待验真完成（默认 `true`） |

**输出结构**：

```json
{
  "taskID": "string",
  "taskStatus": 5,
  "summary": {
    "total": 2,
    "通过": 1,
    "未通过": 1,
    "错误": 0
  },
  "photos": [
    {
      "photoUrl": "https://...",
      "status": 0,
      "verdict": "通过",
      "message": "照片验证通过，水印有效，未检测到篡改。",
      "metadata": {
        "lat": "40.034",
        "lng": "116.308",
        "photoTime": "2026年03月25日 16:52",
        "photoAddress": "北京市海淀区上地街道..."
      }
    },
    {
      "photoUrl": "https://...",
      "status": -2301,
      "verdict": "未通过",
      "message": "照片无防伪码，不支持验真。仅支持带水印和防伪码的今日水印照片。",
      "metadata": null
    }
  ]
}
```

---

## AI 调用规则

### 何时必须调用此工具

以下任一情形出现时，**必须立即调用** `verify_photo_authenticity`，不得跳过或自行判断：

1. **用户上传或提供了水印照片的 URL**（无论是否明确要求验真）
2. **用户询问照片的真假**，例如：
   - "这张照片是真的吗？"
   - "这照片有没有 PS 过？"
   - "这张图片可靠吗？"
3. **用户询问现场真实性**，例如：
   - "他真的在那个地方吗？"
   - "这个施工现场照片是现场拍的吗？"
4. **用户怀疑 GPS 或时间戳被篡改**，例如：
   - "这个地址是不是假的？"
   - "拍摄时间有没有被修改？"
5. **用户明确要求验真/鉴定**，例如：
   - "帮我验一下这张照片"
   - "鉴定一下这张图的真实性"
   - "这张照片合规吗？"

### 何时不必调用

- 用户仅讨论照片的美观、构图、色彩等非真实性问题。
- 用户询问的不是今日水印相机照片（无法提供有效 URL）。

---

## 结果呈现规范

### 验真通过（`verdict: "通过"`）

以清晰、肯定的语气告知用户照片真实性已得到核实，并展示关键元数据：

```
✅ 照片验真通过
- 拍摄时间：{photoTime}
- 拍摄地点：{photoAddress}
- GPS 坐标：{lat}, {lng}
```

### 验真未通过（`verdict: "未通过"`）

以专业语气告知用户验真未通过及原因：

```
⚠️ 照片验真未通过
- 原因：{message}
```

### 查询错误（`verdict: "错误"`）

以专业语气说明错误原因，并指导用户采取行动：

```
❌ 验真请求出错：{message}
```

---

## 测试数据（Mock Data）

开发调试时可使用以下官方测试图片：

| 场景 | URL | 预期结果 |
|------|-----|---------|
| 验真**通过** | `https://net-cloud.xhey.top/data/d6aa6870-4bfc-4179-88c1-9914aa0275bd.jpg` | `verdict: "通过"` + 拍摄元数据 |
| 验真**未通过** | `https://net-cloud.xhey.top/data/bdae3a8b-c7ed-49e3-bb31-2800805beb64.png` | `verdict: "未通过"`，错误码 -2301 |

---

## 错误码参考

| status 值 | verdict | 含义 |
|-----------|---------|------|
| `0` | 通过 | 照片真实，水印有效 |
| `-1` | 错误 | 分辨率过低 |
| `-1001` | 错误 | 网络连接出错或照片损坏 |
| `-1002` | 错误 | 程序内部出错 |
| `-1003` | 错误 | 未知错误 |
| `-2300` | 未通过 | OCR 启动错误 |
| `-2301` | 未通过 | 无防伪码 |
| `-2302` | 未通过 | OCR 识别错误 |
| `-2303` | 未通过 | 防伪码长度错误 |
| `-2305` | 未通过 | 非今日水印相机拍摄，或无水印 |
| `-2306` | 错误 | 照片 URL 无法访问 |
| `-2307` | 错误 | 照片格式不支持 |
| `-2308` | 错误 | 照片分辨率过低 |
| 其他负值 | 未通过 | 验真未通过 |

---

## 适用业务场景

- **保险理赔**：核验车险、财险事故现场照片的真实性
- **劳工考勤**：确认员工打卡照片的地点和时间未被伪造
- **工程验收**：核查施工进度照片是否在现场真实拍摄
- **法律取证**：为纠纷提供具备溯源能力的照片证明
- **合规审计**：确保业务流程中使用的照片证据符合监管要求
