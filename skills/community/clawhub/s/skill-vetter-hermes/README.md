# Skill Vetter 1.1.0 - 技能安全扫描器 🔒

## 更新日志

### v1.1.0 (2026-04-12)
- ✅ 加信任等级判断 (2 级：OFFICIAL/COMMUNITY)
- ✅ 加自动拦截逻辑 (高风险强制阻止)
- ✅ 加扫描失败处理 (宁可错杀)
- ✅ 加 PowerShell 脚本 (skill_vetter.ps1)
- ✅ 优化报告输出格式

## 使用方法

### 手动扫描
```powershell
# 扫描单个技能
.\skill_vetter.ps1 -skillPath "C:\path\to\skill" -skillSource "clawhub/community/weather"

# JSON 输出 (用于自动化)
.\skill_vetter.ps1 -skillPath "C:\path\to\skill" -skillSource "clawhub/community/weather" -outputJson
```

### 集成到 clawhub install
```powershell
# 在安装前自动扫描
$scanResult = & "$PSScriptRoot\skill_vetter.ps1" -skillPath $skillPath -skillSource $source -outputJson | ConvertFrom-Json

if ($scanResult.blockDecision.block) {
    Write-Host "❌ 安装被阻止：$($scanResult.blockDecision.reason)" -ForegroundColor Red
    exit 1
}
```

## 信任等级

| 等级 | 来源 | 扫描强度 | 拦截规则 |
|------|------|---------|---------|
| 🟢 OFFICIAL | 官方技能 | 轻度 | 只拦截 EXTREME |
| 🔴 COMMUNITY | 社区技能 | 严格 | 拦截 HIGH+EXTREME |

## 风险等级

| 等级 | 含义 | 动作 |
|------|------|------|
| 🟢 LOW | 无风险 | 允许安装 |
| 🟡 MEDIUM | 低风险 | 允许安装 (带警告) |
| 🔴 HIGH | 高风险 | 阻止安装 |
| ⛔ EXTREME | 极高风险 | 阻止安装 |

## 红色标志检测

- curl/wget 到未知 URL
- eval/exec 外部输入
- base64 解码
- 凭证文件访问
- 内存文件访问
- sudo/提权
- 直接 IP 连接
- 混淆代码

## 安全原则

1. **宁可错杀，不可放过** - 扫描失败就阻止
2. **高风险强制拦截** - 不给用户确认机会
3. **安全无例外** - 官方技能也可能被篡改

---

_十三香小精灵 🌶️🧚 - 安全扫描，从不妥协_
