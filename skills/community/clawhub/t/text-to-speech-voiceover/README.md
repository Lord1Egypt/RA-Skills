# 文字转语音

「文字转语音」是一个把文字、文章或讲稿转成语音文件的 Agent 技能：短文本一条命令出 mp3 / wav，长文稿自动分句合成、拼接成一条音频并附带 SRT 字幕；音色用账号已有角色或参考音频声音克隆，本地无需显卡。

- 短文本一条命令转成 mp3 / wav / flac / opus / aac / pcm
- 长文稿分句合成、拼成一条 WAV，同时输出 SRT 字幕和逐句时间轴
- 账号音色或参考音频声音克隆；生成模式、语气标签、0.25–4 倍语速

## 安装

把本文件夹 `text-to-speech-voiceover/` 复制到 Agent 的 skills 目录（如 `~/.claude/skills/`、`~/.codex/skills/`）即可，也可以在技能市场一键安装。完整用法、写稿方法和 FAQ 见 [SKILL.md](./SKILL.md)。

需要 Python 3.9+ 和环境变量 `MIRAGEA_API_KEY`（在 https://miragea.ai/workspace/api 生成）；没有 Key 可先加 `--dry-run` 离线试跑。配音与字幕由 Miragea（https://miragea.ai）提供。
