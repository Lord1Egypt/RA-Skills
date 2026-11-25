# tencent-news-cli 手动安装指南

## macOS / Linux

打开终端，执行以下命令：

```sh
curl -fsSL https://mat1.gtimg.com/qqcdn/qqnews/cli/hub/tencent-news/setup.sh | sh
```

脚本会自动完成：识别系统和架构 → 下载 CLI → 验证 → 配置环境变量 → 检测 API Key 状态。

安装完成后重新打开终端（或执行 `source ~/.zshrc`），运行 `tencent-news-cli help` 确认安装成功。

智能体侧不需要重开终端：`scripts/cli-state.sh` 与 `scripts/run-cli.sh` 按固定安装路径查找 CLI，安装后直接重新执行状态脚本即可。脚本按 `$SHELL` → 系统登录 shell → 已有 RC 文件的顺序探测 shell 类型；`$SHELL` 为空的环境（CI、容器、智能体沙箱）也能正确写入环境变量块，探测全部失败时写入 `~/.profile`。

## Windows

打开 PowerShell，执行以下命令：

```powershell
irm https://mat1.gtimg.com/qqcdn/qqnews/cli/hub/tencent-news/setup.ps1 | iex
```

安装完成后重新打开 PowerShell，运行 `tencent-news-cli help` 确认安装成功。

## 故障排查

- **macOS 安全提示**（"无法打开" / "未验证的开发者"）→ 前往「系统设置 → 隐私与安全性」，点击「仍要打开」
- **Windows SmartScreen 拦截** → 在系统提示中选择「更多信息」后允许运行
- **下载失败** → 检查网络连接，确认 CDN 地址 `mat1.gtimg.com` 可达
- **`unsupported os` 或 `unsupported architecture`** → 当前平台不在支持范围内
