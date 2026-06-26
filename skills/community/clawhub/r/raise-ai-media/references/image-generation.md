# 图片生成 API

## 接口

```
POST /open/api/v1/resource/aigc/generation
```

---

## 两种模式

| 模式 | type 值 | 适用场景 | 生成数量 |
|---|---|---|---|
| generation_pro 模式 | `image_generation_pro` | **高质量、质感好**的图片，适合创意探索、素材收集；支持传 references 融合参考图风格（生成时参考其风格，**不是在其基础上编辑**），仍生成 4 张，**消耗积分较多** | 通常 4 张，数量不可自定义 |
| generation 模式 | `image_generation` | 主要用于**图片编辑**（换背景、换风格等），也支持纯文字生图；传 references 则**在参考图基础上直接编辑修改**，**消耗积分较少** | 1 张 |

> 💡 **选择建议**：
> - **默认**（用户无倾向）：`image_generation` + `fast=false` + `resolution=HD`（消耗积分少，效果也不错）
> - 需要**高质量、质感好**的图片（不差积分） → `image_generation_pro`（效果更惊艳，消耗积分多）
> - 需要**基于参考图修改/编辑**（如换背景、换主体） → `image_generation` + `references`
> - 需要**融合参考图风格**（如参考某图的配色/构图生成新图，不差积分） → `image_generation_pro` + `references`
> - 需要**快速预览** → `image_generation` + `fast=true`

---

## 请求示例

**示例 1：generation_pro 模式（高质量，消耗积分多）**

```json
{
  "type": "image_generation_pro",
  "prompt": "一只在海边奔跑的金毛犬，夕阳西下，电影感",
  "ratio": "16:9"
}
```

**示例 2：generation 模式 + 快速预览**

```json
{
  "type": "image_generation",
  "prompt": "一只在海边奔跑的金毛犬，夕阳西下，电影感",
  "ratio": "9:16",
  "fast": true
}
```

**示例 3：generation 模式 + 高质量**

```json
{
  "type": "image_generation",
  "prompt": "一只在海边奔跑的金毛犬，夕阳西下，电影感，光影细节丰富",
  "ratio": "16:9",
  "fast": false,
  "resolution": "4K"
}
```

**示例 4：generation_pro 模式 + 参考图（融合风格，消耗积分多）**

```json
{
  "type": "image_generation_pro",
  "prompt": "赛博朋克风格的城市夜景，霓虹灯光",
  "ratio": "16:9",
  "references": [
    "https://example.com/ref1.jpg",
    "https://example.com/ref2.jpg"
  ]
}
```

---

## 参数说明

### image_generation_pro 参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| type | string | 是 | 固定填 `image_generation_pro` |
| prompt | string | 是 | 图片描述，中文或英文均可，描述越详细效果越好 |
| ratio | string | 否 | 图片比例：`9:16`（竖图）、`3:4`、`1:1`（正方形，默认）、`4:3`、`16:9`（横图） |
| references | string[] | 否 | 参考图片 URL 列表，AI 会融合参考图的风格，最多传 10 张 |

### image_generation 参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| type | string | 是 | 固定填 `image_generation` |
| prompt | string | 是 | 图片描述，中文或英文均可，描述越详细效果越好 |
| ratio | string | 否 | 图片比例：`9:16`（竖图）、`3:4`、`1:1`（正方形，默认）、`4:3`、`16:9`（横图） |
| references | string[] | 否 | 参考图片 URL 列表，不传则纯文字生图，传了则基于参考图修改；最多传 10 张 |
| fast | bool | 否 | `true` = 快速模式，速度快但效果一般；`false`（默认） = 专业模式，效果更好。**建议**：需要快速看效果时用 `true`，最终交付用 `false` |
| resolution | string | 否 | 图片分辨率：`HD`（≈1k，默认）、`UHD`（≈2k）、`4K`（≈4k）。分辨率越高生成越慢 |

---

## 响应格式

提交后返回任务 ID：

```json
{
  "code": 200,
  "msg": "success",
  "data": 123456789
}
```

返回的数字是**任务 ID**，用于后续查询生成结果。图片生成需要 10 秒~3 分钟。

---

## 轮询结果

调用任务状态接口：

```
POST /open/api/v1/resource/aigc/task/status
```

传入任务 ID 列表：

```json
[123456789]
```

### 处理中示例

```json
{
  "code": 200,
  "data": [{
    "opsId": 123456789,
    "status": "PROCESSING",
    "failReason": null
  }]
}
```

### 成功示例

```json
{
  "code": 200,
  "data": [{
    "opsId": 123456789,
    "status": "COMPLETED",
    "failReason": null,
    "urls": [
      "https://xxx.aliyuncs.com/xxx.jpg?Expires=xxx&OSSAccessKeyId=xxx&Signature=xxx",
      "https://xxx.aliyuncs.com/xxx2.jpg?Expires=xxx&OSSAccessKeyId=xxx&Signature=xxx"
    ]
  }]
}
```

> ⚠️ **重要**：`urls` 返回的是完整的带签名的临时链接（含 `Expires`、`OSSAccessKeyId`、`Signature` 参数），**必须完整返回给用户**，直接粘贴到浏览器即可访问。链接有效期约 **24 小时**，建议用户及时下载保存。

> 💡 系统返回的图片数量由 API 决定，全部展示给用户，让用户选择最喜欢的一张。

### 失败示例

```json
{
  "code": 200,
  "data": [{
    "opsId": 123456789,
    "status": "FAILED",
    "failReason": "内容包含敏感词"
  }]
}
```
