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
| `--num-images 4` 或 `-n 4` | `--output-image-count 4` | **多图输出（OG 1-8、Kling 1-9）**；带 `output-` 前缀 |
| `--format png` | `--output-format png` | **指定输出格式（OG）**：`jpeg`/`png`，带 `output-` 前缀 |
| `--mask-url ...` 或 `--mask-file-id ...` | `--file-infos '[{"Type":"File","FileId":"src"},{"Type":"File","FileId":"mask","ReferenceType":"mask"}]'` | **OG 蒙版编辑**：第一张为待编辑源图，第二张为蒙版图（`ReferenceType="mask"`） |

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
| `--model` | string | ✅ | 模型名称（Hunyuan/Qwen/Vidu/Kling/MJ/GG/SI/OG/Jimeng） |
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
| `--file-text` | string | - | 参考图的描述信息（仅 GG 2.5/3.0 有效；仅在使用 `--file-id` 或 `--file-url` 时生效，使用 `--file-infos` 时请将 Text 内嵌到 JSON 元素中） |
| `--reference-type` | string | - | 单参考图的参考类型（`mask`），与 `--file-id`/`--file-url` 配合，**当前仅 GPT-Image2 (OG) 蒙版编辑使用**；多参考图请用 `--file-infos` 内嵌 `ReferenceType` |
| `--file-infos` | string | - | 多个参考图的 JSON 数组，格式：`[{"Type":"Url","Url":"...","Text":"描述","ReferenceType":"mask"}]`；ReferenceType 用于 OG 蒙版编辑 |

> **参考图数量限制**：
> - GG 2.5/3.0：最多 3 张
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
| `--output-image-count` | int | 生成图片张数（**OG 1-8、Kling 1-9**，含 Kling 扩图；其他模型不支持） |
| `--output-format` | string | 指定输出图片格式（**仅 GPT-Image2 / OG 支持**）：`jpeg` / `png` |
| `--output-logo-add` | string | 是否添加图标水印：`Enabled` / `Disabled`（部分模型生效，OG 行为以服务端为准） |

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

> 📌 各能力来自接口实测确认；最大参考图数量、分辨率、宽高比都已通过真接口提交验证。

| 模型 | 版本 | 宽高比 | 分辨率 | 参考图 | 特点 |
|------|------|--------|--------|--------|------|
| Hunyuan | 3.0, 3d_2.0 | 不支持 AspectRatio（3.0 通过 ExtInfo `size` 传），3d_2.0 全景图固定 | 3.0：宽高均在 [512, 2048]，乘积 ≤ 1024×1024，**通过 ExtInfo `size`**，默认 1024×1024；3d_2.0 全景图：720P–4K | 0~3张 | 混元模型；**3.0 自定义分辨率示例**：`--ext-info '{"AdditionalParameters": "{\"size\":\"728x1024\"}"}'`；**3d_2.0 + `--scene-type 3d_panorama` 用于 360° 全景图**（混元世界模型，文生 / 图生均可）|
| Qwen | 0925 | 不支持 AspectRatio | 自由设宽高，输出像素 [512×512, 2048×2048]，默认 1024×1024，**通过 ExtInfo `width`/`height`** | 0~1张 | 千问模型；**自定义分辨率示例**：`--ext-info '{"AdditionalParameters": "{\"width\":1024, \"height\":1024}"}'` |
| Vidu | q2 | 16:9, 9:16, 1:1, 3:4, 4:3, 21:9, 2:3, 3:2 | 1080P, 2K, 4K（默认 1080P） | 0~7张 | 生数模型；文生图 / 参考生图 |
| Kling | 2.1 | 16:9, 9:16, 1:1, 4:3, 3:4, 3:2, 2:3, 21:9 | 1K, 2K（默认 1K） | 0~4张 | 可灵 2.1 |
| Kling | 3.0 | 16:9, 9:16, 1:1, 4:3, 3:4, 3:2, 2:3, 21:9 | 1K, 2K（默认 1K） | 0~1张 | 可灵 3.0 |
| Kling | 3.0-Omni | 16:9, 9:16, 1:1, 4:3, 3:4, 3:2, 2:3, 21:9, **auto** | 1K, 2K, **4K**（默认 1K） | 0~10张 | 可灵 3.0-Omni；**支持主体生图**（多张参考图）；输出支持一次生成 1-9 张（`--output-image-count`）|
| Kling | **O1** | 16:9, 9:16, 1:1, 4:3, 3:4, 3:2, 2:3, 21:9, **auto** | 1K, 2K, **4K**（默认 1K） | 0~10张 | 可灵 O1；与 3.0-Omni 类似；接口实测确认支持 |
| Kling | **scene** | 不适用（由 `--ext-info` 四个 ratio 字段控制扩图范围） | 与原图等比放大，面积 ≤ 原图 3 倍 | **仅 1 张（必填）** | **扩图专用特殊版本**，非常规生图版本；必须配合 `--scene-type image_expand`；详见 §10.3 |
| MJ | v8.1, v7 | 通过 prompt 指定（如 `--ar 16:9`） | 通过 prompt 指定（如 `--q 2`） | 0~3张 | Midjourney 模型；**接口名为 `MJ`**（`Midjourney` 接口拒绝）；v8.1 为最新版 |
| MJ | **v8.2** | 通过 prompt 指定 | 通过 prompt 指定（`--q` 仅支持 `1`/`4`） | 0~3张 | MJ 最新版本（2026-08-03 上新）；`--q` 质量档位与 v7/niji_7 不同（v7/niji_7 支持 `1`/`2`/`4`） |
| MJ | **niji_7** | 通过 prompt 指定 | 通过 prompt 指定（`--q` 支持 `1`/`2`/`4`） | 0~3张 | 二次元专用模型（2026-07-23 上新）；每次仍固定生成 4 张 |
| GG | 2.5 | 1:1, 3:2, 2:3, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9 | 1K, 2K, 4K（默认 1K） | 0~3张 | nano banana（GG 2.5）；**接口名 `GG`，历史别名 `GEM` 也被接口接受** |
| GG | 3.0 | 1:1, 3:2, 2:3, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9 | 1K, 2K, 4K（默认 1K） | 0~14张 | nano banana pro（GG 3.0）；支持扩图 |
| GG | 3.1 | 1:1, 3:2, 2:3, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9, **1:4, 4:1, 1:8, 8:1** | **512**, 1K, 2K, 4K（默认 1K） | 0~14张 | nano2（GG 3.1）；分辨率多 512 档；宽高比多 4 个极端比例 |
| GG | **3.1-lite** | 1:1, 3:2, 2:3, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9 | 1K（**仅支持 1K 直出**），2K/4K 走超分 | 0~14张 | nano banana 2 lite（GG 3.1-lite，2026-07-08 上新）；轻量版，仅原生 1K 出图，2K/4K 需超分放大 |
| SI | **4.0** | 通过 prompt 指定 | 1K, 2K, 4K（默认 1K） | 0~14张 | Seedream 4.0；**支持多图输出**：Prompt 指定数量 + `--ext-info '{"AdditionalParameters": "{\"sequential_image_generation\":\"auto\"}"}'` |
| SI | 4.5 | 通过 prompt 指定 | 2K, 4K（默认 2K） | 0~14张 | Seedream 4.5 |
| SI | 5.0-lite | 通过 prompt 指定 | 2K, **3K**, 4K（默认 2K） | 0~14张 | Seedream 5.0-lite；多 3K 分辨率档 |
| SI | **5.0-pro** | 通过 prompt 指定 | 1K, 2K, 4K（默认 1K） | 0~14张 | Seedream 5.0-pro（2026-07-16 上新）；旗舰版本，画质更优 |
| OG | image2_low, image2_medium, image2_high | 1:1, 3:2, 2:3, 3:4, 4:3, 16:9, 9:16, 21:9, 9:21 | 1K, 2K, 4K（默认 1K） | 0~16张 | **GPT-Image2**：多语种文本渲染强、支持 jpeg/png 输出（`--output-format`）、支持一次生 1~8 张（`--output-image-count`）、支持蒙版编辑（`ReferenceType=mask`）、支持自定义任意 size（16 倍数，需走 `--ext-info`）；不支持透明背景；按输入图片计费 |
| Jimeng | 4.0 | 不支持 AspectRatio | 通过 ExtInfo `width`/`height`，分辨率范围 [1024×1024, 4096×4096] | 0~10张 | 即梦 4.0；**自定义分辨率示例**：`--ext-info '{"AdditionalParameters": "{\"width\":1920, \"height\":1080}"}'`；风格化效果优秀 |

### FileInfos 参数结构

`FileInfos` 是一个数组，用于传递参考图信息。每个元素包含以下字段：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `Type` | string | ✅ | 输入类型（File: 点播媒体文件, Url: 可访问的 URL） |
| `FileId` | string | -* | 图片文件的媒体文件 ID（Type=File 时必填） |
| `Url` | string | -* | 可访问的文件 URL（Type=Url 时必填） |
| `Text` | string | - | 输入图片的描述信息（仅 GG 2.5/3.0 有效） |
| `ReferenceType` | string | - | 参考类型：`mask` 表示该图作为蒙版（**仅 GPT-Image2 / OG 蒙版编辑使用**） |

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
| `OutputImageCount` | int | - | 生成图片张数（OG 1-8、Kling 1-9，含 Kling 扩图） |
| `OutputFormat` | string | - | 输出格式（仅 GPT-Image2 / OG 支持）：jpeg / png |
| `LogoAdd` | string | - | 是否添加图标水印：Enabled / Disabled（部分模型生效） |

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
python3 scripts/vod_aigc_image.py create \
    --model Hunyuan \
    --prompt "一只可爱的小猫在草地上玩耍，阳光明媚"
```

#### GG 模型生图（指定分辨率和宽高比）
```bash
python3 scripts/vod_aigc_image.py create \
    --model GG \
    --model-version 2.5 \
    --prompt "a beautiful sunset over the ocean" \
    --output-resolution 2K \
    --output-aspect-ratio 16:9
```

#### Kling 模型生图（永久存储）
```bash
python3 scripts/vod_aigc_image.py create \
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
python3 scripts/vod_aigc_image.py create \
    --model Hunyuan \
    --prompt "换成冬天雪景" \
    --file-id 3704211509819
```

#### Vidu q2 模型 + 参考图 FileId（风格参考）
```bash
python3 scripts/vod_aigc_image.py create \
    --model Vidu \
    --model-version q2 \
    --prompt "山水画风格" \
    --file-id 5145403721231891303
```

#### 使用 URL 作为参考图
```bash
python3 scripts/vod_aigc_image.py create \
    --model Kling \
    --model-version 2.1 \
    --prompt "将图片风格改为水彩画" \
    --file-url "https://example.com/reference.jpg"
```

#### GG 多张参考图（最多 3 张）

> 🚨 **多张参考图必须使用 `--file-infos` JSON 数组**，不存在 `--file-ids` 参数，`--file-id` 只支持单张图片。

```bash
python3 scripts/vod_aigc_image.py create \
    --model GG \
    --model-version 3.0 \
    --prompt "融合这三张图片的风格" \
    --file-infos '[{"Type":"File","FileId":"3704211509819"},{"Type":"File","FileId":"3704211509820"},{"Type":"File","FileId":"3704211509821"}]'
```

#### GG 多张参考图（含描述文字）

> ⚠️ 使用 `--file-infos` 时，`--file-text` 参数无效。Text 描述必须内嵌到每个 JSON 元素的 `"Text"` 字段中。

```bash
python3 scripts/vod_aigc_image.py create \
    --model GG \
    --model-version 3.0 \
    --prompt "融合这三张图片的风格" \
    --file-infos '[{"Type":"File","FileId":"3704211509819","Text":"第一张图的风格"},{"Type":"File","FileId":"3704211509820","Text":"第二张图的构图"},{"Type":"File","FileId":"3704211509821","Text":"第三张图的色调"}]'
```

### 3 开启提示词优化

```bash
python3 scripts/vod_aigc_image.py create \
    --model Hunyuan \
    --prompt "风景画" \
    --enhance-prompt Enabled
```

### 4 默认等待任务完成

```bash
# 提交任务并自动等待完成（默认最多等待 600 秒）
python3 scripts/vod_aigc_image.py create \
    --model Hunyuan \
    --prompt "一只小狗"

# 不等待，仅提交任务
python3 scripts/vod_aigc_image.py create \
    --model Hunyuan \
    --prompt "一只小狗" \
    --no-wait
```

### 5 查询任务状态

```bash
# 查询并等待任务完成（默认自动等待）
python3 scripts/vod_aigc_image.py query --task-id task_xxx

# 仅查询当前状态，不等待
python3 scripts/vod_aigc_image.py query --task-id task_xxx --no-wait
```

### 6 禁止人物生成（output-person-generation）

> ⚠️ **参数值严格区分大小写**：`AllowAdult`（允许成年人物）、`Disallowed`（禁止人物生成），不得使用 `disable`、`disallowed` 等小写形式。

```bash
# 禁止生成人物
python3 scripts/vod_aigc_image.py create \
    --model Hunyuan \
    --prompt "美丽的山水风景" \
    --output-person-generation Disallowed \
    --sub-app-id 1500046725

# 允许成年人物生成
python3 scripts/vod_aigc_image.py create \
    --model Hunyuan \
    --prompt "人物肖像" \
    --output-person-generation AllowAdult
```

### 7 查看支持的模型

```bash
python3 scripts/vod_aigc_image.py models
```

---

## 8 GPT-Image2 (OG) 高级特性

> 📌 **`OG` = GPT-Image2**：腾讯云接口的 ModelName 是 `OG`，对外宣传名称是 GPT-Image2。三档质量：`image2_low` / `image2_medium` / `image2_high`，速度与画质递增。

> 💪 **核心能力**：多语种文本渲染（中/英/日/韩/阿）、多图输出（1~8 张）、自定义任意 size（16 倍数）、jpeg/png 输出、蒙版编辑、最多 16 张参考图。

> ⚠️ **不支持**：透明背景（如需降级 gpt-image-1.5）。

### 8.1 通用文生图（对应文档 3.14.2）

```bash
python3 scripts/vod_aigc_image.py create \
    --model OG --model-version image2_medium \
    --prompt "A futuristic city at sunset, photorealistic" \
    --output-aspect-ratio 16:9 \
    --output-resolution 2K \
    --output-storage-mode Temporary \
    --sub-app-id 1308104797
```

### 8.2 多图输出 OutputImageCount（对应文档 3.14.3）

> ⚠️ **取值范围**：OG 1-8、Kling 1-9（含 Kling 扩图）。

```bash
# 一次生 4 张
python3 scripts/vod_aigc_image.py create \
    --model OG --model-version image2_low \
    --prompt "Cute cartoon corgi, multiple variations" \
    --output-aspect-ratio 1:1 \
    --output-image-count 4 \
    --output-storage-mode Temporary \
    --sub-app-id 1308104797
```

返回的 `Output.FileInfos` 数组长度即等于 `OutputImageCount`。

### 8.3 自定义 size / auto 模式（对应文档 3.14.4，通过 `--ext-info`）

> ⚠️ **size 约束**：宽高均为 16 的倍数；最长边 ≤ 3840；总像素 655,360 ~ 8,294,400。
> auto 模式由模型自动决定尺寸，此时 `--output-aspect-ratio` 不要传 `auto`。

```bash
# 自定义 size: 2000x1104
python3 scripts/vod_aigc_image.py create \
    --model OG --model-version image2_medium \
    --prompt "Wide cinematic banner" \
    --ext-info '{"AdditionalParameters":"{\"size\":\"2000x1104\"}"}' \
    --output-storage-mode Temporary \
    --sub-app-id 1308104797

# auto 模式
python3 scripts/vod_aigc_image.py create \
    --model OG --model-version image2_medium \
    --prompt "A scene that decides its own aspect ratio" \
    --ext-info '{"AdditionalParameters":"{\"size\":\"auto\"}"}' \
    --sub-app-id 1308104797
```

### 8.4 蒙版编辑 ReferenceType=mask（对应文档 3.14.6）

> 🚨 **强制规则**：第一个 FileInfos 元素是**待编辑源图**，第二个元素是**蒙版图**且必须带 `"ReferenceType":"mask"`。蒙版图为 PNG，白色区域代表待替换区域，透明/黑色区域代表保留。

```bash
# 多参考图 + 蒙版（推荐方式）
python3 scripts/vod_aigc_image.py create \
    --model OG --model-version image2_medium \
    --prompt "Replace the masked area with a bright red flower" \
    --file-infos '[{"Type":"File","FileId":"<source_id>"},{"Type":"File","FileId":"<mask_id>","ReferenceType":"mask"}]' \
    --output-storage-mode Temporary \
    --sub-app-id 1308104797

# 单参考图 + 蒙版（仅传蒙版图）
python3 scripts/vod_aigc_image.py create \
    --model OG --model-version image2_medium \
    --prompt "Generate content matching this mask" \
    --file-id <mask_id> --reference-type mask \
    --sub-app-id 1308104797
```

### 8.5 指定输出格式 OutputFormat（对应文档 3.14.7）

```bash
# 输出 jpeg
python3 scripts/vod_aigc_image.py create \
    --model OG --model-version image2_medium \
    --prompt "A red apple on a wooden table" \
    --output-format jpeg \
    --sub-app-id 1308104797

# 输出 png
python3 scripts/vod_aigc_image.py create \
    --model OG --model-version image2_high \
    --prompt "Detailed product render" \
    --output-format png \
    --sub-app-id 1308104797
```

### 8.6 透明图层（对应文档 3.14.5）

> ⚠️ **GPT-Image2 不支持透明背景**（文档明确："如需透明背景，需降级使用 gpt-image-1.5"）。当前 VOD 接入的是 image2 系列，**不要给 OG 传透明背景需求**，会得到不透明背景图。如确需透明背景，请联系腾讯云商务确认 image1.5 的接入方式。

### 8.7 三档质量选型建议

| 版本 | 速度 | 成本 | 推荐场景 |
|------|------|------|---------|
| `image2_low` | 最快 | 最低 | 快速草稿、提示词迭代、批量测试 |
| `image2_medium` | 中 | 中 | 大多数日常生产、通用设计（推荐默认） |
| `image2_high` | 最慢 | 最高 | 最终成品、印刷物料、高精度产品图、复杂文本/小字体渲染 |

---

## 9 Hunyuan 3D 全景图（混元世界模型）

> 📌 **能力定位**：Hunyuan `3d_2.0` 版本配合 `--scene-type 3d_panorama` 生成 **360° ERP 全景图**，可用于 VR / AR、影视背景、虚拟直播等场景；输入支持纯文本（文生 3D）或单张参考图（图生 3D）。生视频侧的 `3d_scene`（3D 模型/3DGS/Mesh）属于生视频脚本范畴，不在本脚本。

### 9.1 文生 3D 全景图

```bash
python3 scripts/vod_aigc_image.py create \
    --model Hunyuan --model-version 3d_2.0 \
    --scene-type 3d_panorama \
    --prompt "一个古风的山间寺庙庭院，雪景，黄昏柔光" \
    --output-storage-mode Temporary \
    --sub-app-id 1308104797
```

### 9.2 图生 3D 全景图（单张参考图）

```bash
python3 scripts/vod_aigc_image.py create \
    --model Hunyuan --model-version 3d_2.0 \
    --scene-type 3d_panorama \
    --prompt "保留场景结构，将其扩展为 360° 全景" \
    --file-url "https://example.com/photo.jpg" \
    --output-storage-mode Temporary \
    --sub-app-id 1308104797
```

### 9.3 与普通 Hunyuan 3.0 的区别

| 维度 | Hunyuan 3.0（默认） | Hunyuan 3d_2.0 |
|---|---|---|
| 用途 | 通用文生图 / 图生图 | 360° 全景图专用 |
| `--scene-type` | 不传 | **必须**传 `3d_panorama` |
| 输出 | 普通图片 | ERP 全景图 |

---

## 10 Kling 高级特性

> 📌 **能力定位**：Kling 生图侧支持普通文/图生图、**多图输出（1-9 张）**、**扩图（outpainting）**。Kling 的动作控制 / 数字人 / 对口型 / 视频编辑 等场景属于 **生视频** 范畴，请用 `vod_aigc_video.py`。

### 10.1 普通文生图 / 图生图

```bash
# 文生图
python3 scripts/vod_aigc_image.py create \
    --model Kling --model-version 2.1 \
    --prompt "赛博朋克未来城市夜景" \
    --output-resolution 2k --output-aspect-ratio 16:9 \
    --sub-app-id 1308104797

# 图生图（FileId 或 URL 任选其一）
python3 scripts/vod_aigc_image.py create \
    --model Kling --model-version 3.0-Omni \
    --file-id 5145403721231891303 \
    --prompt "将风格改为水彩画" \
    --sub-app-id 1308104797
```

### 10.2 一次生成多张图（OutputImageCount 1-9）

```bash
python3 scripts/vod_aigc_image.py create \
    --model Kling --model-version 3.0 \
    --prompt "写实风格的山水画" \
    --output-image-count 5 --output-aspect-ratio 16:9 \
    --sub-app-id 1308104797
```

返回的 `Output.FileInfos` 数组长度等于 `OutputImageCount`。

### 10.3 Kling 扩图（outpainting）

> 🚨 **强制规则**（对应官方接入指南 3.9.11 节，已通过文档规范核实）：
> - **`--model-version` 必须传固定值 `scene`**（不是 2.1/3.0/3.0-Omni/O1 中任何一个，这是扩图专用的特殊版本标识）
> - **`--scene-type` 必须传 `image_expand`**
> - 只能输入**单张**参考图（`--file-id` 或 `--file-url` 二选一，**不支持** `--file-infos` 多图）
> - 必须通过 `--ext-info` 传入 4 个方向的扩充比例（4 个字段均为**必填**）
> - `--prompt` 为选填，最长 2500 字符
> - `--output-image-count` 取值范围 `[1, 9]`，默认 1
> - `--output-storage-mode` 建议用 `Permanent`（永久存储）

**ratio 参数说明**（取值范围 `[0, 2]`，新图整体面积不得超过原图 3 倍）：

| 字段 | 必填 | 含义 |
|---|---|---|
| `up_expansion_ratio` | ✅ | 向上扩充范围，基于原图**高度**的倍数（如原图高 20，值为 0.1，则向上扩 20×0.1=2） |
| `down_expansion_ratio` | ✅ | 向下扩充范围，基于原图**高度**的倍数 |
| `left_expansion_ratio` | ✅ | 向左扩充范围，基于原图**宽度**的倍数 |
| `right_expansion_ratio` | ✅ | 向右扩充范围，基于原图**宽度**的倍数 |

**命令模板（URL 输入）**：

```bash
python3 scripts/vod_aigc_image.py create \
    --model Kling --model-version scene \
    --scene-type image_expand \
    --file-url "https://example.com/source.jpg" \
    --prompt "补全周围天空与海面（≤2500 字符）" \
    --output-image-count 2 \
    --output-storage-mode Permanent \
    --ext-info '{"AdditionalParameters":"{\"up_expansion_ratio\":0.1,\"down_expansion_ratio\":0.2,\"left_expansion_ratio\":0.3,\"right_expansion_ratio\":0.4}"}' \
    --sub-app-id 1308104797
```

**命令模板（FileId 输入）**：

```bash
python3 scripts/vod_aigc_image.py create \
    --model Kling --model-version scene \
    --scene-type image_expand \
    --file-id <参考图 FileId> \
    --prompt "补全周围天空与海面" \
    --output-image-count 2 \
    --output-storage-mode Permanent \
    --ext-info '{"AdditionalParameters":"{\"up_expansion_ratio\":0.2,\"down_expansion_ratio\":0.2,\"left_expansion_ratio\":0.3,\"right_expansion_ratio\":0.3}"}' \
    --sub-app-id 1308104797
```

> ✅ **已通过 `--dry-run` 验证**：脚本参数体系无需改动即可正确构造该请求，生成的 JSON 与官方文档规范完全一致。此前版本文档缺少 `--model-version scene` 和 `--scene-type image_expand` 两个必填字段，已修正。

### 10.4 多图主体生图（3.0-Omni / O1，最多 10 张参考图）

Kling 3.0-Omni 与 O1 支持**最多 10 张参考图**做主体生图，通过 `--file-infos` JSON 数组传入：

```bash
python3 scripts/vod_aigc_image.py create \
    --model Kling --model-version 3.0-Omni \
    --prompt "将这些角色组合成一幅家庭合影，写实风格" \
    --file-infos '[
        {"Type":"Url","Url":"https://e.com/p1.jpg"},
        {"Type":"Url","Url":"https://e.com/p2.jpg"},
        {"Type":"Url","Url":"https://e.com/p3.jpg"}
    ]' \
    --output-resolution 4K --output-aspect-ratio auto \
    --sub-app-id 1308104797
```

> 接口实测确认：3.0-Omni 与 O1 都支持 4K + `auto` 宽高比 + 最多 10 张参考图。

### 10.5 Kling 4K 输出（仅 3.0-Omni / O1）

```bash
python3 scripts/vod_aigc_image.py create \
    --model Kling --model-version 3.0-Omni \
    --prompt "雪山日出，超写实摄影风格" \
    --output-resolution 4K \
    --output-aspect-ratio 16:9 \
    --sub-app-id 1308104797
```

| 版本 | 1K | 2K | 4K |
|---|---|---|---|
| 2.1 / 3.0 | ✅ | ✅ | ❌ |
| **3.0-Omni / O1** | ✅ | ✅ | **✅** |

### 10.6 Kling O1（与 3.0-Omni 类似的旗舰版本）

```bash
python3 scripts/vod_aigc_image.py create \
    --model Kling --model-version O1 \
    --prompt "电影级人物肖像" \
    --output-resolution 4K \
    --output-aspect-ratio auto \
    --sub-app-id 1308104797
```

> 接口实测确认：O1 与 3.0-Omni 在分辨率、宽高比、参考图数量上完全一致，可视为旗舰版本互补。

---

## 11 Vidu 高级特性

> 📌 **能力定位**：Vidu q2 生图侧支持**最多 7 张参考图融合**、**4K 高分辨率**、**多种宽高比**。Vidu 的固定主体能力（CreateAigcSubject）属于独立接口，不在本脚本范畴。

### 11.1 普通文生图（高分辨率）

```bash
python3 scripts/vod_aigc_image.py create \
    --model Vidu --model-version q2 \
    --prompt "水墨风格的山水" \
    --output-resolution 4K --output-aspect-ratio 16:9 \
    --sub-app-id 1308104797
```

### 11.2 单图风格参考

```bash
python3 scripts/vod_aigc_image.py create \
    --model Vidu --model-version q2 \
    --file-id 5145403721231891303 \
    --prompt "保持构图换成秋季色调" \
    --sub-app-id 1308104797
```

### 11.3 多图参考（最多 7 张，融合多张图风格）

> 🚨 **多张参考图必须用 `--file-infos`**，传 JSON 数组。`--file-id` / `--file-url` 仅支持单张。

```bash
python3 scripts/vod_aigc_image.py create \
    --model Vidu --model-version q2 \
    --file-infos '[
        {"Type":"Url","Url":"https://e.com/a.jpg"},
        {"Type":"Url","Url":"https://e.com/b.jpg"},
        {"Type":"Url","Url":"https://e.com/c.jpg"},
        {"Type":"Url","Url":"https://e.com/d.jpg"}
    ]' \
    --prompt "融合这几张图的风格" \
    --sub-app-id 1308104797
```

### 11.4 Vidu q2 支持的分辨率与宽高比

| 维度 | 取值 |
|---|---|
| 分辨率 | `1080p`, `2K`, `4K` |
| 宽高比 | 16:9, 9:16, 1:1, 3:4, 4:3, 21:9, 2:3, 3:2 |
| 参考图 | 0~7 张 |

---

## 12 SI（Seedream）高级特性

### 12.1 SI 4.0 多图输出（sequential_image_generation）

SI 4.0 支持一次生成多张图片，需要满足两个条件：

1. **Prompt 中明确指定输出张数**（如"输出 3 张图片"）
2. **ExtInfo 透传** `sequential_image_generation: auto`

```bash
python3 scripts/vod_aigc_image.py create \
    --model SI --model-version 4.0 \
    --prompt "国风插画，仙鹤与松树，输出 3 张" \
    --ext-info '{"AdditionalParameters": "{\"sequential_image_generation\":\"auto\"}"}' \
    --output-storage-mode Temporary \
    --sub-app-id 1308104797
```

> ⚠️ **仅 SI 4.0 支持** sequential 多图输出；SI 4.5 / SI 5.0-lite 暂不支持此能力。

### 12.2 SI 各版本分辨率对比

| 版本 | 分辨率档位 | 默认 | 参考图 |
|---|---|---|---|
| SI 4.0 | 1K, 2K, 4K | 1K | 0~14 张 |
| SI 4.5 | 2K, 4K | 2K | 0~14 张 |
| SI 5.0-lite | 2K, 3K, 4K | 2K | 0~14 张 |
| SI 5.0-pro | 1K, 2K, 4K | 1K | 0~14 张 |

> SI 系列的宽高比通过 Prompt 指定（在文本中描述 16:9、9:16 等），不通过 `--output-aspect-ratio` 参数。

---

## 13 自定义分辨率（ExtInfo width/height/size）

部分模型不支持 `--output-resolution` / `--output-aspect-ratio` 标准参数，需通过 `--ext-info` 透传自定义分辨率。

### 13.1 Hunyuan 3.0 自定义 size

```bash
python3 scripts/vod_aigc_image.py create \
    --model Hunyuan --model-version 3.0 \
    --prompt "中国水墨山水，竖向构图" \
    --ext-info '{"AdditionalParameters": "{\"size\":\"728x1024\"}"}' \
    --output-storage-mode Temporary \
    --sub-app-id 1308104797
```

**约束**：宽、高均在 [512, 2048]，宽高乘积 ≤ 1024×1024 像素，默认 1024×1024。

### 13.2 Qwen 0925 自定义 width/height

```bash
python3 scripts/vod_aigc_image.py create \
    --model Qwen --model-version 0925 \
    --prompt "未来科幻城市夜景" \
    --ext-info '{"AdditionalParameters": "{\"width\":1024, \"height\":1024}"}' \
    --output-storage-mode Temporary \
    --sub-app-id 1308104797
```

**约束**：输出像素 [512×512, 2048×2048]，默认 1024×1024。

### 13.3 Jimeng 4.0 自定义 width/height

```bash
python3 scripts/vod_aigc_image.py create \
    --model Jimeng --model-version 4.0 \
    --prompt "国风插画" \
    --ext-info '{"AdditionalParameters": "{\"width\":1920, \"height\":1080}"}' \
    --output-storage-mode Temporary \
    --sub-app-id 1308104797
```

**约束**：分辨率范围 [1024×1024, 4096×4096]。

### 13.4 ExtInfo 自定义分辨率 vs OutputConfig 对比

| 模型 | 标准 `--output-resolution` / `--output-aspect-ratio` | ExtInfo 自定义分辨率 |
|---|---|---|
| **Hunyuan 3.0** | ❌ 不支持 | ✅ `size` |
| **Qwen 0925** | ❌ 不支持 | ✅ `width`/`height` |
| **Jimeng 4.0** | ❌ 不支持 | ✅ `width`/`height` |
| **OG (GPT-Image2)** | ✅ 支持 + 自定义 | ✅ 任意 size（16 倍数）|
| 其他模型（Kling/GG/SI/Vidu/MJ）| ✅ 支持 | — |

---

## 14 接口实测发现的关键约束

> 这些约束已通过真接口提交验证（2026-06-30）

### 14.1 ModelName 别名

| ModelName 写法 | 接口实测 | 说明 |
|---|---|---|
| `GG` | ✅ 接受 | **skill 当前用法**（产品文档标准名）|
| `GEM` | ✅ 接受 | 历史别名，接口同时接受 |
| `MJ` | ✅ 接受 | skill 当前用法 |
| `Midjourney` | ❌ **拒绝**：`ModelName Midjourney is invalid` | 不可用 |

### 14.2 GG 3.1 极端宽高比实测确认

GG 3.1 接口实测支持以下"极端宽高比"（其他模型大多不支持）：

| AspectRatio | 用途 |
|---|---|
| `1:4`, `4:1` | 极窄 / 极宽全景图 |
| `1:8`, `8:1` | 超长条幅，如电商横幅、网页 banner |

```bash
python3 scripts/vod_aigc_image.py create \
    --model GG --model-version 3.1 \
    --prompt "电商网页 banner，长条幅构图" \
    --output-aspect-ratio 8:1 \
    --output-resolution 4K \
    --sub-app-id 1308104797
```

---