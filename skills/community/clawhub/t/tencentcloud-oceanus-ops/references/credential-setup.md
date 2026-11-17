# Credential Setup

How to persistently configure TencentCloud credentials for the Oceanus CLI.

> **Hard rules** (also restated in `SKILL.md → Execution Protocol → Credential safety`):
> 1. **NEVER** read, print, or echo the values of `TENCENTCLOUD_SECRET_ID` /
>    `TENCENTCLOUD_SECRET_KEY` / `TENCENTCLOUD_SECURITY_TOKEN` (no `echo`,
>    `env | grep`, `printenv`, …).
> 2. **NEVER** ask the user to paste their SecretId/SecretKey into chat.
>    Instruct them to run the configuration commands **themselves, in their
>    own local terminal**.
> 3. The CLI (`scripts/oceanus_ops.py`) reads credentials internally from the
>    environment — never pass them through command arguments.
> 4. If a tool result accidentally contains a credential-shaped value,
>    **redact it** (e.g. `***REDACTED***`) before quoting in chat.

## Sensitive variables

| Variable | Required? | Purpose |
| -------- | --------- | ------- |
| `TENCENTCLOUD_SECRET_ID`        | Yes              | Permanent / sub-account access key ID |
| `TENCENTCLOUD_SECRET_KEY`       | Yes              | Matching secret key |
| `TENCENTCLOUD_SECURITY_TOKEN`   | Only for STS     | Temporary credential token |

Get keys from the [腾讯云 CAM 控制台](https://console.cloud.tencent.com/cam/capi).

## Persistent configuration templates by OS

The user runs **exactly one** of these blocks in their own terminal,
substituting the placeholders. After writing the file, they must `source`
it (or restart the terminal / IDE) for the new shell to pick up the vars.

### macOS (default shell: zsh) — `~/.zshrc`

```bash
cat >> ~/.zshrc <<'EOF'

# TencentCloud Oceanus credentials
export TENCENTCLOUD_SECRET_ID="你的SecretId"
export TENCENTCLOUD_SECRET_KEY="你的SecretKey"
# export TENCENTCLOUD_SECURITY_TOKEN="你的Token"   # 仅临时凭证需要
EOF
chmod 600 ~/.zshrc
source ~/.zshrc
```

### Linux (bash) — `~/.bashrc` (or `~/.bash_profile` on some distros)

```bash
cat >> ~/.bashrc <<'EOF'

# TencentCloud Oceanus credentials
export TENCENTCLOUD_SECRET_ID="你的SecretId"
export TENCENTCLOUD_SECRET_KEY="你的SecretKey"
# export TENCENTCLOUD_SECURITY_TOKEN="你的Token"
EOF
chmod 600 ~/.bashrc
source ~/.bashrc
```

### Linux / macOS with fish shell — `~/.config/fish/conf.d/tencentcloud.fish`

```fish
mkdir -p ~/.config/fish/conf.d
cat > ~/.config/fish/conf.d/tencentcloud.fish <<'EOF'
set -gx TENCENTCLOUD_SECRET_ID "你的SecretId"
set -gx TENCENTCLOUD_SECRET_KEY "你的SecretKey"
# set -gx TENCENTCLOUD_SECURITY_TOKEN "你的Token"
EOF
chmod 600 ~/.config/fish/conf.d/tencentcloud.fish
source ~/.config/fish/conf.d/tencentcloud.fish
```

### Windows (PowerShell) — user-level environment (persistent)

```powershell
# 在用户级环境变量中持久化（重新打开 PowerShell / IDE 后生效）
[Environment]::SetEnvironmentVariable("TENCENTCLOUD_SECRET_ID", "你的SecretId", "User")
[Environment]::SetEnvironmentVariable("TENCENTCLOUD_SECRET_KEY", "你的SecretKey", "User")
# [Environment]::SetEnvironmentVariable("TENCENTCLOUD_SECURITY_TOKEN", "你的Token", "User")

# 当前 PowerShell 窗口立即生效（无需重启）
$env:TENCENTCLOUD_SECRET_ID  = [Environment]::GetEnvironmentVariable("TENCENTCLOUD_SECRET_ID","User")
$env:TENCENTCLOUD_SECRET_KEY = [Environment]::GetEnvironmentVariable("TENCENTCLOUD_SECRET_KEY","User")
```

### Windows (CMD) — `setx`

```cmd
setx TENCENTCLOUD_SECRET_ID  "你的SecretId"
setx TENCENTCLOUD_SECRET_KEY "你的SecretKey"
:: setx TENCENTCLOUD_SECURITY_TOKEN "你的Token"
```

> 提示：`setx` 配置后必须**重新打开 CMD/IDE** 才能加载到环境；本窗口不会立即生效。

## Handling `MissingCredentials` errors

When any command returns:

```json
{"success": false, "error": {"code": "MissingCredentials", ...}}
```

The agent MUST:

1. **Stop further command execution immediately.** Do not retry, do not
   switch to other commands, and do not try to "diagnose" the missing
   variables (no `env`, no `printenv`, no `echo $TENCENTCLOUD_*`).
2. **Detect the user's OS** from `<user_info>` (`darwin` / `linux` / `win32`)
   or via a single non-sensitive probe (`uname -s` on Unix, `echo %OS%` on
   Windows). Never read or print credential variables during this probe.
3. **Provide the matching configuration template above**, instructing the
   user to run it **themselves, in their own terminal**, and remind them
   to `source` the file or restart the terminal/IDE.
4. **Wait for the user to confirm** ("已配置") before re-running the failed
   command. Do not proceed with mutations or further reads until then.

### Reusable Chinese reply template

> 当前环境未检测到腾讯云访问凭证（`TENCENTCLOUD_SECRET_ID` /
> `TENCENTCLOUD_SECRET_KEY`）。为了一劳永逸，建议你在 **本地终端** 中执行
> 下面与你操作系统匹配的命令，把凭证写入 shell 配置文件（不要把密钥粘贴
> 到本对话）：
>
> *(根据 OS 给出对应的代码块，并把 `你的SecretId` / `你的SecretKey` 替换
>  为占位符提示)*
>
> 配置完成后：
> - macOS / Linux：执行 `source <对应配置文件>` 或重新打开终端；
> - Windows：重新打开 PowerShell / CMD / IDE。
>
> 凭证可在 [腾讯云 CAM 控制台](https://console.cloud.tencent.com/cam/capi)
> 获取。**请勿将 SecretId / SecretKey 输入到这个对话框里**，配置完成后告诉
> 我"已配置"，我会重新执行原任务。

## Success path

When credentials **are** configured (CLI returns `success: true`): never
report, summarize, or hint at the actual values — even partial fragments,
lengths, or prefixes are forbidden. Treat their existence as opaque: only
state that the operation succeeded.
