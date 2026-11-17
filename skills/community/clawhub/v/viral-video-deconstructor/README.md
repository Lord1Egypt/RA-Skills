# 🎬 爆款短视频拆解

多平台爆款短视频拆解与原创改写 Skill。覆盖 **抖音 / 快手 / YouTube / 哔哩哔哩 / 微信视频号 / 小红书**。

把「模糊想法 / 视频链接 / 视频文件 / 已有文案」加工成可直接拍摄或喂给 AI 视频工具（即梦 / 可灵 / Runway / ComfyUI）的成品：

> 爆点摘要 → 黄金 3 秒 → 逐镜结构 → 原创改写脚本 → 复刻分镜 & 视频提示词反推

并在交付前跑**合规闸门**（敏感词扫描 + 平台限流自检），确保「无敏感词、不会被平台限流」。

## 快速开始

1. 把本文件夹放入 Skill 目录（如 `~/.workbuddy/skills/`）。
2. 本地视频转录依赖（可选，仅当你要转录本地视频时）：
   ```bash
   python scripts/setup_transcribe.py   # 跨平台一键安装 ffmpeg + openai-whisper
   python scripts/transcribe.py <视频文件> --model small --lang zh --out out
   ```
3. 合规扫描：
   ```bash
   python scripts/sensitive_check.py 你的文案.txt
   ```

## 目录

- `SKILL.md`：触发词与五阶段执行逻辑（agent 读取）
- `references/`：`platforms.md`(六平台规格) · `compliance.md`(限流红线) · `output-templates.md`(报告模板) · `transcription.md`(转录流程) · `sensitive_words.txt`(敏感词库)
- `scripts/`：`sensitive_check.py` · `setup_transcribe.py` · `transcribe.py`

## ClawHub 类目

- 类目（categories）：`creative` —— 创意创作（视频 / 写作）
- 主题（topics）：短视频、视频拆解、脚本创作、内容运营

## 说明

- 敏感词库**非穷尽**，请按自身类目补充高频风险词。
- 平台算法 / 合规口径会变动，以各平台官方规则为准。
- 改写须为原创改编，不替用户做搬运 / 去水印 / 伪造数据等违规动作。
- License: MIT
