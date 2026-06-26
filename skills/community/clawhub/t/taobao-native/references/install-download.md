# 淘宝桌面版：安装包下载与安装（Reference）

> **何时阅读本文**：仅在 **用户明确表示要安装/重装** 时按此执行。默认购物任务**不要**主动帮用户下载安装。

## 原则

**不要主动给用户下载安装**（除非用户提出或已陷入无法继续的装机场景）。

## 基础地址 {base}

```
https://tblifecdn.taobao.com/taobaopc/ai/latest
```

## 目录组织

```
{base}/taobao-setup-{platform}-{arch}.{ext}
```

| 片段 | 取值 | 说明 |
|------|------|------|
| `platform` | `win7` \| `win10` \| `darwin` | Windows 按最低兼容分支区分；macOS 固定 `darwin` |
| `arch` | `x64` \| `arm64` | Windows 为 `x64`；Apple Silicon 为 `arm64`，Intel Mac 为 `x64` |
| `ext` | `.exe` \| `.dmg`  | Windows 用 `.exe`；macOS 用 `.dmg`|

## 下载安装逻辑

1. 根据当前平台、架构下载安装包；
2. 安装：
   - Windows 可以通过 `powershell -Command "Start-Process -FilePath '{download path}' -ArgumentList '/S'"` 等命令运行安装向导；注意不要使用 `-Wait`，安装完成后程序会自动启动，需要轮询查看是否启动，进程名是「淘宝桌面版」；
   - macOS 挂载 `.dmg` 拖拽或使用提供的安装流程。
3. 启动：若没自动启动，
   - Windows 执行 `taobao-native launch`；
   - macOS 执行 `open -a /Applications/淘宝桌面版.app`；
