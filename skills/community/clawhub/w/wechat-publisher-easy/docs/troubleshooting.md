# 微信公众号发布技能 - 故障排查手册

**版本：** V1.1.3  
**更新日期：** 2026-03-28  

---

## 📋 目录

1. [IP 白名单问题](#1-ip 白名单问题)
2. [Token 获取失败](#2-token 获取失败)
3. [定时任务执行失败](#3-定时任务执行失败)
4. [草稿创建失败](#4-草稿创建失败)
5. [中文乱码问题](#5-中文乱码问题)
6. [环境变量问题](#6-环境变量问题)
7. [网络访问问题](#7-网络访问问题)
8. [快速诊断命令](#8-快速诊断命令)

---

## 1. IP 白名单问题

### 症状

```
错误码：40164
错误信息：invalid ip xxx.xxx.xxx.xxx, not in whitelist
```

### 原因

微信公众号后台未将当前出口 IP 添加到白名单，API 调用被拒绝。

### 解决方案

**步骤 1：查看当前出口 IP**

```bash
# Windows PowerShell
Invoke-RestMethod -Uri 'http://ip-api.com/json/' | Select-Object -ExpandProperty query

# macOS / Linux
curl -s http://ip-api.com/json/ | grep -o '"query":"[^"]*"' | cut -d'"' -f4

# 或直接访问网页
https://ip-api.com/
```

**步骤 2：添加到微信白名单**

1. 登录微信公众号后台：https://mp.weixin.qq.com/
2. 左侧菜单：**设置 → 公众号设置 → 功能设置**
3. 找到 **IP 白名单** 配置项
4. 点击"修改"，添加步骤 1 中获取的 IP
5. 保存配置

**步骤 3：验证**

```bash
# 等待 5 分钟后重新执行
openclaw skill run wechat-publisher
```

### 注意事项

- ⚠️ **家用宽带 IP 可能动态变化**，如 IP 变更需重新添加
- ⚠️ **公司网络通常 IP 固定**，添加一次即可
- ⚠️ **使用代理/VPN 时**，出口 IP 为代理服务器 IP
- ✅ 建议同时添加当前 IP 和备用 IP（如公司 + 家里）

---

## 2. Token 获取失败

### 症状

```
错误：invalid appid
错误：invalid appsecret
错误：43101 (user refuse to accept the msg)
```

### 原因

| 错误信息 | 可能原因 | 解决方案 |
|----------|----------|----------|
| `invalid appid` | AppID 配置错误 | 检查 config.json 中 app_id 是否正确 |
| `invalid appsecret` | AppSecret 错误或已重置 | 重新生成并更新配置 |
| `43101` | 公众号未认证 | 完成公众号认证 |

### 解决方案

**检查 AppID 和 AppSecret：**

1. 登录微信公众号后台
2. 左侧菜单：**开发 → 基本配置**
3. 找到"公众号开发信息"
4. 核对 AppID 是否正确
5. 如 AppSecret 遗忘，点击"重置"生成新的

**更新配置：**

```bash
# 方式 1：交互式配置
openclaw skill config wechat-publisher

# 方式 2：命令行配置
openclaw skill config wechat-publisher --app-id wxebff9eadface1489 --app-secret xxxxxxxx

# 方式 3：手动编辑配置文件
# Windows: notepad $env:USERPROFILE\.agents\skills\wechat-publisher\config\config.json
# macOS/Linux: nano ~/.agents/skills/wechat-publisher/config/config.json
```

---

## 3. 定时任务执行失败

### 症状

```
定时任务状态：error
最后执行：5h ago
下次执行：in 19h
```

### 原因排查

**排查步骤 1：查看任务状态**

```bash
# 列出所有定时任务
openclaw cron list

# 查看任务详情
openclaw cron list | findstr "每日 AI 新闻"
```

**排查步骤 2：检查任务日志**

```bash
# 查看结果文件
Get-ChildItem ~/.openclaw/workspace/memory/wechat-scheduled-*.md | Sort-Object LastWriteTime -Descending | Select-Object -First 1 | Get-Content
```

**排查步骤 3：手动执行测试**

```bash
# 立即执行一次
openclaw skill run wechat-publisher

# 或手动运行脚本
powershell -ExecutionPolicy Bypass -File ~/.openclaw/workspace/memory/wechat-publish-daily.ps1
```

### 常见原因

| 原因 | 症状 | 解决方案 |
|------|------|----------|
| IP 白名单未配置 | 40164 错误 | 添加 IP 到白名单 |
| 环境变量不可用 | Token 获取失败 | 使用硬编码密钥脚本 |
| 脚本编码问题 | 解析错误 | 使用 UTF8 无 BOM 编码 |
| 网络超时 | 连接失败 | 检查网络连接 |

---

## 4. 草稿创建失败

### 症状

```
错误：40007 (invalid media id)
错误：45009 (reach max api daily quota limit)
错误：46003 (file not exist)
```

### 原因和解决方案

| 错误码 | 错误信息 | 原因 | 解决方案 |
|--------|----------|------|----------|
| `40007` | invalid media id | 封面图素材 ID 无效 | 重新上传封面图或使用默认值 |
| `45009` | api daily quota limit | API 调用次数超限 | 等待次日或申请提升配额 |
| `46003` | file not exist | 素材不存在 | 检查素材 ID 是否正确 |

### 获取封面图素材 ID

**方式 1：使用公众号已有素材**

1. 登录公众号后台
2. 左侧菜单：**内容与互动 → 素材管理**
3. 找到需要的图片，点击查看
4. 从 URL 中提取 media_id

**方式 2：上传新素材**

```bash
# 使用微信 API 上传
# 见 wechat-publish-final-procedure.md
```

---

## 5. 中文乱码问题

### 症状

```
发布内容显示为： 定时发布成功
标题乱码：AI ձ
```

### 原因

PowerShell 脚本编码不是 UTF-8，或文件保存时使用了错误编码。

### 解决方案

**确保脚本使用 UTF-8 编码：**

```powershell
# 脚本开头添加
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 写入文件时指定编码
Set-Content -Path $file -Value $content -Encoding UTF8
```

**检查文件编码：**

```bash
# PowerShell
Get-Content file.ps1 -Encoding UTF8

# 或使用 Notepad++ 查看编码
# 菜单：编码 → 转为 UTF-8 无 BOM 编码格式
```

---

## 6. 环境变量问题

### 症状

```
错误：Cannot bind argument to parameter 'Path' because it is null.
错误：The term 'WECHAT_APP_SECRET' is not recognized
```

### 原因

定时任务在隔离会话中运行，无法访问主会话的环境变量。

### 解决方案

**方案 1：使用硬编码密钥（推荐）**

在脚本中直接写入 AppID 和 AppSecret：

```powershell
$AppId = "wxebff9eadface1489"
$AppSecret = "44c10204ceb1bfb3f7ac096754976454"
```

**方案 2：配置文件存储**

将配置写入文件而非环境变量：

```json
{
  "app_id": "wxebff9eadface1489",
  "app_secret": "44c10204ceb1bfb3f7ac096754976454"
}
```

---

## 7. 网络访问问题

### 症状

```
错误：Unable to connect to the remote server
错误：A connection attempt failed
错误：Connection timed out
```

### 原因排查

**检查网络连接：**

```bash
# 测试微信 API 连通性
Test-NetConnection api.weixin.qq.com -Port 443

# 或使用 curl
curl -I https://api.weixin.qq.com/
```

**检查代理配置：**

```bash
# Windows
netsh winhttp show proxy

# 如有代理，可能需要绕过
set NO_PROXY=*.weixin.qq.com,api.weixin.qq.com
```

**检查防火墙：**

```bash
# Windows 防火墙
netsh advfirewall firewall show rule name=all | findstr "WeChat"
```

---

## 8. 快速诊断命令

### 一键诊断脚本

```powershell
# 保存为 diagnose.ps1 并执行

Write-Host "=== 微信公众号发布技能诊断 ===" -ForegroundColor Cyan

# 1. 检查出口 IP
Write-Host "`n[1] 出口 IP:" -ForegroundColor Yellow
$ip = Invoke-RestMethod -Uri 'http://ip-api.com/json/'
Write-Host "  IP: $($ip.query)"
Write-Host "  ISP: $($ip.isp)"
Write-Host "  地区：$($ip.country) $($ip.regionName) $($ip.city)"

# 2. 检查微信 API 连通性
Write-Host "`n[2] 微信 API 连通性:" -ForegroundColor Yellow
try {
    $test = Invoke-RestMethod -Uri 'https://api.weixin.qq.com/' -TimeoutSec 5
    Write-Host "  ✅ 可访问" -ForegroundColor Green
} catch {
    Write-Host "  ❌ 无法访问：$($_.Exception.Message)" -ForegroundColor Red
}

# 3. 检查配置文件
Write-Host "`n[3] 配置文件:" -ForegroundColor Yellow
$configPath = "$env:USERPROFILE\.agents\skills\wechat-publisher\config\config.json"
if (Test-Path $configPath) {
    $config = Get-Content $configPath | ConvertFrom-Json
    Write-Host "  文件：$configPath"
    Write-Host "  AppID: $($config.app_id)"
    Write-Host "  AppSecret: $($config.app_secret.Substring(0,8))******"
} else {
    Write-Host "  ❌ 配置文件不存在" -ForegroundColor Red
}

# 4. 检查定时任务
Write-Host "`n[4] 定时任务状态:" -ForegroundColor Yellow
try {
    $cron = & openclaw cron list 2>$null | ConvertFrom-Json
    foreach ($task in $cron) {
        if ($task.name -like "*微信*") {
            Write-Host "  任务：$($task.name)"
            Write-Host "  状态：$($task.status)"
            Write-Host "  下次执行：$($task.nextRunAt)"
        }
    }
} catch {
    Write-Host "  无法获取定时任务状态"
}

Write-Host "`n=== 诊断完成 ===" -ForegroundColor Cyan
```

### 诊断检查清单

- [ ] 出口 IP 已添加到微信白名单
- [ ] AppID 和 AppSecret 配置正确
- [ ] 网络连接正常
- [ ] 定时任务状态为"ok"
- [ ] 脚本文件编码为 UTF-8
- [ ] 公众号已认证

---

## 📞 获取帮助

如以上方法无法解决问题，请通过以下方式联系技术支持：

| 渠道 | 联系方式 | 响应时间 |
|------|----------|----------|
| **文档** | https://docs.openclaw.ai | - |
| **邮箱** | support@wechat-publisher.ai | 24 小时 |
| **微信** | 关注公众号"小蛋蛋助手" | 工作日 9:00-18:00 |
| **GitHub** | https://github.com/403914291 | 24 小时 |

**联系时请提供：**
1. 错误信息截图
2. 诊断脚本输出
3. 操作系统版本
4. 技能版本

---

_本手册最后更新：2026-03-28_  
_技能版本：V1.1.3_
