#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_consistency.py — seedancer 一致性 + 硬门检查器（v5，零依赖）

v5 相对 v4 的新增（`PLAN-20261006-001` 的 G2 与 G3'）：
  · G2 **脚本执行可靠性**：每个**检查组**开跑前向 **stderr** 打 `[RUN ] <编号> <说明>` 并 flush
       —— 中断时最后一行就是断点（此前只在最后汇总，中断后看不出跑到哪）；`--quiet` 时不打。
       打在 stderr 是为了**保住 stdout 的解析契约**（`--json` 只走 stdout）。
       （粒度是**按检查组**：19 项 → 10 个检查组 + 1 个收尾行 = 11 行 `[RUN ]`，不是逐条 —— 由 `REV-20261006-023` W6 指出措辞）
  · G3' **规范枚举一致性（A3）**：同一"硬门要素集"在任何**同行枚举**处必须**完整且同序**。
       我最初判定原 G3（"把「四项事实」在入口的 5 处删到 2 处"）**不可达**，理由是三条约束 ——
       该结论**已被 `REV-20261006-025` 证伪**（其中两条归因错、一条误用"下沉即失能"）。
       故原 G3 **已实施（用户决策 D7）**：保留契约区注释与定义节标题，另三处改为**文件内指针**。
       本断言（A3）是与之配套的"把重复变成受守护的一致性"（**WARN 级**）。
  · `A4` **文件内指针可解析**（TD-10）：`见 §主 · 子` 的主标题必须**唯一存在**；
       带 `· 子` 时，子标题必须是**比主标题更深层级**、且落在**主标题范围内**的标题。
       动因：D7 重写时我写的指针 `见 §输出格式硬门 · 镜头自然段写法` **字符串比对能过**，
       但那个「·」想表达的层级关系并不成立 —— 引用类断言此前从不"实地走一遍"
       （`REV-20261006-027` W2-a）。
       ⚠️ **A4 不能保证"被指向的内容真的在那里"**（那是语义问题）：它只验"标题存在且层级关系成立"。
       故 `CHANGELOG`/`COMPAT` 中说它"防错位指针"是**过高表述**，已收敛（见各文件）。
  （本版合计 **19 项**）

v4 相对 v3 的新增（依据 RETRO-20261006-008 模式 4「检查器假绿」+ 攻击测试实证）：
  · A2  关键小节的**内容行**必须存在 —— v3 的 A1 只断言"短语在节内存在"，
        删掉整段内容只留标题时仍会 PASS（tests/attack_test.py 实测 6/6 漏网）。
        现由 SECTION_CONTENT 逐节断言：①必需内容行逐字存在 ②**该节标题在同级必须唯一**
        （防"清空真段体 + 文末追加同名诱饵段"绕过）③**非标题内容行数 ≥ 必需词数**
        （防"整张表换成一句罗列"式掏空）。攻击测试守护该断言。
        ⚠️ 仍**不保证语义完整**：A2 是**字面子串存在性**，同义改写、删掉定义只留小标题、
           同一关键词在别行再次出现 —— 这三种仍可能漏检（见下方「已知限制」）。

v3 相对 v2 的新增（依据 ClawHub 安全评审 [SDI-1] 与 v9.0.1 发布复盘）：
  · V3  skill-card.md 的「Skill Version(s)」字段必须 == 权威版本（v2 的已知盲区）
  · V4  skill-card.md 的 Publisher 必须 == _meta.json 的 author

v2 相对 v1 的修复（依据 REV-20261005-010 的"假绿"清单）：
  · M3  改用 json.loads 按键精确比较（v1 对 JSON 格式的 _meta.json 完全空转）
  · M4  来源清单改为从 _meta.json.upstream_sources **推导**并与 LICENSE **单向**核对
        （即 upstream_sources ⊆ LICENSE；v1 是硬编码 8 token。早先此处误写"双向"，已更正）
  · I1  INDEX 与加载表都改为**集合精确匹配**（v1 用 OR + 子串，与文档矛盾）
  · I3  加载表条目改为**集合精确**；每个触发时机必须在 SKILL.md 的**加载表之外**真实出现
        （v1 只做子串匹配，28 篇塞进一行"(未定位)"即骗过）
  · D1  修滑窗计量（v1 每命中 +8 导致 12 行报"≥296 行"）；白名单改为**契约检查**：
        标注必须写明 target=<file>，且**围栏模板里的区块名与两张词表**必须在 target 中逐字存在
        （由 D2 断言：模板逐行 + CONTRACT_KEY_LINES 逐条）
  · V1  取**全部**版本戳比对（v1 只取首末），并纳入 README/docs 标题行
  · A*  新增 28 条**硬门锚点**断言（此前只存在于一次性施工脚本，声明"缺一即构建失败"无实现）
  · K1  预算：>44KB WARN，>52KB FAIL

用法：
    python scripts/check_consistency.py [--json] [--quiet]
退出码：0 = 无 FAIL；1 = 存在 FAIL；2 = 用法/环境错误

已知限制（如实声明，勿当成"已覆盖"）：
  · V1 只比对**版本戳**（_meta/VERSION/frontmatter/标题戳/末戳/徽章/CHANGELOG），
    **不覆盖** COMPAT.md、release-notes.md、references/ 内页脚 —— 这些位置仍可能残留旧版本号
    （skill-card.md 自 v3 起改由 V3/V4 覆盖，不再属于 V1 盲区）
  · M4 为**单向**（_meta.upstream_sources ⊆ LICENSE）；LICENSE 多出的来源不会被报出
  · I1/I2/I3 依赖**表格格式**（首列为触发时机、次列反引号文件名）；换格式会误报
  · D1 只比 SKILL.md ↔ references，reference 之间互抄不查；且为 WARN 级
  · A1 是"关键短语在应有节内存在"，**不等于该节完整**（删掉整节而短语在别处仍出现 → 不报）
  · A2 覆盖 SECTION_CONTENT 里的 7 节，且为**字面子串**判据。已实证的**残余漏检**（`REV-20261006-018/021`）：
    ① **删掉定义只留小标题**（`2. **观察关系**`）不报；
    ② **占位行凑数**（1 行必需词 + N 行"（占位）"）满足"行数下限"但不报；
    ③ **语义反转**（把 `=` 改成 `≠`、加"禁止"）仍按字面通过；
    ④ **把词藏进代码围栏 / `>` 引用块**能冒充内容 —— **设计使然**：硬门等式本就写在围栏里，
       剥离围栏会把合法内容判成缺失（实测误红），故不剥离；
    ⑤ **未列入 SECTION_CONTENT 的小节**仍可被"删内容留标题"（需要覆盖请加入该表并同步 `tests/attack_test.py`）
    （已加固而**不再漏检**的：同义改写必需词→**会报红**；清空段体+**2–6 级**同名诱饵段→报红；
    **HTML 注释**包词→报红）
  · A2 **会误拦合法改写**：把必需词换成同义词（`视觉起点`→`画面起点`）→ 报"缺内容行"；
    把该节降成 4 级标题 → 报"节缺失"；把 4 行合并成 3 行 → 报"内容行 3 < 必需词 4"。
    这是"字面锁"的固有代价：**对行数/字节敏感、对语义无感** —— 既拦不住掏空，也拦得住等价改写。改前请同步本表
  · A2 的标题唯一性按 **2–6 级**统计；但 `SECTION_CONTENT` 的键本身若被改名（如加空格/半角括号）会报"节缺失"
  · A3 只守护 `ENUM_GUARDS` 里的要素集（当前仅「四项事实」），且**只在"整行完整包含全部键"时**校验**顺序**；
    **部分枚举（少一个键）完全不在判据内**；不判"是否多出其它要素"；跨行枚举不查；
    代码围栏内的整行枚举**算内容**（与 `A2` 取舍一致）
  · A3 为 **WARN 级**（不阻塞构建）—— 它由"分隔符启发式"两度收紧而来，
    历史版本分别被 `REV-20261006-024`（假红）与 `REV-20261006-025`（11 个反例）证伪；
    现行版**删去一切分隔符猜测**，宁可少报不可误报
  · A3 与 A2 对 HTML 注释的处理已统一（A3 整篇剥、A2 整段剥）；此前**跨行注释**两侧双标（`REV-20261006-026`）
  · G2 的逐步状态打在 **stderr**（`--quiet` 不打印）；`--json` 的 stdout 契约不受影响；
    粒度是**按检查组**（19 项 → 10 个检查组 + 1 收尾行），不是逐条
  · D2 只取**契约区首个围栏**模板，且逐行比对**跳过 <12 字符的行**（短行不校验）
  · K1 只测入口体积，references/ 总量无上限；且 K1 的 WARN 分支不升级为 FAIL
"""

from __future__ import annotations

import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAIL, WARN = "FAIL", "WARN"
SKIP_DIRS = {".git", "_git_baseline", "__pycache__", "node_modules"}
MD_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
BARE_REF = re.compile(r"(?<![(\w/])references/([A-Za-z0-9_\-]+\.md)")
VERSION_RE = re.compile(r"Seedancer v(\d+\.\d+\.\d+)")
BADGE_RE = re.compile(r"version-(\d+\.\d+\.\d+)-")
RUNTIME_DIRS = ("runs/", "outputs/", "04-prompts/", ".seedancer/")   # 运行期产物（复核后收窄）

# 硬门锚点：这些字符串必须存在于入口（删内容时若丢失即构建失败）
ANCHORS = [
    "九条黄金规则", "SCALE LAW", "矛盾检测", "硬门总览", "核心硬规则", "台词容量",
    "分组硬门", "镜头密度", "隐藏切镜", "Smin", "Bmin", "Gmax", "承接等式", "组尾",
    "运镜设计", "主动运镜三要素", "输出格式硬门", "逐字使用", "四项事实",
    "空间与人物指代硬门", "媒介翻译表", "体量控制", "CINEDANCE 16-block", "Style Prefix",
    "交付物体系", "视频模型选用前必须先询问用户", "失败现象对照表", "参考文档加载表",
]
# 契约区必须逐字存在于 target 的关键串（区块名 + 词表锚点）
CONTRACT_KEY_LINES = [
    "## 使用的 @资产清单", "## 状态资产引用", "## 参数确认", "## 全局风格提示词",
    "## 角色音色设定", "## 第1组：组标题", "### 每镜四项事实（缺一不可）", "### 时间码规范",
]


def read(path):
    with io.open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def walk(root=None, exts=None):
    root = root or ROOT
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if exts is None or name.endswith(exts):
                yield os.path.join(dirpath, name)


class Report:
    def __init__(self):
        self.items = []

    def add(self, cid, title, level, ok, detail=""):
        self.items.append({"id": cid, "title": title, "level": level,
                           "ok": bool(ok), "detail": detail})

    @property
    def fails(self):
        return [i for i in self.items if not i["ok"] and i["level"] == FAIL]

    @property
    def warns(self):
        return [i for i in self.items if not i["ok"] and i["level"] == WARN]


SKILL = "SKILL.md"


def skill_text():
    p = os.path.join(ROOT, SKILL)
    return read(p) if os.path.isfile(p) else ""


def load_table(skill):
    m = re.search(r"(?ms)^##\s*参考文档加载表.*?(?=^##\s|\Z)", skill)
    return m.group(0) if m else ""


def load_table_entries(skill):
    """返回 {文件名: 触发时机}（从加载表表格行精确解析）。"""
    out = {}
    for line in load_table(skill).splitlines():
        if not line.startswith("|") or "---" in line or "门控 / 阶段" in line:
            continue
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if len(cells) < 2:
            continue
        trigger = cells[0]
        for f in re.findall(r"`([A-Za-z0-9_\-]+\.md)`", cells[1]):
            out[f] = trigger
    return out


# ---------- V ----------
def check_versions(rep):
    try:
        meta = json.loads(read(os.path.join(ROOT, "_meta.json")))
        authority = meta.get("version", "")
    except Exception as e:  # noqa: BLE001
        rep.add("V1", "版本戳多处一致", FAIL, False, "_meta.json 无法解析：%s" % e)
        return ""
    seen = {}
    if os.path.isfile(os.path.join(ROOT, "VERSION")):
        seen["VERSION"] = read(os.path.join(ROOT, "VERSION")).strip()
    skill = skill_text()
    fm = skill.split("---", 2)[1] if skill.startswith("---") else ""
    m = re.search(r"^version:\s*\"?([\d.]+)", fm, re.M)
    seen["SKILL.md(frontmatter)"] = m.group(1) if m else "(未找到)"
    stamps = VERSION_RE.findall(skill)
    if not stamps:
        seen["SKILL.md(标题戳)"] = "(未找到)"
    else:
        seen["SKILL.md(标题戳)"] = stamps[0]
        seen["SKILL.md(末戳)"] = stamps[-1]
        if len(set(stamps)) > 1:
            seen["SKILL.md(全部戳)"] = "/".join(sorted(set(stamps)))
    ch = read(os.path.join(ROOT, "CHANGELOG.md")) if os.path.isfile(os.path.join(ROOT, "CHANGELOG.md")) else ""
    m = re.search(r"v?(\d+\.\d+\.\d+)", ch[:400])
    seen["CHANGELOG.md"] = m.group(1) if m else "(未找到)"
    for rel, key in (("README.md", "README.md"), ("docs/README-cn.md", "docs/README-cn.md")):
        p = os.path.join(ROOT, rel)
        if not os.path.isfile(p):
            continue
        t = read(p)
        m = BADGE_RE.search(t)
        seen[key + "(徽章)"] = m.group(1) if m else "(未找到)"
        m = VERSION_RE.search(t)
        if m:
            seen[key + "(标题戳)"] = m.group(1)
    bad = {k: v for k, v in seen.items() if v != authority}
    rep.add("V1", "版本戳全部一致（含标题/末戳/徽章）", FAIL, not bad,
            "权威=_meta.json(%s)；不一致：%s" % (authority, "、".join("%s=%s" % kv for kv in bad.items()))
            if bad else "%d 处一致（%s）；跳过：release-notes.md(v7.x 存档)、LICENSE(归因区块版本中立)"
            % (len(seen), authority))
    # V2：CHANGELOG 必须有**结构化**条目（标题行或表格行），不是子串
    pat = re.compile(r"(^#+\s*Seedancer v%s\b)|(^\|\s*\*{0,2}v%s\b)" % (re.escape(authority), re.escape(authority)), re.M)
    rep.add("V2", "CHANGELOG 有当前版本的结构化条目", FAIL, bool(pat.search(ch)),
            "未找到形如 '# Seedancer v%s 更新日志' 或表格行的条目" % authority if not pat.search(ch)
            else "已找到结构化条目")
    # V3/V4：skill-card.md 的版本戳与 Publisher 必须与权威元数据一致
    # （v3 新增；此前 skill-card.md 是 V1 的已知盲区 —— 见文件头"已知限制"）
    sc_p = os.path.join(ROOT, "skill-card.md")
    if os.path.isfile(sc_p):
        sc = read(sc_p)
        mv = re.search(r"^##\s*Skill Version\(s\):[^\n]*\n(.+)$", sc, re.M)
        vm = re.search(r"(\d+\.\d+\.\d+)", mv.group(1)) if mv else None
        got_v = vm.group(1) if vm else "(未找到)"
        rep.add("V3", "skill-card.md 版本戳 == 权威版本", FAIL, got_v == authority,
                "skill-card.md 版本=%s vs 权威=%s" % (got_v, authority) if got_v != authority
                else "skill-card.md 版本一致（%s）" % got_v)
        author = str(meta.get("author", "")).strip()
        pub = sc.split("## Publisher:", 1)[1].split("###", 1)[0] if "## Publisher:" in sc else ""
        pm = re.search(r"clawhub\.ai/user/([A-Za-z0-9_\-]+)", pub)
        got_p = pm.group(1) if pm else "(未找到)"
        rep.add("V4", "skill-card.md Publisher == _meta.json author", FAIL,
                bool(author) and got_p == author,
                "publisher=%s vs author=%s" % (got_p, author) if got_p != author
                else "Publisher 一致（%s）" % got_p)
    else:
        rep.add("V3", "skill-card.md 版本戳 == 权威版本", FAIL, False, "skill-card.md 不存在")
    return authority


# ---------- M ----------
def check_metadata(rep):
    meta_p = os.path.join(ROOT, "_meta.json")
    try:
        meta = json.loads(read(meta_p))
        rep.add("M1", "_meta.json 是合法 JSON", FAIL, True, "json.loads 通过")
    except Exception as e:  # noqa: BLE001
        rep.add("M1", "_meta.json 是合法 JSON", FAIL, False, "解析失败：%s" % e)
        meta = {}
    skill = skill_text()
    fm = skill.split("---", 2)[1] if skill.startswith("---") else ""
    required = ["name", "description", "license", "author", "version", "tags", "platforms"]
    empty = [k for k in required if not re.search(r"^%s:\s*\S" % k, fm, re.M)]
    rep.add("M2", "frontmatter 7 字段齐备且非空", FAIL, not empty,
            "缺或空：%s" % "、".join(empty) if empty else "7 个字段齐备且非空")
    diffs = []
    for key in ("name", "version", "license", "author"):
        m = re.search(r"^%s:\s*\"?([^\"\n]+)\"?\s*$" % key, fm, re.M)
        a = m.group(1).strip() if m else ""
        b = str(meta.get(key, "")).strip()
        if not a or not b:
            diffs.append("%s: frontmatter=%r vs _meta=%r（有空值）" % (key, a, b))
        elif a != b:
            diffs.append("%s: frontmatter=%s vs _meta=%s" % (key, a, b))
    rep.add("M3", "frontmatter 与 _meta.json 逐字段一致", FAIL, not diffs,
            "；".join(diffs) if diffs else "4 个关键字段一致")
    # M4：来源清单由 _meta.json 推导，与 LICENSE **单向**核对（upstream_sources ⊆ LICENSE）
    #     （早先此处注释误写"双向"，与 docstring 及实现不符 —— 由 REV-20261006-017/020 抓出并更正）
    sources = meta.get("upstream_sources") or []
    lic = read(os.path.join(ROOT, "LICENSE"))
    if not sources:
        rep.add("M4", "LICENSE 归因与 _meta.json 来源清单一致（合规）", FAIL, False,
                "_meta.json 缺 upstream_sources（无法推导来源清单）")
    else:
        miss = [s for s in sources if s not in lic]
        rep.add("M4", "LICENSE 归因与 _meta.json 来源清单一致（合规）", FAIL, not miss,
                "LICENSE 缺来源：%s" % "、".join(miss) if miss
                else "%d 个来源均在 LICENSE 有归因" % len(sources))


# ---------- L ----------
def check_links(rep):
    dead = []
    for path in walk(exts=(".md", ".json", ".sh", ".txt")):
        rel = os.path.relpath(path, ROOT).replace("\\", "/")
        text = read(path)
        targets = set(MD_LINK.findall(text)) | set("references/" + m for m in BARE_REF.findall(text))
        for t in targets:
            t = t.split("#")[0].strip()
            if not t or t.startswith(("http", "mailto:", "asset://")):
                continue
            if re.search(r"[<>{}*%]", t):      # 模板占位（{} <> * % 一致处理）
                continue
            if any(t.startswith(d) or ("/" + d) in t for d in RUNTIME_DIRS):
                continue
            cand_abs = os.path.normpath(os.path.join(os.path.dirname(path), t))
            cand_root = os.path.normpath(os.path.join(ROOT, t))
            if not (os.path.isfile(cand_abs) or os.path.isfile(cand_root)
                    or os.path.isdir(cand_abs) or os.path.isdir(cand_root)):
                dead.append("%s → %s" % (rel, t))
    rep.add("L1", "相对路径引用均可解析（无死链）", FAIL, not dead,
            "死链 %d 处：%s" % (len(dead), "；".join(sorted(set(dead))[:10])) if dead else "无死链")


# ---------- I ----------
def check_index(rep):
    ref_dir = os.path.join(ROOT, "references")
    refs = {f for f in os.listdir(ref_dir) if f.endswith(".md") and f != "INDEX.md"} \
        if os.path.isdir(ref_dir) else set()
    idx_p = os.path.join(ref_dir, "INDEX.md")
    idx = read(idx_p) if os.path.isfile(idx_p) else ""
    idx_set = set(re.findall(r"^\|\s*`([A-Za-z0-9_\-]+\.md)`", idx, re.M))
    skill = skill_text()
    table = load_table_entries(skill)
    table_set = set(table)

    missing_idx = sorted(refs - idx_set)
    extra_idx = sorted(idx_set - refs)
    rep.add("I1", "references 集合 == INDEX 集合（精确）", FAIL, not (missing_idx or extra_idx),
            "缺登记：%s；多登记：%s" % ("、".join(missing_idx) or "无", "、".join(extra_idx) or "无")
            if (missing_idx or extra_idx) else "%d 篇精确一致" % len(refs))

    missing_tbl = sorted(refs - table_set)
    extra_tbl = sorted(table_set - refs)
    rep.add("I2", "references 集合 == 加载表集合（精确）", FAIL, not (missing_tbl or extra_tbl),
            "未接线：%s；幽灵条目：%s" % ("、".join(missing_tbl) or "无", "、".join(extra_tbl) or "无")
            if (missing_tbl or extra_tbl) else "%d 篇精确一致" % len(refs))

    # I3：每个触发时机必须在 SKILL.md 的**加载表之外**真实出现（堵 "(未定位)" 兜底）
    outside = skill.replace(load_table(skill), "")
    heading_lines = {re.sub(r"^#{2,6}\s*", "", l).strip() for l in outside.splitlines()
                     if re.match(r"^#{2,6}\s", l)}
    triggers = set(table.values())
    empty = sorted(n for n, tv in table.items() if not tv.strip())
    phantom = sorted(t for t in triggers if t and t not in heading_lines)
    problems = []
    if empty:
        problems.append("空触发：%s" % "、".join(empty[:5]))
    if phantom:
        problems.append("非标题触发：%s" % "、".join(phantom[:5]))
    rep.add("I3", "加载表触发时机必须是正文中真实标题行", FAIL, not problems,
            "；".join(problems) if problems
            else "%d 个触发时机均为真实标题行" % len(triggers))


# ---------- D ----------
def check_duplication(rep, threshold=40):
    skill_p = os.path.join(ROOT, SKILL)
    raw = read(skill_p)
    m = re.search(r"(?ms)<!--\s*dup-allow-start[^>]*-->", raw)
    contract = ""
    if m:
        j = raw.find("<!-- dup-allow-end -->", m.end())
        contract = raw[m.end():j] if j > 0 else ""
    body = re.sub(r"(?ms)<!--\s*dup-allow-start.*?<!-- dup-allow-end -->", "", raw)
    lines = [l.strip() for l in body.splitlines()]
    idx = {}
    for i in range(len(lines) - 8 + 1):
        w = tuple(lines[i:i + 8])
        if sum(len(x) for x in w) > 60:
            idx.setdefault(w, i + 1)
    hits = []
    for path in walk(os.path.join(ROOT, "references"), (".md",)):
        rl = [l.strip() for l in read(path).splitlines()]
        run = 0
        start = 0
        for k in range(len(rl) - 8 + 1):
            if tuple(rl[k:k + 8]) in idx:
                if run == 0:
                    start = idx[tuple(rl[k:k + 8])]
                run += 1                      # 滑窗步进 1 行 → 连续行数 = run + 7
            else:
                if run + 7 >= threshold:
                    hits.append("%s ↔ SKILL.md:%d 连续 ≥%d 行" % (os.path.basename(path), start, run + 7))
                run = 0
        if run + 7 >= threshold:
            hits.append("%s ↔ SKILL.md:%d 连续 ≥%d 行" % (os.path.basename(path), start, run + 7))
    rep.add("D1", "无大段逐字重复（契约区除外，阈值 %d 行）" % threshold, WARN, not hits,
            "；".join(hits[:6]) if hits else "未发现大段逐字重复")

    # D2：契约区必须真的与目标文件一致（把白名单从"豁免"变成"更强的检查"）
    tm = re.search(r"target=([A-Za-z0-9_\-]+\.md)", m.group(0)) if m else None
    if not tm:
        rep.add("D2", "契约区标注了目标文件并可校验", FAIL, False,
                "dup-allow-start 未写 target=<file>，无法校验契约区")
    else:
        target_p = os.path.join(ROOT, "references", tm.group(1))
        if not os.path.isfile(target_p):
            rep.add("D2", "契约区目标文件存在", FAIL, False, "references/%s 不存在" % tm.group(1))
        else:
            tgt_text = read(target_p)
            tgt_lines = {l.strip() for l in tgt_text.splitlines() if len(l.strip()) >= 12}
            tpl = re.search(r"(?ms)```[a-z]*\n(.*?)```", contract)
            body = tpl.group(1) if tpl else contract
            miss_lines = [l.strip() for l in body.splitlines()
                          if len(l.strip()) >= 12 and l.strip() not in tgt_lines]
            # 区块名 + 两张词表锚点：必须逐字存在于 target（此前 CONTRACT_KEY_LINES 定义后**零引用**，
            # 声明了"契约区逐字校验"却完全空转 —— 由 REV-20261006-017/018 抓出并在此接上）
            miss_keys = [k for k in CONTRACT_KEY_LINES if k not in tgt_text]
            problems = ([("模板缺 %d 行：%s" % (len(miss_lines), " ｜ ".join(miss_lines[:3])))
                         if miss_lines else ""]
                        + [("缺区块名/词表 %d 条：%s" % (len(miss_keys), " ｜ ".join(miss_keys[:3])))
                           if miss_keys else ""])
            problems = [p for p in problems if p]
            rep.add("D2", "契约区（模板逐行 + 区块名/词表锚点）都在目标文件中", FAIL, not problems,
                    "目标 %s：%s" % (tm.group(1), "；".join(problems)) if problems
                    else "模板 %d 行 + 锚点 %d 条全部存在于 %s"
                         % (len(body.splitlines()), len(CONTRACT_KEY_LINES), tm.group(1)))


# ---------- A / K ----------
ANCHOR_SECTION = {
    "九条黄金规则": "九条黄金规则", "SCALE LAW": "SCALE LAW", "矛盾检测": "矛盾检测",
    "硬门总览": "五大硬门系统", "核心硬规则": "五大硬门系统",
    "台词容量": "台词容量预检", "分组硬门": "分组硬门", "承接等式": "分组硬门", "组尾": "分组硬门",
    "镜头密度": "镜头密度四道门", "隐藏切镜": "镜头密度四道门",
    "Smin": "镜头密度四道门", "Bmin": "镜头密度四道门", "Gmax": "镜头密度四道门",
    "运镜设计": "运镜设计", "主动运镜三要素": "运镜设计",
    "输出格式硬门": "输出格式硬门", "逐字使用": "输出格式硬门", "四项事实": "输出格式硬门",
    "空间与人物指代硬门": "空间与人物指代硬门", "媒介翻译表": "媒介翻译表", "体量控制": "体量控制",
    "CINEDANCE 16-block": "CINEDANCE", "Style Prefix": "Style Prefix",
    "交付物体系": "交付物体系", "视频模型选用前必须先询问用户": "模型自动选择系统",
    "失败现象对照表": "失败现象对照表", "参考文档加载表": "参考文档加载表",
}

# A2：关键小节必须包含这些**内容行**（防「删内容留标题」的假绿）
#     本轮 G1 新增；对应版本号升级与否见 `PLAN-20261006-001` §4 的 D2（**未确认前不写死版本号**）
# 守护：tests/attack_test.py（在**临时副本**上变异，不再原地改写本技能目录）
SECTION_CONTENT = {
    "每镜四项事实（缺一不可）": ["视觉起点", "观察关系", "构图落位", "摄影机状态"],
    "主动运镜三要素（缺一不可）": ["起始观察点", "运动轨迹方向", "停止结果"],
    "承接等式": ["上一组末尾空间状态", "下一组人物空间站位"],
    "时间码规范": ["整数秒", "不重叠", "组时长"],
    "台词写法": ["逐字嵌入", "引号"],
    "硬门总览": ["台词容量", "分组硬门", "镜头密度", "运镜设计"],
    "核心硬规则（不可跳过）": ["台词容量预检先于分组", "组尾必须是可继承稳定状态", "承接等式"],
}

# A3（G3'）：规范枚举一致性 —— 同一"硬门要素集"在任何**同行枚举**处必须完整且同序。
#   为什么这么写（而不是按 G3 原计划删重复）：见 check_canonical_enumerations 的 docstring。
ENUM_GUARDS = {
    "四项事实": SECTION_CONTENT["每镜四项事实（缺一不可）"],
}

# G2：是否打印 `[RUN ]` 逐步状态（stderr）。由 main() 按 `--quiet` 设置。
TRACE = True

# A4：文件内指针的显式语法 —— `见 §<主标题>[ · <子标题>]`（见 check_pointer_resolution）
POINTER_RE = re.compile(r"见\s*§\s*([^（(）)。,，;；\s·]+)(?:\s*·\s*([^（(）)。,，;；\s]+))?")


def sections_of(skill):
    """按 ## 切段 → {标题: 段文本}（标题去掉 # 与首尾空白）。"""
    out, cur, buf = {}, None, []
    for line in skill.splitlines():
        if re.match(r"^##\s", line):
            if cur:
                out[cur] = "\n".join(buf)
            cur = re.sub(r"^##\s*", "", line).strip()
            buf = [line]
        else:
            buf.append(line)
    if cur:
        out[cur] = "\n".join(buf)
    return out


def check_anchors(rep):
    skill = skill_text()
    secs = sections_of(skill)
    missing, wrong = [], []
    for a in ANCHORS:
        want = ANCHOR_SECTION.get(a, "")
        hit = [h for h in secs if want and want in h]
        if not hit:
            missing.append("%s(节缺失:%s)" % (a, want))
        elif a not in secs[hit[0]]:
            wrong.append("%s(不在节「%s」内)" % (a, hit[0]))
    problems = missing + wrong
    rep.add("A1", "硬门锚点按节存在（%d 条，按节定位）" % len(ANCHORS), FAIL, not problems,
            "问题项：%s" % "；".join(problems[:6]) if problems else "%d 条均在其应有节内" % len(ANCHORS))


def sections_by_level(skill, level=3):
    """按指定标题级别切段 → {标题(去 #): 段文本}（遇同级或更高级标题即结束）。"""
    out, cur, buf = {}, None, []
    for line in skill.splitlines():
        m = re.match(r"^(#{2,6})\s+(.*)$", line)
        if m:
            lv = len(m.group(1))
            if lv == level:
                if cur:
                    out[cur] = "\n".join(buf)
                cur = m.group(2).strip()
                buf = [line]
                continue
            if lv < level and cur:
                out[cur] = "\n".join(buf)
                cur, buf = None, []
                continue
        if cur:
            buf.append(line)
    if cur:
        out[cur] = "\n".join(buf)
    return out


def heading_occurrences(skill, levels=(2, 3, 4, 5, 6)):
    """统计**同名**标题在指定级别集合内的出现次数 → {标题: 次数}。

    用于防"重复标题诱饵"绕过 A2。
    v0.3.0（F3，`REV-20261006-021`）：由只统计 2/3 级改为 **2–6 级全覆盖** ——
    此前用**4 级**同名标题当诱饵可绕过（`dup_level4_decoy` 实测假绿）。
    """
    counts = {}
    for line in skill.splitlines():
        m = re.match(r"^(#{2,6})\s+(.*)$", line)
        if m and len(m.group(1)) in levels:
            name = m.group(2).strip()
            counts[name] = counts.get(name, 0) + 1
    return counts


def strip_comments_whole(text):
    """**整篇**剥离 HTML 注释（含跨行注释）。

    `strip_markup` 是**逐行**调用的（对单行注释有效，对**跨行**注释无效）；
    A2 在**整段**上调用 `strip_markup` 故能剥掉跨行注释 —— 两侧曾因此**双标**
    （`REV-20261006-026`）。A3 改为整篇先剥一次，使两侧对注释的处理一致。
    """
    return re.sub(r"(?s)<!--.*?-->", "", text)


def strip_markup(text):
    """剥离 **HTML 注释** 与 **代码围栏标记行**（保留围栏内的内容行）。

    v0.3.0（F4，`REV-20261006-021`）：A2 原先直接在原始文本里找必需词，
    于是"把词塞进 `<!-- -->`"就能冒充内容。现剥离 HTML 注释后再判。
    ⚠️ **刻意不剥离代码围栏内容与 `>` 引用块**：本技能的硬门等式**本身就写在围栏里**
      （如「承接等式」的 `上一组末尾空间状态 = 下一组人物空间站位`），
      剥离它们会把**合法内容**判成缺失（实测误红）。代价是：
      "把词藏进代码块/引用块"仍能冒充内容 —— 已列入文件头「已知限制」。
    """
    t = re.sub(r"(?s)<!--.*?-->", "", text)
    return "\n".join(l for l in t.splitlines() if not l.lstrip().startswith("```"))


def check_section_content(rep):
    """A2：关键小节的**内容行**必须存在，且该节标题（2–6 级）必须**唯一**。

    防三类假绿（`REV-20261006-018/019/021` 实证）：
      ① 删内容留标题（原 v3 的 A1 拦不住）；
      ② **重复标题诱饵**：清空真段体 + 追加同名段（`sections_by_level` 是 dict，后者覆盖前者）；
      ③ **把词藏进注释/代码围栏/引用块** 冒充内容。
    另加「非标题内容行数 ≥ 必需词数」，拦"整张表换成一句罗列关键词"式掏空。
    判据为**字面子串**：拦不住语义掏空与占位凑数（见文件头「已知限制」）。
    """
    skill = skill_text()
    h3 = sections_by_level(skill, 3)
    h2 = sections_by_level(skill, 2)
    occ = heading_occurrences(skill)
    problems = []
    for heading, keys in SECTION_CONTENT.items():
        total_occ = occ.get(heading, 0)
        if total_occ == 0:
            problems.append("%s(节缺失)" % heading)
            continue
        if total_occ > 1:
            problems.append("%s(标题重复 ×%d —— 疑似同名诱饵段)" % (heading, total_occ))
            continue
        sec = h3.get(heading) or h2.get(heading) or ""
        body = [l for l in strip_markup(sec).splitlines()
                if l.strip() and not l.lstrip().startswith("#")]
        absent = [k for k in keys if k not in "\n".join(body)]
        if absent:
            problems.append("%s(缺内容行:%s)" % (heading, "、".join(absent)))
        elif len(body) < len(keys):
            problems.append("%s(内容行 %d < 必需词 %d，疑似被概括掏空)" % (heading, len(body), len(keys)))
    rep.add("A2", "关键小节内容行存在（%d 节；标题唯一 + 行数下限 + 必需词）" % len(SECTION_CONTENT),
            FAIL, not problems,
            "问题项：%s" % "；".join(problems[:6]) if problems
            else "%d 个小节：标题唯一、行数达标、必需词齐全" % len(SECTION_CONTENT))


def check_budget(rep):
    p = os.path.join(ROOT, SKILL)
    size = os.path.getsize(p)
    kb = size / 1024
    # 单阈值：目标 = v9 实测（44KB），失败线 = v8 水平（52KB）—— >目标即 WARN，>失败线即 FAIL
    if size > 52 * 1024:
        rep.add("K1", "SKILL.md 体积预算", FAIL, False,
                "当前 %.1f KB 超过失败线 52KB（v8.0.0 为 54.7KB，等于退回重构前）" % kb)
    else:
        rep.add("K1", "SKILL.md 体积预算", WARN, size <= 44 * 1024,
                "当前 %.1f KB（目标 ≤44KB；v8.0.0 = 54.7KB）" % kb)


def check_canonical_enumerations(rep):
    """A3（G3'）：**规范枚举顺序** —— 当某一行**完整包含**某个硬门要素集时，其顺序必须与规范一致。

    为什么需要：审计发现「四项事实」在入口出现 **5 处**，存在**不一致风险**。
    「删到 2 处」（原 G3）经 `REV-20261006-025` 证明**可达**（用**文件内指针**），
    并**已于 v10.0.0 由用户决策 D7 执行**（见 `PLAN §1.3`；`SKILL.md` 现仅 2 处）。
    本断言是配套的"把重复变成受守护的一致性"（**WARN 级**）。

    ⚠️ **本判据经过两次收紧（过程留痕，勿当"一次写对"）**：
      · v5 首版：凡同行出现 ≥2 个键 → 必须完整且同序。被 `REV-20261006-024` 抓到
        **假红**（散文 `视觉起点与观察关系需一一对应。` 被判失败）。
      · v5 第二版：加"相邻键之间只能是分隔符"的启发式 → 被 `REV-20261006-025` 抓到
        **11 个反例**：顿号散文 / 括号 / **表格行**（`|` 被当分隔符）/ 全角逗号 → 假红；
        全角 `＋` / `→` 当分隔符 → 假绿。**该启发式已被删除**。
      · 现行版（第三版）：**不做任何分隔符猜测**，只处理"整行完整包含全部键"这一**无歧义**情形，
        且**降级为 WARN**（不再阻塞构建）—— 宁可少报，不可误报。

    判据（现行）：先把**整篇**的 HTML 注释剥掉、按行处理；若某行**包含全部**规范键，
    则要求它们**按规范顺序**出现、且**每个键只出现一次**。
    残余（如实声明）：**部分枚举**（少一个键）完全不在判据内（`A2` 只对 7 个受守护小节兜底）；
    代码围栏内的整行枚举**算内容**（与 `A2` 的取舍一致）。
    """
    skill = strip_comments_whole(skill_text())          # 整篇剥注释 → 与 A2 判据一致（修跨行注释双标）
    problems = []
    for name, keys in ENUM_GUARDS.items():
        for i, line in enumerate(skill.splitlines(), 1):
            if not all(k in line for k in keys):
                continue
            pos = [line.find(k) for k in keys]
            if pos != sorted(pos):
                problems.append("L%d %s：顺序与规范不符" % (i, name))
            elif len(set(pos)) != len(pos):
                problems.append("L%d %s：有键重复出现" % (i, name))
    rep.add("A3", "规范枚举顺序（%s；整行完整包含时校验）" % "／".join(ENUM_GUARDS), WARN,
            not problems,
            "问题项：%s" % "；".join(problems[:4]) if problems
            else "所有「整行完整包含」处均按规范顺序")


def heading_texts(skill):
    """返回文档里所有 `##`–`######` 标题的文本（去掉 # 与首尾空白）。"""
    return [m.group(1).strip() for m in re.finditer(r"(?m)^#{2,6}\s+(.*)$", skill)]


def heading_spans(skill):
    """返回按出现顺序的标题列表 `[(level, text, line_idx)]`（`##`–`######`）。"""
    out = []
    for i, line in enumerate(skill.splitlines()):
        m = re.match(r"^(#{2,6})\s+(.*)$", line)
        if m:
            out.append((len(m.group(1)), m.group(2).strip(), i))
    return out


def check_pointer_resolution(rep):
    """A4（TD-10）：**文件内指针的层级关系必须成立**。

    背景（`REV-20261006-027` W2-a）：D7 重写时我写了指针 `见 §输出格式硬门 · 镜头自然段写法` ——
    **字符串比对能过**，但那个「·」想表达的层级关系并不成立（`镜头自然段写法` 与
    `每镜四项事实` 在 `SKILL.md` 里是**同级小节**）。**引用类断言此前只看"字符串是否出现"，
    从不"实地走一遍"。**

    指针语法：`见 §<主标题>`，可带 `· <子标题>` 表示"在**主标题范围内**的某个更深层级标题"。
    （本判据匹配**任何包含该形状的文本**，因此 `参见 §X` / `详见 §X` 也会被检查 —— 这是有意的：
    它们同样是指针。）

    判据：
      · `§<主标题>` 必须能匹配到**唯一**一个标题（按"标题文本包含"匹配，容忍 emoji/装饰）；
        匹配 0 个 → 悬空引用；匹配 ≥2 个 → 歧义。
      · 带 `· <子标题>` 时，该子标题必须①级别**比主标题更深** ②出现在**主标题的范围内**
        （即主标题之后、下一个同级或更高级标题之前）。

    ⚠️ **A4 不能保证"被指向的内容真的在那里"**（语义问题）：例如 `§输出格式硬门 · 镜头自然段写法`
      在层级上**是成立的**（后者确实是前者的子节），所以原错位指针**仍会被 A4 判通过** ——
      它错的是"定义并不在 `镜头自然段写法` 这一节里"，这超出字面判据能表达的范围。
    作用域：只扫 **`SKILL.md`**。
    """
    skill = skill_text()
    spans = heading_spans(skill)
    problems = []
    for i, line in enumerate(skill.splitlines(), 1):
        for m in POINTER_RE.finditer(line):
            main, sub = m.group(1), (m.group(2) or "").strip()
            hit = [(idx, lvl, txt) for idx, (lvl, txt, _ln) in enumerate(spans) if main in txt]
            if not hit:
                problems.append("L%d 「§%s」无对应标题" % (i, main))
                continue
            if len(hit) > 1:
                problems.append("L%d 「§%s」匹配 %d 个标题（歧义）" % (i, main, len(hit)))
            if not sub:
                continue
            mi, mlvl, _mtxt = hit[0]
            end = len(spans)
            for j in range(mi + 1, len(spans)):
                if spans[j][0] <= mlvl:
                    end = j
                    break
            in_range = [t for (lvl, t, _ln) in spans[mi + 1:end] if lvl > mlvl and sub in t]
            if not in_range:
                problems.append("L%d 「§%s · %s」子标题不在主标题范围内的更深层级（疑似层级错位）"
                                % (i, main, sub))
    rep.add("A4", "文件内指针层级成立（见 §主 · 子）", FAIL, not problems,
            "问题项：%s" % "；".join(problems[:4]) if problems
            else "所有 `见 §…` 指针的主标题唯一、子标题层级成立")


def trace(cid, what):
    """G2（脚本执行可靠性）：把"执行到哪一步"打到 **stderr**（保住 stdout 契约），
    并 flush —— 中断时最后一行 `[RUN ]` 就是断点。`--quiet` 时不打印。"""
    if TRACE:
        print("[RUN ] %-9s %s" % (cid, what), file=sys.stderr, flush=True)


def main(argv=None):
    global TRACE
    if not os.path.isfile(os.path.join(ROOT, "SKILL.md")):
        print("用法/环境错误：SKILL.md 不存在于 %s" % ROOT, file=sys.stderr)
        return 2
    argv = list(sys.argv[1:] if argv is None else argv)
    TRACE = "--quiet" not in argv
    rep = Report()
    trace("V1–V4", "版本戳一致性（含 skill-card）")
    version = check_versions(rep)
    trace("M1–M4", "元数据 / 来源合规")
    check_metadata(rep)
    trace("L1", "相对路径引用（死链）")
    check_links(rep)
    trace("I1–I3", "索引与加载表接线")
    check_index(rep)
    trace("D1–D2", "逐字重复与契约区")
    check_duplication(rep)
    trace("A1", "硬门锚点按节存在")
    check_anchors(rep)
    trace("A2", "关键小节内容行")
    check_section_content(rep)
    trace("A3", "规范枚举一致性")
    check_canonical_enumerations(rep)
    trace("A4", "文件内指针层级成立")
    check_pointer_resolution(rep)
    trace("K1", "入口体积预算")
    check_budget(rep)
    trace("—", "全部检查项执行完毕")

    if "--json" in argv:
        print(json.dumps({"version": version, "fail": len(rep.fails), "warn": len(rep.warns),
                          "items": rep.items}, ensure_ascii=False, indent=2))
    else:
        quiet = "--quiet" in argv
        if not quiet:            # --quiet 的契约是"只保留 RESULT 行"（由 REV-20261006-029 D1 指出 banner 残留）
            print("== seedancer 一致性检查 v5（权威版本：%s）" % version)
        for i in rep.items:
            if i["ok"] and quiet:
                continue
            mark = "OK  " if i["ok"] else ("FAIL" if i["level"] == FAIL else "WARN")
            print("[%s] %-4s %s — %s" % (mark, i["id"], i["title"], i["detail"]))
        print("RESULT: %s (%d fail, %d warn)"
              % ("PASS" if not rep.fails else "FAIL", len(rep.fails), len(rep.warns)))
    return 0 if not rep.fails else 1


if __name__ == "__main__":
    raise SystemExit(main())
