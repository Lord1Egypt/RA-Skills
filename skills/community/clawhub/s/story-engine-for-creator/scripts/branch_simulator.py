"""剧情多分支推演（Branch Simulator）。

设计前提（实测确立，不是推测）：
  1) 主引擎 `UltimateCausalNovelEngine` 是单时间线单实例设计，`simulate_chapter` 只做单线。
  2) `copy.deepcopy(engine)` 可完整隔离分支状态（traits / chapters / causal_graph 均无共享引用）。
  3) 因此本模块完全位于主引擎之外：不改 `Story Engine for Creator.py` 一行，
     只做「快照 → 派生 → 独立推演 → 指标对比 → 选线」。

已知前置缺陷（本模块以开关规避，不掩盖）：
  - 模块级函数 `auto_register_characters` 会把普通名词误注册为角色（实测可注册出「成本」）。
    分支越多，角色表分叉越严重。`strict_characters=True` 时在推演上下文内临时屏蔽该函数，
    并在报告中如实标注「本次推演关闭了自动角色注册」。
  - `GlobalState.version` 从不递增（实测推进一章后仍为 0），故不依赖它做溯源，
    改用章节节点语义文本的 SHA1 指纹。

结构依赖的防呆：
  本模块的判定依赖 `audit_text` 的返回结构。若主引擎改了结构，直接取键会静默拿到 None
  并判成 False，看起来像「分支没通过」。故 `validate_audit_shape` 在取数前逐层校验，
  不通过即抛 `AuditShapeError`，由 `Branch.metrics` 转成显式失败而非静默红。

判定立场：不存在跨分支的唯一最优解。本模块输出帕累托前沿与排序建议，
排序规则明写、可复核，最终选线权归作者。
"""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
import sys
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

# 技能包适配：包内引擎文件名为 story_engine.py（仓库模板名为
# "Story Engine for Creator.py"，两者内容一致）。也可用 SE_ENGINE_PATH 覆盖。
_ENGINE_FILE = Path(__file__).with_name("story_engine.py")
_ENGINE_MODULE_NAME = "story_engine_creator"

ENGINE: Any = None


def load_engine_module(path: Optional[Path] = None):
    """加载主引擎模块（文件名含空格，不能直接 import）。"""
    global ENGINE
    if ENGINE is not None:
        return ENGINE
    if path:
        target = Path(path)
    else:
        env_path = os.environ.get("SE_ENGINE_PATH")
        target = Path(env_path) if env_path else _ENGINE_FILE
    if not target.exists():
        raise FileNotFoundError(f"找不到主引擎文件：{target}")
    if _ENGINE_MODULE_NAME in sys.modules:
        ENGINE = sys.modules[_ENGINE_MODULE_NAME]
        return ENGINE
    spec = importlib.util.spec_from_file_location(_ENGINE_MODULE_NAME, target)
    module = importlib.util.module_from_spec(spec)
    sys.modules[_ENGINE_MODULE_NAME] = module
    spec.loader.exec_module(module)
    ENGINE = module
    return ENGINE


@contextmanager
def strict_character_registry(enabled: bool = True):
    """推演上下文内屏蔽自动角色注册。

    只在本上下文内替换模块级函数，退出即还原；主引擎源码不改。
    目的是避免「成本」「绝第三」这类非人名进入角色表，污染分支对比。
    """
    m = load_engine_module()
    original = m.auto_register_characters
    if not enabled:
        yield False
        return
    m.auto_register_characters = lambda state, nodes: None
    try:
        yield True
    finally:
        m.auto_register_characters = original


@dataclass
class Branch:
    """一条推演分支：独立引擎 + 独立章节 + 独立审计结果。"""

    key: str
    label: str
    outline: str
    engine: Any = None
    chapter: Any = None
    text: str = ""
    audit: Optional[Dict[str, Any]] = None
    parent_snapshot: Dict[str, Any] = field(default_factory=dict)
    error: str = ""

    def metrics(self, baseline_characters: List[str]) -> Dict[str, Any]:
        """把审计结果压成可横向比较的量。判定式逐条复用引擎自身的口径，不自创。"""
        if self.error:
            return {"ok": False, "error": self.error}

        audit = self.audit if isinstance(self.audit, dict) else {}
        # 先校验结构，再取数：结构不符必须显式报错，不允许静默判 False。
        try:
            validate_audit_shape(audit)
        except AuditShapeError as exc:
            return {"ok": False, "error": f"审计结构异常：{exc}"}

        ledger = ((audit.get("foreshadow") or {}).get("ledger")) or {}
        faces = _audit_faces(self.engine, audit)
        drift = sorted(
            set(self.engine.global_state.characters) - set(baseline_characters)
        ) if self.engine is not None else []

        nodes = 0
        if self.chapter is not None:
            nodes = sum(len(line.nodes) for line in self.chapter.causal_lines)

        return {
            "ok": True,
            "all_passed": bool(audit.get("all_passed", False)),
            "faces": faces,
            "failed_faces": [k for k, v in faces.items() if not v],
            "unrecovered": len(ledger.get("unrecovered_topics") or []),
            "unrecovered_topics": ledger.get("unrecovered_topics") or [],
            "foreshadow_set": ledger.get("set_count", 0),
            "foreshadow_pay": ledger.get("pay_count", 0),
            "character_drift": drift,
            "drift_count": len(drift),
            "nodes": nodes,
            "chars": len(self.text or ""),
        }


class AuditShapeError(ValueError):
    """审计报告结构与预期不符。

    存在意义：`_audit_faces` 依赖 audit_text 的返回结构。若主引擎改了结构，
    直接 `.get()` 会静默拿到 None 并判 False，看起来像"分支没通过"，
    实际是"读错了字段"。这类静默误判比崩溃危险，故一律显式抛出。
    """


_REQUIRED_AUDIT_KEYS = (
    "presentation",
    "causal",
    "logical",
    "spacetime",
    "foreshadow",
    "all_passed",
)


def validate_audit_shape(audit: Any) -> bool:
    """校验 audit_text 返回结构。不通过即抛 AuditShapeError，附具体缺失位置。"""
    if not isinstance(audit, dict):
        raise AuditShapeError(f"报告根节点应为 dict，实为 {type(audit).__name__}")

    missing = [k for k in _REQUIRED_AUDIT_KEYS if k not in audit]
    if missing:
        raise AuditShapeError(f"缺少顶层字段 {missing}（主引擎返回结构可能已变更）")

    if not isinstance(audit["presentation"], dict):
        raise AuditShapeError(
            f"presentation 应为 dict，实为 {type(audit['presentation']).__name__}"
        )

    causal = audit["causal"]
    if causal is not None:
        if not isinstance(causal, dict):
            raise AuditShapeError(f"causal 应为 dict 或 None，实为 {type(causal).__name__}")
        if "collapse_verdict" not in causal:
            raise AuditShapeError("causal 缺少 collapse_verdict")
        reconstruction = causal.get("reconstruction")
        if not isinstance(reconstruction, dict):
            raise AuditShapeError("causal.reconstruction 缺失或不是 dict")
        if "converged" not in reconstruction:
            raise AuditShapeError("causal.reconstruction 缺少 converged")

    logical = audit["logical"]
    if logical is not None:
        if not isinstance(logical, dict):
            raise AuditShapeError(f"logical 应为 dict 或 None，实为 {type(logical).__name__}")
        if "overall_passed" not in logical:
            raise AuditShapeError("logical 缺少 overall_passed")

    spacetime = audit["spacetime"]
    if spacetime is not None:
        if not isinstance(spacetime, dict):
            raise AuditShapeError(f"spacetime 应为 dict 或 None，实为 {type(spacetime).__name__}")
        if "passed" not in spacetime:
            raise AuditShapeError("spacetime 缺少 passed")

    foreshadow = audit["foreshadow"]
    if not isinstance(foreshadow, dict):
        raise AuditShapeError(
            f"foreshadow 应为 dict，实为 {type(foreshadow).__name__}"
        )
    ledger = foreshadow.get("ledger")
    if not isinstance(ledger, dict):
        raise AuditShapeError("foreshadow.ledger 缺失或不是 dict")
    for key in ("all_closed", "unrecovered_topics", "set_count", "pay_count"):
        if key not in ledger:
            raise AuditShapeError(f"foreshadow.ledger 缺少 {key}")

    return True


def _audit_faces(engine: Any, audit: Dict[str, Any]) -> Dict[str, bool]:
    """五个审计面的判定，口径与 `audit_text` 内部完全一致（见主引擎 2258-2267 行）。

    不可自创判据：presentation 必须交给 presentation_auditor，
    causal 需同时满足 collapse_verdict == STABLE 与 reconstruction.converged。
    """
    presentation = audit.get("presentation") or {}
    causal = audit.get("causal")
    logical = audit.get("logical")
    spacetime = audit.get("spacetime")
    ledger = ((audit.get("foreshadow") or {}).get("ledger")) or {}

    try:
        pres_passed = bool(engine.presentation_auditor.all_passed({"presentation": presentation}))
    except Exception:
        pres_passed = False
    try:
        causal_passed = causal is None or (
            causal.get("collapse_verdict") == "STABLE"
            and bool((causal.get("reconstruction") or {}).get("converged"))
        )
    except Exception:
        causal_passed = False
    logical_passed = logical is None or bool(logical.get("overall_passed"))
    spacetime_passed = spacetime is None or bool(spacetime.get("passed"))
    ledger_passed = bool(ledger.get("all_closed", True))

    return {
        "presentation": pres_passed,
        "causal": causal_passed,
        "logical": logical_passed,
        "spacetime": spacetime_passed,
        "foreshadow": ledger_passed,
    }


FACE_LABELS = {
    "presentation": "叙",
    "causal": "因",
    "logical": "逻",
    "spacetime": "时",
    "foreshadow": "伏",
}

FACE_NAMES = {
    "presentation": "人称/视角",
    "causal": "因果链",
    "logical": "逻辑",
    "spacetime": "时空",
    "foreshadow": "伏笔未回收",
}


def _display_width(text: str) -> int:
    """中文/全角按 2 列计算，否则 f-string 定宽对齐必然错位。"""
    import unicodedata

    return sum(
        2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1 for ch in str(text)
    )


def _pad(text: Any, width: int, align: str = "left") -> str:
    text = str(text)
    gap = max(0, width - _display_width(text))
    return (" " * gap + text) if align == "right" else (text + " " * gap)


class BranchSimulator:
    """在既有引擎之外做分叉：快照 → 派生 → 独立推演 → 对比。

    用法：
        sim = BranchSimulator(engine)
        branches = sim.fork([
            ("妥协线", "林夏接受第三方评审 -> 项目延期两周 -> 成本回到预算内"),
            ("对抗线", "林夏拒绝第三方评审 -> 坚持自研上线 -> 预算超支"),
        ])
        print(sim.table(branches))
        new_engine = sim.pick(branches, "妥协线")
    """

    def __init__(
        self,
        base_engine: Any,
        strict_characters: bool = True,
        title_prefix: str = "分支",
    ):
        self.base = base_engine
        self.strict_characters = strict_characters
        self.title_prefix = title_prefix
        self.baseline_characters = sorted(base_engine.global_state.characters)
        self.snapshot = self._snapshot(base_engine)

    # ---------------- 快照 ----------------

    @staticmethod
    def _snapshot(engine: Any) -> Dict[str, Any]:
        """分叉点指纹：章节数 + 全部节点「前提⇒结论」文本的 SHA1。

        GlobalState.version 恒为 0，不能用作溯源。
        指纹不能用 node_id：node_id 是 uuid4，每次运行都变，无法跨会话比对。
        故对节点语义文本取哈希——同一分叉点跨运行稳定可复现。
        """
        node_ids: List[str] = []
        semantics: List[str] = []
        for ch in getattr(engine, "chapters", []):
            for line in ch.causal_lines:
                for node in line.nodes:
                    node_ids.append(node.node_id)
                    semantics.append(f"{node.premise}=>{node.conclusion}")
        digest = hashlib.sha1("\n".join(semantics).encode("utf-8")).hexdigest()[:12]
        return {
            "chapters": len(getattr(engine, "chapters", [])),
            "node_count": len(node_ids),
            "digest": digest,
            "characters": len(engine.global_state.characters),
        }

    # ---------------- 派生与推演 ----------------

    def fork(
        self,
        variants: List[Any],
        render: bool = True,
        chapter_id: Optional[int] = None,
        max_rewrites: int = 1,
    ) -> List[Branch]:
        """从同一快照派生多条分支，各自独立推演。

        variants 支持两种形态：
          - ("标签", "用 -> 连接的大纲")
          - {"label": ..., "outline": ..., "characters": {...}}  # 可选分支专属角色档案
        """
        m = load_engine_module()
        next_id = chapter_id or (self.snapshot["chapters"] + 1)
        branches: List[Branch] = []

        for index, item in enumerate(variants):
            if isinstance(item, (tuple, list)) and len(item) >= 2:
                label, outline = str(item[0]), str(item[1])
                extra_chars = None
            elif isinstance(item, dict):
                label = str(item.get("label") or f"{self.title_prefix}{index + 1}")
                outline = str(item.get("outline") or "")
                extra_chars = item.get("characters")
            else:
                label, outline, extra_chars = f"{self.title_prefix}{index + 1}", str(item), None

            key = f"b{index + 1}"
            branch = Branch(
                key=key,
                label=label,
                outline=outline,
                parent_snapshot=dict(self.snapshot),
            )
            try:
                engine = copy.deepcopy(self.base)
                if extra_chars:
                    engine.global_state.characters.update(extra_chars)
                branch.engine = engine

                with strict_character_registry(self.strict_characters):
                    # 主引擎会把无箭头片段降级为「前提 +（待续）」的占位节点，
                    # 这种分支没有真实因果转换，必须先拦下，否则会被计为可用分支。
                    if "->" not in outline and "→" not in outline:
                        branch.error = "分支大纲缺少因果箭头（需「A -> B」或「A → B」形式）"
                        branches.append(branch)
                        continue
                    nodes = m.parse_outline_to_nodes(outline)
                    if not nodes:
                        branch.error = "大纲无法解析出因果节点"
                        branches.append(branch)
                        continue
                    for node in nodes:
                        if not node.character:
                            node.character = m.extract_character_from_text(
                                node.premise + node.conclusion
                            )
                    first = nodes[0].character if nodes else "主角"
                    line = m.CausalLine(line_id=f"ch{next_id}", character=first, nodes=nodes)
                    chapter = engine.plan_chapter(next_id, f"{self.title_prefix}·{label}", [line])
                    branch.chapter = chapter

                if chapter is None:
                    branch.error = "plan_chapter 返回空章节"
                    branches.append(branch)
                    continue

                if render:
                    rendered = engine.render_chapter(chapter)
                    branch.text = rendered if isinstance(rendered, str) else (chapter.content or "")
                else:
                    branch.text = outline

                branch.audit = self._audit(engine, branch, outline, max_rewrites)
            except Exception as exc:  # 单分支失败不拖垮整组推演
                branch.error = f"{type(exc).__name__}: {exc}"
            branches.append(branch)

        return branches

    def _audit(
        self, engine: Any, branch: Branch, outline: str, max_rewrites: int
    ) -> Dict[str, Any]:
        """分支自审：走引擎既有 audit_text；不达标时最多重写 max_rewrites 次。"""
        audit = engine.audit_text(
            branch.text, outline=outline, characters=engine.global_state.characters
        )
        attempts = 0
        while (
            not audit.get("all_passed")
            and engine.llm_provider is not None
            and attempts < max_rewrites
        ):
            presentation = audit.get("presentation") or {}
            issues: List[Any] = []
            for name in (
                "narration_perspective",
                "dialogue_era",
                "dialogue_cognition",
                "dialogue_registry",
            ):
                issues += (presentation.get(name) or {}).get("issues", [])
            if not issues:
                break
            repair = engine.repair_presentation_issues(
                branch.text, issues, outline=outline, characters=engine.global_state.characters
            )
            if not repair.get("rewritten"):
                break
            branch.text = repair["new_text"]
            attempts += 1
            audit = engine.audit_text(
                branch.text, outline=outline, characters=engine.global_state.characters
            )
        return audit

    # ---------------- 对比 ----------------

    def compare(self, branches: List[Branch]) -> Dict[str, Any]:
        """输出对比报告。排序规则明写，不伪装成客观最优。"""
        rows = []
        for branch in branches:
            metrics = branch.metrics(self.baseline_characters)
            rows.append(
                {
                    "key": branch.key,
                    "label": branch.label,
                    "outline": branch.outline,
                    "metrics": metrics,
                    "error": branch.error,
                }
            )

        valid = [r for r in rows if r["metrics"].get("ok")]
        # 排序规则（逐级）：审计失败面少 → 角色漂移少 → 未回收伏笔少 → 文本信息量多
        ranked = sorted(
            valid,
            key=lambda r: (
                len(r["metrics"]["failed_faces"]),
                r["metrics"]["drift_count"],
                r["metrics"]["unrecovered"],
                -r["metrics"]["chars"],
            ),
        )
        for position, row in enumerate(ranked, start=1):
            row["rank"] = position
            row["pareto"] = self._is_pareto(row, valid)

        return {
            "snapshot": self.snapshot,
            "strict_characters": self.strict_characters,
            "total": len(rows),
            "usable": len(valid),
            "failed": [r["key"] for r in rows if not r["metrics"].get("ok")],
            "rows": rows,
            "ranked_keys": [r["key"] for r in ranked],
            "recommended": ranked[0]["key"] if ranked else "",
            "ranking_rule": "审计失败面数 ↑ → 角色漂移数 ↑ → 未回收伏笔数 ↑ → 文本字数 ↓",
            "disclaimer": "排序规则是可复核的偏好，不是唯一最优解；帕累托前沿内的分支均无支配关系。",
        }

    @staticmethod
    def _is_pareto(row: Dict[str, Any], valid: List[Dict[str, Any]]) -> bool:
        """帕累托前沿：不存在同时在三项指标上都不差且至少一项更优的其他分支。"""
        mine = (
            len(row["metrics"]["failed_faces"]),
            row["metrics"]["drift_count"],
            row["metrics"]["unrecovered"],
        )
        for other in valid:
            if other is row:
                continue
            theirs = (
                len(other["metrics"]["failed_faces"]),
                other["metrics"]["drift_count"],
                other["metrics"]["unrecovered"],
            )
            if all(t <= m for t, m in zip(theirs, mine)) and theirs != mine:
                return False
        return True

    # ---------------- 呈现与导出 ----------------

    def table(self, branches: List[Branch]) -> str:
        report = self.compare(branches)
        head = (
            f"分叉点：第 {report['snapshot']['chapters']} 章后"
            f"（节点 {report['snapshot']['node_count']}，指纹 {report['snapshot']['digest']}）"
            f"｜自动角色注册：{'关闭' if self.strict_characters else '开启'}"
        )
        cols = [(3, "序"), (16, "分支"), (8, "审计"), (10, "失败面"), (5, "漂移"), (7, "未回收"), (6, "字数")]
        lines = [head, ""]
        lines.append("".join(_pad(name, width) for width, name in cols))
        lines.append("-" * (sum(w for w, _ in cols) + 2))
        order = {k: i for i, k in enumerate(report["ranked_keys"])}
        # 按排名输出，避免「行序」与「序号」两套顺序并存造成误读
        ordered = sorted(
            report["rows"],
            key=lambda r: order.get(r["key"], len(order) + 1),
        )
        for row in ordered:
            metrics = row["metrics"]
            if not metrics.get("ok"):
                lines.append(
                    _pad("-", 3) + _pad(row["label"], 16) + "跳过  " + row["error"]
                )
                continue
            rank = order.get(row["key"], 0) + 1
            mark = "*" if row.get("pareto") else " "
            failed = metrics["failed_faces"]
            faces = "".join(FACE_LABELS[f] for f in failed) if failed else "无"
            lines.append(
                _pad(rank, 3)
                + _pad(row["label"], 16)
                + _pad("通过" if metrics["all_passed"] else "未通过", 8)
                + _pad(faces, 10)
                + _pad(metrics["drift_count"], 5)
                + _pad(metrics["unrecovered"], 7)
                + _pad(metrics["chars"], 6, "right")
                + mark
            )
        lines.append("-" * (sum(w for w, _ in cols) + 2))
        lines.append("失败面缩写：叙=人称/视角 因=因果链 逻=逻辑 时=时空 伏=伏笔未回收")
        lines.append(f"排序规则：{report['ranking_rule']}")
        lines.append("* = 帕累托前沿内（无支配关系）；推荐项仅作默认，最终选线归作者")
        return "\n".join(lines)

    def to_markdown(self, branches: List[Branch]) -> str:
        report = self.compare(branches)
        snap = report["snapshot"]
        md = [
            "# 剧情多分支推演报告",
            "",
            f"- 分叉点：第 {snap['chapters']} 章后",
            f"- 快照指纹：`{snap['digest']}`（{snap['node_count']} 个因果节点）",
            f"- 自动角色注册：{'关闭（strict_characters=True）' if self.strict_characters else '开启'}",
            f"- 分支总数：{report['total']} ｜ 可用：{report['usable']}",
            "",
            "## 分支对比",
            "",
            "| 序 | 分支 | 审计 | 失败面 | 角色漂移 | 未回收伏笔 | 字数 | 帕累托 |",
            "|---|---|---|---|---|---|---|---|",
        ]
        order = {k: i for i, k in enumerate(report["ranked_keys"])}
        for row in sorted(report["rows"], key=lambda r: order.get(r["key"], len(order) + 1)):
            metrics = row["metrics"]
            if not metrics.get("ok"):
                md.append(
                    f"| - | {row['label']} | 跳过 | {row['error']} | - | - | - | - |"
                )
                continue
            md.append(
                f"| {order.get(row['key'], 0) + 1} | {row['label']} | "
                f"{'通过' if metrics['all_passed'] else '未通过'} | "
                f"{'、'.join(FACE_NAMES[f] for f in metrics['failed_faces']) or '无'} | "
                f"{metrics['drift_count']} | {metrics['unrecovered']} | "
                f"{metrics['chars']} | {'是' if row.get('pareto') else '否'} |"
            )

        md += ["", "## 各分支明细", ""]
        for row in report["rows"]:
            metrics = row["metrics"]
            md.append(f"### {row['label']}（{row['key']}）")
            md.append("")
            md.append(f"- 大纲：`{row['outline']}`")
            if not metrics.get("ok"):
                md.append(f"- ⚠️ 推演失败：{row['error']}")
                md.append("")
                continue
            md.append(f"- 因果节点：{metrics['nodes']} ｜ 成文 {metrics['chars']} 字")
            md.append(
                f"- 伏笔：SET {metrics['foreshadow_set']} / PAY {metrics['foreshadow_pay']}"
                f" / 未回收 {metrics['unrecovered']}"
            )
            if metrics["unrecovered_topics"]:
                md.append(f"- 未回收主题：{'、'.join(metrics['unrecovered_topics'])}")
            if metrics["character_drift"]:
                md.append(f"- ⚠️ 角色表新增：{'、'.join(metrics['character_drift'])}")
            md.append("")

        md += [
            "## 判定声明",
            "",
            f"- 排序规则：{report['ranking_rule']}",
            f"- 推荐（仅默认值）：{report['recommended'] or '无可用分支'}",
            f"- {report['disclaimer']}",
            "",
        ]
        return "\n".join(md)

    def to_json(self, branches: List[Branch]) -> Dict[str, Any]:
        return self.compare(branches)

    def pick(self, branches: List[Branch], key: str) -> Any:
        """选定分支，返回其引擎实例（主线上用它替换 self）。

        只返回引擎，不改动调用方状态：合流是显式动作，由调用方决定何时写回。
        """
        for branch in branches:
            if branch.key == key or branch.label == key:
                if branch.error or branch.engine is None:
                    raise ValueError(f"分支 {key} 不可用：{branch.error}")
                return branch.engine
        raise KeyError(f"找不到分支：{key}")


# ---------------- CLI ----------------

_DEMO_BASE_OUTLINE = (
    "林夏在评审会上坚持自研方案 -> 周舟梳理两套方案利弊 -> 林夏意识到忽略成本，同意第三方评审"
)

_DEMO_VARIANTS = [
    ("妥协线", "林夏接受第三方评审 -> 项目延期两周 -> 成本回落到预算内"),
    ("对抗线", "林夏拒绝第三方评审 -> 坚持自研上线 -> 预算超支四十个百分点"),
    ("折中线", "林夏接受评审但保留自研核心 -> 第三方只审成本模型 -> 上线推迟一周"),
]


class _DemoLLM:
    """演示用本地替身：不联网、不产生外部调用。"""

    def generate(self, prompt: str, **kwargs) -> str:
        return "（演示：未接入 LLM）角色在此节点推进，事件按大纲顺序展开。"


def _demo(out_dir: Optional[Path] = None) -> int:
    m = load_engine_module()
    state = m.GlobalState()
    state.characters["林夏"] = {"name": "林夏", "traits": ["固执"]}
    engine = m.UltimateCausalNovelEngine("分支推演演示", state)
    engine.set_llm_provider(_DemoLLM())
    # 基线章节按作者身份显式给角色，故同样关闭自动注册，避免把「周舟」这类名字漏进对比基线
    with strict_character_registry(True):
        engine.create_chapter_from_outline(1, "分歧与选择", _DEMO_BASE_OUTLINE)

    sim = BranchSimulator(engine, strict_characters=True)
    branches = sim.fork(_DEMO_VARIANTS)
    print(sim.table(branches))
    print()
    report = sim.compare(branches)
    print("推荐（默认）：", report["recommended"] or "无")
    print("失败分支：", report["failed"] or "无")

    if out_dir:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "branch_report.md").write_text(sim.to_markdown(branches), encoding="utf-8")
        (out_dir / "branch_report.json").write_text(
            json.dumps(sim.to_json(branches), ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"报告已写入：{out_dir}")
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    if not argv or "--help" in argv or "-h" in argv:
        print(
            "剧情多分支推演\n\n"
            "  python branch_simulator.py --demo [--out 目录]\n"
            "  python branch_simulator.py --variants variants.json [--out 目录] [--allow-auto-chars]\n\n"
            "variants.json 形态：\n"
            '  {"base_outline": "...", "variants": [{"label": "分支A", "outline": "A -> B -> C"}]}\n'
        )
        return 0

    out_dir = None
    if "--out" in argv:
        out_dir = Path(argv[argv.index("--out") + 1])

    if "--demo" in argv:
        return _demo(out_dir)

    if "--variants" in argv:
        path = Path(argv[argv.index("--variants") + 1])
        payload = json.loads(path.read_text(encoding="utf-8"))
        m = load_engine_module()
        state = m.GlobalState()
        for name, profile in (payload.get("characters") or {}).items():
            state.characters[name] = profile
        engine = m.UltimateCausalNovelEngine(payload.get("title") or "分支推演", state)
        engine.set_llm_provider(_DemoLLM())
        if payload.get("base_outline"):
            engine.create_chapter_from_outline(1, "已写章节", payload["base_outline"])
        sim = BranchSimulator(
            engine, strict_characters="--allow-auto-chars" not in argv
        )
        branches = sim.fork(payload.get("variants") or [])
        print(sim.table(branches))
        if out_dir:
            out_dir.mkdir(parents=True, exist_ok=True)
            (out_dir / "branch_report.md").write_text(
                sim.to_markdown(branches), encoding="utf-8"
            )
            (out_dir / "branch_report.json").write_text(
                json.dumps(sim.to_json(branches), ensure_ascii=False, indent=2), encoding="utf-8"
            )
            print(f"报告已写入：{out_dir}")
        return 0

    print("未指定动作，见 --help")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
