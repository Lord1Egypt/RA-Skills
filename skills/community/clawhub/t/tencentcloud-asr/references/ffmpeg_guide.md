# Agent 指南：如何由自治 Agent 自动安装 FFmpeg

> ⚠️ **Agent 必读**：这份文档是给自治 Agent 用的，不是给终端用户看的安装教程。默认目标是 **Agent 在后台自己完成安装**，只有在自动安装被阻塞时，才向用户请求最小化协助。

## 核心原则

1. **先自治，不先求助**：当缺少 `ffmpeg` / `ffprobe` 时，Agent 必须先运行 `python3 <SKILL_DIR>/scripts/ensure_ffmpeg.py --execute`，尝试自动安装。
2. **只走系统包管理器**：优先 `apt-get`、`dnf`、`yum`、`zypper`、`brew`、`winget`、`choco`。不要默认使用 `npm`、GitHub Releases、手工下载 ZIP、第三方脚本一键安装。
3. **避免 GitHub 直拉**：在国内网络环境下，GitHub 直链、`ffmpeg-static`、手动下载预编译二进制都不是优先方案。
4. **先装 `ffprobe` 所在包，再继续 ASR**：本 Skill 的真实需求不是“勉强能跑一次识别”，而是稳定拿到时长、采样率、声道数并在必要时完成转码。因此应该确保 `ffmpeg` 与 `ffprobe` 一起可用。
5. **RHEL 系默认仓库缺包时要自动补仓库**：对 `dnf` / `yum` 场景，如果直接安装 `ffmpeg` 报“仓库里没有包”，脚本应自动尝试补 `epel-release` 和 `rpmfusion-free-release`，再重试安装。
6. **只有在安装链路被阻塞时才找用户**：例如没有可用包管理器、没有权限、公司内网拦截对应软件源，或补仓库后仍然失败。

## 推荐执行流

### 1. 先检测是否已可用

如果系统中已经同时存在 `ffmpeg` 和 `ffprobe`，直接继续，不要重复安装。

### 2. 自动安装

默认执行：

```bash
python3 <SKILL_DIR>/scripts/ensure_ffmpeg.py --execute
```

该脚本会：
- 先检测 `ffmpeg` / `ffprobe` 是否已存在
- 按系统自动选择最合适的本地包管理器
- 输出结构化结果，说明是已安装、已成功安装，还是被阻塞

### 3. 平台优先级

- **Ubuntu / Debian**：优先 `apt-get install ffmpeg`
- **RHEL / CentOS / Rocky / AlmaLinux**：先尝试 `dnf` 或 `yum install ffmpeg`；如果仓库里没有包，再自动补 `epel-release` 和 `rpmfusion-free-release`
- **openSUSE**：优先 `zypper install ffmpeg`
- **macOS**：仅当本机已经有 `brew` 时，才用 `brew install ffmpeg`
- **Windows**：优先 `winget install --id Gyan.FFmpeg -e`，其次 `choco install ffmpeg -y`

## 明确禁止的路径

以下方案默认不要走：

- `npm install -g ffmpeg-static`
- GitHub Releases 直链下载
- 手工下载 ZIP / 7z 再解压
- 在线执行陌生安装脚本
- 为了装 FFmpeg 先去额外安装另一个包管理器

这些路径的问题不是“完全不能用”，而是它们对自治 Agent 来说**网络脆弱、失败面大、可恢复性差**，尤其在国内网络环境下更明显。

## 被阻塞时的最小化协助策略

只有在 `ensure_ffmpeg.py --execute` 返回结构化失败后，Agent 才可以向用户请求协助。此时应遵循：

1. **先说结论，不讲原理**：只说“当前机器缺少音频处理组件，我已经尝试自动安装但被系统限制拦住了”。
2. **只提一个最小动作**：例如“请帮我在这台机器上授予安装权限”或“请确认系统包管理器可用”。
3. **不要甩大段命令教学**：用户不是来学习 FFmpeg 安装的。
4. **不要建议 GitHub / npm 兜底**：即使失败，也不要把高失败率方案当默认补救路线。

## Agent 对用户的推荐话术

仅在自动安装失败时，才可以用类似下面的话术：

> “我已经尝试在后台自动安装音频处理组件，但当前机器的包管理器/权限受限，暂时没法继续。请帮我放开这台机器的安装权限，或确认系统包管理器可用；一旦恢复，我会继续自动完成后续处理。”
