#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_consistency.py — storyforge-writing 一致性检查器（v5，零依赖）

v5（v0.5.0）：
  · D1  新增「产物校验覆盖声明 ↔ 校验器代码一致」：INVARIANTS.md 等文档引用的每个大写问题码
        都必须在 `check_framework_artifact.py --list-codes` 中存在；当前态文档不得再写过时的「6 类违规」。
        （v0.4.0 的 INVARIANTS 声称 INV-C-1 / INV-S-2 有机器覆盖，实际校验器不查记录内多余键 —— 文档与代码脱节无人发现。）
  · K1  去掉「contracts 总量 ≥20KB」下限（体积下限只会奖励写长）；SKILL.md 预算收紧到 ≤16KB（WARN）。
  · V2  额外核对 COMPAT.md §4 与 INVARIANTS.md 中的「技能包自检 N 项」。
  · L2  本地前缀增加 `examples/`、`tests/`。
  合计 21 项断言。

v4 相对 v3 的修复（实测：WSL 原件缺 references/ 却仍被判 PASS = 假阴性）：
  · L2  新增「被引用的本地文件都存在」。v3 的 L1 只认 markdown 链接 `[t](p)`，
        而 SKILL.md 用**反引号 code span** `` `references/schema-tables.md` `` 引用 → L1 看不见。
        且 R3 只在 references/ **存在时**扫孤儿，目录整体缺失时直接判"无孤儿"。
        两处叠加 → 「引用了但文件不存在」的死链**完全没有断言覆盖**。
        L2 改为从**原文**抽取 `references|contracts|scripts/<name>.<ext>` 并逐条验存。
  · R3  职责澄清：只防「多余文件（孤儿）」，存在性交给 L2；并修 title 表述。
  · V2  新增「版本与断言数的当前态声明自洽」：SKILL 的「本技能版本」↔ frontmatter ↔ 实际断言数、
        README 断言数、skill-card 版本，全部对齐（这类漂移此前全靠人工发现）。
  合计 19 项断言（v0.2.0 = 14 → v0.2.1 +C4 = 15 → v0.2.2 +L2 +V2 = 17 → v0.3.0 +X1 +X2 = 19）。

v2/v3 相对 v1 的修复（依据 REV-20261005-018 的"可绕过清单"）：
  · C1  改为「新三态齐备 **且** 旧词 `insufficient` 不得作为操作规则出现」（v1 是"出现即合格"）
  · C2  三词齐备 **且** 必须有规则句（禁止编造/不得把推断当事实）
  · C3  改为**逐行**标注：任何含「达芬奇」的行必须自带来源标注（v1 是文件级豁免）
  · R1/R2 改为**解析路由表行**并与 contracts/ 目录做**集合精确**比对（v1 只做全文串集合闭包，
        删掉表格行也能过；且对反斜杠写法会假红）
  · A1  锚点覆盖**全部 9 个契约**，并加**内容下限**（每份 ≥15 非空行）
  · V1  frontmatter 版本必须**同时出现在正文**（v1 只看 frontmatter 有没有）
  · M2  逐文档基线 ≥6 条且每条含版本；`primary_source` 非空；修 detail 文案 bug
  · B1  新增自洽检查：正文基线表与 frontmatter `documents` 的文档路径**集合一致**
  · K1  SKILL.md 体积 + contracts/ 总量双下限
  · 退出码 2：SKILL.md 缺失（v1 直接 traceback）

已知限制（如实声明）：不校验与上游逐字一致；不检测上游是否更新；路由分类语义无法断言；
L2 只认 `references|contracts|scripts` 三类**本地前缀**，裸文件名与上游路径（`src/`、`docs/`）不在其内。
"""

import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAIL, WARN = "FAIL", "WARN"
MD_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
CONTRACT_REF = re.compile(r"contracts[/\\]([A-Za-z0-9_\-]+\.md)")
# L2：本地相对文件引用（反引号 code span / 正文 / 链接都逃不过）。刻意要求**带扩展名**，
# 以排除 `scripts/act1-4`（项目内路径）与 `scripts/**episode-01..04**`（glob 示例）；
# 左边界 `(?<![\w/\\])` 防止命中子路径片段（如 `apps/api/scripts/seed.ts`）。
# v0.3.0 加固（U5 反例 L2-a/b/c）：接受反斜杠、可选 `./` 前缀、子目录——
#   `references\x.md` / `./references/x.md` / `references/sub/x.md` 此前会被漏检。
LOCAL_REF = re.compile(
    r"(?<![\w/\\])(?:\./)?(?:references|contracts|scripts|examples|tests)[/\\]"
    r"[A-Za-z0-9_][A-Za-z0-9_.\-/\\]*\.(?:md|py|json|ya?ml|txt|ts)"
)


def local_rel_path(ref):
    """把引用规整为仓库相对路径（统一分隔符、去掉 `./`），供存在性检查使用。"""
    p = ref.replace("\\", "/")
    while p.startswith("./"):
        p = p[2:]
    return p

ANCHORS = {
    "A-characters.md": ["角色卡", "关系"],
    "A-interactive.md": ["AdventureContentV2", "commitAdventureAction", "八"],
    "A-longform.md": ["节点", "allowed writes", "跨模式验收"],
    "A-world-engine.md": ["worldCode", "WorldRelease", "WorldRequirementAdapter", "禁止读取"],
    "B-comic.md": ["字段闭集", "边界"],
    "B-motion-drama.md": ["物料", "Prompt IR", "不静默忽略"],
    "C-post.md": ["交接", "完成门"],
    "C-screenplay.md": ["忠实保留", "合理改编", "新增假设", "不可变剧本版本"],
    "S-data-envelope.md": ["PROJECT_TABLES", "CURRENT_BACKUP_VERSION", "精确键集", "旁车"],
}
MIN_LINES = 12
MIN_CHARS = 800
MIN_HEADINGS = 3


def read(p):
    with io.open(p, encoding="utf-8-sig", errors="replace") as fh:
        return fh.read()


class Report:
    def __init__(self):
        self.items = []

    def add(self, cid, title, level, ok, detail=""):
        self.items.append({"id": cid, "title": title, "level": level, "ok": bool(ok), "detail": detail})

    @property
    def fails(self):
        return [i for i in self.items if not i["ok"] and i["level"] == FAIL]

    @property
    def warns(self):
        return [i for i in self.items if not i["ok"] and i["level"] == WARN]


def route_table_entries(skill):
    """从路由表表格行精确解析契约名（表格行 = 以 | 开头且含 contracts/）。"""
    out = set()
    for line in skill.splitlines():
        if line.startswith("|") and "contracts/" in line or (line.startswith("|") and "contracts\\" in line):
            out |= {m for m in CONTRACT_REF.findall(line)}
    return out


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    skill_p = os.path.join(ROOT, "SKILL.md")
    if not os.path.isfile(skill_p):
        print("用法/环境错误：SKILL.md 不存在于 %s" % ROOT, file=sys.stderr)
        return 2
    rep = Report()
    skill = read(skill_p)
    fm = skill.split("---", 2)[1] if skill.startswith("---") else ""
    body = skill.split("---", 2)[2] if skill.count("---") >= 2 else skill
    cdir = os.path.join(ROOT, "contracts")
    files = {f for f in os.listdir(cdir) if f.endswith(".md")} if os.path.isdir(cdir) else set()

    # V1
    m = re.search(r"^version:\s*([\d.]+)", fm, re.M)
    ver = m.group(1) if m else ""
    in_body = bool(ver) and ("v" + ver in body or ver in body)
    rep.add("V1", "版本戳存在且正文可见", FAIL, bool(ver) and in_body,
            "version=%s；正文%s出现" % (ver or "(未找到)", "" if in_body else "**未**"))

    # M1
    need = ["name", "description", "version", "license", "compatibility", "metadata"]
    miss = [k for k in need if not re.search(r"^%s:" % k, fm, re.M)]
    rep.add("M1", "frontmatter 必备字段齐备", FAIL, not miss,
            "缺：%s" % "、".join(miss) if miss else "6 项齐备")

    # M2
    docs = re.findall(r'-\s+"?(docs/[^"\n:]+|[A-Za-z0-9_./\-]+\.(?:md|ts))(?::\s*([^"\n]+))?"?', fm)
    has_tail = bool(re.search(r"source_version_baseline:\s*\n\s+audited:", fm))
    primary = re.search(r"primary_source:\s*\"?([^\"\n]+)", fm)
    # 版本判据（v0.3.0 加固，U5 指出旧判据退化为"尾部含字母 v"）：
    #   接受点号版本（1.8.0 / v1.8.0）或 `vN`（如 schema v10）；拒绝 "whatever" / "（2026-09-28）" 这类非版本尾。
    VER_RE = re.compile(r"v\d+(?:\.\d+)+|\bv\d+\b|\d+\.\d+")
    ok_m2 = has_tail and bool(primary and primary.group(1).strip()) and len(docs) >= 6 \
        and all(VER_RE.search(d[1] or "") for d in docs)
    bad_m2 = [d[0] for d in docs if not VER_RE.search(d[1] or "")]
    rep.add("M2", "基线为逐文档版本（≥6 条且各含版本 + primary_source）", FAIL, ok_m2,
            "结构=%s；primary_source=%s；文档条目=%d" % (
                "有" if has_tail else "缺",
                (primary.group(1).strip() if primary else "缺"), len(docs))
            + ("；无版本尾：%s" % "、".join(bad_m2[:4]) if bad_m2 else ""))

    # R1/R2：路由表 vs contracts/
    routed = route_table_entries(skill)
    ghost = sorted(routed - files)
    rep.add("R1", "路由表引用的契约都存在（解析表格行 + 集合精确）", FAIL, not ghost,
            "幽灵契约：%s" % "、".join(ghost) if ghost else "全部存在（%d 个）" % len(routed))
    # 横切契约：必须在显式声明的块里（标题含「横切契约」），而不是任意 bullet
    # 行式收集：从含「横切契约」的行开始，连同**该行本身**直到空行 —— 不依赖跨行正则
    cross, collecting = set(), False
    for line in skill.splitlines():
        if "横切契约" in line:
            collecting = True
        elif collecting and not line.strip():
            break
        if collecting:
            cross |= {m for m in CONTRACT_REF.findall(line)}
    listed = cross
    routed_all = routed | listed
    orphan = sorted(files - routed_all)
    rep.add("R2", "每个契约都在路由表或横切契约块中（无孤儿）", FAIL, not orphan,
            "孤儿：%s" % "、".join(orphan) if orphan else "%d 个契约均被路由" % len(files))


    # R3：references/ 下每个文件都必须被入口引用（防**孤儿参考**——seedancer 的教训）
    #     职责边界：R3 只管「文件多余」，**不存在**（引用了却没有）由 L2 负责。
    refdir = os.path.join(ROOT, "references")
    orphan_ref = []
    if os.path.isdir(refdir):
        for f in sorted(os.listdir(refdir)):
            if f.endswith(".md") and f != "INDEX.md" and f not in skill:
                orphan_ref.append("references/" + f)
    rep.add("R3", "references/ 下无孤儿（多余文件；存在性见 L2）", FAIL, not orphan_ref,
            "孤儿：%s" % "、".join(orphan_ref) if orphan_ref else "无孤儿")

    # L1
    dead = []
    for path in [skill_p] + [os.path.join(cdir, f) for f in sorted(files)]:
        for t in MD_LINK.findall(read(path)):
            t = t.split("#")[0].strip()
            if not t or t.startswith(("http", "mailto:", "asset://")) or re.search(r"[<>{}*%]", t):
                continue
            base = os.path.dirname(path)
            if not (os.path.isfile(os.path.normpath(os.path.join(base, t)))
                    or os.path.isfile(os.path.normpath(os.path.join(ROOT, t)))):
                dead.append("%s → %s" % (os.path.relpath(path, ROOT), t))
    rep.add("L1", "相对路径引用可解析（markdown 链接）", FAIL, not dead,
            "死链：%s" % "；".join(dead[:6]) if dead else "无死链")

    # L2：被引用的**本地**相对文件都必须存在 —— 覆盖反引号 code span（L1 的盲区）
    #     仅认本地目录前缀 references|contracts|scripts，避免把上游路径（src/、docs/）误判。
    scan_l2 = ["SKILL.md"] + ["contracts/" + f for f in sorted(files)]
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in {".git", "scripts", "__pycache__"}]
        for fn in sorted(filenames):
            if fn.endswith(".md"):
                rel = os.path.relpath(os.path.join(dirpath, fn), ROOT).replace("\\", "/")
                if rel not in scan_l2:
                    scan_l2.append(rel)
    missing_ref = []
    for rel in scan_l2:
        p2 = os.path.join(ROOT, rel.replace("/", os.sep))
        if not os.path.isfile(p2):
            continue
        for ref in sorted(set(LOCAL_REF.findall(read(p2)))):
            relref = local_rel_path(ref)
            if not os.path.isfile(os.path.join(ROOT, *relref.split("/"))):
                missing_ref.append("%s → %s" % (rel, ref))
    rep.add("L2", "被引用的本地文件都存在（含反引号 code span）", FAIL, not missing_ref,
            "缺失：%s" % "；".join(sorted(set(missing_ref))[:6]) if missing_ref else "全部存在（%d 类前缀）" % 5)

    # X1/X2：横切参考的自洽与交叉一致
    #   X1  `field-registry.md` §1 的每张表都必须在 `schema-tables.md` 的表清单里（禁凭空多表）
    #   X2  两份参考文件**自述的计数**必须等于实际行数：
    #       · field-registry §1 总表数 / 总项数 / §3 集合表数 / **逐表 `（N 项）`**
    #       · schema-tables §2 自述「N 张」= §2 行数
    #       v0.3.0 加固（U5/U3 反例）：标题正则放宽（尾随空白 / 半角括号 / 无空格）并**查重复表名**；
    #       X2 增加**逐表**计数与 §2 自述计数（此前只比总和 → 改单表计数、删/加 §2 行都漏检）。
    fr_p = os.path.join(ROOT, "references", "field-registry.md")
    st_p = os.path.join(ROOT, "references", "schema-tables.md")
    SEC_H = re.compile(r"^###\s+`([A-Za-z_][A-Za-z0-9_]*)`\s*[（(]\s*(\d+)\s*项\s*[）)]\s*$")
    FR_ROW = re.compile(r"^\|\s*`([A-Za-z_][A-Za-z0-9_]*)`\s*\|\s*`")
    x1_bad, x2_bad = [], []
    if os.path.isfile(fr_p):
        fr = read(fr_p)
        sec1 = fr.split("## 1.")[1].split("## 2.")[0] if "## 1." in fr and "## 2." in fr else ""
        # §3 只取到**下一个二级标题**之前
        # （不硬编码 "## 4." —— 自测反例：把 §4 改名成 §3.5 会让硬编码边界失效，
        #   只读表被算进 §3 却不报错。见 `generated/_selftest_x2.py`）
        if "## 3." in fr:
            _rest = fr.split("## 3.", 1)[1]
            _nxt = re.search(r"^## ", _rest, re.M)
            sec3 = _rest[:_nxt.start()] if _nxt else _rest
        else:
            sec3 = ""
        # 逐表：标题计数 vs 实际行数；并查重复表名
        declared, actual, order = {}, {}, []
        cur = None
        for line in sec1.splitlines():
            hm = SEC_H.match(line)
            if hm:
                cur = hm.group(1)
                order.append(cur)
                declared[cur] = declared.get(cur, 0) + int(hm.group(2))
                actual.setdefault(cur, 0)
                continue
            if cur and FR_ROW.match(line):
                actual[cur] = actual.get(cur, 0) + 1
        dup = sorted({t for t in order if order.count(t) > 1})
        if dup:
            x2_bad.append("§1 重复表名：%s" % "、".join(dup[:3]))
        for t in order:
            if declared.get(t, 0) != actual.get(t, 0):
                x2_bad.append("§1 `%s` 自述 %d 项 ≠ 实际 %d" % (t, declared.get(t, 0), actual.get(t, 0)))
        fr_tables = sorted(set(order))
        n_items = sum(actual.values())
        # 总表数 / 总项数 / 集合表数
        m_self = re.search(r"可写字段总表（\*\*(\d+)\s*张表\s*/\s*(\d+)\s*项\*\*）", fr)
        if not m_self:
            x2_bad.append("§1 标题未声明「N 张表 / M 项」计数")
        else:
            if int(m_self.group(1)) != len(fr_tables):
                x2_bad.append("§1 自述表数 %s ≠ 实际 %d" % (m_self.group(1), len(fr_tables)))
            if int(m_self.group(2)) != n_items:
                x2_bad.append("§1 自述项数 %s ≠ 实际 %d" % (m_self.group(2), n_items))
        sec3_tables = re.findall(r"^\|\s*`([A-Za-z_][A-Za-z0-9_]*)`\s*\|", sec3, re.M)
        m_ad = re.search(r"集合表写回策略（\*\*(\d+)\s*张表\*\*）", fr)
        if not m_ad:
            x2_bad.append("§3 标题未声明集合表数")
        elif int(m_ad.group(1)) != len(sec3_tables):
            x2_bad.append("§3 自述集合表数 %s ≠ 实际 %d" % (m_ad.group(1), len(sec3_tables)))
        # X1：与 schema-tables.md §2 交叉（单向：可写表 ⊆ 全部表）；并校验 §2 自述计数
        #   v0.3.2 修复（U3 `REV-20261007-033`，27 变异实证）：
        #     ① **不硬编码节号字面量**：旧代码用 `split("## 4.")` —— 标题一旦改形
        #        （`## 四、` / 全角 `４` / 整行删除）字面量即失配，**整段守护被静默跳过**；
        #        现改由**节号正则**定位，且**找不到即报错**（不静默）。
        #     ② 小节标题正则**容忍空白**：`###  \`x\``（两空格）/ 前导缩进 / 全角空格
        #        在 CommonMark 下都是合法 H3，旧正则 `^### \`` 对它们**隐形**。
        #     ③ 先**剥离围栏代码块与 HTML 注释**（防"正文样例被当真标题"的假红）。
        #     ④ §4 补**重复名**检查；标题级别放宽到 3–6 级（防"用 `####` 藏假表名"）。
        def _strip_noise(s):
            s = re.sub(r"```.*?```", "", s, flags=re.S)
            return re.sub(r"<!--.*?-->", "", s, flags=re.S)

        def _section(s, num_pat, keyword):
            """按**节号 + 标题关键词**定位二级节：返回 `(标题行, 正文)`；找不到返回 `(None, None)`。

            为什么要 keyword（`REV-20261007-033` 的"假红 M5s/t"）：文件**别处**若出现
            形如 `## 4. 示例` 的行（引用/样例），只按节号取**首个匹配**会切错。
            要求标题含关键词即可精确定位；标题被改名则**找不到 → 报错**（不静默跳过）。
            """
            for m_ in re.finditer(r"^##[ \t\u3000]*" + num_pat + r"[ \t\u3000]*[.、．][^\n]*$", s, re.M):
                if keyword in m_.group(0):
                    rest = s[m_.end():]
                    nxt = re.search(r"^##[ \t\u3000]", rest, re.M)
                    return m_.group(0), (rest[:nxt.start()] if nxt else rest)
            return None, None

        if os.path.isfile(st_p):
            st = read(st_p)
            st_clean = _strip_noise(st)
            h2, body2 = _section(st_clean, r"[2２]", "全部表索引")
            st_rows = []
            if h2 is None:
                x2_bad.append("schema-tables §2 节标题缺失或无法按节号定位")
            else:
                st_rows = re.findall(r"^\|\s*`([A-Za-z_][A-Za-z0-9_]*)`\s*\|\s*`[^`]+`\s*\|\s*$", body2, re.M)
                m_st = re.search(r"（\**(\d+)\s*张", h2)
                if not m_st:
                    x2_bad.append("schema-tables §2 标题未声明「N 张」")
                elif int(m_st.group(1)) != len(st_rows):
                    x2_bad.append("schema-tables §2 自述 %s 张 ≠ 实际 %d" % (m_st.group(1), len(st_rows)))
                dup2 = sorted({t for t in st_rows if st_rows.count(t) > 1})
                if dup2:
                    x2_bad.append("schema-tables §2 重复表名：%s" % "、".join(dup2[:3]))
            x1_bad = sorted(set(fr_tables) - set(st_rows))

            # §4（全表字段清单，v0.3.2 新增）：自述表数 = 实际小节数；表名 ⊆ §2；无重复名
            #   守护理由：§4 是**机械生成**的（生成器 `work/regen_sec4_fields.py` 已被另一会话清理误删、
#   不可恢复 —— 见 `INC-20261007-001`；**§4 当前不可重生成**，任何手改必须靠本断言兜住）；上游更新后
            #   若只重生成一半、或只改自述不改内容，这里会报红。
            h4, body4 = _section(st_clean, r"[4４]", "全表字段清单")
            if h4 is None:
                x2_bad.append("schema-tables §4「全表字段清单」节缺失或无法按节号定位"
                              "（若已删除该节，须同步删除本守护）")
            else:
                heads4 = re.findall(r"^[ \t\u3000]*#{3,6}[ \t\u3000]+`([^`\n]+)`", body4, re.M)
                m_st4 = re.search(r"（\**(\d+)\s*表", h4)
                if not m_st4:
                    x2_bad.append("schema-tables §4 标题未声明「N 表」")
                elif int(m_st4.group(1)) != len(heads4):
                    x2_bad.append("schema-tables §4 自述 %s 表 ≠ 实际 %d 表" % (m_st4.group(1), len(heads4)))
                dup4 = sorted({t for t in heads4 if heads4.count(t) > 1})
                if dup4:
                    x2_bad.append("schema-tables §4 重复表名：%s" % "、".join(dup4[:3]))
                extra4 = sorted(set(heads4) - set(st_rows))
                if extra4:
                    x2_bad.append("schema-tables §4 含 §2 没有的表名：%s" % "、".join(extra4[:4]))
        else:
            x1_bad = ["schema-tables.md 缺失，无法交叉核对"]
    else:
        x1_bad = ["references/field-registry.md 缺失"]
    rep.add("X1", "field-registry 的表都在 schema-tables 表清单内", FAIL, not x1_bad,
            "多出：%s" % "、".join(x1_bad[:6]) if x1_bad else "无多出")
    rep.add("X2", "参考文件自述计数 = 实际行数（含逐表）", FAIL, not x2_bad,
            "；".join(x2_bad[:4]) if x2_bad else "计数一致（逐表 + 总计）")

    # C1
    triad = ("missing", "omitted", "partial-selection")
    trim_lines = [l for l in skill.splitlines() if ("裁剪" in l or "三态" in l)]
    ok_triad = any(all(k in l for k in triad) for l in trim_lines)
    # insufficient 只在**裁剪语境**下才算违规（避免与裁剪无关的用词造成假红）
    bad_line = [l for l in skill.splitlines()
                if "insufficient" in l and ("裁剪" in l or "omitted" in l or "missing" in l)]
    ok_c1 = ok_triad and not bad_line
    rep.add("C1", "裁剪三态为现行术语且旧词已清除", FAIL, ok_c1,
            ("裁剪语境仍含旧词 insufficient" if bad_line else "")
            + ("" if ok_triad else "；三态未与「裁剪/三态」同句出现（可能只是词表）")
            or "三态与裁剪同句，且裁剪语境无旧词")

    # C2
    words = ("OBSERVED", "INFERRED", "UNKNOWN")
    rule = any(k in skill for k in ("禁止编造", "不得编造", "不得把推断当事实", "必须标为 UNKNOWN", "UNKNOWN 或留空"))
    ok_c2 = all(k in skill for k in words) and rule
    rep.add("C2", "证据分级三词齐备且有规则句", FAIL, ok_c2,
            ("三词齐备" if all(k in skill for k in words) else "缺 " + "、".join(k for k in words if k not in skill))
            + ("；有规则句" if rule else "；**无**规则句（只是词表）"))

    # C3：逐行标注
    bad = []
    scan = ["SKILL.md"] + ["contracts/" + f for f in sorted(files)]
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in {".git", "scripts", "__pycache__"}]
        for fn in filenames:
            if fn.endswith(".md"):
                rel = os.path.relpath(os.path.join(dirpath, fn), ROOT).replace("\\", "/")
                if rel not in scan:
                    scan.append(rel)
    for rel in scan:
        for i, line in enumerate(read(os.path.join(ROOT, rel.replace("/", os.sep))).splitlines(), 1):
            if re.search(r"达芬奇|达文西|DaVinci", line) and not re.search(
                    r"环境来源|非源仓库基线|ai-memory|环境\(INFERRED\)|环境（INFERRED）", line):
                bad.append("%s:%d" % (rel, i))
    rep.add("C3", "含「达芬奇」的每一行都自带来源标注", FAIL, not bad,
            "未标注：%s" % "、".join(bad[:6]) if bad else "逐行均已标注")

    # A1 + 内容下限
    miss_a, thin = [], []
    for f in sorted(files):
        t = read(os.path.join(cdir, f))
        n = len([l for l in t.splitlines() if l.strip()])
        heads = len([l for l in t.splitlines() if l.startswith("#")])
        if n < MIN_LINES or len(t) < MIN_CHARS or heads < MIN_HEADINGS:
            thin.append("%s(%d 行/%d 字符/%d 标题)" % (f, n, len(t), heads))
        for k in ANCHORS.get(f, []):
            if k not in t:
                miss_a.append("%s:%s" % (f, k))
    rep.add("A1", "契约锚点齐备（%d 文件 / %d 锚点）"
            % (len(ANCHORS), sum(len(v) for v in ANCHORS.values())), FAIL, not miss_a,
            "缺失：%s" % "、".join(miss_a[:6]) if miss_a else "全部存在")
    rep.add("A2", "每份契约实质下限（≥%d 行 / ≥%d 字符 / ≥%d 标题）" % (MIN_LINES, MIN_CHARS, MIN_HEADINGS), FAIL, not thin,
            "过薄：%s" % "、".join(thin) if thin else "全部达标")

    # B1：基线表（正文） vs frontmatter documents 自洽
    table_docs = set(re.findall(r"`(docs/[A-Za-z0-9_./\-]+\.md)`", body)) \
        | {m for m in re.findall(r"\((docs/[A-Za-z0-9_./\-]+\.md)\)", body)}
    fm_docs = {d[0] for d in docs if d[0].startswith("docs/")}
    diff = sorted(fm_docs ^ table_docs)
    rep.add("B1", "基线表与 frontmatter documents 的文档集合一致", FAIL, not diff,
            "不一致：%s" % "、".join(diff[:6]) if diff else "%d 份文档两处一致" % len(fm_docs))


    # C4：provenance / evidenceGrade 的存放位置**单源一致**（用户使用中发现的跨文件矛盾）
    se_txt = read(os.path.join(ROOT, "contracts", "S-data-envelope.md")) if os.path.isfile(
        os.path.join(ROOT, "contracts", "S-data-envelope.md")) else ""
    problems4 = []
    if "旁车" not in se_txt:
        problems4.append("S-data-envelope.md 未声明旁车规则（权威缺失）")
    if "provenance" in skill:
        if "contracts/S-data-envelope.md" not in skill:
            problems4.append("SKILL.md 提到 provenance 但未指向权威 `contracts/S-data-envelope.md`")
        if "旁车" not in skill:
            problems4.append("SKILL.md 提到 provenance 但未说明「旁车文件」")
    # 冲突扫描：任何文件的该行若声称 provenance 进 JSON/记录内，且未含旁车/不得/sidecar 限定 → 冲突
    for rel in ["SKILL.md", "README.md", "CHANGELOG.md", "COMPAT.md"] + \
               ["contracts/" + f for f in sorted(files)]:
        p = os.path.join(ROOT, rel.replace("/", os.sep))
        if not os.path.isfile(p):
            continue
        for i, line in enumerate(read(p).splitlines(), 1):
            if "provenance" in line or "evidenceGrade" in line:
                risky = ("每块带" in line) or ("记录内" in line and "不得" not in line) or \
                        ("JSON 里" in line and "不得" not in line)
                ok_marker = ("旁车" in line) or ("sidecar" in line.lower()) or ("不得" in line) or \
                            ("S-data-envelope" in line)
                if risky and not ok_marker:
                    problems4.append("%s:%d 疑似与旁车规则冲突" % (rel, i))
    rep.add("C4", "provenance / evidenceGrade 存放规则单源一致", FAIL, not problems4,
            "；".join(problems4[:5]) if problems4 else "单源一致（权威：S-data-envelope.md §3）")

    # K1
    size = os.path.getsize(skill_p)
    ctotal = sum(os.path.getsize(os.path.join(cdir, f)) for f in files)
    if size > 60 * 1024:
        rep.add("K1", "体积预算", FAIL, False, "SKILL.md=%.1fKB 超过失败线 60KB" % (size / 1024))
    else:
        rep.add("K1", "体积预算（SKILL.md ≤16KB；每次加载都占上下文）", WARN,
                size <= 16 * 1024,
                "SKILL.md=%.1fKB；contracts 合计=%.1fKB" % (size / 1024, ctotal / 1024))

    # E1（v0.4.0）：行为评估集结构完备（**断言"技能被使用时怎么做"，不是文档自洽**）
    ev_p = os.path.join(ROOT, "evals", "behaviour.json")
    e1 = []
    if not os.path.isfile(ev_p):
        e1.append("evals/behaviour.json 缺失（行为评估集是 v0.4.0 起的交付项）")
    else:
        try:
            ev = json.loads(read(ev_p))
        except Exception as e:  # noqa: BLE001
            ev = None
            e1.append("evals/behaviour.json 不是合法 JSON：%s" % e)
        if not isinstance(ev, dict):
            e1.append("evals/behaviour.json 顶层必须是 JSON 对象，得到 %s"
                      % type(ev).__name__)
        else:
            items = ev.get("evals") or []
            if not isinstance(items, list):
                e1.append("evals 字段必须是 list")
                items = []
            if len(items) < 6:
                e1.append("评估条数 %d < 6" % len(items))
            for it in items:
                if not isinstance(it, dict):
                    e1.append("存在非对象条目")
                    continue
                i = it.get("id")
                for k in ("id", "prompt", "expected", "expectations"):
                    if not it.get(k):
                        e1.append("eval#%s 缺 %s" % (i, k))
                ex = it.get("expectations")
                if not isinstance(ex, list) or len(ex) < 2:
                    e1.append("eval#%s 的 expectations 少于 2 条（判据不可判定）" % i)
                elif any(not isinstance(x, str) or len(x.strip()) < 8 for x in ex):  # L5：判据须实质（≥8 字）
                    e1.append("eval#%s 的 expectations 含空项或过短（<8 字，不可判定）" % i)
            if items and not any(isinstance(it, dict) and it.get("counter_example") for it in items):
                e1.append("缺反例（至少 1 条 counter_example=true）")
    rep.add("E1", "行为评估集结构完备（≥6 条 · 每条 4 段 · ≥2 条判据 · 含反例）", FAIL, not e1,
            "；".join(e1[:4]) if e1 else "结构完备（%d 条）" % len((ev or {}).get("evals", [])))

    # D1（v0.5.0）：产物校验覆盖声明 ↔ 校验器代码
    d1 = []
    chk = os.path.join(ROOT, "scripts", "check_framework_artifact.py")
    try:
        import subprocess
        out = subprocess.run([sys.executable, chk, "--list-codes"], capture_output=True, text=True, timeout=60).stdout
        codes = {l.split()[0] for l in out.splitlines() if l.strip()}
    except Exception as e:  # noqa: BLE001
        codes = set()
        d1.append("无法运行 --list-codes：%s" % e)
    if not codes and not d1:
        d1.append("--list-codes 输出为空")
    code_re = re.compile(r"`([A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+)(?:_\*)?`")
    known_non_codes = {"CONTEXT_SOURCES", "FIELD_REGISTRY", "PROJECT_TABLES", "CURRENT_BACKUP_VERSION",
                       "STORYFORGE_SCHEMA_VERSION", "ADOPTION_EXTENSIONS", "ADOPTION_SCHEMAS",
                       "STORYFORGE_STORES", "CURRENT_EXPORT_VERSION", "CURRENT_PROJECT_EXPORT_KEYS"}
    for rel in ("contracts/INVARIANTS.md", "contracts/S-data-envelope.md", "contracts/A-longform.md", "README.md"):
        p_ = os.path.join(ROOT, rel)
        if not os.path.isfile(p_):
            continue
        for c in sorted(set(code_re.findall(read(p_)))):
            if c in known_non_codes or c.startswith("INV_"):
                continue
            if codes and c not in codes and not any(k.startswith(c) for k in codes):
                d1.append("%s 引用了校验器中不存在的问题码 `%s`" % (rel, c))
    for rel in ("SKILL.md", "README.md", "contracts/INVARIANTS.md"):
        p_ = os.path.join(ROOT, rel)
        if os.path.isfile(p_) and re.search(r"覆盖\s*\**6\s*类", read(p_)):
            d1.append("%s 仍写「覆盖 6 类违规」（过时，问题码以 --list-codes 为准）" % rel)
    rep.add("D1", "产物校验覆盖声明 ↔ 校验器问题码一致", FAIL, not d1,
            "；".join(d1[:4]) if d1 else "一致（%d 个问题码）" % len(codes))

    # V2：版本与断言数的「当前态」声明必须自洽（根治 v0.2.1→v0.2.2 那种四处数字互不一致）
    #     注意：本断言计入总数，故 total = 已登记项 + 1（自身）。
    total = len(rep.items) + 1
    v2 = []
    # 先验存在性：这三个是「当前态声明文件」，缺失即 FAIL（否则下面的 if isfile 会静默跳过）
    for fn, why in (("README.md", "入口说明"), ("COMPAT.md", "工作副本说明"), ("skill-card.md", "ClawHub 卡片")):
        if not os.path.isfile(os.path.join(ROOT, fn)):
            v2.append("%s 缺失（%s，当前态声明文件必须有）" % (fn, why))
    mver = re.search(r"本技能版本\*{0,2}\s*[：:]\s*\*{0,2}\s*v?([\d.]+)", skill)
    if not mver:
        v2.append("SKILL.md 未找到「本技能版本」声明")
    elif ver and mver.group(1) != ver:
        v2.append("SKILL.md 本技能版本 v%s ≠ frontmatter %s" % (mver.group(1), ver))
    mcnt = re.search(r"本技能版本[^\n]*?（\s*(\d+)\s*项断言）", skill)
    if not mcnt:
        v2.append("SKILL.md「本技能版本」行未声明断言数")
    elif int(mcnt.group(1)) != total:
        v2.append("SKILL.md 声明 %s 项断言 ≠ 实际 %d" % (mcnt.group(1), total))
    readme_p = os.path.join(ROOT, "README.md")
    if os.path.isfile(readme_p):
        for n in sorted(set(re.findall(r"(\d+)\s*项断言", read(readme_p)))):
            if int(n) != total:
                v2.append("README.md 声明 %s 项断言 ≠ 实际 %d" % (n, total))
    card_p = os.path.join(ROOT, "skill-card.md")
    if os.path.isfile(card_p):
        mc = re.search(r"Skill Version\(s\):\s*<br>\s*\n\s*([\d.]+)", read(card_p))
        if mc and ver and mc.group(1) != ver:
            v2.append("skill-card.md 版本 %s ≠ frontmatter %s" % (mc.group(1), ver))
    compat_p = os.path.join(ROOT, "COMPAT.md")
    if os.path.isfile(compat_p):
        ct = read(compat_p)
        mcv = re.search(r"\|\s*当前版本\s*\|\s*\*\*v?([\d.]+)\*\*", ct)
        if mcv and ver and mcv.group(1) != ver:
            v2.append("COMPAT.md 当前版本 %s ≠ frontmatter %s" % (mcv.group(1), ver))
        if ("**%d（现行）**" % total) not in ct:
            v2.append("COMPAT.md 未标注现行断言数 %d" % total)
        for n in re.findall(r"技能包自检[（(，,\s]*(\d+)\s*项", ct):
            if int(n) != total:
                v2.append("COMPAT.md「技能包自检 %s 项」≠ 实际 %d" % (n, total))
    inv_p = os.path.join(ROOT, "contracts", "INVARIANTS.md")
    if os.path.isfile(inv_p):
        for n in re.findall(r"技能包自检[（(，,\s]*(\d+)\s*项", read(inv_p)):
            if int(n) != total:
                v2.append("INVARIANTS.md「技能包自检 %s 项」≠ 实际 %d" % (n, total))
    rep.add("V2", "版本与断言数的当前态声明自洽", FAIL, not v2,
            "；".join(v2[:4]) if v2 else "一致（v%s / %d 项）" % (ver, total))
    # 自检：V2 必须是**最后一项**，否则 total 的自增假设失效（U5 指出：正常结构下该守卫恒假，
    # 真正能抓"删掉 V2 整段"的是仓库侧外部断言 I21，见 tests/integration/run_integration.py）
    if len(rep.items) != total:
        rep.items[-1]["ok"] = False
        rep.items[-1]["detail"] = ("**内部错误**：V2 非最后一项（len=%d ≠ total=%d）—— "
                                   "total 计算失效，请把 V2 移到所有 rep.add 之后"
                                   % (len(rep.items), total))

    if "--json" in argv:
        print(json.dumps({"fail": len(rep.fails), "warn": len(rep.warns), "items": rep.items},
                         ensure_ascii=False, indent=2))
    else:
        quiet = "--quiet" in argv
        print("== storyforge-writing 一致性检查 v5")
        for i in rep.items:
            if i["ok"] and quiet:
                continue
            mark = "OK  " if i["ok"] else ("FAIL" if i["level"] == FAIL else "WARN")
            print("[%s] %-3s %s — %s" % (mark, i["id"], i["title"], i["detail"]))
        print("RESULT: %s (%d fail, %d warn)" % ("PASS" if not rep.fails else "FAIL",
                                                 len(rep.fails), len(rep.warns)))
    return 0 if not rep.fails else 1


if __name__ == "__main__":
    raise SystemExit(main())
