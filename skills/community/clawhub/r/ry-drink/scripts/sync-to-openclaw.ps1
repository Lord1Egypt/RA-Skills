# 将完整 ry-drink Skill（含 tools.json + handlers）同步到 OpenClaw 容器
# 用法（PowerShell，按实际容器名修改 OPENCLAW_CONTAINER）:
#   .\scripts\sync-to-openclaw.ps1 -Container openclaw-gateway

param(
    [string]$Container = "openclaw-gateway",
    [string]$SkillSource = (Join-Path $PSScriptRoot ".."),
    [string]$TargetPath = "/home/node/.openclaw/workspace/skills/ry-drink"
)

$ErrorActionPreference = "Stop"
$SkillSource = (Resolve-Path $SkillSource).Path

Write-Host "Source: $SkillSource"
Write-Host "Target container: $Container -> $TargetPath"

docker exec $Container mkdir -p /home/node/.openclaw/workspace/skills 2>$null
docker cp "$SkillSource/." "${Container}:${TargetPath}/"

Write-Host "Synced. Verify tools.json:"
docker exec $Container ls -la "$TargetPath"
docker exec $Container test -f "$TargetPath/tools.json" && Write-Host "OK: tools.json present" || Write-Host "ERROR: tools.json missing"

Write-Host @"

Next steps:
1. Align cs-agent workspace (merchant-system install will do this), or:
   docker exec $Container sh -c 'grep workspace ~/.openclaw/agents.json || true'
2. Set skill env (or re-install ry-drink from merchant UI):
   RY_DRINK_API_BASE=http://192.168.0.66:8080/user-biz
   RY_DRINK_SAAS_ID=sf8b00e05  RY_DRINK_Tenant_ID=5  RY_DRINK_SHOP_ID=8
3. Restart gateway if needed, then test booking and check merchant-biz log for 预约订座消息已推送
"@
