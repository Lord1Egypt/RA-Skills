---
id: module-38
name: 报告脱敏导出
description: 把合规报告/监控报告中的主机名、IP、MAC、域名打码后导出，供对外提交；参考wps redact双轨识别（规则+上下文），默认生成脱敏HTML/JSON到output目录，零真实IP泄露，原始报告不改动
keywords: ['脱敏', '打码', 'redact', '报告导出', 'IP打码', '主机名打码', '对外提交']
permission: user
mode: readonly
subset: advanced
---

## 🆕 模块 38：报告脱敏导出

> ⚠️ 审计报告要发给上级与检查方，**脱敏是提交动作的一部分**。本模块默认读原始报告、生成脱敏副本到 `~/.workbuddy/output/winskill/`，**不改动原始报告**（只读基因 + 死规则 13）。
>
> 🔒 双轨识别（参考 wps redact）：**规则轨**用正则匹配 IPv4/IPv6/MAC/域名/主机名；**上下文轨**在"主机/Host/计算机名/Computer"等标签后跟的值优先打码，避免误伤普通数字。

<details>
<summary>📋 展开查看：模块 38：报告脱敏导出</summary>

### 38.1 生成脱敏报告

```powershell
# ===== 报告脱敏导出（默认脱敏合规报告，可指定文件）=====
$outDir = "$env:USERPROFILE\.workbuddy\output\winskill"
$src = Join-Path $outDir "compliance_report.html"   # 可改为 monitor_dashboard.html 或任意 .md/.html/.json
if (-not (Test-Path $src)) { Write-Host "❌ 源报告不存在：$src"; exit 1 }
$dst = Join-Path $outDir "compliance_report.redacted.html"
$py = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $py) { $py = (Get-Command py -ErrorAction SilentlyContinue).Source }
if (-not $py) { Write-Host "❌ 脱敏需要 Python（仅标准库）"; exit 1 }

$redactor = @'
import sys, re, html, json

src, dst = sys.argv[1], sys.argv[2]
with open(src, encoding="utf-8") as f: text = f.read()

stats = {"ip":0, "mac":0, "host":0, "domain":0}

# ---------- 规则轨 1：IPv4（排除 0.0.0.0 / 255.255.255.255 / 版本号）----------
IPV4 = re.compile(r'(?<![\d.])(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)(?![\d.])')
def mask_ip(m):
    ip = m.group(0)
    stats["ip"] += 1
    parts = ip.split(".")
    return parts[0] + ".<redacted>." + parts[-1]   # 保留首末段便于定位，中段打码

# ---------- 规则轨 2：MAC ----------
MAC = re.compile(r'(?<![\w:])([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}(?![\w:])')
def mask_mac(m):
    stats["mac"] += 1
    return "<MAC-REDACTED>"

# ---------- 规则轨 3：域名（含公司域名，保留 TLD）----------
DOMAIN = re.compile(r'(?<![\w@.-])([a-zA-Z0-9-]+\.)+(com|cn|net|org|local|internal|corp)(?![\w-])', re.I)
def mask_domain(m):
    stats["domain"] += 1
    return "<redacted>." + m.group(2).lower()

# ---------- 上下文轨：主机名 / 计算机名标签后的值 ----------
# 标签优先匹配长词（ComputerName/HostName 在 Computer/Host 前），允许「主机 Host:」这类中英混排
HOST_LABEL = re.compile(r'(计算机名|主机名|ComputerName|HostName|Computer|Host|主机)(?:\s+[A-Za-z]+)?\s*[:：]\s*([A-Za-z0-9][\w-]{2,})', re.I)
def mask_host(m):
    stats["host"] += 1
    return m.group(1) + ": <HOST-REDACTED>"

# ---------- 执行顺序：先上下文（主机名），再结构化（MAC/IP/域名）----------
text = HOST_LABEL.sub(mask_host, text)
text = MAC.sub(mask_mac, text)
text = IPV4.sub(mask_ip, text)
text = DOMAIN.sub(mask_domain, text)

with open(dst, "w", encoding="utf-8") as f: f.write(text)
print("REDACT_OK|%s|ip=%d|mac=%d|host=%d|domain=%d" % (dst, stats["ip"], stats["mac"], stats["host"], stats["domain"]))
'@
$redPath = Join-Path $outDir "redactor.py"
Set-Content -Path $redPath -Value $redactor -Encoding utf8
$result = & $py $redPath $src $dst

if ($result -match '^REDACT_OK') {
    Write-Host "✅ 脱敏报告已生成：$dst"
    Write-Host "   $result"
    # 自检：脱敏副本里不应再有真实 IP / 主机名（与生成器同一套正则，避免漂移）
    $check = & $py -c @"
import sys,re
t=open(sys.argv[1],encoding='utf-8').read()
ip=re.compile(r'(?<![\d.])(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)(?![\d.])')
leaks=[m.group(0) for m in ip.finditer(t) if not m.group(0).startswith(('0.','127.','255.'))]
print('LEAK|'+','.join(leaks) if leaks else 'CLEAN')
"@ $dst
    if ($check -match '^LEAK\|') { Write-Host "⚠️ 检测到疑似残留 IP：$($check -replace '^LEAK\|','')，请人工复核" }
    else { Write-Host "✅ 自检通过：脱敏副本无真实 IP 泄露" }
} else { Write-Host "❌ 脱敏失败：$result" }
```

### 38.2 脱敏规则说明

| 轨 | 匹配对象 | 处理方式 | 防误伤 |
|----|----------|----------|--------|
| 上下文轨 | 计算机名/主机名/Host 标签后的值 | 整值替换为 `<HOST-REDACTED>` | 只在标签后匹配，不碰正文数字 |
| 规则轨 | IPv4 地址 | 保留首末段，中段打码 `10.<redacted>.1` | 排除 `0.*`/`127.*`/`255.*`/`.0` 网段 |
| 规则轨 | MAC 地址 | 整值 `<MAC-REDACTED>` | 六段十六进制格式校验 |
| 规则轨 | 域名（.com/.cn/.corp/.local 等） | 保留 TLD，主域打码 | 大小写不敏感 |

### 38.3 自定义规则（社区可补充）

在 `references/compliance/redact-rules.yaml` 增加条目即可扩展（如员工工号、内部项目代号），格式：
```yaml
patterns:
  - name: 工号
    regex: 'EMP-\d{6}'
    replacement: '<EMP-REDACTED>'
```

### 38.4 验收自检

| 目标 | 方式 |
|------|------|
| 脱敏报告零真实 IP 泄露 | 38.1 生成后自动跑残留 IP 正则扫描，命中即告警 |

### 报错与解决

| 报错 | 原因 | 解决 |
|------|------|------|
| `源报告不存在` | 先跑模块 37 生成报告 | 运行 37.1 合规体检 |
| `脱敏需要 Python` | 未装 Python | 装官方 Python（仅标准库） |
| 疑似残留 IP | 非常规格式（IPv6/内网特殊段） | 人工复核，或在 redact-rules.yaml 补规则 |

</details>


[↑ 返回顶部](#module-1)

---
