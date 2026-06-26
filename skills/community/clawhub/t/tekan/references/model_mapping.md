# 模型名称映射规则

本文件定义了 API 模型名称与用户展示名称之间的映射关系。

## 核心规则

1. **构造命令时**：始终使用 `API 名称`（即 `--model` 参数的值）
2. **与用户沟通时**：始终使用 `展示名称`（中文名）
3. **用户说出展示名称时**：自动识别并映射为对应的 API 名称
4. **标记为「禁止使用」的模型**：不得向用户推荐，也不得主动使用

---

## 禁止使用的模型

以下模型不得推荐、不得使用。即使 `list-models` 返回了它们，也应忽略。

| API 名称 | 原因 |
|----------|------|
| `Lite` | 已下线 |
| `Pro` | 已下线 |
| `Plus` | 已下线 |
| `Best` | 已下线 |

---

## 视频模型映射

### 图生视频 / 文生视频 / Omni 参考

| API 名称 | 展示名称 | 供应商展示名 |
|----------|---------|-------------|
| `Standard` | 地表最强模型S2.0-白名单版（支持上传真人图） | seedance |
| `Fast` | 地表最强模型S2.0 Fast-白名单版（支持上传真人图） | seedance |
| `Seedance 1.5 Pro` | Seedance 1.5 Pro | seedance |
| `Seedance 1.0 Pro` | Seedance 1.0 Pro | seedance |
| `Seedance 1.0 Pro Fast` | Seedance 1.0 Pro Fast | seedance |
| `Kling V3` | 可灵 V3 | 可灵 |
| `Kling V3 Reference Video` | 可灵 V3 Reference Video | 可灵 |
| `Kling O3` | 可灵 O3 | 可灵 |
| `Kling O3 Reference-to-Video` | 可灵 O3 Reference-to-Video | 可灵 |
| `Kling 2.6` | 可灵 2.6 | 可灵 |
| `Kling O1 Reference-to-Video` | 可灵 O1 Reference-to-Video | 可灵 |
| `Kling 2.5 Turbo Pro` | 可灵 2.5 Turbo Pro | 可灵 |
| `Kling 2.5 Turbo Std` | 可灵 2.5 Turbo Std | 可灵 |
| `Sora 2` | 拟真世界模型 V2 | 拟真世界模型 |
| `Sora 2 Pro` | 拟真世界模型 2 Pro | 拟真世界模型 |
| `Veo 3.1` | 电影级画质模型 V3.1 | 电影级画质模型 |
| `Veo 3.1 Reference to video` | 电影级画质模型 V3.1 Reference to video | 电影级画质模型 |
| `Veo 3.1 Fast` | 电影级画质模型 V3.1 fast | 电影级画质模型 |
| `Veo 3.1 Fast Reference to video` | 电影级画质模型 V3.1 fast Reference to video | 电影级画质模型 |
| `MiniMax-Hailuo-02` | 海螺 V2 | 海螺 |
| `MiniMax-Hailuo-2.3` | 海螺 V2.3 | 海螺 |
| `MiniMax-Hailuo-2.3-Fast` | 海螺-2.3-Fast | 海螺 |
| `Vidu Q3 Pro` | Vidu Q3 Pro | Vidu |
| `Vidu Q2 Reference to Video` | Vidu Q2 Reference to Video | Vidu |
| `Vidu Q2` | Vidu Q2 | Vidu |
| `Wan 2.6` | 万象 V2.6 | 万象 |

### 视频编辑

| API 名称 | 展示名称 | 供应商展示名 |
|----------|---------|-------------|
| `Standard` | 地表最强模型S2.0-白名单版（支持上传真人图） | seedance |
| `Fast` | 地表最强模型S2.0 Fast-白名单版（支持上传真人图） | seedance |
| `Kling O3 Video-Edit` | 可灵 O3 Video-Edit | 可灵 |
| `Kling O1 Video-Edit` | 可灵 O1 Video-Edit | 可灵 |

### 动态控制

| API 名称 | 展示名称 | 供应商展示名 |
|----------|---------|-------------|
| `Kling Motion Control Pro V3` | 可灵 Motion Control Pro V3 | 可灵 |
| `Kling Motion Control Std V3` | 可灵 Motion Control Std V3 | 可灵 |
| `Kling Motion Control Pro` | 可灵 Motion Control Pro | 可灵 |
| `Kling Motion Control Std` | 可灵 Motion Control Std | 可灵 |

---

## 图片模型映射

适用于文生图 (text2image) 和图像编辑 (image_edit)。

| API 名称 | 展示名称 | 供应商展示名 |
|----------|---------|-------------|
| `Nano Banana 2` | 全能图片模型 V2 | 全能图片模型 |
| `Nano Banana Pro` | 全能图片模型 Pro | 全能图片模型 |
| `Nano Banana` | 全能图片模型 | 全能图片模型 |
| `Seedream 5.0` | Seedream 5.0 | Seedream |
| `Seedream 4.5` | Seedream 4.5 | Seedream |
| `Seedream 4.0` | Seedream 4.0 | Seedream |
| `GPT Image 1.5` | 强语义理解模型 V1.5 | 强语义理解模型 |
| `Kontext-Pro` | 强上下文一致性模型 pro | 强上下文一致性模型 |
| `Imagen 4` | 照片级写实模型 V4 | 照片级写实模型 |
