#!/usr/bin/env python3
"""
同花顺持仓监控脚本
根据 monitor_config.json 中的阈值配置，检查持仓风险项并输出报警信息

用法:
    python monitor.py              # 运行一次监控检查
    python monitor.py --dry-run   # 仅显示会触发但不复写状态
"""

import sys
import json
import os
import argparse
from pathlib import Path
from datetime import datetime, timedelta

# ============ 路径配置 ============
SKILL_DIR = Path(__file__).parent.parent
MEMORY_DIR = SKILL_DIR / "memory"
DATA_DIR = SKILL_DIR / "data"

# ============ 工具函数 ============
def _to_float(v, default=0.0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def _to_int(v, default=0):
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def _load_json(path: Path, default=None):
    if path.exists():
        try:
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return default if default is not None else {}


def _save_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ============ 加载数据 ============
def load_positions():
    """从缓存加载持仓数据"""
    cache = DATA_DIR / "positions.json"
    if not cache.exists():
        return None
    try:
        data = json.loads(cache.read_text(encoding="utf-8"))
        # 尝试新版格式
        if "positions" in data:
            return data["positions"]
        return data.get("positions")
    except Exception:
        return None


def load_monitor_state() -> dict:
    return _load_json(MEMORY_DIR / "monitor_state.json", {})


def save_monitor_state(state: dict):
    _save_json(MEMORY_DIR / "monitor_state.json", state)


# ============ 监控检查 ============
def check_alerts(positions_data: dict, monitor_config: dict, state: dict, dry_run: bool = False) -> list[dict]:
    """
    检查所有监控条件，返回触发的告警列表
    """
    alerts_triggered = []

    if not positions_data.get("ok"):
        return [{"level": "error", "name": "数据获取失败", "message": positions_data.get("error", "未知错误")}]

    data = positions_data.get("data", {})
    overview = data.get("overview", {})
    items = data.get("items", [])

    total_asset = _to_float(overview.get("total_asset"))
    total_value = _to_float(overview.get("total_value"))
    total_position_rate = (total_value / total_asset * 100) if total_asset else 0

    # 当前时间
    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")

    monitor_alerts = monitor_config.get("alerts", [])

    for alert_cfg in monitor_alerts:
        alert_name = alert_cfg["name"]
        condition = alert_cfg["condition"]
        threshold = alert_cfg.get("threshold", 0)
        message_template = alert_cfg.get("message", "")
        cooldown_hours = alert_cfg.get("cooldown_hours", 24)

        # 检查冷却期
        if not dry_run:
            if alert_name in state:
                last_triggered = state[alert_name].get("last_triggered")
                if last_triggered:
                    last_time = datetime.fromisoformat(last_triggered)
                    if now - last_time < timedelta(hours=cooldown_hours):
                        continue  # 在冷却期内

        triggered = False
        details = []

        if condition == "position_rate_above":
            # 单股仓位超过 X%
            for pos in items:
                rate = _to_float(pos.get("position_rate"))
                if rate > threshold:
                    triggered = True
                    details.append(f"{pos.get('stock_name','')}({pos.get('stock_code','')}) 仓位 {rate:.1f}%")

        elif condition == "profit_rate_below":
            # 单股亏损率超过 X%（成本为基准）
            for pos in items:
                cost = _to_float(pos.get("cost_price"))
                current = _to_float(pos.get("current_price"))
                if cost > 0:
                    rate = (current - cost) / cost * 100
                    if rate < threshold:
                        triggered = True
                        details.append(
                            f"{pos.get('stock_name','')}({pos.get('stock_code','')}) 收益率 {rate:.1f}%"
                        )

        elif condition == "hold_days_above":
            # 持仓天数超过 X 天
            for pos in items:
                days = _to_int(pos.get("hold_days"))
                if days > threshold:
                    triggered = True
                    details.append(f"{pos.get('stock_name','')}({pos.get('stock_code','')}) 持仓 {days} 天")

        elif condition == "total_position_above":
            # 总仓位超过 X%
            if total_position_rate > threshold:
                triggered = True
                details.append(f"总仓位 {total_position_rate:.1f}%（阈值 {threshold}%）")

        elif condition == "daily_loss_above":
            # 单日亏损超过 X%（需要今日行情，暂用持仓盈亏代替）
            for pos in items:
                hold_profit = _to_float(pos.get("hold_profit"))
                mv = _to_float(pos.get("market_value"))
                if mv > 0:
                    # 用持仓盈亏率估算
                    cost_total = _to_float(pos.get("cost_price")) * _to_int(pos.get("hold_count"))
                    if cost_total > 0:
                        rate = hold_profit / cost_total * 100
                        if rate < -threshold:
                            triggered = True
                            details.append(
                                f"{pos.get('stock_name','')}({pos.get('stock_code','')}) 亏损 {rate:.1f}%"
                            )

        if triggered:
            msg = message_template
            if details:
                msg += "\n   " + " | ".join(details[:5])  # 最多显示5条详情
            alert_record = {
                "name": alert_name,
                "message": msg,
                "triggered_at": now.isoformat(),
                "details": details,
                "level": "warning",
            }
            alerts_triggered.append(alert_record)

            # 更新状态
            if not dry_run:
                state[alert_name] = {
                    "last_triggered": now.isoformat(),
                    "trigger_count": state.get(alert_name, {}).get("trigger_count", 0) + 1,
                    "last_message": msg,
                }

    return alerts_triggered


# ============ 报告格式化 ============
def format_alerts(alerts: list[dict], positions_data: dict = None) -> str:
    lines = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines.append("=" * 52)
    lines.append(f"   持仓监控报告  {now}")
    lines.append("=" * 52)

    if positions_data and positions_data.get("ok"):
        data = positions_data.get("data", {})
        overview = data.get("overview", {})
        items = data.get("items", [])
        total_asset = _to_float(overview.get("total_asset"))
        total_value = _to_float(overview.get("total_value"))
        position_rate = (total_value / total_asset * 100) if total_asset else 0
        lines.append(f"\n📊 当前持仓：{len(items)} 只  总资产 {total_asset:,.2f} 元  仓位 {position_rate:.1f}%")

    if not alerts:
        lines.append("\n✅ 暂无触发阈值的风险项，持仓状态正常。")
    else:
        lines.append(f"\n⚠️ 共触发 {len(alerts)} 项风险监控：")
        for i, alert in enumerate(alerts, 1):
            level_icon = "🔴" if alert.get("level") == "error" else "⚠️"
            lines.append(f"\n{level_icon} [{i}] {alert['name']}")
            lines.append(f"   {alert['message']}")
            if alert.get("triggered_at"):
                lines.append(f"   触发时间：{alert['triggered_at'][:16]}")

    lines.append("\n" + "=" * 52)
    lines.append("  仅供参考，不构成投资建议")
    lines.append("=" * 52)
    return "\n".join(lines)


# ============ 主入口 ============
def run_monitor(dry_run: bool = False):
    """执行监控检查"""
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

    monitor_config = _load_json(MEMORY_DIR / "monitor_config.json", {"enabled": True, "alerts": []})
    if not monitor_config.get("enabled", True):
        print("监控未启用（monitor_config.json 中 enabled=false）")
        return

    print("正在加载持仓数据...", flush=True)
    positions = load_positions()
    if not positions or not positions.get("ok"):
        print("无法加载持仓数据，请先运行：python -m uv run scripts/analyze.py positions")
        print("(或 python -m uv run scripts/analyze.py analyze 会自动获取并缓存持仓数据)")
        sys.exit(1)

    state = {} if dry_run else load_monitor_state()

    print("正在检查监控阈值...", flush=True)
    alerts = check_alerts(positions, monitor_config, state, dry_run=dry_run)

    if not dry_run:
        save_monitor_state(state)

    report = format_alerts(alerts, positions)
    print(report)


def main():
    parser = argparse.ArgumentParser(description="同花顺持仓监控")
    parser.add_argument("--dry-run", action="store_true", help="仅显示会触发的告警，不写入状态")
    args = parser.parse_args()
    run_monitor(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
