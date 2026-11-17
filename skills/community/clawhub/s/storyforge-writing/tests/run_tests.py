#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""run_tests.py — 校验器的正例 + 反例回归（零依赖）。

以 `examples/minimal/` 为**金样例**（必须 --strict 0 error），再逐条注入一种违规，
断言校验器给出**期望的 code 与级别**。每条规则至少一个反例 —— 「断言先对真实参照物验证」。

用法：python tests/run_tests.py     退出码 0 = 全部通过
"""
import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GOLD = os.path.join(ROOT, "examples", "minimal")
CHECK = os.path.join(ROOT, "scripts", "check_framework_artifact.py")
MAKE = os.path.join(ROOT, "scripts", "make_sidecar.py")
FW, SIDE, MAN = "storyforge-framework.json", "storyforge-framework.provenance.json", "context-manifest.json"
PY = sys.executable


def load(d, f):
    with open(os.path.join(d, f), encoding="utf-8") as fh:
        return json.load(fh)


def dump(d, f, obj):
    with open(os.path.join(d, f), "w", encoding="utf-8") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=1)


def run(d, *flags):
    p = subprocess.run([PY, CHECK, "--json", *flags, os.path.join(d, FW)], capture_output=True, text=True)
    try:
        out = json.loads(p.stdout)
        issues = out["artifacts"][0]["issues"]
    except Exception:  # noqa: BLE001
        issues = []
    return p.returncode, issues


def resign(d):
    """改了主文件后重新生成旁车哈希（保留 sources），模拟「作者按流程刷新旁车」。"""
    subprocess.run([PY, MAKE, os.path.join(d, FW), "--write"], capture_output=True, check=True)


def chapters(fw):
    return next(b for b in fw["blocks"] if b["table"] == "chapters")["records"]


def chars(fw):
    return next(b for b in fw["blocks"] if b["table"] == "characters")["records"]


CASES = []


def case(name, code, level="ERROR", flags=(), resign_after=True, exact=None):
    def deco(fn):
        CASES.append((name, fn, code, level, tuple(flags), resign_after, exact))
        return fn
    return deco


@case("记录内混入 provenance", "SIDECAR_FIELD_IN_RECORD")
def _(d):
    fw = load(d, FW); chars(fw)[0]["provenance"] = "p1.md"; dump(d, FW, fw)


@case("记录内混入 evidenceGrade", "SIDECAR_FIELD_IN_RECORD")
def _(d):
    fw = load(d, FW); chars(fw)[0]["evidenceGrade"] = "OBSERVED"; dump(d, FW, fw)


@case("未知字段（默认 WARN）", "FIELD_UNKNOWN", "WARN")
def _(d):
    fw = load(d, FW); chars(fw)[0]["totallyMadeUp"] = 1; dump(d, FW, fw)


@case("未知字段（--strict 升 ERROR）", "FIELD_UNKNOWN", "ERROR", flags=("--strict",))
def _(d):
    fw = load(d, FW); chars(fw)[0]["totallyMadeUp"] = 1; dump(d, FW, fw)


@case("枚举写中文长描述", "ENUM_VIOLATION")
def _(d):
    fw = load(d, FW); chars(fw)[0]["roleWeight"] = "主角·核心"; dump(d, FW, fw)


@case("改了记录但没刷新旁车（声明 sf-c14n-v1）", "EVIDENCE_HASH_MISMATCH", resign_after=False)
def _(d):
    fw = load(d, FW); chars(fw)[0]["name"] = "林照（改）"; dump(d, FW, fw)


@case("伪造哈希且未声明规范化（兼容期 WARN）", "EVIDENCE_HASH_UNVERIFIABLE", "WARN", resign_after=False)
def _(d):
    s = load(d, SIDE); s.pop("hashCanonicalization"); s["blockProvenance"][0]["contentHash"] = "sha256:deadbeef"; dump(d, SIDE, s)


@case("recordCount 与实际不符", "EVIDENCE_COUNT_MISMATCH", resign_after=False)
def _(d):
    s = load(d, SIDE); s["blockProvenance"][0]["recordCount"] = 999; dump(d, SIDE, s)


@case("旁车登记了不存在的表", "SIDECAR_TABLE_ORPHAN", resign_after=False)
def _(d):
    s = load(d, SIDE); x = copy.deepcopy(s["blockProvenance"][0]); x["table"] = "foreshadows"
    s["blockProvenance"].append(x); dump(d, SIDE, s)


@case("主文件的表在旁车中无条目（--strict）", "SIDECAR_TABLE_UNCOVERED", flags=("--strict",), resign_after=False)
def _(d):
    s = load(d, SIDE); s["blockProvenance"] = s["blockProvenance"][:2]; dump(d, SIDE, s)


@case("有记录但既无 sources 也无 notes", "EVIDENCE_SILENT_ABSENT", resign_after=False)
def _(d):
    s = load(d, SIDE); s["blockProvenance"][0]["sources"] = []; s["blockProvenance"][0].pop("notes", None); dump(d, SIDE, s)


@case("evidenceGrade 非闭集", "EVIDENCE_GRADE", resign_after=False)
def _(d):
    s = load(d, SIDE); s["blockProvenance"][0]["evidenceGrade"] = "PROBABLY"; dump(d, SIDE, s)


@case("--sources-root 下找不到来源文件", "EVIDENCE_SOURCE_MISSING", flags=("--sources-root", "<D>"), resign_after=False)
def _(d):
    s = load(d, SIDE); s["blockProvenance"][0]["sources"][0]["md"] = "settings/ghost.md"; dump(d, SIDE, s)


@case("来源非文件凭证（卷目/口述/代码位置/通配）不得误报缺失", "EVIDENCE_SOURCE_NONPATH", "NOTE",
      flags=("--sources-root", "<D>"), resign_after=False, exact=5)
def _(d):
    # 回归 v0.5.0 假红：这 5 类都不是 --sources-root 下的文件，旧逻辑一律报 EVIDENCE_SOURCE_MISSING(ERROR)。
    # rc 必须为 0 —— 即「一条 ERROR 都没有」，这正是本用例的断言点。
    s = load(d, SIDE)
    s["blockProvenance"][0]["sources"] = [
        {"md": "晉書/卷049", "grade": "OBSERVED"},
        {"md": "作者确认（杜小文 2026-10-06）", "grade": "OBSERVED"},
        {"md": "src/lib/types/world-ownership.ts:46 (Work)", "grade": "OBSERVED"},
        {"md": "knowledge/*.md", "grade": "OBSERVED"},
        {"md": "scripts/episode-01..04.md", "grade": "OBSERVED"},
    ]
    dump(d, SIDE, s)


@case("形如文件的引用仍必须验存（不许因修假红而放过）", "EVIDENCE_SOURCE_MISSING",
      flags=("--sources-root", "<D>"), resign_after=False, exact=1)
def _(d):
    # 与上一条配对：修假红不得把「真缺文件」也一并跳过。
    s = load(d, SIDE)
    s["blockProvenance"][0]["sources"] = [
        {"md": "晉書/卷049", "grade": "OBSERVED"},          # 非文件 → 跳过
        {"md": "settings/really-absent.md", "grade": "OBSERVED"},   # 像文件 → 必须报缺失
    ]
    dump(d, SIDE, s)


@case("旁车用历史键名 blocks", "SIDECAR_KEY", "WARN", resign_after=False)
def _(d):
    s = load(d, SIDE); s["blocks"] = s.pop("blockProvenance"); dump(d, SIDE, s)


@case("章节 id 用字符串代号", "CHAPTER_ID_NOT_INT")
def _(d):
    fw = load(d, FW); chapters(fw)[0]["id"] = "ep30"; dump(d, FW, fw)


@case("章节 order 重复", "CHAPTER_ORDER")
def _(d):
    fw = load(d, FW); c = copy.deepcopy(chapters(fw)[0]); c["id"] = 302
    c.pop("continuityHandoff"); c.pop("planReconciliation"); chapters(fw).append(c); dump(d, FW, fw)


@case("外键悬空且未登记", "FK_DANGLING")
def _(d):
    fw = load(d, FW); fw["blocks"][1]["records"][0]["toCharacterId"] = 999; dump(d, FW, fw)


@case("外键悬空但已登记 unresolvedRefs", "FK_DANGLING_DECLARED", "WARN")
def _(d):
    fw = load(d, FW); fw["blocks"][1]["records"][0]["toCharacterId"] = 999; dump(d, FW, fw)
    s = load(d, SIDE); s["unresolvedRefs"] = [{"table": "characterRelations", "field": "toCharacterId",
                                              "value": 999, "reason": "该角色尚未生成"}]; dump(d, SIDE, s)


@case("continuityHandoff 缺字段（只报一次，回归 v3 重复报错）", "HANDOFF_SHAPE", exact=2)
def _(d):
    fw = load(d, FW); h = chapters(fw)[0]["continuityHandoff"]; h.pop("openLoops"); h["evidenceQuotes"] = []
    dump(d, FW, fw)


@case("planReconciliation 未确认就标 confirmed", "RECONCILIATION_UNCONFIRMED")
def _(d):
    fw = load(d, FW); chapters(fw)[0]["planReconciliation"]["reviewStatus"] = "confirmed-constraint"; dump(d, FW, fw)


@case("planReconciliation 对账项缺证据", "RECONCILIATION_SHAPE")
def _(d):
    fw = load(d, FW); chapters(fw)[0]["planReconciliation"]["completedGoals"][0]["evidenceQuotes"] = []; dump(d, FW, fw)


@case("顶层带 version", "TOP_LEVEL_VERSION")
def _(d):
    fw = load(d, FW); fw["version"] = 14; dump(d, FW, fw)


@case("未知表名", "TABLE_UNKNOWN")
def _(d):
    fw = load(d, FW); fw["blocks"].append({"table": "madeUpTable", "records": [{"id": 9, "projectId": 1}]}); dump(d, FW, fw)


@case("只读表被写入", "TABLE_NOT_WRITABLE", "WARN")
def _(d):
    fw = load(d, FW); fw["blocks"].append({"table": "temporalFacts", "records": [{"id": 9, "projectId": 1}]}); dump(d, FW, fw)
    s = load(d, SIDE); s["blockProvenance"].append({"table": "temporalFacts", "recordCount": 1, "contentHash": "",
                                                   "evidenceGrade": "UNKNOWN", "sources": [], "notes": "测试"}); dump(d, SIDE, s)


@case("context-manifest 缺失", "SIDECAR_MISSING", resign_after=False)
def _(d):
    os.remove(os.path.join(d, MAN))


@case("context-manifest 非法 JSON", "MANIFEST_INVALID", resign_after=False)
def _(d):
    with open(os.path.join(d, MAN), "w") as fh:
        fh.write("{not json")


@case("裁剪项无 reason", "MANIFEST_INVALID", resign_after=False)
def _(d):
    m = load(d, MAN); m["entries"][1].pop("reason"); dump(d, MAN, m)


@case("manifest 旧形态（--strict）", "MANIFEST_LEGACY", flags=("--strict",), resign_after=False)
def _(d):
    dump(d, MAN, {"read": ["settings/premise.md"]})


def main():
    fails = 0
    tmp = tempfile.mkdtemp(prefix="sf-tests-")
    try:
        # 0) 金样例必须 --strict 通过
        g = os.path.join(tmp, "gold"); shutil.copytree(GOLD, g)
        rc, iss = run(g, "--strict", "--sources-root", g)
        errs = [i for i in iss if i["level"] in ("ERROR", "WARN")]
        ok = rc == 0 and not errs
        print("[%s] 金样例 --strict 零 ERROR/WARN" % ("PASS" if ok else "FAIL"), "" if ok else errs)
        fails += not ok
        # 1) make_sidecar 幂等且保留 sources
        before = load(g, SIDE); resign(g); after = load(g, SIDE)
        ok = [x["sources"] for x in before["blockProvenance"]] == [x["sources"] for x in after["blockProvenance"]] \
            and [x["contentHash"] for x in before["blockProvenance"]] == [x["contentHash"] for x in after["blockProvenance"]]
        print("[%s] make_sidecar 幂等且保留 sources" % ("PASS" if ok else "FAIL")); fails += not ok
        # 2) 反例
        for n, (name, fn, code, level, flags, rs, exact) in enumerate(CASES):
            d = os.path.join(tmp, "c%02d" % n); shutil.copytree(GOLD, d)
            fn(d)
            if rs:
                resign(d)
            fl = tuple(d if f == "<D>" else f for f in flags)
            rc, iss = run(d, *fl)
            hits = [i for i in iss if i["code"] == code and i["level"] == level]
            want_rc = 1 if level == "ERROR" else 0
            ok = bool(hits) and rc == want_rc and (exact is None or len([i for i in iss if i["code"] == code]) == exact)
            print("[%s] %s → %s/%s（rc=%d）" % ("PASS" if ok else "FAIL", name, code, level, rc))
            if not ok:
                print("       实得：", [(i["level"], i["code"]) for i in iss])
            fails += not ok
        # 3) 技能包自检
        p = subprocess.run([PY, os.path.join(ROOT, "scripts", "check_consistency.py"), "--quiet"],
                           capture_output=True, text=True)
        ok = p.returncode == 0
        print("[%s] check_consistency.py" % ("PASS" if ok else "FAIL"))
        if not ok:
            print(p.stdout[-2000:])
        fails += not ok
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    total = len(CASES) + 3
    print("RESULT: %d/%d passed" % (total - fails, total))
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
