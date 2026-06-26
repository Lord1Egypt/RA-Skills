---
name: raise-ai-media
description: |
  RaiseAI 媒体生成工具集 - 生图、生视频、脚本生成、图片解析、视频解析。
  当用户提到以下任何关键词时必须触发此技能：生成图片、生成视频、图片生成、视频生成、脚本生成、
  图片解析、图生文、反推提示词、视频解析、视频脚本、图片生图、视频生视频、
  AI生图、AI生视频、AI创作、Media generation、image generation、video generation、
  text-to-image、text-to-video、图片转视频、一键成片。

  即使用户没有明确使用上述词汇，只要他们要求制作图片、视频、脚本，或从图片/视频中提取内容，都应使用此技能。

  ⚠️ 默认行为（重要）：用户没有明确要求"高质量"或"质感好"时，图片必须用 `image_generation` + `fast=false` + `resolution=HD`，视频必须用 `fast_video` + `resolution=HD`。不要擅自升级到 `image_generation_pro`，除非用户明确说了"高质量"、"效果好"、"质感好"等。
metadata:
  {
    "openclaw": {
      "requires": { "env": ["RAISE_AI_API_KEY"] },
      "optionalEnv": [],
      "primaryEnv": "RAISE_AI_API_KEY",
      "baseUrl": "https://ai.micrease.com",
      "homepage": "https://ai.micrease.com"
    }
  }
---

# RaiseAI 媒体生成工具集

## 核心约束

- **Base URL**: `https://ai.micrease.com`
- **认证**: `Authorization: {RAISE_AI_API_KEY}`，API Key 格式为 `sk-xxx`
- **所有生成任务均为异步**，提交后需要等待生成完成

> ⚠️ **API Key 配置**：用户可通过告诉 Agent「我的 RaiseAI API Key 是 xxx」自动完成配置（存储在环境变量中），或参考 `references/api-setup.md` 手动配置。

---

## 快速决策表

| 用户意图 | 接口 type 值 | 关键行为 |
|---|---|---|
| 「生成高质量图片」 | `image_generation_pro` | 效果更惊艳，需要等待 |
| 「生成图片」（用户无倾向） | `image_generation` + `fast=false` + `resolution=HD` | **默认**，专业模式，高清画质，需要等待 |
| 「编辑/修改这张图片」 | `image_generation` + `references` | 基于参考图修改，需要等待 |
| 「快速生成预览图」 | `image_generation` + `fast=true` | 快速预览，需要等待 |
| 「生成视频」（用户无倾向） | `fast_video` + `resolution=HD` | **默认**，快速模式，高清画质，需要等待 |
| 「生成视频脚本」 | `video_script` | 可传参考素材，需要等待 |
| 「这张图是怎么生成的」 | `image_prompt_extraction` | 反推提示词，需要等待 |
| 「这个视频的脚本是什么」 | `video_script_extraction` | 反推视频脚本，需要等待 |

---

## 通用工作流

每个生成任务都遵循以下流程：

### 1. 提交请求

```
POST /open/api/v1/resource/aigc/generation
```

Header:
```
Authorization: {RAISE_AI_API_KEY}
Content-Type: application/json; charset=utf-8
```

根据用户意图选择正确的 `type` 值，构造请求体。详细参数参考对应 reference 文档。

收到响应后提取 **任务 ID**（`data` 字段）。

### references 参数限制

| 接口 | references 上限 | 备注 |
|---|---|---|
| `image_generation` / `image_generation_pro` | 10 张 | 融合参考图风格时使用 |
| `video_script` | 15 个 | 参考素材时使用 |
| `fast_video` / `pro_video` | 不支持 | 使用 `startFrame` / `endFrame` 代替 |
| `image_prompt_extraction` | 不支持 | 使用 `url` 单个传 |
| `video_script_extraction` | 不支持 | 使用 `url` 单个传 |

### 2. 等待生成

每隔 **5 秒** 调用一次查询接口，直到生成完成或失败。

**对用户这样说**：提交后告诉用户"好的，正在为你生成中，请稍等~"，不要提及技术细节（如"轮询"、"接口"、"任务 ID"等）。如果用户没有回复，默默轮询即可，不要反复告知用户"还在生成中"。

> ⚠️ **超时处理**：如果等待超过 5 分钟仍未完成，告诉用户"抱歉，这次生成花费的时间比较长，你可以稍后再来找我查看结果"，不再继续等待。

### 3. 通知用户结果 ⭐

**这是最关键的步骤**。生成完成后，必须将结果**完整告知用户**：

| 任务类型 | 成功后从哪取结果 | 如何告知用户 |
|---|---|---|
| 图片生成 | `ImageTask.urls` → `List<String>` | **直接展示所有图片链接**，告诉用户"图片已生成好啦！链接有效期约 24 小时，记得及时下载保存哦~" |
| 视频生成 | `VideoTask.urls` → `List<String>` | **直接展示所有视频链接** |
| 脚本生成 | `ScriptTask.content` → `List<Map<String, Any?>>` | 每个元素含 `segment`、`timeRange`、`description`、`narration` 等字段，**完整展示脚本内容** |
| 图片反推 | `PromptTask.content` → `List<Map<String, Any?>>` | 提示词文本通常在 `prompt` 字段，**直接展示给用户**，告诉他们"这就是这张图的提示词，可以用来生成风格相似的图~" |
| 视频反推 | `PromptTask.content` → `List<Map<String, Any?>>` | **完整展示脚本内容**（含 segment、timeRange、description、narration） |

> 💡 失败时，用友好的语气告知用户（如"哎呀，这次生成失败了…"），从 `failReason` 读取原因，并给出具体修改建议，不要只说"生成失败"而不解释原因。

---

## 决策指南

### 图片生成选型

> ⚠️ **强制规则**：除非用户明确说"高质量"、"效果好"、"质感好"，否则一律使用默认选项，不要擅自换成 `image_generation_pro`。

- **默认（用户无倾向）→ 必须用这个**：`image_generation` + `fast=false` + `resolution=HD`
- 用户说"高质量/效果好/质感好" → `image_generation_pro`（效果更惊艳，消耗积分多）
- 用户上传参考图并说"换背景/换主体/编辑" → `image_generation` + `references`
- 用户上传参考图并说"融合风格/参考这张图生成" → `image_generation_pro` + `references`
- 用户说"快速预览/先看看效果" → `image_generation` + `fast=true`

### 视频生成选型

> ⚠️ **强制规则**：除非用户有明确的首帧/尾帧控制需求，否则一律使用默认选项，不要擅自换成 `pro_video`。

- **默认（用户无倾向）→ 必须用这个**：`fast_video` + `resolution=HD`
- 用户说"首帧控制"（不需要尾帧） → `fast_video` + `startFrame`
- 用户说"首帧+尾帧控制" → `pro_video`（支持尾帧）
- 纯文字生视频（无图片控制） → `fast_video`，不传 `startFrame`

---

## Reference 文档索引

需要详细参数说明时，读取对应文档：

| 文档 | 内容 |
|---|---|
| `references/api-setup.md` | API Key 配置、认证 Header |
| `references/image-generation.md` | 图片生成（image_generation_pro/image_generation）完整参数与响应 |
| `references/video-generation.md` | 视频生成（fast_video/pro_video）完整参数与响应 |
| `references/script-generation.md` | 视频脚本生成完整参数与响应 |
| `references/prompt-extraction.md` | 图片/视频反推提示词完整参数与响应 |
| `references/polling-and-errors.md` | 轮询机制、状态说明、错误处理 |

---

## 快速示例

### 默认专业模式生成图片

1. 提交生成请求: `{"type":"image_generation","prompt":"竹林深处，雾气缭绕","ratio":"9:16","fast":false,"resolution":"HD"}`
2. 等待生成完成（每隔 5 秒检查一次）
3. **通知用户**: 从 `urls` 获取完整图片链接，提示链接会过期
