#!/usr/bin/env python3
"""环境变量配置一致性检查：.env.example 与各环境 .env、代码里实际读取的变量三者对齐。纯标准库。

用法：
  python3 env_sync_check.py                      # 当前目录：.env.example 对比 .env* 并扫描代码
  python3 env_sync_check.py --example .env.example --env .env.production --src src/
  python3 env_sync_check.py --json --strict      # 有缺失必填变量则退出码 1
检查项：示例里有、环境文件缺（缺配置）；环境文件有、示例没有（未登记）；代码读取但示例没有（漏文档）；示例定义但代码从未读取（僵尸变量）；环境文件里的疑似真实密钥；重复定义。
"""
import argparse, json, math, os, re, sys
from collections import Counter

ENV_LINE = re.compile(r"^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$")
READ_PATTERNS = [
    re.compile(r"os\.environ(?:\.get)?\s*[\[\(]\s*['\"]([A-Z][A-Z0-9_]+)['\"]"),   # python
    re.compile(r"os\.getenv\s*\(\s*['\"]([A-Z][A-Z0-9_]+)['\"]"),
    re.compile(r"process\.env\.([A-Z][A-Z0-9_]+)"),                                 # node
    re.compile(r"process\.env\[['\"]([A-Z][A-Z0-9_]+)['\"]\]"),
    re.compile(r"import\.meta\.env\.([A-Z][A-Z0-9_]+)"),                            # vite
    re.compile(r"os\.Getenv\s*\(\s*\"([A-Z][A-Z0-9_]+)\""),                         # go
    re.compile(r"os\.LookupEnv\s*\(\s*\"([A-Z][A-Z0-9_]+)\""),
    re.compile(r"System\.getenv\s*\(\s*\"([A-Z][A-Z0-9_]+)\""),                     # java
    re.compile(r"ENV\[['\"]([A-Z][A-Z0-9_]+)['\"]\]|ENV\.fetch\(['\"]([A-Z][A-Z0-9_]+)['\"]"),  # ruby
    re.compile(r"getenv\s*\(\s*['\"]([A-Z][A-Z0-9_]+)['\"]"),                       # php/c
    re.compile(r"\$\{([A-Z][A-Z0-9_]+)(?::-[^}]*)?\}"),                              # shell / compose
    re.compile(r"env::var\s*\(\s*\"([A-Z][A-Z0-9_]+)\""),                            # rust
    re.compile(r"Env\.get\(['\"]([A-Z][A-Z0-9_]+)['\"]"),
]
# ---- 密钥启发式：名字 + 值 双重判定；名字像密钥还不够，值也要真的像密钥才报 ----
# 连接串类命名：以 _URL 结尾但确实带凭据，要先于下面的「非敏感命名」排除
DSN_NAME = re.compile(r"(?:^|_)(?:DSN|DATABASE_URL|DB_URL|CONNECTION_STRING|CONN_STR(?:ING)?)(?:_|$)", re.I)
# 命中即认为名字指向密钥
SECRET_NAME = re.compile(r"""(?xi)
      PASSWORD | PASSWD | (?:^|_)PWD(?:_|$)
    | SECRET | CREDENTIALS? | PASSPHRASE | TOKEN
    | (?:API|ACCESS|PRIVATE|SECRET|SIGNING|SIGN|CIPHER|ENCRYPT(?:ION)?|DECRYPT(?:ION)?|
       MASTER|APP|CLIENT|AUTH|SESSION|HMAC|JWT|LICENSE|WEBHOOK)_?KEYS?
    | SIGNING | SIGNATURE | CIPHER | SALT | PEPPER | PRIVATE | CERT(?:IFICATE)?
    | KEYSTORE | TRUSTSTORE | (?:^|_)AUTH(?:_|$) | (?:^|_)KEY(?:_|$)
""")
# 名字里带这些词的一律不当密钥：*_KEY_ID、PUBLIC_KEY、KEY_PREFIX、*_KEYS_COUNT、各种 URL/ID/开关/超时
NON_SECRET_NAME = re.compile(r"""(?xi)
      PUBLIC
    | (?:^|_)KEYS?_(?:ID|IDS|NAME|NAMES|PREFIX|SUFFIX|PATH|FILE|DIR|COUNT|NUM|NUMBER|TOTAL|SIZE|
       LEN|LENGTH|VERSION|ALGO(?:RITHM)?|TTL|ROTATION|REF|ARN|URI|URL|ENABLED?)(?:_|$)
    | (?:^|_)(?:SECRET|TOKEN|PASSWORD|CERT|KEYSTORE|SALT)_(?:NAME|NAMES|ID|IDS|REF|ARN|PATH|FILE|DIR|
       MANAGER|PROVIDER|BACKEND|STORE|TTL|EXPIRES?(?:_IN)?|EXPIRY|EXPIRATION|TIMEOUT|LENGTH|LEN|SIZE|
       COUNT|PREFIX|SUFFIX|HEADER|ISSUER|AUDIENCE|ALGO(?:RITHM)?|ROTATION|VERSION|URL|URI|ENDPOINT|
       ENABLED?|REQUIRED|MODE|TYPE|SCOPE|SCOPES|ROUNDS)(?:_|$)
    | _(?:URL|URI|ENDPOINT|HOST|HOSTNAME|DOMAIN|PORT|ADDR|ADDRESS|ID|IDS|NAME|PATH|FILE|DIR|FOLDER|
       ENABLED|ENABLE|DISABLED|MODE|TYPE|KIND|FORMAT|ALGO|ALGORITHM|TTL|TIMEOUT|EXPIRY|EXPIRES|
       EXPIRATION|COUNT|NUM|NUMBER|TOTAL|SIZE|LEN|LENGTH|LIMIT|VERSION|REGION|ZONE|ISSUER|AUDIENCE|
       SUBJECT|PROVIDER|STRATEGY|REALM|SCOPE|SCOPES|METHOD|HEADER|HEADERS|ROTATION|REF|ARN|PREFIX|
       SUFFIX|PATTERN|REGEX|TEMPLATE|SCHEMA|SCHEME|LEVEL|POLICY|ROLE|USER|USERNAME|OWNER|SECONDS|
       MS|MINUTES|HOURS|DAYS)$
""")
# 一眼是占位符的整值：空、<...>、***、${VAR}、changeme、your-...、xxx、REPLACE_ME、TODO 等
PLACEHOLDER = re.compile(r"""(?xi)^\s*(
      | -+ | n/?a | none | null | nil | undefined | \*+ | x+ | \?+ | _+ | \.+
    | \$\{[^}]*\} | \$[A-Za-z_][A-Za-z0-9_]* | %[A-Za-z_]+% | \{\{[^}]*\}\} | <[^>]*> | \[[^\]]*\]
    | (?:change|replace|update|set|fill|insert|put|paste)[-_ ]?(?:me|it|this|here|your)[-_ ]?\w*
    | your[-_. ].* | my[-_ ]?(?:secret|password|passwd|key|token|dsn).*
    | place[-_ ]?holder\w* | example\w* | sample\w* | dummy\w* | fake\w* | mock\w* | demo\w*
    | todo\w* | fixme\w* | tbd | redacted\w* | masked\w* | hidden | omitted | unset | disabled
    | secret | password | passwd | token | api[-_ ]?key | key | credential | value | string
    )\s*$""")
# 值里任意位置出现这些词就当占位符（CHANGE_THIS_TO_A_REAL_SECRET 这种）
PLACEHOLDER_WORD = re.compile(r"""(?xi)(?:^|[^A-Za-z0-9])(
      change[-_]?(?:me|this|it)? | replace[-_]?(?:me|this|it)? | your[-_] | place[-_]?holder
    | example | sample | dummy | fake | mock | redacted | masked | todo | fixme | tbd
    | not[-_]?set | fill[-_]?(?:me|in) | set[-_]?me | insert[-_]?your | xxxx+
    | real[-_]?secret | secret[-_]?here | key[-_]?here | value[-_]?here | goes[-_]?here
    )(?:[^A-Za-z0-9]|$)""")
URL_LIKE = re.compile(r"^[A-Za-z][A-Za-z0-9+.\-]*://")
URL_CRED = re.compile(r"^[A-Za-z][A-Za-z0-9+.\-]*://[^:@/\s]*:(?P<pw>[^@/\s]*)@")
NUMERIC = re.compile(r"^[\d.,:_+\-]+$")
SRC_EXT = {".py", ".js", ".ts", ".tsx", ".jsx", ".mjs", ".cjs", ".go", ".java", ".kt", ".rb", ".php", ".rs", ".sh", ".bash", ".yml", ".yaml", ".toml", ".cfg", ".ini", ".env"}


def parse_env(path):
    vars_, dups = {}, []
    for i, line in enumerate(open(path, encoding="utf-8", errors="replace"), 1):
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        m = ENV_LINE.match(line)
        if not m:
            continue
        k, v = m.group(1), m.group(2).strip()
        if v[:1] in ("'", '"') and v[-1:] == v[:1] and len(v) >= 2:
            v = v[1:-1]
        else:
            v = v.split(" #", 1)[0].strip()
        if k in vars_:
            dups.append((k, i))
        vars_[k] = (v, i)
    return vars_, dups


def scan_src(root):
    found = {}
    for r, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "vendor", ".venv", "venv", "dist", "build", "__pycache__", ".next", "target")]
        for fn in files:
            if os.path.splitext(fn)[1] not in SRC_EXT or fn.startswith(".env"):
                continue
            p = os.path.join(r, fn)
            try:
                text = open(p, encoding="utf-8", errors="ignore").read()
            except OSError:
                continue
            for pat in READ_PATTERNS:
                for m in pat.finditer(text):
                    name = next(g for g in m.groups() if g)
                    found.setdefault(name, set()).add(os.path.relpath(p, root))
    return found


def secret_name(k):
    """变量名是否指向密钥：先认连接串，再排除 *_KEY_ID / PUBLIC_KEY / KEY_PREFIX / *_KEYS_COUNT 这类命名。"""
    u = (k or "").upper()
    if DSN_NAME.search(u):
        return True
    if NON_SECRET_NAME.search(u):
        return False
    return bool(SECRET_NAME.search(u))


def entropy(v):
    """Shannon 熵（bit/字符）：随机密钥通常 ≥ 3，重复串与纯数字远低于此。"""
    n = len(v)
    if n < 2:
        return 0.0
    return -sum((c / n) * math.log2(c / n) for c in Counter(v).values())


def strong_value(v):
    """值本身像不像密钥：长度 ≥ 12、不是占位形态、熵/字符类混排够高。"""
    v = (v or "").strip()
    if len(v) < 12 or PLACEHOLDER.match(v) or PLACEHOLDER_WORD.search(v) or NUMERIC.match(v):
        return False
    classes = sum(bool(re.search(p, v)) for p in (r"[a-z]", r"[A-Z]", r"\d", r"[^A-Za-z0-9]"))
    e = entropy(v)
    return e >= 3.0 or (e >= 2.5 and classes >= 3)


def looks_real_secret(k, v):
    """名字像密钥且值也像密钥才算真密钥；连接串只看内嵌的密码部分。"""
    v = (v or "").strip()
    if not v:
        return False
    m = URL_CRED.match(v)
    if m:                                  # postgresql://user:pass@host/db：只判断 pass 那一段
        return strong_value(m.group("pw"))
    if URL_LIKE.match(v):                  # 是 URL 但没内嵌凭据，不算密钥
        return False
    return secret_name(k) and strong_value(v)


def main():
    ap = argparse.ArgumentParser(description=".env 一致性检查")
    ap.add_argument("--example", default=None, help="示例文件，默认自动找 .env.example / .env.sample / .env.template")
    ap.add_argument("--env", action="append", help="要对比的环境文件，可多次；默认自动找 .env、.env.* （排除示例）")
    ap.add_argument("--src", default=".", help="扫描代码的目录")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true", help="有「环境文件缺变量」则退出码 1")
    a = ap.parse_args()
    root = a.src
    example = a.example or next((f for f in (".env.example", ".env.sample", ".env.template", ".env.dist") if os.path.exists(os.path.join(root, f))), None)
    envs = a.env or sorted(f for f in os.listdir(root) if f.startswith(".env") and f != example and not f.endswith((".example", ".sample", ".template", ".dist")) and os.path.isfile(os.path.join(root, f)))
    envs = [e if os.path.isabs(e) or os.path.exists(e) else os.path.join(root, e) for e in envs]
    report = {"example": example, "envs": envs, "findings": []}

    def add(sev, kind, msg, where=None):
        report["findings"].append({"severity": sev, "kind": kind, "message": msg, "where": where})

    ex_vars, ex_dups = parse_env(os.path.join(root, example) if example and not os.path.isabs(example) else example) if example else ({}, [])
    for k, ln in ex_dups:
        add("warn", "duplicate", f"示例文件重复定义 {k}（第 {ln} 行）", example)
    code_vars = scan_src(root)
    for env in envs:
        vars_, dups = parse_env(env)
        name = os.path.basename(env)
        for k, ln in dups:
            add("warn", "duplicate", f"{name} 重复定义 {k}（第 {ln} 行，后者生效）", name)
        for k in sorted(set(ex_vars) - set(vars_)):
            add("high", "missing", f"{name} 缺少示例中登记的 {k}", name)
        for k in sorted(set(vars_) - set(ex_vars)) if example else []:
            add("info", "unregistered", f"{name} 定义了示例中没有的 {k}（考虑登记到 {example}）", name)
        for k, (v, ln) in vars_.items():
            if looks_real_secret(k, v):
                add("warn", "secret", f"{name} 第 {ln} 行的 {k} 看起来是真实密钥；确认该文件在 .gitignore 中且未被提交", name)
    for k, (v, ln) in ex_vars.items():
        if looks_real_secret(k, v):
            add("high", "secret-in-example", f"示例文件第 {ln} 行的 {k} 看起来是真实密钥，示例文件会被提交到仓库", example)
    if example:
        for k in sorted(set(code_vars) - set(ex_vars)):
            files = sorted(code_vars[k])[:3]
            add("warn", "undocumented", f"代码读取了 {k} 但示例文件没有登记（{', '.join(files)}）", files[0] if files else None)
        for k in sorted(set(ex_vars) - set(code_vars)):
            add("info", "unused", f"示例登记了 {k} 但代码中没有找到读取处（可能通过框架/配置库间接读取，或已废弃）", example)
    order = {"high": 0, "warn": 1, "info": 2}
    report["findings"].sort(key=lambda f: (order[f["severity"]], f["kind"], f["message"]))
    report["code_vars"] = sorted(code_vars)
    if a.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"示例文件：{example or '（未找到）'}；环境文件：{', '.join(os.path.basename(e) for e in envs) or '（无）'}；代码中读取 {len(code_vars)} 个变量")
        if not report["findings"]:
            print("  ✓ 三方一致")
        for f in report["findings"]:
            print(f"  [{f['severity'].upper():4}] {f['kind']:18} {f['message']}")
        c = {s: sum(1 for f in report["findings"] if f["severity"] == s) for s in ("high", "warn", "info")}
        print(f"  小计：high {c['high']} / warn {c['warn']} / info {c['info']}")
    bad = any(f["kind"] in ("missing", "secret-in-example") for f in report["findings"])
    sys.exit(1 if (a.strict and bad) else 0)


if __name__ == "__main__":
    main()
