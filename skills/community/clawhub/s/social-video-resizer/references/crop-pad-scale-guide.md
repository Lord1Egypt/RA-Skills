# Crop / Pad / Scale 决策树与命令参考

## 三种策略

- **Crop（裁切）**：切掉画面两侧/上下，主体放大占屏。信息有损，冲击力强。
- **Pad（补边）**：完整保留原画面，边缘补模糊背景/纯色/图形区。信息无损，主体变小。
- **Scale（等比缩放）**：只在分辨率变化、比例不变时使用。**非等比拉伸永远禁止。**

## 决策树

```
目标比例 == 源比例？
├── 是 → 只需 scale 到目标分辨率
└── 否 → 主体（人脸/产品/字幕）是否集中在可保留区域？
    ├── 是（逐镜头确认）→ Crop
    │     └── 字幕是否会被切？
    │           ├── 会 → Crop + 重烧字幕，或改 Pad
    │           └── 不会 → Crop 直接出
    └── 否（主体分散/占满画面）→ Pad
          ├── 横转竖 → 上下 pad：上加标题区，下加品牌区（信息流最优）
          ├── 竖转横 → 两侧模糊 pad，或重构图（左人右卡）
          └── 品牌有底色规范 → 纯色 pad + logo
```

## 方向性经验

| 转换 | 默认策略 | 说明 |
|---|---|---|
| 16:9 → 9:16 | 上下 pad + 标题区 | crop 仅当主体全程居中 |
| 16:9 → 1:1 / 4:5 | 中心 crop（偏主体侧） | 信息损失通常可接受 |
| 9:16 → 16:9 | 两侧模糊 pad 或重构图 | 硬 crop 几乎必切主体 |
| 9:16 → 1:1 | 中心 crop | 检查顶部人脸和底部字幕 |
| 1:1 → 9:16 | 上下 pad | — |

## ffmpeg 命令参考

等比缩放（比例不变）：

    ffmpeg -i in.mp4 -vf "scale=1080:1920:flags=lanczos" -c:a copy out.mp4

中心 crop 16:9 → 9:16（先裁后缩）：

    ffmpeg -i in.mp4 -vf "crop=ih*9/16:ih,scale=1080:1920" -c:a copy out.mp4

偏移 crop（主体偏左，x 从 120px 起裁）：

    ffmpeg -i in.mp4 -vf "crop=608:1080:120:0,scale=1080:1920" -c:a copy out.mp4

上下 pad 16:9 → 9:16（原片居中，上下黑边可换色）：

    ffmpeg -i in.mp4 -vf "scale=1080:608,pad=1080:1920:0:(oh-ih)/2:color=0x101010" out.mp4

两侧模糊 pad 9:16 → 16:9（本片放大模糊做底）：

    ffmpeg -i in.mp4 -filter_complex "[0:v]scale=1920:1080,boxblur=20:5[bg];[0:v]scale=-1:1080[fg];[bg][fg]overlay=(W-w)/2:0" out.mp4

压体积（目标 ~30MB / 60s ≈ 4Mbps）：

    ffmpeg -i in.mp4 -c:v libx264 -b:v 4M -maxrate 4.5M -bufsize 8M -c:a aac -b:a 128k out.mp4

## 使用注意

- crop 参数必须先看片定坐标，不能默认中心
- pad 底色用品牌色时写十六进制（color=0xRRGGBB）
- 交付命令时注明"坐标基于源 1920×1080，若源不同需换算"
