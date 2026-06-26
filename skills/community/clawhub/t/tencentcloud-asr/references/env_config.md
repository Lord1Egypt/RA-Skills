# 腾讯云 ASR 环境变量配置

## 何时阅读本文档

仅在以下情况阅读：

- 用户明确要求手工配置环境变量
- 用户要求“给我详细配置步骤”
- Agent 不能代为注入当前命令环境，必须改走手工配置

如果只是单次任务，优先在当前命令或当前子进程里临时注入，不要默认改用户的 shell profile。

## 必要凭证

- 基础识别：`TENCENTCLOUD_SECRET_ID`、`TENCENTCLOUD_SECRET_KEY`
- 极速版额外需要：`TENCENTCLOUD_APPID`

## 风险口径

- **群聊**：`❌ 这是群聊，不要把 SecretId、SecretKey、AppId 直接发出来，否则会泄漏。建议你手工配置，或者切到私聊后我再帮你配置。`
- **私聊**：`⚠️ 即使是私聊，密钥也会经过 LLM，存在泄漏风险。更建议你手工配置；如果你确认要我代配，可以把 SecretId、SecretKey 发给我；如果要用极速版，再补 AppId。`
- **无法判断**：按群聊处理。

## 手工配置命令

### macOS / Linux（当前终端临时生效）

```bash
export TENCENTCLOUD_SECRET_ID="你的SecretId"
export TENCENTCLOUD_SECRET_KEY="你的SecretKey"
export TENCENTCLOUD_APPID="你的AppId"    # 仅极速版需要
```

### macOS / Linux（写入 `~/.zshrc` 持久生效）

```bash
echo 'export TENCENTCLOUD_SECRET_ID="你的SecretId"' >> ~/.zshrc
echo 'export TENCENTCLOUD_SECRET_KEY="你的SecretKey"' >> ~/.zshrc
echo 'export TENCENTCLOUD_APPID="你的AppId"' >> ~/.zshrc
source ~/.zshrc
```

### Windows PowerShell

```powershell
$env:TENCENTCLOUD_SECRET_ID = "你的SecretId"
$env:TENCENTCLOUD_SECRET_KEY = "你的SecretKey"
$env:TENCENTCLOUD_APPID = "你的AppId"
```

## Agent 约束

- 单次任务优先“当前命令注入”，不要为了立刻执行一次识别去改 `~/.bashrc`、`~/.zshrc`
- 不要把密钥写进工作区代码
- 如果用户刚提供了密钥，配置完成后应直接进入自检或识别，不要停留在教学解释
