"""scripts/research_cli.py - HITL 大纲确认交互（A5 真交互，CLI 版）。

提供 research_interactive()：先以 confirm_outline=True 跑 research 生成 outline.md，
若需确认则提示用户编辑后继续（输入 continue / 直接回车 = 继续，其它 = 取消）。
库不强制任何 UI 框架，纯标准输入；调用方可在 agent 环境用等价交互替换。
"""

import builtins
from typing import Any, Dict

import research as _research


def research_interactive(query: str, cfg=None, vault_dir=None, **kw) -> Dict[str, Any]:
    """大纲确认交互式研究。

    - 首轮 confirm_outline=True → 若返回 needs_confirm，提示用户编辑 outline.md。
    - 用户输入 continue（或回车）则关闭 confirm_outline 重跑继续；其它输入视为取消。
    - vault_dir 默认 None（纯内存）；如需留存传 vault_dir="..."。
    """
    kw.setdefault("confirm_outline", True)
    if vault_dir is not None:
        kw["vault_dir"] = vault_dir
    out = _research.research(query, cfg=cfg, **kw)
    if out.get("needs_confirm"):
        ol = out.get("outline")
        try:
            ans = (
                builtins.input(
                    f"[research] 大纲已生成: {ol}\n"
                    f"[research] 编辑后输入 continue 继续，其它退出: "
                )
                .strip()
                .lower()
            )
        except Exception:
            ans = "cancel"
        if ans not in ("continue", ""):
            out["cancelled"] = True
            return out
        kw2 = dict(kw)
        kw2["confirm_outline"] = False
        out = _research.research(query, cfg=cfg, **kw2)
    return out


def research(query: str, cfg=None, on_progress=None, vault_dir=None, **kw) -> Dict[str, Any]:
    """稳定可嵌入 SDK（P2-14）：非交互式跑 research，并通过 on_progress 暴露阶段事件。

    - 不触 stdin，适合 agent / 后台 / 单元测试调用。
    - on_progress(event: dict) 在关键阶段触发：stage ∈ {start, tier, skipped, outline,
      warnings, done, error}，附阶段相关信息（tier / skip_reason / confidence / warnings 等）。
    - vault_dir 默认 None（纯内存，P1-7 默认关）；如需留存传 vault_dir="..."。
    - confirm_outline 默认 False（SDK 不阻塞）；需要 HITL 大纲确认请用 research_interactive()。
    """

    def _emit(stage, **info):
        if callable(on_progress):
            try:
                on_progress({"stage": stage, **info})
            except Exception:
                pass

    _emit("start", query=query)
    try:
        kw.setdefault("confirm_outline", False)
        if vault_dir is not None:
            kw["vault_dir"] = vault_dir
        out = _research.research(query, cfg=cfg, **kw)
        if out.get("skipped"):
            _emit("skipped", reason=out.get("skip_reason"))
        elif out.get("needs_confirm"):
            _emit("outline", outline=out.get("outline"))
        warns = (out.get("meta") or {}).get("warnings") or []
        if warns:
            _emit("warnings", count=len(warns), warnings=warns)
        _emit("done", confidence=out.get("confidence"), tier_used=out.get("tier_used"))
        return out
    except Exception as e:  # 向上抛，但先发 error 事件便于观测
        _emit("error", error=str(e))
        raise
