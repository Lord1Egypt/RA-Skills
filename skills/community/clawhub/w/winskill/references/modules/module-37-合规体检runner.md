---
id: module-37
name: 合规体检 runner
description: 等保2.0/CIS一键体检runner，YAML清单驱动（检查项→探测命令→结构化判定），逐项自动探测输出达标/不达标/需人工核验三态HTML报告，每项附证据命令与输出摘要，不达标项链接修复映射表，只读探测写操作走确认流程
keywords: ['等保2.0', 'CIS', '合规体检', 'runner', '三态报告', 'audit', '自动探测']
permission: admin
mode: readonly
subset: advanced
---

## 🆕 模块 37：合规体检 runner（等保 2.0 / CIS）

> ⚠️ **只读探测**：runner 只执行 YAML 里的只读探测命令，不修改任何配置。修复建议走模块 38 的「清单+确认」流程，改不改永远用户说了算（守只读基因）。
>
> 🔒 **安全判定**：YAML 里的 `op` 是白名单操作符（`ge/le/eq/ne/contains/regex`），runner 用解释器执行，**不用 `Invoke-Expression` 跑任意表达式**（防注入）。

<details>
<summary>📋 展开查看：模块 37：合规体检 runner</summary>

### 37.1 一键体检（生成三态 HTML 报告）

> 需管理员权限（部分探测项）。清单来自 `references/compliance/*.yaml`，改条款只换数据文件、不改 runner 代码。

```powershell
# ===== 合规体检 runner =====
$outDir = "$env:USERPROFILE\.workbuddy\output\winskill"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$html = Join-Path $outDir "compliance_report.html"
$json = Join-Path $outDir "compliance_result.json"

# YAML 清单源（skill 仓库内，只读）——多候选目录探测，兼容安装/开发/对话三种执行环境
$candidates = @(
    "$env:USERPROFILE\.workbuddy\skills\winskill\references\compliance",
    ".\references\compliance",
    "D:\skill\winskill\references\compliance"
)
$dpHint = $candidates | Where-Object { Test-Path (Join-Path $_ 'dp-2.0.yaml') } | Select-Object -First 1
if (-not $dpHint) { Write-Host "❌ 找不到合规清单目录（dp-2.0.yaml），请确认 skill 已正确安装"; exit 1 }

# runner 用 Python（标准库，YAML 扁平解析 + 命令执行 + 白名单判定 + HTML 渲染）
$py = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $py) { $py = (Get-Command py -ErrorAction SilentlyContinue).Source }
if (-not $py) { Write-Host "❌ 合规 runner 需要 Python（仅标准库）"; exit 1 }

$runner = @'
import sys, os, json, html, re, subprocess
from datetime import datetime

items_dir, json_path, html_path = sys.argv[1], sys.argv[2], sys.argv[3]

# ---------- 极简 YAML 解析（只认本 skill 的扁平缩进结构，无需第三方库）----------
def unesc(v):
    r"""解码 YAML 双引号内的转义：双反斜杠转单反斜杠、转义引号转引号（供正则与 PowerShell 路径使用）"""
    return v.strip().strip('"').replace('\\\\', '\\').replace('\\"', '"')

def parse_yaml(path):
    """解析 compliance/*.yaml：按顶层段名(items/fixes)归入对应列表，避免修复项污染检查项"""
    doc = {"version":"-", "updated":"-", "standard":"-", "items":[], "fixes":[]}
    cur = None
    section = None
    with open(path, encoding="utf-8-sig") as f:
        for raw in f:
            line = raw.rstrip("\n")
            s = line.strip()
            if not s or s.startswith("#") or s == "---": continue
            if not line.startswith(" ") and s.endswith(":"):
                section = s[:-1].strip()          # items: / fixes: / patterns:
                if section not in doc: doc[section] = []
                continue
            m = re.match(r'^([A-Za-z_]+):\s*(.+)$', s)
            if m and not line.startswith("  "):
                doc[m.group(1)] = unesc(m.group(2))
                continue
            if s.startswith("- "):
                cur = {}
                target = section if section in doc else "items"
                doc[target].append(cur)
                s = s[2:]
                if ":" in s:
                    k,v = s.split(":",1); cur[k.strip()] = unesc(v)
                continue
            if cur is not None and ":" in s and line.startswith("    "):
                k,v = s.split(":",1)
                cur[k.strip()] = unesc(v)
    return doc

def load_all(d):
    out = []
    for fn in sorted(os.listdir(d)):
        if fn.endswith(".yaml"):
            try: out.append(parse_yaml(os.path.join(d, fn)))
            except Exception as e: print("WARN 解析失败 %s: %s" % (fn, e))
    return out

# ---------- 白名单判定解释器 ----------
OPS = {"ge": lambda a,b: a>=b, "le": lambda a,b: a<=b,
       "eq": lambda a,b: a==b, "ne": lambda a,b: a!=b,
       "contains": lambda a,b: str(b) in str(a),
       "regex": lambda a,b: re.search(str(b), str(a)) is not None}

def judge(expect, actual):
    """expect 形如 'ge 8' / 'eq true' / 'contains Success and Failure'"""
    parts = expect.split(None, 1)
    if len(parts) != 2 or parts[0] not in OPS: return None  # 无法自动判定
    op, target = parts
    a, b = actual, target
    if op in ("ge","le"):
        try: a, b = float(a), float(b)
        except (ValueError, TypeError): return None
    elif op == "eq":
        if str(b).lower() in ("true","false"):
            a = str(a).lower() in ("true","1","yes")
            b = str(b).lower() == "true"
        else:
            a, b = str(a), str(b)
    try: return OPS[op](a, b)
    except Exception: return None

# ---------- 逐项探测 ----------
def probe(item):
    cmd = item.get("check", "")
    if not cmd: return ("MANUAL", "无探测命令", "")
    # 只读白名单：命令必须以安全前缀开头
    safe = ("net ", "auditpol", "Get-", "reg query", "sc query")
    if not cmd.strip().startswith(safe):
        return ("MANUAL", "命令不在只读白名单，需人工核验", cmd)
    try:
        ps = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
        r = subprocess.run([ps,"-NoProfile","-Command",cmd], capture_output=True, text=True, timeout=30)
        out = (r.stdout or r.stderr or "").strip()
        return ("PROBED", out[:600], cmd)
    except subprocess.TimeoutExpired:
        return ("MANUAL", "探测超时（>30s），需人工核验", cmd)
    except Exception as e:
        return ("MANUAL", "探测异常: %s" % e, cmd)

results = []
for doc in load_all(items_dir):
    for it in doc["items"]:
        status, evidence, cmd = probe(it)
        if status == "MANUAL":
            verdict = "需人工核验"
        else:
            if "extract" in it:
                m = re.search(it["extract"], evidence)
                actual = m.group(1) if m and m.lastindex else evidence
            else:
                actual = evidence
            v = judge(it.get("expect",""), actual)
            verdict = "达标" if v is True else ("不达标" if v is False else "需人工核验")
        results.append({
            "standard": doc["standard"], "version": doc["version"],
            "id": it.get("id",""), "category": it.get("category",""),
            "item": it.get("item",""), "level": it.get("level",""),
            "expect": it.get("expect",""), "verdict": verdict,
            "evidence": evidence, "command": cmd,
            "fix_id": it.get("fix_id","")
        })

summary = {
    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "host": os.environ.get("COMPUTERNAME",""),
    "total": len(results),
    "pass": sum(1 for r in results if r["verdict"]=="达标"),
    "fail": sum(1 for r in results if r["verdict"]=="不达标"),
    "manual": sum(1 for r in results if r["verdict"]=="需人工核验"),
}
summary["coverage"] = round((summary["pass"]+summary["fail"])/summary["total"]*100, 1) if results else 0

with open(json_path,"w",encoding="utf-8") as f:
    json.dump({"summary":summary,"results":results}, f, ensure_ascii=False, indent=2)

# ---------- 三态 HTML 报告 ----------
def esc(x): return html.escape(str(x))
rows = ""
for r in results:
    color = {"达标":"#1D9E75","不达标":"#E24B4A","需人工核验":"#BA7517"}[r["verdict"]]
    rows += ("<tr><td>%s</td><td>%s</td><td>%s</td><td style='color:%s'>%s</td>"
             "<td><code>%s</code></td><td><pre>%s</pre></td></tr>") % (
        esc(r["standard"]), esc(r["id"]), esc(r["item"]), color, esc(r["verdict"]),
        esc(r["command"]), esc(r["evidence"][:300]))

doc = """<!doctype html><html lang="zh"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>合规体检报告</title>
<style>body{font:14px system-ui,"Microsoft YaHei",sans-serif;background:#F7F7F5;color:#2C2C2A;margin:0;padding:24px}
.wrap{max-width:1100px;margin:0 auto}h1{font-size:20px;font-weight:500}
.sum{display:flex;gap:12px;margin:16px 0}.k{background:#fff;border:1px solid rgba(0,0,0,.08);border-radius:12px;padding:12px 20px}
.k b{font-size:24px;font-weight:500;display:block}table{width:100%%;border-collapse:collapse;background:#fff}
th,td{border:1px solid #e5e5e0;padding:8px;text-align:left;font-size:12px;vertical-align:top}
th{background:#F1EFE8}td pre{margin:0;white-space:pre-wrap;word-break:break-all;font-size:11px;color:#5F5E5A}
code{font-size:11px;color:#185FA5}.foot{color:#888;font-size:11px;margin-top:12px}</style></head><body><div class="wrap">
<h1>Windows Server 合规体检报告</h1>
<div class="foot">主机 %s · 生成 %s · 单文件离线 · 只读探测</div>
<div class="sum"><div class="k">检查项<b>%d</b></div><div class="k" style="color:#1D9E75">达标<b>%d</b></div>
<div class="k" style="color:#E24B4A">不达标<b>%d</b></div><div class="k" style="color:#BA7517">人工核验<b>%d</b></div>
<div class="k">覆盖率<b>%s%%</b></div></div>
<table><tr><th>标准</th><th>条款</th><th>检查项</th><th>判定</th><th>证据命令</th><th>输出摘要</th></tr>%s</table>
<div class="foot">自动探测覆盖率=达标+不达标；其余标注人工核验。不达标项修复建议见模块38（清单+确认，绝不自动修改）。</div>
</div></body></html>""" % (
    esc(summary["host"]), esc(summary["time"]), summary["total"], summary["pass"],
    summary["fail"], summary["manual"], summary["coverage"], rows)

with open(html_path,"w",encoding="utf-8") as f: f.write(doc)
print("AUDIT_OK|%d|%d|%d|%d|%s" % (summary["total"],summary["pass"],summary["fail"],summary["manual"],summary["coverage"]))
'@
$runnerPath = Join-Path $outDir "compliance_runner.py"
Set-Content -Path $runnerPath -Value $runner -Encoding utf8
$result = & $py $runnerPath $dpHint $json $html

if ($result -match '^AUDIT_OK') {
    $p = $result -split '\|'
    Write-Host "✅ 合规体检完成：$html"
    Write-Host "   检查 $($p[1]) 项 · 达标 $($p[2]) · 不达标 $($p[3]) · 人工核验 $($p[4]) · 覆盖率 $($p[5])%"
    Write-Host "   结果 JSON：$json"
} else { Write-Host "❌ 体检失败：$result" }
```

### 37.2 查看不达标项 + 修复建议映射

```powershell
$json = "$env:USERPROFILE\.workbuddy\output\winskill\compliance_result.json"
if (Test-Path $json) {
    $r = Get-Content $json -Raw | ConvertFrom-Json
    Write-Host "`n❌ 不达标项（修复建议见 references/compliance/remediation.yaml）："
    $r.results | Where-Object verdict -eq '不达标' | Format-Table id, item, expect, fix_id -AutoSize
    Write-Host "⚠️ 修复命令仅作参考，须经「展示清单 → 用户确认」流程，runner 绝不自动执行写操作"
} else { Write-Host "❌ 先运行 37.1 体检" }
```

### 37.3 验收自检

| 目标 | 查看方式 |
|------|----------|
| 等保自动探测覆盖率 ≥70% | 报告顶部「覆盖率」，达标+不达标占比 |
| 其余明确标「人工核验」 | 报告判定列黄色项 |
| 全项体检 ≤15 分钟 | 每项探测超时 30s 上限，10~17 项串行最坏 ~8 分钟 |

### 报错与解决

| 报错 | 原因 | 解决 |
|------|------|------|
| `合规 runner 需要 Python` | 未装 Python | 装官方 Python（仅标准库），无需 pip |
| 覆盖率低 | 多数项无 extract/expect 结构化判定 | 在 YAML 补 `extract` 正则 + `expect` 三元组 |
| 某项「需人工核验」 | 命令不在只读白名单或超时 | 属安全设计，人工核对即可 |
| `auditpol 拒绝访问` | 需管理员权限 | 以管理员身份运行 |

</details>


[↑ 返回顶部](#module-1)

---
