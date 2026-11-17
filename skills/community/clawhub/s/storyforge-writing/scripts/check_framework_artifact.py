#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_framework_artifact.py — storyforge framework 产物级校验器（零依赖，v4）

规则来源：
  - references/field-registry.md（AI 可写字段 / 类型 / 枚举）
  - references/schema-tables.md（§2 全部表索引 = 表名单源；§4 全表字段清单 = 数据模型字段）
  - contracts/S-data-envelope.md（语料结构 / 旁车 / 规范化哈希 / context-manifest）
  - contracts/A-longform.md（§8 编号与引用 / §9.1 后验原语形状）

用法：
  python scripts/check_framework_artifact.py [--strict] [--json] [--sources-root DIR] <framework.json> [...]
  python scripts/check_framework_artifact.py --list-codes

  --strict        「兼容期 WARN」升级为 ERROR（新产物建议一律加 --strict）
  --sources-root  旁车 sources 中 md/path/file 的解析根目录；给出时对**像文件的引用**逐个验存
                   （史书卷目 / 作者口述 / 推导说明 / 通配简写等非文件凭证只报 NOTE，见 `_is_checkable_path`）
  --json          机读输出（每条问题带稳定 code）
  --list-codes    列出全部问题码及其默认级别（供文档/断言核对）

退出码：0 = 全部 PASS；1 = 至少一个 FAIL；2 = 用法/环境错误

版本轨迹：
  v1（2026-10-07）6 类契约违规；v3 表名改 §2 单源。
  v4（v0.5.0）：
    · 问题以 (level, code, path, message) **结构化产出**（不再靠关键词反推 code）；
    · **字段闭集**：记录内 `provenance`/`evidenceGrade` → ERROR（SIDECAR_FIELD_IN_RECORD）；
      未知字段 → WARN（--strict 下 ERROR）；
    · **证据复算**：按 `sf-c14n-v1` 复算 contentHash、核对 recordCount、旁车表 ↔ 主文件表双向对齐；
    · `continuityHandoff` 校验移出逐字段循环（v3 每多一个字段就重复报一遍）；新增 `planReconciliation` 校验；
    · `context-manifest.json` 必须是合法 JSON 对象，`entries[]` 按 §3.2 校验三态；
    · 旁车按 `<stem>.provenance.json` 配对（不再把目录里所有旁车套到每个产物上）；
    · **修假红**：`--sources-root` 只对「像文件」的引用验存（`_is_checkable_path`），
      非文件凭证（史书卷目 / 作者口述 / 上游代码位置 / 通配简写）降为 NOTE `EVIDENCE_SOURCE_NONPATH`
      —— 实测历史产物被误报 40 + 12 条 ERROR，全部为假红。
"""
import json
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)
from sf_hash import CANONICALIZATION, records_by_table, records_hash  # noqa: E402

ERROR, WARN, NOTE = "ERROR", "WARN", "NOTE"
GRADES = ("OBSERVED", "INFERRED", "UNKNOWN")
SIDECAR_ONLY_KEYS = ("provenance", "evidenceGrade")
SYSTEM_FIELDS = {"id", "projectId", "createdAt", "updatedAt"}
MANIFEST_STATES = ("read", "missing", "omitted", "partial-selection")
REVIEW_STATUS = ("pending", "confirmed-constraint", "applied-outline", "dismissed")

# code → (默认级别, 说明)。「兼容期」项默认 WARN，--strict 升为 ERROR。
CODES = {
    "TOP_LEVEL_VERSION": (ERROR, "顶层含 version（冒充备份包）"),
    "TOP_LEVEL_BLOCKS": (ERROR, "顶层 blocks 不是 list"),
    "NOT_OBJECT": (ERROR, "记录/块不是对象"),
    "TABLE_UNKNOWN": (ERROR, "表名不在 schema-tables.md §2"),
    "TABLE_NOT_WRITABLE": (WARN, "表在 schema 中但无 FIELD_REGISTRY 登记（只读/系统表，AI 不应写）【兼容期】"),
    "MISSING_ID": (ERROR, "记录缺整数 id"),
    "MISSING_PROJECT_ID": (ERROR, "记录缺整数 projectId"),
    "SIDECAR_FIELD_IN_RECORD": (ERROR, "provenance/evidenceGrade 混入记录（只能在旁车）"),
    "FIELD_UNKNOWN": (WARN, "字段不在该表的数据模型（§4）中 —— 精确键集下会被拒收【兼容期】"),
    "FIELD_NOT_WRITABLE": (WARN, "字段在数据模型中但未登记为 AI 可写（运行时 unknown_write_field）【兼容期】"),
    "ENUM_VIOLATION": (ERROR, "枚举值不在闭集"),
    "FK_TYPE": (ERROR, "外键不是数字"),
    "FK_DANGLING": (ERROR, "外键悬空且未在 unresolvedRefs 登记"),
    "FK_DANGLING_DECLARED": (WARN, "外键悬空但已在 unresolvedRefs 登记"),
    "FIELD_NULL_OR_EMPTY": (WARN, "字段为 null/空"),
    "CHAPTER_ID_NOT_INT": (ERROR, "chapters.id 不是整数（代号只能进 title/文件名）"),
    "CHAPTER_ORDER": (ERROR, "chapters.order 非整数或重复"),
    "HANDOFF_SHAPE": (ERROR, "continuityHandoff 形状不符 A-longform §9.1"),
    "RECONCILIATION_SHAPE": (ERROR, "planReconciliation 形状不符 A-longform §9.1"),
    "RECONCILIATION_UNCONFIRMED": (ERROR, "planReconciliation 已非 pending 却无 reviewedAt（未确认 ≠ 已确认）"),
    "SIDECAR_MISSING": (ERROR, "context-manifest.json 缺失"),
    "MANIFEST_INVALID": (ERROR, "context-manifest.json 不是合法 JSON 对象或 entries 形状错误"),
    "MANIFEST_LEGACY": (WARN, "context-manifest.json 无 entries[]（旧形态，见 S-data-envelope §3.2）【兼容期】"),
    "PROVENANCE_MISSING": (WARN, "没有可配对的 *.provenance.json"),
    "PROVENANCE_UNPAIRED": (WARN, "无 <stem>.provenance.json，回退到目录内全部旁车"),
    "SIDECAR_UNREADABLE": (ERROR, "旁车不可读/非法 JSON"),
    "SIDECAR_KEY": (WARN, "旁车键名非规范（契约：blockProvenance）"),
    "SIDECAR_SHAPE": (ERROR, "blockProvenance 不是 list / 项不是对象 / 缺 5 字段"),
    "SIDECAR_TABLE_ORPHAN": (ERROR, "旁车登记了主文件中不存在的表"),
    "SIDECAR_TABLE_UNCOVERED": (WARN, "主文件的表在旁车中无 provenance 条目【兼容期】"),
    "EVIDENCE_GRADE": (ERROR, "evidenceGrade 不在闭集"),
    "EVIDENCE_NO_HASH": (ERROR, "contentHash 为空"),
    "EVIDENCE_HASH_FORM": (WARN, "contentHash 非 sha256: 形态且未标注占位算法"),
    "EVIDENCE_HASH_MISMATCH": (ERROR, "已声明 sf-c14n-v1，但复算哈希不一致"),
    "EVIDENCE_HASH_UNVERIFIABLE": (WARN, "未声明 hashCanonicalization，且按 sf-c14n-v1 复算不一致 —— 无法复算【兼容期】"),
    "EVIDENCE_COUNT_MISMATCH": (ERROR, "recordCount 与主文件实际记录数不一致"),
    "EVIDENCE_SILENT_ABSENT": (ERROR, "有记录但既无 sources 也无 notes（静默缺失）"),
    "EVIDENCE_ABSENT_DECLARED": (NOTE, "有记录、sources 为空，但 notes 已显式声明原因"),
    "EVIDENCE_NO_SOURCES": (ERROR, "sources 不是 list"),
    "EVIDENCE_NO_MARKER": (ERROR, "sources 项缺来源标记（md/path/file/key）"),
    "EVIDENCE_SOURCE_GRADE": (WARN, "sources 项等级缺省或非闭集"),
    "EVIDENCE_NESTED": (ERROR, "sources[].sources 不是字符串数组"),
    "EVIDENCE_SOURCE_MISSING": (ERROR, "--sources-root 下找不到 sources 指向的**文件**"),
    "EVIDENCE_SOURCE_NONPATH": (NOTE, "sources 项是非文件凭证（卷目/口述/推导/通配），不作文件验存"),
}
STRICT_UPGRADE = {c for c, (lv, d) in CODES.items() if "【兼容期】" in d}


class Issues:
    def __init__(self, strict):
        self.strict, self.items = strict, []

    def add(self, code, path, msg):
        level = CODES[code][0]
        if self.strict and code in STRICT_UPGRADE:
            level = ERROR
        self.items.append({"level": level, "code": code, "field_path": path, "message": msg})

    def count(self, level):
        return sum(1 for i in self.items if i["level"] == level)


# ---------------------------------------------------------------- 参考文件解析
def _read(p):
    with open(p, encoding="utf-8") as fh:
        return fh.read()


def parse_registry():
    """field-registry.md §1 → {table: {field: {type, enum}}}。"""
    p = os.path.join(SKILL_ROOT, "references", "field-registry.md")
    if not os.path.isfile(p):
        return {}
    reg = _read(p)
    sec1 = re.split(r"^## 2\.", reg, flags=re.M)[0]
    spec = {}
    for s in re.split(r"\n### ", sec1):
        m = re.match(r"`([A-Za-z0-9_]+)`", s)
        if not m:
            continue
        fields = {}
        for line in s.split("\n"):
            mm = re.match(r"\|\s*`([A-Za-z0-9_]+)`\s*\|\s*`([a-z]+)`\s*\|([^|]*)\|", line)
            if mm:
                f, ty, vals = mm.group(1), mm.group(2), mm.group(3).strip()
                ev = [v.strip("` ") for v in vals.split("\u00b7")] if vals and vals != "\u2014" else []
                fields[f] = {"type": ty, "enum": ev}
        spec[m.group(1)] = fields
    return spec


def _strip_noise(s):
    s = re.sub(r"```.*?```", "", s, flags=re.S)
    return re.sub(r"<!--.*?-->", "", s, flags=re.S)


def _section(text, num_pat, keyword):
    cands = [m for m in re.finditer(r"^##[ \t\u3000]*" + num_pat + r"[ \t\u3000]*[.、．][^\n]*$", text, re.M)
             if keyword in m.group(0)]
    if len(cands) != 1:
        return None, None, len(cands)
    head = cands[0]
    rest = text[head.end():]
    nxt = re.search(r"^##[ \t\u3000]", rest, re.M)
    return head.group(0), (rest[:nxt.start()] if nxt else rest), 1


def parse_schema_tables():
    """返回 (§2 表名集合, §2 自述张数, §4 {table: 字段集合})。§2 必须唯一命中（防伪造同名节旁路）。"""
    p = os.path.join(SKILL_ROOT, "references", "schema-tables.md")
    if not os.path.isfile(p):
        return set(), None, {}
    raw = _read(p)
    head, sec2, n = _section(_strip_noise(raw), r"[2２]", "全部表索引")
    if head is None:
        print("错误：schema-tables.md「§2 全部表索引」命中 %d 个（应为 1）" % n, file=sys.stderr)
        return set(), None, {}
    names = set(re.findall(r"^\|\s*`([A-Za-z0-9_]+)`\s*\|\s*`[^`]+`\s*\|\s*$", sec2, re.M))
    mtxt = re.search(r"（\**(\d+)\s*张", head)
    # §4 字段清单在 ```text 围栏内，故用**未剥离**的原文定位（标题仍须唯一）
    model = {}
    h4, sec4, _ = _section(re.sub(r"<!--.*?-->", "", raw, flags=re.S), r"[4４]", "全表字段清单")
    if sec4:
        for chunk in re.split(r"^###[ \t]+", sec4, flags=re.M)[1:]:
            mt = re.match(r"`([A-Za-z0-9_]+)`", chunk)
            if not mt:
                continue
            fields = set(re.findall(r"`([A-Za-z0-9_]+)\??`:", chunk))
            if fields:                      # 4 张交叉类型表未解析出字段 → 不纳入闭集判定
                model[mt.group(1)] = fields
    return names, (int(mtxt.group(1)) if mtxt else None), model


def _is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


# 旁车 sources 除了「项目内文件」还承载**非文件凭证**：
#   · 史书卷目        晉書/卷049、三國志/卷19、世說新語/德行
#   · 作者口述/裁决    作者确认（杜小文 2026-10-06）、作者裁决(四幕为主)
#   · 上游代码位置     src/lib/types/world-ownership.ts:46 (Work)
#   · 通配/范围简写    knowledge/*.md、scripts/episode-01..04.md
#   · 推导/说明        故事逻辑推导、p2/p3
# 这些按「本目录下的文件」去判存在性必然假红（v0.5.0 实测：长铗传 40 条 / 广陵散 12 条全部误报）。
# 因此只有**明确长得像文件**的引用才做存在性检查；其余降为 NOTE，既不误报也不静默丢弃。
_SOURCE_NONPATH_CHARS = ("*", "?", "[", "]", "..", " ", "\t", "（", "）", "(", ")", "、", "，", "；")
_SOURCE_PATH_EXTS = (".md", ".json", ".ts", ".tsx", ".js", ".jsx", ".yml", ".yaml", ".txt", ".csv", ".html")


def _is_checkable_path(s):
    """True = 该 sources 引用确实指向 --sources-root 下的一个文件。"""
    if not isinstance(s, str):
        return False
    t = s.strip()
    if not t or any(c in t for c in _SOURCE_NONPATH_CHARS):
        return False
    if ":" in t:                       # file.ts:46 / URL / 卷目行号
        return False
    return t.lower().endswith(_SOURCE_PATH_EXTS)


# ---------------------------------------------------------------- 旁车
def pick_sidecars(path, iss):
    dirn = os.path.dirname(os.path.abspath(path))
    stem = os.path.splitext(os.path.basename(path))[0]
    paired = os.path.join(dirn, stem + ".provenance.json")
    if os.path.isfile(paired):
        return [paired]
    others = sorted(os.path.join(dirn, f) for f in os.listdir(dirn) if f.endswith(".provenance.json"))
    if others:
        iss.add("PROVENANCE_UNPAIRED", "", "未找到 %s.provenance.json，回退使用：%s"
                % (stem, ", ".join(os.path.basename(o) for o in others)))
    else:
        iss.add("PROVENANCE_MISSING", "", "provenance sidecar missing")
    return others


def check_manifest(path, iss):
    mp = os.path.join(os.path.dirname(os.path.abspath(path)), "context-manifest.json")
    if not os.path.exists(mp):
        iss.add("SIDECAR_MISSING", "", "context-manifest.json missing")
        return
    try:
        m = json.loads(_read(mp))
    except (ValueError, OSError) as e:
        iss.add("MANIFEST_INVALID", "context-manifest", "不是合法 JSON：%s" % e)
        return
    if not isinstance(m, dict):
        iss.add("MANIFEST_INVALID", "context-manifest", "顶层必须是对象，得到 %s" % type(m).__name__)
        return
    entries = m.get("entries")
    if entries is None:
        iss.add("MANIFEST_LEGACY", "context-manifest", "无 entries[]（读了什么/遗漏什么不可机读）")
        return
    if not isinstance(entries, list):
        iss.add("MANIFEST_INVALID", "context-manifest.entries", "entries 必须是 list")
        return
    for i, e in enumerate(entries):
        p = "context-manifest.entries[%d]" % i
        if not isinstance(e, dict) or not e.get("source"):
            iss.add("MANIFEST_INVALID", p, "每项必须是含 source 的对象")
            continue
        st = e.get("state")
        if st not in MANIFEST_STATES:
            iss.add("MANIFEST_INVALID", p, "state=%r 不在闭集 %s" % (st, "/".join(MANIFEST_STATES)))
        elif st != "read" and not str(e.get("reason") or "").strip():
            iss.add("MANIFEST_INVALID", p, "state=%s 必须给出 reason（裁剪必须留证据）" % st)


def check_sidecars(path, blocks_by_table, iss, sources_root):
    unresolved = set()
    seen_tables = set()
    for sp in pick_sidecars(path, iss):
        name = os.path.basename(sp)
        try:
            pr = json.loads(_read(sp))
        except (ValueError, OSError) as e:
            iss.add("SIDECAR_UNREADABLE", name, "%s unreadable: %s" % (name, e))
            continue
        if not isinstance(pr, dict):
            iss.add("SIDECAR_UNREADABLE", name, "顶层必须是对象")
            continue
        for u in (pr.get("unresolvedRefs") or []):
            if isinstance(u, dict) and {"table", "field", "value", "reason"} <= set(u) \
                    and str(u.get("reason") or "").strip():
                unresolved.add((u["table"], u["field"], json.dumps(u["value"])))
        canon = pr.get("hashCanonicalization")
        bp = pr.get("blockProvenance")
        if bp is None:
            if "blocks" in pr:
                iss.add("SIDECAR_KEY", name, "sidecar uses non-canonical key blocks (contract: `blockProvenance`)")
                bp = pr.get("blocks")          # 仍按同形状校验内容（只报偏离，不改历史产物）
            else:
                iss.add("SIDECAR_KEY", name, "no `blockProvenance` key (sidecar uses: %s)"
                        % ",".join(list(pr.keys())[:6]))
                continue
        if not isinstance(bp, list):
            iss.add("SIDECAR_SHAPE", name, "blockProvenance must be a list, got %s" % type(bp).__name__)
            continue
        need = {"table", "recordCount", "contentHash", "evidenceGrade", "sources"}
        for i, it in enumerate(bp):
            p = "blockProvenance[%d]" % i
            if not isinstance(it, dict):
                iss.add("SIDECAR_SHAPE", p, "不是对象")
                continue
            miss = sorted(need - set(it))
            if miss:
                iss.add("SIDECAR_SHAPE", p, "missing %s" % miss)
                continue
            t = it["table"]
            seen_tables.add(t)
            if t not in blocks_by_table:
                iss.add("SIDECAR_TABLE_ORPHAN", p, "table=%r 不在主文件 blocks[] 中" % t)
                actual = None
            else:
                actual = blocks_by_table[t]
                if it["recordCount"] != len(actual):
                    iss.add("EVIDENCE_COUNT_MISMATCH", p, "recordCount=%r ≠ 主文件实际 %d 条"
                            % (it["recordCount"], len(actual)))
            if it["evidenceGrade"] not in GRADES:
                iss.add("EVIDENCE_GRADE", p, "evidenceGrade=%r 不在闭集 {OBSERVED,INFERRED,UNKNOWN}"
                        % (it["evidenceGrade"],))
            ch = it["contentHash"]
            if not isinstance(ch, str) or not ch.strip():
                iss.add("EVIDENCE_NO_HASH", p, "contentHash 为空（证据不可核验）")
            elif not ch.startswith("sha256:"):
                if "fnv1a64" not in ch:
                    iss.add("EVIDENCE_HASH_FORM", p, "contentHash 非 sha256 形态且未标注占位算法：%r" % ch[:24])
            elif actual is not None:
                calc = records_hash(actual)
                if calc != ch:
                    if canon == CANONICALIZATION:
                        iss.add("EVIDENCE_HASH_MISMATCH", p, "声明 %s，复算=%s… ≠ 登记=%s…"
                                % (canon, calc[:19], ch[:19]))
                    else:
                        iss.add("EVIDENCE_HASH_UNVERIFIABLE", p, "未声明 hashCanonicalization；按 %s 复算=%s… ≠ 登记=%s…"
                                % (CANONICALIZATION, calc[:19], ch[:19]))
            srcs, rc = it["sources"], it["recordCount"]
            if not isinstance(srcs, list):
                iss.add("EVIDENCE_NO_SOURCES", p, "sources 必须是 list")
                continue
            if rc and not srcs:
                if str(it.get("notes") or "").strip():
                    iss.add("EVIDENCE_ABSENT_DECLARED", p, "recordCount=%s 但 sources 为空（notes 已声明原因）" % rc)
                else:
                    iss.add("EVIDENCE_SILENT_ABSENT", p, "recordCount=%s 但既无 sources 也无 notes —— 静默缺失" % rc)
                continue
            for j, s in enumerate(srcs):
                sp_ = "%s.sources[%d]" % (p, j)
                if not isinstance(s, dict):
                    iss.add("EVIDENCE_NO_MARKER", sp_, "不是对象")
                    continue
                files = [s[k] for k in ("md", "path", "file") if s.get(k)]
                nested = s.get("sources")
                if not (files or (s.get("key") and isinstance(nested, list) and nested)):
                    iss.add("EVIDENCE_NO_MARKER", sp_, "缺来源标记（md/path/file/key 任一）")
                if nested is not None:
                    if not (isinstance(nested, list) and all(isinstance(x, str) for x in nested)):
                        iss.add("EVIDENCE_NESTED", sp_, "sources[].sources 必须是字符串数组")
                    else:
                        files += nested
                if (s.get("grade") or s.get("evidence")) not in GRADES:
                    iss.add("EVIDENCE_SOURCE_GRADE", sp_, "等级缺省或非闭集：%r" % (s.get("grade") or s.get("evidence"),))
                if sources_root:
                    for f in files:
                        if not isinstance(f, str):
                            continue
                        if not _is_checkable_path(f):
                            iss.add("EVIDENCE_SOURCE_NONPATH", sp_, "非文件凭证，未作 exist 校验：%s" % f)
                        elif not os.path.exists(os.path.join(sources_root, f)):
                            iss.add("EVIDENCE_SOURCE_MISSING", sp_, "%s 不存在于 --sources-root" % f)
    for t in blocks_by_table:
        if seen_tables and t not in seen_tables:
            iss.add("SIDECAR_TABLE_UNCOVERED", t, "表 %s 在旁车中无 provenance 条目" % t)
    return unresolved


# ---------------------------------------------------------------- 后验原语
def _quotes_ok(q):
    return isinstance(q, list) and q and all(
        isinstance(x, dict) and x.get("quote") and _is_int(x.get("startOffset")) and _is_int(x.get("endOffset"))
        for x in q)


def check_handoff(h, p, iss):
    if not isinstance(h, dict):
        iss.add("HANDOFF_SHAPE", p, "必须是对象")
        return
    need = ("finalScene", "stateChanges", "knowledgeChanges", "commitments", "openLoops",
            "evidenceQuotes", "sourceTextHash")
    miss = [k for k in need if k not in h]
    if miss:
        iss.add("HANDOFF_SHAPE", p, "缺必需字段 %s（A-longform.md §9.1）" % miss)
    fs = h.get("finalScene")
    if "finalScene" in h and not (isinstance(fs, dict) and isinstance(fs.get("activeCharacters"), list)):
        iss.add("HANDOFF_SHAPE", p + ".finalScene", "必须含 activeCharacters: string[]")
    for k in ("stateChanges", "knowledgeChanges", "commitments", "openLoops"):
        if k in h and not isinstance(h[k], list):
            iss.add("HANDOFF_SHAPE", p + "." + k, "必须是数组")
    if not _quotes_ok(h.get("evidenceQuotes")):
        iss.add("HANDOFF_SHAPE", p + ".evidenceQuotes", "必须是非空数组，每项含 quote + startOffset + endOffset")


def check_reconciliation(r, p, iss):
    if not isinstance(r, dict):
        iss.add("RECONCILIATION_SHAPE", p, "必须是对象")
        return
    for k in ("completedGoals", "unfinishedGoals", "deviations", "newConstraints", "nextChapterImpacts"):
        if k not in r:
            iss.add("RECONCILIATION_SHAPE", p, "缺必需对账类 %s" % k)
            continue
        items = r[k]
        if not isinstance(items, list):
            iss.add("RECONCILIATION_SHAPE", p + "." + k, "必须是数组")
            continue
        for i, it in enumerate(items):
            if not (isinstance(it, dict) and str(it.get("text") or "").strip() and _quotes_ok(it.get("evidenceQuotes"))):
                iss.add("RECONCILIATION_SHAPE", "%s.%s[%d]" % (p, k, i), "Item 须含 text + 非空带偏移 evidenceQuotes")
    st = r.get("reviewStatus")
    if st not in REVIEW_STATUS:
        iss.add("RECONCILIATION_SHAPE", p + ".reviewStatus", "reviewStatus=%r 不在闭集 %s" % (st, "/".join(REVIEW_STATUS)))
    elif st != "pending" and not r.get("reviewedAt"):
        iss.add("RECONCILIATION_UNCONFIRMED", p + ".reviewStatus", "reviewStatus=%s 但无 reviewedAt —— 语料生成时须起于 pending" % st)


# ---------------------------------------------------------------- 主体
def check(path, spec, schema_tables, model, strict=False, sources_root=None):
    iss = Issues(strict)
    try:
        d = json.loads(_read(path))
    except (ValueError, OSError) as e:
        iss.add("TOP_LEVEL_BLOCKS", "", "JSON parse error: %s" % e)
        return iss, 0
    if not isinstance(d, dict):
        iss.add("TOP_LEVEL_BLOCKS", "", "顶层必须是对象")
        return iss, 0
    if "version" in d:
        iss.add("TOP_LEVEL_VERSION", "version", "top-level `version` must NOT be present (would mimic a backup package)")
    blocks = d.get("blocks")
    if not isinstance(blocks, list):
        iss.add("TOP_LEVEL_BLOCKS", "blocks", "top-level `blocks` must be a list, got %s" % type(blocks).__name__)
        blocks = []
    by_table = records_by_table(blocks)

    check_manifest(path, iss)
    unresolved = check_sidecars(path, by_table, iss, sources_root)

    all_ids = {r.get("id") for recs in by_table.values() for r in recs if isinstance(r, dict)}
    orders = []
    for t, recs in by_table.items():
        if t not in schema_tables:
            iss.add("TABLE_UNKNOWN", str(t), "table not in schema-tables.md index: %s" % t)
        elif t not in spec:
            iss.add("TABLE_NOT_WRITABLE", t, "table has no FIELD_REGISTRY entry: %s（只读/系统表，AI 不应写）" % t)
        fs, allowed = spec.get(t, {}), model.get(t)
        for i, r in enumerate(recs):
            p = "%s[%d]" % (t, i)
            if not isinstance(r, dict):
                iss.add("NOT_OBJECT", p, "%s not an object" % p)
                continue
            if t == "chapters" and isinstance(r.get("id"), str):
                iss.add("CHAPTER_ID_NOT_INT", p + ".id", "`id` 是字符串 %r —— 章节必须用整数 id，代号只能进 title/文件名" % r["id"])
            elif not _is_int(r.get("id")):
                iss.add("MISSING_ID", p + ".id", "missing numeric `id`")
            if not _is_int(r.get("projectId")):
                iss.add("MISSING_PROJECT_ID", p + ".projectId", "missing numeric `projectId`")
            for k in r:
                if k in SIDECAR_ONLY_KEYS:
                    iss.add("SIDECAR_FIELD_IN_RECORD", "%s.%s" % (p, k), "`%s` 只能放旁车（S-data-envelope §3）" % k)
                elif k in SYSTEM_FIELDS or k in fs:
                    continue
                elif allowed is not None and k not in allowed:
                    iss.add("FIELD_UNKNOWN", "%s.%s" % (p, k), "字段 `%s` 不在 %s 的数据模型中（schema-tables §4）" % (k, t))
                elif t in spec:
                    iss.add("FIELD_NOT_WRITABLE", "%s.%s" % (p, k), "字段 `%s` 未登记为 %s 的 AI 可写字段" % (k, t))
            for f, fsp in fs.items():
                if f not in r:
                    continue
                v = r[f]
                if v is None or v == []:
                    iss.add("FIELD_NULL_OR_EMPTY", "%s.%s" % (p, f), "null/empty (unresolved)")
                    continue
                if fsp["type"] == "enum" and v not in fsp["enum"]:
                    iss.add("ENUM_VIOLATION", "%s.%s" % (p, f), "enum violation: %r not in %s" % (v, fsp["enum"]))
                if fsp["type"] == "number" and f.endswith("Id"):
                    if not isinstance(v, (int, float)) or isinstance(v, bool):
                        iss.add("FK_TYPE", "%s.%s" % (p, f), "must be number, got %s" % type(v).__name__)
                    elif _is_int(v) and v not in all_ids:
                        if (t, f, json.dumps(v)) in unresolved:
                            iss.add("FK_DANGLING_DECLARED", "%s.%s" % (p, f), "=%s dangling（unresolvedRefs 已登记）" % v)
                        else:
                            iss.add("FK_DANGLING", "%s.%s" % (p, f), "=%s dangling 且未登记 —— 须置 null 并在旁车 unresolvedRefs 留痕（A-longform §8）" % v)
            if t == "chapters":
                if r.get("continuityHandoff") is not None:
                    check_handoff(r["continuityHandoff"], p + ".continuityHandoff", iss)
                if r.get("planReconciliation") is not None:
                    check_reconciliation(r["planReconciliation"], p + ".planReconciliation", iss)
                orders.append((p, r.get("order")))
    seen, dup = set(), set()
    for p, o in orders:
        if o is None:
            continue
        if not _is_int(o):
            iss.add("CHAPTER_ORDER", p + ".order", "`order` 必须是整数，得到 %r" % (o,))
        elif o in seen:
            dup.add(o)
        else:
            seen.add(o)
    if dup:
        iss.add("CHAPTER_ORDER", "chapters", "`order` 重复：%s（章序必须唯一）" % sorted(dup)[:5])
    return iss, len(by_table)


def main():
    args, strict, want_json, sources_root = [], False, False, None
    it = iter(sys.argv[1:])
    for a in it:
        if a == "--strict":
            strict = True
        elif a == "--json":
            want_json = True
        elif a == "--sources-root":
            sources_root = next(it, None)
        elif a == "--list-codes":
            for c, (lv, dsc) in CODES.items():
                print("%-28s %-5s %s" % (c, lv, dsc))
            return 0
        else:
            args.append(a)
    if not args:
        print("用法：python check_framework_artifact.py [--strict] [--json] [--sources-root DIR] <framework.json> [...]",
              file=sys.stderr)
        return 2
    spec = parse_registry()
    schema_tables, declared, model = parse_schema_tables()
    if not spec or not schema_tables or declared is None or declared != len(schema_tables):
        print("ERROR: 参考文件不可信（registry=%d 表；schema §2 自述 %s / 实际 %d）—— 校验未完成"
              % (len(spec), declared, len(schema_tables)), file=sys.stderr)
        return 2
    missing = [p for p in args if not os.path.isfile(p)]
    for mp in missing:
        print("ERROR: artifact not found: %s" % mp, file=sys.stderr)
    if missing:
        print("ABORTED: %d path(s) not found — 校验未完成" % len(missing))
        return 2
    if sources_root and not os.path.isdir(sources_root):
        print("ERROR: --sources-root 不是目录：%s" % sources_root, file=sys.stderr)
        return 2

    results, total = [], 0
    for p in args:
        iss, ntab = check(p, spec, schema_tables, model, strict, sources_root)
        ne = iss.count(ERROR)
        total += ne
        results.append({"path": p, "status": "PASS" if ne == 0 else "FAIL", "tables": ntab,
                        "errors": ne, "warnings": iss.count(WARN), "issues": iss.items})
    if want_json:
        print(json.dumps({"schema": "storyforge.artifact-check.v2", "strict": strict,
                          "hashCanonicalization": CANONICALIZATION,
                          "registryTables": len(spec), "schemaIndexTables": len(schema_tables),
                          "modelTables": len(model), "artifacts": results}, ensure_ascii=False, indent=1))
        return 0 if total == 0 else 1
    print("registry tables: %d | schema index tables: %d | model tables: %d | strict=%s"
          % (len(spec), len(schema_tables), len(model), strict))
    for r in results:
        print("=" * 72)
        print("ARTIFACT:", r["path"])
        print("STATUS: %s | tables: %s | errors: %d | warnings: %d" % (r["status"], r["tables"], r["errors"], r["warnings"]))
        shown = {ERROR: 0, WARN: 0, NOTE: 0}
        for i in r["issues"]:
            lim = 30 if i["level"] == ERROR else 10
            shown[i["level"]] += 1
            if shown[i["level"]] <= lim:
                print("   %-5s %-26s %s %s" % (i["level"], i["code"], i["field_path"], i["message"]))
        for lv, lim in ((ERROR, 30), (WARN, 10), (NOTE, 10)):
            if shown[lv] > lim:
                print("   ... +%d more %s（用 --json 查看全部）" % (shown[lv] - lim, lv))
    print("=" * 72)
    print("TOTAL ERRORS:", total)
    return 0 if total == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
