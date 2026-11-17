# 音频生成与处理

先查询 `audio models --json`，再按输出的 functionId/bindingId 选择已发布能力；语音使用 `functions --function audio.speech.generate --json`。只有当前目录发布的模型可以生成，旧模型名字仍被识别不表示当前账号可用。普通生成需要 `--model` 和 `--prompt`，可选 `--function`、`--binding`；所有收费以实际服务为准。

| 模型 | 控件 |
| --- | --- |
| `elevenlabs_sound_effects` | 仅提示词，不传时长或 seed |
| `seaart_sound_effects` | 必须提供 `--duration-seconds`，1–5秒 |
| `elevenlabs_music_generator` | `--duration-ms` 3000–600000，可选 `--seed` |

```sh
seagames-cli audio generate --model elevenlabs_sound_effects --prompt "木门轻轻打开" --output door.mp3
seagames-cli audio generate --model seaart_sound_effects --prompt "海浪轻拍沙滩" --duration-seconds 5 --wait --json
seagames-cli audio generate --model elevenlabs_music_generator --prompt "安静村庄的循环背景音乐" --duration-ms 30000 --wait --json
```

MiniMax Music 和 Mureka 的兼容参数仍可在帮助中看到，但不要把它们当作已发布选项；只有实时发布目录包含时才使用。音乐、音效输出格式由返回资源决定，不能把 WAV 直接命名为 MP3。未指定文件名的下载按实际格式命名；已有任务用 `tasks download --task-id ID --output-dir NEW_DIRECTORY` 取回。

## 音频工具

本地音频先上传：

```sh
seagames-cli resources upload --file source.wav --type audio --receipt upload.json --json
seagames-cli audio process --resource-id AUDIO --start 1 --end 5 --format wav --normalize --output trimmed.wav --json
```

`--start` 默认 0 秒，`--end` 可省略；结束必须大于开始。`--format` 为 mp3/wav，`--normalize` 启用响度处理。输出后缀应与请求格式一致。此工具返回媒体 job，通过 `media-jobs get/wait --job-id ID --json` 恢复观察，不使用 generation task ID；完成后使用 `media-jobs download --job-id ID --output-dir NEW_DIRECTORY` 取回完整结果。

## 当前绑定参数校验

当前目录包含执行端点时，SeaArt 音效校验 durationSeconds 对应 duration_seconds，Eleven 音乐校验 durationMilliseconds 对应 music_length_ms 及显式 seed；CLI 在报价前拒绝端点撤下或已发布范围不允许的值。Eleven 音效只检查端点存在，仍不开放上游 duration/loop/output_format 等字段，generation-v1 对这些字段的限制不变。

## 语音生成 SeedAudio 1.0

`audio generate --model volces_seed_audio_1_0` 默认选择已发布的 `audio.speech.generate`，不会回退到音乐功能或绕过发布开关。`--prompt` 是完整朗读文本，去除首尾空白后为 1–2000 个 Unicode 字符；不支持音色克隆、参考音频或文本引用。报价携带同一文本的字符数，价格和字符档位由服务端决定。

```sh
seagames-cli audio generate --model volces_seed_audio_1_0 --prompt "欢迎来到冒险世界。" --quote-only --json
seagames-cli audio generate --model volces_seed_audio_1_0 --prompt "欢迎来到冒险世界。" --speech-rate 1.25 --pitch-rate -3 --loudness-rate 0.75 --audio-format mp3 --sample-rate 24000 --project-id PROJECT_ID --output speech.mp3 --json
```

语速 `--speech-rate` 和音量 `--loudness-rate` 为 0.5–2 倍，默认 1；音调 `--pitch-rate` 为 -12–12 整数，默认 0。CLI 将倍率转换为服务端百分比偏移，不要直接传 25 表示 1.25 倍。

默认 MP3、24000 Hz；格式支持 mp3/wav/pcm/ogg_opus，采样率支持 8000/16000/24000/32000/44100/48000（32000、44100 为 API 支持的额外选项）。不指定输出文件名可避免后缀与实际格式冲突。沿用项目绑定、默认后台入图和 `--no-attach`；以回执中的交付状态确认入图完成。中断后通过 `tasks` 和 `canvas operation` 查询原任务，不重新生成。
