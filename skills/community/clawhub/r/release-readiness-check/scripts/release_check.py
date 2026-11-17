#!/usr/bin/env python3
"""上线前五分钟体检：把 Dockerfile / K8s 清单 / SQL 迁移 / OpenAPI / .env 五项检查串起来，汇总成一份报告。

用法:
  python3 scripts/release_check.py [目标目录] [--out 报告路径] [--json] [--strict]
                                   [--skip dockerfile,k8s] [--openapi-base 旧规范]

- 自动发现目标目录里的 Dockerfile*、含 kind: 的 K8s YAML、*.sql、openapi*.json/yaml、.env*；
- 逐项用子进程调用 scripts/checks/ 下的独立脚本（--json），失败不影响其他项；
- 产出 Markdown 报告：总览表 → 各项 top 问题 → 门禁结论；默认写到系统临时目录并打印绝对路径。
- 门禁三态：有 high → 不建议上线；无 high 但有「无法判断」项 → 无法判断（--strict 退出码 1，
  拿不到证据不等于通过）；全部项都有结论且无 high → 可以上线。目录里没有这类文件算「不适用」，不影响放行。
纯 Python 标准库，不联网、不执行构建、不连集群、不连数据库。
"""
import argparse
import datetime
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CHECKS_DIR = os.path.join(HERE, "checks")
SEVS = ("high", "warn", "info")
SEV_ORDER = {"high": 0, "warn": 1, "info": 2}
TOP_N = 10
MAX_SNIFF = 2 * 1024 * 1024  # 超过 2MB 的 YAML 不做内容嗅探

SKIP_DIRS = {".git", ".hg", ".svn", "node_modules", "vendor", ".venv", "venv", "__pycache__",
             "dist", "build", "target", ".idea", ".vscode", ".tox", ".mypy_cache",
             ".pytest_cache", "site-packages", ".next", ".terraform"}

ITEM_TITLES = {
    "dockerfile": ("Dockerfile 体检", "dockerfile-check"),
    "k8s": ("K8s 清单体检", "k8s-manifest-check"),
    "sql": ("SQL 迁移风险", "sql-migration-check"),
    "openapi": ("OpenAPI 破坏性变更", "openapi-breaking-diff"),
    "env": (".env 一致性", "env-sync-check"),
}
ITEM_ORDER = ["dockerfile", "k8s", "sql", "openapi", "env"]
SKIP_ALIASES = {"docker": "dockerfile", "dockerfile": "dockerfile", "df": "dockerfile",
                "k8s": "k8s", "kubernetes": "k8s", "manifest": "k8s",
                "sql": "sql", "migration": "sql", "migrations": "sql",
                "openapi": "openapi", "api": "openapi", "swagger": "openapi",
                "env": "env", "dotenv": "env"}

OPENAPI_NAME = re.compile(r"^(openapi|swagger)[\w.\-]*\.(json|ya?ml)$", re.I)
KIND_LINE = re.compile(r"^\s{0,4}kind:\s*\S", re.M)
APIVERSION_LINE = re.compile(r"^\s{0,4}apiVersion:\s*\S", re.M)
OPENAPI_MARK = re.compile(r"^\s*[\"']?(openapi|swagger)[\"']?\s*:\s*[\"']?[23]", re.M)

OPENAPI_FIX = "破坏性变更走新版本路径（如 /v2）或新增字段并保留旧字段过渡，同时在变更日志里逐条列出并通知调用方"


# ---------------------------------------------------------------- 发现

def read_head(path, limit=MAX_SNIFF):
    try:
        if os.path.getsize(path) > limit:
            return ""
        with open(path, encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return ""


def discover(root):
    """走一遍目标目录，按类型归类文件。返回相对 root 的路径列表。"""
    found = {k: [] for k in ITEM_ORDER}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".git"))
        for fn in sorted(filenames):
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, root)
            low = fn.lower()
            if fn == "Dockerfile" or fn.startswith("Dockerfile.") or low.endswith(".dockerfile"):
                found["dockerfile"].append(rel)
                continue
            if low.endswith(".sql"):
                found["sql"].append(rel)
                continue
            if OPENAPI_NAME.match(fn):
                found["openapi"].append(rel)
                continue
            if low.endswith((".yaml", ".yml", ".json")):
                text = read_head(full)
                if OPENAPI_MARK.search(text):
                    found["openapi"].append(rel)
                elif low.endswith((".yaml", ".yml")) and KIND_LINE.search(text) and APIVERSION_LINE.search(text):
                    found["k8s"].append(rel)
    # .env 只看目标目录根部，env_sync_check.py 本身按 --src 目录找示例与环境文件
    try:
        found["env"] = sorted(f for f in os.listdir(root)
                              if f.startswith(".env") and os.path.isfile(os.path.join(root, f)))
    except OSError:
        found["env"] = []
    return found


# ---------------------------------------------------------------- 子进程

def run_check(script, args, cwd):
    """调用 checks/<script>，返回 (数据, 错误说明)。"""
    path = os.path.join(CHECKS_DIR, script)
    if not os.path.isfile(path):
        return None, f"缺少检查脚本 {script}（技能包不完整）"
    cmd = [sys.executable, path] + list(args) + ["--json"]
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=180)
    except subprocess.TimeoutExpired:
        return None, f"{script} 执行超过 180 秒，已放弃"
    except OSError as e:
        return None, f"{script} 无法执行：{e}"
    out = (p.stdout or "").strip()
    err = (p.stderr or "").strip().splitlines()
    tail = f"：{err[-1]}" if err else ""
    # 调用子脚本时不传 --strict，子脚本正常「发现问题」也是退出码 0；
    # 非 0 只可能是崩溃 / 文件读不出来 / 参数不对 —— 这是「拿不到证据」，不是「通过」。
    if p.returncode != 0:
        return None, f"{script} 以退出码 {p.returncode} 结束（崩溃或文件解析失败，不是「发现问题」）{tail}"
    if not out:
        return None, f"{script} 没有输出（退出码 {p.returncode}）{tail}"
    try:
        return json.loads(out), None
    except json.JSONDecodeError:
        return None, f"{script} 输出不是合法 JSON（退出码 {p.returncode}）{tail}"


def finding(sev, code, where, message, fix=""):
    return {"severity": sev if sev in SEVS else "info", "code": str(code or ""),
            "where": where or "", "message": message or "", "fix": fix or ""}


# ---------------------------------------------------------------- 规范校验

HTTP_METHODS = ("get", "put", "post", "delete", "options", "head", "patch", "trace")


def load_spec(path):
    """读一份 OpenAPI 规范，返回 (文档, 错误说明)。"""
    try:
        text = open(path, encoding="utf-8").read()
    except OSError as e:
        return None, f"读不出来（{e.strerror or e}）"
    except UnicodeDecodeError:
        return None, "不是 UTF-8 文本"
    if path.lower().endswith((".yaml", ".yml")):
        try:
            import yaml  # noqa: PLC0415
        except ImportError:
            return None, "YAML 规范需要 PyYAML（pip install pyyaml），或先转成 JSON"
        try:
            return yaml.safe_load(text), None
        except Exception as e:  # noqa: BLE001  PyYAML 的异常类型不统一
            return None, f"YAML 解析失败：{str(e).splitlines()[0]}"
    try:
        return json.loads(text), None
    except json.JSONDecodeError as e:
        return None, f"JSON 解析失败：{e}"


def validate_spec(path):
    """能不能拿来比对：必须解析成对象、含 openapi/swagger 版本字段、paths 非空且至少有一个接口。
    不合格返回原因字符串（调用方据此标「无法判断」），合格返回 None。"""
    doc, err = load_spec(path)
    if err:
        return err
    if not isinstance(doc, dict):
        return f"顶层不是对象（解析出 {type(doc).__name__}）"
    if not (doc.get("openapi") or doc.get("swagger")):
        return "缺少 openapi / swagger 版本字段，不像一份 OpenAPI 规范"
    paths = doc.get("paths")
    if not isinstance(paths, dict) or not paths:
        return "没有非空的 paths，规范里没有任何接口可比对"
    ops = 0
    for item in paths.values():
        if not isinstance(item, dict):
            continue
        ops += 1 if "$ref" in item else sum(1 for m in HTTP_METHODS if m in item)
    if not ops:
        return "paths 里没有任何 HTTP 方法（get/post/…），没有接口可比对"
    return None


# ---------------------------------------------------------------- 五项检查
# 每个检查返回 (findings, 执行错误, 证据缺口, 备注)；证据缺口 = (代码, 原因)，表示「无法判断」。

def check_dockerfile(root, files):
    data, err = run_check("dockerfile_check.py", files, root)
    if err:
        return [], err, None, []
    out, parsed, blank = [], 0, []
    for r in data or []:
        n = int(r.get("instructions") or 0)
        parsed += n
        if not n:
            blank.append(str(r.get("file", "?")))
        for f in r.get("findings", []):
            line = f.get("line") or 0
            where = f"{r.get('file', '?')}:L{line}" if line else str(r.get("file", "?"))
            out.append(finding(f.get("severity"), f.get("rule"), where, f.get("message"), f.get("fix")))
    if not parsed:
        return out, None, ("empty-input", f"{len(files)} 个 Dockerfile 一条指令都没解析出来"
                           f"（{', '.join(blank[:3]) or '，'.join(files[:3])}），等于没查"), []
    notes = [f"{len(blank)} 个 Dockerfile 没有解析出指令，这部分没被检查：{', '.join(blank[:5])}"] if blank else []
    return out, None, None, notes


def check_k8s(root, files):
    data, err = run_check("k8s_check.py", files, root)
    if err:
        return [], err, None, []
    data = data or {}
    out = []
    for f in data.get("findings", []):
        where = " ".join(x for x in (f.get("file"), f.get("object")) if x and x != "-")
        out.append(finding(f.get("severity"), f.get("rule"), where, f.get("message"), f.get("fix")))
    objects = int(data.get("objects") or 0)
    tmpl = sorted({f.get("file") for f in data.get("findings", []) if f.get("rule") == "K000"} - {None})
    if not objects:
        why = f"{len(files)} 个 YAML 一个对象都没解析出来，等于没查"
        if tmpl:
            why += f"；其中 {len(tmpl)} 个是 Helm/Kustomize 模板（先 helm template 渲染）：{', '.join(tmpl[:3])}"
        return out, None, ("empty-input", why), []
    notes = [f"{len(tmpl)} 个文件是模板（带 {{{{ }}}}），已跳过、没被检查：{', '.join(tmpl[:5])}"] if tmpl else []
    return out, None, None, notes


def check_sql(root, files):
    data, err = run_check("sql_migration_check.py", files, root)
    if err:
        return [], err, None, []
    out, stmts, blank = [], 0, []
    for r in data or []:
        n = int(r.get("statements") or 0)
        stmts += n
        if not n:
            blank.append(str(r.get("file", "?")))
        for f in r.get("findings", []):
            line = f.get("line") or 0
            where = f"{r.get('file', '?')}:L{line}" if line else str(r.get("file", "?"))
            msg = f.get("message", "")
            stmt = (f.get("statement") or "").strip()
            if stmt:
                msg = f"{msg}（语句 `{stmt[:90]}`）"
            out.append(finding(f.get("severity"), f.get("rule"), where, msg, f.get("fix")))
    if not stmts:
        return out, None, ("empty-input", f"{len(files)} 个 .sql 一条语句都没解析出来"
                           f"（{', '.join(blank[:3])}），等于没查"), []
    notes = [f"{len(blank)} 个 .sql 没有解析出语句，这部分没被检查：{', '.join(blank[:5])}"] if blank else []
    return out, None, None, notes


def check_openapi(root, new_spec, base_spec):
    data, err = run_check("openapi_diff.py", [base_spec, new_spec], root)
    if err:
        return [], err, None, []
    out = []
    for x in (data or {}).get("breaking", []):
        out.append(finding("high", x.get("kind"), x.get("where"), x.get("message"), OPENAPI_FIX))
    for x in (data or {}).get("non_breaking", []):
        out.append(finding("info", x.get("kind"), x.get("where"), x.get("message")))
    return out, None, None, []


def check_env(root, files):
    data, err = run_check("env_sync_check.py", ["--src", "."], root)
    if err:
        return [], err, None, []
    data = data or {}
    out = [finding(f.get("severity"), f.get("kind"), f.get("where"), f.get("message"))
           for f in data.get("findings", [])]
    example, envs = data.get("example"), data.get("envs") or []
    if not example:
        return out, None, ("no-baseline",
                           f"找到 {len(files)} 个 .env* 文件（{', '.join(files[:3])}），但没有示例文件"
                           "（.env.example / .env.sample / .env.template / .env.dist），"
                           "无法判断有没有少配变量；补一份示例文件，或用 --skip env 明确豁免"), []
    notes = []
    if not envs:
        notes.append(f"只有示例文件 `{example}`、没有可对比的环境文件，这次只做了「代码 ↔ 示例」对齐；"
                     "要查某个环境少配了什么，把该环境的 .env 放进目标目录，或单独跑 env-sync-check --env")
    return out, None, None, notes


# ---------------------------------------------------------------- 编排

def count(findings):
    return {s: sum(1 for f in findings if f["severity"] == s) for s in SEVS}


NA_REASON = {
    "dockerfile": "没有找到 Dockerfile*",
    "k8s": "没有找到同时含 apiVersion: 与 kind: 的 YAML",
    "sql": "没有找到 .sql 文件",
    "openapi": "没有找到 openapi*/swagger* 规范文件",
    "env": "没有找到 .env* 文件",
}


def run_all(root, found, skip, openapi_base):
    items = []
    for key in ITEM_ORDER:
        title, sibling = ITEM_TITLES[key]
        files = found.get(key, [])
        item = {"id": key, "title": title, "skill": sibling, "targets": files,
                "status": "na", "reason_code": "", "reason": "", "notes": [],
                "counts": {s: 0 for s in SEVS}, "findings": []}
        if key in skip:
            item.update(status="skipped", reason_code="user-skip", reason="按 --skip 跳过（显式豁免，不计入门禁）")
            items.append(item); continue
        if not files:
            item.update(status="na", reason_code="n/a", reason=NA_REASON[key] + "，本项不适用")
            items.append(item); continue
        if key == "openapi":
            res = openapi_item(root, item, files, openapi_base)
            if res is None:
                items.append(item); continue
            findings, err, gap, notes = res
        else:
            findings, err, gap, notes = {"dockerfile": check_dockerfile, "k8s": check_k8s,
                                         "sql": check_sql, "env": check_env}[key](root, files)
        findings.sort(key=lambda f: (SEV_ORDER[f["severity"]], f["where"], f["code"]))
        item["findings"] = findings
        item["counts"] = count(findings)
        item["notes"] = notes
        if err:
            # 子脚本没跑成 = 拿不到证据，按「无法判断」处理，不能算通过
            item.update(status="unknown", reason_code="check-failed", reason=err)
        elif gap:
            item.update(status="unknown", reason_code=gap[0], reason=gap[1])
        else:
            item["status"] = "ok"
        items.append(item)
    return items


def openapi_item(root, item, files, openapi_base):
    """OpenAPI 项的前置条件：要有旧版规范、两份都要是能比对的规范。
    不满足时直接把 item 标成「无法判断」并返回 None。"""
    def gap(code, reason):
        item.update(status="unknown", reason_code=code, reason=reason)
        return None

    if not openapi_base:
        return gap("no-baseline",
                   f"找到 {len(files)} 份规范（{', '.join(files[:3])}）但没有旧版本可比；"
                   "加 --openapi-base <上一版规范> 才能判断有没有破坏性变更，或用 --skip openapi 明确豁免")
    base_abs = os.path.abspath(openapi_base)
    if not os.path.isfile(base_abs):
        return gap("missing-base", f"--openapi-base 指定的文件不存在：{base_abs}")
    # 旧版规范本身可能就在目标目录里，比对时要把它排掉
    rest = [f for f in files if os.path.realpath(os.path.join(root, f)) != os.path.realpath(base_abs)]
    if not rest:
        return gap("same-file", f"--openapi-base（{base_abs}）和目标目录里唯一的规范是同一个文件，没有可比对的新版本")
    new_abs = os.path.join(root, rest[0])
    bad = [(pth, why) for pth, why in ((base_abs, validate_spec(base_abs)), (new_abs, validate_spec(new_abs))) if why]
    if bad:
        return gap("skipped-invalid",
                   "规范不合格，无法比对（拿不到证据，不计入通过）：" + "；".join(f"`{pth}` {why}" for pth, why in bad))
    item["targets"] = [f"{base_abs} → {rest[0]}"]
    findings, err, _, notes = check_openapi(root, rest[0], base_abs)
    if len(rest) > 1:
        notes.append(f"目标目录里有 {len(rest)} 份规范，只比对了 `{rest[0]}`；"
                     f"其余 {len(rest) - 1} 份没有比对：{', '.join(rest[1:4])}")
    return findings, err, None, notes


# ---------------------------------------------------------------- 报告

STATUS_ZH = {"ok": "已检查", "na": "不适用", "skipped": "已跳过", "unknown": "无法判断"}


def clip(s, n):
    """表格里截断长原因，截了就加省略号（完整原因在「各项问题」与「门禁结论」里）。"""
    s = (s or "").replace("\n", " ")
    return s if len(s) <= n else s[:n - 1].rstrip("，；、 ") + "…"


def gate(items, total):
    """三态门禁：有 high → 不建议上线；无 high 但有「无法判断」→ 无法判断（门禁拿不到证据不放行）；
    全部项都有结论且无 high → 可以上线。「不适用」和 --skip 不影响放行。"""
    unknown = [i for i in items if i["status"] == "unknown"]
    concluded = [i for i in items if i["status"] in ("ok", "unknown")]
    ran = [i for i in items if i["status"] == "ok"]
    g = {"unknown": [i["id"] for i in unknown], "checked": [i["id"] for i in ran],
         "high": total["high"], "warn": total["warn"], "info": total["info"]}
    if not concluded:
        g.update(verdict="unknown", blocked=True, headline="无法判断",
                 why="五项检查都没有给出结论——目标目录里没有可检对象，或者全被 --skip 跳过了。"
                     "确认一下目标目录是不是选错了。")
        return g
    if total["high"]:
        why = (f"有 {total['high']} 个 high 级问题（密钥泄露、锁表迁移、接口破坏性变更、配置缺失这类"
               "会直接打到线上的问题）。先把 high 清零，再跑一次本体检。")
        if unknown:
            why += f"另外还有 {len(unknown)} 项无法判断，一并补齐证据。"
        g.update(verdict="no-go", blocked=True, headline="不建议上线", why=why)
        return g
    if unknown:
        g.update(verdict="unknown", blocked=True,
                 headline=f"无法判断，缺 {len(unknown)} 项证据",
                 why=f"没有发现 high，但有 {len(unknown)} 项（{'、'.join(i['title'] for i in unknown)}）"
                     "没有拿到结论——拿不到证据不等于通过，门禁不放行（`--strict` 退出码 1）。"
                     "按上面每项写的原因补齐输入，或者用 --skip 显式豁免后再跑一次。")
        return g
    if total["warn"]:
        g.update(verdict="go-with-warn", blocked=False, headline="可以上线，但先看一眼 warn",
                 why=f"{len(ran)} 项都有结论、没有 high；{total['warn']} 个 warn 多是可复现性、资源限制、"
                     "探针、密钥疑似这类问题，确认一遍风险再发。")
        return g
    g.update(verdict="go", blocked=False, headline="可以上线",
             why=f"{len(ran)} 项都有结论，没有 high / warn 级问题。")
    return g


def render(root, items, generated):
    total = {s: sum(i["counts"][s] for i in items) for s in SEVS}
    g = gate(items, total)
    ran = [i for i in items if i["status"] == "ok"]
    unknown = [i for i in items if i["status"] == "unknown"]
    na = [i for i in items if i["status"] == "na"]
    skipped = [i for i in items if i["status"] == "skipped"]
    lines = [f"# 上线体检报告 · {os.path.basename(root.rstrip(os.sep)) or root}", "",
             f"- 目标目录：`{root}`",
             f"- 生成时间：{generated}",
             f"- 检查项：共 {len(items)} 项，有结论 {len(ran)} 项，无法判断 {len(unknown)} 项，"
             f"不适用 {len(na)} 项，按 --skip 跳过 {len(skipped)} 项", "",
             "## 一、总览", "",
             "| 检查项 | 状态 | high | warn | info | 覆盖 / 原因 |", "|---|---|---:|---:|---:|---|"]
    for i in items:
        c = i["counts"]
        if i["status"] == "ok":
            cover = f"{len(i['targets'])} 个文件" if i["id"] != "openapi" else "1 组对比"
            nums = [str(c["high"]), str(c["warn"]), str(c["info"])]
        elif i["status"] == "unknown":
            cover = f"（{i['reason_code']}）{clip(i['reason'], 70)}"
            nums = [str(c["high"]) if c["high"] else "?", str(c["warn"]) if c["warn"] else "?",
                    str(c["info"]) if c["info"] else "?"]
        else:
            cover = clip(i["reason"], 70) or "-"
            nums = ["-", "-", "-"]
        lines.append(f"| {i['title']} | {STATUS_ZH[i['status']]} | {nums[0]} | {nums[1]} | {nums[2]} | {cover} |")
    lines += [f"| **合计** | | **{total['high']}** | **{total['warn']}** | **{total['info']}** | |", "",
              "「无法判断」是没拿到证据（子脚本没跑成、输入不合格），不是「通过」；"
              "「不适用」是目录里根本没有这类文件，不影响放行。", "",
              "## 二、各项问题", ""]
    for i in items:
        lines.append(f"### {i['title']}")
        if i["status"] in ("na", "skipped"):
            lines += ["", f"> {STATUS_ZH[i['status']]}：{i['reason']}", ""]
            continue
        if i["status"] == "unknown":
            lines += ["", f"> **无法判断（{i['reason_code']}）**：{i['reason']}", "",
                      "> 这一项没有进入「通过」的判断，门禁按缺证据处理。", ""]
        else:
            lines += ["", "覆盖：" + ", ".join(f"`{t}`" for t in i["targets"][:8])
                      + (f" 等 {len(i['targets'])} 个" if len(i["targets"]) > 8 else ""), ""]
        for note in i["notes"]:
            lines += [f"注意：{note}", ""]
        if not i["findings"]:
            if i["status"] == "ok":
                lines += ["✓ 没有发现问题。", ""]
            continue
        for f in i["findings"][:TOP_N]:
            head = f"- **[{f['severity'].upper()}]** `{f['code']}`"
            if f["where"]:
                head += f" · `{f['where']}`"
            lines.append(f"{head} — {f['message']}")
            if f["fix"]:
                lines.append(f"  - → 改法：{f['fix']}")
        if len(i["findings"]) > TOP_N:
            lines.append(f"- …… 共 {len(i['findings'])} 条，此处只列前 {TOP_N} 条；"
                         f"跑 `{i['skill']}` 单项技能看全量。")
        lines.append("")
    lines += ["## 三、门禁结论", ""]
    if unknown:
        lines.append(f"缺 {len(unknown)} 项证据，逐条原因：")
        for i in unknown:
            lines.append(f"- **{i['title']}**（`{i['reason_code']}`）：{i['reason']}")
        lines.append("")
    lines += [f"**{g['headline']}** — {g['why']}", ""]
    if skipped:
        lines += [f"（{len(skipped)} 项按 --skip 显式豁免，不计入结论："
                  f"{'、'.join(i['title'] for i in skipped)}）", ""]
    lines += ["---", "",
              "本报告由 `release-readiness-check` 生成；每一项都能单独安装成技能用："
              "`dockerfile-check`、`k8s-manifest-check`、`sql-migration-check`、"
              "`openapi-breaking-diff`、`env-sync-check`。"]
    return "\n".join(lines) + "\n"


def pad(s, width):
    """终端列对齐：中日韩字符按两格宽度算。"""
    w = sum(2 if ord(c) > 0x2E7F else 1 for c in s)
    return s + " " * max(1, width - w)


def default_out(root):
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    slug = re.sub(r"[^\w.-]+", "-", os.path.basename(root.rstrip(os.sep)) or "project").strip("-") or "project"
    return os.path.join(tempfile.gettempdir(), f"release-readiness-{slug}-{stamp}.md")


# ---------------------------------------------------------------- 入口

def main():
    ap = argparse.ArgumentParser(description="上线前五分钟体检：五项检查一次跑完并汇总成报告")
    ap.add_argument("path", nargs="?", default=".", help="目标项目目录，默认当前目录")
    ap.add_argument("--out", default=None, help="Markdown 报告路径，默认写到系统临时目录")
    ap.add_argument("--json", action="store_true", help="同时把汇总结果以 JSON 打到标准输出")
    ap.add_argument("--strict", action="store_true",
                    help="有 high 或有「无法判断」项则退出码 1，用于 CI 门禁")
    ap.add_argument("--skip", default="", help="逗号分隔跳过项：dockerfile,k8s,sql,openapi,env")
    ap.add_argument("--openapi-base", default=None, help="上一版 OpenAPI 规范；给了才做破坏性变更比对")
    a = ap.parse_args()

    root = os.path.abspath(a.path)
    if not os.path.isdir(root):
        print(f"目标不是目录：{root}", file=sys.stderr); sys.exit(2)
    skip, unknown = set(), []
    for raw in a.skip.split(","):
        s = raw.strip().lower()
        if not s:
            continue
        (skip.add(SKIP_ALIASES[s]) if s in SKIP_ALIASES else unknown.append(raw.strip()))
    if unknown:
        print(f"--skip 里有不认识的项：{', '.join(unknown)}；可选值 {', '.join(ITEM_ORDER)}", file=sys.stderr)
        sys.exit(2)

    found = discover(root)
    items = run_all(root, found, skip, a.openapi_base)
    generated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    out_path = os.path.abspath(a.out or default_out(root))
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(render(root, items, generated))

    total = {s: sum(i["counts"][s] for i in items) for s in SEVS}
    g = gate(items, total)
    if a.json:
        print(json.dumps({"target": root, "generated": generated, "report": out_path,
                          "total": total, "gate": g, "items": items}, ensure_ascii=False, indent=2))
    else:
        print(f"上线体检 · {root}")
        for i in items:
            c = i["counts"]
            if i["status"] == "ok":
                tail = f"high {c['high']} / warn {c['warn']} / info {c['info']}"
            elif i["status"] == "unknown":
                tail = f"无法判断（{i['reason_code']}）：{i['reason']}"
            else:
                tail = f"{STATUS_ZH[i['status']]}：{i['reason']}"
            print(f"  {pad(i['title'], 24)}{tail}")
        print(f"\n合计：high {total['high']} / warn {total['warn']} / info {total['info']}"
              f"；无法判断 {len(g['unknown'])} 项")
        print(f"门禁：{g['headline']}")
        print(f"报告：{out_path}")
    sys.exit(1 if (a.strict and g["blocked"]) else 0)


if __name__ == "__main__":
    main()
