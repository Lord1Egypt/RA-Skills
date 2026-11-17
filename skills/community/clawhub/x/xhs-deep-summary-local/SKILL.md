---
name: xhs-deep-summary-local
description: 本地免费一键深度总结小红书【视频】笔记：yt-dlp 拉取视频（无需 cookie）、faster-whisper 本地转写、输出元数据+逐字稿，再由 LLM 做结构化深度总结。专用于小红书视频笔记的采集与归档。图片笔记/纯文字笔记需另用 xhs-note-summary 类技能。
version: "1.0.0"
license: MIT
metadata:
  openclaw:
    requires:
      bins: ["curl"]
---

# 小红书视频深度总结（本地版 / xhs-deep-summary-local）

> **备注：本技能面向「小红书视频笔记」。图片笔记、纯文字笔记的采集另需一个技能（规划中）。**
>
> **⚠️ 合规提示**：仅限个人学习 / 本地处理使用，请遵守小红书等平台服务条款；转写结果建议仅存入个人知识库，勿对外公开再分发平台内容。

## 技能说明
专用于**小红书视频笔记**的一键深度总结。组合了无水印视频提取、音频分离、本地 AI 语音转录和深度文本总结，**全部在本地免费完成**（不依赖任何付费 API / token）。
相比市场版 `xhs-video-summary`（依赖 clawhub 的 `xiaohongshu-extract` 与 `openai-whisper`），本技能自包含：直接调用 managed venv 里的 `yt-dlp` + `faster-whisper` + `imageio-ffmpeg`，无需那两个装不上的外部依赖。

## 环境依赖（managed venv）
- `~/.workbuddy/binaries/python/envs/default` 已装：`yt-dlp`、`faster-whisper`、`imageio-ffmpeg`、`huggingface_hub`（managed python venv）
- whisper 模型：`~/.workbuddy/models/faster-whisper-small`（CT2 格式；HF 不可达时从 ModelScope 拉取）
- 外部二进制：`curl`（系统自带）

如缺失，环境搭建见文末。

## 工作流
当用户提供小红书视频链接时：

1. **运行脚本**（传入 URL）：
   ```bash
   python <skill_dir>/scripts/run.py "<xhs_url>"
   ```
   脚本自动完成：抽元数据 → 下载视频 → 提音频 → faster-whisper 转写，产出 `xhs_meta.json` + `xhs_temp.txt`。

2. **读取产物**：
   - `xhs_meta.json`：标题、描述、视频直链、时长等
   - `xhs_temp.txt`：视频全部语音逐字稿

3. **输出结构化深度总结**（必须含以下模块）：
   - 🎬 **视频基础信息**（标题、作者、互动数据、时长）
   - 💡 **视频主题**（一句话概括核心话题）
   - 📝 **详细内容拆解**（按逻辑/知识点拆解）
   - 🛠 **实用价值**（对观众的具体帮助）
   - 💎 **关键金句**（原话摘录 2-3 句）

4. **修正识别误差**：转录稿常有口语/方言误识，整理时据上下文修正术语，例如：
   `胃酸`↔"卫酸"、`肠漏`↔"长漏"、`SIBO`↔"sable"、`胃蛋白酶`↔"被蛋白莓"、`盐酸甜菜碱`↔"盐酸甜菜剑"、`法莫替丁/奥美拉唑`↔"法末替丁/奥美拉做耐性" 等。

5. **归档**：写 Obsidian「00-采集 Grasp」+ IMA 知识库目标文件夹（如「营养补剂」，需 IMA 凭证 `~/.config/ima/`）。

6. **清理临时大文件**：
   ```bash
   rm -f xhs_temp.mp4 xhs_temp.mp3
   ```
   （`xhs_meta.json` / `xhs_temp.txt` 如需后续归档可暂留）

## 环境搭建（新机 / 新 venv 部署）
```bash
VENV_PY=~/.workbuddy/binaries/python/envs/default/bin/python
$VENV_PY -m pip install imageio-ffmpeg yt-dlp faster-whisper huggingface_hub
# 下载 CT2 模型（ModelScope 镜像，HF 不可达时可用）：
#   把 Systran/faster-whisper-small 的文件拉到 ~/.workbuddy/models/faster-whisper-small/
# run.py 通过环境变量 XHS_WHISPER_MODEL 可覆盖模型路径；XHS_VENV_PY 可覆盖 venv python 路径。
```

## 已知约束
- 小红书链接需带有效的 `xsec_token`（App 分享出来的链接自带），过期后需重新获取。
- 个别笔记若服务端强制登录，yt-dlp 会抽不到 `video_stream_url`；此时需用户提供浏览器 cookie（Netscape 格式）并加 `--cookies` 参数。
- 元数据里作者/点赞数小红书常不返回（yt-dlp 解析为 null），如实标注即可。
