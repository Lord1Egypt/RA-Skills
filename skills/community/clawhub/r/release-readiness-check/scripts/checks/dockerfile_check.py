#!/usr/bin/env python3
"""Dockerfile 体检：基于最佳实践的静态检查，纯标准库。

用法：
  python3 dockerfile_check.py [Dockerfile 或目录 ...] [--json] [--strict]
  默认检查当前目录的 Dockerfile。--strict 时存在 high/warn 级问题则退出码 1。
"""
import argparse, json, os, re, sys

SECRET_NAME = re.compile(r"(PASSWORD|PASSWD|SECRET|TOKEN|API_?KEY|PRIVATE_?KEY|ACCESS_?KEY|CREDENTIAL)", re.I)


def parse(text):
    """返回 [(行号, 指令, 参数)]，合并续行、跳过注释与空行。"""
    out, buf, start = [], "", None
    for i, raw in enumerate(text.splitlines(), 1):
        line = raw.rstrip()
        if not buf and (not line.strip() or line.lstrip().startswith("#")):
            continue
        if start is None:
            start = i
        if line.endswith("\\"):
            buf += line[:-1] + " "
            continue
        buf += line
        m = re.match(r"\s*([A-Za-z]+)\s*(.*)$", buf, re.S)
        if m:
            out.append((start, m.group(1).upper(), m.group(2).strip()))
        buf, start = "", None
    if buf and start is not None:
        m = re.match(r"\s*([A-Za-z]+)\s*(.*)$", buf, re.S)
        if m:
            out.append((start, m.group(1).upper(), m.group(2).strip()))
    return out


def check(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        text = f.read()
    ins = parse(text)
    findings = []

    def add(rule, sev, line, msg, fix):
        findings.append({"rule": rule, "severity": sev, "line": line, "message": msg, "fix": fix})

    # 分阶段
    stages, cur = [], []
    for item in ins:
        if item[1] == "FROM" and cur:
            stages.append(cur); cur = []
        cur.append(item)
    if cur:
        stages.append(cur)
    final = stages[-1] if stages else []

    for line, name, arg in ins:
        if name == "FROM":
            img = arg.split()[0] if arg.split() else ""
            if img.lower() == "scratch" or img.startswith("$"):
                pass
            elif "@sha256:" in img:
                pass
            elif ":" not in img.split("/")[-1] or img.endswith(":latest"):
                add("DF001", "warn", line, f"基础镜像未固定版本：{img}", "写明具体标签或 digest，如 python:3.12-slim 或 @sha256:…，保证构建可复现")
        elif name == "MAINTAINER":
            add("DF017", "info", line, "MAINTAINER 已废弃", "改用 LABEL org.opencontainers.image.authors=\"…\"")
        elif name == "ADD":
            src = arg.split()[0] if arg.split() else ""
            if not re.match(r"https?://", src) and not re.search(r"\.(tar|tgz|tar\.gz|tar\.bz2|tar\.xz)$", src):
                add("DF004", "info", line, "本地文件用 ADD", "普通复制用 COPY；ADD 只在需要自动解压 tar 或拉取 URL 时使用")
        elif name in ("ENV", "ARG"):
            for m in re.finditer(r"([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(\"[^\"]+\"|'[^']+'|\S+)", arg):
                k, v = m.group(1), m.group(2).strip("\"'")
                if SECRET_NAME.search(k) and v and not v.startswith("$") and v.lower() not in ("", "changeme", "xxx"):
                    add("DF006", "high", line, f"{name} 中疑似把敏感值写进镜像：{k}", "镜像层会永久保留该值；改用运行时注入（-e / secrets）或 BuildKit 的 --mount=type=secret")
            # ENV KEY value（无等号）形式
            m2 = re.match(r"([A-Za-z_][A-Za-z0-9_]*)\s+(\S+)$", arg)
            if m2 and "=" not in arg and SECRET_NAME.search(m2.group(1)) and not m2.group(2).startswith("$"):
                add("DF006", "high", line, f"{name} 中疑似把敏感值写进镜像：{m2.group(1)}", "改用运行时注入或 --mount=type=secret")
        elif name == "RUN":
            cmd = arg
            low = cmd.lower()
            if "sudo " in low:
                add("DF011", "warn", line, "RUN 中使用 sudo", "构建时默认就是 root，无需 sudo；需要降权时用 USER 指令")
            if re.search(r"(curl|wget)[^|]*\|\s*(sudo\s+)?(ba|z|da)?sh\b", low):
                add("DF012", "warn", line, "远程脚本直接管道进 shell 执行", "先下载、校验（sha256 / 签名）再执行，或固定脚本版本")
            if "chmod 777" in low or "chmod -r 777" in low:
                add("DF016", "warn", line, "chmod 777", "按需给最小权限，如 755 / 644")
            if "apt-get upgrade" in low or "apt upgrade" in low:
                add("DF002", "warn", line, "apt-get upgrade 会让镜像不可复现且膨胀", "改为固定基础镜像版本；需要安全更新就换更新的基础镜像标签")
            if re.search(r"apt(-get)?\s+install", low):
                if "--no-install-recommends" not in low:
                    add("DF002", "info", line, "apt-get install 未加 --no-install-recommends", "加上以减少不必要的依赖与镜像体积")
                if "apt-get update" not in low and "apt update" not in low:
                    add("DF003", "warn", line, "apt-get install 与 apt-get update 不在同一 RUN", "合并为 RUN apt-get update && apt-get install -y …，避免命中过期的缓存层")
                if not re.search(r"rm\s+-rf\s+/var/lib/apt/lists", low):
                    add("DF002", "info", line, "apt 安装后未清理 /var/lib/apt/lists", "同一 RUN 末尾追加 && rm -rf /var/lib/apt/lists/*")
            if re.search(r"\bpip3?\s+install", low) and "--no-cache-dir" not in low and "pip_no_cache_dir" not in low:
                add("DF007", "info", line, "pip install 未加 --no-cache-dir", "加上以避免把下载缓存打进镜像")
            if re.search(r"\bnpm\s+install\b", low) and "npm ci" not in low:
                add("DF007", "info", line, "npm install 而非 npm ci", "有 lockfile 时用 npm ci --omit=dev，安装可复现且更快")
            if re.search(r"\byum\s+install\b", low) and "yum clean all" not in low:
                add("DF002", "info", line, "yum install 后未清理缓存", "同一 RUN 末尾追加 && yum clean all")
            if re.search(r"\bapk\s+add\b", low) and "--no-cache" not in low:
                add("DF002", "info", line, "apk add 未加 --no-cache", "改为 apk add --no-cache …")
        elif name in ("CMD", "ENTRYPOINT"):
            if not arg.startswith("["):
                add("DF015", "info", line, f"{name} 使用 shell 形式", "改为 exec 形式（JSON 数组），让进程成为 PID 1、正确接收 SIGTERM")
        elif name == "WORKDIR":
            if not (arg.startswith("/") or arg.startswith("$") or re.match(r"[A-Za-z]:\\", arg)):
                add("DF013", "info", line, "WORKDIR 使用相对路径", "用绝对路径，避免依赖前面的 WORKDIR")

    # 最终阶段的整体检查
    names = [n for _, n, _ in final]
    if final:
        if "USER" not in names:
            add("DF005", "warn", final[0][0], "最终镜像未切换非 root 用户", "创建专用用户并在末尾 USER app（或使用发行版自带的 nonroot 用户）")
        if "HEALTHCHECK" not in names and any(n in ("CMD", "ENTRYPOINT") for n in names):
            add("DF009", "info", final[0][0], "没有 HEALTHCHECK", "长期运行的服务加 HEALTHCHECK，编排系统才能判断存活")
        if "WORKDIR" not in names and any(n in ("COPY", "ADD", "RUN") for n in names):
            add("DF013", "info", final[0][0], "没有 WORKDIR", "设置 WORKDIR /app 之类的工作目录，避免文件散落在根目录")
        runs = [l for l, n, _ in final if n == "RUN"]
        if len(runs) > 8:
            add("DF014", "info", runs[0], f"最终阶段有 {len(runs)} 个 RUN 层", "把相关命令合并成少数几个 RUN，减少层数与体积")
        # COPY . . 出现在依赖安装之前
        copy_all = [l for l, n, a in final if n in ("COPY", "ADD") and re.match(r"\.\s+", a + " ")]
        installs = [l for l, n, a in final if n == "RUN" and re.search(r"(pip|npm|yarn|pnpm|go mod|cargo|bundle|composer|mvn|gradle)", a.lower())]
        if copy_all and installs and copy_all[0] < installs[0]:
            add("DF008", "info", copy_all[0], "COPY . . 在依赖安装之前", "先只复制依赖清单（requirements.txt / package*.json / go.mod 等）并安装，再 COPY 其余源码，充分利用构建缓存")
    d = os.path.dirname(os.path.abspath(path))
    if not os.path.exists(os.path.join(d, ".dockerignore")):
        add("DF018", "info", 0, "同目录没有 .dockerignore", "添加 .dockerignore 排除 .git、node_modules、构建产物与本地配置，减小构建上下文")
    # 去重
    seen, uniq = set(), []
    for f in findings:
        key = (f["rule"], f["line"], f["message"])
        if key not in seen:
            seen.add(key); uniq.append(f)
    order = {"high": 0, "warn": 1, "info": 2}
    uniq.sort(key=lambda f: (order[f["severity"]], f["line"]))
    return {"file": path, "instructions": len(ins), "stages": len(stages), "findings": uniq}


def find_targets(args):
    out = []
    for a in args or ["."]:
        if os.path.isdir(a):
            for root, dirs, files in os.walk(a):
                dirs[:] = [x for x in dirs if x not in (".git", "node_modules", "vendor", ".venv")]
                for fn in files:
                    if fn == "Dockerfile" or fn.startswith("Dockerfile.") or fn.endswith(".dockerfile"):
                        out.append(os.path.join(root, fn))
        else:
            out.append(a)
    return out


def main():
    ap = argparse.ArgumentParser(description="Dockerfile 体检")
    ap.add_argument("paths", nargs="*", help="Dockerfile 或目录")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true", help="有 high/warn 则退出码 1")
    a = ap.parse_args()
    targets = find_targets(a.paths)
    if not targets:
        print("未找到 Dockerfile", file=sys.stderr); sys.exit(2)
    results = [check(p) for p in targets]
    if a.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for r in results:
            print(f"== {r['file']}  （{r['instructions']} 条指令，{r['stages']} 个阶段）")
            if not r["findings"]:
                print("  ✓ 没有发现问题")
            for f in r["findings"]:
                loc = f"L{f['line']}" if f["line"] else "文件"
                print(f"  [{f['severity'].upper():4}] {f['rule']} {loc}: {f['message']}\n         → {f['fix']}")
            c = {s: sum(1 for f in r["findings"] if f["severity"] == s) for s in ("high", "warn", "info")}
            print(f"  小计：high {c['high']} / warn {c['warn']} / info {c['info']}")
    bad = any(f["severity"] in ("high", "warn") for r in results for f in r["findings"])
    sys.exit(1 if (a.strict and bad) else 0)


if __name__ == "__main__":
    main()
