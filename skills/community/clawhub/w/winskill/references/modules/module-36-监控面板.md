---
id: module-36
name: 单文件 HTML 监控面板
description: 从模块35的SQLite/CSV数据生成单文件HTML监控面板（CPU/内存/磁盘/服务四象限+趋势线），优先内嵌本地ECharts，找不到自动降级纯SVG自绘，离线打开≤2秒，只写入output目录
keywords: ['监控面板', 'HTML面板', 'ECharts', '四象限', '趋势图', 'dashboard']
permission: user
mode: readonly
subset: advanced
---

## 🆕 模块 36：单文件 HTML 监控面板

> ⚠️ 数据来自模块 35 的统一存储（SQLite WAL 或 CSV），本模块只读数据、只生成 HTML 到 `~/.workbuddy/output/winskill/`，不修改任何系统配置（守只读基因 + 死规则 13）。
>
> 💡 渲染双轨：检测到本地 ECharts 就内嵌进 HTML（交互式图表）；找不到就用**纯 SVG 自绘**趋势线。两种都是**单文件、离线、零服务端**，双击即开。

<details>
<summary>📋 展开查看：模块 36：单文件 HTML 监控面板</summary>

### 36.1 生成面板

```powershell
# ===== 生成单文件 HTML 监控面板 =====
$outDir = "$env:USERPROFILE\.workbuddy\output\winskill"
$db  = Join-Path $outDir "metrics.db"
$csv = Join-Path $outDir "metrics.csv"
$html = Join-Path $outDir "monitor_dashboard.html"
$py  = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $py) { $py = (Get-Command py -ErrorAction SilentlyContinue).Source }
if (-not $py) { Write-Host "❌ 生成面板需要 Python（仅用标准库，无需 pip 安装）"; exit 1 }
if (-not (Test-Path $db) -and -not (Test-Path $csv)) { Write-Host "❌ 无监控数据，请先安装模块 35 并跑几次采样"; exit 1 }

# 生成器（运行时生成，读取统一存储 → 输出单文件 HTML）
$gen = @'
import sys, os, csv, json, html, glob

db_path, csv_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]

# ---------- 读数据（SQLite 优先，回退 CSV）----------
rows = []
mode = "SQLite"
try:
    import sqlite3
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        raw = conn.execute("SELECT ts,cpu,mem,disk,svc,evt FROM metrics ORDER BY ts").fetchall()
        conn.close()
        rows = [dict(ts=r[0], cpu=r[1], mem=r[2], disk=r[3], svc=r[4] or "", evt=r[5] or 0) for r in raw]
except Exception:
    mode = "CSV"
if not rows and os.path.exists(csv_path):
    mode = "CSV"
    with open(csv_path, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            def fnum(k):
                try: return float(r.get(k) or 0)
                except ValueError: return 0
            rows.append(dict(ts=r["Timestamp"], cpu=fnum("CPU_Pct"), mem=fnum("Mem_Pct"),
                             disk=fnum("Disk_Pct"), svc=r.get("SvcDown", ""), evt=fnum("EvtErr")))

if not rows:
    print("NO_DATA")
    sys.exit(1)

recent = rows[-1]
series = {k: [r[k] for r in rows] for k in ("cpu", "mem", "disk", "evt")}
labels = [r["ts"][11:16] for r in rows][-60:]
for k in series: series[k] = series[k][-60:]

# ---------- 找本地 ECharts（找到则内嵌，找不到降级 SVG）----------
echarts_js = ""
candidates = []
if os.environ.get("ECHARTS_JS"): candidates.append(os.environ["ECHARTS_JS"])
candidates += glob.glob(os.path.join(os.path.expanduser("~"), "**", "echarts.min.js"), recursive=False)
candidates += ["/usr/share/echarts/echarts.min.js", "C:/echarts/echarts.min.js"]
for p in candidates:
    if p and os.path.exists(p):
        try:
            with open(p, encoding="utf-8") as f: echarts_js = f.read()
            break
        except OSError: pass
chart_mode = "ECharts" if echarts_js else "SVG"

# ---------- SVG 降级趋势线 ----------
def svg_line(vals, color, maxv=100):
    if len(vals) < 2: return '<text x="10" y="20" fill="#888">数据点不足</text>'
    w, h, pad = 640, 150, 12
    step = (w - 2*pad) / (len(vals)-1)
    pts = " ".join("%.1f,%.1f" % (pad + i*step, h-pad-(min(float(v),maxv)/maxv)*(h-2*pad)) for i,v in enumerate(vals))
    return '<polyline fill="none" stroke="%s" stroke-width="2" points="%s"/>' % (color, pts)

# ---------- 四象限卡片 ----------
def qcard(name, val, warn, unit="%"):
    if val is None: val = 0
    level = "danger" if val >= warn else ("warn" if val >= warn*0.8 else "ok")
    color = {"ok":"#1D9E75","warn":"#BA7517","danger":"#E24B4A"}[level]
    return ('<div class="q"><div class="ql">%s</div><div class="qv" style="color:%s">%s%s</div>'
            '<div class="bar"><i style="width:%d%%;background:%s"></i></div></div>') % (
            html.escape(name), color, round(float(val),1), unit, min(int(float(val)),100), color)

svc_status = "正常" if not recent.get("svc") else "异常: " + html.escape(str(recent["svc"]))
svc_color = "#1D9E75" if not recent.get("svc") else "#E24B4A"
qsvc = ('<div class="q"><div class="ql">服务</div><div class="qv" style="color:%s;font-size:22px">%s</div>'
        '<div class="bar"><i style="width:%d%%;background:%s"></i></div></div>') % (
        svc_color, svc_status, (100 if recent.get("svc") else 0), svc_color)
quad = (qcard("CPU", recent.get("cpu"), 90) + qcard("内存", recent.get("mem"), 95) +
        qcard("磁盘", recent.get("disk"), 95) + qsvc)

if chart_mode == "ECharts":
    chart_div = '<div id="chart" style="height:260px"></div>'
    chart_js = """
<script>%s</script>
<script>
var c=echarts.init(document.getElementById('chart'));
c.setOption({animation:false,title:{text:'CPU / 内存 / 磁盘 趋势',left:'center',textStyle:{fontSize:14}},
 tooltip:{trigger:'axis'},legend:{data:['CPU','内存','磁盘'],bottom:0},
 xAxis:{type:'category',data:%s},
 yAxis:{type:'value',max:100},
 series:[{name:'CPU',type:'line',data:%s,smooth:true},
         {name:'内存',type:'line',data:%s,smooth:true},
         {name:'磁盘',type:'line',data:%s,smooth:true}]});
</script>""" % (echarts_js, json.dumps(labels), json.dumps(series["cpu"]),
                json.dumps(series["mem"]), json.dumps(series["disk"]))
else:
    chart_div = ('<div class="svgwrap"><div class="lg"><span style="color:#378ADD">━ CPU</span> '
                 '<span style="color:#1D9E75">━ 内存</span> <span style="color:#BA7517">━ 磁盘</span></div>'
                 '<svg viewBox="0 0 664 174" width="100%%">%s%s%s</svg></div>') % (
                 svg_line(series["cpu"], "#378ADD"), svg_line(series["mem"], "#1D9E75"),
                 svg_line(series["disk"], "#BA7517"))
    chart_js = ""

doc = """<!doctype html><html lang="zh"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Winskill 监控面板</title>
<style>
body{font-family:system-ui,-apple-system,"Microsoft YaHei",sans-serif;background:#F7F7F5;color:#2C2C2A;margin:0;padding:24px}
.wrap{max-width:760px;margin:0 auto}
h1{font-size:20px;font-weight:500;margin:0 0 4px}
.meta{color:#5F5E5A;font-size:12px;margin-bottom:20px}
.quads{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:20px}
.q{background:#fff;border:1px solid rgba(0,0,0,.08);border-radius:12px;padding:14px}
.ql{font-size:12px;color:#5F5E5A;margin-bottom:6px}
.qv{font-size:26px;font-weight:500}
.bar{height:5px;background:#EFEEE9;border-radius:3px;margin-top:10px;overflow:hidden}
.bar i{display:block;height:100%%;border-radius:3px}
.card{background:#fff;border:1px solid rgba(0,0,0,.08);border-radius:12px;padding:16px;margin-bottom:16px}
.lg{font-size:12px;color:#5F5E5A;margin-bottom:8px}
.svgwrap svg{display:block}
.foot{font-size:11px;color:#888;text-align:center;margin-top:12px}
</style></head><body><div class="wrap">
<h1>Winskill 监控面板</h1>
<div class="meta">数据源：%s · 采样点：%d · 生成：%s · 渲染：%s · 单文件离线</div>
<div class="quads">%s</div>
<div class="card">%s%s</div>
<div class="foot">由 winskill 生成 · 每小时可重新生成本地面板</div>
</div></body></html>""" % (
    html.escape(mode), len(rows), html.escape(__import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M")),
    chart_mode, quad, chart_div, chart_js)

with open(out_path, "w", encoding="utf-8") as f: f.write(doc)
print("PANEL_OK|%s|%s|%d" % (mode, chart_mode, len(rows)))
'@
$genPath = Join-Path $outDir "gen_dashboard.py"
Set-Content -Path $genPath -Value $gen -Encoding utf8
$result = & $py $genPath $db $csv $html

if ($result -match '^PANEL_OK') {
    $parts = $result -split '\|'
    Write-Host "✅ 面板已生成：$html"
    Write-Host "   模式：$($parts[1]) / 渲染 $($parts[2]) / $($parts[3]) 个采样点 · 双击离线打开"
} elseif ($result -match 'NO_DATA') {
    Write-Host "❌ 无有效数据，请先跑几次采样（模块 35.1）"
} else {
    Write-Host "❌ 生成失败：$result"
}
```

### 36.2 打开 / 自动刷新

```powershell
# 打开面板（默认浏览器）
$html = "$env:USERPROFILE\.workbuddy\output\winskill\monitor_dashboard.html"
if (Test-Path $html) { Start-Process $html } else { Write-Host "❌ 面板不存在，先运行 36.1 生成" }

# 如需每天自动刷新面板：注册一个每日任务，命令同 36.1（此处不自动注册，避免打扰）
```

### 36.3 ECharts 内嵌说明（可选增强）

- 想用真·ECharts 交互图表：设置环境变量 `ECHARTS_JS` 指向本机 `echarts.min.js` 路径，再跑 36.1，生成器会把它内嵌进 HTML。
- 未设置或找不到 → 自动用纯 SVG 折线，功能等价（看趋势），体积更小、打开更快。
- 两种方式都不联网、不需要服务端、不新增 `.js` 文件到 skill 仓库（守死规则 13）。

### 报错与解决

| 报错 | 原因 | 解决 |
|------|------|------|
| `生成面板需要 Python` | 未装 Python | 装官方 Python（仅标准库），或用模块 35 的 CSV 模式 + 手工查看 |
| `无监控数据` | 采样器未运行 | 先装模块 35 并手动跑一次采样 |
| 图表空白 | 数据点 <2 | 采样积累更久后再生成 |
| 打开 >2 秒 | ECharts 文件过大 | 用精简版 echarts.simple.min.js，或改 SVG 模式（不设 ECHARTS_JS） |

</details>


[↑ 返回顶部](#module-1)

---
