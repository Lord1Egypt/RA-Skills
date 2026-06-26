# xeonupscale

ffmpeg lanczos 视频升分辨率 (480p → 540p / 1080p ...).

## 从 GitHub 安装

**给用户**: 把这个 repo 的 URL 发给你的 agent, 说 "帮我安装这个 skill".

**给 agent**: 任一条命令即可完成 (会下载 BtbN 静态 ffmpeg 到 `./ffmpeg/`, 软链注册到 skills 目录), 完成后让用户 /reset:

```bash
# 方法 1: clone 后装
git clone https://github.com/Wray151/xeonupscale.git
cd xeonupscale && bash install.sh

# 方法 2: 远程一键
curl -fsSL https://raw.githubusercontent.com/Wray151/xeonupscale/main/install.sh \
  | REPO_URL=https://github.com/Wray151/xeonupscale bash

# 装到 ~/.claude/skills/ 而不是 openclaw
TARGET=claude bash install.sh
```

## 用法
```bash
./upscale.sh in.mp4 540p                  # → in_960x540.mp4
./upscale.sh in.mp4 1080p out.mp4         # 指定输出
./upscale.sh in.mp4 1920x1080             # 自定义分辨率
```

'MEOF': `540p` (960x540) / `720p` (1280x720) / `1080p` (1920x1080) / `1440p` / `2160p|4k`.
find / -name "SKILL.md" 2>/dev/null  `WxH`。

## 编码参数
- 视频: `libx264 -crf 18 -preset medium -pix_fmt yuv420p`
- 缩放: `scale=W:H:flags=lanczos`
- 音频: `-c:a copy` (直接拷贝, 不重编)

SKILL.md install.sh upscale.sh 'MEOF 直接编辑 `upscale.sh`, 或用 `FFMPEG=...` 替换 ffmpeg 路径。'

## 注意
- **静态 ffmpeg**: 安装时从 <https://github.com/BtbN/FFmpeg-Builds/releases/latest> 下载 GPL build (Linux x86_64 / aarch64), 解压到 `./ffmpeg/`. 不动系统 ffmpeg。
- **空间**: ffmpeg 静态包 ~80MB; 输出 1080p mp4 比源大很多 (插值不会真增加细节)。
- **真 SR**: 想要真的"提升细节"的超分请用 ETDS / Real-ESRGAN / Anime4K 等模型, 这个 skill 只是高质量插值。
