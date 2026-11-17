# 00-工作台

沙雕动画小助手（Web 社区版）的安装、启动、自检与版本锁定。

## 命令

```bash
bash 00-工作台/setup_app.sh doctor    # 自检：node / npm / git / ffmpeg / 端口
bash 00-工作台/setup_app.sh install   # clone + npm install（一次性）
bash 00-工作台/setup_app.sh start     # 启动主应用
bash 00-工作台/setup_app.sh start-tts # 同时启动本地 TTS Provider（可选）
bash 00-工作台/setup_app.sh path      # 打印安装路径
bash 00-工作台/new_project.sh <剧名>   # 新建项目骨架（目录 + 立项单 + 剧本模板）
bash 00-工作台/patch_vertical.sh apply # 打 9:16 竖屏补丁（导出 1080×1920 必需）
bash 00-工作台/patch_vertical.sh status
bash 00-工作台/patch_vertical.sh restore
```

## 9:16 竖屏补丁（重要）

原版 app 的相机基准是 **16:9（1456×819）**，导出预设也只有 1080p/720p 横屏。
本 skill 默认做 9:16，所以 `patch_vertical.sh apply` 会把：

- 相机基准 → `819×1456`
- 导出预设 → `1080×1920` / `720×1280`
- 字幕默认字号 → `30`，底部安全区 → `10%`

改的是安装目录里的两个文件，原文件备份为 `*.bak-vertical`，可 `restore` 还原。

> 已对当前安装的 app 执行过 `apply`。换机器 / 重装后要重新执行一次。

## 安装到哪

默认 `~/FunnyAnimationAssitant`。想换位置：

```bash
export FAA_HOME="$HOME/tools/FunnyAnimationAssitant"
bash 00-工作台/setup_app.sh install
```

## 浏览器

必须用 **Chrome / Edge**。项目依赖 File System Access API，Safari / Firefox 打开本地文件夹会缺能力。

## 版本锁定

`lock.json` 记录首次验证通过的 commit、app 版本、`.anime` schema 版本。升级 app 后：

1. 更新 `lock.json`；
2. 重跑 `04-工程/shadiao-anime-skill/scripts/validate_anime.mjs`；
3. 用 v0.1 的示例项目做一次「打开 → 预览 → 导出」回归。

## 注意

- `npm run dev` 只启动前端；不配 TTS Provider 时，工程里**预生成好的音频**仍可播放（`ttsConfig.audioPath` 直接读文件）。
- `npm run dev:with-tts` 会额外启动 `examples/tts-provider`，用于在 app 内改词后重新生成语音。
- 首次 `npm install` 约 1–3 分钟；不需要 Python。
