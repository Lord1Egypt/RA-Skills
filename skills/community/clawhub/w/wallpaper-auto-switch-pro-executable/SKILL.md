---
name: wallpaper-auto-switch-pro-executable
description: 在 macOS 本机从本地壁纸文件夹中立即换壁纸，或安装 launchd 定时轮换任务的可执行技能。
metadata: {"openclaw":{"emoji":"🖼️","requires":{"bins":["bash","osascript","find","gshuf"]}},"tags":["wallpaper","desktop","macos","automation","launchd"],"category":"desktop-automation"}
---

# Wallpaper Auto Switch Pro Executable

这是一个 **可执行版** 的 macOS 壁纸轮换技能。

它与“说明型 skill”不同：
- 自带本地脚本
- 能立即切换壁纸
- 能安装 launchd 定时任务
- 能卸载定时任务
- 不假装联网搜索或自动下载图片

## 适用范围

仅适用于 **macOS**，并且要求用户已经准备好了一个本地壁纸文件夹。

支持这些任务：
- 立刻从某个文件夹随机换一张壁纸
- 检查某个文件夹里有多少可用图片
- 安装每 N 分钟自动轮换一次的 launchd 任务
- 卸载已经安装的自动轮换任务
- 查看当前 launchd 任务配置路径

## 不做的事情

- 不自动联网下载壁纸
- 不伪造“已换成功”
- 不支持 Windows 或 Linux
- 不支持 WeChat / QQ / 手机壁纸
- 不依赖虚构的 OpenClaw 壁纸 UI 页面

## 依赖

本 skill 依赖以下 macOS 本机能力：
- `bash`
- `osascript`
- `find`
- `shuf`

## 默认图片后缀

会识别以下图片格式：
- jpg
- jpeg
- png
- heic
- webp

## 使用方式

### 1. 立即随机换壁纸

当用户说：
- 立刻从某个文件夹换一张壁纸
- 帮我随机切换桌面背景
- 用本地壁纸目录马上换一张

你应运行：

```bash
bash {baseDir}/scripts/rotate_once.sh "/Users/用户名/Pictures/WallpaperAuto"
```

如果用户没有给目录，优先建议这些常用目录：
- `~/Pictures/WallpaperAuto`
- `~/Pictures/Wallpapers`
- `~/Desktop/wallpapers`

### 2. 检查文件夹中可用壁纸数量

当用户说：
- 检查这个文件夹能不能用
- 看看这个目录里有多少张壁纸
- 帮我列出可用图片

你应运行：

```bash
bash {baseDir}/scripts/list_images.sh "/Users/用户名/Pictures/WallpaperAuto"
```

### 3. 安装自动轮换任务

当用户说：
- 帮我安装自动换壁纸
- 每 60 分钟自动切换一次
- 用 launchd 定时轮换壁纸

你应运行：

```bash
bash {baseDir}/scripts/install_launchagent.sh "/Users/用户名/Pictures/WallpaperAuto" 60
```

第二个参数是分钟数。

### 4. 卸载自动轮换任务

当用户说：
- 关闭自动换壁纸
- 卸载壁纸轮换任务
- 停止定时换壁纸

你应运行：

```bash
bash {baseDir}/scripts/uninstall_launchagent.sh
```

## 输出要求

### 如果是“立即换壁纸”
输出：
1. 使用的文件夹
2. 是否成功
3. 实际设置的文件路径
4. 如果失败，明确失败原因

### 如果是“安装自动轮换”
输出：
1. 壁纸目录
2. 轮换间隔（分钟）
3. launchd plist 路径
4. 是否安装成功
5. 如何卸载

### 如果是“检查文件夹”
输出：
1. 目录是否存在
2. 可识别图片数量
3. 前几个文件名示例
4. 是否建议继续安装自动轮换

## 真实性要求

- 只有脚本命令真实成功后，才能说“已安装”或“已切换”
- 如果目录不存在、图片数量为 0、launchd 加载失败、osascript 执行失败，必须明确报错
- 不要假装已创建 schedule
- 不要假装已成功切换桌面

## 安全与兼容性要求

- 只操作用户明确提供的目录
- 不删除用户图片
- 不移动用户文件
- launchd 仅写入当前用户的 `~/Library/LaunchAgents`
- 默认 label：`com.openclaw.wallpaperrotator`

## 推荐回答策略

### A. 用户只说“帮我自动换壁纸”
先问或建议：
- 你的壁纸文件夹在哪里？
- 如果没有，建议使用 `~/Pictures/WallpaperAuto`
- 你想每隔多少分钟/小时切换？

### B. 用户已经有目录
优先先检查目录：

```bash
bash {baseDir}/scripts/list_images.sh "目录"
```

如果目录可用，再继续：
- 立刻切换一次
- 或安装定时任务

### C. 用户要求“马上执行”
优先执行 `rotate_once.sh`。

## 常用目录建议

- `~/Pictures/WallpaperAuto`
- `~/Pictures/Wallpapers`

## 示例

用户：帮我把 `~/Pictures/WallpaperAuto` 设成随机壁纸并马上切换。  
你应运行：

```bash
bash {baseDir}/scripts/rotate_once.sh "$HOME/Pictures/WallpaperAuto"
```

用户：帮我每 120 分钟自动换一次壁纸，目录是 `~/Pictures/WallpaperAuto`。  
你应运行：

```bash
bash {baseDir}/scripts/install_launchagent.sh "$HOME/Pictures/WallpaperAuto" 120
```
