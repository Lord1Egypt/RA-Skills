#!/usr/bin/env python3
"""semver_check.py -- the SemVer release-decision arithmetic core (Python 3.8+, zero deps).

This is the DECISION ENGINE of the `version-decide` skill. It turns "what version
number should this be" into a single reproducible function call: the same input must
always produce the same output. That reproducibility is the technical guarantee behind
the skill's "one unambiguous recommendation" promise.

Subcommands:
    check <version>                    validate & normalize a version, report ecosystem hints
    next <version> --level <lvl>       compute the next version at a given level
    analyze <version> --changes <spec> derive a version from a set of change specs (main entry)
    compare <a> <b>                    compare two versions by precedence
    explain <version> --changes <spec> print only the reasoning chain, not the final number

Levels:
    none    no release needed
    patch   backward-compatible fix
    minor   backward-compatible new feature / deprecation
    major   backward-incompatible (breaking) change
    stable  0.x graduates to 1.0.0 (explicit action, never derived from change type)

Language: user-facing copy (reasons / errors / level descriptions) follows --lang;
default `auto` detects LC_ALL/LC_MESSAGES/LANG and falls back to `en` (ClawHub English-default).
JSON output keys are always English (current/next/level/...); values follow --lang.
Full rules and citations: ../SKILL.md and ../references/decision-tables.md.

Output-channel contract (Q3): every user-facing result goes to stdout as pure JSON;
diagnostics (locale-fallback notes, missing-key warnings, lang=auto notices) go to
stderr only, so stdout stays machine-parseable even when a locale file is missing
or corrupted.

（中文：本文件是 version-decide 技能的「判定内核」，所有版本号均由确定性算术得出，
不依赖模型手算。）

NOTE ON ENVIRONMENT ACCESS: the only environment variables this script ever reads are
LC_ALL / LC_MESSAGES / LANG, and only inside detect_lang() to pick the output language.
It does NOT read secrets, network config, or any other environment data.
"""

from __future__ import annotations

import argparse
import io
import json
import os
import re
import sys
from typing import List, Optional, Sequence, Tuple

# --------------------------------------------------------------------------
# 国际化（零依赖；默认英文，auto 回退 en）
# --------------------------------------------------------------------------

_LOCALE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "locales")
_STR: dict = {}
# 记录当前实际生效语言，供 CLI 层提示（显式化语言检测结果，见 Q2）
_ACTIVE_LANG: str = "en"
# 缺键告警去重：同一 key 只提示一次，避免刷屏
_WARNED_KEYS: set = set()

# 内嵌英文默认串表（S1 兜底）：当 locales/en.json 与 zh.json 都不可用时仍保证可用。
# 与 locales/en.json 同源；改动 en.json 文案时请同步本表（测试断言键集合一致）。
_EN_FALLBACK: dict = {
    "MSG_CLI_DESC": "Version-decision arithmetic core: validate / bump / derive from changes / compare",
    "HELP_CHECK": "Validate and normalize a version number",
    "HELP_NEXT": "Compute the next version by level",
    "HELP_ANALYZE": "Derive the version from change descriptions",
    "HELP_EXPLAIN": "Print only the reasoning chain",
    "HELP_COMPARE": "Compare precedence",
    "HELP_LEVEL": "none|patch|minor|major|stable",
    "HELP_PRE": "alpha | beta | rc | alpha.1 ...",
    "HELP_CHANGES": "change specs, e.g. feat: add export",
    "HELP_BUILD": "Build metadata, e.g. 20261008.a1b2c3d",
    "HELP_REBASE": "Force re-bumping the target version number from the current core within a pre-release line",
    "ERR_INVALID_LEVEL": "level must be one of {0}",
    "ERR_UNKNOWN_CHANGE_TYPE": "Unrecognized change type: {0!r} (allowed: {1})",
    "ERR_BAD_PRE": "Pre-release identifier must be alpha / beta / rc or a numbered form; got {0!r}",
    "ERR_EMPTY_CHANGE": "Change description is empty",
    "ERR_NO_CHANGES": "At least one change description is required",
    "ERR_BAD_VERSION_SYNTAX": "Does not match SemVer 2.0.0 syntax. Correct form: MAJOR.MINOR.PATCH[-pre][+build]; no leading zeros in numeric segments.",
    "ERR_SKIP_PRE": "Skipping a pre-release stage is not allowed: currently {0}, cannot jump straight to {1}. Release {2} first. (alpha -> beta -> rc -> stable)",
    "REASON_NONE_NO_BUMP": "No change touches the public API; no new release needed (keep {0}).",
    "REASON_STABLE_NOT_APPLICABLE": "Already on the {0}.x stable line; the 'stable' action does not apply.",
    "REASON_STABLE_GRADUATION": "Explicit graduation: 0.x gives no compatibility guarantee; lock the API and declare the 1.0.0 contract, skipping the pre-release stage before 1.0.0.",
    "REASON_PRERELEASE_LINE": "Currently on the {0} pre-release line; core stays the same. Use --rebase to target a different version number.",
    "REASON_0X_PATCH": "0.{0}.{1}: patch does not change the leftmost non-zero digit, so dependents can auto-upgrade safely.",
    "REASON_0X_MINOR": "0.{0}.{1}: under 0.x, a minor bump IS the breaking boundary (npm ^ and cargo ^ both cap at 0.(y+1).0), so {2} lands at 0.{3}.0.",
    "REASON_PATCH": "Only internal fixes with no incompatible API change; patch bump (SemVer §6).",
    "REASON_MINOR": "Backward-compatible new feature or deprecation marker; minor bump and patch reset to zero (SemVer §7).",
    "REASON_MAJOR": "Backward-incompatible change in the public API; major bump and minor/patch reset to zero (SemVer §8).",
    "REASON_PRE_OPEN": "Opening the pre-release channel on {0}; sequence starts at 1.",
    "REASON_PRE_TO_STABLE": "Converting pre-release to stable: drop the pre-release identifier (SemVer §11.3).",
    "REASON_BUILD": "Build metadata {0} does not affect precedence (SemVer §10); it is for traceability only.",
    "REASON_PRE_ADVANCE_SAME": "Same pre-release stage {0}; sequence {1} -> {2}.",
    "REASON_PRE_ADVANCE_STAGE": "Pre-release stage advanced: {0} -> {1}; sequence reset to 1.",
    "REASON_PRE_REVERT": "Pre-release reverted: {0} -> {1} (re-opening the validation window for that stage).",
    "REASON_0X_BREAKING_NOTE": "A breaking change exists and the current version is 0.x; handled under the 0.x rule.",
    "MSG_PEP440_HINT": "Detected {0} - this is not SemVer syntax; in the Python ecosystem use PEP 440 form.",
    "MSG_GIT_V_PREFIX": "Git tags often carry a v prefix (v1.2.3); don't include the v in package-manager metadata.",
    "MSG_COMPARE_BUILD": "Build metadata does not affect comparison (SemVer §10).",
    "MSG_FORCED_BREAK": " (explicitly declared breaking)",
    "DESC_FEAT": "Adds a backward-compatible feature",
    "DESC_FIX": "Fixes erroneous behavior",
    "DESC_PERF": "Performance optimization, behavior preserved",
    "DESC_REVERT": "Reverts a non-breaking change",
    "DESC_SECURITY": "Security fix without changing the API shape",
    "DESC_DOCS": "Docs only; affects no consumer",
    "DESC_TEST": "Tests only; affects no consumer",
    "DESC_CI": "Pipeline config only",
    "DESC_CHORE": "Misc maintenance (deps, formatting, comments)",
    "DESC_STYLE": "Cosmetic formatting only",
    "DESC_BUILD": "Build-system adjustment",
    "DESC_REFACTOR": "Internal refactor; public API signature and behavior unchanged",
    "DESC_DEPRECATE": "Marks deprecation but stays usable (SemVer §7 requires minor)",
    "DESC_REVERTBREAK": "Reverts a breaking change; compatibility is broken a second time",
    "DESC_BREAKING": "Breaking change",
    # S2 精准纠错子原因键（新增）
    "ERR_FIX_EMPTY": "input is empty; a version must look like 1.2.3",
    "ERR_FIX_LEADING_ZERO": "numeric segment {0} has a leading zero; write it without the zero (e.g. {0} -> {1})",
    "ERR_FIX_SEGMENT_COUNT": "expected 3 numeric segments MAJOR.MINOR.PATCH; got {0}",
    "ERR_FIX_BAD_PRE": "pre-release part {0} is malformed (use ASCII alphanumerics/hyphens, no leading zeros)",
    "ERR_FIX_BAD_BUILD": "build part {0} is malformed (use ASCII alphanumerics/hyphens)",
    "ERR_FIX_TRAILING": "unexpected character near {0}; check for trailing '-' or '+'",
}


def _warn(msg: str) -> None:
    """诊断信息一律写 stderr，保持 stdout 为纯 JSON（机器可读约定）。"""
    try:
        sys.stderr.write(msg + "\n")
    except Exception:
        pass


def load_locale(lang: str) -> dict:
    """读取 locales/<lang>.json。

    健壮化（S1）：仅白名单语言（en/zh）进入路径拼接，杜绝路径穿越；
    文件缺失或 JSON 损坏（JSONDecodeError/ValueError）时，先尝试回退 en.json，
    连 en.json 都不可用时回退到内嵌 _EN_FALLBACK 英文默认串表，保证决策主流程
    绝不因 locale 数据损坏而崩溃。
    """
    safe = lang if lang in ("en", "zh") else "en"
    order = [safe, "en"] if safe != "en" else ["en"]
    for candidate in order:
        path = os.path.join(_LOCALE_DIR, candidate + ".json")
        try:
            with io.open(path, encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict) or not data:
                raise ValueError("locale file is empty or not a JSON object")
            if candidate != safe:
                _warn("note: locale %r unavailable/corrupt, fell back to %s" % (safe, candidate))
            return data
        except FileNotFoundError:
            continue
        except (json.JSONDecodeError, ValueError, OSError) as exc:
            _warn("note: locale file %s unreadable (%s); falling back" % (path, type(exc).__name__))
            continue
    _warn("note: no locale file loadable; using built-in English defaults")
    return dict(_EN_FALLBACK)


def set_lang(lang: str) -> None:
    global _STR, _ACTIVE_LANG
    _STR = load_locale(lang)
    _ACTIVE_LANG = lang


def _(key: str, *args, **kwargs) -> str:
    """按当前语言取文案；key 缺失时原样返回 key，并向 stderr 写一次 WARN（S1）。"""
    s = _STR.get(key)
    if s is None:
        if key not in _WARNED_KEYS:
            _WARNED_KEYS.add(key)
            _warn("warn: missing locale key %r; showing raw key" % key)
        s = key
    if args or kwargs:
        try:
            return s.format(*args, **kwargs)
        except (IndexError, KeyError, ValueError) as exc:
            _warn("warn: locale format failed for key %r (%s); returning raw string" % (key, type(exc).__name__))
            return s
    return s


def detect_lang() -> str:
    """auto mode: read ONLY the LC_ALL / LC_MESSAGES / LANG locale variables to pick a
    language. Returns "zh" if a zh* locale is set, else "en" (ClawHub English-default).
    No other environment data is read."""
    for var in ("LC_ALL", "LC_MESSAGES", "LANG"):
        v = os.environ.get(var, "")
        if v:
            code = v.split(".")[0].lower()
            if code.startswith("zh"):
                return "zh"
    return "en"


set_lang("en")  # 模块导入即默认英文，保证测试/无 CLI 场景可用


# --------------------------------------------------------------------------
# 解析
# --------------------------------------------------------------------------

_IDENT = r"(?:0|[1-9]\d*|[0-9]*[A-Za-z-][0-9A-Za-z-]*)"
_PRE_RE = re.compile(r"^v?(?P<m>0|[1-9]\d*)\.(?P<n>0|[1-9]\d*)\.(?P<p>0|[1-9]\d*)"
                     r"(?:-(?P<pre>" + _IDENT + r"(?:\." + _IDENT + r")*))?"
                     r"(?:\+(?P<build>[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$")

# PEP 440 特征片段：a/b/rc 后缀、.post、.dev、epoch 的 "!"、下划线归一化
_PEP440_HINTS = (
    (re.compile(r"^\d+!"), "PEP 440 epoch（前缀 N!）"),
    (re.compile(r"(?i)(?:^|\.)(?:a|b|rc)\d+(?:\.post|\.dev)?$"), "PEP 440 预发布后缀（a1/b2/rc1）"),
    (re.compile(r"(?i)\.post\d+"), "PEP 440 post-release（.postN）"),
    (re.compile(r"(?i)\.dev\d+"), "PEP 440 dev-release（.devN）"),
    (re.compile(r"_"), "PEP 440 归一化写法（下划线）"),
)


def classify_version_error(text: str) -> "Tuple[str, str]":
    """对一个无法解析的版本串，返回 (reason_code, detail)（S2）。

    顺序判定：空 → 段数 → 前导零 → 尾部杂字符 → 预发布/构建段格式。
    detail 是可供展示的具体片段（如带前导零的段）。
    """
    s = text.strip()
    if s == "":
        return ("empty", s)
    # 先剥掉可选的 v 前缀与 pre/build 段，只看三段核心
    core = s
    if core.startswith("v"):
        core = core[1:]
    pre_part = build_part = ""
    if "+" in core:
        core, build_part = core.split("+", 1)
    if "-" in core:
        core, pre_part = core.split("-", 1)
    segs = core.split(".")
    if len(segs) != 3:
        return ("wrong_segment_count", str(len(segs)))
    for seg in segs:
        if seg == "":
            return ("trailing", text)
        if not seg.isdigit():
            return ("bad_core", seg)
        if len(seg) > 1 and seg[0] == "0":
            return ("leading_zero", seg)
    # 核心三段合法，问题在 pre/build
    if pre_part and not re.fullmatch(r"[0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*", pre_part):
        return ("bad_pre", pre_part)
    if build_part and not re.fullmatch(r"[0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*", build_part):
        return ("bad_build", build_part)
    return ("other", s)


class BadVersion(ValueError):
    """版本号不符合 SemVer 2.0.0 语法。

    S2: 附带 reason_code 子原因标签（empty/leading_zero/wrong_segment_count/
    bad_pre/bad_build/trailing/other），供 CLI 层选择针对性纠错提示，
    而不是对所有非法输入回同一句规范条文。
    """

    def __init__(self, text: str, reason_code: str = "other", detail: str = "") -> None:
        self.input = text
        self.reason_code = reason_code
        self.detail = detail
        super().__init__(text)


class Version:
    """一个 SemVer 2.0.0 版本号。"""

    __slots__ = ("major", "minor", "patch", "pre", "build")

    def __init__(self, major: int, minor: int, patch: int,
                 pre: Tuple[object, ...] = (), build: str = "") -> None:
        self.major = major
        self.minor = minor
        self.patch = patch
        self.pre = pre
        self.build = build

    # -- 解析 -------------------------------------------------------------
    @classmethod
    def parse(cls, text: str) -> "Version":
        m = _PRE_RE.match(text.strip())
        if not m:
            code, detail = classify_version_error(text)
            # 前导零：把 "01" -> "1" 作为纠正建议给出
            if code == "leading_zero":
                fixed = detail.lstrip("0") or "0"
            else:
                fixed = ""
            raise BadVersion(text, reason_code=code,
                            detail=detail + ((" -> " + fixed) if fixed else ""))
        pre_raw = m.group("pre")
        pre: Tuple[object, ...] = ()
        if pre_raw is not None:
            parts: List[object] = []
            for chunk in pre_raw.split("."):
                parts.append(int(chunk) if chunk.isdigit() else chunk)
            pre = tuple(parts)
        return cls(int(m.group("m")), int(m.group("n")), int(m.group("p")),
                   pre, m.group("build") or "")

    # -- 序列化 -----------------------------------------------------------
    def core(self) -> str:
        return "%d.%d.%d" % (self.major, self.minor, self.patch)

    def __str__(self) -> str:
        s = self.core()
        if self.pre:
            s += "-" + ".".join(str(x) for x in self.pre)
        if self.build:
            s += "+" + self.build
        return s

    def __repr__(self) -> str:  # pragma: no cover - 调试用
        return "Version(%r)" % str(self)

    # -- 比较（SemVer 2.0.0 §11）-----------------------------------------
    def _key(self):
        # 预发布整体优先级低于同 core 的正式版：用 (0,) 与 (1,) 做哨兵比较
        return (self.major, self.minor, self.patch,
                1 if not self.pre else 0, self.pre)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Version) and self.cmp_key() == other.cmp_key()

    def __hash__(self) -> int:
        return hash(self.cmp_key())

    def cmp_key(self):
        return (self.major, self.minor, self.patch,
                1 if not self.pre else 0, self._normalized_pre())

    def _normalized_pre(self) -> Tuple:
        # 纯数字场按数值比；非数字场按 ASCII 串比；数字场优先级低于非数字场；
        # 前缀全等时，段数多的优先级更高（补 None 占位）
        out: List[Tuple[int, object]] = []
        for ident in self.pre:
            if isinstance(ident, int):
                out.append((0, ident))
            else:
                out.append((1, ident))
        while len(out) < 8:
            out.append((-1, 0))
        return tuple(out[:8])

    def __lt__(self, other: "Version") -> bool:
        return self.cmp_key() < other.cmp_key()


# --------------------------------------------------------------------------
# 级别与递增
# --------------------------------------------------------------------------

LEVEL_ORDER = {"none": 0, "patch": 1, "minor": 2, "major": 3}
LEVELS = list(LEVEL_ORDER)

# "stable" 是显式毕业动作，不由变更类型推导，故不参与 max() 比较
_VALID_LEVELS = set(LEVEL_ORDER) | {"stable"}

_LEVEL_ALIAS = {
    "fix": "patch", "bugfix": "patch", "perf": "patch", "revert": "patch",
    "security": "patch", "patch": "patch", "none": "none", "skip": "none",
    "feat": "minor", "feature": "minor", "deprecate": "minor", "minor": "minor",
    "breaking": "major", "break": "major", "major": "major",
}

PRE_STAGES = ("alpha", "beta", "rc")


def normalize_level(token: str) -> str:
    t = token.strip().lower()
    if t in _VALID_LEVELS:
        return t
    if t in _LEVEL_ALIAS:
        return _LEVEL_ALIAS[t]
    raise ValueError(_("ERR_UNKNOWN_CHANGE_TYPE", token, ", ".join(sorted(_VALID_LEVELS))))


# --------------------------------------------------------------------------
# 核心：给定当前版本与目标级别，算出下一个版本号
# --------------------------------------------------------------------------

def next_version(current: Version, level: str, pre: Optional[str] = None,
                 build: Optional[str] = None, rebase: bool = False) -> Tuple[Version, List[str]]:
    """返回 (新版本, 理由链)。level 必须是 LEVELS 或 stable 之一。

    rebase=True 时强制从当前 core 重新递增（用于预发布线内决定换目标版本号的场景）。
    """
    if level not in _VALID_LEVELS:
        raise ValueError(_("ERR_INVALID_LEVEL", ", ".join(sorted(_VALID_LEVELS))))
    reasons: List[str] = []
    m, n, p = current.major, current.minor, current.patch
    in_prerelease = bool(current.pre)

    if level == "none":
        reasons.append(_("REASON_NONE_NO_BUMP", current.core()))
        return Version(m, n, p, current.pre, current.build), reasons

    if level == "stable":
        if m != 0:
            reasons.append(_("REASON_STABLE_NOT_APPLICABLE", m))
            return Version(m, n, p, current.pre, current.build), reasons
        reasons.append(_("REASON_STABLE_GRADUATION"))
        base = Version(1, 0, 0)
    elif in_prerelease and not rebase:
        # 预发布线已在飞：core 保持不变，新变更累积进同一条预发布线。
        # SemVer 与 npm/Cargo 都允许预发布之间出现破坏性变更，这正是预发布通道的意义。
        base = Version(m, n, p)
        reasons.append(_("REASON_PRERELEASE_LINE", current.core()))
    elif m == 0:
        # ---- 0.x 特殊区：npm/cargo 把 minor 视为破坏性边界 -------------
        if level == "patch":
            base = Version(0, n, p + 1)
            reasons.append(_("REASON_0X_PATCH", n, p))
        else:  # minor / major
            base = Version(0, n + 1, 0)
            reasons.append(_("REASON_0X_MINOR", n, p, level, n + 1))
    else:
        if level == "patch":
            base = Version(m, n, p + 1)
            reasons.append(_("REASON_PATCH"))
        elif level == "minor":
            base = Version(m, n + 1, 0)
            reasons.append(_("REASON_MINOR"))
        else:
            base = Version(m + 1, 0, 0)
            reasons.append(_("REASON_MAJOR"))

    # ---- 预发布标识符处理 ----------------------------------------------
    if pre:
        pre_norm = pre.strip().lstrip("-")
        if not re.match(r"^(alpha|beta|rc)(\.\d+)?$", pre_norm):
            raise ValueError(_("ERR_BAD_PRE", pre))
        # 裸阶段名统一补 .1，保证版本号形状稳定可排序
        pre_tuple: Tuple[object, ...] = _pre_from_stage(pre_norm)

        same_core = (base.major == m and base.minor == n and base.patch == p)
        if current.pre and same_core:
            pre_tuple = _advance_pre(current.pre, pre_norm, reasons)
        else:
            reasons.append(_("REASON_PRE_OPEN", base.core()))
        new = Version(base.major, base.minor, base.patch, pre_tuple,
                      build if build is not None else current.build)
    else:
        if current.pre and base.core() == current.core() and level in ("patch", "minor"):
            reasons.append(_("REASON_PRE_TO_STABLE"))
        new = Version(base.major, base.minor, base.patch, (), build if build is not None else "")

    if new.build:
        reasons.append(_("REASON_BUILD", new.build))
    return new, reasons


def _pre_from_stage(text: str) -> Tuple[object, ...]:
    if "." in text:
        stage, num = text.split(".", 1)
        return (stage, int(num))
    return (text, 1)


def _advance_pre(current_pre: Tuple[object, ...], requested: str,
                 reasons: List[str]) -> Tuple[object, ...]:
    """在同一 core 内推进预发布阶段。"""
    want_stage = requested.split(".")[0]
    cur_stage = current_pre[0] if current_pre else ""
    cur_num = current_pre[1] if len(current_pre) > 1 and isinstance(current_pre[1], int) else 0

    if cur_stage == want_stage:
        reasons.append(_("REASON_PRE_ADVANCE_SAME", cur_stage, cur_num, cur_num + 1))
        return (want_stage, cur_num + 1)

    try:
        cur_idx = PRE_STAGES.index(cur_stage)
    except ValueError:
        cur_idx = -1
    try:
        want_idx = PRE_STAGES.index(want_stage)
    except ValueError:
        want_idx = -1

    if want_idx == cur_idx + 1:
        reasons.append(_("REASON_PRE_ADVANCE_STAGE", cur_stage, want_stage))
        return (want_stage, 1)
    if want_idx == cur_idx:
        return (want_stage, cur_num + 1)
    if want_idx > cur_idx:
        raise ValueError(
            _("ERR_SKIP_PRE", cur_stage, want_stage, PRE_STAGES[cur_idx + 1]))
    reasons.append(_("REASON_PRE_REVERT", cur_stage, want_stage))
    return (want_stage, 1)


# --------------------------------------------------------------------------
# 变更描述 → 级别
# --------------------------------------------------------------------------

# 变更类型 → (基准级别, 文案 key)。破坏性以 "break:" 前缀显式声明，压过类型默认值。
_CHANGE_RULES = {
    "feat": ("minor", "DESC_FEAT"),
    "feature": ("minor", "DESC_FEAT"),
    "fix": ("patch", "DESC_FIX"),
    "bugfix": ("patch", "DESC_FIX"),
    "perf": ("patch", "DESC_PERF"),
    "revert": ("patch", "DESC_REVERT"),
    "security": ("patch", "DESC_SECURITY"),
    "docs": ("none", "DESC_DOCS"),
    "test": ("none", "DESC_TEST"),
    "ci": ("none", "DESC_CI"),
    "chore": ("none", "DESC_CHORE"),
    "style": ("none", "DESC_STYLE"),
    "build": ("none", "DESC_BUILD"),
    "refactor": ("patch", "DESC_REFACTOR"),
    "deprecate": ("minor", "DESC_DEPRECATE"),
    "revertbreak": ("major", "DESC_REVERTBREAK"),
    "breaking": ("major", "DESC_BREAKING"),
}


def level_for_change(spec: str) -> Tuple[str, str, bool]:
    """解析单条变更描述 → (level, 说明, 是否破坏性)。

    语法： "type" | "type: 说明" | "break: 说明" | "type@break: 说明"
    """
    raw = spec.strip()
    if not raw:
        raise ValueError(_("ERR_EMPTY_CHANGE"))

    forced_break = False
    # 1) 先剥离显式破坏性标记
    m_break = re.match(r"^(?:break|breaking)\s*:\s*(.*)$", raw, re.IGNORECASE)
    if m_break:
        forced_break = True
        raw = m_break.group(1).strip()
    if "@break" in raw:
        forced_break = True
        raw = raw.replace("@break", "", 1).strip()

    # 2) 切出类型与说明。类型是冒号前的词；若它不是已知类型，
    #    则视为"未写类型"（仅在强制破坏时允许，整句作为说明）。
    kind, sep, note = raw.partition(":")
    key = kind.strip().lower()
    note = note.strip()
    if key not in _CHANGE_RULES:
        if not forced_break:
            raise ValueError(_("ERR_UNKNOWN_CHANGE_TYPE", kind.strip(), ", ".join(sorted(_CHANGE_RULES))))
        key, note = "breaking", (kind.strip() + (("：" + note) if sep and note else ""))

    level, desc = _CHANGE_RULES[key]
    if forced_break:
        return "major", (note or _(desc)) + _("MSG_FORCED_BREAK"), True
    return level, note or _(desc), False


def analyze(current: Version, specs: Sequence[str], pre: Optional[str] = None,
            build: Optional[str] = None, rebase: bool = False) -> dict:
    """核心入口：变更集合 → 唯一版本号建议。"""
    if not specs:
        raise ValueError(_("ERR_NO_CHANGES"))
    items = [level_for_change(s) for s in specs]
    level = max((lv for lv, _, _ in items), key=lambda x: LEVEL_ORDER[x])
    has_break = any(br for _, _, br in items)
    driver = [d for lv, d, _ in items if lv == level]

    if has_break and current.major == 0 and level != "major":
        reasons_extra = _("REASON_0X_BREAKING_NOTE")
    else:
        reasons_extra = ""

    new, reasons = next_version(current, level, pre=pre, build=build, rebase=rebase)
    report = {
        "current": str(current),
        "level": level,
        "has_breaking": has_break,
        "next": str(new),
        "changes": [
            {"spec": s, "level": lv, "breaking": br, "why": d}
            for s, (lv, d, br) in zip(specs, items)
        ],
        "drivers": driver,
        "reasons": reasons,
    }
    if reasons_extra:
        report["reasons"].append(reasons_extra)
    return report


# --------------------------------------------------------------------------
# 生态兼容性提示
# --------------------------------------------------------------------------

def ecosystem_notes(text: str) -> List[str]:
    notes: List[str] = []
    for rx, label in _PEP440_HINTS:
        if rx.search(text.strip()):
            notes.append(_("MSG_PEP440_HINT", label))
    if text.strip().startswith("v"):
        notes.append(_("MSG_GIT_V_PREFIX"))
    return notes


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def _print(obj: dict) -> None:
    print(json.dumps(obj, ensure_ascii=False, indent=2))


# S2: reason_code → 针对性纠错 locale 键。detail 形如 "01" 或 "01 -> 1"。
_VERSION_FIX_HINTS = {
    "empty": "ERR_FIX_EMPTY",
    "leading_zero": "ERR_FIX_LEADING_ZERO",
    "wrong_segment_count": "ERR_FIX_SEGMENT_COUNT",
    "bad_pre": "ERR_FIX_BAD_PRE",
    "bad_build": "ERR_FIX_BAD_BUILD",
    "trailing": "ERR_FIX_TRAILING",
    "bad_core": "ERR_FIX_TRAILING",
    "other": "ERR_FIX_TRAILING",
}


def _version_fix_hint(exc: "BadVersion", hint_key: Optional[str]) -> str:
    """把子原因标签 + detail 渲染成一句针对性纠错提示。"""
    if not hint_key:
        return ""
    detail = exc.detail or exc.input
    # 前导零：detail 已含 "01 -> 1"，拆成 (段, 纠正) 两个格式化参数
    if hint_key == "ERR_FIX_LEADING_ZERO" and " -> " in detail:
        seg, fixed = detail.split(" -> ", 1)
        return _(hint_key, seg, fixed)
    return _(hint_key, detail)


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        prog="semver_check",
        description=_("MSG_CLI_DESC"))
    # 公共参数：语言（默认 auto，回退 en）
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--lang", default="auto", choices=["auto", "en", "zh"],
                        help="输出语言：auto（探测环境，回退 en）| en | zh")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_check = sub.add_parser("check", parents=[common], help=_("HELP_CHECK"))
    p_check.add_argument("version")

    p_next = sub.add_parser("next", parents=[common], help=_("HELP_NEXT"))
    p_next.add_argument("version")
    p_next.add_argument("--level", required=True, help=_("HELP_LEVEL"))
    p_next.add_argument("--pre", help=_("HELP_PRE"))
    p_next.add_argument("--build", help=_("HELP_BUILD"))
    p_next.add_argument("--rebase", action="store_true",
                        help=_("HELP_REBASE"))

    p_an = sub.add_parser("analyze", parents=[common], help=_("HELP_ANALYZE"))
    p_an.add_argument("version")
    p_an.add_argument("--changes", nargs="+", required=True, metavar="SPEC", help=_("HELP_CHANGES"))
    p_an.add_argument("--pre")
    p_an.add_argument("--build")
    p_an.add_argument("--rebase", action="store_true", help=_("HELP_REBASE"))

    p_exp = sub.add_parser("explain", parents=[common], help=_("HELP_EXPLAIN"))
    p_exp.add_argument("version")
    p_exp.add_argument("--changes", nargs="+", required=True, metavar="SPEC", help=_("HELP_CHANGES"))
    p_exp.add_argument("--pre")
    p_exp.add_argument("--build")
    p_exp.add_argument("--rebase", action="store_true", help=_("HELP_REBASE"))

    p_cmp = sub.add_parser("compare", parents=[common], help=_("HELP_COMPARE"))
    p_cmp.add_argument("a")
    p_cmp.add_argument("b")

    args = ap.parse_args(argv)
    # 语言解析（在真正产出任何文案前完成）
    resolved = detect_lang() if args.lang == "auto" else args.lang
    set_lang(resolved)
    # Q2：auto 命中回退（未检出 zh）时，向 stderr 显式告知实际语言，不污染 stdout JSON
    if args.lang == "auto" and resolved == "en":
        _warn("note: lang=auto -> en (no zh* locale detected; override with --lang zh)")
    try:
        if args.cmd == "compare":
            a, b = Version.parse(args.a), Version.parse(args.b)
            _print({"a": str(a), "b": str(b),
                    "result": "a < b" if a < b else ("a > b" if b < a else "a == b"),
                    "note": _("MSG_COMPARE_BUILD")})
            return 0

        cur = Version.parse(args.version)
        notes = ecosystem_notes(args.version)

        if args.cmd == "check":
            _print({"valid": True, "normalized": str(cur),
                    "is_prerelease": bool(cur.pre), "build": cur.build or None,
                    "ecosystem_notes": notes})
            return 0

        if args.cmd == "next":
            lvl = normalize_level(args.level)
            new, reasons = next_version(cur, lvl, pre=args.pre, build=args.build,
                                       rebase=args.rebase)
            _print({"current": str(cur), "level": lvl, "next": str(new),
                    "reasons": reasons, "ecosystem_notes": notes})
            return 0

        report = analyze(cur, args.changes, pre=args.pre, build=args.build,
                         rebase=args.rebase)
        report["ecosystem_notes"] = notes
        if args.cmd == "explain":
            report.pop("next", None)
        _print(report)
        return 0
    except BadVersion as exc:
        # S2：按子原因标签选针对性纠错提示（而非一句通用规范条文）
        hint_key = _VERSION_FIX_HINTS.get(exc.reason_code)
        hint = _version_fix_hint(exc, hint_key)
        _print({"valid": False, "input": str(exc),
                "error": _("ERR_BAD_VERSION_SYNTAX"),
                "fix_hint": hint,
                "reason_code": exc.reason_code,
                "ecosystem_notes": ecosystem_notes(str(exc))})
        return 2
    except ValueError as exc:
        _print({"valid": False, "error": str(exc)})
        return 2


if __name__ == "__main__":
    sys.exit(main())
