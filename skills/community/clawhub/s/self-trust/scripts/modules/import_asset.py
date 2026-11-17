# -*- coding: utf-8 -*-
"""第三方资产导入（§7.3）：CSV / 手动录入 → 拉取候选 → 人工核对 → 确认生效。

状态机（§7.3 硬约束）：
- ``imported_pending``：导入已拉取但尚未人工核对确认；**禁止任何支取审批**
  （judge 入口前置拦截，见 modules/judge.py）。
- ``imported_confirmed``：用户修正确认后生效，资产池正式纳入资金池。

数据中立机制（§3 / §11.5）：
- 候选数据先暂存于 RUNTIME 区 ``pending_import``，**不立即写入 live corpus**；
  核对确认（confirm）后才落到配置区的 corpus / monthly_contribution /
  liabilities / rigid_annual_expenses；取消（cancel）仅清 staging 并还原
  corpus_status，live corpus 原值不受污染（避免未核实数据污染后续所有审批）。
- 两步确认 + token 防漂移（复用 §5.4 范式）。

CSV 格式（balances）：``name,balance,kind[,monthly]``
  kind ∈ {asset, liability, rigid}；asset 余额为正；liability 余额为正（债务额）、
  monthly=月供；rigid 余额为正（年支出额）、monthly 缺省=余额/12。
CSV 格式（flows，可选）：``date,amount``（date YYYY-MM-DD；amount 正负=收支；
  月均净流入 = Σ/月数）。
"""
from __future__ import annotations

import csv
import secrets
from datetime import date, datetime
from pathlib import Path
from typing import Any, Optional

from core import audit as audit_io
from core import contract as contract_io
from core.i18n import CORPUS_STATUS_ZH, zh
from core.util import make_token as _token, contract_sha as _contract_sha


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def parse_money(raw: Any) -> float:
    """解析金额（M1/M2）：容忍币种符号（¥ $ ￥）、千分位逗号、首尾空白；
    落到「分」并 round 2 位，避免浮点亚分漂移；非法 → ValueError。"""
    if raw is None:
        return 0.0
    s = str(raw).strip()
    if not s:
        return 0.0
    s = (s.replace("¥", "").replace("￥", "").replace("$", "")
          .replace(",", "").replace(" ", "").strip())
    try:
        return round(float(s), 2)
    except ValueError:
        raise ValueError(f"金额无法解析: {raw!r}")


def normalize_flow_date(ds: str) -> str:
    """流水日期归一化（M2）：接受 年-月-日 / 年/月/日 / 年.月.日 / 年-月（年首格式），
    分隔符统一为「-」；仅接受「4 位年在前」以避免美式 MM/DD/YYYY 歧义；非法 → ValueError。"""
    s = str(ds).strip()
    if not s:
        raise ValueError("flows CSV date 为空")
    norm = s.replace("/", "-").replace(".", "-")
    parts = [p for p in norm.split("-") if p != ""]
    if parts and len(parts[0]) == 4 and all(p.isdigit() for p in parts[:3]):
        return norm  # YYYY-MM-DD / YYYY-MM
    raise ValueError(f"flows CSV date 须为「年-月-日」（年在前），得到 {ds!r}")


def parse_balances_csv(path: Any) -> list[dict[str, Any]]:
    """解析余额 CSV（name,balance,kind[,monthly[,due_month]]）→ 规范行列表。

    - balance / monthly 走 parse_money（容忍 ¥ $ 千分位逗号，M2）；
    - due_month 仅 rigid 有意义（1–12 月，M3），缺省/非法 → None。
    """
    p = Path(path)
    rows: list[dict[str, Any]] = []
    with open(p, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, 1):
            name = (row.get("name") or "").strip()
            kind = (row.get("kind") or "").strip().lower()
            if not name or not kind:
                raise ValueError(f"balances CSV 第 {i} 行缺少 name 或 kind")
            if kind not in ("asset", "liability", "rigid"):
                raise ValueError(
                    f"balances CSV 第 {i} 行 kind 须为 asset/liability/rigid，得到 {kind!r}")
            balance = parse_money(row.get("balance"))
            monthly_raw = (row.get("monthly") or "").strip()
            monthly_val = parse_money(monthly_raw) if monthly_raw else 0.0
            due_raw = (row.get("due_month") or row.get("due") or row.get("month") or "").strip()
            due_month = None
            if due_raw:
                try:
                    dm = int(float(due_raw))
                    if 1 <= dm <= 12:
                        due_month = dm
                except (ValueError, TypeError):
                    due_month = None  # 非 1–12 整数 → 视为无到期月（不报错，交由人工核对）
            rows.append({"name": name, "balance": balance, "kind": kind,
                         "monthly": monthly_val, "due_month": due_month})
    if not rows:
        raise ValueError("balances CSV 为空（至少需要一行资产）")
    return rows


def parse_flows_csv(path: Any) -> list[tuple[str, float]]:
    """解析流水 CSV（date,amount）→ [(date_str, amount), ...]。

    amount 走 parse_money（M2）；date 走 normalize_flow_date（M2 多格式容错）。
    """
    p = Path(path)
    out: list[tuple[str, float]] = []
    with open(p, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, 1):
            ds = (row.get("date") or "").strip()
            am = (row.get("amount") or "").strip()
            if not ds or not am:
                raise ValueError(f"flows CSV 第 {i} 行缺少 date 或 amount")
            amount = parse_money(am)
            out.append((normalize_flow_date(ds), amount))
    return out


def _money_close(a: float, b: float, tol: float = 0.005) -> bool:
    """金额容差相等（M1）：落到分后比较，避免浮点亚分差异导致误判。"""
    return abs(float(a) - float(b)) <= tol


def _merge_list_by_name(staged: list[dict[str, Any]], corrected: list[dict[str, Any]],
                        name_key: str) -> list[dict[str, Any]]:
    """按 name 合并修正列表（M6）：修正项覆盖/新增同名条目，未提及的暂存项保留，
    避免「部分负债/刚性修正」整体覆盖暂存清单造成的数据丢失。"""
    by_name: dict[Any, dict[str, Any]] = {item.get(name_key): item for item in staged}
    for item in corrected:
        by_name[item.get(name_key)] = item
    return list(by_name.values())


def _dedup_balances(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """按 (name, kind) 去重合并，防止同一账户在 CSV/手动录入中重复列出导致资产/负债双倍计入。

    - 完全重复行（name/balance/kind/monthly 全同）= 同账户重复导出 → 丢弃多余副本。
    - 同 name+kind 但余额/月供不同 = 歧义（可能错列/重复导出）→ 取「文件中后出现者」
      （最新快照）覆盖并告警，不静默丢弃、也不求和（求和会让同账户余额翻倍，污染 corpus）。
    """
    warnings: list[dict[str, Any]] = []
    seen: dict[tuple[str, str], int] = {}  # (name, kind) -> index in merged
    merged: list[dict[str, Any]] = []
    for r in rows:
        key = (r["name"], r["kind"])
        idx = seen.get(key)
        if idx is None:
            merged.append(dict(r))
            seen[key] = len(merged) - 1
            continue
        prev = merged[idx]
        # M1：金额按「分」容差比较（≤0.005），避免浮点亚分差异误判为非重复行
        if (_money_close(prev["balance"], r["balance"])
                and _money_close(prev["monthly"], r["monthly"])):
            continue  # 完全重复 → 丢弃副本（修复 H1：不再双倍计入）
        # M8：同账户余额不同 → 视为重复导出/错账，取最新出现值覆盖并告警，
        # 不再求和（求和会让同一账户余额翻倍，污染 corpus/负债）。
        prev["balance"] = r["balance"]
        prev["monthly"] = r["monthly"]
        warnings.append({
            "name": r["name"], "kind": r["kind"],
            "reason": (f"「{r['name']}」({r['kind']}) 出现多次且余额/月供不一致，"
                       "已按最新出现值覆盖合并，请核对是否为错账或重复导出"),
        })
    return merged, warnings


def compute_candidates(balances: list[dict[str, Any]],
                       flows: Optional[list[tuple[str, float]]] = None) -> dict[str, Any]:
    """由余额 / 流水行推导导入候选。

    返回：{ corpus, monthly_contribution, liabilities, rigid_annual_expenses,
            suspicious, summary }
    - corpus = Σ 资产余额（kind=asset）
    - liabilities = [{name, balance, monthly_payment, annual_rate}]
    - rigid_annual_expenses = [{name, amount, due_month}]
    - monthly_contribution = 流水月均净流入（无流水则 0）
    - suspicious = 流水异常月份（月净流入绝对值 > 3×中位数，提示用户核对）
    """
    corpus = 0.0
    liabilities: list[dict[str, Any]] = []
    rigid: list[dict[str, Any]] = []
    asset_rows = liability_rows = rigid_rows = 0
    # 修复 H1：先按 (name, kind) 去重合并，避免重复行导致资产/负债双倍计入
    balances, dedup_warnings = _dedup_balances(balances)
    for r in balances:
        if r["kind"] == "asset":
            asset_rows += 1
            corpus += float(r["balance"])
        elif r["kind"] == "liability":
            liability_rows += 1
            liabilities.append({
                "name": r["name"],
                "balance": abs(float(r["balance"])),
                "monthly_payment": float(r["monthly"]),
                "annual_rate": 0.0,
            })
        elif r["kind"] == "rigid":
            rigid_rows += 1
            rigid.append({
                "name": r["name"],
                "amount": float(r["balance"]),
                "due_month": r.get("due_month"),  # M3：透传到期月（缺省 None，不再恒 None）
            })
    monthly = 0.0
    suspicious: list[dict[str, Any]] = []
    if flows:
        by_month: dict[str, float] = {}
        for ds, amt in flows:
            month = ds[:7]  # YYYY-MM
            by_month[month] = by_month.get(month, 0.0) + float(amt)
        nets = list(by_month.values())
        if nets:
            # 真中位：奇数取中项，偶数取上下中位均值（原写法偶数取上中位，偏误）
            _sn = sorted(nets)
            _n = len(_sn)
            median = (_sn[_n // 2] + _sn[(_n - 1) // 2]) / 2
            monthly = sum(nets) / len(nets)
            for m, net in sorted(by_month.items()):
                if median and abs(net) > 3 * abs(median):
                    suspicious.append({
                        "month": m, "net": net,
                        "reason": (f"月净流入 {net} 偏离中位数 {median} 超 3 倍，"
                                   "请核对是否有重复记账 / 错账 / 币种错配"),
                    })
    # provided：来源（CSV/手动）实际提供了哪些分类。confirm 据此只覆盖显式项，
    # 缺类（如 CSV 只有资产、没有负债/刚性行）视为「未提供」→ 保留 live 原值（#1 修复）。
    provided = {
        "corpus": asset_rows > 0,
        "monthly_contribution": bool(flows),
        "liabilities": liability_rows > 0,
        "rigid_annual_expenses": rigid_rows > 0,
    }
    return {
        "corpus": corpus,
        "monthly_contribution": monthly,
        "liabilities": liabilities,
        "rigid_annual_expenses": rigid,
        "suspicious": suspicious,
        "warnings": dedup_warnings,
        "provided": provided,
        "summary": {
            "total_assets": corpus,
            "liabilities_count": len(liabilities),
            "rigid_count": len(rigid),
            "months_flow": len(flows) if flows else 0,
        },
    }


def _staging_baseline_sha(contract: dict[str, Any], prior_status: str) -> str:
    """契约摘要（排除 stage 自身写入的 pending_import，仅对真实配置区）。

    与 confirm 时的比对口径一致：契约在 stage→confirm 之间仅 pending_import /
    corpus_status 被本流程改动，其余真实字段须不变；中途 customize 改动会被检出。
    注意必须「删除」pending_import 键而非置 null——原契约存为 `pending_import: null`，
    键删除后与 confirm 侧口径一致，否则 sha 不匹配会误拒每一次确认。
    """
    base = {k: v for k, v in contract.items() if k != "pending_import"}
    base["corpus_status"] = prior_status
    return _contract_sha(base)


def stage_import(contract: dict[str, Any], candidates: dict[str, Any],
                 source: str, today: Optional[date] = None) -> dict[str, Any]:
    """§7.3 第一步：拉取候选并暂存，置 corpus_status=imported_pending（锁定审批）。

    live corpus 暂不写入（staging 在 RUNTIME 区 pending_import），核对确认才落盘。
    返回摘要 + 确认 token（confirm 须带；cancel 亦须带）。
    """
    # R3：已有待核对导入（imported_pending）未确认/取消时，禁止重复 stage 静默覆盖
    #     旧候选；须先 confirm 或 cancel 当前导入，再发起新导入。
    if contract.get("corpus_status") == "imported_pending" and contract.get("pending_import"):
        return {
            "ok": False, "error": "already_staged",
            "message": ("已有待核对导入未确认/取消，"
                        "禁止重复拉取覆盖旧候选（R3）；请先 confirm 或 cancel "
                        "当前导入，再发起新导入。"),
        }
    prior_status = contract.get("corpus_status", "manual")
    _sha = _staging_baseline_sha(contract, prior_status)
    staging = {
        "source": source,
        "candidates": candidates,
        "prior_status": prior_status,
        "staged_at": _now(),
        # M9 加固：记下 stage 时契约摘要，confirm 时比对，防 stage 后 customize
        # 改动 live 契约被陈旧暂存覆盖（customize 自身有同等护栏，import 此前缺失）。
        "contract_sha": _sha,
    }
    tok = _token(staging, _sha)
    staging["token"] = tok
    contract["corpus_status"] = "imported_pending"
    contract["pending_import"] = staging
    return {
        "ok": True,
        "staged": True,
        "needs_confirm": True,
        "import_status": "imported_pending",
        "token": tok,
        "source": source,
        "summary": candidates["summary"],
        "suspicious": candidates["suspicious"],
        "warnings": candidates.get("warnings", []),
        "candidates": {
            "corpus": candidates["corpus"],
            "monthly_contribution": candidates["monthly_contribution"],
            "liabilities": candidates["liabilities"],
            "rigid_annual_expenses": candidates["rigid_annual_expenses"],
        },
        "message": (
            "已拉取第三方资产候选并暂存，审批已锁定。"
            "请逐项核对摘要与可疑流水；确认请带本 token 执行 confirm，"
            "或带 token 执行 cancel 放弃本次导入。"),
    }


def _get_staging(contract: dict[str, Any], token: str) -> tuple[Optional[dict[str, Any]], Optional[str]]:
    staging = contract.get("pending_import")
    # M9：恒定时间比较，防时序攻击推断 token（secrets.compare_digest）
    if not staging or not secrets.compare_digest(
            str(staging.get("token") or ""), str(token or "")):
        return None, "bad_token"
    return staging, None


def confirm_import(contract: dict[str, Any], token: str,
                   corrections: Optional[dict[str, Any]] = None,
                   today: Optional[date] = None) -> dict[str, Any]:
    """§7.3 第二步：核对确认，将候选（可被 corrections 修正）落到 live 配置区。

    corpus / monthly_contribution / liabilities / rigid_annual_expenses 写入；
    corpus_status → imported_confirmed；清空 pending_import。
    """
    staging, err = _get_staging(contract, token)
    if err:
        return {"ok": False, "error": err,
                "message": "导入 token 不匹配（须用 stage 返回的 token）"}
    # M9 加固：stage 后契约若被改动（如中途 customize），拒绝确认，
    # 防陈旧暂存值覆盖 live 编辑导致静默数据丢失。
    # 注意：比对须排除 stage 自身写入的 pending_import / corpus_status，
    # 仅对真实配置区求 sha（与 stage 时存的 baseline 一致）。
    _base = {k: v for k, v in contract.items() if k != "pending_import"}
    _base["corpus_status"] = staging.get("prior_status", contract.get("corpus_status"))
    if _contract_sha(_base) != staging.get("contract_sha"):
        return {"ok": False, "error": "contract_changed",
                "message": "导入暂存后契约已变更（如中途 customize），"
                           "请重新 stage 再确认。"}
    cands = dict(staging["candidates"])
    # 来源显式提供了哪些分类（stage 时标记）；旧数据无 provided 则回退为「全部覆盖」。
    staged_provided = cands.get("provided", {
        "corpus": True, "monthly_contribution": True,
        "liabilities": True, "rigid_annual_expenses": True,
    })
    if corrections:
        for k, v in corrections.items():
            if v is None:
                continue
            # M6：列表型分类（liabilities / rigid_annual_expenses）按 name 合并修正，
            # 而非整表覆盖暂存清单——部分修正不再丢数据。
            if k in ("liabilities", "rigid_annual_expenses") and isinstance(v, list):
                cands[k] = _merge_list_by_name(cands.get(k, []), v, "name")
            else:
                cands[k] = v
    # 仅覆盖「来源提供」或「人工修正」的分类；其余 live 原值保留，
    # 避免 CSV 缺某类（如负债/刚性）时静默清空已录入资产（#1 修复）。
    provided = dict(staged_provided)
    if corrections:
        for k in corrections:
            provided[k] = True
    if provided.get("corpus"):
        contract["corpus"] = float(cands["corpus"])
    if provided.get("monthly_contribution"):
        contract["monthly_contribution"] = float(cands["monthly_contribution"])
    if provided.get("liabilities"):
        contract["liabilities"] = cands["liabilities"]
    if provided.get("rigid_annual_expenses"):
        contract["rigid_annual_expenses"] = cands["rigid_annual_expenses"]
    contract["corpus_status"] = "imported_confirmed"
    contract["pending_import"] = None
    return {
        "ok": True,
        "confirmed": True,
        "corpus_status": "imported_confirmed",
        "import_status": "imported_confirmed",
        "applied": {
            "corpus": contract["corpus"],
            "monthly_contribution": contract["monthly_contribution"],
            "liabilities": contract["liabilities"],
            "rigid_annual_expenses": contract["rigid_annual_expenses"],
        },
        "message": ("第三方资产已核对确认并生效，"
                    "资产池正式纳入资金池，可正常审批。"),
    }


def cancel_import(contract: dict[str, Any], token: str) -> dict[str, Any]:
    """放弃导入：还原 corpus_status（prior_status）并清空 pending_import；live corpus 不变。"""
    staging, err = _get_staging(contract, token)
    if err:
        return {"ok": False, "error": err,
                "message": "导入 token 不匹配（须用 stage 返回的 token）"}
    prior = staging.get("prior_status", "manual")
    contract["corpus_status"] = prior
    contract["pending_import"] = None
    return {
        "ok": True,
        "cancelled": True,
        "corpus_status_restored": prior,
        "import_status": prior,
        "message": f"已放弃本次导入，资产状态还原为「{zh(CORPUS_STATUS_ZH, prior)}」（实际资产未改动）。",
    }
