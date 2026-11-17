# AIGC 生音频参数与示例 — `mps_aigc_audio.py`

**功能**：AI 生成音频，支持文生音效、视频生音效、文生音乐（含歌词 / 纯音乐）、歌曲翻唱。
封装 `CreateAigcAudioTask` + `DescribeAigcAudioTask`。

> ⚠️ 生成结果默认存于 MPS 临时存储（12 小时），请尽快下载；配置 COS 后写回自有桶永久保存。

## 模型与场景对照（真接口实测，2026-08-08）

| 场景 | `--scene-type` | 模型 `--model` | 版本 `--model-version` | 说明 |
|------|------|------|------|------|
| 文生音效 / 视频生音效 | `sfx` | `Kling` | 不填 | 实测输出约 5s |
| 文生音乐 | `music` | `MiniMaxMusic` | `2.0` / `2.5` / `2.6` / `3.0` | 支持 `--lyric` 歌词、`--instrumental` 纯音乐；实测时长 143~447s |
| 文生音乐 | `music` | `GL`（Google Lyria）| `3.0-clip` / `3.0-pro` | 支持 `--lyric`；实测 clip≈25s、pro≈175s |
| 歌曲翻唱 | `music` | `Tme` | 不填 | 需 `--song-id` + `--ref-audio-url` |

- `--scene-type` **可省略**，脚本按模型自动推导（Kling→`sfx`，其余→`music`）。
- ⚠️ **MiniMaxMusic / GL 的 `--model-version` 必填**：真实调用实测不传版本时接口报 `InvalidParameterValue: Not support this ModelVersion`（与「默认使用稳定版本」的接口描述不符），脚本已强制校验。
- ⚠️ **GL `3.0-pro` 必须提供歌词**：不传 `--lyric` 时任务会 `FAIL`（`no parts in response`）；`3.0-clip` 无此限制，可用于纯音乐场景。
- **MiniMaxMusic 3.0 已验证可用**，`actions/CreateAigcAudioTask.json` 仅收录到 2.6（接口描述滞后）。
- **`tts` 场景不由本脚本承载**：接口 `SceneType` 实际支持 `tts,music,sfx`，但 Kling 传 `tts` 报 `Invalid model name for TTS`。语音合成请用 [`mps_dubbing.py`](mps_dubbing.md)。

## 参数说明

| 参数 | 说明 |
|------|------|
| `--model` | 模型：`Kling`（默认）/ `MiniMaxMusic` / `GL` / `Tme` |
| `--model-version` | 模型版本。`Kling` / `Tme` **不接受版本号**（传了会报错）|
| `--scene-type` | 场景：`sfx` / `music`。默认按模型推导 |
| `--prompt` | 音频描述（最多 2000 字符）。除 `Tme` 外必填 |
| `--lyric` | 歌词（仅 `MiniMaxMusic` / `GL`）。多行用 `\n` 分隔，走 `AdditionalParameters.lyric` |
| `--instrumental` | 生成纯音乐、不含人声（仅 `MiniMaxMusic`），走 `AdditionalParameters.is_instrumental`；与 `--lyric` 互斥 |
| `--song-id` | 已授权歌曲 ID（仅 `Tme`），走 `ExtraParameters.ResourceId` |
| `--ref-video-url` | 参考视频 URL（视频生音效，仅 `Kling`）。需外网可访问的**真实视频** |
| `--ref-video-cos-key` / `--ref-video-cos-bucket` / `--ref-video-cos-region` | 参考视频 COS 输入，脚本自动生成预签名 URL |
| `--ref-audio-url` | 参考音频 URL（歌曲翻唱等场景）|
| `--ref-audio-cos-key` / `--ref-audio-cos-bucket` / `--ref-audio-cos-region` | 参考音频 COS 输入，脚本自动生成预签名 URL |
| `--output-audio-format` | 输出格式：`mp3` / `wav`（默认由模型决定）|
| `--additional-parameters` | 附加参数（JSON 字符串），与 `--lyric` / `--instrumental` 合并后传入 |
| `--download-dir` | 任务完成后下载音频到指定目录（默认仅打印链接）|
| `--cos-bucket-name` / `--cos-bucket-region` / `--cos-bucket-path` | 结果存储 COS（默认路径 `/output/aigc-audio/`）|
| `--no-wait` | 仅创建任务不等待 |
| `--task-id` | 查询已有任务结果 |
| `--poll-interval` | 轮询间隔（秒），默认 5 |
| `--max-wait` | 最长等待（秒），默认 **600**（音乐生成较慢，实测可达 3~4 分钟）|
| `--operator` | 操作者名称 |
| `--region` | MPS 服务区域（默认 `ap-guangzhou`）|
| `--dry-run` | 仅打印请求参数 |

## 强制规则

- **接口无 `Duration` 与 `OutputConfig` 字段**：音频时长由模型决定，不可指定；输出格式用顶层 `OutputAudioFormat`。文档 3.13.2 中的 `OutputConfig{StorageMode/OutputAudioFormat}` 与 `Duration` 与 `actions/CreateAigcAudioTask.json` 不符，**以接口定义为准**。
- **场景与模型必须匹配**：`Kling` 只支持 `sfx`；`MiniMaxMusic` / `GL` / `Tme` 只支持 `music`。错配会被脚本拒绝。
- **`SceneType` 必填**：不传会被接口拒绝（`Invalid SceneType. Supported: tts,music,sfx`），脚本已按模型自动填充。
- **`Tme` 歌曲翻唱必须同时提供 `--song-id` 与参考音频**：缺 ID 时接口报 `SongId is required for TME model`；且参考音频须为**真实歌曲音频且 URL 可下载**（实测传预签名 COS 图片报 `download file error: 403`）。
- **视频生音效必须传真实视频**：传图片会失败（`Video format is invalid`）。
- **`Tme` 需真实授权歌曲资源**：实测传非授权音频会报 `tme inner error`，无授权资源时该能力无法验证。
- 参考素材只支持 URL（`VideoInfos[].VideoUrl` / `AudioInfos[].AudioUrl`），不支持 CosInputInfo；使用 `--ref-*-cos-key` 时脚本自动转预签名 URL。

## 示例命令

```bash
# 文生音效（Kling，默认模型）
python3 scripts/mps_aigc_audio.py --prompt "雨声与远处的雷声，电影氛围"

# 视频生音效：依据视频内容生成匹配音效
python3 scripts/mps_aigc_audio.py --prompt "与画面匹配的环境音" \
    --ref-video-url https://example.com/src.mp4

# 视频生音效（COS 输入，自动转预签名 URL）
python3 scripts/mps_aigc_audio.py --prompt "环境音" \
    --ref-video-cos-key input/scene.mp4

# 文生音乐 + 歌词（MiniMaxMusic）
python3 scripts/mps_aigc_audio.py --model MiniMaxMusic --model-version 2.6 \
    --prompt "轻快的流行音乐，节奏明快，旋律优美" \
    --lyric "阳光洒在窗台上\n新的一天开始了\n微风轻轻吹过"

# 纯音乐（不含人声）
python3 scripts/mps_aigc_audio.py --model MiniMaxMusic --model-version 2.6 --prompt "轻柔的钢琴曲" --instrumental

# 文生音乐（GL / Google Lyria）
python3 scripts/mps_aigc_audio.py --model GL --model-version 3.0-pro \
    --prompt "an epic orchestral soundtrack with rising tension" \
    --lyric "Hold on to the light"

# 歌曲翻唱（Tme，需授权歌曲 ID）
python3 scripts/mps_aigc_audio.py --model Tme --song-id 4758500_1 \
    --ref-audio-url https://example.com/source.wav

# 指定输出格式 + 下载到本地
python3 scripts/mps_aigc_audio.py --prompt "海浪声" \
    --output-audio-format wav --download-dir ./audio_out

# 存储到自有 COS 桶
python3 scripts/mps_aigc_audio.py --prompt "森林鸟鸣" \
    --cos-bucket-name mybucket-125xxx --cos-bucket-region ap-guangzhou

# 仅提交任务不等待
python3 scripts/mps_aigc_audio.py --prompt "鸟鸣" --no-wait

# 查询任务结果
python3 scripts/mps_aigc_audio.py --task-id 2600011633-AigcAudio-xxxxxxxx
```

## 任务查询

生音频任务有**独立的查询通道**（`DescribeAigcAudioTask`），TaskId 含 `AigcAudio` 字样，
必须用本脚本的 `--task-id` 查询，不能用 `mps_aigc_image.py` / `mps_aigc_video.py` /
`mps_get_video_task.py` 查询（跨通道会返回 ResourceNotFound）。

返回字段：`Status`（`WAIT` / `RUN` / `DONE` / `FAIL`）、`Message`、`AudioInfos[].Url`、
`AudioInfos[].Duration`（音频时长，秒）。
