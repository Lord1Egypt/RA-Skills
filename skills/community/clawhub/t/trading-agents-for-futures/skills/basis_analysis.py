"""基差分析 Skill

封装基差与期现关系指标计算和规则驱动的基差分析。
纯本地计算，不依赖任何外部模块。
"""

from __future__ import annotations

from typing import Dict, Any, Optional
import datetime as _dt

from core.core_engine import AnalysisResult


def run(
    symbol: str,
    basis_data: Optional[Dict[str, Any]] = None,
    spot_price: Optional[float] = None,
    futures_price: Optional[float] = None,
    config: Optional[Dict[str, Any]] = None,
    **kwargs,
) -> AnalysisResult:
    """执行基差分析"""
    import pandas as pd
    import numpy as np

    result = AnalysisResult(skill_name="basis_analysis")

    try:
        indicators = {}

        # 处理基差时序数据
        if basis_data is not None:
            df = pd.DataFrame(basis_data)
            if "basis" in df.columns or "基差" in df.columns:
                df = df.rename(columns={"基差": "basis"})

            if "basis" in df.columns:
                basis_series = df["basis"].dropna().astype(float)
                if len(basis_series) >= 2:
                    indicators["latest_basis"] = float(basis_series.iloc[-1])
                    indicators["data_points"] = len(basis_series)
                    if len(basis_series) >= 20:
                        # ==================== 季节性 Z-score（核心修复）====================
                        # 问题：20天滚动Z-score会跨季节比较不同季节数据，导致失真
                        # 修复：强制优先同月份比较，同月数据不足时回退到60天滚动窗口
                        seasonal_mean = None
                        seasonal_std = None
                        seasonal_count = 0
                        curr_month = None
                        date_col = None
                        for col_name in df.columns:
                            col_lower = str(col_name).lower()
                            if any(k in col_lower for k in ("日期", "时间", "date", "time")):
                                date_col = col_name
                                break
                        if date_col:
                            try:
                                _dates = pd.to_datetime(df[date_col], errors="coerce")
                                latest_date = _dates.iloc[-1]
                                if pd.notna(latest_date):
                                    curr_month = latest_date.month
                                    same_mask = _dates.dt.month == curr_month
                                    same_month_vals = df.loc[same_mask, "basis"].dropna().astype(float)
                                    seasonal_count = len(same_month_vals)
                                    if seasonal_count >= 3:
                                        seasonal_mean = same_month_vals.mean()
                                        seasonal_std = same_month_vals.std()
                            except Exception:
                                pass
                        if seasonal_mean is not None and seasonal_std and seasonal_std > 0:
                            mean = seasonal_mean
                            std = seasonal_std
                            indicators["zscore_method"] = f"seasonal_M{curr_month}({seasonal_count}pts)"
                        else:
                            lookback = min(60, len(basis_series))
                            mean = basis_series.iloc[-lookback:].mean()
                            std = basis_series.iloc[-lookback:].std()
                            indicators["zscore_method"] = f"rolling_{lookback}d"
                        indicators["basis_zscore"] = round((basis_series.iloc[-1] - mean) / std, 2) if std and std > 0 else 0
                        indicators["basis_slope_20d"] = round(basis_series.iloc[-1] - basis_series.iloc[-20], 2)
                        if seasonal_mean is not None and seasonal_std and seasonal_std > 0:
                            rolling_mean_60 = basis_series.iloc[-60:].mean()
                            rolling_std_60 = basis_series.iloc[-60:].std()
                            if rolling_std_60 and rolling_std_60 > 0:
                                indicators["zscore_rolling_60d"] = round((basis_series.iloc[-1] - rolling_mean_60) / rolling_std_60,2)

        # 现货和期货价格 → 直接计算基差
        if spot_price is not None and futures_price is not None:
            current_basis = futures_price - spot_price
            basis_pct = (current_basis / spot_price) * 100
            indicators["spot_price"] = spot_price
            indicators["futures_price"] = futures_price
            indicators["current_basis"] = current_basis
            indicators["basis_pct"] = basis_pct

            if current_basis > 0:
                indicators["structure"] = "contango"
            elif current_basis < 0:
                indicators["structure"] = "backwardation"
            else:
                indicators["structure"] = "flat"

        result.add_data("indicators", indicators)
        if not indicators:
            indicators["soft_data_hint"] = (
                f"API 未返回 {symbol} 基差数据。请 AI Agent 搜索补全："
                f"'{symbol} 现货价格 {_dt.datetime.now().strftime('%Y年%m月')}'"
            )
            indicators["search_actions"] = [
                {"query": f"{symbol} 现货价格 基差 升贴水 {_dt.datetime.now().strftime('%Y年%m月')}", "source": "web", "priority": "high"},
                {"query": f"100ppi.com {symbol} 现货 价格", "source": "100ppi", "priority": "medium"},
            ]
        if basis_data and isinstance(basis_data, dict) and "日期" in basis_data:
            dates = [d for d in basis_data.get("日期", []) if d]
            if dates:
                result.add_data("data_date", str(dates[-1]))

        signal = _rule_based_basis_signal(indicators)
        result.add_data("rule_based_signal", signal)
        result.set_signal(signal.get("direction", "neutral"), signal.get("confidence", 0.3))
        result.bullets.extend(signal.get("signals", []) + signal.get("details", []))

    except Exception as e:
        result.add_error(f"基差分析出错: {e}")

    return result


def _rule_based_basis_signal(indicators: Dict[str, Any]) -> Dict[str, Any]:
    score = 0
    signals = []
    details = []

    basis_pct = indicators.get("basis_pct")
    zscore = indicators.get("basis_zscore")
    slope = indicators.get("basis_slope_20d")
    structure = indicators.get("structure")
    zscore_method = indicators.get("zscore_method", "unknown")

    if basis_pct is not None:
        if basis_pct > 5:
            score -= 1
            details.append(f"[基差] 期货大幅升水({basis_pct:.1f}%)，现货供应充裕")
        elif basis_pct < -5:
            score += 1
            details.append(f"[基差] 期货大幅贴水({basis_pct:.1f}%)，现货偏紧")
        elif -2 <= basis_pct <= 2:
            details.append(f"[基差] 基差合理({basis_pct:.1f}%)，期现趋于收敛")
        else:
            details.append(f"[基差] 基差{basis_pct:.1f}%")

    if zscore is not None:
        zscore_tag = f"{zscore_method}" if zscore_method != "unknown" else ""
        if zscore > 2:
            score -= 1
            signals.append(f"基差处于历史高位(Z={zscore:.1f}, {zscore_tag})")
            details.append(f"[历史] 基差处于历史高位(Z={zscore:.1f}, {zscore_tag})，均值回归压力向下")
        elif zscore < -2:
            score += 1
            signals.append(f"基差处于历史低位(Z={zscore:.1f}, {zscore_tag})")
            details.append(f"[历史] 基差处于历史低位(Z={zscore:.1f}, {zscore_tag})，均值回归向上")
        elif zscore > 1.5:
            details.append(f"[历史] 基差偏高(Z={zscore:.1f}, {zscore_tag})，处于历史偏高位置，均值回归概率上升")
        elif zscore < -1.5:
            details.append(f"[历史] 基差偏低(Z={zscore:.1f}, {zscore_tag})，处于历史偏低位置，均值回归概率上升")

    if slope is not None:
        if slope > 0:
            details.append("[趋势] 基差走强，现货相对走强")
        else:
            details.append("[趋势] 基差走弱，期货相对走强")

    if structure == "backwardation":
        score += 1
        signals.append("现货升水结构")
        details.append("[结构] 现货升水(Backwardation)，对多头有利")
    elif structure == "contango":
        score -= 1
        signals.append("期货升水结构")
        details.append("[结构] 期货升水(Contango)，对空头有利")

    # 交叉验证：斜率与结构矛盾时降信降权
    if structure and slope is not None:
        slope_dir = "strengthening_backwardation" if slope < 0 else "weakening_backwardation"
        if structure == "backwardation" and slope > 0:
            details.append(f"[交叉验证] 结构backwardation但基差斜率+{slope:.1f}(走弱)，现货紧张在缓解，方向信号需打折")
            score *= 0.5
        elif structure == "contango" and slope < 0:
            details.append(f"[交叉验证] 结构contango但基差斜率{slope:.1f}(走强)，现货在走强，结构信号不可靠")
            score *= 0.5

    if score > 0:
        direction = "bullish"
        confidence = min(0.6, 0.4 + score * 0.1)
    elif score < 0:
        direction = "bearish"
        confidence = min(0.6, 0.4 + abs(score) * 0.1)
    else:
        direction = "neutral"
        confidence = 0.3

    return {"direction": direction, "confidence": confidence, "score": score, "signals": signals + details}
