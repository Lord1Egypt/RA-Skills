# 声音克隆

「声音克隆」是一个用一段本人参考音频及其原文克隆声音、再用这个声音给文案配音的 Agent 技能，也可直接使用账号里已复刻的角色；支持单句试听、整稿配音并输出 SRT 字幕，本地无需显卡。

- 参考音频 URL + 原文即可用这个声音配音；也可用账号里已复刻的角色
- 单句试听对比生成模式，再整稿生成 WAV + SRT + 逐句时间轴
- 语气标签、0.25–4 倍语速；只克隆本人或已授权的声音

## 安装

把本文件夹 `voice-cloning-voiceover/` 复制到 Agent 的 skills 目录（如 `~/.claude/skills/`、`~/.codex/skills/`）即可，也可以在技能市场一键安装。完整用法、写稿方法和 FAQ 见 [SKILL.md](./SKILL.md)。

需要 Python 3.9+ 和环境变量 `MIRAGEA_API_KEY`（在 https://miragea.ai/workspace/api 生成）；没有 Key 可先加 `--dry-run` 离线试跑。配音与字幕由 Miragea（https://miragea.ai）提供。
