---
name: seedance2-video-gen
description: >
  Seedance 2.0 AI 视频生成技能。根据用户描述（文字/图片/视频/音频），
  自动生成 Seedance 2.0 API 调用参数，支持文生视频、图生视频、参考视频三种模式。
  支持 @素材名 语法控制角色、镜头、动作、声音。
  触发词：生成视频、制作视频、AI视频、图生视频、文生视频、视频生成
metadata:
  author: Anna
  version: 1.0.0
  language: zh-CN
  models:
    - seedance-2.0-text-to-video
    - seedance-2.0-image-to-video
    - seedance-2.0-reference-to-video
    - seedance-2.0-fast-text-to-video
    - seedance-2.0-fast-image-to-video
    - seedance-2.0-fast-reference-to-video
---

# Seedance 2.0 视频生成技能

> 版本：1.0.0
> API 来源：EvoLink.ai
> 文档：https://seedance2api.app

---

## 核心能力

1. **理解需求** → 选择合适的模型（文生视频/图生视频/参考视频）
2. **构建 Prompt** → 使用 @素材名 语法精确控制内容
3. **生成 API 参数** → 输出符合 EvoLink API 规范的 JSON
4. **提供完整调用示例** → 附 curl / fetch / Python 代码

---

## 模型选择指南

| 用户需求 | 推荐模型 |
|---------|---------|
| 纯文字描述生成视频 | `seedance-2.0-text-to-video` |
| 一张图动画化 | `seedance-2.0-image-to-video` |
| 多模态参考（图+视频+音频组合）| `seedance-2.0-reference-to-video` |
| 快速迭代测试 | `*-fast-*` 系列（更快）|

---

## API 基础信息

**接口地址：**
```
POST https://api.evolink.ai/v1/videos/generations
GET  https://api.evolink.ai/v1/tasks/{task_id}
```

**认证：** `Authorization: Bearer $SEEDANCE_API_KEY`

**环境变量：** `SEEDANCE_API_KEY`（需用户在 EvoLink.ai 注册获取）

---

## 工作流程

### Step 1：理解用户需求

**必问信息（如未提供则推断）：**
- 内容主题（人物/产品/场景/抽象概念）
- 是否需要参考素材（图/视频/音频）
- 视频时长（4-15秒，默认5秒）
- 画面比例（16:9 / 9:16 / 1:1 / 4:3 / 3:4 / 21:9）
- 是否需要音效

**判断模型类型：**
- 只有文字 → Text-to-Video
- 有1-2张参考图 → Image-to-Video
- 有图+视频/音频/多图 → Reference-to-Video

### Step 2：构建 Prompt（@素材名语法）

**基础规则：**
```
@image1  = 第1张参考图（人物外观/场景/产品）
@video1  = 第1个参考视频（镜头运动/角色动作）
@video2  = 第2个参考视频（辅助镜头/动作）
@audio1  = 第1个参考音频（背景音乐/音效）
```

**常用写法：**
```
@image1 as the first frame  # 指定首帧
Reference camera movement from @video1  # 参考镜头
Reference character action from @video1  # 参考动作
Background BGM references @audio1  # 背景音乐
Extend @video1 by 5s  # 视频延长
```

### Step 3：生成 API 调用参数

**Text-to-Video：**
```json
{
  "model": "seedance-2.0-text-to-video",
  "prompt": "中文或英文 prompt",
  "duration": 5,
  "quality": "720p",
  "aspect_ratio": "16:9",
  "generate_audio": true
}
```

**Image-to-Video（1张图）：**
```json
{
  "model": "seedance-2.0-image-to-video",
  "prompt": "@image1 as the first frame, ...",
  "image_urls": ["https://..."],
  "duration": 5,
  "quality": "720p",
  "aspect_ratio": "16:9",
  "generate_audio": true
}
```

**Reference-to-Video（多模态）：**
```json
{
  "model": "seedance-2.0-reference-to-video",
  "prompt": "@image1 as the first frame, @video1 as camera reference, ...",
  "image_urls": ["https://..."],
  "video_urls": ["https://..."],
  "audio_urls": ["https://..."],
  "duration": 5,
  "quality": "720p",
  "aspect_ratio": "16:9",
  "generate_audio": true
}
```

### Step 4：输出完整调用示例

提供 curl / Python / JavaScript 三种调用方式。

---

## 输入规格

| 类型 | 格式 | 数量 | 单文件限制 |
|------|------|------|-----------|
| 图片 | jpeg, png, webp, bmp, tiff, gif | ≤9张 | <30MB |
| 视频 | mp4, mov | ≤3个 | <50MB |
| 音频 | mp3, wav | ≤3个 | <15MB |

**总上限：** ≤12个文件（图+视频+音频）

---

## 输出规格

| 参数 | 可选值 |
|------|--------|
| 时长 | 4-15秒，或 -1（智能时长） |
| 分辨率 | 480p / 720p |
| 比例 | 16:9 / 9:16 / 1:1 / 4:3 / 3:4 / 21:9 / adaptive |
| 音效 | generate_audio: true（含音效/配乐） |

**视频链接有效期：** 24小时

---

## 价格参考

| 分辨率 | 标准价格 |
|--------|---------|
| 480p | 4.63 credits/秒 |
| 720p | 10.00 credits/秒 |

（音频生成不额外收费）

---

## 注意事项

1. **合规**：不支持写实真人脸，建议使用插画/AI虚拟角色
2. **镜头控制**：镜头运动需通过 @video1 参考提供，纯文字描述镜头效果不稳定
3. **视频延长**：Extend 时 prompt 需描述原视频最后一帧的状态作为起点
4. **One-Shot 写法**：结尾必须加 "No scene cuts throughout, one continuous shot."
5. **长视频分段**：10秒以上建议用时间轴分段：`0-3s: ... / 3-6s: ...`

---

## 相关资源

- API 文档：https://seedance2api.app
- 获取 API Key：https://evolink.ai/signup
- Prompt 案例库：prompts/
- 官方用例参考：cases/
