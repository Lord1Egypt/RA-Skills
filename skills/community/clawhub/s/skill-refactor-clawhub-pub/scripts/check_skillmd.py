#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_skillmd.py — SKILL.md 机械项确定性 lint（skill-md-optimizer 配套）

零出网、零必需凭据。仅标准库 + PyYAML（缺失时自动尝试安装，装不上则 BLOCKED）。
职责：判「机械项」（H6）——frontmatter 语法/字段、name/slug 规范、描述长度、
正文行数、token 预算估算、references 路径悬空（代码举例除外）、trigger 无 NOT-for 边界、
ClawHub Natural-Language Policy 两形态探针（NL-001/002）。
模型只做「判断层」（该不该拆 references、措辞好坏），机械项交给本脚本，保证跨 Agent 可复现。

用法：
  python check_skillmd.py <SKILL.md 路径> [--platform skillhub|clawhub|claude|workbuddy|github] \
      [--token-budget 3500] [--json]

退出码契约（与 skill-publish-gate 同构，CI 友好）：
  0  PASS      无 blocker（可有 medium/low 建议项）
  2  NEEDS_FIX  仅建议项（medium/low）
  1  BLOCKED    命中 blocker（语法解析失败 / 缺 name / 预算超硬上限等）

--json 输出 schema（schema_version 1.0，CI 冻结）：
  { schema_version, verdict, exit_code, counts{blocker,medium,low},
    issues[{rule_id,severity,msg,hint}] }
"""
import argparse
import json
import os
import re
import sys

# ---------------------------------------------------------------- 基础工具

def log(level, rule_id, msg, level_label=None, hint=""):
    """统一命中记录。hint = 诊断+建议方案（人工兜底：Agent 改不动时按此指给人）。"""
    global _FINDINGS
    _FINDINGS.append({
        "rule_id": rule_id,
        "severity": level,           # "blocker" | "medium" | "low"
        "msg": msg,
        "hint": hint,               # 诊断 + 建议方案
    })
    label = level_label or {
        "blocker": "BLOCKER", "medium": "MEDIUM", "low": "LOW",
    }[level]
    print(f"[{label}] {rule_id}: {msg}", file=sys.stderr)


_FINDINGS = []


def parse_frontmatter(text):
    """分离 YAML frontmatter 与正文。返回 (fm_text, body_text)。"""
    if not text.startswith("---"):
        log("blocker", "FM-001", "文件未以 '---' 开头，无 frontmatter。")
        return "", text
    lines = text.split("\n")
    # 找闭合的 '---'
    close = None
    for i in range(1, len(lines)):
        if lines[i].strip() in ("---", "..."):
            close = i
            break
    if close is None:
        log("blocker", "FM-002", "frontmatter 缺少闭合 '---'（YAML 块未关闭）。")
        return "", text
    fm_text = "\n".join(lines[1:close])
    body = "\n".join(lines[close + 1:])
    return fm_text, body


def load_yaml(fm_text, path, platform):
    """解析 frontmatter YAML。失败即 BLOCKED（不静默通过）。

    PyYAML 缺失时不自动安装（H4 零网络契约；天禧AI 平台红旗特征禁用 subprocess），
    直接报 BLOCKER，由用户手动 `pip install pyyaml` 解决。
    """
    try:
        import yaml  # type: ignore
    except ImportError:
        log("blocker", "FM-003",
            "缺 PyYAML 且无法自动安装（本 skill 遵守零网络契约，不调用 subprocess 装包）。",
            hint="诊断：PyYAML 未安装。\n"
                 "方案：`python -m pip install pyyaml` 后重跑；"
                 "或在 CI 环境预装依赖。")
        return None
    try:
        data = yaml.safe_load(fm_text)
        if not isinstance(data, dict):
            log("blocker", "FM-004", "frontmatter 顶层不是 mapping（YAML 解析异常）。")
            return None
        return data
    except yaml.YAMLError as e:
        log("blocker", "FM-005", f"YAML 解析失败（很可能是半角冒号+空格或引号问题）：{e}")
        return None


NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
DESC_CHAR_LIMIT = 1024        # Claude 触发元数据字符上限（保守）
BODY_LINE_SOFT = 200         # 软上限（建议）
BODY_LINE_HARD = 500         # 硬上限（blocker）


def estimate_tokens(body, estimator="char"):
    """T3.2 分层估算器。

    - "char"（默认）：len(body)//4，零依赖、离线可复现（CI 友好，主路径）。
    - "tiktoken"：若宿主已装 OpenAI 官方 tiktoken 且可加载 cl100k_base，则用真
      tokenizer；缺库 / 无缓存（离线）则自动回落 char 并返回 (估算值, 实际用的算法)。
    返回 (est, used)：est 为 token 估算值，used 为实际采用的算法名（"char" 或 "tiktoken"）。
    不抛异常——估算精度降级不是合规 BLOCKED，只标注。
    """
    if estimator == "tiktoken":
        try:
            import tiktoken  # type: ignore
            enc = tiktoken.encoding_for_model("gpt-4")  # cl100k_base
            return len(enc.encode(body)), "tiktoken"
        except Exception:
            # 缺库 / 离线无缓存：回落字符法，不 BLOCKED（H4 零网络契约优先）
            return len(body) // 4, "char(fallback)"
    return len(body) // 4, "char"


def check_name(slug, name, data, platform):
    # name 规范
    if not name:
        log("blocker", "FM-101", "缺 name（YAML 必需）。",
            hint="诊断：frontmatter 无 name 键 → 宿主无法识别该 skill。\n"
                 "方案：加 `name: <小写连字符slug>`；name 须匹配 ^[a-z0-9]+(-[a-z0-9]+)*$ 且 ≤64 字符。")
        return
    if not NAME_RE.match(name):
        log("medium", "FM-102", f"name '{name}' 不符合小写连字符 slug 规范（^[a-z0-9]+(-[a-z0-9]+)*$）。",
            hint="诊断：name 含大写字母/下划线/空格。\n方案：改为小写+连字符，如 My_Skill → my-skill。")
    # slug（若存在）须等于 name
    slug_val = data.get("slug")
    if slug_val and slug_val != name:
        log("low", "FM-103", f"slug '{slug_val}' 与 name '{name}' 不一致。",
            hint="诊断：slug 与 name 分叉会导致分发/检索对不上。\n方案：让 slug 与 name 保持一致，或删掉多余字段。")
    # description 必需
    desc = data.get("description")
    if not desc:
        log("blocker", "FM-104", "缺 description（触发核心，YAML 必需）。",
            hint="诊断：无 description → 渐进式披露 L1 无触发元数据，skill 永不命中。\n"
                 "方案：补 1~3 句『做什么 + 何时用 + 何时不用』，含触发词与非触发边界（NOT-for）。")
        return
    # description 长度
    if len(str(desc)) > DESC_CHAR_LIMIT:
        log("low", "FM-105", f"description 长 {len(str(desc))} 字符 > {DESC_CHAR_LIMIT}，宿主可能截断。",
            hint="诊断：description 超出 1024 字符 → 长尾被截断，关键词丢失。\n"
                 "方案：压缩到 1024 内（保留模式+触发词+NOT-for），把冗长说明下沉到正文/references。")
    # 平台特定字段
    if platform == "clawhub":
        if not data.get("license"):
            log("medium", "PL-CL-1", "ClawHub 强制 MIT-0；缺 license 字段。",
                hint="诊断：frontmatter 无 license 键 → ClawHub 会回退默认并可能阻断上架。\n"
                     "方案：在 frontmatter 顶层加 `license: MIT-0`（若脚本有第三方依赖则按实际选 Apache-2.0/MIT）。")
        # 识别两种声明路径：顶层 requires（host-side） 或 metadata.openclaw.requires（ClawHub-native 嵌套）
        top_requires = data.get("requires")
        meta = data.get("metadata")
        nested_requires = None
        if isinstance(meta, dict):
            oc = meta.get("openclaw")
            if isinstance(oc, dict):
                nested_requires = oc.get("requires")
        requires_present = bool(top_requires or nested_requires)
        if not requires_present:
            log("low", "PL-CL-2",
                "ClawHub：若脚本读 env/调二进制/联网，需在 requires 声明（一致性红线）。",
                hint="诊断：未声明 requires（顶层或 metadata.openclaw.requires 都没有）。"
                     "若本 skill 的 scripts/ 确有读 env、调外部二进制或联网，则『声明行为』与『实际行为』不一致。\n"
                     "方案：若确需声明，按实际依赖写 `metadata.openclaw.requires.bins/env/anyBins/config`；"
                     "若全本地零依赖（如纯标准库 Python），可不写——此时本项仅为提醒，可直接忽略或留 TODO 注释说明。")
    if platform == "skillhub":
        if not data.get("license"):
            log("low", "PL-SH-1", "SkillHub：建议保留 license（GitHub 同源分发）。",
                hint="诊断：无 license 键。\n方案：建议与 GitHub 仓库 LICENSE 保持一致（本 skill 默认 MIT-0）。")


def check_body(body, data, platform, token_budget, estimator="char"):
    lines = body.count("\n") + (1 if body else 0)
    if lines > BODY_LINE_HARD:
        log("blocker", "BD-001", f"正文 {lines} 行 > 硬上限 {BODY_LINE_HARD}；请拆 references。",
            hint="诊断：正文 >500 行 → 触发后一次性灌入过多 token，挤占 5000 压缩额度。\n"
                 "方案：把细节/细则/参考样例下沉到 references/（L3 按需加载），正文只留流程+硬约束。")
    elif lines > BODY_LINE_SOFT:
        log("medium", "BD-002", f"正文 {lines} 行 > 软上限 {BODY_LINE_SOFT}（建议拆 references）。",
            hint="诊断：正文偏长（>200 行）。\n方案：考虑把可独立查阅的块拆到 references/，正文保持精简。")
    # token 预算估算（T3.2 分层：char 默认 / tiktoken 真数）
    est, used = estimate_tokens(body, estimator)
    tag = "" if used == "char" else f"（{used}）"
    if est > token_budget:
        log("blocker", "BD-003", f"正文估算 ~{est} token{tag} > 预算 {token_budget}；请下沉细则。",
            hint="诊断：正文 token 超预算 → 宿主压缩时易被截断或挤占其他 skill。\n"
                 "方案：把低频细则下沉到 references/，或调大 --token-budget 匹配真实上下文窗口。"
                 "（tag 标注实际估算算法；tiktoken 缺库/离线会自动回落 char。）")
    elif est > token_budget * 0.8:
        log("low", "BD-004", f"正文估算 ~{est} token{tag} 贴近预算 {token_budget}（80% 以上）。",
            hint="诊断：正文已接近预算 80%。\n方案：再删冗述或下沉，给压缩留 20% 余量。")
    # trigger 边界检查：description/when_to_use 是否有 NOT-for / 不适用
    desc = str(data.get("description") or "") + " " + str(data.get("when_to_use") or "")
    has_boundary = bool(re.search(r"(NOT for|不适用|不触发|不用于|do NOT use|not for)", desc, re.I))
    if not has_boundary:
        log("medium", "TR-001", "frontmatter 缺触发边界（NOT-for / 不适用）——易误触发。",
            hint="诊断：description/when_to_use 只有正向触发，无 NOT-for → 相邻 skill 易抢词。\n"
                 "方案：在 description 末尾加一句『NOT for: …（列 1~3 个最易混淆场景）』。")
    # 硬约束层检查：正文是否显式标「每轮/硬约束/HARD」
    has_hard = bool(re.search(r"(硬约束|HARD CONSTRAINT|每轮必须|must obey every)", body, re.I))
    if not has_hard:
        log("low", "ST-001", "正文未见显式「硬约束/每轮必须」层——压缩后规则易丢。",
            hint="诊断：正文没有『硬约束/每轮必须』标记层 → 压缩时规则可能被裁。\n"
                 "方案：把『每轮必须遵守』的红线集中在一个『硬约束』小节，并显式标注每轮必须。")


def check_refs(body, base_dir):
    """references/assets 相对路径悬空检测。

    T1.4 边界修正：只认「正文散文里的引用」，剥离 markdown 代码围栏（``` 块）
    ——代码块里的 `scripts/gate.py` 那类是「代码举例」，不算悬空引用，不报。
    """
    # 剥掉 ``` ... ``` 代码围栏，避免把代码里的路径举例误判为悬空引用
    def _strip_code_fences(text):
        out, in_block = [], False
        for ln in text.split("\n"):
            if ln.lstrip().startswith("```"):
                in_block = not in_block
                continue
            if not in_block:
                out.append(ln)
        return "\n".join(out)
    scanned = _strip_code_fences(body)
    pat = re.compile(r"\((?:references|assets|scripts)/[^\s\)\'\"\]\[]+")
    for m in pat.finditer(scanned):
        token = m.group(0).strip("(")
        # 去掉锚点/行号
        token = token.split("#")[0]
        p = token.split("(")[0]
        rel = p.strip("`").strip()
        if not rel:
            continue
        full = os.path.join(base_dir, rel)
        if not os.path.exists(full):
            log("medium", "RF-001", f"引用路径 '{rel}' 不存在（悬空）。",
                hint="诊断：正文散文引用了不存在的 references/assets/scripts 文件 → 渐进式披露断链。\n"
                     "方案：补建该文件，或把引用改成实际存在的路径；引用须相对 skill 根目录。"
                     "（代码块内的路径举例不受此检，故安全。）")


# ---------------------------------------------------------------- T1.2 自然语言政策机械探针

def check_language(body, data, fm_blob):
    """ClawHub Natural Language Policy 机械探针（§6.0 两形态，低/中档，不阻断）。

    形态 1（low）：frontmatter 有 `language:` 但附近无理由/选择声明。
    形态 2（medium）：正文用户可见指令锁死单语言，无 auto/zh/en 三态或语言说明。
    两者都不阻断（保持 NEEDS_FIX 档），只是给维护者「该不该补语言选择」的提示。
    """
    # 形态 1：frontmatter 显式 language: 且没有就近的 language-choice 说明
    lang_val = data.get("language")
    if lang_val:
        fm_has_just = bool(re.search(
            r"(language[-_ ]?choice|language[-_ ]?policy|三态|auto.*zh.*en|zh.*auto.*en|locale)",
            fm_blob, re.I))
        if not fm_has_just:
            log("low", "NL-001",
                f"frontmatter 有 `language: {lang_val}` 但无就近的语言选择/理由声明。",
                hint="诊断：单语言 frontmatter 标记易命中 ClawHub NL-Policy 形态 1（Low）。\n"
                     "方案：要么删掉 `language:`，要么在 frontmatter 加一句理由"
                     "（如『本 skill 默认 en，宿主可覆写』），或在正文补三态 auto/zh/en 选择。")
    # 形态 2：正文锁死单语言且无三态/语言说明。
    # 边界（合规出口，任一即豁免）：
    #   (a) frontmatter 已显式 `language:` —— 锁定了 locale（NL-001 负责补理由），
    #       此时不再重复报 NL-002，避免把「已声明语言的合规 skill」误判成锁死；
    #   (b) 正文有三态 / 语言说明 / 锁定 locale 理由（面向单一受众的显式声明）。
    fm_declared_lang = bool(lang_val)
    has_tristate = bool(re.search(
        r"(auto/zh/en|auto.*zh.*en|zh.*en.*auto|三态|language[-_ ]?choice|output language|"
        r"输出语言|user's language|宿主语言|跟随用户语言|锁定.*zh|锁定.*en|locked to|面向.{0,6}(用户|受众))",
        body, re.I))
    if not fm_declared_lang and not has_tristate:
        log("medium", "NL-002",
            "正文未见语言声明（frontmatter 无 language:、正文也无三态/locale 说明）。",
            hint="诊断：既无 frontmatter language: 也无正文语言说明 → 宿主默认锁死单语言，"
                 "易命中 ClawHub NL-Policy 形态 2（Medium）。\n"
                 "方案：在正文加一小节『语言』，声明 auto/zh/en 三态（或说明锁定某 locale 的理由）；"
                 "或在 frontmatter 加 `language: <code>` 并配理由。"
                 "若本 skill 本就只服务单一 locale，请显式写出理由，保持 NL-Policy 可解释。")


# ---------------------------------------------------------------- 主流程

def run(path, platform, token_budget, as_json, estimator="char"):
    global _FINDINGS
    _FINDINGS = []
    if not os.path.isfile(path):
        log("blocker", "IO-001", f"文件不存在或不可读：{path}")
        if as_json:
            print(json.dumps({"verdict": "BLOCKED", "issues": _FINDINGS}, ensure_ascii=False))
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    base_dir = os.path.dirname(os.path.abspath(path))
    fm_text, body = parse_frontmatter(text)
    data = load_yaml(fm_text, path, platform)

    if data is not None:
        name = data.get("name") or ""
        check_name(os.path.basename(path), name, data, platform)
        check_body(body, data, platform, token_budget, estimator)
        check_refs(body, base_dir)
        # T1.2 Natural-Language Policy 机械探针（两形态，不阻断）
        check_language(body, data, fm_text)

    # verdict 判定
    has_blocker = any(f["severity"] == "blocker" for f in _FINDINGS)
    has_adv = any(f["severity"] in ("medium", "low") for f in _FINDINGS)
    if has_blocker:
        verdict, code = "BLOCKED", 1
    elif has_adv:
        verdict, code = "NEEDS_FIX", 2
    else:
        verdict, code = "PASS", 0

    counts = {"blocker": 0, "medium": 0, "low": 0}
    for f in _FINDINGS:
        counts[f["severity"]] += 1

    if as_json:
        # T1.6 JSON schema 冻结（CI / pre-publish hook 消费）。顶层稳定字段：
        #   schema_version, verdict, exit_code, counts{blocker,medium,low},
        #   issues[] 每条固定 4 字段 {rule_id, severity, msg, hint}
        print(json.dumps({
            "schema_version": "1.0",
            "verdict": verdict,
            "exit_code": code,
            "counts": counts,
            "issues": [
                {
                    "rule_id": f["rule_id"],
                    "severity": f["severity"],
                    "msg": f["msg"],
                    "hint": f.get("hint", ""),
                }
                for f in _FINDINGS
            ],
        }, ensure_ascii=False, indent=2))
    else:
        print(f"\n=== verdict: {verdict} (exit {code}) ===")
        print(f"blocker={counts['blocker']}  medium={counts['medium']}  low={counts['low']}")
        # 人工兜底：Agent 改不动时按「诊断 + 建议方案」指给人，按严重度分层
        if _FINDINGS:
            print("\n=== 诊断 + 建议方案（人工兜底）===")
            for sev in ("blocker", "medium", "low"):
                grp = [f for f in _FINDINGS if f["severity"] == sev]
                if not grp:
                    continue
                label = {"blocker": "BLOCKER（阻断发布，必改）",
                         "medium": "MEDIUM（建议改，影响质量）",
                         "low": "LOW（可忽略/提醒项）"}[sev]
                print(f"\n-- {label} --")
                for f in grp:
                    print(f"  [{f['rule_id']}] {f['msg']}")
                    hint = (f.get("hint") or "").strip()
                    if hint:
                        for ln in hint.splitlines():
                            print(f"    {ln}" if ln else "")
            print("\n（Agent 无法自动修复时，把以上逐条交给维护者：先按『方案』处理；"
                  "BLOCKER 未清零前不得发布。）")

    sys.exit(code)


def main():
    ap = argparse.ArgumentParser(description="SKILL.md 机械项确定性 lint")
    ap.add_argument("target", help="SKILL.md 路径")
    ap.add_argument("--platform", default="skillhub",
                    choices=["skillhub", "clawhub", "claude", "workbuddy", "github"],
                    help="目标平台口径（默认 skillhub）")
    ap.add_argument("--token-budget", type=int, default=3500,
                    help="正文 token 预算（默认 3500 ≈ 官方 500 行上限；上下文更大可上调）")
    ap.add_argument("--json", action="store_true", help="stdout 仅输出 JSON")
    ap.add_argument("--estimator", default="char", choices=["char", "tiktoken"],
                    help="正文 token 估算器：char=len/4（默认，零依赖离线）；"
                         "tiktoken=OpenAI 官方真数，缺库/离线自动回落 char")
    args = ap.parse_args()
    run(args.target, args.platform, args.token_budget, args.json, args.estimator)


if __name__ == "__main__":
    main()
