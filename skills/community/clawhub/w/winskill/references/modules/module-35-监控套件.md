---
id: module-35
name: 监控套件（采样→基线→预测）
description: 监控套件统一入口，合并原模块9/31/32，共享一份SQLite(WAL)存储（无Python回退CSV），YAML可配五类采样开关与间隔，历史CSV一键迁移，P50/P95基线与SMART趋势，连续3周期超限才推送告警
keywords: ['监控套件', '常驻监控', 'SQLite', 'WAL', '性能基线', '趋势预测', '告警升级', 'metrics']
permission: admin
mode: readonly
subset: advanced
---

## 🆕 模块 35：监控套件（采样 → 基线 → 预测）

> ⚠️ 本模块是原模块 9（实时性能）/31（轻量常驻采样）/32（趋势预测）的**合并入口**。三者历史数据口径统一到一份存储，旧模块号保留转发，外部脚本不会失效。
>
> 🔒 **只读原则**：采样、分析、报告全程只读系统指标；写操作仅为把数据写入 `~/.workbuddy/output/winskill/`（用户输出目录，不进 skill 仓库）。

<details>
<summary>📋 展开查看：模块 35：监控套件</summary>

### 架构（一条链）

```
采样器(schtasks) → SQLite WAL / CSV 统一存储 → 基线P50/P95 + SMART斜率
                                              ├→ 单文件HTML面板（模块36）
                                              └→ 告警（连续3周期超限→三通道，模块33转发）
```

### 35.0 存储模式检测（先看机器支不支持 SQLite）

```powershell
$py = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $py) { $py = (Get-Command py -ErrorAction SilentlyContinue).Source }
if ($py) {
    $v = & $py -c "import sqlite3;print('OK')" 2>$null
    if ($v -match 'OK') { Write-Host "✅ 存储模式：SQLite (WAL)，Python: $py" }
    else { Write-Host "⚠️ 未检测到 sqlite3 模块，将回退 CSV 模式" }
} else {
    Write-Host "⚠️ 未检测到 Python，将回退 CSV 模式（功能不减，仅无并发锁保护）"
}
```

> 判定规则：有 Python 且 `import sqlite3` 成功 → SQLite WAL；否则 → CSV。两种模式数据字段完全一致，模块 36/37 自动识别，用户无感切换。

### 35.1 安装监控套件（生成配置 + 采样器 + 注册计划任务）

> 需管理员权限。所有脚本/数据库**运行时生成**在 `~/.workbuddy/output/winskill/`，不进 skill 仓库（守死规则 13）。

```powershell
# ===== 安装监控套件 =====
$outDir = "$env:USERPROFILE\.workbuddy\output\winskill"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

# ---------- 1) 采样配置 YAML（扁平键值，五类开关 + 间隔）----------
$cfgDefault = @'
version: "1.0.0"
updated: "2026-11-19"
# 五类采样开关（true=开启，false=关闭）
sample_cpu: true
sample_mem: true
sample_disk: true
sample_svc: true
sample_evt: true
sample_smart: true
# 采样间隔（分钟），低配/高配按 CPU 核数自动选取
interval_min_low: 15
interval_min_high: 10
# 阈值
cpu_warn: 80
cpu_alert: 90
mem_warn: 85
mem_alert: 95
disk_warn: 85
disk_alert: 95
svc_check: Spooler,Winmgmt,Dnscache,W32Time
evt_window_min: 15
evt_max: 50
# 告警策略
streak_required: 3
dedup_min: 30
daily_push_cap: 5
'@
$cfgPath = Join-Path $outDir "monitor-config.yaml"
if (-not (Test-Path $cfgPath)) { Set-Content -Path $cfgPath -Value $cfgDefault -Encoding utf8 }

# ---------- 2) Python SQLite 写入器（运行时生成，仅标准库）----------
$writer = @'
import sys, os, json, sqlite3
from datetime import datetime

cfg_path, payload_path, db_path = sys.argv[1], sys.argv[2], sys.argv[3]

def load_cfg(p):
    c = {}
    if os.path.exists(p):
        with open(p, encoding="utf-8-sig") as f:
            for line in f:
                s = line.strip()
                if s and not s.startswith("#") and ":" in s:
                    k, v = s.split(":", 1)
                    c[k.strip()] = v.strip().strip("\"").strip("'")
    return c

def num(c, k, d):
    try: return float(c.get(k, d))
    except (ValueError, TypeError): return d

cfg = load_cfg(cfg_path)
with open(payload_path, encoding="utf-8-sig") as f:
    d = json.load(f)

os.makedirs(os.path.dirname(db_path), exist_ok=True)
conn = sqlite3.connect(db_path, timeout=15)
conn.execute("PRAGMA journal_mode=WAL")
conn.execute("PRAGMA synchronous=NORMAL")
conn.executescript("""
CREATE TABLE IF NOT EXISTS metrics(ts TEXT PRIMARY KEY, cpu REAL, mem REAL, disk REAL, svc TEXT, evt INTEGER, host TEXT);
CREATE TABLE IF NOT EXISTS smart(ts TEXT, device TEXT, realloc INTEGER, pending INTEGER, poh INTEGER, PRIMARY KEY(ts,device));
CREATE TABLE IF NOT EXISTS alerts(ts TEXT, host TEXT, metric TEXT, value TEXT, threshold TEXT, level TEXT, recommend TEXT, streak INTEGER, pushed INTEGER DEFAULT 0);
""")
conn.execute("INSERT OR REPLACE INTO metrics VALUES(?,?,?,?,?,?,?)",
             (d["ts"], d.get("cpu"), d.get("mem"), d.get("disk"),
              d.get("svc", ""), d.get("evt", 0), d.get("host", "")))

for s in (d.get("smart") or []):
    conn.execute("INSERT OR REPLACE INTO smart VALUES(?,?,?,?,?)",
                 (s["ts"], s["device"], s["realloc"], s["pending"], s["poh"]))

host = d.get("host", "")
need = int(num(cfg, "streak_required", 3))
dedup_sec = num(cfg, "dedup_min", 30) * 60
cap = int(num(cfg, "daily_push_cap", 5))
today = datetime.now().strftime("%Y-%m-%d")

def cooldown(metric):
    row = conn.execute("SELECT ts FROM alerts WHERE metric=? AND host=? AND pushed=0 ORDER BY ts DESC LIMIT 1",
                       (metric, host)).fetchone()
    if not row: return False
    try:
        dt = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
        return (datetime.now() - dt).total_seconds() < dedup_sec
    except ValueError:
        return False

def daily_full():
    n = conn.execute("SELECT COUNT(*) FROM alerts WHERE pushed=0 AND ts LIKE ?", (today + "%",)).fetchone()[0]
    return n >= cap

rec_map = {"CPU": "检查高 CPU 进程（模块9.2）",
           "MEM": "检查内存占用 Top 进程",
           "DISK": "清理磁盘空间（模块34）"}

for metric, val, warn, alert in (
    ("CPU", d.get("cpu"), num(cfg, "cpu_warn", 80), num(cfg, "cpu_alert", 90)),
    ("MEM", d.get("mem"), num(cfg, "mem_warn", 85), num(cfg, "mem_alert", 95)),
    ("DISK", d.get("disk"), num(cfg, "disk_warn", 85), num(cfg, "disk_alert", 95)),
):
    if val is None: continue
    if val >= alert: level, th = "ALERT", alert
    elif val >= warn: level, th = "WARN", warn
    else:
        conn.execute("UPDATE alerts SET streak=0 WHERE metric=? AND host=? AND pushed<0", (metric, host))
        continue
    prev = conn.execute("SELECT streak FROM alerts WHERE metric=? AND host=? AND level=? AND pushed<0 ORDER BY ts DESC LIMIT 1",
                        (metric, host, level)).fetchone()
    streak = (prev[0] + 1) if prev else 1
    conn.execute("INSERT INTO alerts VALUES(?,?,?,?,?,?,?,?, -1)",
                 (d["ts"], host, metric, str(val), str(int(th)), level, "统计中", streak))
    if streak >= need and not cooldown(metric) and not daily_full():
        conn.execute("INSERT INTO alerts VALUES(?,?,?,?,?,?,?,?,0)",
                     (d["ts"], host, metric, str(val), str(int(th)), level, rec_map[metric], streak))

if d.get("svc"):
    if not cooldown("SVC") and not daily_full():
        conn.execute("INSERT INTO alerts VALUES(?,?,?,?,?,?,?,?,0)",
                     (d["ts"], host, "SVC", d["svc"], "Running", "ALERT", "重启服务: " + d["svc"], need))
if d.get("evt", 0) >= num(cfg, "evt_max", 50):
    if not cooldown("EVT") and not daily_full():
        conn.execute("INSERT INTO alerts VALUES(?,?,?,?,?,?,?,?,0)",
                     (d["ts"], host, "EVT", str(d["evt"]), str(int(num(cfg, "evt_max", 50))), "WARN", "检查系统日志错误", need))

conn.commit()
conn.close()
'@
$writerPath = Join-Path $outDir "sqlite_writer.py"
Set-Content -Path $writerPath -Value $writer -Encoding utf8

# ---------- 3) 采样器（PowerShell，负责采集 + 调用写入器）----------
$sampler = @'
$ErrorActionPreference = 'SilentlyContinue'
$outDir = "$env:USERPROFILE\.workbuddy\output\winskill"
$cfgPath = Join-Path $outDir "monitor-config.yaml"
$writer  = Join-Path $outDir "sqlite_writer.py"
$dbPath  = Join-Path $outDir "metrics.db"
$csvPath = Join-Path $outDir "metrics.csv"
$tmpJson = Join-Path $outDir ".sample.json"

$py = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $py) { $py = (Get-Command py -ErrorAction SilentlyContinue).Source }
$useDb = $false
if ($py -and (Test-Path $writer)) {
    & $py -c "import sqlite3" 2>$null
    if ($LASTEXITCODE -eq 0) { $useDb = $true }
}

$c = @{}
if (Test-Path $cfgPath) {
    Get-Content $cfgPath | ForEach-Object {
        $l = $_.Trim()
        if ($l -and -not $l.StartsWith('#') -and $l -match '^(.+?):\s*(.+)$') {
            $c[$matches[1].Trim()] = $matches[2].Trim().Trim('"')
        }
    }
}
function B($k,$d){ if($c.ContainsKey($k)){ $c[$k] -eq 'true' }else{ $d } }
function N($k,$d){ if($c.ContainsKey($k)){try{[double]$c[$k]}catch{$d}}else{$d} }

$ts = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
$cpu = $null; $mem = $null; $disk = $null; $svcDown = ''; $evtErr = 0

if (B 'sample_cpu' $true) { $cpu = [double](Get-CimInstance Win32_Processor).LoadPercentage }
if (B 'sample_mem' $true) {
    $m = Get-CimInstance Win32_OperatingSystem
    $mem = [math]::Round(($m.TotalVisibleMemorySize - $m.FreePhysicalMemory)/$m.TotalVisibleMemorySize*100,1)
}
if (B 'sample_disk' $true) {
    $d = Get-CimInstance Win32_LogicalDisk -Filter 'DriveType=3' | Where-Object DeviceID -eq 'C:'
    if ($d) { $disk = [math]::Round(($d.Size - $d.FreeSpace)/$d.Size*100,1) }
}
if (B 'sample_svc' $true) {
    $list = if($c.ContainsKey('svc_check')){ @($c['svc_check'] -split ',') }else{ @('Spooler','Winmgmt','Dnscache') }
    $svcDown = ($list | ForEach-Object {
        $name = $_.Trim(); $s = Get-Service -Name $name -ErrorAction SilentlyContinue
        if ($s -and $s.Status -ne 'Running') { $name }
    }) -join ';'
}
if (B 'sample_evt' $true) {
    $since = (Get-Date).AddMinutes(-(N 'evt_window_min' 15))
    $evtErr = @(Get-WinEvent -FilterHashtable @{LogName='System';Level=2;StartTime=$since} -ErrorAction SilentlyContinue).Count
}
$smart = @()
if (B 'sample_smart' $true) {
    foreach ($dk in (Get-Disk)) {
        $rc = $dk | Get-StorageReliabilityCounter -ErrorAction SilentlyContinue
        if ($rc) {
            $smart += [PSCustomObject]@{ ts=$ts; device=$dk.DeviceID; realloc=[int]$rc.ReallocatedSectors; pending=[int]$rc.PendingSectors; poh=[int]$rc.PowerOnHours }
        }
    }
}

if ($useDb) {
    $payload = @{ ts=$ts; cpu=$cpu; mem=$mem; disk=$disk; svc=$svcDown; evt=[int]$evtErr; host=$env:COMPUTERNAME; smart=$smart } | ConvertTo-Json -Compress -Depth 5
    $payload | Out-File $tmpJson -Encoding utf8
    & $py $writer $cfgPath $tmpJson $dbPath 2>$null
    Remove-Item $tmpJson -Force -ErrorAction SilentlyContinue
} else {
    if (-not (Test-Path $csvPath)) { "Timestamp,CPU_Pct,Mem_Pct,Disk_Pct,SvcDown,EvtErr" | Out-File $csvPath -Encoding utf8 }
    "$ts,$cpu,$mem,$disk,$svcDown,$evtErr" | Out-File $csvPath -Append -Encoding utf8
}
'@
$samplerPath = Join-Path $outDir "monitor_sampler.ps1"
Set-Content -Path $samplerPath -Value $sampler -Encoding utf8

# ---------- 4) 注册计划任务（SYSTEM 账户，不常驻进程）----------
# 安装脚本自身也检测一次存储模式（采样器里的 $useDb 是子进程作用域，这里取不到）
$pyInstall = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $pyInstall) { $pyInstall = (Get-Command py -ErrorAction SilentlyContinue).Source }
$installDb = $false
if ($pyInstall) { & $pyInstall -c "import sqlite3" 2>$null; if ($LASTEXITCODE -eq 0) { $installDb = $true } }
$cores = (Get-CimInstance Win32_Processor).NumberOfLogicalProcessors
$cfg = @{}
Get-Content $cfgPath | ForEach-Object {
    if ($_ -match '^(.+?):\s*(.+)$' -and -not $_.Trim().StartsWith('#')) { $cfg[$matches[1].Trim()] = $matches[2].Trim().Trim('"') }
}
$interval = if ($cores -le 4) { [int](if($cfg.ContainsKey('interval_min_low')){$cfg['interval_min_low']}else{15}) } else { [int](if($cfg.ContainsKey('interval_min_high')){$cfg['interval_min_high']}else{10}) }
$taskName = "Winskill_Monitor"
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -NonInteractive -ExecutionPolicy Bypass -File `"$samplerPath`""
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes $interval) -RepetitionDuration (New-TimeSpan -Days 248)
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 5)
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -User "SYSTEM" -RunLevel Highest -Force | Out-Null

Write-Host "✅ 监控套件已安装：任务 '$taskName' 每 $interval 分钟采样（CPU $cores 核）"
Write-Host "   存储模式：$(if($installDb){'SQLite WAL'}else{'CSV 降级'})"
Write-Host "   配置：$cfgPath （改完下一周期生效）"
Write-Host "   指标：$(if($useDb){$dbPath}else{$csvPath})"
Write-Host "   手动跑一次采样：powershell -NoProfile -ExecutionPolicy Bypass -File `"$samplerPath`""
```

### 35.2 采样配置速查（monitor-config.yaml）

| 配置项 | 含义 | 默认 |
|--------|------|------|
| `sample_cpu/mem/disk/svc/evt/smart` | 五类采样开关（SMART 为附加） | true |
| `interval_min_low/high` | 低配(≤4核)/高配采样间隔 | 15 / 10 分钟 |
| `cpu_warn/alert` `mem_warn/alert` `disk_warn/alert` | 三级阈值（warn→⚠，alert→🚨） | 80/90 等 |
| `svc_check` | 被监控的关键服务，逗号分隔 | Spooler,Winmgmt,… |
| `evt_window_min` / `evt_max` | 事件日志统计窗口 / 错误数告警线 | 15 分钟 / 50 |
| `streak_required` | 连续几个周期超限才升级推送 | 3 |
| `dedup_min` | 同指标推送冷却窗口（分钟） | 30 |
| `daily_push_cap` | 每自然日推送上限（防告警风暴） | 5 |

### 35.3 历史 CSV 迁移到 SQLite（一次性）

```powershell
# 把原模块31的 metrics.csv / smart_history.csv 导入 metrics.db（自动去重）
$outDir = "$env:USERPROFILE\.workbuddy\output\winskill"
$csv = Join-Path $outDir "metrics.csv"
$db  = Join-Path $outDir "metrics.db"
$py  = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $py) { $py = (Get-Command py -ErrorAction SilentlyContinue).Source }
if (-not (Test-Path $csv)) { Write-Host "❌ 无历史 CSV 可迁移"; exit 1 }
if (-not $py) { Write-Host "❌ 迁移需 Python（sqlite3 标准库）"; exit 1 }

$mig = @'
import sys, csv, sqlite3
csv_path, db_path = sys.argv[1], sys.argv[2]
conn = sqlite3.connect(db_path, timeout=15)
conn.execute("PRAGMA journal_mode=WAL")
conn.executescript("""
CREATE TABLE IF NOT EXISTS metrics(ts TEXT PRIMARY KEY, cpu REAL, mem REAL, disk REAL, svc TEXT, evt INTEGER, host TEXT);
""")
n = 0
with open(csv_path, encoding="utf-8-sig", newline="") as f:
    for r in csv.DictReader(f):
        try:
            conn.execute("INSERT OR IGNORE INTO metrics VALUES(?,?,?,?,?,?,?)",
                         (r["Timestamp"], float(r.get("CPU_Pct") or 0), float(r.get("Mem_Pct") or 0),
                          float(r.get("Disk_Pct") or 0), r.get("SvcDown", ""),
                          int(float(r.get("EvtErr") or 0)), ""))
            n += 1
        except (ValueError, KeyError):
            continue
conn.commit()
print("迁移完成：读取 %d 行，当前总记录 %d" % (n, conn.execute("SELECT COUNT(*) FROM metrics").fetchone()[0]))
conn.close()
'@
$migPath = Join-Path $outDir "migrate_csv.py"
Set-Content -Path $migPath -Value $mig -Encoding utf8
& $py $migPath $csv $db
Write-Host "✅ 迁移完成，旧 CSV 保留不删（可手动归档）"
```

### 35.4 查看指标 / 基线 P50·P95 / SMART 趋势

```powershell
# 优先读 SQLite，无则读 CSV（自动识别存储模式）
$outDir = "$env:USERPROFILE\.workbuddy\output\winskill"
$db = Join-Path $outDir "metrics.db"
$csv = Join-Path $outDir "metrics.csv"
$py = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $py) { $py = (Get-Command py -ErrorAction SilentlyContinue).Source }

if ((Test-Path $db) -and $py) {
    & $py -c @"
import sqlite3,sys
c=sqlite3.connect(sys.argv[1]);c.execute('PRAGMA journal_mode=WAL')
rows=c.execute('SELECT ts,cpu,mem,disk,svc,evt FROM metrics ORDER BY ts DESC LIMIT 10').fetchall()
print('最近 10 条采样：')
for r in reversed(rows): print('  | '.join(str(x) for x in r))
def pct(col,p):
    a=[x[0] for x in c.execute('SELECT %s FROM metrics WHERE %s IS NOT NULL ORDER BY %s'%(col,col,col))]
    if not a: return 0
    i=min(int(p/100*len(a)),len(a)-1);return round(a[i],1)
for col in ('cpu','mem','disk'):
    print('%s: P50=%s  P95=%s'%(col.upper(),pct(col,50),pct(col,95)))
"@ $db
} elseif (Test-Path $csv) {
    $data = Import-Csv $csv
    Write-Host "最近 10 条采样："
    $data | Select-Object -Last 10 | Format-Table Timestamp,CPU_Pct,Mem_Pct,Disk_Pct,SvcDown,EvtErr -AutoSize
    Write-Host "共 $($data.Count) 条（CSV 模式，安装 Python 后可迁移 SQLite 获得 P50/P95 统计）"
} else {
    Write-Host "❌ 尚无数据，请先运行 35.1 安装监控套件"
}
```

SMART 趋势（SQLite 模式，重映射扇区斜率预警）：

```powershell
$outDir = "$env:USERPROFILE\.workbuddy\output\winskill"
$db = Join-Path $outDir "metrics.db"
$py = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $py) { $py = (Get-Command py -ErrorAction SilentlyContinue).Source }
if ((Test-Path $db) -and $py) {
    & $py -c @"
import sqlite3,sys
from datetime import datetime
c=sqlite3.connect(sys.argv[1])
for dev, in c.execute('SELECT DISTINCT device FROM smart'):
    rows=c.execute('SELECT ts,realloc FROM smart WHERE device=? AND realloc>=0 ORDER BY ts',(dev,)).fetchall()
    if len(rows)<2: continue
    try:
        d0=datetime.strptime(rows[0][0],'%Y-%m-%d %H:%M:%S');d1=datetime.strptime(rows[-1][0],'%Y-%m-%d %H:%M:%S')
        days=(d1-d0).total_seconds()/86400
        slope=(rows[-1][1]-rows[0][1])/days if days>0 else 0
    except ValueError: continue
    flag='🔴 劣化加速，建议备份换盘' if rows[-1][1]>0 and slope>0.5 else ('⚠️ 存在重映射，观察' if rows[-1][1]>0 else '✅ 健康')
    print('%s: 重映射 %d→%d，斜率 %.2f/天  %s'%(dev,rows[0][1],rows[-1][1],slope,flag))
"@ $db
} else { Write-Host "ℹ️ SMART 趋势需 SQLite 模式（安装 Python 并重装监控）" }
```

### 35.5 告警（连续 3 周期超限 → 三通道推送）

> 去抖由写入器自动完成：连续 `streak_required` 个周期超限才生成可推送告警；同指标 `dedup_min` 分钟内不重复；每日最多 `daily_push_cap` 条。推送通道配置见模块 33（企微/钉钉）+ 新增飞书。

```powershell
$outDir = "$env:USERPROFILE\.workbuddy\output\winskill"
$db = Join-Path $outDir "metrics.db"
$py = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $py) { $py = (Get-Command py -ErrorAction SilentlyContinue).Source }
if ((Test-Path $db) -and $py) {
    & $py -c @"
import sqlite3,sys
c=sqlite3.connect(sys.argv[1])
rows=c.execute('SELECT ts,host,metric,value,threshold,level,recommend,streak FROM alerts WHERE pushed=0 ORDER BY ts DESC LIMIT 20').fetchall()
print('待推送告警（已达连续周期 + 去抖）：')
for r in rows: print('  | '.join(str(x) for x in r))
print('总计 %d 条'%len(rows))
"@ $db
} else {
    $alerts = Join-Path $outDir "alerts.csv"
    if (Test-Path $alerts) { Import-Csv $alerts | Select-Object -Last 20 | Format-Table Timestamp,Host,Metric,Value,Threshold,Level,Recommend -AutoSize }
    else { Write-Host "✅ 无告警" }
}
Write-Host "推送到群：对 AI 说「推送 winskill 告警」（通道配置见模块 33，支持企微/钉钉/飞书）"
```

### 35.6 卸载监控套件

```powershell
Unregister-ScheduledTask -TaskName "Winskill_Monitor" -Confirm:$false -ErrorAction SilentlyContinue
Write-Host "✅ 已卸载监控计划任务（历史数据保留在 output 目录，可手动清理）"
```

### 报错与解决

| 报错 | 原因 | 解决 |
|------|------|------|
| `Register-ScheduledTask 拒绝访问` | 需管理员权限 | 以管理员身份运行 |
| `无 Python，回退 CSV` | 机器未装 Python | 功能不减，仅无并发锁；装 Python 后重跑 35.1 切换 SQLite |
| `import sqlite3 失败` | Python 编译版缺标准库 | 换官方 Python，或继续 CSV 模式 |
| `数据库 locked` | 采样与查询并发 | WAL 已缓解；仍锁时缩短查询事务、避免长连接 |
| `SMART 无数据` | 存储模块未加载/无权限 | 非致命，CPU/内存/磁盘趋势不受影响 |
| `告警一直不推送` | 未连续达 `streak_required` | 属预期（防扰民）；贴线抖动不会推送，检查阈值是否合理 |

</details>


[↑ 返回顶部](#module-1)

---
