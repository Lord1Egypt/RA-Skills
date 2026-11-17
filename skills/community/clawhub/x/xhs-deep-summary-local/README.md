# xhs-deep-summary-local · 安装说明（给收到这个包的朋友）

小红书**【视频】笔记**本地深度总结技能：抽元数据 → 下载视频 → 本地语音转写 → 输出逐字稿，**全程免费、无需付费 API / token / cookie**。

## 1. 安装技能
把整个 `xhs-deep-summary-local/` 目录解压到：
```
~/.workbuddy/skills/xhs-deep-summary-local
```

## 2. 装依赖（managed python venv）
```bash
~/.workbuddy/binaries/python/envs/default/bin/python -m pip install imageio-ffmpeg yt-dlp faster-whisper huggingface_hub
```

## 3. 下载转写模型（CT2 格式，约 460MB）
把 ModelScope 上 `Systran/faster-whisper-small` 的文件拉到：
```
~/.workbuddy/models/faster-whisper-small/
```
（HF 不可达时用 ModelScope 镜像；可用环境变量 `XHS_WHISPER_MODEL` 覆盖模型路径、`XHS_VENV_PY` 覆盖 venv 路径。）

## 4. 使用
在 WorkBuddy 对话里贴一条小红书**视频**分享链接（带 `xsec_token`），说「用 xhs-deep-summary-local 总结这个视频」即可。脚本产出 `xhs_meta.json`（元数据）+ `xhs_temp.txt`（逐字稿），再由 LLM 做结构化深度总结。

## 注意
- 仅支持**视频**笔记；图片 / 纯文字笔记另需技能。
- 小红书分享链接有时效，失效后需重新从 App 分享获取。
- 个别笔记若服务端强制登录，yt-dlp 抽不到直链时，需浏览器 cookie（Netscape 格式）并加 `--cookies` 参数。

## 合规与免责声明
- 本技能仅用于**个人学习、本地处理**，请遵守小红书等平台的服务条款与当地法律法规。
- 请勿将转写 / 抓取的内容用于商业用途，或未经授权对外公开再分发。
- 转写结果建议仅存入个人知识库（如 Obsidian / IMA），勿外传平台原文。
- 使用本工具即表示你理解并自行承担相关平台规则与法律法规风险。
