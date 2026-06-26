# vod_create_aigc_advanced_custom_element — 详细参数与示例
> 此文件由 references 拆分生成，对应脚本：`scripts/vod_create_aigc_advanced_custom_element.py`

### ⚠️ 常见参数错误

| 错误用法 | 正确用法 | 说明 |
|---------|---------|------|
| `--name 主体名` | `--element-name 主体名` | 自定义主体参数带 `element-` 前缀 |
| `--image-list url1,url2` | `--element-image-list '{"frontal_image":"...","refer_images":[...]}'` | 参考图用 JSON 格式的 `--element-image-list` |

## 目录

**参数说明**
- [通用参数](#通用参数)
- [create 参数](#create-参数创建主体)（必需参数 / 可选参数）
- [参考方式说明](#参考方式说明)（video_refer / image_refer）
- [ElementVideoList / ElementImageList / TagList 格式](#elementvideolist-格式)
- [list 子命令参数](#list-子命令参数)
- [创建记录结构 mem/elements.json](#创建记录结构memelementsjson)

**使用示例**
- [交互式引导创建](#交互式引导创建推荐)
- [创建多图主体（image_refer）](#创建多图主体image_refer)
- [创建视频角色主体（video_refer）](#创建视频角色主体video_refer绑定音色)
- [查看已创建主体记录](#查看已创建主体记录)
- [高级用法（去重/优先级/透传）](#高级用法)

---

## 参数说明


基于 `CreateAigcAdvancedCustomElement` API，支持通过视频或多张图片创建自定义主体。

### 通用参数（`create` 子命令）

| 参数 | 类型 | 说明 |
|------|------|------|
| `--sub-app-id` | int | 点播应用 ID（**必填**，也可通过环境变量 `TENCENTCLOUD_VOD_SUB_APP_ID` 设置） |
| `--region` | string | 地域，默认 `ap-guangzhou` |
| `--json` | flag | JSON 格式输出 |
| `--dry-run` | flag | 预览请求参数，不调用 API |

> ⚠️ `--sub-app-id`、`--region`、`--dry-run`、`--no-wait`、`--max-wait` 仅 `create` 子命令支持；`--json` 在 `create` 和 `list` 子命令中均支持。

### create 参数（创建主体）

#### 必需参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--element-name` | string | ✅ | 主体名称，不能超过 **20 个字符**。建议取能体现功能的名字，方便后续查询。 |
| `--element-description` | string | ✅ | 主体描述，不能超过 **100 个字符**。请做好功能描述。 |
| `--reference-type` | enum | ✅ | 主体参考方式：`video_refer`（视频角色主体）/ `image_refer`（多图主体） |

#### 可选参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--element-voice-id` | string | - | 主体音色 ID，绑定音色库中已有音色。留空不绑定音色。**仅 `video_refer` 类型支持。** |
| `--element-video-list` | JSON string | video_refer 时必填 | 主体参考视频列表（JSON 字符串）。见下方格式说明。 |
| `--element-image-list` | JSON string | image_refer 时必填 | 主体参考图列表（JSON 字符串）。见下方格式说明。 |
| `--tag-list` | JSON string | - | 主体标签列表（JSON 字符串）。见下方格式说明。 |
| `--session-id` | string | - | 用于去重的识别码（最长 50 字符，3天内重复会返回错误） |
| `--session-context` | string | - | 来源上下文，用于透传用户请求信息（最长 1000 字符） |
| `--tasks-priority` | int | - | 任务优先级（-10 到 10，数值越大优先级越高，默认 0） |
| `--interactive` / `-i` | flag | - | 启用交互式引导模式，逐步提示输入各参数（**推荐新用户使用**） |
| `--no-wait` | flag | - | 仅提交任务，不等待结果（默认自动等待） |
| `--max-wait` | int | - | 最大等待时间（秒，默认 600） |

### 参考方式说明

| ReferenceType | 说明 | 支持音色绑定 | 使用的参数 |
|---------------|------|------------|-----------|
| `video_refer` | 视频角色主体，通过参考视频定义外表 | ✅ 支持 | `--element-video-list` |
| `image_refer` | 多图主体，通过多张图片定义外表 | ❌ 不支持 | `--element-image-list` |

### ElementVideoList 格式

仅 `video_refer` 类型使用。视频格式仅支持 MP4/MOV，时长 3s～8s，宽高比 16:9 或 9:16，1080P，最多 1 段，大小不超过 200MB。

```json
{"refer_videos":[{"video_url":"https://example.com/ref.mp4"}]}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `refer_videos` | array | 参考视频列表，最多 1 段 |
| `refer_videos[].video_url` | string | 视频 URL（必填，不得为空） |

### ElementImageList 格式

仅 `image_refer` 类型使用。至少包含 1 张正面参考图，1～3 张其他角度参考图。

```json
{
  "frontal_image": "https://example.com/front.jpg",
  "refer_images": [
    {"image_url": "https://example.com/side.jpg"},
    {"image_url": "https://example.com/back.jpg"}
  ]
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `frontal_image` | string | ✅ | 正面参考图 URL（必须包含 1 张） |
| `refer_images` | array | ✅ | 其他角度或特写参考图（1～3 张，需与正面图有差异） |
| `refer_images[].image_url` | string | ✅ | 参考图 URL |

### TagList 格式

```json
[{"tag_id": "o_101"}, {"tag_id": "o_102"}]
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `tag_id` | string | 标签 ID，格式示例：`o_101`、`o_102` |

### list 子命令参数

无额外参数，直接运行即可查看本地 `mem/elements.json` 中的历史创建记录。

| 参数 | 类型 | 说明 |
|------|------|------|
| `--json` | flag | JSON 格式输出完整记录 |

### 创建记录结构（mem/elements.json）

每次创建成功后，以下字段自动追加到 `mem/elements.json`：

| 字段 | 类型 | 说明 |
|------|------|------|
| `created_at` | string | 创建时间（本地时间，格式 `YYYY-MM-DD HH:MM:SS`） |
| `task_id` | string | 任务 ID |
| `request_id` | string | 请求 ID |
| `sub_app_id` | int | 子应用 ID |
| `element_name` | string | 主体名称 |
| `element_description` | string | 主体描述 |
| `reference_type` | string | 参考方式 |
| `element_voice_id` | string/null | 音色 ID |
| `element_video_list` | string/null | 参考视频（JSON 字符串） |
| `element_image_list` | string/null | 参考图（JSON 字符串） |
| `tag_list` | string/null | 标签列表（JSON 字符串） |
| `session_id` | string/null | 去重识别码 |
| `session_context` | string/null | 来源上下文 |
| `tasks_priority` | int/null | 任务优先级 |

### API 接口对应关系

| 功能 | API 接口 | 文档链接 |
|------|---------|---------|
| 创建 AIGC 高级自定义主体 | `CreateAigcAdvancedCustomElement` | https://cloud.tencent.com/document/api/266/129121 |

### 错误码说明

| 错误类型 | 原因 | 处理建议 |
|---------|------|---------|
| MissingParameter | 缺少必需参数 | 检查 ElementName、ElementDescription、ReferenceType 是否提供 |
| InvalidParameterValue.ElementName | 主体名称超过 20 字符 | 缩短主体名称 |
| InvalidParameterValue.ElementDescription | 主体描述超过 100 字符 | 缩短主体描述 |
| InvalidParameterValue.ReferenceType | 参考方式不支持 | 使用 `video_refer` 或 `image_refer` |
| InvalidParameterValue.ElementVideoList | 视频格式或参数不符合要求 | 检查视频格式（MP4/MOV）、时长（3s～8s）、分辨率（1080P） |
| InvalidParameterValue.ElementImageList | 图片参数不符合要求 | 确保包含 frontal_image 和至少 1 张 refer_images |
| InvalidParameterValue.ElementVoiceId | 音色 ID 不存在或类型不支持 | 确认音色库中存在该音色；image_refer 类型不支持绑定音色 |
| SubAppId 必填 | 未指定子应用 ID | 添加 `--sub-app-id` 参数或设置环境变量 `TENCENTCLOUD_VOD_SUB_APP_ID` |
| LimitExceeded | 频率限制 | 默认 20次/秒 |

---


---


## 使用示例


### 基础用法

#### 交互式引导创建（推荐）
```bash
python scripts/vod_create_aigc_advanced_custom_element.py create --interactive
```

交互式引导会逐步提示输入：
1. **主体名称**（≤20字符）
2. **主体描述**（≤100字符）
3. **参考方式**（video_refer / image_refer）
4. **音色 ID**（仅 video_refer，可跳过）
5. **参考视频/图片 URL**
6. **标签列表**（可跳过）
7. **子应用 ID**

#### 创建多图主体（image_refer）
```bash
python scripts/vod_create_aigc_advanced_custom_element.py create \
    --sub-app-id 1500046725 \
    --element-name "商品展示主体" \
    --element-description "用于电商商品展示的多图定制主体，支持换装和商品图生成" \
    --reference-type image_refer \
    --element-image-list '{"frontal_image":"https://example.com/front.jpg","refer_images":[{"image_url":"https://example.com/side.jpg"},{"image_url":"https://example.com/back.jpg"}]}' \
    --tag-list '[{"tag_id":"o_101"},{"tag_id":"o_102"}]'
```

#### 创建视频角色主体（video_refer，绑定音色）
```bash
python scripts/vod_create_aigc_advanced_custom_element.py create \
    --sub-app-id 1500046725 \
    --element-name "视频角色A" \
    --element-description "从参考视频中定制的角色主体，绑定专属音色，用于短视频生成" \
    --reference-type video_refer \
    --element-video-list '{"refer_videos":[{"video_url":"https://example.com/ref_video.mp4"}]}' \
    --element-voice-id "123333" \
    --tag-list '[{"tag_id":"o_201"}]'
```

#### 创建视频角色主体（不绑定音色）
```bash
python scripts/vod_create_aigc_advanced_custom_element.py create \
    --sub-app-id 1500046725 \
    --element-name "角色B" \
    --element-description "纯视觉角色主体，不绑定音色" \
    --reference-type video_refer \
    --element-video-list '{"refer_videos":[{"video_url":"https://example.com/actor.mp4"}]}'
```

#### 预览请求参数（不实际执行）
```bash
python scripts/vod_create_aigc_advanced_custom_element.py create \
    --sub-app-id 1500046725 \
    --element-name "测试主体" \
    --element-description "测试用主体，验证参数格式" \
    --reference-type image_refer \
    --element-image-list '{"frontal_image":"https://example.com/front.jpg","refer_images":[{"image_url":"https://example.com/side.jpg"}]}' \
    --dry-run
```

### 查看已创建主体记录

```bash
# 列表格式查看
python scripts/vod_create_aigc_advanced_custom_element.py list

# JSON 格式查看（适合程序处理）
python scripts/vod_create_aigc_advanced_custom_element.py list --json
```

#### 示例输出

```
共 2 条主体创建记录：

[1] 主体名称: 商品展示主体
    创建时间: 2026-03-25 23:30:00
    TaskId  : 1500046725-CreateAigcAdvancedCustomElement-abc123t
    描述    : 用于电商商品展示的多图定制主体
    参考方式: image_refer
    标签    : [{"tag_id": "o_101"}, {"tag_id": "o_102"}]

[2] 主体名称: 视频角色A
    创建时间: 2026-03-25 23:35:00
    TaskId  : 1500046725-CreateAigcAdvancedCustomElement-def456t
    描述    : 从参考视频中定制的角色主体，绑定专属音色
    参考方式: video_refer
    标签    : [{"tag_id": "o_201"}]
```

### 高优先级任务创建

```bash
python scripts/vod_create_aigc_advanced_custom_element.py create \
    --sub-app-id 1500046725 \
    --element-name "紧急主体" \
    --element-description "高优先级紧急创建的主体" \
    --reference-type image_refer \
    --element-image-list '{"frontal_image":"https://example.com/front.jpg","refer_images":[{"image_url":"https://example.com/side.jpg"}]}' \
    --tasks-priority 10 \
    --session-id "unique-session-001"
```

### mem/elements.json 示例结构

```json
[
  {
    "created_at": "2026-03-25 23:30:00",
    "task_id": "1500046725-CreateAigcAdvancedCustomElement-abc123t",
    "request_id": "2ff6980c-db91-488b-bb5b-04e8eb5661d2",
    "sub_app_id": 1500046725,
    "element_name": "商品展示主体",
    "element_description": "用于电商商品展示的多图定制主体",
    "reference_type": "image_refer",
    "element_voice_id": null,
    "element_video_list": null,
    "element_image_list": "{\"frontal_image\":\"https://example.com/front.jpg\",\"refer_images\":[{\"image_url\":\"https://example.com/side.jpg\"}]}",
    "tag_list": "[{\"tag_id\":\"o_101\"},{\"tag_id\":\"o_102\"}]",
    "session_id": null,
    "session_context": null,
    "tasks_priority": null
  }
]
```

