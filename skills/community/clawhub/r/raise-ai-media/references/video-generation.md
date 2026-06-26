# 视频生成 API

## 接口

```
POST /open/api/v1/resource/aigc/generation
```

---

## 两种模式

| 模式 | type 值 | 分辨率 | 帧控制 | 说明 |
|---|---|---|---|---|
| 快速模式 | `fast_video` | 480p / 720p / 1080p | 仅支持**首帧** | 适合快速预览，支持文生视频 |
| 专业模式 | `pro_video` | 480p / 720p / 1080p | 支持**首帧+尾帧** | 适合高质量输出，支持首帧尾帧控制 |

> 💡 **选择建议**：
> - **默认**（用户无倾向）：`fast_video` + `resolution=HD`（快速模式，高清画质）
> - 需要**首帧控制**（不需尾帧） → `fast_video` + `startFrame`
> - 需要**首帧+尾帧控制** → `pro_video`（支持首帧+尾帧）
> - 两种模式都支持**文生视频**（不传 startFrame 时）

---

## 请求示例

**示例 1：快速生成视频（适合预览）**

```json
{
  "type": "fast_video",
  "prompt": "海浪轻轻拍打金色沙滩，日出时分，天空呈现橙红色渐变",
  "resolution": "HD"
}
```

**示例 2：快速模式 + 首帧（文生视频 + 首帧控制）**

```json
{
  "type": "fast_video",
  "prompt": "海浪轻轻拍打金色沙滩，日出时分",
  "startFrame": "https://example.com/start.jpg",
  "resolution": "HD"
}
```

**示例 3：专业模式 + 首位帧（高质量，支持首尾帧）**

```json
{
  "type": "pro_video",
  "prompt": "城市街景，车流穿梭，夜晚灯光璀璨",
  "startFrame": "https://example.com/start.jpg",
  "endFrame": "https://example.com/end.jpg",
  "resolution": "HD"
}
```

---

## 参数说明

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| type | string | 是 | `fast_video` = 快速模式，`pro_video` = 专业模式（支持尾帧） |
| prompt | string | 是 | 视频内容描述，越详细越好 |
| startFrame | string | 否 | 起始帧图片 URL（必须是可公开访问的图片链接）。传此字段则视频以此图作为第 1 帧；不传则为纯文字生视频 |
| endFrame | string | 否 | 结束帧图片 URL（仅 pro_video 支持）。指定时**必须同时指定 startFrame** |
| resolution | string | 否 | 分辨率：`SD`（480p）、`HD`（720p，默认）、`UHD`（1080p） |

---

## 响应格式

提交后返回任务 ID：

```json
{
  "code": 200,
  "msg": "success",
  "data": 789012345
}
```

---

## 轮询结果

调用任务状态接口：

```
POST /open/api/v1/resource/aigc/task/status
```

传入任务 ID 列表：

```json
[789012345]
```

### 成功示例

```json
{
  "code": 200,
  "data": [{
    "opsId": 789012345,
    "status": "COMPLETED",
    "failReason": null,
    "urls": [
      "https://xxx.aliyuncs.com/xxx.mp4?Expires=xxx&OSSAccessKeyId=xxx&Signature=xxx",
      "https://xxx.aliyuncs.com/xxx2.mp4?Expires=xxx&OSSAccessKeyId=xxx&Signature=xxx"
    ]
  }]
}
```

> ⚠️ **重要**：`urls` 返回的是带签名的临时链接，**必须完整返回给用户**。链接有效期约 **24 小时**，建议用户及时下载保存。
