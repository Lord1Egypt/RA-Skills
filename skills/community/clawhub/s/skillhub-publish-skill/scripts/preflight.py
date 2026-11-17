#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Skill 发布前预检（纯标准库，零第三方依赖）。

在把 Skill 提交平台审核之前，用确定性脚本把「会被拒的问题」一次查清。

覆盖检查项：
    frontmatter   缺必填字段 / slug 非法 / version 非 SemVer / 折叠标量
    包结构        位图与独立 LICENSE 拒收、__pycache__ 等垃圾、超体积
    密钥泄漏      API Key / 私钥 / 硬编码口令 / Bearer 令牌
    安全红线      rm -rf 家目录、curl|sh 下载执行、读取 .ssh
    占位符        TODO / FIXME / <your-key> 等残留
    **WAF 风险**  美元符号+双花括号连写等腾讯云 WAF 命中特征（本脚本独有）

前三项参考公开的发布预检实践，第四项 WAF 风险来自实测（累计评分制）。

用法：
    python preflight.py <skill目录> [--platform skillhub|clawhub|github|all]
                                     [--max-size-mb 10] [--json]

退出码：存在 ERROR 返回 1，否则 0（可直接接发布脚本做卡点）。
"""
import argparse
import json
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

BITMAP_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".ico", ".svg"}
JUNK_DIRS = {"__pycache__", "node_modules", ".git", ".venv", "venv", "dist", "build", ".idea", ".vscode"}
JUNK_EXTS = {".pyc", ".pyo", ".class", ".so", ".dll", ".exe", ".DS_Store"}

# SkillHub 服务端接受的类型（2026-09-19 用真实请求实测，非猜测）：
#   ✅ .md（含 references/*.md）、.yaml/.yml、.py、.json、.txt 等文本
#   ❌ 位图（.png/.jpg/…）、LICENSE（无论有无扩展名）
# 注意：**不存在「只有 SKILL.md/manifest.yaml/scripts」的白名单** ——
# `.md` 是允许的，所以 references/ 目录可以正常带上。
SKILLHUB_ALLOWED_FILES = {"SKILL.md", "manifest.yaml", "manifest.yml"}
SKILLHUB_ALLOWED_PREFIXES = ("scripts/", "references/", "assets/")
SKILLHUB_ALLOWED_EXTS = {".md", ".yaml", ".yml", ".py", ".json", ".txt", ".toml", ".cfg", ".ini", ".sh"}
SKILLHUB_NEVER = {".gitignore", ".gitattributes", ".ds_store"}

SLUG_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")

SECRET_PATTERNS = [
    (r"\bsk-[A-Za-z0-9]{16,}", "疑似 OpenAI/Anthropic 风格 API Key"),
    (r"\bskh_[A-Za-z0-9]{20,}", "疑似 SkillHub API Token（skh_ 开头）"),
    (r"\bgho_[A-Za-z0-9]{20,}", "疑似 GitHub OAuth Token（gho_ 开头）"),
    (r"\bghp_[A-Za-z0-9]{20,}", "疑似 GitHub PAT（ghp_ 开头）"),
    (r"\bAKIA[0-9A-Z]{16}\b", "疑似 AWS Access Key"),
    (r"\bLTAI[0-9A-Za-z]{12,}", "疑似阿里云 AccessKeyId"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "疑似私钥文件内容"),
    (r"(?i)\b(password|passwd|secret|api[_-]?key)\b\s*[:=]\s*['\"][A-Za-z0-9+/]{12,}['\"]",
     "疑似硬编码口令/密钥"),
    (r"(?i)\bbearer\s+[A-Za-z0-9\-_.]{16,}", "疑似 Bearer 令牌"),
]

DANGEROUS_PATTERNS = [
    (r"rm\s+-rf\s+(/|~|\$HOME|\*)", "递归删除系统/家目录类命令"),
    (r"\.ssh\b", "读取用户 SSH 目录"),
    (r"curl\s+[^\n|]*\|\s*(ba)?sh", "curl 管道直接执行远程脚本"),
    (r"wget\s+[^\n]*\|\s*(ba)?sh", "wget 管道直接执行远程脚本"),
    (r"(?i)shutil\.rmtree\s*\(\s*['\"]/", "递归删除根目录"),
]

# 这些文件本身就是规则库/文档，正文里必然出现「危险模式」作为检测目标或示例，
# 自指会 100% 误报。对它们只做密钥与占位符检查，跳过安全红线与 WAF 特征。
SELF_REFERENTIAL = {"preflight.py", "waf_bisect.py"}

PLACEHOLDER_PATTERNS = [
    (r"\bTODO\b", "残留 TODO"),
    (r"\bFIXME\b", "残留 FIXME"),
    (r"\bXXX\b", "残留 XXX"),
    (r"<your[-_]?(api[-_]?key|token|password)>", "未替换的占位符"),
    (r"(?i)your[-_]?name[-_]?here", "未替换的占位符"),
    (r"sk-\.\.\.|sk-xxx", "占位符形式的 Key"),
]

# ⚠️ 本脚本独有：腾讯云 WAF 命中特征（写进发布内容会被 566 拦截）
# 规则是累计评分制，单条出现未必触发，但与代码密度叠加跨过阈值即拦。
WAF_RISK_PATTERNS = [
    (r"\$\{\{", "美元符号+双花括号连写（GitHub Actions 表达式语法，被当模板注入/SSTI 特征）"),
    (r"\{%", "Jinja/Twig 模板标签（模板注入特征）"),
    (r"<%=|%>", "ERB/ASP 模板标签（模板注入特征）"),
]

REQUIRED_FM_FIELDS = {
    "skillhub": ["name", "slug", "version", "displayName", "description"],
    "clawhub": ["name", "version", "description"],
    "github": ["name", "description"],
}


def load_frontmatter(md_path):
    """解析 SKILL.md 的 YAML frontmatter（简化实现，够用）。"""
    text = open(md_path, encoding="utf-8", errors="replace").read()
    if not text.startswith("---"):
        return {}, text
    lines = text.split("\n")
    end = -1
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end < 0:
        return {}, text
    fm = {}
    for raw in lines[1:end]:
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        k, _, v = line.partition(":")
        k, v = k.strip(), v.strip()
        if not k:
            continue
        if v.startswith("[") and v.endswith("]"):
            inner = v[1:-1].strip()
            fm[k] = [] if not inner else [s.strip().strip("'\"") for s in inner.split(",") if s.strip()]
        else:
            fm[k] = v[1:-1] if len(v) >= 2 and v[0] == v[-1] and v[0] in ("'", '"') else v
    return fm, text


def collect_files(skill_dir):
    out = []
    for root, dirs, names in os.walk(skill_dir):
        dirs[:] = [d for d in dirs if d not in JUNK_DIRS]
        for n in names:
            p = os.path.join(root, n)
            rel = os.path.relpath(p, skill_dir).replace("\\", "/")
            out.append((rel, p, os.path.getsize(p)))
    return sorted(out)


class Report:
    def __init__(self):
        self.items = []

    def add(self, level, cat, msg, fix=""):
        self.items.append({"level": level, "category": cat, "message": msg, "fix": fix})

    def err(self, cat, msg, fix=""):
        self.add("ERROR", cat, msg, fix)

    def warn(self, cat, msg, fix=""):
        self.add("WARN", cat, msg, fix)

    def info(self, cat, msg, fix=""):
        self.add("INFO", cat, msg, fix)

    def count(self, level):
        return sum(1 for i in self.items if i["level"] == level)


def check_frontmatter(rep, fm, platform):
    plats = ["skillhub", "clawhub", "github"] if platform == "all" else [platform]
    for pl in plats:
        for f in REQUIRED_FM_FIELDS.get(pl, []):
            val = fm.get(f)
            if val is None or (isinstance(val, str) and not val.strip()):
                rep.err("frontmatter", f"[{pl}] 缺必填字段 `{f}`", f"在 SKILL.md frontmatter 补 `{f}: ...`")

    slug = str(fm.get("slug") or "").strip()
    if slug and not SLUG_RE.match(slug):
        rep.err("frontmatter", f"slug 非法（须 kebab-case 小写）：{slug}",
                "改为纯小写字母/数字/连字符，且不以连字符开头结尾")

    ver = str(fm.get("version") or "").strip()
    if ver and not SEMVER_RE.match(ver):
        rep.err("frontmatter", f"version 非 SemVer（须 x.y.z）：{ver}", "改为 1.0.0 形式")

    # 折叠标量：> 或 | 开头会让部分平台解析失败
    for k, v in fm.items():
        if isinstance(v, str) and v in (">", "|", ">-", "|-"):
            rep.warn("frontmatter", f"字段 `{k}` 使用了折叠/块标量（{v}）",
                     "改为单行普通标量，部分平台解析器不识别")

    desc = str(fm.get("description") or "")
    if len(desc) < 20:
        rep.warn("frontmatter", f"description 过短（{len(desc)} 字符）",
                 "写清「做什么 + 什么场景触发」，建议 2-3 个用户真实会说出口的短语")
    if re.search(r"(提升|提高|准确率)\s*\d+\s*倍|100%\s*(准确|成功)", desc):
        rep.warn("frontmatter", "description 含无来源的效果宣称", "审核打回重灾区，删掉或补来源")


def check_structure(rep, skill_dir, files, platform, max_size_mb):
    total = sum(s for _, _, s in files)
    if total > max_size_mb * 1024 * 1024:
        rep.err("包结构", f"总体积 {total/1024/1024:.2f}MB 超过 {max_size_mb}MB 上限",
                "删除大文件；SkillHub 超限直接拒收")

    names = [rel for rel, _, _ in files]
    if "SKILL.md" not in names:
        rep.err("包结构", "缺少 SKILL.md", "每个 skill 必须有 SKILL.md")

    # 位图会被拒收（图标走表单单独上传）
    for rel, p, _ in files:
        ext = os.path.splitext(rel)[1].lower()
        if ext in BITMAP_EXTS:
            rep.err("包结构", f"包含位图文件：{rel}",
                    "图片会被拒收；图标请在发布表单单独上传，绝不打进包")
        if os.path.basename(rel).upper() == "LICENSE" or os.path.basename(rel).upper().startswith("LICENSE."):
            rep.err("包结构", f"包含独立 LICENSE 文件：{rel}", "平台拒收独立 LICENSE；许可写 frontmatter 的 `license` 字段")
        if os.path.basename(rel).upper().startswith("README"):
            rep.warn("包结构", f"包含 README：{rel}", "SkillHub 白名单不含 README，会被拒；内容并进 SKILL.md")

    # SkillHub 服务端接受范围（实测：不是窄白名单，.md 是允许的）
    if platform in ("skillhub", "all"):
        for rel, _, _ in files:
            base = os.path.basename(rel)
            low = base.lower()
            ext = os.path.splitext(low)[1]
            if low in SKILLHUB_NEVER:
                # 本地存在 .gitignore 很正常（任何 git 仓库都有）；只要不放包里就没事。
                # 打包器会自动排除，所以这里是 INFO 而非 ERROR。
                rep.info("包结构", f"{rel} 不会被打进包（服务端拒收此类型）",
                         "无需处理；scripts/publish.py 会自动排除")
                continue
            if low.startswith("license"):
                continue  # 已单独报错
            if (rel in SKILLHUB_ALLOWED_FILES or rel.startswith(SKILLHUB_ALLOWED_PREFIXES)
                    or ext in SKILLHUB_ALLOWED_EXTS):
                continue
            rep.warn("包结构", f"类型可能不被服务端接受：{rel}",
                     "SkillHub 接受 .md/.yaml/.py/.json/.txt 等文本；位图与 LICENSE 必拒")


def check_content(rep, files):
    for rel, p, _ in files:
        ext = os.path.splitext(rel)[1].lower()
        if ext in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".svg", ".zip"}:
            continue
        try:
            text = open(p, encoding="utf-8", errors="replace").read()
        except Exception:
            continue

        is_self = os.path.basename(rel) in SELF_REFERENTIAL
        is_doc = rel.lower().endswith(".md")

        for pat, why in SECRET_PATTERNS:
            for m in re.finditer(pat, text):
                frag = m.group(0)
                masked = frag[:8] + "…" + frag[-4:] if len(frag) > 14 else frag[:8] + "…"
                # 密钥在任何文件里都是红线，包括自指文件
                rep.err("密钥泄漏", f"{rel}: {why} → `{masked}`", "改用环境变量读取；凭据绝不进仓库")

        # 安全红线：自指规则库跳过（它必须写下这些模式才能检测）
        if not is_self:
            for pat, why in DANGEROUS_PATTERNS:
                if re.search(pat, text):
                    # 文档里作为「反面示例/安装命令」出现时降级为提醒
                    lvl = rep.warn if is_doc else rep.err
                    fix = ("确认是教程/示例而非真实执行；若为安装命令属正常用法，无需处理"
                           if is_doc else "移除该行为，安全扫描会重点审视")
                    lvl("安全红线", f"{rel}: {why}", fix)

        for pat, why in PLACEHOLDER_PATTERNS:
            if re.search(pat, text) and not is_self:
                rep.warn("占位符", f"{rel}: {why}", "发布前清理或替换为真实内容")

        # WAF 特征：自指规则库跳过（规则自身就含这些字面量）
        if not is_self:
            for pat, why in WAF_RISK_PATTERNS:
                n = len(re.findall(pat, text))
                if n:
                    rep.warn("WAF风险", f"{rel}: {why}（{n} 处）",
                             "腾讯云 WAF 累计评分制，与代码密度叠加会返回 566。"
                             "规避：在字符间插一个空格并在注释说明复制时删掉；"
                             "改完跑 scripts/waf_bisect.py --step check 确认全量为 401")


def main():
    ap = argparse.ArgumentParser(description="Skill 发布前预检")
    ap.add_argument("target", help="skill 目录或 SKILL.md 路径")
    ap.add_argument("--platform", default="all", choices=["all", "skillhub", "clawhub", "github"])
    ap.add_argument("--max-size-mb", type=float, default=10.0)
    ap.add_argument("--json", action="store_true", help="以 JSON 输出")
    args = ap.parse_args()

    target = os.path.abspath(args.target)
    skill_dir = os.path.dirname(target) if os.path.isfile(target) else target
    md = os.path.join(skill_dir, "SKILL.md")

    if not os.path.exists(md):
        print(f"ERROR: 找不到 {md}", file=sys.stderr)
        return 1

    fm, _ = load_frontmatter(md)
    files = collect_files(skill_dir)

    rep = Report()
    check_frontmatter(rep, fm, args.platform)
    check_structure(rep, skill_dir, files, args.platform, args.max_size_mb)
    check_content(rep, files)

    rep.info("发布操作", "visibility 建议选 public，否则别人搜不到")
    rep.info("发布操作", "更新时 version 必须高于线上版本")
    rep.info("发布操作", "连续发布多个 Skill 间隔 20-30 秒，否则触发限流")

    n_err, n_warn, n_info = rep.count("ERROR"), rep.count("WARN"), rep.count("INFO")

    if args.json:
        print(json.dumps({
            "target": skill_dir, "platform": args.platform,
            "summary": {"ERROR": n_err, "WARN": n_warn, "INFO": n_info},
            "files": [rel for rel, _, _ in files],
            "findings": rep.items,
        }, ensure_ascii=False, indent=2))
        return 1 if n_err else 0

    print(f"预检目标：{skill_dir}")
    print(f"平台：{args.platform}    文件数：{len(files)}    "
          f"体积：{sum(s for _,_,s in files)/1024:.1f}KB")
    print("=" * 68)
    for level in ("ERROR", "WARN", "INFO"):
        group = [i for i in rep.items if i["level"] == level]
        if not group:
            continue
        icon = {"ERROR": "✗", "WARN": "!", "INFO": "i"}[level]
        print(f"\n[{level}] {len(group)} 项")
        for i in group:
            print(f"  {icon} ({i['category']}) {i['message']}")
            if i["fix"]:
                print(f"      → {i['fix']}")
    print("\n" + "=" * 68)
    print(f"合计：ERROR {n_err} / WARN {n_warn} / INFO {n_info}")
    if n_err:
        print("✗ 存在 ERROR，修复后再发布")
        return 1
    print("✓ 无 ERROR，可以发布" + ("（WARN 建议处理）" if n_warn else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
