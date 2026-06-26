# vod_aigc_video — 详细参数与示例
> 此文件由 references 拆分生成，对应脚本：`scripts/vod_aigc_video.py`

## 参数说明
### 基础参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--model` | enum | ✅ | 模型名称（Hailuo/Kling/Jimeng/Vidu/Hunyuan/Mingmou/GV/OS） |
| `--model-version` | string | - | 模型版本（不填则使用默认版本） |
| `--prompt` | string | ❌* | 生成视频的提示词（当没有参考文件时必填） |
| `--negative-prompt` | string | ❌ | 要阻止模型生成视频的提示词（负面提示词） |
| `--enhance-prompt` | enum | ❌ | 是否自动优化提示词（Enabled: 开启, Disabled: 关闭） |

### 参考文件参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--file-id` | string | ❌ | 参考文件的媒体文件 ID（单个值；多个参考图请使用 `--file-infos`） |
| `--file-url` | string | ❌ | 参考文件的 URL（单个值；多个参考图请使用 `--file-infos`） |
| `--file-infos` | JSON | ❌ | 多个参考图的 JSON 数组，格式：`[{"Type":"Url","Url":"..."}]` |

### 首尾帧生成参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--last-frame-file-id` | string | ❌ | 尾帧文件的媒体文件 ID（用于首尾帧生成） |
| `--last-frame-url` | string | ❌ | 尾帧文件的 URL（用于首尾帧生成） |

### 输出配置参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--output-storage-mode` | enum | ❌ | 存储模式（Permanent: 永久存储, Temporary: 临时存储，默认 Temporary） |
| `--output-media-name` | string | ❌ | 输出文件名（最长 64 个字符） |
| `--output-class-id` | int | ❌ | 分类 ID（默认 0，表示其他分类） |
| `--output-expire-time` | string | ❌ | 输出文件的过期时间（ISO 8601 格式，如 2026-12-31T23:59:59+08:00） |
| `--output-duration` | int | ❌ | 生成视频的时长（秒，不同模型支持的时长不同） |
| `--output-resolution` | enum | ❌ | 生成视频的分辨率（不同模型支持的分辨率不同） |
| `--output-aspect-ratio` | enum | ❌ | 指定所生成视频的宽高比（不同模型支持的宽高比不同） |
| `--output-audio-generation` | enum | ❌ | 是否生成音频（Enabled: 开启, Disabled: 关闭，默认 Disabled；GV/OS/Vidu 支持） |
| `--output-person-generation` | enum | ❌ | 是否允许人物或人脸生成（AllowAdult: 允许, Disallowed: 禁止） |
| `--output-enhance-switch` | enum | ❌ | 是否启用视频增强（Enabled/Disabled；分辨率超过模型直出能力时默认启用） |
| `--output-off-peak` | enum | ❌ | 是否开启错峰（Enabled: 开启, Disabled: 关闭） |
| `--output-frame-interpolate` | enum | ❌ | 是否开启 Vidu 智能插帧（Enabled: 开启, Disabled: 关闭） |
| `--output-logo-add` | enum | ❌ | 是否开启图标水印（Enabled: 开启, Disabled: 关闭；目前仅 Vidu 支持） |
| `--input-compliance-check` | enum | ❌ | 是否开启输入内容的合规性检查（Enabled: 开启, Disabled: 关闭） |
| `--output-compliance-check` | enum | ❌ | 是否开启输出内容的合规性检查（Enabled: 开启, Disabled: 关闭） |

### 其他参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--procedure` | string | ❌ | 任务流名称，生成视频后自动执行指定任务流 |
| `--seed` | int | ❌ | 模型随机种子（指定后可复现生成结果） |
| `--input-region` | enum | ❌ | 输入文件的区域信息（Mainland: 国内, Oversea: 国外，默认 Mainland） |
| `--scene-type` | enum | ❌ | 场景类型（motion_control: 动作控制/Kling, avatar_i2v: 数字人/Kling, lip_sync: 对口型/Kling, template_effect: 特效模板/Vidu, subject_reference: 固定主体参考/Vidu） |
| `--subject-infos` | JSON | ❌ | 固定主体 JSON 数组，格式：`[{"Id":"...","Name":"..."}]`（⚠️ SDK 暂不支持，参数可传入但当前不生效） |
| `--element-ids` | string | ❌ | 高级自定义主体 ID（逗号分隔，如 `865750283577090106`），与 `--ext-info` 互斥，优先级更高 |
| `--elements-file` | path | ❌ | 从 JSON 文件读取主体 ID 列表（如 `mem/elements.json`），与 `--element-ids` 互斥 |
| `--session-id` | string | ❌ | 用于去重的识别码（最长 50 个字符，三天内重复会返回错误） |
| `--session-context` | string | ❌ | 来源上下文，用于透传用户请求信息（最长 1000 个字符） |
| `--tasks-priority` | int | ❌ | 任务优先级（数值越大优先级越高，范围 -10 到 10） |
| `--ext-info` | string | ❌ | 保留字段，特殊用途时使用（与 `--element-ids` 互斥，优先级更低） |

### 通用参数（仅 `create` 子命令支持）

| 参数 | 类型 | 说明 |
|------|------|------|
| `--sub-app-id` | int | 子应用 ID（从 2023 年 12 月 25 日起开通点播的客户必须填写，也可通过环境变量 TENCENTCLOUD_VOD_SUB_APP_ID 设置） |
| `--region` | string | 腾讯云区域（默认 ap-guangzhou） |
| `--json` | flag | JSON 格式输出 |
| `--dry-run` | flag | 只打印请求参数预览，不发送请求 |
| `--no-wait` | flag | 仅提交任务，不等待结果（默认自动等待） |
| `--max-wait` | int | 最大等待时间（秒，默认 1800） |

> ⚠️ **注意**：`vod_aigc_video.py` **没有 `query` 子命令**。查询生视频任务状态请使用 `vod_describe_task.py --task-id <task_id>`。

### 模型参数限制对比

#### Hailuo（海螺）

| 参数 | 支持值 |
|------|--------|
| 版本 | 02, 2.3, 2.3-fast |
| 时长 | 6s, 10s（默认 6s） |
| 分辨率 | 768P, 1080P（默认 768P） |
| 宽高比 | 不支持 |
| 首尾帧生成 | 不支持 |
| 音频生成 | 不支持 |

#### Kling（可灵）

| 参数 | 支持值 |
|------|--------|
| 版本 | 1.6, 2.0, 2.1, 2.5, O1, 3.0-Omni |
| 时长 | 5s, 10s（默认 5s） |
| 分辨率 | 720P, 1080P（默认 720P） |
| 宽高比 | 16:9, 9:16, 1:1（默认 16:9） |
| 首尾帧生成 | 支持（2.1 版本必须指定 1080P） |
| 场景类型 | motion_control, avatar_i2v, lip_sync |

#### Jimeng（即梦）

| 参数 | 支持值 |
|------|--------|
| 版本 | 3.0pro |
| 首尾帧生成 | 不支持 |
| 音频生成 | 不支持 |

#### Vidu（生数）

| 参数 | 支持值 |
|------|--------|
| 版本 | q2, q2-pro, q2-turbo, q3-pro, q3-turbo |
| 时长 | 1-10 秒（自定义） |
| 分辨率 | 720P, 1080P（默认 720P） |
| 宽高比 | 16:9, 9:16, 1:1, 3:4, 4:3（默认 16:9） |
| 首尾帧生成 | 支持（仅 q2-pro, q2-turbo） |
| 多图参考 | q2 支持 1-7 张 |
| 场景类型 | template_effect（特效模板）, subject_reference（固定主体参考） |

#### Hunyuan（混元）

| 参数 | 支持值 |
|------|--------|
| 版本 | 1.5 |
| 首尾帧生成 | 不支持 |
| 音频生成 | 不支持 |

#### Mingmou（明眸）

| 参数 | 支持值 |
|------|--------|
| 版本 | 1.0 |
| 首尾帧生成 | 不支持 |
| 音频生成 | 不支持 |

#### GV（GV）

| 参数 | 支持值 |
|------|--------|
| 版本 | 3.1, 3.1-fast |
| 时长 | 固定 8 秒 |
| 分辨率 | 720P, 1080P（默认 720P） |
| 宽高比 | 16:9, 9:16（默认 16:9） |
| 多图参考 | 最多 3 张 |
| 首尾帧生成 | 支持 |

#### OS（OS）

| 参数 | 支持值 |
|------|--------|
| 版本 | 2.0 |
| 时长 | 4s, 8s, 12s（默认 8s） |
| 分辨率 | 固定 720P |
| 宽高比 | 16:9, 9:16（默认 16:9） |
| 首尾帧生成 | 不支持 |

### 任务状态说明

| 状态 | 说明 |
|------|------|
| WAIT | 等待中 |
| RUN | 处理中 |
| FINISH | 已完成 |
| FAIL | 失败 |

### API 接口对应关系

| 功能 | API 接口 | 文档链接 |
|------|---------|---------|
| 创建 AIGC 生视频任务 | `CreateAigcVideoTask` | https://cloud.tencent.com/document/api/266/126239 |
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
| 首尾帧限制 | Kling 2.1 首尾帧必须指定 1080P | 调整分辨率为 1080P 或更换模型版本 |
| 会话重复 | SessionId 在 3 天内重复使用 | 更换 SessionId 或等待过期 |

---


---


## 使用示例
### 1 基础文生视频

#### GV 模型文生视频
```bash
python scripts/vod_aigc_video.py create \
    --model GV \
    --prompt "一只小狗在草地上奔跑，阳光明媚"
```

#### Hailuo 模型（指定分辨率和时长）
```bash
python scripts/vod_aigc_video.py create \
    --model Hailuo \
    --model-version 2.3 \
    --prompt "海边日落的延时摄影" \
    --output-resolution 1080P \
    --output-duration 10
```

#### Kling 模型（高清 1080P，5 秒）
```bash
python scripts/vod_aigc_video.py create \
    --model Kling \
    --model-version 2.1 \
    --prompt "城市夜景的航拍镜头" \
    --output-resolution 1080P \
    --output-duration 5 \
    --output-aspect-ratio 16:9
```

#### Kling O1 模型 + 自定义主体（element-ids）
> ⚠️ **注意**：`--model` 只传 `Kling`，版本号 `O1` 通过 `--model-version` 单独传入，禁止写成 `--model "Kling O1"`。
> ⚠️ **注意**：使用 `--element-ids` 时，`--prompt` 中必须用 `<<<element_1>>>` 占位符替换主体称谓。
```bash
python scripts/vod_aigc_video.py create \
    --model Kling \
    --model-version O1 \
    --element-ids "866084540648271963" \
    --prompt "<<<element_1>>>在海边行走" \
    --sub-app-id 1500046725
```

### 2 图生视频

#### 使用 FileId 作为首帧
```bash
python scripts/vod_aigc_video.py create \
    --model Kling \
    --model-version 2.1 \
    --file-id 3704211509819 \
    --prompt "让图片中的人物慢慢走动起来"
```

#### 使用 URL 作为首帧
```bash
python scripts/vod_aigc_video.py create \
    --model GV \
    --file-url "https://example.com/first_frame.jpg" \
    --prompt "相机缓慢向前推进"
```

### 3 首尾帧生视频

```bash
python scripts/vod_aigc_video.py create \
    --model GV \
    --file-url "https://example.com/first.jpg" \
    --last-frame-url "https://example.com/last.jpg" \
    --prompt "smooth transition between the two scenes"
```

### 4 默认等待任务完成

```bash
# 生视频耗时较长（已设置默认 1800 秒超时）
python scripts/vod_aigc_video.py create \
    --model GV \
    --prompt "一只猫在窗边晒太阳"

# 不等待，仅提交任务
python scripts/vod_aigc_video.py create \
    --model GV \
    --prompt "一只猫在窗边晒太阳" \
    --no-wait
```

### 5 永久存储

```bash
python scripts/vod_aigc_video.py create \
    --model Hailuo \
    --prompt "风景视频" \
    --output-storage-mode Permanent \
    --output-media-name "我的生成视频"
```

### 6 查看支持的模型

```bash
python scripts/vod_aigc_video.py models
```

