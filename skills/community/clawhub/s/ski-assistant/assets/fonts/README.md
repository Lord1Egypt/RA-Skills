# Fonts / 字体资源

本目录存放用于小红书分享卡片生成的可选字体文件。

## 字体优先级

`card_generator.py` 按以下顺序自动查找字体（无需手动配置）：

| 优先级 | macOS | Linux | Windows |
|--------|-------|-------|---------|
| 1（首选） | `/System/Library/Fonts/PingFang.ttc` | `/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc` | `C:/Windows/Fonts/simhei.ttf` |
| 2（常规） | `/System/Library/Fonts/PingFang.ttc` | `/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc` | `C:/Windows/Fonts/msyh.ttc` |
| 3（兜底） | 系统默认字体 | 系统默认字体 | 系统默认字体 |

## 手动安装（可选）

如果系统上缺少中日韩字体导致卡片文字显示异常，可将字体文件放入本目录：

1. 下载 [Noto Sans CJK](https://github.com/googlefonts/noto-cjk)（开源免费）
2. 将 `.ttc` 或 `.ttf` 文件放入 `assets/fonts/`
3. 卡片生成器会自动检测并使用

## 推荐字体

- **Noto Sans SC**（简体中文）— Google Fonts / GitHub: googlefonts/noto-cjk
- **Noto Sans TC**（繁体中文）
- **思源黑体 / Source Han Sans** — Adobe + Google 联合开发
