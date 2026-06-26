# wallpaper-auto-switch-pro-executable

一个面向 **macOS 本机** 的可执行壁纸轮换 skill。

## 功能

- 立即从本地文件夹随机切换壁纸
- 检查本地文件夹中的可用图片数量
- 安装 launchd 定时任务，实现自动轮换
- 卸载 launchd 定时任务

## 适用场景

- MacBook / iMac / Mac mini
- 已有本地壁纸文件夹
- 希望不依赖第三方 App
- 希望用系统自带 `launchd + osascript` 来定时换壁纸

## 目录结构

```text
wallpaper-auto-switch-pro-executable/
├── SKILL.md
├── README.md
├── CHANGELOG.md
└── scripts/
    ├── common.sh
    ├── list_images.sh
    ├── rotate_once.sh
    ├── install_launchagent.sh
    └── uninstall_launchagent.sh
```

## 依赖

- bash
- osascript
- find
- shuf

## 快速开始

### 1. 测试你的壁纸目录

```bash
bash scripts/list_images.sh "$HOME/Pictures/WallpaperAuto"
```

### 2. 立刻切换一次

```bash
bash scripts/rotate_once.sh "$HOME/Pictures/WallpaperAuto"
```

### 3. 安装自动轮换（例如每 60 分钟）

```bash
bash scripts/install_launchagent.sh "$HOME/Pictures/WallpaperAuto" 60
```

### 4. 卸载自动轮换

```bash
bash scripts/uninstall_launchagent.sh
```

## 说明

- 壁纸会应用到当前用户桌面
- launchd plist 写入：`~/Library/LaunchAgents/com.openclaw.wallpaperrotator.plist`
- 如果系统没有授予相关自动化权限，第一次执行 `osascript` 时可能会提示授权

## 不支持

- Windows
- Linux
- 自动联网下载壁纸
- 手机壁纸
- 虚构的 OpenClaw 壁纸控制面板
