# vod_aigc_image — 详细参数与示例
> 此文件由 references 拆分生成，对应脚本：`scripts/vod_aigc_image.py`

### ⚠️ 常见参数错误

| 错误用法 | 正确用法 | 说明 |
|---------|---------|------|
| `--model hunyuan-3.0` | `--model Hunyuan --model-version 3.0` | 模型名和版本号分开 |
| `--model vidu-q2` 或 `--model vidu` | `--model Vidu --model-version q2` | **模型名必须大写首字母（`Vidu`），版本号单独用 `--model-version q2`** |
| `--aspect-ratio 16:9` | `--output-aspect-ratio 16:9` | 生图输出参数带 `output-` 前缀 |
| `--resolution 2K` | `--output-resolution 2K` | 生图分辨率参数带 `output-` 前缀 |
| `--class-id 10` | `--output-class-id 10` | **生图输出分类 ID 必须用 `--output-class-id`，不能用 `--class-id`** |
| `--file-ids id1,id2` | `--file-infos '[{"Type":"File","FileId":"id1"}]'` | 多参考图用 `--file-infos` JSON 数组 |
| `--person-generation Disallowed` | `--output-person-generation Disallowed` | 禁止人物生成参数带 `output-` 前缀 |

## 参数说明
### 通用参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `--sub-app-id` | int | 子应用 ID（也可通过环境变量 `TENCENTCLOUD_VOD_SUB_APP_ID` 设置） |
| `--region` | string | 腾讯云区域（默认 `ap-guangzhou`） |
| `--json` | flag | JSON 格式输出 |
| `--dry-run` | flag | 只打印请求参数预览，不发送请求 |

### create 参数（创建生图任务）

#### 模型参数（必填）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--model` | string | ✅ | 模型名称（Hunyuan/Qwen/Vidu/Kling/MJ/GEM） |
| `--model-version` | string | - | 模型版本（不填则使用默认版本） |

#### 提示词参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--prompt` | string | ✅* | 生成图片的提示词（当没有参考图时必填） |
| `--negative-prompt` | string | - | 要阻止模型生成图片的提示词（负面提示词） |
| `--enhance-prompt` | string | - | 是否自动优化提示词（Enabled/Disabled） |

#### 参考图参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--file-id` | string | - | 参考图的 FileId（仅支持单张，多张请用 `--file-infos`） |
| `--file-url` | string | - | 参考图的 URL（仅支持单张，多张请用 `--file-infos`；与 `--file-id` 互斥） |
| `--file-text` | string | - | 参考图的描述信息（仅 GEM 2.5/3.0 有效；仅在使用 `--file-id` 或 `--file-url` 时生效，使用 `--file-infos` 时请将 Text 内嵌到 JSON 元素中） |
| `--file-infos` | string | - | 多个参考图的 JSON 数组，格式：`[{"Type":"Url","Url":"...","Text":"描述"}]` |

> **参考图数量限制**：
> - GEM 2.5/3.0：最多 3 张
> - Vidu q2：最多 7 张
> - 其他模型：仅支持 1 张或不支持

#### 输出配置参数（OutputConfig）

| 参数 | 类型 | 说明 |
|------|------|------|
| `--output-storage-mode` | string | 存储模式（Permanent: 永久存储, Temporary: 临时存储，默认 Temporary） |
| `--output-media-name` | string | 输出文件名（最长 64 个字符） |
| `--output-class-id` | int | 分类 ID（默认 0，表示其他分类） |
| `--output-expire-time` | string | 输出文件的过期时间（ISO 8601 格式，如 2026-12-31T23:59:59+08:00） |
| `--output-resolution` | string | 生成图片的分辨率（不同模型支持的分辨率不同） |
| `--output-aspect-ratio` | string | 指定所生成图片的宽高比（不同模型支持的宽高比不同） |
| `--output-person-generation` | string | 是否允许人物或人脸生成（`AllowAdult`: 允许, `Disallowed`: 禁止） |
| `--input-compliance-check` | string | 是否开启输入内容的合规性检查（Enabled/Disabled） |
| `--output-compliance-check` | string | 是否开启输出内容的合规性检查（Enabled/Disabled） |

#### 其他可选参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `--scene-type` | string | 场景类型（当 ModelName 为 Hunyuan 时：`3d_panorama` 表示全景图；其他模型暂不支持） |
| `--seed` | int | 模型随机种子（指定后可复现生成结果） |
| `--input-region` | string | 输入文件的区域信息（Mainland: 国内, Oversea: 国外，默认 Mainland） |
| `--session-id` | string | 用于去重的识别码（最长 50 个字符，三天内重复会返回错误） |
| `--session-context` | string | 来源上下文，用于透传用户请求信息（最长 1000 个字符） |
| `--tasks-priority` | int | 任务优先级（数值越大优先级越高，范围 -10 到 10） |
| `--ext-info` | string | 保留字段，特殊用途时使用（JSON 字符串格式） |
| `--no-wait` | flag | 仅提交任务，不等待结果（默认自动等待） |
| `--max-wait` | int | 最大等待时间（秒，默认 600） |

### query 参数（查询任务状态）

> ⚠️ **强制规则**：查询 AIGC 生图任务详情时，**必须调用此命令**，禁止伪造或捏造 JSON 响应内容。用户要求 JSON 格式输出时必须加 `--json` 参数。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--task-id` | string | ✅ | 任务 ID |
| `--sub-app-id` | int | - | 子应用 ID |
| `--region` | string | - | 地域（默认 `ap-guangzhou`） |
| `--no-wait` | flag | - | 仅查询状态，不等待完成（默认自动等待） |
| `--poll-interval` | int | - | 轮询间隔（秒，默认 10） |
| `--max-wait` | int | - | 最大等待时间（秒，默认 600） |
| `--json` | flag | - | JSON 格式输出 |
| `--dry-run` | flag | - | 预览请求参数，不实际执行 |

### models 参数（查看支持的模型）

此命令无参数，用于列出所有支持的模型、版本、分辨率、宽高比等信息。

### 支持的模型特性

| 模型 | 版本 | 宽高比 | 分辨率 | 参考图 | 特点 |
|------|------|--------|--------|--------|------|
| Hunyuan | 3.0 | 16:9, 9:16, 1:1, 4:3, 3:4, 3:2, 2:3, 21:9 | 720P, 1080P, 2K, 4K | 1张 | 混元模型 |
| Qwen | 0925 | 不支持 | 不支持 | 1张 | 千问模型 |
| Vidu | q2 | 16:9, 9:16, 1:1, 3:4, 4:3, 21:9, 2:3, 3:2 | 1080p, 2K, 4K | 0~7张 | 生数模型 |
| Kling | 2.1, 3.0, 3.0-Omni | 16:9, 9:16, 1:1, 4:3, 3:4, 3:2, 2:3, 21:9 | 1k, 2k | 1张 | 可灵模型 |
| MJ | v7 | - | - | - | Midjourney 模型 |
| GEM | 2.5, 3.0 | 1:1, 3:2, 2:3, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9 | 1K, 2K, 4K | 0~3张 | 支持参考图 Text 描述 |

### FileInfos 参数结构

`FileInfos` 是一个数组，用于传递参考图信息。每个元素包含以下字段：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `Type` | string | ✅ | 输入类型（File: 点播媒体文件, Url: 可访问的 URL） |
| `FileId` | string | -* | 图片文件的媒体文件 ID（Type=File 时必填） |
| `Url` | string | -* | 可访问的文件 URL（Type=Url 时必填） |
| `Text` | string | - | 输入图片的描述信息（仅 GEM 2.5/3.0 有效） |

### OutputConfig 参数结构

`OutputConfig` 是一个对象，用于配置输出媒体文件的各项参数：

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `StorageMode` | string | Temporary | 存储模式（Permanent/Temporary） |
| `MediaName` | string | - | 输出文件名 |
| `ClassId` | int | 0 | 分类 ID |
| `ExpireTime` | string | - | 过期时间（ISO 8601 格式） |
| `Resolution` | string | - | 分辨率 |
| `AspectRatio` | string | - | 宽高比 |
| `PersonGeneration` | string | - | 是否允许人物生成（AllowAdult/Disallowed） |
| `InputComplianceCheck` | string | - | 输入合规检查（Enabled/Disabled） |
| `OutputComplianceCheck` | string | - | 输出合规检查（Enabled/Disabled） |

### 任务状态说明

| 状态 | 说明 |
|------|------|
| WAIT | 等待中 |
| RUNNING | 处理中 |
| FINISH | 已完成 |
| FAIL | 失败 |

### API 接口对应关系

| 功能 | API 接口 | 文档链接 |
|------|---------|---------|
| 创建 AIGC 生图任务 | `CreateAigcImageTask` | https://cloud.tencent.com/document/api/266/126240 |
| 查询任务状态 | `DescribeTaskDetail` | https://cloud.tencent.com/document/api/266/33431 |

### 错误码说明

| 错误类型 | 原因 | 处理建议 |
|---------|------|---------|
| 模型版本不支持 | 指定的 ModelVersion 不存在 | 查看支持的模型列表，选择正确的版本 |
| 分辨率不支持 | 指定的 Resolution 模型不支持 | 查看模型特性表格，选择支持的分辨率 |
| 宽高比不支持 | 指定的 AspectRatio 模型不支持 | 查看模型特性表格，选择支持的宽高比 |
| 参考图数量超限 | 提供的参考图数量超过模型限制 | 查看模型特性表格，限制在允许范围内 |
| Prompt 必填 | 未提供 Prompt 且没有参考图 | 添加 --prompt 参数或提供参考图 |
| SubAppId 必填 | 未指定子应用 ID | 添加 --sub-app-id 参数或设置环境变量 |
| 拉取任务失败 | URL 无法访问 | 确保 URL 可公网访问，暂不支持 Dash 格式 |

---

## 使用示例
### 1 基础文生图

#### 混元模型生图
```bash
python scripts/vod_aigc_image.py create \
    --model Hunyuan \
    --prompt "一只可爱的小猫在草地上玩耍，阳光明媚"
```

#### GEM 模型生图（指定分辨率和宽高比）
```bash
python scripts/vod_aigc_image.py create \
    --model GEM \
    --model-version 2.5 \
    --prompt "a beautiful sunset over the ocean" \
    --output-resolution 2K \
    --output-aspect-ratio 16:9
```

#### Kling 模型生图（永久存储）
```bash
python scripts/vod_aigc_image.py create \
    --model Kling \
    --model-version 2.1 \
    --prompt "赛博朋克风格的未来城市夜景" \
    --output-resolution 2K \
    --output-aspect-ratio 16:9 \
    --output-storage-mode Permanent
```

### 2 图生图（参考图）

#### 使用 FileId 作为参考图
```bash
python scripts/vod_aigc_image.py create \
    --model Hunyuan \
    --prompt "换成冬天雪景" \
    --file-id 3704211509819
```

#### Vidu q2 模型 + 参考图 FileId（风格参考）
```bash
python scripts/vod_aigc_image.py create \
    --model Vidu \
    --model-version q2 \
    --prompt "山水画风格" \
    --file-id 5145403721231891303
```

#### 使用 URL 作为参考图
```bash
python scripts/vod_aigc_image.py create \
    --model Kling \
    --model-version 2.1 \
    --prompt "将图片风格改为水彩画" \
    --file-url "https://example.com/reference.jpg"
```

#### GEM 多张参考图（最多 3 张）

> 🚨 **多张参考图必须使用 `--file-infos` JSON 数组**，不存在 `--file-ids` 参数，`--file-id` 只支持单张图片。

```bash
python scripts/vod_aigc_image.py create \
    --model GEM \
    --model-version 3.0 \
    --prompt "融合这三张图片的风格" \
    --file-infos '[{"Type":"File","FileId":"3704211509819"},{"Type":"File","FileId":"3704211509820"},{"Type":"File","FileId":"3704211509821"}]'
```

#### GEM 多张参考图（含描述文字）

> ⚠️ 使用 `--file-infos` 时，`--file-text` 参数无效。Text 描述必须内嵌到每个 JSON 元素的 `"Text"` 字段中。

```bash
python scripts/vod_aigc_image.py create \
    --model GEM \
    --model-version 3.0 \
    --prompt "融合这三张图片的风格" \
    --file-infos '[{"Type":"File","FileId":"3704211509819","Text":"第一张图的风格"},{"Type":"File","FileId":"3704211509820","Text":"第二张图的构图"},{"Type":"File","FileId":"3704211509821","Text":"第三张图的色调"}]'
```

### 3 开启提示词优化

```bash
python scripts/vod_aigc_image.py create \
    --model Hunyuan \
    --prompt "风景画" \
    --enhance-prompt Enabled
```

### 4 默认等待任务完成

```bash
# 提交任务并自动等待完成（默认最多等待 600 秒）
python scripts/vod_aigc_image.py create \
    --model Hunyuan \
    --prompt "一只小狗"

# 不等待，仅提交任务
python scripts/vod_aigc_image.py create \
    --model Hunyuan \
    --prompt "一只小狗" \
    --no-wait
```

### 5 查询任务状态

```bash
# 查询并等待任务完成（默认自动等待）
python scripts/vod_aigc_image.py query --task-id task_xxx

# 仅查询当前状态，不等待
python scripts/vod_aigc_image.py query --task-id task_xxx --no-wait
```

### 6 禁止人物生成（output-person-generation）

> ⚠️ **参数值严格区分大小写**：`AllowAdult`（允许成年人物）、`Disallowed`（禁止人物生成），不得使用 `disable`、`disallowed` 等小写形式。

```bash
# 禁止生成人物
python scripts/vod_aigc_image.py create \
    --model Hunyuan \
    --prompt "美丽的山水风景" \
    --output-person-generation Disallowed \
    --sub-app-id 1500046725

# 允许成年人物生成
python scripts/vod_aigc_image.py create \
    --model Hunyuan \
    --prompt "人物肖像" \
    --output-person-generation AllowAdult
```

### 7 查看支持的模型

```bash
python scripts/vod_aigc_image.py models
```

---

