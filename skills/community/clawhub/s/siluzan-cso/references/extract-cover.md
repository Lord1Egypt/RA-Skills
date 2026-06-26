# extract-cover — 视频封面截取

> 从视频中截取指定时间点的帧，按目标平台规格裁剪缩放，可选自动上传到素材库。
> 需要本机安装 **ffmpeg**，命令会自动检测，未安装时报错提示。

---

## 用法

```bash
# 查看所有平台规格
siluzan-cso extract-cover --list-platforms

# 截取第 3 秒的帧，按 YouTube 规格输出
siluzan-cso extract-cover -f video.mp4 -p youtube -t 3

# 截取多个时间点（输出多张备选封面）
siluzan-cso extract-cover -f video.mp4 -p tiktok -t 1 5 10

# 截取后自动上传到素材库（输出 sourceImageId，可直接填入发布配置）
siluzan-cso extract-cover -f video.mp4 -p youtube -t 3 --upload

# 指定输出目录
siluzan-cso extract-cover -f video.mp4 -p youtube -t 3 -o /path/to/output/
```

---

## 平台规格速查

| 平台 ID（`-p` 参数） | 平台名称           | 尺寸      | 比例 |
| -------------------- | ------------------ | --------- | ---- |
| `youtube`            | YouTube            | 1280×720  | 16:9 |
| `youtube-shorts`     | YouTube Shorts     | 1080×1920 | 9:16 |
| `tiktok`             | TikTok             | 1080×1920 | 9:16 |
| `twitter`            | Twitter / X        | 1280×720  | 16:9 |
| `facebook`           | Facebook           | 1280×720  | 16:9 |
| `instagram`          | Instagram          | 1080×1080 | 1:1  |
| `instagram-portrait` | Instagram Portrait | 1080×1350 | 4:5  |
| `douyin`             | 抖音 (Douyin)      | 1080×1920 | 9:16 |
| `channel`            | 微信视频号         | 1080×1440 | 3:4  |

> 完整规格（含文件大小限制等）运行 `siluzan-cso extract-cover --list-platforms` 查看。

---

## `--upload` 输出字段

加 `--upload` 后自动上传，输出：

| 字段            | 用途                           |
| --------------- | ------------------------------ |
| `sourceImageId` | 发布配置 `cover.sourceImageId` |
| `imageUrl`      | 发布配置 `cover.imageUrl`      |

---

## 交叉引用

- 上传封面到素材库（不截取，直接上传已有图片）→ 参见 `references/upload.md`
- 获取封面后提交发布 → 参见 `references/publish.md`
