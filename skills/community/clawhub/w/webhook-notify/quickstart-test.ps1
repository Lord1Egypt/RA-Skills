# Webhook Notify v2.0.0 快速开始测试

Write-Host "=== Webhook Notify v2.0.0 快速开始测试 ===" -ForegroundColor Cyan
Write-Host ""

# 加载函数库
Write-Host "步骤 1: 加载函数库..." -ForegroundColor Yellow
. "E:\devdir\clawd\skills\webhook-notify\webhook-functions.ps1"
Write-Host "OK 函数库加载成功" -ForegroundColor Green
Write-Host ""

# 发送测试消息
Write-Host "步骤 2: 发送测试消息..." -ForegroundColor Yellow
$testMsg = "[openclaw] Webhook Notify v2.0.0 快速开始测试成功！"
$result = Send-Webhook -Url "https://oapi.dingtalk.com/robot/send?access_token=***" -Message $testMsg

if ($result) {
    Write-Host "OK 发送成功" -ForegroundColor Green
} else {
    Write-Host "FAIL 发送失败" -ForegroundColor Red
}
Write-Host ""

# 测试连通性
Write-Host "步骤 3: 测试连通性..." -ForegroundColor Yellow
Test-Webhook-Connection -Url "https://oapi.dingtalk.com/robot/send?access_token=***"
Write-Host ""

Write-Host "=== 测试完成 ===" -ForegroundColor Cyan