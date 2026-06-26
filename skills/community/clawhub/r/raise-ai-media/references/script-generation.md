# 视频脚本生成 API

## 接口

```
POST /open/api/v1/resource/aigc/generation
```

---

## 功能说明

根据产品图片或视频素材，AI 自动生成视频拍摄脚本（旁白、画面描述、时间轴）。

> 💡 **小技巧**：传 1 个视频做参考，或传多张产品图片，AI 会结合素材内容生成更贴合的脚本。

---

## 请求示例

```json
{
  "type": "video_script",
  "prompt": "生成一个 60 秒的产品宣传视频脚本，包含开场、产品展示、结尾三部分",
  "references": [
    "https://example.com/product1.jpg",
    "https://example.com/product2.jpg"
  ]
}
```

---

## 参数说明

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| type | string | 是 | 固定填 `video_script` |
| prompt | string | 是 | 脚本要求，如：视频时长、风格、内容重点、场景数量等 |
| references | string[] | 否 | 参考素材 URL（图片或视频），最多传 15 个 |

---

## 响应格式

提交后返回任务 ID：

```json
{
  "code": 200,
  "msg": "success",
  "data": 456789012
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
[456789012]
```

### 成功示例

```json
{
  "code": 200,
  "data": [{
    "opsId": 456789012,
    "status": "COMPLETED",
    "failReason": null,
    "content": [
      {
        "segment": "开场",
        "timeRange": "0-5秒",
        "description": "产品全景展示",
        "narration": "欢迎来到今天的..."
      },
      {
        "segment": "产品展示",
        "timeRange": "5-50秒",
        "description": "产品细节特写",
        "narration": "首先让我们看看..."
      }
    ]
  }]
}
```

`status=COMPLETED` 后从 `content` 获取脚本内容。`content` 是一个结构化列表，每个元素包含 `segment`（段落名）、`timeRange`（时间范围）、`description`（画面描述）、`narration`（旁白）等字段。将脚本完整返回给用户。
