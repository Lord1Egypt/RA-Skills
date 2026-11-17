---
name: "tiktok-douyin-dl"
description: "抖音/TikTok 无水印视频和图文批量下载工具。Linux 预编译单文件，支持 douyin-dl 和 tiktok-dl 两个命令。"
---

# TikTok & 抖音无水印下载器 (tiktok-douyin-dl)

跨平台的高效工具套件，用于下载 TikTok 和抖音无水印视频及图文作品。

## 安装位置（永久目录）

- **douyin-dl**: `~/.local/bin/douyin-dl` (75MB)
- **tiktok-dl**: `~/.local/bin/tiktok-dl` (75MB)
- **源码仓库**: `https://github.com/Xynrin/tiktok-douyin-dl`
- **Release 版本**: v1.6.4
- **浏览器缓存**: `~/.cache/ms-playwright/`（首次运行自动下载，完成后后续秒用）
- **Playwright 浏览器**: Chromium 141（约 173MB + 104MB headless shell）

## 使用说明

### 抖音无水印下载

```bash
# CLI 模式（推荐）：直接传链接
douyin-dl "https://v.douyin.com/xxxxx/" "保存目录"

# 交互模式：运行后粘贴链接
douyin-dl
```

### TikTok 无水印下载

```bash
# CLI 模式
tiktok-dl "https://www.tiktok.com/@user/video/xxxxx" "保存目录"

# 交互模式
tiktok-dl
```

## 首次运行注意事项

- 第一次跑会自动下载 Playwright Chromium 浏览器（约 280MB）
- 如果下载太慢，可以用 CNPIP 镜像加速：
  ```bash
  pip3 install playwright --break-system-packages -i https://pypi.tuna.tsinghua.edu.cn/simple
  playwright install chromium
  ```
- Chromium 下载完成后，后续使用无需再下载

## 功能特点

- ✅ 抖音视频/图文无水印批量下载
- ✅ TikTok 视频无水印下载
- ✅ Linux 预编译单文件运行（含 PyInstaller 打包）
- ✅ CLI 参数直接传链接，也支持交互模式
- ✅ 命令行热更新
- ✅ 内置免责声明

## 更新到最新版本

```bash
curl -fL "https://github.com/Xynrin/tiktok-douyin-dl/releases/download/v1.6.4/douyin-dl" -o ~/.local/bin/douyin-dl
curl -fL "https://github.com/Xynrin/tiktok-douyin-dl/releases/download/v1.6.4/tiktok-dl" -o ~/.local/bin/tiktok-dl
chmod +x ~/.local/bin/douyin-dl ~/.local/bin/tiktok-dl
```

## 注意事项

- 运行即代表已同意《免责声明》中的所有条款
- 所有知识产权、平台协议及法律相关风险均由使用者自行承担
