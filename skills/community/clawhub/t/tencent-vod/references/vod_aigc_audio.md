# vod_aigc_audio.py 参考文档

VOD AIGC 生音频任务工具，基于 `CreateAigcAudioTask` API。
支持文生音效 / 视频生音效（Kling）、文生音乐（MiniMaxMusic / GL(Google Lyria)）。

## 参数说明

### 基础参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--model` | enum | ❌ | 模型名称：`Kling`（音效）/ `MiniMaxMusic` / `GL`（音乐） |
| `--model-version` | string | ❌ | 模型版本；**Kling 建议留空**（使用系统默认稳定版本，文档示例中该字段为空）；`MiniMaxMusic` 支持 `2.0/2.5/2.6/3.0`；`GL` 支持 `3.0-clip/3.0-pro` |
| `--scene-type` | enum | ❌ | 场景类型：`sfx`（音效，Kling 专用）/ `music`（音乐，MiniMaxMusic/GL 专用） |
| `--prompt` | string | ❌ | 生成音频的描述（提示词） |

### 参考视频参数（视频生音效场景）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--video-id` | string | ❌ | 参考视频的 VOD 文件 FileId |
| `--video-url` | string | ❌ | 参考视频的 URL |
| `--video-infos` | string | ❌ | 多个参考视频的 JSON 数组，格式：`[{"Type":"Url","Url":"..."}]`；与 `--video-id`/`--video-url` 互斥（单文件方式优先） |

### 参考音频参数（如传入音频生成音乐场景）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--audio-id` | string | ❌ | 参考音频的 VOD 文件 FileId |
| `--audio-url` | string | ❌ | 参考音频的 URL |
| `--audio-infos` | string | ❌ | 多个参考音频的 JSON 数组，格式：`[{"Type":"Url","Url":"..."}]` |

### AdditionalParameters 便捷参数

`CreateAigcAudioTask` 的 `AdditionalParameters` 字段用于传入模型特殊场景参数（JSON 字符串）。脚本提供以下便捷参数，会自动合并进同一个 JSON：

| 参数 | 类型 | 说明 |
|------|------|------|
| `--bgm-prompt` | string | 配乐生成提示词（**视频生音效场景，Kling**），合并为 `AdditionalParameters.bgm_prompt` |
| `--asmr-mode` | enum(`true`/`false`) | 是否开启 ASMR 模式（增强细节音效，适合高沉浸内容场景），合并为 `AdditionalParameters.asmr_mode`（布尔值） |
| `--lyrics` | string | 歌词内容（**文生音乐场景，MiniMaxMusic**），合并为 `AdditionalParameters.lyrics` |
| `--additional-parameters` | string | 保留字段，原始 JSON 字符串透传，会与上述便捷参数合并（便捷参数优先） |

### 输出配置参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--output-storage-mode` | enum | ❌ | 存储模式：`Permanent`（永久）/ `Temporary`（临时，默认） |
| `--output-media-name` | string | ❌ | 输出文件名，最长 64 字符 |
| `--output-class-id` | int | ❌ | 输出文件分类 ID，默认 0 |
| `--output-expire-time` | string | ❌ | 输出文件过期时间，ISO 8601 格式 |
| `--output-duration` | int | ❌ | 生成音频的时长（秒），**取值范围 [0, 60]**，默认不填 |
| `--output-audio-format` | string | ❌ | 输出音频格式，如 `wav`、`mp3`，默认不填 |

### 通用参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `--sub-app-id` | int | 子应用 ID，2023-12-25 后开通点播的客户必填 |
| `--region` | string | 地域，默认 `ap-guangzhou` |
| `--no-wait` | flag | 仅提交任务，不等待结果 |
| `--max-wait` | int | 最大等待时间(秒)，默认 600 |
| `--json` | flag | JSON 格式输出完整响应 |
| `--dry-run` | flag | 预览请求参数，不实际执行 |

### 模型/场景对应关系（文档 3.13.1）

| 模块 | ModelName | ModelVersion | SceneType |
|------|-----------|--------------|-----------|
| 文生音效 | Kling | 空（不填） | sfx |
| 视频生音效 | Kling | 空（不填） | sfx |
| 文生音乐 | MiniMaxMusic | 2.0/2.5/2.6/3.0 | music |
| 文生音乐 | GL（Google Lyria） | 3.0-clip/3.0-pro | music |

脚本内置校验：`--model` 与 `--scene-type` 搭配错误（如 `Kling` + `music`），或 `MiniMaxMusic`/`GL` 传入非法 `--model-version`，均会在提交前直接报错拦截。

## 使用示例

### 1 文生音效（Kling）

```bash
python3 scripts/vod_aigc_audio.py create \
    --model Kling --scene-type sfx \
    --prompt "春节庆祝时的烟花声" \
    --output-storage-mode Temporary --output-duration 6 \
    --sub-app-id 1308104797
```

> 实测产物：6.06 秒 mp3 音频（128kbps，44.1kHz）。

### 2 视频生音效（Kling，带配乐 + ASMR 模式）

```bash
python3 scripts/vod_aigc_audio.py create \
    --model Kling --scene-type sfx \
    --video-url "https://example.com/ref.mp4" \
    --prompt "温柔的风声，远处鸟鸣，偶尔的脚步声，翻书声，雨滴打在窗玻璃上的声音" \
    --bgm-prompt "治愈系钢琴曲，轻柔的弦乐伴奏，温暖舒缓的旋律，带有淡淡的情感起伏，适合剧情类视频" \
    --asmr-mode true \
    --output-duration 6 \
    --sub-app-id 1308104797
```

> ⚠️ **实测发现**：视频生音效场景下，`Output` 会同时返回 `AudioInfos`（独立音频）和 `VideoInfos`（合成后的视频，即原视频配上生成的音效），脚本会分别打印两类产物。

### 3 文生音乐（MiniMaxMusic，带歌词）

```bash
python3 scripts/vod_aigc_audio.py create \
    --model MiniMaxMusic --model-version 2.0 --scene-type music \
    --prompt "一首欢乐的歌" \
    --lyrics "大海啊，全是水，骏马啊，四条腿" \
    --output-audio-format mp3 \
    --sub-app-id 1308104797
```

### 4 文生音乐（GL/Google Lyria）

GL 接口只接受 `Prompt` 参数，**歌词和风格需要自行拼接进 Prompt**，脚本不做自动拼接（因为拼接规则依赖场景选择，见下）。拼接规则（文档 3.13.2③）：

| 场景 | 拼接格式 |
|------|----------|
| 有歌词 + 有风格 | `{风格描述}\n\nLyrics:\n{歌词内容}` |
| 无歌词 + 有风格（自动写词） | `{风格描述}` |
| 纯音乐 + 有风格 | `{风格描述}, instrumental, no vocals.` |

```bash
# 纯音乐（无歌词），风格描述 + instrumental 后缀
python3 scripts/vod_aigc_audio.py create \
    --model GL --model-version 3.0-clip --scene-type music \
    --prompt "轻快的电子舞曲风格, instrumental, no vocals." \
    --output-audio-format mp3 \
    --sub-app-id 1308104797

# 有歌词 + 有风格
python3 scripts/vod_aigc_audio.py create \
    --model GL --model-version 3.0-clip --scene-type music \
    --prompt "轻快民谣风格

Lyrics:
大海啊，全是水，骏马啊，四条腿" \
    --output-audio-format mp3 \
    --sub-app-id 1308104797
```

### 5 列出支持的模型

```bash
python3 scripts/vod_aigc_audio.py models
```

### 6 预览请求参数（不实际执行）

```bash
python3 scripts/vod_aigc_audio.py create --model Kling --scene-type sfx --prompt "test" --dry-run
```

## 查询任务状态

`vod_aigc_audio.py` 无 `query` 子命令，AIGC 生音频任务（TaskId 含 `AigcAudioTask`）请使用：

```bash
python3 scripts/vod_describe_task.py --task-id <TaskId>
```

## 实测经验与踩坑

1. **Kling 场景 ModelVersion 留空**：文档示例和真实调用中，Kling 的 `ModelVersion` 字段均为空字符串（不传），实测也验证过传空是正确用法，不要强行指定版本号。
2. **AdditionalParameters 是嵌套 JSON 字符串**：`bgm_prompt`/`asmr_mode`/`lyrics` 都是 `AdditionalParameters` 内部字段，最终请求里 `AdditionalParameters` 本身是一个被 `json.dumps` 序列化过的字符串，脚本已自动处理该序列化，无需手动转义。
3. **视频生音效会返回视频产物**：不仅返回音效音频文件，还会返回合成了音效的视频文件（`Output.VideoInfos`），如果只需要音频，注意从 `AudioInfos` 里取。
4. **GL 需要手动拼接歌词/风格**：GL（Google Lyria）接口本身不支持独立传歌词字段，必须按上述三种场景规则拼接进 `--prompt`，脚本不做自动拼接判断（因为需要用户明确场景意图）。
5. **`--output-duration` 仅对文生/视频生音效场景有效**，取值范围 `[0, 60]` 秒；文生音乐场景（MiniMaxMusic/GL）该字段作用不明确，官方文档未标注音乐场景的时长控制方式，建议留空让模型自行决定时长。
