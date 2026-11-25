#!/usr/bin/env python3
"""skill_audit.py — awesome-skills 全库静态体检。

机械检查项(SKILL.md frontmatter 完整性 / 相对路径引用 / 触发词冲突 /
README 收录 / 网络边界声明),供 skill-review-pro 全库轮检使用,也可独立运行。

用法:
    python3 skill_audit.py [仓库根目录]
    # 仓库根目录默认: 脚本所在目录的上一级(即 awesome-skills 根)

输出: 逐 skill 元数据摘要 + 触发词总数 + 问题清单(无问题则输出"(无问题)")。
退出码: 0 = 无问题, 1 = 存在问题, 2 = 用法错误。
"""
import re
import sys
from pathlib import Path


def extract_triggers(desc_block: str) -> list[str]:
    """从 frontmatter description 块中线性提取触发词。

    匹配「触发词：」或「Triggers:」行,收集该行及其后续缩进续行,
    直到出现下一个非缩进非空行为止。不使用嵌套量词正则,避免灾难性回溯。
    """
    lines = desc_block.split("\n")
    collected: list[str] = []
    capturing = False
    for line in lines:
        if re.match(r"^\s*(触发词|Triggers)\s*[：:]", line):
            capturing = True
            collected.append(re.sub(r"^\s*(触发词|Triggers)\s*[：:]\s*", "", line))
            continue
        if capturing:
            # 缩进续行或空行继续收集;遇到新的顶层内容(非缩进、非空)则停止
            if line.strip() == "" or line.startswith("  "):
                collected.append(line)
            else:
                capturing = False
    text = " ".join(collected)
    # NOT for / NOT-for 段是边界声明,不是触发词,冲突检查前截断
    cut = re.split(r"NOT\s*for\s*[：:]", text, maxsplit=1)[0]
    words = [w.strip().rstrip(".。").lower() for w in re.split(r"[,，/、]", cut)]
    return [w for w in words if len(w) >= 2]


def audit(root: Path) -> tuple[list[str], dict]:
    issues: list[str] = []
    all_triggers: dict[str, list[str]] = {}
    meta: dict[str, dict] = {}

    skills = sorted(d for d in root.iterdir() if d.is_dir() and (d / "SKILL.md").exists())
    print(f"发现 {len(skills)} 个 skill\n")

    for d in skills:
        sid = d.name
        text = (d / "SKILL.md").read_text(encoding="utf-8")

        m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        if not m:
            issues.append(f"[{sid}] 缺少 frontmatter")
            continue
        fm = m.group(1)

        name = re.search(r"^name:\s*(.+)$", fm, re.M)
        ver = re.search(r'^version:\s*"?([^"\n]+)"?', fm, re.M)
        if not name:
            issues.append(f"[{sid}] frontmatter 缺 name")
        if not ver:
            issues.append(f"[{sid}] frontmatter 缺 version")

        # description 块 = description: 行之后、下个顶层键(无缩进行)之前的所有缩进行
        dm = re.search(r"^description:\s*>-?\s*\n", fm, re.M)
        desc_block = ""
        desc_len = 0
        if dm:
            start = dm.end()
            desc_lines = []
            for line in fm[start:].split("\n"):
                if line.strip() == "" or line.startswith(" "):
                    desc_lines.append(line)
                else:
                    break
            desc_block = "\n".join(desc_lines)
            desc_len = len("".join(l.strip() for l in desc_lines))
        else:
            issues.append(f"[{sid}] frontmatter description 不是块标量(>-)")
        if desc_len > 1024:
            issues.append(f"[{sid}] description 过长: {desc_len} chars (YAML 加载上限 1024)")
        meta[sid] = {
            "version": ver.group(1) if ver else "?",
            "desc_len": desc_len,
        }

        # 相对路径引用检查(markdown 链接,排除 http/https/anchor/mailto)
        for lm in re.finditer(r"\[[^\]]*\]\(([^)]+)\)", text):
            url = lm.group(1).strip()
            if url.startswith(("http", "#", "mailto:")):
                continue
            target = url.split("#")[0]
            if not target:
                continue
            if not (d / target).resolve().exists():
                issues.append(f"[{sid}] SKILL.md 引用不存在: {url}")

        triggers = extract_triggers(desc_block)
        if triggers:
            all_triggers[sid] = triggers

    # 触发词冲突
    seen: dict[str, str] = {}
    for sid, words in all_triggers.items():
        for w in words:
            if w in seen and seen[w] != sid:
                issues.append(f"[触发词冲突] '{w}' 同时出现在 {seen[w]} 和 {sid}")
            seen[w] = sid

    # README 收录
    readme = (root / "README.md").read_text(encoding="utf-8")
    for d in skills:
        if d.name not in readme:
            issues.append(f"[README] 未收录 {d.name}")

    # 网络边界声明:声明性检查,声明的内容是否真实仍需人工确认
    # (SkillSpector "Excessive Agency / Description-Behavior Mismatch" 审查标准)
    _NON_COMMAND = re.compile(
        r"(fetch 封装|原生 fetch|网络请求库|HTTP 客户端|日志上报|远程日志|"
        r"网络爬取|联网搜题|搜题时|网络/缓存|代理配置|registry 镜像|镜像命令|"
        r"网络代理|网络故障|网络异常|检查网络|网络请求的|的上报|不上传|"
        r"远程存储|服务端|后端接口|接口调用|超时|5xx|示例|example|不要写|"
        r"不写|禁止|负面清单|失败|提示用户|镜像|registry 配置|代理)",
        re.I,
    )
    _CMD_PAT = re.compile(
        r"(?<![\w./-])("
        r"curl\s|wget\s|npx\s|uvx\s|pip\s+install|npm\s+(install|i|view|pub)|"
        r"pnpm\s+(dlx|add|create)|bun\s+(create|add)|apt(-get)?\s+install|brew\s+install"
        r")"
    )
    _NET_TOOL_PAT = re.compile(r"\b(WebFetch|WebSearch|web_fetch|web_search)\b")
    _DECL_PAT = re.compile(r"网络访问声明|无网络|不发起网络请求|无网络外发|no network|offline|仅本地网络|不出网|不联网|离线")
    for d in skills:
        sid2 = d.name
        body2 = (d / "SKILL.md").read_text(encoding="utf-8")
        signals = []
        if _NET_TOOL_PAT.search(body2):
            signals.append("声明/使用 WebFetch/WebSearch 工具")
        # 命令形态:要求命令动词后跟空格 + 参数 token,过滤教学语境的裸关键词
        for line_no, line in enumerate(body2.split("\n"), 1):
            for cm in _CMD_PAT.finditer(line):
                tail = line[cm.end():cm.end() + 40]
                if not re.match(r"\s*\S", tail):
                    continue
                # 教学语境整行排除:「不要写 curl 示例」这类负面清单不是网络能力
                if _NON_COMMAND.search(line):
                    continue
                ctx = line.strip()
                signals.append(f"网络命令信号(L{line_no}): {ctx[:60]}")
        # 逐 skill 声明检查
        fm2 = re.match(r"^---\n(.*?)\n---\n", body2, re.S)
        fm_text = fm2.group(1) if fm2 else ""
        has_decl = bool(_DECL_PAT.search(body2))
        if signals and not has_decl:
            issues.append(
                f"[{sid2}] 疑似网络能力但未声明边界: "
                + "; ".join(sorted(set(signals))[:3])
                + " → 请在 SKILL.md 显式声明网络边界(允许哪些域名/操作,或声明「无网络访问」)"
            )

    print("== 各 skill 元数据 ==")
    for sid, m in sorted(meta.items()):
        print(f"  {sid}: v{m['version']}, desc {m['desc_len']} chars")
    print(f"\n== 触发词总数: {sum(len(v) for v in all_triggers.values())} ==")
    print("\n== 问题清单 ==")
    if not issues:
        print("  (无问题)")
    for i in issues:
        print(" ", i)
    return issues, meta


def main() -> int:
    if len(sys.argv) > 2:
        print(__doc__)
        return 2
    if len(sys.argv) == 2:
        root = Path(sys.argv[1]).resolve()
    else:
        root = Path(__file__).resolve().parent.parent.parent
    if not (root / "README.md").exists():
        print(f"错误: {root} 不是 awesome-skills 仓库根(缺少 README.md)")
        return 2
    issues, _ = audit(root)
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
