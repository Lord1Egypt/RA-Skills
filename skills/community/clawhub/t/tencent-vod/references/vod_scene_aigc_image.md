# vod_scene_aigc_image — 详细参数与示例
> 此文件由 references 拆分生成，对应脚本：`scripts/vod_scene_aigc_image.py`

### ⚠️ 常见参数错误

| 错误用法 | 正确用法 | 说明 |
|---------|---------|------|
| `change-clothes ...` | `generate --scene-type change_clothes` | 场景化生图用 `generate` 子命令 |
| `--prompt "背景"`（商品图） | `--product-prompt "背景"` | 商品图提示词用 `--product-prompt`；换衣用 `--change-prompt` |
| `--storage-mode Permanent` | `--output-storage-mode Permanent` | 存储模式参数名以 `--output-` 开头 |
| 未提供 FileId 直接生成 | 先上传图片获取 FileId | 用户未提供图片时必须追问，不得使用占位符 |

## 参数说明


基于 `CreateSceneAigcImageTask` API，支持 AI 换衣、AI 生商品图、AI 扩图等场景化图片生成。

### 通用参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `--sub-app-id` | int | 点播应用 ID（必需，也可通过环境变量 `TENCENTCLOUD_VOD_SUB_APP_ID` 设置） |
| `--region` | string | 地域，默认 `ap-guangzhou` |
| `--json` | flag | JSON 格式输出 |
| `--dry-run` | flag | 预览请求参数，不调用 API |
| `--no-wait` | flag | 仅提交任务，不等待结果（默认自动等待） |
| `--max-wait` | int | 最大等待时间（秒，默认 600） |

### generate 参数（创建场景化生图任务）

> ⚠️ **输入文件处理规则**：
> - 用户提供了**本地图片路径** → 先用 `vod_upload.py upload --file <路径>` 上传，再将返回的 FileId 填入 `"File:<FileId>"`
> - 用户提供了**图片 URL** → 直接使用 `"Url:<URL>"` 格式
> - 用户**未提供任何图片/FileId** → **FileId 是必传参数，必须询问用户提供 FileId 或本地文件路径**，不得使用占位符生成命令

#### 必需参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--sub-app-id` | int | ✅ | 点播应用 ID |
| `--scene-type` | enum | ✅ | AI生图场景类型：`change_clothes`（AI换衣）、`product_image`（AI生商品图）、`outpainting`（AI扩图） |

#### 输入文件参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--input-files` | string list | - | 输入图片列表，格式：`File:FileId` 或 `Url:URL` |

> **不同场景的输入要求**：
> - AI换衣场景：只能输入 1 张模特图片
> - AI生商品图场景：需输入 1～10 张同一产品的不同角度的图片
> - AI扩图场景：输入 1 张待扩图图片

#### AI换衣场景参数（scene-type=change_clothes）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--clothes-files` | string list | - | 衣物图片列表，格式：`File:FileId` 或 `Url:URL`，最多 4 张 |
| `--change-prompt` | string | - | AI换衣的提示词 |

#### AI生商品图场景参数（scene-type=product_image）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--product-prompt` | string | - | 生成图片背景的提示词，缺省则内部自动生成灵感 |
| `--negative-prompt` | string | - | 要阻止模型生成图片的提示词 |
| `--product-desc` | string | - | 关于产品的详细描述，有助于生成更符合要求的图片 |
| `--more-requirement` | string | - | 特殊要求，如有特殊要求可通过该字段传入 |
| `--output-image-count` | int | - | 期望生成的图片张数（1-10，默认 1） |

#### 输出配置参数（OutputConfig）

| 参数 | 类型 | 说明 |
|------|------|------|
| `--output-storage-mode` | enum | 存储模式：`Permanent`（永久存储）、`Temporary`（临时存储，默认） |
| `--media-name` | string | 输出文件名（最长 64 字符） |
| `--class-id` | int | 分类 ID（默认 0） |
| `--expire-time` | string | 过期时间（ISO 8601 格式，如 `2026-12-31T23:59:59+08:00`） |
| `--aspect-ratio` | enum | 输出图片宽高比：`1:1`、`3:2`、`2:3`、`3:4`、`4:3`、`4:5`、`5:4`、`16:9`、`9:16`、`21:9` |
| `--image-width` | int | 输出图像宽度（仅AI扩图场景有效） |
| `--image-height` | int | 输出图像高度（仅AI扩图场景有效） |
| `--resolution` | enum | 输出分辨率：`1K`、`2K`、`4K`（仅AI换衣场景有效） |

#### 编码配置参数（仅AI换衣场景有效）

| 参数 | 类型 | 说明 |
|------|------|------|
| `--encode-format` | enum | 图片格式：`JPEG`、`PNG` |
| `--encode-quality` | int | 图片相对质量（1-100，以原图质量为标准） |

#### 其他可选参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `--session-id` | string | 用于去重的识别码（最长 50 字符，3天内重复会返回错误） |
| `--session-context` | string | 来源上下文，用于透传用户请求信息（最长 1000 字符） |
| `--tasks-priority` | int | 任务优先级（-10 到 10，数值越大优先级越高，默认 0） |
| `--ext-info` | string | 保留字段，特殊用途时使用 |

### query 参数（查询任务）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--task-id` | string | ✅ | 任务 ID |
| `--sub-app-id` | int | - | 子应用 ID（也可通过环境变量 `TENCENTCLOUD_VOD_SUB_APP_ID` 设置） |
| `--region` | string | - | 地域，默认 `ap-guangzhou` |
| `--json` | flag | - | JSON 格式输出 |
| `--dry-run` | flag | - | 预览请求参数，不调用 API |

### 数据结构说明

#### SceneInfo 场景信息

```json
{
  "Type": "change_clothes",
  "ChangeClothesConfig": {
    "ClothesFileInfos": [
      {"Type": "File", "FileId": "xxx"}
    ],
    "Prompt": "衬衫打开一点"
  }
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `Type` | string | 场景类型：`change_clothes`、`product_image`、`outpainting` |
| `ChangeClothesConfig` | object | AI换衣配置（Type=change_clothes 时有效） |
| `ProductImageConfig` | object | AI生商品图配置（Type=product_image 时有效） |

#### ChangeClothesConfig 换衣配置

| 字段 | 类型 | 说明 |
|------|------|------|
| `ClothesFileInfos` | array | 衣物图片列表，最多 4 张 |
| `Prompt` | string | AI换衣提示词 |

#### ProductImageConfig 商品图配置

| 字段 | 类型 | 说明 |
|------|------|------|
| `Prompt` | string | 背景生成提示词 |
| `NegativePrompt` | string | 负面提示词 |
| `ProductDesc` | string | 产品描述 |
| `MoreRequirement` | string | 特殊要求 |
| `OutputImageCount` | int | 生成图片数量（1-10） |

#### FileInfos 文件信息

```json
[
  {"Type": "File", "FileId": "3704211xxx509819"},
  {"Type": "Url", "Url": "https://example.com/img.jpg"}
]
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `Type` | string | 类型：`File`（点播媒体文件）、`Url`（可访问的 URL） |
| `FileId` | string | 媒体文件 ID（Type=File 时必填） |
| `Url` | string | 文件 URL（Type=Url 时必填） |

#### OutputConfig 输出配置

```json
{
  "StorageMode": "Temporary",
  "MediaName": "output.jpg",
  "ClassId": 0,
  "ExpireTime": "2026-12-31T23:59:59+08:00",
  "AspectRatio": "1:1",
  "Resolution": "2K",
  "EncodeConfig": {
    "Format": "JPEG",
    "Quality": 90
  }
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `StorageMode` | string | 存储模式 |
| `MediaName` | string | 输出文件名 |
| `ClassId` | int | 分类 ID |
| `ExpireTime` | string | 过期时间 |
| `AspectRatio` | string | 宽高比 |
| `ImageWidth` | int | 图像宽度（扩图场景） |
| `ImageHeight` | int | 图像高度（扩图场景） |
| `Resolution` | string | 分辨率（换衣场景） |
| `EncodeConfig` | object | 编码配置（换衣场景） |

### 任务状态说明

| 状态 | 说明 |
|------|------|
| `PROCESSING` | 处理中 |
| `SUCCESS` | 成功 |
| `FAIL` | 失败 |

### API 接口对应关系

| 功能 | API 接口 | 文档链接 |
|------|---------|---------|
| 创建场景化 AIGC 图片任务 | `CreateSceneAigcImageTask` | https://cloud.tencent.com/document/api/266/126968 |
| 查询任务详情 | `DescribeTaskDetail` | https://cloud.tencent.com/document/api/266/33431 |

### 错误码说明

| 错误类型 | 原因 | 处理建议 |
|---------|------|---------|
| MissingParameter | 缺少必需参数 | 检查 SubAppId 和 SceneInfo 是否提供 |
| InvalidParameterValue.SceneType | 场景类型不支持 | 使用支持的场景类型：change_clothes、product_image、outpainting |
| InvalidParameterValue.AspectRatio | 宽高比不支持 | 检查场景支持的宽高比列表 |
| InvalidParameterValue.Resolution | 分辨率不支持 | 换衣场景支持 1K/2K/4K |
| InvalidParameterValue.FileInfos | 输入图片数量不符合要求 | 换衣场景需 1 张，商品图场景需 1-10 张 |
| InvalidParameterValue.ClothesFileInfos | 衣物图片数量超限 | 最多支持 4 张衣物图片 |
| InvalidParameter | 参数格式错误 | 检查 FileInfos 格式是否为 Type:Value |
| LimitExceeded | 频率限制 | 默认 20次/秒 |

---


---


## 使用示例


基于 `CreateSceneAigcImageTask` API，支持 AI 换衣、AI 生商品图、AI 扩图等场景化图片生成。

### AI换衣场景

#### 基础换衣（使用点播文件）
```bash
python scripts/vod_scene_aigc_image.py generate \
    --sub-app-id 251007502 \
    --scene-type change_clothes \
    --input-files "File:3704211509819" \
    --clothes-files "File:3704211509820" \
    --change-prompt "衬衫打开一点"
```

#### 换衣并使用 URL 图片
```bash
python scripts/vod_scene_aigc_image.py generate \
    --sub-app-id 251007502 \
    --scene-type change_clothes \
    --input-files "Url:https://example.com/model.jpg" \
    --clothes-files "Url:https://example.com/shirt.jpg" \
    --change-prompt "换成休闲风格"
```

#### 多件衣物换衣
```bash
python scripts/vod_scene_aigc_image.py generate \
    --sub-app-id 251007502 \
    --scene-type change_clothes \
    --input-files "File:3704211509819" \
    --clothes-files "File:3704211509820" "File:3704211509821" "File:3704211509822" \
    --change-prompt "搭配这套衣服"
```

#### 换衣并指定输出分辨率
```bash
python scripts/vod_scene_aigc_image.py generate \
    --sub-app-id 251007502 \
    --scene-type change_clothes \
    --input-files "File:3704211509819" \
    --clothes-files "File:3704211509820" \
    --change-prompt "衬衫打开一点" \
    --resolution 4K \
    --aspect-ratio 3:4
```

#### 换衣并指定编码格式
```bash
python scripts/vod_scene_aigc_image.py generate \
    --sub-app-id 251007502 \
    --scene-type change_clothes \
    --input-files "File:3704211509819" \
    --clothes-files "File:3704211509820" \
    --change-prompt "衬衫打开一点" \
    --encode-format JPEG \
    --encode-quality 95
```

#### 换衣并等待完成
```bash
python scripts/vod_scene_aigc_image.py generate \
    --sub-app-id 251007502 \
    --scene-type change_clothes \
    --input-files "File:3704211509819" \
    --clothes-files "File:3704211509820" \
    --change-prompt "衬衫打开一点" \

```

#### 永久存储生成的图片
```bash
python scripts/vod_scene_aigc_image.py generate \
    --sub-app-id 251007502 \
    --scene-type change_clothes \
    --input-files "File:3704211509819" \
    --clothes-files "File:3704211509820" \
    --change-prompt "衬衫打开一点" \
    --output-storage-mode Permanent \
    --media-name "换衣结果"
```

---

### AI生商品图场景

#### 基础商品图生成（单张产品图）
```bash
python scripts/vod_scene_aigc_image.py generate \
    --sub-app-id 251007502 \
    --scene-type product_image \
    --input-files "File:3704211509819" \
    --product-prompt "红色春节背景，喜庆氛围"
```

#### 多角度商品图生成
```bash
python scripts/vod_scene_aigc_image.py generate \
    --sub-app-id 251007502 \
    --scene-type product_image \
    --input-files "File:3704211509819" "File:3704211509820" "File:3704211509821" \
    --product-prompt "蓝色科技背景，未来感"
```

#### 带详细描述的商品图
```bash
python scripts/vod_scene_aigc_image.py generate \
    --sub-app-id 251007502 \
    --scene-type product_image \
    --input-files "File:3704211509819" \
    --product-prompt "森林背景，自然光线" \
    --product-desc "这是一瓶高端矿泉水，透明玻璃瓶身" \
    --more-requirement "要有阳光照射效果，突出瓶身质感"
```

#### 批量生成多张商品图
```bash
python scripts/vod_scene_aigc_image.py generate \
    --sub-app-id 251007502 \
    --scene-type product_image \
    --input-files "File:3704211509819" \
    --product-prompt "不同场景背景" \
    --output-image-count 10 \
    --aspect-ratio 1:1
```

#### 指定负面提示词
```bash
python scripts/vod_scene_aigc_image.py generate \
    --sub-app-id 251007502 \
    --scene-type product_image \
    --input-files "File:3704211509819" \
    --product-prompt "简洁白色背景" \
    --negative-prompt "杂乱、模糊、低质量" \
    --product-desc "一款精致的手表"
```

#### 指定分类和过期时间
```bash
python scripts/vod_scene_aigc_image.py generate \
    --sub-app-id 251007502 \
    --scene-type product_image \
    --input-files "File:3704211509819" \
    --product-prompt "商务场景" \
    --class-id 100 \
    --expire-time "2026-12-31T23:59:59+08:00" \
    --output-storage-mode Permanent
```

---

### AI扩图场景

#### 基础扩图（仅指定宽高比）
```bash
python scripts/vod_scene_aigc_image.py generate \
    --sub-app-id 251007502 \
    --scene-type outpainting \
    --input-files "File:3704211509819" \
    --aspect-ratio 16:9
```

#### 指定具体尺寸扩图
```bash
python scripts/vod_scene_aigc_image.py generate \
    --sub-app-id 251007502 \
    --scene-type outpainting \
    --input-files "File:3704211509819" \
    --aspect-ratio 16:9 \
    --image-width 1920 \
    --image-height 1080
```

#### 扩图为竖屏比例
```bash
python scripts/vod_scene_aigc_image.py generate \
    --sub-app-id 251007502 \
    --scene-type outpainting \
    --input-files "File:3704211509819" \
    --aspect-ratio 9:16 \
    --image-width 1080 \
    --image-height 1920
```

---

### 查询任务

#### 基础查询
```bash
python scripts/vod_scene_aigc_image.py query \
    --task-id "251007502-SceneAigcImageTask-abc123"
```

#### 指定子应用查询
```bash
python scripts/vod_scene_aigc_image.py query \
    --task-id "251007502-SceneAigcImageTask-abc123" \
    --sub-app-id 251007502
```

#### JSON 格式输出
```bash
python scripts/vod_scene_aigc_image.py query \
    --task-id "251007502-SceneAigcImageTask-abc123" \
    --json
```

---

