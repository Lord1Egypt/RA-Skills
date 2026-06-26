"""库存仓单分析 Skill

封装库存仓单指标计算和规则驱动的库存仓单分析，为期货交易决策提供供需基本面视角。
"""

from __future__ import annotations

from typing import Dict, Any, Optional
import datetime as _dt

from core.core_engine import AnalysisResult


def run(
    symbol: str,
    inventory_data: Optional[Dict[str, Any]] = None,
    warehouse_receipt_data: Optional[Dict[str, Any]] = None,
    config: Optional[Dict[str, Any]] = None,
    **kwargs,
) -> AnalysisResult:
    """执行库存仓单分析
    
    Args:
        symbol: 合约代码
        inventory_data: 库存时序数据
        warehouse_receipt_data: 仓单数据
        config: 配置参数
        
    Returns:
        AnalysisResult: 库存仓单分析结果
    """
    result = AnalysisResult(skill_name="inventory_analysis")
    
    try:
        import pandas as pd
        import numpy as np
        
        indicators = {}
        
        # 处理库存数据
        if inventory_data is not None:
            df_inv = pd.DataFrame(inventory_data)
            inv_cols = [c for c in df_inv.columns if c.lower() in ["inventory", "stock", "库存", "仓单"]]
            if inv_cols:
                df_inv = df_inv.rename(columns={inv_cols[0]: "inventory"})
            
            if "inventory" in df_inv.columns:
                inv_series = df_inv["inventory"].dropna().astype(float)
                if len(inv_series) >= 2:
                    indicators["latest_inventory"] = float(inv_series.iloc[-1])
                    indicators["inv_change_wow"] = round((inv_series.iloc[-1] - inv_series.iloc[-2]) / inv_series.iloc[-2] * 100, 2) if inv_series.iloc[-2] != 0 else 0
                    if len(inv_series) >= 5:
                        indicators["inv_change_mom"] = round((inv_series.iloc[-1] - inv_series.iloc[-5]) / inv_series.iloc[-5] * 100, 2) if inv_series.iloc[-5] != 0 else 0
                    if len(inv_series) >= 20:
                        # ==================== 季节性 Z-score（核心修复）====================
                        # 问题：滚动Z-score会跨季节比较（如5月vs10月），农产品库存含义完全不同
                        # 修复：强制优先同月份比较，同月数据不足时回退到60天滚动窗口
                        seasonal_mean = None
                        seasonal_std = None
                        seasonal_count = 0
                        curr_month = None
                        date_col = None
                        for col_name in df_inv.columns:
                            col_lower = str(col_name).lower()
                            if any(k in col_lower for k in ("日期", "时间", "date", "time")):
                                date_col = col_name
                                break
                        if date_col:
                            try:
                                _dates = pd.to_datetime(df_inv[date_col], errors="coerce")
                                latest_date = _dates.iloc[-1]
                                if pd.notna(latest_date):
                                    curr_month = latest_date.month
                                    same_mask = _dates.dt.month == curr_month
                                    same_month_vals = df_inv.loc[same_mask, "inventory"].dropna().astype(float)
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
                            lookback = min(60, len(inv_series))
                            mean = inv_series.iloc[-lookback:].mean()
                            std = inv_series.iloc[-lookback:].std()
                            indicators["zscore_method"] = f"rolling_{lookback}d"
                        indicators["inv_zscore"] = round((inv_series.iloc[-1] - mean) / std, 2) if std and std > 0 else 0
                        if seasonal_mean is not None and seasonal_std and seasonal_std > 0:
                            rolling_mean_60 = inv_series.iloc[-60:].mean()
                            rolling_std_60 = inv_series.iloc[-60:].std()
                            if rolling_std_60 and rolling_std_60 > 0:
                                indicators["zscore_rolling_60d"] = round((inv_series.iloc[-1] - rolling_mean_60) / rolling_std_60, 2)
                    indicators["data_points"] = len(inv_series)
        
        # 处理仓单数据
        if warehouse_receipt_data is not None:
            df_wr = pd.DataFrame(warehouse_receipt_data)
            wr_cols = [c for c in df_wr.columns if c.lower() in ["receipt", "warehouse", "仓单", "注册仓单"]]
            if wr_cols:
                df_wr = df_wr.rename(columns={wr_cols[0]: "warehouse_receipt"})
            
            if "warehouse_receipt" in df_wr.columns:
                last_wr = df_wr.iloc[-1]
                indicators["latest_warehouse_receipt"] = float(last_wr["warehouse_receipt"]) if pd.notna(last_wr.get("warehouse_receipt")) else None
                
                if len(df_wr) >= 5:
                    indicators["wr_change_5d"] = float(df_wr["warehouse_receipt"].iloc[-1] - df_wr["warehouse_receipt"].iloc[-5]) if pd.notna(df_wr["warehouse_receipt"].iloc[-5]) else None
                
                indicators["wr_data_points"] = len(df_wr)
        
        result.add_data("indicators", indicators)
        if not indicators:
            indicators["soft_data_hint"] = (
                f"API 未返回 {symbol} 库存数据。请 AI Agent 搜索补全："
                f"'{symbol} 库存 仓单 {_dt.datetime.now().strftime('%Y年%m月')}'"
            )
            indicators["search_actions"] = [
                {"query": f"{symbol} 期货 库存 仓单 注册仓单 {_dt.datetime.now().strftime('%Y年%m月')}", "source": "web", "priority": "high"},
                {"query": f"site:shfe.com.cn OR site:dce.com.cn OR site:czce.com.cn {symbol} 仓单 库存", "source": "exchange", "priority": "high"},
            ]
        if inventory_data and isinstance(inventory_data, dict) and "日期" in inventory_data:
            dates = [d for d in inventory_data.get("日期", []) if d]
            if dates:
                result.add_data("data_date", str(dates[-1]))
        
        signal = _rule_based_inventory_signal(indicators)
        result.add_data("rule_based_signal", signal)
        result.set_signal(signal.get("direction", "neutral"), signal.get("confidence", 0.3))
        result.bullets.extend(signal.get("signals", []) + signal.get("details", []))
        
    except Exception as e:
        result.add_error(f"库存仓单分析出错: {e}")
    
    return result


def _rule_based_inventory_signal(indicators: Dict[str, Any]) -> Dict[str, Any]:
    """基于规则的库存仓单信号"""
    score = 0
    signals = []
    details = []  # 详细分析理由
    
    zscore = indicators.get("inv_zscore")
    zscore_method = indicators.get("zscore_method", "unknown")
    wow = indicators.get("inv_change_wow")
    mom = indicators.get("inv_change_mom")
    latest = indicators.get("latest_inventory")
    wr = indicators.get("latest_warehouse_receipt")
    wr_change = indicators.get("wr_change_5d")
    
    # ============ 库存绝对量 ============
    if latest is not None:
        # 库存绝对量分析需要结合Z分数
        details.append(f"🔍 【库存】当前库存={latest:,.0f}吨")
    
    # ============ 历史分位分析(Z分数) ============
    if zscore is not None:
        zscore_tag = f"({zscore_method})" if zscore_method != "unknown" else ""
        if zscore > 2.5:
            score -= 2
            signals.append(f"库存处于历史极高位置(Z={zscore:.1f} {zscore_tag})")
            details.append(f"📊 【历史分位】Z={zscore:.1f} {zscore_tag}，库存处于97.5%分位以上，历史极高水平")
            details.append("⚠️ 供给严重过剩，去库压力极大，对价格形成显著下行压力")
        elif zscore > 1.5:
            score -= 1
            signals.append(f"库存处于历史高位(Z={zscore:.1f} {zscore_tag})")
            details.append(f"📊 【历史分位】Z={zscore:.1f} {zscore_tag}，库存处于85%以上分位，偏高水平")
            details.append("⚠️ 供给相对充裕，库存去化需要时间，对价格形成一定压力")
        elif zscore > 0.5:
            score -= 0.5
            signals.append(f"库存处于历史偏高位置(Z={zscore:.1f} {zscore_tag})")
            details.append(f"📊 【历史分位】Z={zscore:.1f} {zscore_tag}，库存处于60%-85%分位，中性偏空")
        elif zscore < -2.5:
            score += 2
            signals.append(f"库存处于历史极低位置(Z={zscore:.1f} {zscore_tag})")
            details.append(f"📊 【历史分位】Z={zscore:.1f} {zscore_tag}，库存处于2.5%分位以下，历史极低水平")
            details.append("✅ 供给严重不足，低库存对价格形成显著支撑，({'可能存在供应紧张' if latest and latest < 50000 else '现货强势'})")
        elif zscore < -1.5:
            score += 1
            signals.append(f"库存处于历史低位(Z={zscore:.1f} {zscore_tag})")
            details.append(f"📊 【历史分位】Z={zscore:.1f} {zscore_tag}，库存处于15%分位以下，低位水平")
            details.append("✅ 供给相对偏紧，库存偏低对价格形成支撑")
        elif zscore < -0.5:
            score += 0.5
            signals.append(f"库存处于历史偏低位置(Z={zscore:.1f} {zscore_tag})")
            details.append(f"📊 【历史分位】Z={zscore:.1f} {zscore_tag}，库存处于40%分位以下，中性偏多")
        else:
            details.append(f"📊 【历史分位】Z={zscore:.1f} {zscore_tag}，库存处于历史中位附近，供需基本平衡")
    
    # ============ 周度变化 ============
    if wow is not None:
        if wow > 15:
            score -= 2
            signals.append(f"库存周度大增(+{wow:.1f}%)")
            details.append(f"📈 【周变化】库存环比大增+{wow:.1f}%，短期供给激增，价格压力显著")
        elif wow > 5:
            score -= 1
            signals.append(f"库存周度增加(+{wow:.1f}%)")
            details.append(f"📈 【周变化】库存环比增加+{wow:.1f}%，短期供给上升，对价格形成压力")
        elif wow > 0:
            score -= 0.5
            signals.append(f"库存周度微增(+{wow:.1f}%)")
            details.append(f"📈 【周变化】库存环比微增+{wow:.1f}%，短期供给略增")
        elif wow < -15:
            score += 2
            signals.append(f"库存周度大降({wow:.1f}%)")
            details.append(f"📉 【周变化】库存环比大降{abs(wow):.1f}%，短期去库明显，({'供应紧张' if zscore and zscore > 0 else '需求强劲'})")
        elif wow < -5:
            score += 1
            signals.append(f"库存周度下降({wow:.1f}%)")
            details.append(f"📉 【周变化】库存环比下降{abs(wow):.1f}%，短期去库进行中")
        elif wow < 0:
            score += 0.5
            signals.append(f"库存周度微降({wow:.1f}%)")
            details.append(f"📉 【周变化】库存环比微降{abs(wow):.1f}%，短期去库缓慢进行")
        else:
            details.append(f"➡️ 【周变化】库存环比持平({wow:+.1f}%)，短期供需平衡")
    
    # ============ 月度变化 ============
    if mom is not None:
        if mom > 20:
            score -= 2
            signals.append(f"库存月度大增(+{mom:.1f}%)")
            details.append(f"📈 【月变化】库存环比大增+{mom:.1f}%，月度供给大幅上升，趋势性累库中")
        elif mom > 10:
            score -= 1
            signals.append(f"库存月度增加(+{mom:.1f}%)")
            details.append(f"📈 【月变化】库存环比增加+{mom:.1f}%，月度供给上升，趋势偏空")
        elif mom > 0:
            score -= 0.5
            signals.append(f"库存月度微增(+{mom:.1f}%)")
            details.append(f"📈 【月变化】库存环比微增+{mom:.1f}%，月度供给略增")
        elif mom < -20:
            score += 2
            signals.append(f"库存月度大降({mom:.1f}%)")
            details.append(f"📉 【月变化】库存环比大降{abs(mom):.1f}%，月度去库明显，({'供应收缩' if wow and wow < 0 else '需求旺盛'})")
        elif mom < -10:
            score += 1
            signals.append(f"库存月度下降({mom:.1f}%)")
            details.append(f"📉 【月变化】库存环比下降{abs(mom):.1f}%，月度去库进行中")
        elif mom < 0:
            score += 0.5
            signals.append(f"库存月度微降({mom:.1f}%)")
            details.append(f"📉 【月变化】库存环比微降{abs(mom):.1f}%，月度去库缓慢")
        else:
            details.append(f"➡️ 【月变化】库存月度持平({mom:+.1f}%)，月度供需平衡")
    
    # ============ 仓单变化 ============
    if wr is not None:
        details.append(f"🔍 【仓单】当前仓单={wr:,.0f}手")
    
    if wr_change is not None:
        if wr_change > 5000:
            score -= 1
            signals.append(f"仓单大幅增加(+{wr_change:,.0f}手)")
            details.append(f"📈 【仓单】注册仓单增加+{wr_change:,.0f}手，({'产业客户看空后市' if structure == 'contango' else '现货销售不畅'})")
        elif wr_change > 1000:
            score -= 0.5
            signals.append(f"仓单增加(+{wr_change:,.0f}手)")
            details.append(f"📈 【仓单】注册仓单增加+{wr_change:,.0f}手，仓单压力上升")
        elif wr_change < -5000:
            score += 1
            signals.append(f"仓单大幅减少({wr_change:,.0f}手)")
            details.append(f"📉 【仓单】注册仓单减少{abs(wr_change):,.0f}手，({'产业客户看好后市' if structure == 'backwardation' else '现货需求旺盛'})")
        elif wr_change < -1000:
            score += 0.5
            signals.append(f"仓单减少({wr_change:,.0f}手)")
            details.append(f"📉 【仓单】注册仓单减少{abs(wr_change):,.0f}手，仓单压力缓解")
    
    # ============ 综合评分 ============
    if score >= 3:
        direction = "bullish"
        confidence = min(0.7, 0.35 + score * 0.06)
    elif score > 0:
        direction = "bullish"
        confidence = min(0.6, 0.35 + score * 0.08)
    elif score <= -3:
        direction = "bearish"
        confidence = min(0.7, 0.35 + abs(score) * 0.06)
    elif score < 0:
        direction = "bearish"
        confidence = min(0.6, 0.35 + abs(score) * 0.08)
    else:
        direction = "neutral"
        confidence = 0.3
    
    # 合并所有信号
    all_signals = signals + details
    
    return {
        "direction": direction,
        "confidence": confidence,
        "score": score,
        "signals": all_signals,
    }