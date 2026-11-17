# -*- coding: utf-8 -*-
"""self-trust 统一 CLI 入口（设计文档 §8.3 #1 / §9）。

子命令：judge | init | report | reconcile | calibrate | reward | reset | appeal | log
- 全部输出结构化 JSON（stdout，UTF-8）；LLM 铁律：禁止心算，数字原样引用本输出。
- 数据目录解析优先级：--data-dir > SELFTRUST_DATA_DIR > <home>/.claw/self-trust/（README）。
- 引擎错误显式返回 {"ok": false, "error": ...}，退出码非 0，不吞错。

示例：
    python scripts/cli.py --data-dir /tmp/st init --json \\
        --corpus 200000 --monthly 8000 \\
        --objective "FIRE:3000000:2036-01-01"
    python scripts/cli.py judge --json --amount 6000 --category 合理享受
    python scripts/cli.py judge --action withdraw --request-id abc123
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

# 允许 `python scripts/cli.py` 直接运行（scripts/ 加入 sys.path）
sys.path.insert(0, str(Path(__file__).resolve().parent))

from core import audit as audit_io           # noqa: E402
from core import contract as contract_io     # noqa: E402
from core import crypto as crypto_io         # noqa: E402
from core.contract import GuardError, ContractCorruptedError  # noqa: E402
from core.models import ObjectiveStatus  # noqa: E402
from modules import calibrate as mod_cal     # noqa: E402
from modules import customize as mod_customize  # noqa: E402
from modules import governance as mod_gov    # noqa: E402
from modules import initialize as mod_init   # noqa: E402
from modules import judge as mod_judge       # noqa: E402
from modules import report as mod_report     # noqa: E402
from modules import reward as mod_reward     # noqa: E402
from modules import import_asset as mod_import  # noqa: E402

from render import renderer as rdr  # noqa: E402


def _resolve_subcmd(args: argparse.Namespace | None) -> str:
    """从 argparse namespace 中提取子命令（action/action，judge默认submit）。"""
    if args is None:
        return ""
    action = getattr(args, "action", None)
    if action:
        return action
    return ""


def _emit(payload: dict, code: int = 0,
          args: argparse.Namespace | None = None) -> int:
    # Windows 控制台可能默认 GBK，强制 UTF-8 防中文/符号编码失败（跨平台一致）
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    cmd = args.command if args and getattr(args, "text", False) else ""
    sub = _resolve_subcmd(args) if cmd else ""
    if cmd:
        text = rdr.render(payload, cmd, sub)
        sys.stdout.write(text + "\n")
    else:
        sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    return code


def _parse_objective(spec: str) -> dict:
    """解析 --objective "名称:目标额:期限"；目标额/期限可省略（无期限目标）。"""
    parts = spec.split(":")
    obj: dict = {"name": parts[0]}
    if len(parts) > 1 and parts[1]:
        ta = float(parts[1])
        if ta <= 0:   # L3：目标额须为正，负值会让 f4_lag 达成率变负、语义错乱
            raise ValueError(f"目标额须为正数，得到 {parts[1]!r}（目标 {parts[0]}）")
        obj["target_amount"] = ta
    if len(parts) > 2 and parts[2]:
        obj["deadline"] = parts[2]
    return obj


def _parse_liability(spec: str) -> dict:
    """解析 负债 名称:余额[:月供[:年利率]]（L11：本地实现，解耦 customize 私有导入）。"""
    parts = spec.split(":")
    if len(parts) < 2 or not parts[0] or not parts[1]:
        raise ValueError("--add-liability 格式应为 名称:余额[:月供[:年利率]]")
    return {
        "name": parts[0],
        "balance": float(parts[1]),
        "monthly_payment": float(parts[2]) if len(parts) > 2 and parts[2] else 0.0,
        "annual_rate": float(parts[3]) if len(parts) > 3 and parts[3] else 0.0,
    }


def _parse_rigid(spec: str) -> dict:
    """解析 刚性年支出 名称:金额[:due_month]（L11：本地实现，解耦 customize 私有导入）。"""
    parts = spec.split(":")
    if len(parts) < 2 or not parts[0] or not parts[1]:
        raise ValueError("--add-rigid 格式应为 名称:金额[:due_month]")
    return {
        "name": parts[0],
        "amount": float(parts[1]),
        "due_month": int(parts[2]) if len(parts) > 2 and parts[2] else None,
    }



def _today(args) -> date | None:
    return date.fromisoformat(args.today) if getattr(args, "today", None) else None


def _configure_crypto(args) -> None:
    """按 CLI/环境变量设置加密 session + 审计加密标志（方案 C）。

    - passphrase 模式：--pass / SELFTRUST_PASS 提供密码；
    - key-file 模式：--key-file / SELFTRUST_KEY_FILE 提供密钥文件路径；
    - 非 init 命令：按已存在契约的 crypto.enabled 设置审计日志加密标志；
    - init 命令：按 --encrypt 设置审计加密标志（契约尚不存在）。
    """
    import os
    passphrase = getattr(args, "pass_", None)
    key_file = getattr(args, "key_file", None)
    if not passphrase and not key_file:           # 环境变量回退
        passphrase = os.environ.get("SELFTRUST_PASS")
        key_file = os.environ.get("SELFTRUST_KEY_FILE")
    crypto_io.set_session(passphrase=passphrase, key_file=key_file)

    if getattr(args, "command", None) == "init":
        crypto_io.set_audit_encrypted(bool(getattr(args, "encrypt", False)))
        return
    # 其余命令：探测现有契约，按其加密开关设置审计加密标志
    # resolve_data_dir 不抛异常（命令行 > env > 默认家目录，路径构造均安全），
    # 原裸 except Exception 会静默吞掉一切并使审计加密标志退化，已移除。
    dd = contract_io.resolve_data_dir(args.data_dir)
    enabled = False
    if contract_io.contract_exists(dd):
        # key-file 模式密钥默认落在 <data-dir>/.self-trust.key，无需读契约即可定位
        if not passphrase and not key_file:
            default_kf = dd / ".self-trust.key"
            if default_kf.is_file():
                key_file = str(default_kf)
        try:
            contract = contract_io.read_contract(dd)
            enabled = bool(contract.get("crypto", {}).get("enabled"))
        except crypto_io.CryptoError:
            # 加密契约但密钥不对/缺失：标记加密，让具体命令读时抛清晰错误
            enabled = True
    crypto_io.set_session(passphrase=passphrase, key_file=key_file)
    crypto_io.set_audit_encrypted(enabled)


def cmd_init(args) -> int:
    data_dir = contract_io.resolve_data_dir(args.data_dir)
    objectives = [_parse_objective(s) for s in (args.objective or [])]
    result = mod_init.lazy_init(
        data_dir,
        corpus=args.corpus,
        monthly_contribution=args.monthly,
        objectives=objectives,
        today=_today(args),
        currency=args.currency,
        encrypt=args.encrypt,
        crypto_mode=args.crypto_mode,
    )
    return _emit(result, 0 if result.get("ok") else 1, args)


def cmd_judge(args) -> int:
    data_dir = contract_io.resolve_data_dir(args.data_dir)
    action = args.action or "submit"
    if action == "submit":
        if args.amount is None or args.category is None:
            return _emit({"ok": False, "error": "invalid",
                          "message": "judge 提交须提供 --amount 与 --category"}, 4, args)
        result = mod_judge.submit(
            data_dir, amount=args.amount, category=args.category,
            planned=args.planned, today=_today(args),
            financed_amount=args.financed_amount,
            financed_term_years=args.financed_term_years,
            financed_rate=args.financed_rate,
            financed_monthly=args.financed_monthly,
            currency=args.currency,
            exchange_rate=args.rate)
    elif action in ("withdraw", "finalize") and not args.request_id:
        result = {"ok": False, "error": "invalid",
                  "message": f"{action} 须提供 --request-id"}
    elif action == "withdraw":
        result = mod_judge.withdraw(data_dir, args.request_id, today=_today(args))
    elif action == "finalize":
        result = mod_judge.finalize(data_dir, args.request_id, today=_today(args))
    elif action == "expire":
        result = mod_judge.expire(data_dir, args.request_id, today=_today(args))
    elif action == "reminders":
        contract = contract_io.read_contract(data_dir)
        result = {"ok": True, "reminders":
                  mod_judge.list_due_reminders(contract, today=_today(args))}
    else:  # pragma: no cover - argparse choices 已限制
        result = {"ok": False, "error": "invalid", "message": f"未知 action {action}"}
    return _emit(result, 0 if result.get("ok") else 1, args)


def cmd_demo(args) -> int:
    """§7.2 三场景模拟演示（干跑不落盘）：有契约用真实参数，无契约用演示默认值。"""
    data_dir = contract_io.resolve_data_dir(args.data_dir)
    contract = (contract_io.read_contract(data_dir)
                if contract_io.contract_exists(data_dir) else None)
    result = mod_init.demo_scenarios(contract, today=_today(args))
    return _emit(result, 0 if result.get("ok") else 1, args)


def cmd_report(args) -> int:
    data_dir = contract_io.resolve_data_dir(args.data_dir)
    # §5.4 冷却窗懒惰终裁：报表交互时扫描过期项自动生效（复用 §5.1 范式）
    mod_customize.sweep_pending_config(data_dir)
    result = mod_report.run_report(data_dir, today=_today(args))
    return _emit(result, 0 if result.get("ok") else 1, args)


def cmd_reconcile(args) -> int:
    data_dir = contract_io.resolve_data_dir(args.data_dir)
    result = mod_gov.reconcile(
        data_dir, corpus=args.corpus, income=args.income,
        invest=args.invest, living=args.living, impulse=args.impulse,
        today=_today(args))
    return _emit(result, 0 if result.get("ok") else 1, args)


def cmd_calibrate(args) -> int:
    data_dir = contract_io.resolve_data_dir(args.data_dir)
    result = mod_cal.run_calibrate(data_dir, today=_today(args), force=args.force)
    return _emit(result, 0 if result.get("ok") else 1, args)


def cmd_reward(args) -> int:
    data_dir = contract_io.resolve_data_dir(args.data_dir)
    if args.action == "status":
        contract = contract_io.read_contract(data_dir)
        result = mod_reward.reward_status(contract)
    elif args.action == "unlock":
        result = mod_reward.unlock_rewards(data_dir)
    else:  # claim
        if args.objective is None or args.amount is None:
            return _emit({"ok": False, "error": "invalid",
                          "message": "claim 须提供 --objective 与 --amount"}, 4, args)
        result = mod_reward.claim_reward(
            data_dir, objective=args.objective, amount=args.amount,
            purpose=args.purpose or "", today=_today(args))
    return _emit(result, 0 if result.get("ok") else 1, args)


def cmd_reset(args) -> int:
    data_dir = contract_io.resolve_data_dir(args.data_dir)
    objectives = [_parse_objective(s) for s in (args.objective or [])]
    result = mod_gov.reset_contract(
        data_dir, confirm=args.confirm, corpus=args.corpus,
        monthly_contribution=args.monthly,
        objectives=objectives or None, reason=args.reason or "",
        today=_today(args))
    return _emit(result, 0 if result.get("ok") else 1, args)


def cmd_appeal(args) -> int:
    data_dir = contract_io.resolve_data_dir(args.data_dir)
    if args.override:
        result = mod_gov.override(
            data_dir, request_id=args.request_id, confirm=args.confirm,
            today=_today(args))
    else:
        result = mod_gov.appeal(
            data_dir, request_id=args.request_id, reason=args.reason or "",
            today=_today(args))
    return _emit(result, 0 if result.get("ok") else 1, args)


def cmd_objective(args) -> int:
    data_dir = contract_io.resolve_data_dir(args.data_dir)
    result = mod_cal.transition_objective(
        data_dir, args.name, args.to, confirm=args.confirm,
        today=_today(args))  # N3：传递逻辑 today，审计时间对齐
    return _emit(result, 0 if result.get("ok") else 1, args)


def cmd_log(args) -> int:
    data_dir = contract_io.resolve_data_dir(args.data_dir)
    records = audit_io.read_all(data_dir, args.name)
    return _emit({"ok": True, "log": args.name,
                  "count": len(records), "records": records}, args)


def cmd_customize(args) -> int:
    data_dir = contract_io.resolve_data_dir(args.data_dir)
    # 冷却窗复查（先懒惰扫描过期项自动生效，再列待决 + 二次提醒）
    if args.review:
        result = mod_customize.review_config(data_dir)
        return _emit(result, 0 if result.get("ok") else 1, args)
    # 冷却窗撤回（窗内无理由撤回）
    if args.withdraw:
        if not args.request_id or not args.token:
            return _emit({"ok": False, "error": "invalid",
                          "message": "--withdraw 须同时带 --request-id 与 --token（撤回 token）"}, 4, args)
        result = mod_customize.withdraw_config(data_dir, args.request_id, args.token)
        return _emit(result, 0 if result.get("ok") else 1, args)
    # 预览 / 应用（§5.4 二次确认；削弱自身进冷却窗）
    try:
        changes = mod_customize.build_changes(args)
    except ValueError as e:
        return _emit({"ok": False, "error": "invalid", "message": str(e)}, 4, args)
    result = mod_customize.apply(
        data_dir, changes, confirm=args.confirm, token=args.token,
        reason=args.reason or "")
    return _emit(result, 0 if result.get("ok") else 1, args)


def cmd_import_asset(args) -> int:
    """§7.3 第三方资产导入：CSV/手动 → 暂存(imported_pending) → 核对确认(confirm)。"""
    data_dir = contract_io.resolve_data_dir(args.data_dir)
    contract = contract_io.read_contract(data_dir)  # 须先 init

    if args.confirm:
        if not args.token:
            return _emit({"ok": False, "error": "invalid",
                          "message": "confirm 须带 --token（stage 返回）"}, 4, args)
        corrections: dict[str, Any] = {}
        if args.corpus is not None:
            corrections["corpus"] = args.corpus
        if args.monthly is not None:
            corrections["monthly_contribution"] = args.monthly
        if args.liabilities is not None:
            corrections["liabilities"] = [_parse_liability(s) for s in args.liabilities]
        if args.rigid is not None:
            corrections["rigid_annual_expenses"] = [_parse_rigid(s) for s in args.rigid]
        import_source = (contract.get("pending_import") or {}).get("source", "manual")
        result = mod_import.confirm_import(
            contract, args.token, corrections or None, today=_today(args))
        if result.get("ok"):
            contract_io.write_contract(data_dir, contract, actor="configurator", confirm=True)
            audit_io.append(data_dir, "override_log", {
                "time": audit_io.now_iso(_today(args)), "event": "asset_import_confirmed",
                "source": import_source,
                "applied": result.get("applied"),
                "reason": "第三方资产人工核对确认（§7.3）",
            })
        return _emit(result, 0 if result.get("ok") else 1, args)

    if args.cancel:
        if not args.token:
            return _emit({"ok": False, "error": "invalid",
                          "message": "cancel 须带 --token（stage 返回）"}, 4, args)
        result = mod_import.cancel_import(contract, args.token)
        if result.get("ok"):
            contract_io.write_contract(data_dir, contract, actor="configurator", confirm=True)
        return _emit(result, 0 if result.get("ok") else 1, args)

    # —— 发起导入（stage）——
    if args.balances:
        balances = mod_import.parse_balances_csv(args.balances)
        flows = mod_import.parse_flows_csv(args.flows) if args.flows else None
        candidates = mod_import.compute_candidates(balances, flows)
    elif args.corpus is not None:
        liabilities = [_parse_liability(s) for s in (args.liabilities or [])]
        rigid = [_parse_rigid(s) for s in (args.rigid or [])]
        # provided：手动录入也只标记「显式传参」的分类，confirm 仅覆盖这些（#1 修复）
        provided = {
            "corpus": args.corpus is not None,
            "monthly_contribution": args.monthly is not None,
            "liabilities": args.liabilities is not None,
            "rigid_annual_expenses": args.rigid is not None,
        }
        candidates = {
            "corpus": float(args.corpus),
            "monthly_contribution": float(args.monthly) if args.monthly is not None else 0.0,
            "liabilities": liabilities,
            "rigid_annual_expenses": rigid,
            "suspicious": [],
            "provided": provided,
            "summary": {
                "total_assets": float(args.corpus),
                "liabilities_count": len(liabilities),
                "rigid_count": len(rigid),
                "months_flow": 0,
            },
        }
    else:
        return _emit({"ok": False, "error": "invalid",
                      "message": "须提供 --balances <csv> 或 --corpus <X> 以发起导入"}, 4, args)

    result = mod_import.stage_import(
        contract, candidates, args.source or "manual", today=_today(args))
    if result.get("ok"):
        contract_io.write_contract(data_dir, contract, actor="configurator", confirm=True)
    return _emit(result, 0 if result.get("ok") else 1, args)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="self-trust",
        description="self-trust 自律记账引擎（确定性判定，LLM 只渲染不心算）")
    p.add_argument("--data-dir", default=None,
                   help="数据目录（优先级：本参数 > SELFTRUST_DATA_DIR > <home>/.claw/self-trust/）")
    p.add_argument("--json", action="store_true", default=True,
                   help="结构化 JSON 输出（默认格式）")
    p.add_argument("--text", action="store_true",
                   help="文本渲染输出（§0.5 骨架，带分隔线 + 时间戳）")
    p.add_argument("--today", default=None,
                   help="覆盖当前日期 YYYY-MM-DD（测试/重放用）")
    p.add_argument("--pass", dest="pass_", default=None,
                   help="加密契约密码（passphrase 模式）；亦可用环境变量 SELFTRUST_PASS")
    p.add_argument("--key-file", dest="key_file", default=None,
                   help="加密密钥文件路径（key-file 模式）；亦可用环境变量 SELFTRUST_KEY_FILE")
    sub = p.add_subparsers(dest="command", required=True)

    sp = sub.add_parser("init", help="懒人一键初始化（§7.1）")
    sp.add_argument("--corpus", type=float, required=True, help="资金池初始余额")
    sp.add_argument("--monthly", type=float, required=True,
                    help="月度净流入（净口径：税后收入-负债月供-刚性月摊）")
    sp.add_argument("--objective", action="append", required=True,
                    help='目标 "名称:目标额:期限"（1~3 个，可重复传）')
    sp.add_argument("--currency", default="CNY",
                    help="基准币种代码（默认 CNY；USD/EUR/GBP/HKD/JPY 等）")
    sp.add_argument("--encrypt", action="store_true",
                    help="启用静态加密（opt-in，默认关）；配合 --crypto-mode 选密钥路线")
    sp.add_argument("--crypto-mode", default="passphrase",
                    choices=["passphrase", "keyfile"],
                    help="加密密钥路线：passphrase（密码，每次 --pass）| keyfile（自动生成密钥文件）")
    sp.set_defaults(func=cmd_init)

    sp = sub.add_parser("judge", help="支取审批统一判定 + 冷静期生命周期（§4.4/§5.1）")
    sp.add_argument("--amount", type=float, default=None)
    sp.add_argument("--category", default=None)
    sp.add_argument("--planned", action="store_true", help="是否计划内")
    sp.add_argument("--action", default="submit",
                    choices=["submit", "withdraw", "finalize", "expire", "reminders"],
                    help="submit 提交审批 | withdraw 撤回 | finalize 确认执行 | "
                         "expire 到期终裁 | reminders 双阶段提醒数据")
    sp.add_argument("--request-id", default=None, help="冷静期申请 id")
    sp.add_argument("--financed-amount", type=float, default=0.0,
                    help="融资购房：贷款金额（>0 启用融资模式；首付=总额-本值）")
    sp.add_argument("--financed-term-years", type=float, default=None,
                    help="融资购房：贷款期限（年，默认 30）")
    sp.add_argument("--financed-rate", type=float, default=None,
                    help="融资购房：贷款年利率（默认 0.04）")
    sp.add_argument("--financed-monthly", type=float, default=None,
                    help="融资购房：已知月供（给定则跳过估算）")
    sp.add_argument("--currency", default="CNY",
                    help="消费币种代码（默认 CNY；非 CNY 须同时提供 --rate）")
    sp.add_argument("--rate", type=float, default=None,
                    help="汇率（消费币种→基准币种；如 USD→CNY 7.25）；非 CNY 时必填")
    sp.set_defaults(func=cmd_judge)

    sp = sub.add_parser("demo", help="三场景模拟演示（§7.2，干跑不落盘不影响真实账户）")
    sp.set_defaults(func=cmd_demo)

    sp = sub.add_parser("report", help="记账报表 + 月度快照（§6.1）")
    sp.set_defaults(func=cmd_report)

    sp = sub.add_parser("reconcile", help="hybrid 对账（§3.2，用户拍板修正）")
    sp.add_argument("--corpus", type=float, default=None, help="修正后的资金池余额")
    sp.add_argument("--income", type=float, default=None, help="当月实际注入实绩")
    sp.add_argument("--invest", type=float, default=None)
    sp.add_argument("--living", type=float, default=None)
    sp.add_argument("--impulse", type=float, default=None)
    sp.set_defaults(func=cmd_reconcile)

    sp = sub.add_parser("calibrate", help="月度校准（§6.2/§6.4）")
    sp.add_argument("--force", action="store_true", help="同月强制重跑")
    sp.set_defaults(func=cmd_calibrate)

    sp = sub.add_parser("reward", help="里程碑奖励（§6.3）")
    sp.add_argument("--action", default="status",
                    choices=["status", "unlock", "claim"])
    sp.add_argument("--objective", default=None)
    sp.add_argument("--amount", type=float, default=None)
    sp.add_argument("--purpose", default=None)
    sp.set_defaults(func=cmd_reward)

    sp = sub.add_parser("reset", help="记账重置（§7.1.1，二次确认+审计保留）")
    sp.add_argument("--confirm", action="store_true", help="二次确认（确认重置）")
    sp.add_argument("--corpus", type=float, default=None)
    sp.add_argument("--monthly", type=float, default=None)
    sp.add_argument("--objective", action="append", default=None)
    sp.add_argument("--reason", default=None)
    sp.set_defaults(func=cmd_reset)

    sp = sub.add_parser("appeal", help="申诉 / 人工覆写（§5.2）")
    sp.add_argument("--request-id", required=True)
    sp.add_argument("--reason", default=None)
    sp.add_argument("--override", action="store_true",
                    help="满 3 次申诉后的人工覆写")
    sp.add_argument("--confirm", action="store_true",
                    help="覆写确认（知悉目标延后时长）")
    sp.set_defaults(func=cmd_appeal)

    sp = sub.add_parser("objective", help="目标生命周期迁移（§6.4，用户显式确认）")
    sp.add_argument("--name", required=True)
    sp.add_argument("--to", required=True,
                     choices=[ObjectiveStatus.COMPLETED.value, ObjectiveStatus.ARCHIVED.value])
    sp.add_argument("--confirm", action="store_true")
    sp.set_defaults(func=cmd_objective)

    sp = sub.add_parser("log", help="审计留痕只读查询（§10.1）")
    sp.add_argument("--name", default="approval_log",
                    choices=sorted(audit_io.VALID_LOGS))
    sp.set_defaults(func=cmd_log)

    sp = sub.add_parser("import-asset", help="第三方资产导入（§7.3，CSV/手动 → 核对 → 确认生效）")
    sp.add_argument("--balances", default=None,
                    help="余额 CSV（name,balance,kind[,monthly]；kind∈asset/liability/rigid）")
    sp.add_argument("--flows", default=None,
                    help="流水 CSV（date,amount，可选，用于推算月均净流入）")
    sp.add_argument("--corpus", type=float, default=None,
                    help="手动录入总资产（替代 CSV；或 confirm 时修正候选）")
    sp.add_argument("--monthly", type=float, default=None,
                    help="月度净流入（手动录入或 confirm 时修正候选）")
    sp.add_argument("--liabilities", action="append", default=None,
                    help="负债 名称:余额[:月供[:年利率]]（手动录入或 confirm 时修正）")
    sp.add_argument("--rigid", action="append", default=None,
                    help="刚性年支出 名称:金额[:due_month]（手动录入或 confirm 时修正）")
    sp.add_argument("--source", default=None,
                    help="数据源名称（随手记/钱迹/custom-csv…，仅作标记）")
    sp.add_argument("--confirm", action="store_true",
                    help="核对确认：带 --token 将候选落到资产池（imported_confirmed）")
    sp.add_argument("--cancel", action="store_true",
                    help="放弃导入：带 --token 还原 corpus_status 并清 staging")
    sp.add_argument("--token", default=None, help="stage 返回的确认 token")
    sp.set_defaults(func=cmd_import_asset)

    sp = sub.add_parser("customize", help="记账自定义：增量覆盖契约配置区参数（§5.4 二次确认）")
    sp.add_argument("--set", action="append", default=None,
                    help="设置嵌套字段 DOTPATH=VALUE（如 distribution_rules.invest_ratio=0.3、"
                         "safety_cushion.months=4、optimization_goal=wealth、mode=ledger），可重复")
    sp.add_argument("--add-objective", action="append", default=None,
                    help='新增目标 "名称:目标额:期限"（如 买房:1000000:2030-01-01），可重复')
    sp.add_argument("--whitelist-add", default=None, help="新增极速审批类目 名称")
    sp.add_argument("--per-tx-cap", type=float, default=None,
                    help="白名单单笔上限（须与 --whitelist-add 同传）")
    sp.add_argument("--annual-cap", type=float, default=None,
                    help="白名单年上限（须与 --whitelist-add 同传）")
    sp.add_argument("--whitelist-remove", default=None, help="移除极速审批类目 名称")
    sp.add_argument("--add-liability", action="append", default=None,
                    help="新增负债 名称:余额[:月供[:年利率]]")
    sp.add_argument("--remove-liability", action="append", default=None,
                    help="移除负债 名称")
    sp.add_argument("--add-rigid", action="append", default=None,
                    help="新增刚性年支出 名称:金额[:due_month]")
    sp.add_argument("--remove-rigid", action="append", default=None,
                    help="移除刚性年支出 名称")
    sp.add_argument("--add-category", action="append", default=None,
                    help="新增支出类目词汇（allowed_categories，嵌套于 distribution_rules），"
                         "可重复；去重追加，不修改 invest_ratio 故不触发冷却窗")
    sp.add_argument("--remove-category", action="append", default=None,
                    help="移除支出类目词汇 名称（不存在则报错）")
    sp.add_argument("--record-home-purchase", action="append", default=None,
                    help="记录已购房产（首付+房贷落账）房价:首付比例[:期限年[:利率]]")
    sp.add_argument("--review", action="store_true",
                    help="冷却窗复查：懒惰扫描过期项自动生效，列出窗内待决修改 + 二次提醒")
    sp.add_argument("--withdraw", action="store_true",
                    help="冷却窗撤回：须同时带 --request-id 与 --token（撤回 token）")
    sp.add_argument("--request-id", default=None, help="冷却窗修改 id（复查/撤回用）")
    sp.add_argument("--confirm", action="store_true",
                    help="二次确认（须同时带预览返回的 --token 才落盘）")
    sp.add_argument("--token", default=None,
                    help="预览返回的确认 token（防漂移）；或 --withdraw 时的撤回 token")
    sp.add_argument("--reason", default=None, help="自定义原因（写入 override_log）")
    sp.set_defaults(func=cmd_customize)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        # _configure_crypto 会读契约探 crypto.enabled，损坏契约须在此被守卫捕获
        _configure_crypto(args)
        return args.func(args)
    except FileNotFoundError as e:
        return _emit({"ok": False, "error": "not_found", "message": str(e)}, 2, args)
    except GuardError as e:
        return _emit({"ok": False, "error": "guard", "message": str(e)}, 3, args)
    except crypto_io.CryptoError as e:
        return _emit({"ok": False, "error": "crypto", "message": str(e)}, 5, args)
    except ContractCorruptedError as e:
        # 契约损坏（拼接/截断 JSON）：清晰指向 .bak.corrupt 恢复，不与 crypto 混淆
        return _emit({"ok": False, "error": "contract_corrupted",
                      "message": str(e), "recover": str(e.path) + ".bak.corrupt"}, 6, args)
    except (ValueError, TypeError) as e:
        return _emit({"ok": False, "error": "invalid", "message": str(e)}, 4, args)


if __name__ == "__main__":
    raise SystemExit(main())
