# video-viral-pipeline

> 外语长视频 → 中文字幕成片 → 多条"独立成爆款"的 9:16 竖屏短片（钩子标题+封面+封面帧）→ 可选一键发微信视频号 / 公众号。

一个 Claude Code / OpenClaw **Skill**：给一个视频链接，自动跑完「下载 → 转写 → 翻译 → 烧双语字幕 → 选爆款片段 → 切竖屏 → 配钩子封面 → （可选）发视频号」整条龙。翻译、选片、文案由 Claude 完成，确定性的媒体处理由本 skill 内置脚本完成。

## 安装

```bash
clawhub install video-viral-pipeline      # 或手动放进 ~/.claude/skills/
bash ~/.claude/skills/video-viral-pipeline/scripts/setup.sh
```

`setup.sh` 安装：`yt-dlp`、`ffmpeg-full`(带 libass)、`faster-whisper`(python3.12 venv)，并可选安装视频号发布工具 `social-auto-upload`。

## 用法

对 Claude 说：

> 把这个 YouTube 链接做成中英双语成片，并切 10 条爆款竖屏短片，配封面：<URL>

Claude 会按 `SKILL.md` 的流程执行，产出：
- `…/<片名>-中英双语.mp4`（整片）
- `…切片/*.mp4`（竖屏切片，已带封面帧+双语字幕）
- `…切片/封面/*.jpg`（每条封面图）

发视频号（可选）：

```bash
cd ~/social-auto-upload
PYTHONPATH=. .venv/bin/python ~/.claude/skills/video-viral-pipeline/scripts/publish_shipinhao.py \
  --config publish.json --idx 1     # 先试发 1 条
```

## 内置脚本

| 脚本 | 作用 |
|---|---|
| `scripts/render_clips.py` | 按 `clips.json` 切 9:16 竖屏片段 + 烧钩子标题 |
| `scripts/gen_covers_ai.py` | **用 gpt-image-2 生成爆款封面**（cyber/soft 两风格，自动出 3:4） |
| `scripts/render_covers.py` / `prepend_covers.py` | ffmpeg 兜底封面 + 封面帧 |
| `scripts/publish_shipinhao.py` | 批量发**视频号** |
| `scripts/publish_douyin.py` | 批量发**抖音** |
| `scripts/publish_xiaohongshu.py` | 批量发**小红书**（风控最严，小批量错峰） |
| `scripts/setup.sh` | 一键装依赖 |

**发布覆盖四平台**：视频号 / 抖音 / 小红书（social-auto-upload 浏览器自动化）+ 公众号（xiaohu-wechat-format 推草稿）。封面强烈推荐 `gen_covers_ai.py`（gpt-image-2，中文渲染准，远好于纯 ffmpeg 文字封面）。

配置示例见 `examples/`。

## 依赖与平台

- 主要在 **macOS** 上验证（Intel + Apple Silicon 路径都探测）。
- 转写在 CPU 上约 2x 实时；Apple Silicon 可换 `mlx-whisper` 提速。
- ffmpeg 必须带 `--enable-libass`。

## ⚠️ 重要风险提示

**微信视频号没有官方发布 API**，本 skill 的视频号发布是**浏览器自动化**（驱动视频号助手），属于平台灰色地带、**有账号被限流/封禁的风险**。请：
- 用自己的号、**先试发 1 条**、小批量、错峰；
- 遵守平台规则，对内容与版权负责（翻译搬运他人视频可能涉及版权）。

本 skill 仅提供工具与编排，使用后果由使用者自负。

## License

MIT
