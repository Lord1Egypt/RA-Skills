#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
risk_manager.py — 风险管理引擎

实现 7 条核心风控规则,每条规则返回 RiskAlert 对象(level / message / action),
并提供综合检查函数 run_all_checks(portfolio, market_data)。

风控规则:
    1. check_single_stop_loss          单只持仓止损
    2. check_portfolio_stop_loss        组合止损
    3. check_position_concentration     单一持仓集中度
    4. check_industry_concentration     行业集中度
    5. check_sentiment_extreme          情绪极端
    6. check_consecutive_losses         连续亏损
    7. check_leverage_intent            杠杆意图(拒绝)

用法:
    from risk_manager import run_all_checks
    alerts = run_all_checks(portfolio, market_data)
    for a in alerts:
        print(a.level, a.message, a.action)

依赖: 仅使用 Python 标准库,无第三方依赖。
"""

from __future__ import annotations

import os
import json
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Dict, List, Optional, Sequence


# =============================================================================
# 数据结构定义
# =============================================================================

class AlertLevel(Enum):
    """风控告警级别。"""

    INFO = "info"        # 提示
    WARNING = "warning"  # 警告
    DANGER = "danger"    # 危险(建议减仓)
    BLOCK = "block"      # 阻断(拒绝交易)


class AlertAction(Enum):
    """风控建议动作。"""

    NONE = "none"                # 无动作
    MONITOR = "monitor"          # 持续监控
    REDUCE_POSITION = "reduce"   # 减仓
    STOP_LOSS = "stop_loss"      # 止损清仓
    REJECT_ORDER = "reject"      # 拒绝下单


@dataclass
class RiskAlert:
    """风控告警对象。

    Attributes:
        rule:        触发的规则名称。
        level:       告警级别(AlertLevel)。
        message:     人类可读的告警信息。
        action:      建议动作(AlertAction)。
        details:     额外上下文数据(指标值、阈值等)。
        stock_code:  相关标的代码(可选)。
    """

    rule: str
    level: AlertLevel
    message: str
    action: AlertAction = AlertAction.NONE
    details: Dict[str, Any] = field(default_factory=dict)
    stock_code: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """转换为可序列化字典(便于写入报告/JSON)。"""

        return {
            "rule": self.rule,
            "level": self.level.value,
            "message": self.message,
            "action": self.action.value,
            "details": self.details,
            "stock_code": self.stock_code,
        }


@dataclass
class Position:
    """单只持仓。

    Attributes:
        stock_code:   股票代码,如 "600519"。
        name:         股票名称。
        cost_price:   持仓成本价。
        current_price:当前价。
        volume:       持仓数量(股)。
        industry:     所属行业。
        pnl_pct:      浮动盈亏比例(如 -0.05 表示 -5%)。
    """

    stock_code: str
    name: str = ""
    cost_price: float = 0.0
    current_price: float = 0.0
    volume: int = 0
    industry: str = ""
    pnl_pct: float = 0.0

    @property
    def market_value(self) -> float:
        """当前市值。"""

        return self.current_price * self.volume

    @property
    def cost_value(self) -> float:
        """成本市值。"""

        return self.cost_price * self.volume


@dataclass
class Order:
    """交易订单(用于杠杆意图检查)。

    Attributes:
        stock_code:  标的代码。
        side:        买卖方向 buy/sell。
        volume:      数量。
        price:       价格。
        order_type:  订单类型(normal/margin/financing/futures/options)。
        leverage:    杠杆倍数(1 表示无杠杆)。
    """

    stock_code: str
    side: str = "buy"
    volume: int = 0
    price: float = 0.0
    order_type: str = "normal"
    leverage: float = 1.0


# =============================================================================
# 风控规则实现(7 条)
# =============================================================================

def check_single_stop_loss(
    position: Position,
    threshold: float = -0.05,
) -> Optional[RiskAlert]:
    """规则 1: 单只持仓止损。

    当单只持仓的浮动盈亏比例跌破阈值时触发告警。

    Args:
        position:  持仓对象。
        threshold: 止损阈值(负数,默认 -0.05 即 -5%)。

    Returns:
        触发时返回 RiskAlert,否则返回 None。
    """

    pnl = position.pnl_pct
    if pnl <= threshold:
        # 跌破阈值越深,级别越高
        if pnl <= threshold * 2:
            level = AlertLevel.DANGER
            action = AlertAction.STOP_LOSS
        else:
            level = AlertLevel.WARNING
            action = AlertAction.REDUCE_POSITION
        return RiskAlert(
            rule="single_stop_loss",
            level=level,
            message=(
                f"标的 {position.stock_code}({position.name})浮亏 "
                f"{pnl:.2%},已跌破单只止损阈值 {threshold:.2%}"
            ),
            action=action,
            details={"pnl_pct": pnl, "threshold": threshold},
            stock_code=position.stock_code,
        )
    return None


def check_portfolio_stop_loss(
    portfolio: Sequence[Position],
    threshold: float = -0.08,
) -> Optional[RiskAlert]:
    """规则 2: 组合止损。

    当整个组合的综合浮亏比例跌破阈值时触发。

    Args:
        portfolio: 持仓列表。
        threshold: 组合止损阈值(负数,默认 -0.08 即 -8%)。

    Returns:
        触发时返回 RiskAlert,否则返回 None。
    """

    total_cost = sum(p.cost_value for p in portfolio)
    total_value = sum(p.market_value for p in portfolio)
    if total_cost <= 0:
        return None
    portfolio_pnl = (total_value - total_cost) / total_cost
    if portfolio_pnl <= threshold:
        level = AlertLevel.DANGER if portfolio_pnl <= threshold * 1.5 else AlertLevel.WARNING
        action = AlertAction.STOP_LOSS if portfolio_pnl <= threshold * 1.5 else AlertAction.REDUCE_POSITION
        return RiskAlert(
            rule="portfolio_stop_loss",
            level=level,
            message=(
                f"组合综合浮亏 {portfolio_pnl:.2%},已跌破组合止损阈值 {threshold:.2%}"
            ),
            action=action,
            details={
                "portfolio_pnl_pct": portfolio_pnl,
                "threshold": threshold,
                "total_cost": total_cost,
                "total_value": total_value,
            },
        )
    return None


def check_position_concentration(
    position: Position,
    portfolio: Sequence[Position],
    max_pct: float = 0.30,
) -> Optional[RiskAlert]:
    """规则 3: 单一持仓集中度。

    当单只持仓市值占组合总市值比例超过上限时触发。

    Args:
        position:  待检查的持仓。
        portfolio: 整个组合。
        max_pct:   集中度上限(默认 0.30 即 30%)。

    Returns:
        触发时返回 RiskAlert,否则返回 None。
    """

    total_value = sum(p.market_value for p in portfolio)
    if total_value <= 0:
        return None
    pct = position.market_value / total_value
    if pct > max_pct:
        level = AlertLevel.DANGER if pct > max_pct * 1.5 else AlertLevel.WARNING
        return RiskAlert(
            rule="position_concentration",
            level=level,
            message=(
                f"标的 {position.stock_code} 占组合 {pct:.2%},"
                f"超过单一持仓集中度上限 {max_pct:.2%}"
            ),
            action=AlertAction.REDUCE_POSITION,
            details={"concentration_pct": pct, "max_pct": max_pct},
            stock_code=position.stock_code,
        )
    return None


def check_industry_concentration(
    portfolio: Sequence[Position],
    max_pct: float = 0.40,
) -> Optional[RiskAlert]:
    """规则 4: 行业集中度。

    当单一行业的市值占组合总市值比例超过上限时触发。

    Args:
        portfolio: 整个组合。
        max_pct:   行业集中度上限(默认 0.40 即 40%)。

    Returns:
        触发时返回 RiskAlert,否则返回 None。
    """

    total_value = sum(p.market_value for p in portfolio)
    if total_value <= 0:
        return None
    industry_value: Dict[str, float] = {}
    for p in portfolio:
        key = p.industry or "未知"
        industry_value[key] = industry_value.get(key, 0.0) + p.market_value
    # 找出占比最高的行业
    top_industry, top_value = max(industry_value.items(), key=lambda x: x[1])
    top_pct = top_value / total_value
    if top_pct > max_pct:
        level = AlertLevel.DANGER if top_pct > max_pct * 1.25 else AlertLevel.WARNING
        return RiskAlert(
            rule="industry_concentration",
            level=level,
            message=(
                f"行业 [{top_industry}] 占组合 {top_pct:.2%},"
                f"超过行业集中度上限 {max_pct:.2%}"
            ),
            action=AlertAction.REDUCE_POSITION,
            details={
                "industry": top_industry,
                "concentration_pct": top_pct,
                "max_pct": max_pct,
            },
        )
    return None


def check_sentiment_extreme(
    sentiment_score: float,
    high: float = 90.0,
    low: float = 10.0,
) -> Optional[RiskAlert]:
    """规则 5: 情绪极端。

    当市场情绪指标过高(过热)或过低(过冷)时触发。

    Args:
        sentiment_score: 情绪分数(0-100)。
        high:            过热阈值(默认 90)。
        low:             过冷阈值(默认 10)。

    Returns:
        触发时返回 RiskAlert,否则返回 None。
    """

    if sentiment_score >= high:
        return RiskAlert(
            rule="sentiment_extreme",
            level=AlertLevel.WARNING,
            message=(
                f"市场情绪过热(分数 {sentiment_score:.1f} >= {high}),"
                f"注意追高风险"
            ),
            action=AlertAction.MONITOR,
            details={"sentiment_score": sentiment_score, "type": "overheated"},
        )
    if sentiment_score <= low:
        return RiskAlert(
            rule="sentiment_extreme",
            level=AlertLevel.WARNING,
            message=(
                f"市场情绪过冷(分数 {sentiment_score:.1f} <= {low}),"
                f"注意恐慌蔓延风险"
            ),
            action=AlertAction.MONITOR,
            details={"sentiment_score": sentiment_score, "type": "panicked"},
        )
    return None


def check_consecutive_losses(
    trade_history: Sequence[Dict[str, Any]],
    max_count: int = 3,
) -> Optional[RiskAlert]:
    """规则 6: 连续亏损。

    当最近交易记录中出现连续亏损达到上限时触发,建议暂停交易冷静。

    Args:
        trade_history: 交易记录列表,每条至少包含 "pnl"(盈亏)字段,
                       按时间正序排列(最旧在前)。
        max_count:     连续亏损最大允许次数(默认 3)。

    Returns:
        触发时返回 RiskAlert,否则返回 None。
    """

    if not trade_history:
        return None
    # 从最近一笔往回数连续亏损
    consecutive = 0
    for trade in reversed(trade_history):
        pnl = trade.get("pnl", 0)
        if pnl is None:
            break
        if float(pnl) < 0:
            consecutive += 1
        else:
            break
    if consecutive >= max_count:
        return RiskAlert(
            rule="consecutive_losses",
            level=AlertLevel.DANGER,
            message=(
                f"最近 {consecutive} 笔交易连续亏损,"
                f"达到上限 {max_count},建议暂停交易冷静"
            ),
            action=AlertAction.REJECT_ORDER,
            details={"consecutive_losses": consecutive, "max_count": max_count},
        )
    return None


def check_leverage_intent(order: Order) -> Optional[RiskAlert]:
    """规则 7: 杠杆意图(拒绝)。

    当订单包含融资融券、期货、期权或杠杆倍数 > 1 时,直接拒绝。

    Args:
        order: 交易订单。

    Returns:
        触发时返回 RiskAlert(BLOCK 级别),否则返回 None。
    """

    leverage_types = {"margin", "financing", "futures", "options"}
    if order.order_type in leverage_types or order.leverage > 1.0:
        return RiskAlert(
            rule="leverage_intent",
            level=AlertLevel.BLOCK,
            message=(
                f"订单 {order.stock_code} 含杠杆意图"
                f"(类型={order.order_type}, 倍数={order.leverage}x),"
                f"已拒绝下单"
            ),
            action=AlertAction.REJECT_ORDER,
            details={
                "order_type": order.order_type,
                "leverage": order.leverage,
            },
            stock_code=order.stock_code,
        )
    return None


# =============================================================================
# 综合检查
# =============================================================================

def run_all_checks(
    portfolio: Sequence[Position],
    market_data: Optional[Dict[str, Any]] = None,
    trade_history: Optional[Sequence[Dict[str, Any]]] = None,
    pending_order: Optional[Order] = None,
    sentiment_score: Optional[float] = None,
    single_stop_threshold: float = -0.05,
    portfolio_stop_threshold: float = -0.08,
    position_max_pct: float = 0.30,
    industry_max_pct: float = 0.40,
    sentiment_high: float = 90.0,
    sentiment_low: float = 10.0,
    max_consecutive_losses: int = 3,
) -> List[RiskAlert]:
    """综合风控检查:依次执行 7 条规则并汇总所有告警。

    Args:
        portfolio:                持仓列表。
        market_data:              市场数据(预留,用于扩展)。
        trade_history:            交易历史(用于连续亏损检查)。
        pending_order:            待执行订单(用于杠杆意图检查)。
        sentiment_score:          市场情绪分数(0-100)。
        single_stop_threshold:    单只止损阈值。
        portfolio_stop_threshold: 组合止损阈值。
        position_max_pct:         单一持仓集中度上限。
        industry_max_pct:         行业集中度上限。
        sentiment_high:           情绪过热阈值。
        sentiment_low:            情绪过冷阈值。
        max_consecutive_losses:   连续亏损上限。

    Returns:
        所有触发的 RiskAlert 列表(按级别从高到低排序)。
    """

    alerts: List[RiskAlert] = []
    market_data = market_data or {}

    # 规则 1: 单只止损
    for pos in portfolio:
        alert = check_single_stop_loss(pos, threshold=single_stop_threshold)
        if alert:
            alerts.append(alert)

    # 规则 2: 组合止损
    alert = check_portfolio_stop_loss(portfolio, threshold=portfolio_stop_threshold)
    if alert:
        alerts.append(alert)

    # 规则 3: 单一持仓集中度
    for pos in portfolio:
        alert = check_position_concentration(pos, portfolio, max_pct=position_max_pct)
        if alert:
            alerts.append(alert)

    # 规则 4: 行业集中度
    alert = check_industry_concentration(portfolio, max_pct=industry_max_pct)
    if alert:
        alerts.append(alert)

    # 规则 5: 情绪极端
    if sentiment_score is not None:
        alert = check_sentiment_extreme(
            sentiment_score, high=sentiment_high, low=sentiment_low
        )
        if alert:
            alerts.append(alert)

    # 规则 6: 连续亏损
    if trade_history:
        alert = check_consecutive_losses(trade_history, max_count=max_consecutive_losses)
        if alert:
            alerts.append(alert)

    # 规则 7: 杠杆意图
    if pending_order is not None:
        alert = check_leverage_intent(pending_order)
        if alert:
            alerts.append(alert)

    # 按级别排序: BLOCK > DANGER > WARNING > INFO
    level_order = {
        AlertLevel.BLOCK: 0,
        AlertLevel.DANGER: 1,
        AlertLevel.WARNING: 2,
        AlertLevel.INFO: 3,
    }
    alerts.sort(key=lambda a: level_order.get(a.level, 99))
    return alerts


# =============================================================================
# 报告输出
# =============================================================================

def summarize_alerts(alerts: Sequence[RiskAlert]) -> str:
    """将告警列表汇总为可读的多行字符串(用于报告)。"""

    if not alerts:
        return "风控检查通过,无告警。"
    lines = [f"共触发 {len(alerts)} 条风控告警:"]
    for i, a in enumerate(alerts, 1):
        lines.append(
            f"  {i}. [{a.level.value.upper()}] {a.rule} -> {a.message} "
            f"(建议: {a.action.value})"
        )
    return "\n".join(lines)


def save_alerts(alerts: Sequence[RiskAlert], path: str) -> None:
    """将告警列表以 JSON 形式写入文件。"""

    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    payload = [a.to_dict() for a in alerts]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


# =============================================================================
# 自测入口
# =============================================================================

def _demo() -> None:
    """演示用例:构造一个有问题的组合,运行全部风控检查。"""

    portfolio = [
        Position(
            stock_code="600519", name="贵州茅台",
            cost_price=1800.0, current_price=1600.0,
            volume=100, industry="白酒", pnl_pct=-0.111,
        ),
        Position(
            stock_code="000858", name="五粮液",
            cost_price=200.0, current_price=190.0,
            volume=2000, industry="白酒", pnl_pct=-0.05,
        ),
    ]
    trade_history = [
        {"pnl": -100}, {"pnl": -200}, {"pnl": -50}, {"pnl": 80}, {"pnl": -30},
    ]
    pending = Order(stock_code="600519", order_type="margin", leverage=2.0)

    alerts = run_all_checks(
        portfolio=portfolio,
        trade_history=trade_history,
        pending_order=pending,
        sentiment_score=92.0,
    )
    print(summarize_alerts(alerts))


if __name__ == "__main__":
    _demo()
