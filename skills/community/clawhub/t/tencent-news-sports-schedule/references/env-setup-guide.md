# tencent-news-cli API Key 配置指南

本文件中的设置、明文查看及清除命令供凭证持有人在执行查询的同一设备或沙箱账号的终端手动操作。智能体只用状态脚本验证，不执行 `apikey-get`，不索要或代填真实 Key；统一流程见 [CLI 环境与失败处理](cli-environment.md)。

## 获取 API Key

1. 打开浏览器访问 [API Key 获取页面](https://news.qq.com/exchange?scene=appkey)
2. 按页面引导完成获取

## 设置 API Key

打开终端（macOS / Linux）或 PowerShell（Windows），执行：

```sh
tencent-news-cli apikey-set YOUR_KEY
```

> `YOUR_KEY` 替换为实际获取到的 Key 值，不需要加引号。

验证：

```sh
tencent-news-cli apikey-get
```

## 清除 API Key

仅在需要重置时执行：

```sh
tencent-news-cli apikey-clear
```

## 常见问题

- **未设置 API Key / `API Key not set`** → 前往上述获取页面取得 Key，执行 `tencent-news-cli apikey-set YOUR_KEY`，再执行 `tencent-news-cli apikey-get` 验证
- **`API Key 无效` / `invalid api key` / `unauthorized` / `401` / `403` / 鉴权失败** → 当前 Key 无效、过期或无权访问；重新前往获取页面生成正确 Key，再执行设置和验证命令。不得把此类错误解释成“无数据”“额度用完”或普通网络失败
- **已执行 `apikey-set` 成功，智能体仍提示未设置** → 智能体运行环境常缺少 `SHELL` 变量，CLI 会按 `SHELL` 选择读取的 RC 文件（为空时读 `~/.profile`，zsh 读 `~/.zshrc`，bash 读 `~/.bash_profile`），与用户在终端里写入的文件不一致。不要重复执行 `apikey-set`，否则会留下多份 Key；由智能体按 [共享环境流程](cli-environment.md) 核实配置所在文件并复查；仅命中文件名不证明 Key 有效，验证成功后保持相同 shell 上下文
- **`operation not permitted`** → 确认在有写入权限的终端中执行命令
- **找不到 `tencent-news-cli` 命令** → 只说明当前 shell 的 PATH 里没有该命令，不代表未安装。用户在终端中使用时重新打开终端；智能体应以 `scripts/cli-state.sh` 的 `cliExists` 为准，不需要重开终端。仍未安装时参考 [安装指南](installation-guide.md)

> `YOUR_KEY` 仅作为占位符。真实 Key 只能由用户在本地终端填写，不应发送给智能体，也不得在回复、日志或报告中回显。
