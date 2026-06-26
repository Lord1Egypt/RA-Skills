---
name: agent-factory
description: 创建新的 OpenClaw Agent 并自动配置飞书机器人。当用户说"帮我创建 Agent"、"新建机器人"、"添加新 agent"、"配置新机器人"时触发。用户提供：agent 名称、飞书 appId、appSecret、角色定位。执行完毕后汇报结果。
---

# agent-factory

自动创建新 OpenClaw Agent 并绑定飞书机器人。

## 输入参数

用户需提供：

| 参数 | 说明 | 示例 |
|------|------|------|
| `name` | Agent 名称（英文，无空格） | `baikexia` |
| `displayName` | 显示名称 | `百科虾` |
| `appId` | 飞书机器人 App ID | `cli_xxx` |
| `appSecret` | 飞书机器人 Secret | `xxx` |
| `identity` | 角色定位描述 | `蜗牛公司问答助手` |
| `soul` | 行为准则（可选） | `不准加没要求的功能、不准过度封装、不准瞎重构、不准假装测试通过、不准加装成功、先读再改不准盲改` |
| `skill` | 要安装的 clawhub skill 名称（可选） | `wikipedia` |

## 执行流程

### Step 1: 验证凭证

调用飞书 API 验证 appId/appSecret：

```powershell
$body = @{
  app_id = $appId
  app_secret = $appSecret
} | ConvertTo-Json

$resp = Invoke-RestMethod -Uri "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" `
  -Method POST `
  -Body $body `
  -ContentType "application/json"

if ($resp.code -ne 0) { throw "凭证无效：$($resp.msg)" }
```

### Step 2: 创建 Agent

```powershell
openclaw agents add $name --workspace "$env:USERPROFILE\.openclaw\workspace-$name"
```

### Step 3: 配置飞书账号

读取当前配置，追加新账号：

```powershell
$config = Get-Content "$env:USERPROFILE\.openclaw\openclaw.json" -Raw | ConvertFrom-Json
$config.channels.feishu.accounts | Add-Member -NotePropertyName $name -NotePropertyValue @{
  appId = $appId
  appSecret = $appSecret
  name = $displayName
}
```

### Step 4: 配置路由规则

追加 binding（如已存在则跳过）：

```powershell
$existingBinding = $config.bindings | Where-Object {
    $_.agentId -eq $name -and $_.match.accountId -eq $name
}
if (-not $existingBinding) {
    $config.bindings += @{
        type = "route"
        agentId = $name
        match = @{ channel = "feishu"; accountId = $name }
    }
}
```

### Step 5: 原子写入配置文件

**先备份，再写入临时文件，最后 Move-Item 替换**，防止写入损坏导致配置丢失：

```powershell
$configPath = "$env:USERPROFILE\.openclaw\openclaw.json"
$backupPath = "$env:USERPROFILE\.openclaw\openclaw.json.bak"
$tempPath = "$env:USERPROFILE\.openclaw\openclaw.json.tmp"

Copy-Item $configPath $backupPath -Force
$config | ConvertTo-Json -Depth 100 -Compress | Set-Content $tempPath -NoNewline -Encoding UTF8
Move-Item $tempPath $configPath -Force
```

### Step 6: 创建角色文件

在 `$env:USERPROFILE\.openclaw\workspace-{name}/` 下创建：

- `IDENTITY.md` — 名字、emoji、定位
- `SOUL.md` — 行为准则（用户提供的 soul 或默认模板）
- `AGENTS.md` — 工作手册（可选）
- `USER.md` — 用户占位符

### Step 7: 安装 Skill（如有指定）

使用 `clawhub install` 将 skill 安装到**新 agent 的 workspace** 下，而非当前 active workspace：

```powershell
clawhub install <skill-name> --workdir "$env:USERPROFILE\.openclaw\workspace-$Name"
```

注意：PowerShell 变量在字符串中需要用 `"` 包围双引号，或者先拼接路径再传入。

### Step 8: 开启工具权限

```powershell
openclaw config set channels.feishu.tools.wiki true
openclaw config set channels.feishu.tools.doc true
openclaw config set channels.feishu.tools.drive true
```

### Step 9: 重启网关

```powershell
openclaw gateway restart
```

## 完整脚本

提供两个版本：**Windows (PowerShell)** 和 **Linux/macOS (Bash + jq)**。

### Linux / macOS (Bash)

将以下脚本保存为 `create-agent.sh`，执行 `chmod +x create-agent.sh` 后运行：

```bash
#!/usr/bin/env bash
# create-agent.sh — Linux/macOS 版（需安装 jq）
set -euo pipefail

# ---------- 参数 ----------
while [[ $# -gt 0 ]]; do
  case $1 in
    --name) NAME="$2"; shift 2 ;;
    --display-name) DISPLAY_NAME="$2"; shift 2 ;;
    --app-id) APP_ID="$2"; shift 2 ;;
    --app-secret) APP_SECRET="$2"; shift 2 ;;
    --identity) IDENTITY="$2"; shift 2 ;;
    --soul) SOUL="$2"; shift 2 ;;
    --skill) SKILL="$2"; shift 2 ;;
    *) shift ;;
  esac
done

[[ -z "${NAME:-}" ]] && echo "错误：缺少 --name" && exit 1
[[ -z "${DISPLAY_NAME:-}" ]] && echo "错误：缺少 --display-name" && exit 1
[[ -z "${APP_ID:-}" ]] && echo "错误：缺少 --app-id" && exit 1
[[ -z "${APP_SECRET:-}" ]] && echo "错误：缺少 --app-secret" && exit 1
[[ -z "${IDENTITY:-}" ]] && echo "错误：缺少 --identity" && exit 1
SOUL="${SOUL:-}"
SKILL="${SKILL:-}"
OPENCLAW_DIR="${OPENCLAW_DIR:-$HOME/.openclaw}"
CONFIG_FILE="$OPENCLAW_DIR/openclaw.json"
BACKUP_FILE="$OPENCLAW_DIR/openclaw.json.bak"
WORKSPACE_DIR="$OPENCLAW_DIR/workspace-$NAME"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')

# ---------- 颜色 ----------
RED='\033[0;31m'; GREEN='\033[0;32m'; CYAN='\033[0;36m'; YELLOW='\033[1;33m'; NC='\033[0m'

# ============ Step 1: Validate Feishu credentials ============
echo -e "${CYAN}[1/9]${NC} 验证飞书凭证..."

RESP=$(curl -s -X POST 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' \
  -H 'Content-Type: application/json' \
  -d "$(jq -n --arg id "$APP_ID" --arg secret "$APP_SECRET" '{app_id: $id, app_secret: $secret}')" \
  --max-time 10) || true

CODE=$(echo "$RESP" | jq -r '.code // 99')
if [[ "$CODE" != "0" ]]; then
  MSG=$(echo "$RESP" | jq -r '.msg // "unknown error"')
  echo -e "${RED}错误：凭证无效：$MSG (code: $CODE)${NC}" >&2
  exit 1
fi
BOT_NAME=$(echo "$RESP" | jq -r '.app // "?"')
echo -e "  ${GREEN}✓${NC} 凭证有效，bot name: $BOT_NAME"

# ============ Step 2: Create Agent ============
echo -e "${CYAN}[2/9]${NC} 创建 Agent '$NAME'..."
openclaw agents add "$NAME" --workspace "$WORKSPACE_DIR" 2>&1 || {
  if ! openclaw agents add "$NAME" --workspace "$WORKSPACE_DIR" 2>&1 | grep -q "already exists"; then
    echo -e "${RED}错误：创建 Agent 失败${NC}" >&2
    exit 1
  fi
}
echo -e "  ${GREEN}✓${NC} Agent 创建完成"

# ============ Step 3: Read & backup config ============
echo -e "${CYAN}[3/9]${NC} 读取当前配置..."
cp "$CONFIG_FILE" "$BACKUP_FILE"
CONFIG=$(cat "$CONFIG_FILE")
echo -e "  ${GREEN}✓${NC} 配置已备份到 $BACKUP_FILE"

# ============ Step 4: Add Feishu account ============
echo -e "${CYAN}[4/9]${NC} 配置飞书账号..."

# Ensure accounts object exists
if ! echo "$CONFIG" | jq -e '.channels.feishu.accounts' >/dev/null 2>&1; then
  CONFIG=$(echo "$CONFIG" | jq '.channels.feishu.accounts = {}')
fi
CONFIG=$(echo "$CONFIG" | jq \
  --arg n "$NAME" \
  --arg id "$APP_ID" \
  --arg secret "$APP_SECRET" \
  --arg name "$DISPLAY_NAME" \
  '.channels.feishu.accounts[$n] = {appId: $id, appSecret: $secret, name: $name}')
echo -e "  ${GREEN}✓${NC} 账号 '$DISPLAY_NAME' 已添加"

# ============ Step 5: Add binding rule ============
echo -e "${CYAN}[5/9]${NC} 配置路由规则..."

BINDING=$(jq -n \
  --arg agentId "$NAME" \
  --arg accountId "$NAME" \
  '{type: "route", agentId: $agentId, match: {channel: "feishu", accountId: $accountId}}')

EXISTING=$(echo "$CONFIG" | jq \
  --arg agentId "$NAME" \
  --arg accountId "$NAME" \
  '.bindings[]? | select(.agentId == $agentId and .match.accountId == $accountId)')

if [[ "$EXISTING" == "null" || "$EXISTING" == "" ]]; then
  CONFIG=$(echo "$CONFIG" | jq --argjson binding "$BINDING" '.bindings += [$binding]')
  echo -e "  ${GREEN}✓${NC} 路由规则已添加"
else
  echo -e "  ${GREEN}✓${NC} 路由规则已存在，跳过"
fi

# ============ Step 6: Atomic write config ============
echo -e "${CYAN}[6/9]${NC} 保存配置（原子写入）..."
CONFIG_TMP=$(mktemp)
echo "$CONFIG" | jq '.' > "$CONFIG_TMP" && mv "$CONFIG_TMP" "$CONFIG_FILE"
echo -e "  ${GREEN}✓${NC} 配置已保存"

# ============ Step 7: Create identity files ============
echo -e "${CYAN}[7/9]${NC} 创建角色文件..."
mkdir -p "$WORKSPACE_DIR"

# IDENTITY.md
cat > "$WORKSPACE_DIR/IDENTITY.md" <<EOF
# IDENTITY.md - $DISPLAY_NAME

- **Name:** $DISPLAY_NAME
- **Creature:** $IDENTITY
- **Emoji:** 🦐
- **Avatar:** _(待定)_

---

由 agent-factory skill 于 $TIMESTAMP 自动创建。
EOF

# SOUL.md
if [[ -n "$SOUL" ]]; then
  cat > "$WORKSPACE_DIR/SOUL.md" <<EOF
# SOUL.md - $DISPLAY_NAME 的灵魂

$SOUL

---

由 agent-factory skill 于 $TIMESTAMP 自动创建。
EOF
else
  cat > "$WORKSPACE_DIR/SOUL.md" <<EOF
# SOUL.md - $DISPLAY_NAME 的灵魂

## 我是谁

我是**$DISPLAY_NAME**，$IDENTITY。

## 行事准则

- 全力帮助用户
- 不知道就说不知道，不编造
- 只做本职工作范围内的事

---

由 agent-factory skill 于 $TIMESTAMP 自动创建。
EOF
fi

# AGENTS.md
cat > "$WORKSPACE_DIR/AGENTS.md" <<EOF
# AGENTS.md - $DISPLAY_NAME 工作手册

## 角色

$IDENTITY

## 注意事项

- 保持专注，不越界
- 遇到不确定的问题，告知用户

---

由 agent-factory skill 于 $TIMESTAMP 自动创建。
EOF

# USER.md
cat > "$WORKSPACE_DIR/USER.md" <<EOF
# USER.md

- **Name:** _(待填写)_
- **What to call them:** _(待填写)_

## Context

_(随着对话积累，持续更新这里。)_
EOF

# MEMORY.md — 永久记忆（从当前 agent 复制）
if [[ -f "$HOME/.openclaw/workspace/MEMORY.md" ]]; then
  cp "$HOME/.openclaw/workspace/MEMORY.md" "$WORKSPACE_DIR/MEMORY.md"
  echo -e "  ${GREEN}✓${NC} MEMORY.md 已复制"
else
  cat > "$WORKSPACE_DIR/MEMORY.md" <<'MEMEOF'
# MEMORY.md - 长期记忆

_(随着对话积累，持续更新这里。)_
MEMEOF
  echo -e "  ${GREEN}✓${NC} MEMORY.md 已创建（空白）"
fi

echo -e "  ${GREEN}✓${NC} IDENTITY.md, SOUL.md, AGENTS.md, USER.md, MEMORY.md 已创建"

# ============ Step 7: Install skill (if specified) ============
if [[ -n "$SKILL" ]]; then
  echo -e "${CYAN}[7/9]${NC} 安装 skill '$SKILL' 到新 agent workspace..."
  clawhub install "$SKILL" --workdir "$WORKSPACE_DIR" 2>/dev/null || {
    echo -e "  ${YELLOW}⚠ skill 安装失败，继续执行（可能已存在或无需安装）${NC}"
  }
  echo -e "  ${GREEN}✓${NC} skill '$SKILL' 已安装到 $WORKSPACE_DIR/skills"
fi

# ============ Step 8: Enable tool permissions ============
echo -e "${CYAN}[8/9]${NC} 开启飞书工具权限..."
openclaw config set channels.feishu.tools.wiki true 2>/dev/null || true
echo -e "  ${GREEN}✓${NC} 飞书工具权限已开启"

# ============ Step 9: Restart gateway ============
echo -e "${CYAN}[9/9]${NC} 重启网关..."
openclaw gateway restart 2>/dev/null || true
sleep 3
echo -e "  ${GREEN}✓${NC} 网关重启请求已发送"

# ============ Done ============
echo ""
echo -e "${GREEN}✅ Agent '$DISPLAY_NAME' 创建完成！${NC}"
echo ""
echo -e "${CYAN}配置汇总：${NC}"
echo "  Agent 名称: $NAME"
echo "  显示名称: $DISPLAY_NAME"
echo "  飞书 App ID: $APP_ID"
echo "  Workspace: $WORKSPACE_DIR"
if [[ -n "$SKILL" ]]; then
  echo "  安装 skill: $SKILL -> $WORKSPACE_DIR/skills/$SKILL"
fi
echo "  路由: feishu:$NAME -> $NAME agent"
echo ""
echo -e "${YELLOW}下一步：在飞书里找到 '$DISPLAY_NAME' 机器人，向它发消息测试。${NC}"
```

### Windows (PowerShell)

将以下脚本保存为 `create-agent.ps1`，直接执行即可完成全部流程：

```powershell
#Requires -Version 5.1
param(
    [Parameter(Mandatory=$true)]
    [string]$Name,

    [Parameter(Mandatory=$true)]
    [string]$DisplayName,

    [Parameter(Mandatory=$true)]
    [string]$AppId,

    [Parameter(Mandatory=$true)]
    [string]$AppSecret,

    [Parameter(Mandatory=$true)]
    [string]$Identity,

    [string]$Soul = "",

    [string]$Skill = ""
)

$ErrorActionPreference = "Stop"

# ============ Step 1: Validate Feishu credentials ============
Write-Host "[1/8] 验证飞书凭证..."

$body = @{
    app_id = $AppId
    app_secret = $AppSecret
} | ConvertTo-Json -Compress

try {
    $resp = Invoke-RestMethod -Uri "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" `
        -Method POST `
        -Body $body `
        -ContentType "application/json" `
        -TimeoutSec 10
} catch {
    Write-Error "无法连接飞书服务器：$_"
    exit 1
}

if ($resp.code -ne 0) {
    Write-Error "凭证无效：$($resp.msg) (code: $($resp.code))"
    exit 1
}
Write-Host "  ✓ 凭证有效，bot name: $($resp.app)"

# ============ Step 2: Create Agent ============
Write-Host "[2/8] 创建 Agent '$Name'..."

$agentCmd = "openclaw agents add $Name --workspace `"$env:USERPROFILE\.openclaw\workspace-$Name`""
$addResult = Invoke-Expression $agentCmd 2>&1
if ($LASTEXITCODE -ne 0 -and $addResult -notmatch "already exists") {
    Write-Error "创建 Agent 失败：$addResult"
    exit 1
}
# 验证 workspace 目录已创建
$workspaceDir = "$env:USERPROFILE\.openclaw\workspace-$Name"
if (-not (Test-Path $workspaceDir)) {
    Write-Error "Agent 创建命令执行成功，但 workspace 目录不存在：$workspaceDir"
    exit 1
}
Write-Host "  ✓ Agent 创建完成，workspace 目录已就位"

# ============ Step 3: Read current config ============
Write-Host "[3/8] 读取当前配置..."

$configPath = "$env:USERPROFILE\.openclaw\openclaw.json"
$backupPath = "$env:USERPROFILE\.openclaw\openclaw.json.bak"
Copy-Item $configPath $backupPath -Force

$config = Get-Content $configPath -Raw | ConvertFrom-Json
Write-Host "  ✓ 配置已备份到 $backupPath"

# ============ Step 4: Add Feishu account ============
Write-Host "[4/8] 配置飞书账号..."

if (-not $config.channels.feishu.accounts) {
    $config.channels | Add-Member -NotePropertyName "accounts" -NotePropertyValue ([ordered]@{}) -Force
}
$config.channels.feishu.accounts | Add-Member -NotePropertyName $Name -NotePropertyValue ([ordered]@{
    appId = $AppId
    appSecret = $AppSecret
    name = $DisplayName
}) -Force

# 验证账号已添加
if (-not $config.channels.feishu.accounts.$Name) {
    Write-Error "账号添加失败：配置中未找到 $Name"
    exit 1
}
Write-Host "  ✓ 账号 '$DisplayName' 已添加"

# ============ Step 5: Add binding rule ============
Write-Host "[5/8] 配置路由规则..."

$newBinding = @{
    type = "route"
    agentId = $Name
    match = @{
        channel = "feishu"
        accountId = $Name
    }
}

$existingBinding = $config.bindings | Where-Object {
    $_.agentId -eq $Name -and $_.match.accountId -eq $Name
}
if (-not $existingBinding) {
    $config.bindings += $newBinding
    Write-Host "  ✓ 路由规则已添加"
} else {
    Write-Host "  ✓ 路由规则已存在，跳过"
}

# 验证绑定已加入 config 对象
$bindingCheck = $config.bindings | Where-Object { $_.agentId -eq $Name -and $_.match.accountId -eq $Name }
if (-not $bindingCheck) {
    Write-Error "绑定添加失败：配置中未找到 $Name 的路由规则"
    exit 1
}

# ============ Step 6: Atomic write config ============
Write-Host "[6/8] 保存配置（原子写入）..."
$tempPath = "$env:USERPROFILE\.openclaw\openclaw.json.tmp"
$config | ConvertTo-Json -Depth 100 -Compress | Set-Content $tempPath -NoNewline -Encoding UTF8
Move-Item $tempPath $configPath -Force

# 验证写入的配置文件有效且包含关键数据
try {
    $writtenConfig = Get-Content $configPath -Raw | ConvertFrom-Json
    if (-not $writtenConfig.agents.list) {
        throw "agents.list 缺失"
    }
    if (-not ($writtenConfig.agents.list | Where-Object { $_.id -eq $Name })) {
        throw "agents.list 中未找到 $Name"
    }
    if (-not $writtenConfig.bindings) {
        throw "bindings 缺失"
    }
    if (-not ($writtenConfig.bindings | Where-Object { $_.agentId -eq $Name })) {
        throw "bindings 中未找到 $Name"
    }
} catch {
    Write-Error "配置文件验证失败：$_。备份文件位于 $backupPath"
    exit 1
}
Write-Host "  ✓ 配置已保存并验证有效"

# ============ Step 7: Create identity files ============
Write-Host "[7/8] 创建角色文件..."

$workspaceDir = "$env:USERPROFILE\.openclaw\workspace-$Name"
if (-not (Test-Path $workspaceDir)) {
    New-Item -ItemType Directory -Path $workspaceDir -Force | Out-Null
}

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"

# IDENTITY.md
$identityContent = @"
# IDENTITY.md - $DisplayName

- **Name:** $DisplayName
- **Creature:** $Identity
- **Emoji:** 🦐
- **Avatar:** _(待定)_

---

由 agent-factory skill 于 $timestamp 自动创建。
"@

# SOUL.md
if ($Soul -ne "") {
    $soulContent = @"
# SOUL.md - $DisplayName 的灵魂

$Soul

---

由 agent-factory skill 于 $timestamp 自动创建。
"@
} else {
    $soulContent = @"
# SOUL.md - $DisplayName 的灵魂

## 我是谁

我是**$DisplayName**，$Identity。

## 行事准则

- 全力帮助用户
- 不知道就说不知道，不编造
- 只做本职工作范围内的事

---

由 agent-factory skill 于 $timestamp 自动创建。
"@
}

# AGENTS.md
$agentsContent = @"
# AGENTS.md - $DisplayName 工作手册

## 角色

$Identity

## 注意事项

- 保持专注，不越界
- 遇到不确定的问题，告知用户

---

由 agent-factory skill 于 $timestamp 自动创建。
"@

# USER.md
$userContent = @"
# USER.md

- **Name:** _(待填写)_
- **What to call them:** _(待填写)_

## Context

_(随着对话积累，持续更新这里。)_
"@

Set-Content -Path (Join-Path $workspaceDir "IDENTITY.md") -Value $identityContent -Encoding UTF8
Set-Content -Path (Join-Path $workspaceDir "SOUL.md") -Value $soulContent -Encoding UTF8
Set-Content -Path (Join-Path $workspaceDir "AGENTS.md") -Value $agentsContent -Encoding UTF8
Set-Content -Path (Join-Path $workspaceDir "USER.md") -Value $userContent -Encoding UTF8

# MEMORY.md — 永久记忆（从当前 agent 复制）
$srcMemory = Join-Path $env:USERPROFILE ".openclaw\workspace\MEMORY.md"
$destMemory = Join-Path $workspaceDir "MEMORY.md"
$srcMemoryContent = $null
if (Test-Path $srcMemory) {
    $srcMemoryContent = Get-Content $srcMemory -Raw
    # 检查是否有实质内容（不只是空白模板）
    $srcMemoryLines = ($srcMemoryContent -split "`n").Trim() | Where-Object { $_ -and $_ -notmatch "^#" -and $_ -notmatch "^_" -and $_ -notmatch "随着对话" }
    if ($srcMemoryLines.Count -gt 0) {
        Copy-Item $srcMemory $destMemory -Force
        Write-Host "  ✓ MEMORY.md 已复制（共 $($srcMemoryLines.Count) 行实质内容）"
    } else {
        Write-Host "  ⚠ 源 MEMORY.md 为空白模板，跳过复制，创建空白 MEMORY.md" -ForegroundColor Yellow
        $srcMemoryContent = $null
    }
}
if (-not $srcMemoryContent) {
    $emptyMemory = @"
# MEMORY.md - 长期记忆

_(随着对话积累，持续更新这里。)_
"@
    Set-Content -Path $destMemory -Value $emptyMemory -Encoding UTF8
    Write-Host "  ✓ MEMORY.md 已创建（空白）"
}

# 验证关键文件已写入
$requiredFiles = @("IDENTITY.md", "SOUL.md", "AGENTS.md", "USER.md", "MEMORY.md")
foreach ($file in $requiredFiles) {
    $filePath = Join-Path $workspaceDir $file
    if (-not (Test-Path $filePath)) {
        Write-Error "关键文件缺失：$filePath"
        exit 1
    }
}
Write-Host "  ✓ 所有身份文件已创建并验证存在"

Write-Host "  ✓ IDENTITY.md, SOUL.md, AGENTS.md, USER.md, MEMORY.md 已创建"

# ============ Step 7: Install skill (if specified) ============
if ($Skill -ne "") {
    Write-Host "[7/9] 安装 skill '$Skill' 到新 agent workspace..."
    $skillInstallCmd = "clawhub install $Skill --workdir `"$env:USERPROFILE\.openclaw\workspace-$Name`""
    Invoke-Expression $skillInstallCmd 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  ⚠ skill 安装失败，继续执行（可能已存在或无需安装）" -ForegroundColor Yellow
    } else {
        Write-Host "  ✓ skill '$Skill' 已安装到 $env:USERPROFILE\.openclaw\workspace-$Name\skills"
    }
}

# ============ Step 8: Enable tool permissions ============
Write-Host "[8/9] 开启飞书工具权限..."
$toolPermCmd = "openclaw config set channels.feishu.tools.wiki true"
Invoke-Expression $toolPermCmd 2>&1 | Out-Null
Write-Host "  ✓ 飞书工具权限已开启"

# ============ Step 9: Restart gateway ============
Write-Host "[9/9] 重启网关..."
openclaw gateway restart 2>&1 | Out-Null
Start-Sleep -Seconds 3
Write-Host "  ✓ 网关重启请求已发送"

# ============ Done ============
Write-Host ""
Write-Host "✅ Agent '$DisplayName' 创建完成！" -ForegroundColor Green
Write-Host ""
Write-Host "配置汇总：" -ForegroundColor Cyan
Write-Host "  Agent 名称: $Name"
Write-Host "  显示名称: $DisplayName"
Write-Host "  飞书 App ID: $AppId"
Write-Host "  Workspace: $workspaceDir"
if ($Skill -ne "") {
    Write-Host "  安装 skill: $Skill -> $workspaceDir\skills\$Skill"
}
Write-Host "  路由: feishu:$Name -> $Name agent"
Write-Host ""
Write-Host "下一步：在飞书里找到 '$DisplayName' 机器人，向它发消息测试。" -ForegroundColor Yellow
```

## 执行示例

用户说：
> 帮我创建百科虾，AppID: cli_xxx，Secret: xxx，名字是百科虾，定位是蜗牛公司问答助手

**Linux / macOS：**
```bash
chmod +x create-agent.sh
./create-agent.sh \
  --name "baikexia" \
  --display-name "百科虾" \
  --app-id "cli_xxx" \
  --app-secret "xxx" \
  --identity "蜗牛公司问答助手"
```

**Windows：**
```powershell
.\create-agent.ps1 -Name "baikexia" -DisplayName "百科虾" -AppId "cli_xxx" -AppSecret "xxx" -Identity "蜗牛公司问答助手"
```

## 错误处理

| 错误 | 处理 |
|------|------|
| 凭证无效 | 抛出 `credentials_invalid`，告知用户检查 appId/appSecret |
| Agent 已存在 | 跳过创建，保留现有配置 |
| 配置文件写入失败 | 抛出 `config_write_failed`，保留备份 |
| 路由规则冲突 | 跳过重复规则，继续执行 |

## 注意事项

- 所有 PowerShell 脚本使用 UTF-8 BOM 编码
- 配置文件写入前自动备份到 `openclaw.json.bak`
- 配置写入使用原子操作（temp 文件 + Move-Item / mv），防止写入损坏
- PowerShell 使用 `-Depth 100` 确保完整序列化所有嵌套对象
- Agent 名称只能包含字母、数字、连字符
- 路由规则重复时会跳过，不会覆盖已有规则
