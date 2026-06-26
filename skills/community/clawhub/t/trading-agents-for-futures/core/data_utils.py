#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据获取工具函数

提供统一的期货数据获取接口，封装行情、基差、库存、持仓、新闻等数据源。
支持缓存和在线获取两种模式。
"""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

logger = logging.getLogger(__name__)


class DataProvider:
    """统一数据提供器

    封装行情、基差、库存、持仓、新闻等数据获取逻辑。
    优先从本地缓存读取，缓存未命中时尝试在线获取（如配置允许）。
    """

    def __init__(
        self,
        cache_dir: Optional[str] = None,
        enable_online: bool = True,
    ):
        """初始化

        Args:
            cache_dir: 本地缓存目录路径
            enable_online: 是否允许在线获取数据
        """
        if cache_dir:
            self.cache_dir = Path(cache_dir)
        else:
            self.cache_dir = Path(__file__).resolve().parent.parent / "cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.enable_online = enable_online

    def get_price_data(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        freq: str = "D",
    ) -> pd.DataFrame:
        """获取期货价格数据

        Args:
            symbol: 品种代码，如 "RB"
            start_date: 起始日期，格式 "YYYY-MM-DD"
            end_date: 截止日期，格式 "YYYY-MM-DD"
            freq: 频率，"D"日线 / "W"周线 / "M"月线

        Returns:
            DataFrame，包含 OHLCV 列
        """
        if not start_date:
            start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")

        # 尝试从缓存加载
        cache_file = self.cache_dir / f"price_{symbol}_{freq}.parquet"

        if cache_file.exists():
            try:
                df = pd.read_parquet(cache_file)
                if not df.empty:
                    # 使用"时间"列作为日期过滤依据（兼容有无索引两种情况）
                    if df.index.name == "时间" or "时间" in df.columns:
                        if "时间" not in df.columns:
                            df = df.reset_index()  # 索引是"时间"，重置为列
                        df["时间"] = pd.to_datetime(df["时间"])
                        mask = (df["时间"] >= start_date) & (df["时间"] <= end_date)
                        return df[mask].reset_index(drop=True)
                    else:
                        # 兼容旧缓存：索引是整数，直接用"时间"列
                        if "时间" in df.columns:
                            df["时间"] = pd.to_datetime(df["时间"])
                            mask = (df["时间"] >= start_date) & (df["时间"] <= end_date)
                            return df[mask].reset_index(drop=True)
            except Exception as e:
                logger.warning(f"加载缓存失败: {e}")

        # 在线获取（如配置允许）
        if self.enable_online:
            try:
                df = self._fetch_price_online(symbol, start_date, end_date, freq)
                if not df.empty:
                    df.to_parquet(cache_file)
                return df
            except Exception as e:
                logger.error(f"在线获取价格数据失败: {e}")

        logger.warning(f"无法获取{symbol}价格数据，返回空DataFrame")
        return pd.DataFrame()

    def _fetch_price_online(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
        freq: str,
    ) -> pd.DataFrame:
        """在线获取价格数据"""
        # 降级：直接使用 akshare（使用新浪接口，避免代理SSL问题）
        try:
            import akshare as ak
            
            # 品种代码映射（新浪接口用英文字母代码）
            # 新浪主力合约代码：RB0=螺纹钢主连, CU0=沪铜主连, etc.
            sina_symbol_map = {
                "RB": "RB0", "HC": "HC0", "CU": "CU0",
                "AL": "AL0", "ZN": "ZN0", "NI": "NI0", "PB": "PB0",
                "SN": "SN0", "AG": "AG0", "AU": "AU0",
                "I": "I0", "JM": "JM0", "J": "J0",
                "TA": "TA0", "MA": "MA0", "RU": "RU0",
                "FG": "FG0", "SA": "SA0", "LH": "LH0", "SC": "SC0",
                "L": "L0", "PP": "PP0", "M": "M0",
                "Y": "Y0", "P": "P0", "A": "A0",
                "C": "C0", "CS": "CS0", "RM": "RM0",
                "OI": "OI0", "CF": "CF0", "SR": "SR0",
                "JD": "JD0", "AP": "AP0", "CJ": "CJ0",
                "EG": "EG0", "EB": "EB0", "PG": "PG0",
                "BU": "BU0", "FU": "FU0", "SS": "SS0",
                "LU": "LU0", "BC": "BC0", "NR": "NR0",
                "SP": "SP0", "BR": "BR0", "SF": "SF0",
                "SM": "SM0", "SI": "SI0", "LC": "LC0",
                "PK": "PK0", "WR": "WR0",
            }
            
            sina_symbol = sina_symbol_map.get(symbol.upper(), f"{symbol.upper()}0")
            
            # 使用新浪接口（不需要代理也能用）
            # 注意：新浪接口不需要period参数，直接返回日线数据
            df = ak.futures_main_sina(symbol=sina_symbol, start_date=start_date.replace("-", ""), end_date=end_date.replace("-", ""))
            
            # 规范列名（新浪接口返回列名：日期, 开盘价, 最高价, 最低价, 收盘价, 成交量, 持仓量, 动态结算价）
            if not df.empty:
                # 重命名列
                df = df.rename(columns={
                    "日期": "时间",
                    "开盘价": "开盘",
                    "最高价": "最高",
                    "最低价": "最低",
                    "收盘价": "收盘",
                    "成交量": "成交量",
                    "持仓量": "持仓量",
                })
                
                # 确保有需要的列
                need = ["时间", "开盘", "最高", "最低", "收盘", "成交量", "持仓量"]
                for col in need:
                    if col not in df.columns:
                        df[col] = pd.NA
                df = df[need].copy()
                df["时间"] = pd.to_datetime(df["时间"])
                df = df.sort_values("时间").reset_index(drop=True)
                # 设置时间列为索引，方便缓存加载
                df = df.set_index("时间")
                logger.info(f"成功获取{symbol}价格数据，共{len(df)}条")
            
            return df
        except Exception as e:
            logger.error(f"akshare获取价格数据失败: {e}")
            return pd.DataFrame()

    def get_basis_data(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取基差数据

        Returns:
            DataFrame，包含 basis（基差）、basis_rate（基差率）、spot_price、future_price
        """
        if not start_date:
            start_date = (datetime.now() - timedelta(days=180)).strftime("%Y-%m-%d")
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")

        cache_file = self.cache_dir / f"basis_{symbol}.parquet"
        cache_ttl_minutes = 30  # 基差缓存30分钟，避免高频API调用

        if cache_file.exists():
            try:
                df = pd.read_parquet(cache_file)
                if not df.empty:
                    cache_age = (datetime.now().timestamp() - cache_file.stat().st_mtime) / 60
                    # 缓存未过期 - 直接返回
                    if cache_age < cache_ttl_minutes:
                        if "日期" in df.columns:
                            df["日期"] = pd.to_datetime(df["日期"])
                            mask = (df["日期"] >= start_date) & (df["日期"] <= end_date)
                            return df[mask].reset_index(drop=True)
                        elif df.index.name == "日期":
                            df.index = pd.to_datetime(df.index)
                            mask = (df.index >= start_date) & (df.index <= end_date)
                            return df[mask].reset_index(drop=True)
                    # 缓存过期 - 增量更新
                    elif self.enable_online:
                        logger.info(f"基差缓存过期(>{cache_ttl_minutes}分钟)，增量更新 {symbol}")
                        date_col = "日期" if "日期" in df.columns else (df.index.name if df.index.name == "日期" else None)
                        if date_col:
                            if date_col == "日期":
                                df["日期"] = pd.to_datetime(df["日期"])
                                latest_date_in_cache = df["日期"].max()
                            else:
                                df.index = pd.to_datetime(df.index)
                                latest_date_in_cache = df.index.max()
                            new_start = (latest_date_in_cache + timedelta(days=1)).strftime("%Y-%m-%d")
                            new_df = self._fetch_basis_online(symbol, new_start, end_date)
                            if not new_df.empty:
                                combined = pd.concat([df, new_df], ignore_index=True)
                                combined = combined.drop_duplicates(subset=["日期"]).sort_values("日期").reset_index(drop=True)
                                combined.to_parquet(cache_file)
                                mask = (combined["日期"] >= start_date) & (combined["日期"] <= end_date)
                                logger.info(f"基差增量更新完成: +{len(new_df)}行")
                                return combined[mask].reset_index(drop=True)
            except Exception as e:
                logger.warning(f"加载基差缓存失败: {e}")

        if self.enable_online:
            try:
                df = self._fetch_basis_online(symbol, start_date, end_date)
                if not df.empty:
                    df.to_parquet(cache_file)
                return df
            except Exception as e:
                logger.error(f"在线获取基差数据失败: {e}")

        return pd.DataFrame()

    def _fetch_basis_online(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
    ) -> pd.DataFrame:
        """在线获取基差数据
        
        使用 AkShare futures_spot_price 接口获取现货价格和基差数据
        """
        import akshare as ak
        
        # 品种代码映射（100ppi.com使用的代码）
        # 螺纹钢=RB, 豆粕=M, 菜粕=RM, 铜=CU, 铝=AL, 锌=ZN等
        symbol_map = {
            "RB": ["RB"], "HC": ["HC"], "CU": ["CU"], "AL": ["AL"],
            "ZN": ["ZN"], "NI": ["NI"], "SN": ["SN"], "AG": ["AG"],
            "AU": ["AU"], "I": ["I"], "J": ["J"], "JM": ["JM"],
            "M": ["M"], "Y": ["Y"], "P": ["P"], "RM": ["RM"],
            "CF": ["CF"], "SR": ["SR"], "TA": ["TA"], "MA": ["MA"],
            "RU": ["RU"], "L": ["L"], "PP": ["PP"], "V": ["V"],
            "LH": ["LH"], "SC": ["SC"],
        }
        
        symbols = symbol_map.get(symbol.upper(), [symbol.upper()])
        
        # 转换为YYYYMMDD格式
        start_str = start_date.replace("-", "")
        end_str = end_date.replace("-", "")
        
        all_data = []
        
        # 使用批量接口获取基差数据
        try:
            df = ak.futures_spot_price_daily(start_day=start_str, end_day=end_str, vars_list=symbols)
            if df is not None and not df.empty:
                df = df.rename(columns={
                    "date": "日期",
                    "symbol": "品种",
                    "spot_price": "现货价格",
                    "near_contract": "近月合约",
                    "near_contract_price": "近月价格",
                    "dominant_contract": "主力合约",
                    "dominant_contract_price": "主力价格",
                    "near_basis": "近月基差",
                    "dom_basis": "主力基差",
                    "near_basis_rate": "近月基差率",
                    "dom_basis_rate": "主力基差率",
                })
                if "日期" in df.columns:
                    df["日期"] = pd.to_datetime(df["日期"], format="%Y%m%d")
                return df.sort_values("日期").reset_index(drop=True) if "日期" in df.columns else df
        except Exception:
            pass
        
        # 回退：只获取最近5个交易日
        from datetime import datetime, timedelta
        current = datetime.strptime(end_str, "%Y%m%d")
        start_dt = max(datetime.strptime(start_str, "%Y%m%d"), current - timedelta(days=5))
        
        while current >= start_dt:
            date_str = current.strftime("%Y%m%d")
            try:
                df = ak.futures_spot_price(date=date_str, vars_list=symbols)
                if df is not None and not df.empty:
                    df = df.rename(columns={
                        "var": "品种",
                        "sp": "现货价格",
                        "near_symbol": "近月合约",
                        "near_price": "近月价格",
                        "dom_symbol": "主力合约",
                        "dom_price": "主力价格",
                        "near_basis": "近月基差",
                        "dom_basis": "主力基差",
                        "near_basis_rate": "近月基差率",
                        "dom_basis_rate": "主力基差率",
                        "date": "日期",
                    })
                    all_data.append(df)
            except Exception:
                pass
            current -= timedelta(days=1)
        
        if all_data:
            result = pd.concat(all_data, ignore_index=True)
            result["日期"] = pd.to_datetime(result["日期"], format="%Y%m%d", errors="coerce")
            result = result.sort_values("日期").reset_index(drop=True)
            return result
        
        return pd.DataFrame()

    def get_term_structure_data(
        self,
        symbol: str,
        date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """获取期限结构数据

        Args:
            symbol: 品种代码
            date: 日期，默认最新

        Returns:
            {
                "contracts": [合约列表],
                "prices": [对应价格],
                "months": [交割月份],
                "structure": "contango" | "backwardation" | "flat",
                "roll_yield_pct": 展期收益率
            }
        """
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")

        cache_file = self.cache_dir / f"term_structure_{symbol}.json"

        if cache_file.exists():
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    cached = json.load(f)
                    if cached.get("date") == date:
                        return cached
            except Exception as e:
                logger.warning(f"加载期限结构缓存失败: {e}")

        if self.enable_online:
            try:
                data = self._fetch_term_structure_online(symbol, date)
                if data and any(p > 0 for p in data.get("prices", [])):
                    with open(cache_file, "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    return data
            except Exception as e:
                logger.error(f"在线获取期限结构数据失败: {e}")

        # 兜底：在线获取失败后，使用过期缓存
        if cache_file.exists():
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    cached = json.load(f)
                    if cached and any(p > 0 for p in cached.get("prices", [])):
                        cached["fallback_used"] = True
                        cached["fallback_date"] = cached.get("date", cached.get("fetch_date", ""))
                        cached["data_source_note"] = f"缓存兜底: 在线API不可用，使用本地缓存 {cached.get('date', cached.get('fetch_date', 'unknown'))}"
                        logger.warning(f"期限结构 [{symbol}]: 在线获取失败，使用过期缓存作为兜底")
                        return cached
            except Exception:
                pass

        return {"contracts": [], "prices": [], "months": [], "structure": "unknown", "roll_yield_pct": 0}

    def _fetch_term_structure_online(
        self,
        symbol: str,
        date: str,
    ) -> Dict[str, Any]:
        """在线获取期限结构数据

        使用 AkShare get_roll_yield_bar 获取不同合约的期限结构和展期收益率
        """
        import akshare as ak
        
        try:
            date_str = date.replace("-", "")
            
            data = self._try_fetch_ts(ak, symbol, date_str)
            if data and any(p > 0 for p in data.get("prices", [])):
                data["fetch_date"] = date_str
                data["fallback_used"] = False
                return data
            
            # 回退：尝试前一个交易日（跳过周末）
            from datetime import datetime, timedelta
            prev_date = datetime.strptime(date_str, "%Y%m%d") - timedelta(days=1)
            max_attempts = 30
            for _ in range(max_attempts):
                while prev_date.weekday() >= 5:
                    prev_date -= timedelta(days=1)
                prev_str = prev_date.strftime("%Y%m%d")
                data = self._try_fetch_ts(ak, symbol, prev_str)
                if data and any(p > 0 for p in data.get("prices", [])):
                    data["fetch_date"] = prev_str
                    data["fallback_used"] = True
                    data["fallback_date"] = prev_date.strftime("%Y-%m-%d")
                    logger.info(f"期限结构: 回退使用 {prev_date.strftime('%Y-%m-%d')} 数据（API 当日不可用）")
                    return data
                prev_date -= timedelta(days=1)
        except Exception as e:
            logger.error(f"获取期限结构数据失败: {e}")
        
        return {"contracts": [], "prices": [], "months": [], "structure": "unknown", "roll_yield_pct": 0}
    
    def _try_fetch_ts(self, ak, symbol: str, date_str: str) -> Dict[str, Any]:
        """尝试从指定日期获取期限结构
        
        多层回退策略以应对 akshare 对不同品种/交易所的参数兼容性问题
        """
        import traceback
        sym = symbol.upper()
        
        # akshare get_roll_yield_bar 需要 YYYY-MM-DD 格式
        formatted_date = date_str
        if len(date_str) == 8 and date_str.isdigit():
            formatted_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
        
        # 交易所映射，用于 futures_daily 回退
        EXCHANGE_MAP = {
            "CU": "SHFE", "AL": "SHFE", "ZN": "SHFE", "PB": "SHFE",
            "NI": "SHFE", "SN": "SHFE", "AU": "SHFE", "AG": "SHFE",
            "RB": "SHFE", "WR": "SHFE", "HC": "SHFE", "SS": "SHFE",
            "FU": "SHFE", "BU": "SHFE", "RU": "SHFE", "SP": "SHFE",
            "BC": "SHFE", "NR": "SHFE", "LU": "SHFE", "BR": "SHFE",
            "SC": "INE",
            "A": "DCE", "B": "DCE", "C": "DCE", "CS": "DCE",
            "M": "DCE", "Y": "DCE", "P": "DCE",
            "L": "DCE", "PP": "DCE", "V": "DCE",
            "J": "DCE", "JM": "DCE", "I": "DCE",
            "EG": "DCE", "EB": "DCE", "PG": "DCE", "LH": "DCE",
            "CF": "CZCE", "SR": "CZCE", "OI": "CZCE", "RM": "CZCE",
            "MA": "CZCE", "TA": "CZCE", "FG": "CZCE", "SA": "CZCE",
            "ZC": "CZCE", "UR": "CZCE", "PK": "CZCE", "AP": "CZCE",
            "CJ": "CZCE", "JR": "CZCE", "LR": "CZCE",
            "IF": "CFFEX", "IH": "CFFEX", "IC": "CFFEX",
            "T": "CFFEX", "TF": "CFFEX", "TS": "CFFEX",
            "SI": "GFEX", "LC": "GFEX",
        }
        
        strategies = [
            # 前4个策略用 YYYY-MM-DD 格式（get_roll_yield_bar 所需格式）
            ("type_method=symbol", lambda: ak.get_roll_yield_bar(type_method="symbol", var=sym, date=formatted_date)),
            ("type_method=var", lambda: ak.get_roll_yield_bar(type_method="var", var=sym, date=formatted_date)),
            ("date_only", lambda: ak.get_roll_yield_bar(date=formatted_date)),
            ("var_only", lambda: ak.get_roll_yield_bar(var=sym, date=formatted_date)),
        ]
        
        # 第5个策略：用 get_futures_daily 手动拉全市场数据过滤（终极回退）
        def _futures_daily_fallback():
            upper_sym = sym.upper()
            exchange = None
            # 按前缀匹配交易所（优先匹配最长前缀）
            matched = ""
            for prefix, exch in sorted(EXCHANGE_MAP.items(), key=lambda x: -len(x[0])):
                if upper_sym.startswith(prefix) and len(prefix) > len(matched):
                    exchange = exch
                    matched = prefix

            def _find_variety_column(df):
                """查找品种列，兼容多种列名"""
                for col in ("variety", "symbol", "品种", "合约", "contract", "name"):
                    if col in df.columns:
                        return col
                return None

            def _filter_by_symbol(df, sym_upper, variety_col):
                if variety_col == "symbol":
                    return df[df["symbol"].astype(str).str.upper().str.startswith(sym_upper)]
                elif variety_col:
                    return df[df[variety_col].astype(str).str.upper() == sym_upper]
                return df

            if exchange is None:
                # 未知交易所：尝试所有交易所
                for exch_name in ["SHFE", "DCE", "CZCE", "CFFEX", "INE", "GFEX"]:
                    try:
                        raw = ak.get_futures_daily(start_date=formatted_date, end_date=formatted_date, market=exch_name)
                        if raw is not None and not raw.empty:
                            variety_col = _find_variety_column(raw)
                            if variety_col:
                                subset = _filter_by_symbol(raw, upper_sym, variety_col)
                                if not subset.empty:
                                    return subset.sort_values(variety_col)
                    except Exception:
                        continue
                raise ValueError(f"无法确定 {sym} 的交易所，尝试全部交易所均无数据")
            raw = ak.get_futures_daily(start_date=formatted_date, end_date=formatted_date, market=exchange)
            if raw is None or raw.empty:
                raise ValueError(f"futures_daily {exchange} 无数据")
            variety_col = _find_variety_column(raw)
            if variety_col is None:
                raise ValueError(f"futures_daily {exchange} 无法识别品种列，可用列: {list(raw.columns)}")
            subset = _filter_by_symbol(raw, upper_sym, variety_col)
            if subset.empty:
                raise ValueError(f"futures_daily {exchange} 中无 {sym} 数据")
            return subset.sort_values(variety_col)
        
        strategies.append(("futures_daily_fallback", _futures_daily_fallback))
        
        df = None
        last_error = ""
        for strategy_name, strategy_fn in strategies:
            try:
                result = strategy_fn()
                if result is not None and not result.empty and not (isinstance(result, bool) and result is True):
                    df = result
                    logger.info(f"期限结构 [{symbol}]: 策略 {strategy_name} 成功")
                    break
            except Exception as e:
                last_error = f"{type(e).__name__}: {str(e)[:80]}"
                logger.info(f"期限结构 [{symbol}]: 策略 {strategy_name} 失败 ({last_error})")
                continue
        
        if df is None or df.empty:
            logger.info(f"期限结构 [{symbol}]: 全部策略均失败，将回退到前一交易日")
            return {"contracts": [], "prices": [], "months": [], "structure": "unknown", "roll_yield_pct": 0, "api_error": last_error}
        
        # 列名容错：统一处理可能的列名变体（避免重复映射导致列名重复）
        has_symbol_col = any(c in df.columns for c in ("symbol", "variety", "contract", "品种", "合约"))
        has_close_col = "close" in df.columns or "收盘价" in df.columns
        has_settle_col = "settle" in df.columns or "结算价" in df.columns
        
        col_map = {}
        for col in df.columns:
            col_lower = col.lower().strip()
            if col_lower in ("symbol", "variety", "contract", "合约"):
                if col_lower == "symbol" or not has_symbol_col:
                    col_map[col] = "symbol"
            elif col_lower in ("close", "收盘价", "收盘"):
                if col_lower == "close" or not has_close_col:
                    col_map[col] = "close"
            elif col_lower in ("settle", "结算价", "结算"):
                if col_lower == "settle" or not has_settle_col:
                    col_map[col] = "settle"
        if col_map:
            df = df.rename(columns=col_map)
        
        # 确定合约名列
        symbol_col = None
        for col in ("symbol", "variety", "contract", "品种"):
            if col in df.columns:
                symbol_col = col
                break
        
        if symbol_col is None:
            logger.warning(f"期限结构 [{symbol}]: 无法识别合约名列，可用列: {list(df.columns)}")
            return {"contracts": [], "prices": [], "months": [], "structure": "unknown", "roll_yield_pct": 0, "api_error": "no_symbol_column"}
        
        try:
            df = df.sort_values(symbol_col).reset_index(drop=True)
            contracts = df[symbol_col].tolist()
        except Exception as e:
            logger.warning(f"期限结构 [{symbol}]: 合约名排序失败 ({e})，使用原始顺序")
            contracts = df[symbol_col].tolist()
        
        # 确定价格列
        price_col = "close" if "close" in df.columns else "settle"
        if price_col not in df.columns:
            numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
            if numeric_cols:
                price_col = numeric_cols[0]
            else:
                return {"contracts": [], "prices": [], "months": [], "structure": "unknown", "roll_yield_pct": 0, "api_error": "no_price_column"}
        
        prices_raw = df[price_col].tolist()
        prices = []
        for p in prices_raw:
            try:
                prices.append(float(p))
            except (ValueError, TypeError):
                prices.append(None)
        if all(v is None for v in prices) and price_col == "close" and "settle" in df.columns:
            prices = [float(p) if p is not None else 0.0 for p in df["settle"].tolist()]
        else:
            prices = [p if p is not None else 0.0 for p in prices]
        
        contracts_str = [str(c) for c in contracts]
        months = [c.replace(symbol.upper(), "").replace(symbol, "") for c in contracts_str]
        
        if len(prices) >= 2:
            if prices[0] < prices[-1]:
                structure = "contango"
            elif prices[0] > prices[-1]:
                structure = "backwardation"
            else:
                structure = "flat"
        else:
            structure = "unknown"
        
        roll_yield_pct = 0
        if len(prices) >= 2 and prices[0] > 0:
            roll_yield_pct = round((prices[-1] - prices[0]) / prices[0] * 100, 2)
        
        return {
            "contracts": [str(c) for c in contracts],
            "prices": [float(p) for p in prices],
            "months": months,
            "structure": structure,
            "roll_yield_pct": roll_yield_pct,
        }

    def get_inventory_data(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取库存仓单数据

        Returns:
            DataFrame，包含 inventory（库存量）、warehouse_receipts（仓单量）
        """
        if not start_date:
            start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")

        cache_file = self.cache_dir / f"inventory_{symbol}.parquet"

        if cache_file.exists():
            try:
                df = pd.read_parquet(cache_file)
                if not df.empty:
                    if "时间" in df.columns:
                        df["时间"] = pd.to_datetime(df["时间"])
                        mask = (df["时间"] >= start_date) & (df["时间"] <= end_date)
                        return df[mask].reset_index(drop=True)
                    elif df.index.name == "时间":
                        df.index = pd.to_datetime(df.index)
                        mask = (df.index >= start_date) & (df.index <= end_date)
                        return df[mask].reset_index(drop=True)
            except Exception as e:
                logger.warning(f"加载库存缓存失败: {e}")

        if self.enable_online:
            try:
                df = self._fetch_inventory_online(symbol, start_date, end_date)
                if not df.empty:
                    df.to_parquet(cache_file)
                return df
            except Exception as e:
                logger.error(f"在线获取库存数据失败: {e}")

        return pd.DataFrame()

    def _fetch_inventory_online(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
    ) -> pd.DataFrame:
        """在线获取库存数据
        
        使用 AkShare futures_inventory_em 接口获取期货库存数据
        """
        import akshare as ak
        
        # 品种中文名映射（东方财富网使用的名称）
        symbol_map = {
            "RB": "螺纹钢", "HC": "热轧卷板", "CU": "铜", "AL": "铝",
            "ZN": "锌", "PB": "铅", "NI": "镍", "SN": "锡",
            "AU": "沪金", "AG": "沪银",
            "I": "铁矿石", "J": "焦炭", "JM": "焦煤",
            "M": "豆粕", "Y": "豆油", "P": "棕榈油", "RM": "菜粕",
            "A": "豆一", "B": "豆二", "C": "玉米", "CS": "淀粉",
            "CF": "棉花", "SR": "白糖", "TA": "PTA", "MA": "甲醇",
            "RU": "天然橡胶", "L": "塑料", "PP": "聚丙烯", "V": "PVC",
            "LH": "生猪", "SC": "原油", "FU": "燃料油", "BU": "沥青",
            "SS": "不锈钢", "FG": "玻璃", "SA": "纯碱",
            "EG": "乙二醇", "EB": "苯乙烯", "PG": "液化气",
            "JD": "鸡蛋", "AP": "苹果", "CJ": "红枣",
            "SI": "工业硅", "LC": "碳酸锂", "OI": "菜油",
        }
        
        zh_name = symbol_map.get(symbol.upper(), symbol)
        
        try:
            df = ak.futures_inventory_em(symbol=zh_name)
            if not df.empty:
                df = df.rename(columns={
                    "日期": "时间",
                    "库存": "库存量",
                    "增减": "库存变化",
                })
                df["时间"] = pd.to_datetime(df["时间"])
                mask = (df["时间"] >= start_date) & (df["时间"] <= end_date)
                return df[mask].reset_index(drop=True)
            else:
                logger.warning(f"库存数据: {symbol}({zh_name}) API 返回空数据，品种可能无库存覆盖")
        except Exception as e:
            err_msg = str(e)
            if "请输入正确的symbol" in err_msg or "symbol" in err_msg.lower():
                logger.warning(f"库存数据: {symbol}({zh_name}) 不在东方财富覆盖范围内，err={err_msg[:100]}")
            else:
                logger.error(f"获取库存数据失败 [{symbol}({zh_name})]: {err_msg[:200]}")
        
        return pd.DataFrame()

    def get_position_data(
        self,
        symbol: str,
        date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """获取持仓席位数据

        Args:
            symbol: 品种代码
            date: 日期，默认最新

        Returns:
            {
                "long_positions": [{"member": 会员名, "volume": 多头持仓量}, ...],
                "short_positions": [{"member": 会员名, "volume": 空头持仓量}, ...],
                "top5_long_pct": 前5多头集中度%,
                "top5_short_pct": 前5空头集中度%,
                "net_position": 净持仓方向
            }
        """
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")

        cache_file = self.cache_dir / f"position_{symbol}_{date}.json"

        if cache_file.exists():
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"加载持仓缓存失败: {e}")

        if self.enable_online:
            try:
                data = self._fetch_position_online(symbol, date)
                if data:
                    with open(cache_file, "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                return data
            except Exception as e:
                logger.error(f"在线获取持仓数据失败: {e}")

        return {
            "long_positions": [],
            "short_positions": [],
            "top5_long_pct": 0,
            "top5_short_pct": 0,
            "net_position": "unknown",
        }

    def _fetch_position_online(
        self,
        symbol: str,
        date: str,
    ) -> Dict[str, Any]:
        """在线获取持仓数据
        
        使用 AkShare get_shfe_rank_table 等接口获取持仓席位数据
        """
        import akshare as ak
        
        # 品种代码映射（上期所使用的品种代码）
        # 品种代码映射
        shfe_symbols = ["RB", "HC", "CU", "AL", "ZN", "NI", "SN", "AU", "AG", "RU", "BU", "FU", "SP", "SS", "NR"]
        dce_symbols = ["M", "Y", "P", "A", "B", "C", "CS", "JD", "L", "V", "PP", "J", "JM", "I", "EG", "PG", "EB", "LH"]  # RM属郑商所，已移除
        czce_symbols = ["CF", "SR", "TA", "MA", "RM", "OI", "RI", "WH", "PM", "JR", "LR", "SF", "SM", "ZC", "AP", "UR", "CJ", "SA"]
        
        sym = symbol.upper()
        
        # 获取前一个交易日作为默认（当前日期可能非交易日）
        date_str = date.replace("-", "")
        
        try:
            # 先尝试当前日期
            result = self._try_fetch_position(sym, date_str)
            if result and result.get("long_positions"):
                return result
            
            # 回退：尝试前一个交易日
            from datetime import datetime, timedelta
            prev_date = datetime.strptime(date_str, "%Y%m%d") - timedelta(days=1)
            zip_cleared = False
            for _ in range(30):
                while prev_date.weekday() >= 5:
                    prev_date -= timedelta(days=1)
                prev_str = prev_date.strftime("%Y%m%d")
                try:
                    result = self._try_fetch_position(sym, prev_str)
                except Exception as e2:
                    err = str(e2)
                    if ("zip" in err.lower() or "not a zip" in err.lower()) and not zip_cleared:
                        self._clear_akshare_cache()
                        zip_cleared = True
                        result = self._try_fetch_position(sym, prev_str)
                    else:
                        result = None
                if result and result.get("long_positions"):
                    return result
                prev_date -= timedelta(days=1)
                
        except Exception as e:
            logger.error(f"获取持仓数据失败: {e}")
        
        return {"long_positions": [], "short_positions": [], "top5_long_pct": 0, "top5_short_pct": 0, "net_position": "unknown"}

    def _clear_akshare_cache(self):
        """清除 AkShare 内部缓存中损坏的 zip 文件（按需触发，不全清）"""
        import tempfile
        akshare_cache = Path(tempfile.gettempdir()) / "akshare"
        if akshare_cache.exists():
            cleaned = 0
            for item in akshare_cache.iterdir():
                if not item.is_file():
                    continue
                if not (item.name.endswith(".zip") or item.name.endswith(".tmp")):
                    continue
                if item.stat().st_size == 0:
                    try:
                        item.unlink()
                        cleaned += 1
                    except Exception:
                        pass
            if cleaned:
                logger.info(f"已清理 AkShare 缓存中 {cleaned} 个损坏文件")
    
    def _try_fetch_position(self, sym: str, date_str: str) -> Dict[str, Any]:
        """尝试从指定日期获取持仓数据"""
        import akshare as ak
        
        dce_symbols = ["M", "Y", "P", "A", "B", "C", "CS", "JD", "L", "V", "PP", "J", "JM", "I", "EG", "PG", "EB", "LH"]  # RM属郑商所，已移除
        czce_symbols = ["CF", "SR", "TA", "MA", "RM", "OI", "RI", "WH", "PM", "JR", "LR", "SF", "SM", "ZC", "AP", "UR", "CJ", "SA"]
        
        try:
            if sym in czce_symbols:
                result = ak.get_rank_table_czce(date=date_str)
            elif sym in dce_symbols:
                result = ak.futures_dce_position_rank(date=date_str, vars_list=[sym])
            else:
                result = ak.get_shfe_rank_table(date=date_str)
            
            if isinstance(result, dict):
                candidates = []
                for key, df in result.items():
                    if isinstance(df, pd.DataFrame) and not df.empty:
                        if "variety" in df.columns:
                            target_data = df[df["variety"] == sym]
                        elif "symbol" in df.columns:
                            target_data = df[df["symbol"].str.startswith(sym)]
                        else:
                            target_data = df
                        
                        if not target_data.empty:
                            vol_score = 0.0
                            for col in ["long_open_interest", "short_open_interest"]:
                                if col in target_data.columns:
                                    s = target_data[col].astype(str).str.replace(",", "", regex=False)
                                    vol_score += pd.to_numeric(s, errors="coerce").sum()
                            candidates.append((vol_score, target_data))
                
                if candidates:
                    candidates.sort(key=lambda x: x[0], reverse=True)
                    best_df = candidates[0][1]
                    logger.info(f"持仓: 从{len(candidates)}个合约中选中主力(总持仓={candidates[0][0]:.0f}手)")
                    return self._parse_position_data(best_df, sym)
            elif isinstance(result, pd.DataFrame) and not result.empty:
                return self._parse_position_data(result, sym)
        except Exception as e:
            err_str = str(e)
            if "not a zip file" in err_str.lower() or "zip" in err_str.lower():
                logger.warning(f"持仓: {sym}({date_str}) AkShare缓存损坏(zip)，向上抛出触发清理")
                raise
            else:
                logger.warning(f"获取{sym}持仓数据({date_str})失败: {err_str[:150]}")
        
        return {"long_positions": [], "short_positions": [], "top5_long_pct": 0, "top5_short_pct": 0, "net_position": "unknown"}
    
    def _parse_position_data(self, df: pd.DataFrame, symbol: str) -> Dict[str, Any]:
        """解析持仓数据"""
        if df.empty:
            return {"long_positions": [], "short_positions": [], "top5_long_pct": 0, "top5_short_pct": 0, "net_position": "unknown"}
        
        # 多头持仓
        if "long_party_name" in df.columns and "long_open_interest" in df.columns:
            long_df = df[["long_party_name", "long_open_interest"]].dropna()
            long_df = long_df[long_df["long_party_name"].notna() & (long_df["long_party_name"] != "None")]
            long_df = long_df.sort_values("long_open_interest", ascending=False)
            long_positions = [
                {"member": row["long_party_name"], "volume": float(str(row["long_open_interest"]).replace(",", ""))}
                for _, row in long_df.iterrows()
            ]
        else:
            long_positions = []
        
        # 空头持仓
        if "short_party_name" in df.columns and "short_open_interest" in df.columns:
            short_df = df[["short_party_name", "short_open_interest"]].dropna()
            short_df = short_df[short_df["short_party_name"].notna() & (short_df["short_party_name"] != "None")]
            short_df = short_df.sort_values("short_open_interest", ascending=False)
            short_positions = [
                {"member": row["short_party_name"], "volume": float(str(row["short_open_interest"]).replace(",", ""))}
                for _, row in short_df.iterrows()
            ]
        else:
            short_positions = []
        
        # 计算集中度
        total_long = sum(p["volume"] for p in long_positions)
        total_short = sum(p["volume"] for p in short_positions)
        
        top5_long = sum(p["volume"] for p in long_positions[:5])
        top5_short = sum(p["volume"] for p in short_positions[:5])
        
        top5_long_pct = (top5_long / total_long * 100) if total_long > 0 else 0
        top5_short_pct = (top5_short / total_short * 100) if total_short > 0 else 0
        
        # 净持仓方向
        net_long = sum(p["volume"] for p in long_positions)
        net_short = sum(p["volume"] for p in short_positions)
        if net_long > net_short * 1.1:
            net_position = "long"
        elif net_short > net_long * 1.1:
            net_position = "short"
        else:
            net_position = "neutral"
        
        return {
            "long_positions": long_positions,
            "short_positions": short_positions,
            "top5_long_pct": round(top5_long_pct, 2),
            "top5_short_pct": round(top5_short_pct, 2),
            "net_position": net_position,
        }

    def get_news_data(
        self,
        symbol: str,
        days: int = 7,
    ) -> List[Dict[str, Any]]:
        """获取新闻数据

        Args:
            symbol: 品种代码
            days: 最近天数

        Returns:
            [{"title": 标题, "content": 内容, "date": 日期, "source": 来源}, ...]
        """
        cache_file = self.cache_dir / f"news_{symbol}_{days}.json"
        cache_ttl_minutes = 60  # 缓存有效期1小时

        if cache_file.exists():
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    cache_datetime = data.get("cached_datetime", "")
                    if cache_datetime:
                        cache_time = datetime.strptime(cache_datetime, "%Y-%m-%d %H:%M:%S")
                        age_minutes = (datetime.now() - cache_time).total_seconds() / 60
                        if age_minutes < cache_ttl_minutes:
                            return data.get("news", [])
            except Exception as e:
                logger.warning(f"加载新闻缓存失败: {e}")

        if self.enable_online:
            try:
                news = self._fetch_news_online(symbol, days)
                with open(cache_file, "w", encoding="utf-8") as f:
                    json.dump(
                        {"cached_datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "news": news},
                        f,
                        ensure_ascii=False,
                        indent=2,
                    )
                return news
            except Exception as e:
                logger.error(f"在线获取新闻数据失败: {e}")

        return []

    def _fetch_news_online(
        self,
        symbol: str,
        days: int,
    ) -> List[Dict[str, Any]]:
        """在线获取新闻数据
        
        使用 AkShare futures_news_shmet 接口获取期货新闻
        """
        import akshare as ak
        
        # 品种关键词映射
        keyword_map = {
            "RB": "螺纹钢", "HC": "热卷", "CU": "铜", "AL": "铝",
            "M": "豆粕", "RM": "菜粕", "Y": "豆油", "P": "棕榈油",
            "CF": "棉花", "SR": "白糖", "I": "铁矿石", "J": "焦炭",
            "JM": "焦煤", "RU": "橡胶", "SC": "原油", "AU": "黄金",
            "AG": "白银", "ZN": "锌", "NI": "镍", "SN": "锡",
        }
        
        try:
            # 先获取全部新闻
            df = ak.futures_news_shmet(symbol="全部")
            
            if df is None or df.empty:
                return []
            
            # 重命名列
            df = df.rename(columns={
                "发布时间": "date",
                "内容": "content",
            })
            
            # 提取标题（取内容前50字）
            df["title"] = df["content"].str[:50]
            
            # 转换日期（处理时区）
            df["date"] = pd.to_datetime(df["date"]).dt.tz_convert("Asia/Shanghai").dt.tz_localize(None)
            
            # 筛选近N天的新闻
            from datetime import datetime, timedelta
            cutoff = datetime.now() - timedelta(days=days)
            df = df[df["date"] >= cutoff]
            
            # 如果指定了品种，尝试筛选；如果没匹配到则返回所有新闻
            if symbol.upper() in keyword_map:
                keyword = keyword_map[symbol.upper()]
                filtered = df[df["content"].str.contains(keyword, na=False)]
                # 如果筛选有结果就用筛选结果，否则返回全部
                if not filtered.empty:
                    df = filtered
            
            # 转换为列表
            news_list = []
            for _, row in df.iterrows():
                news_list.append({
                    "title": row["title"],
                    "content": row["content"],
                    "date": row["date"].strftime("%Y-%m-%d %H:%M"),
                    "source": "上海金属网",
                })
            
            return news_list
            
        except Exception as e:
            logger.error(f"获取新闻数据失败: {e}")
        
        return []

    def get_all_data(
        self,
        symbol: str,
        date: Optional[str] = None,
        news_days: int = 7,
    ) -> Dict[str, Any]:
        """一键获取所有数据

        Args:
            symbol: 品种代码
            date: 分析日期，默认今天
            news_days: 新闻回溯天数

        Returns:
            {
                "price": DataFrame,
                "basis": DataFrame,
                "term_structure": dict,
                "inventory": DataFrame,
                "position": dict,
                "news": list,
            }
        """
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")

        start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")

        return {
            "price": self.get_price_data(symbol, start_date, date),
            "basis": self.get_basis_data(symbol, start_date, date),
            "term_structure": self.get_term_structure_data(symbol, date),
            "inventory": self.get_inventory_data(symbol, start_date, date),
            "position": self.get_position_data(symbol, date),
            "news": self.get_news_data(symbol, news_days),
        }


# 便捷函数
def create_data_provider(
    cache_dir: Optional[str] = None,
    enable_online: bool = False,
) -> DataProvider:
    """工厂函数：创建数据提供器"""
    return DataProvider(cache_dir=cache_dir, enable_online=enable_online)


# 缓存管理工具
def clear_cache(cache_dir: Optional[str] = None) -> int:
    """清空缓存目录

    Returns:
        清理的文件数量
    """
    cache_dir = Path(cache_dir) if cache_dir else Path.home() / ".trading_agent_cache"
    if not cache_dir.exists():
        return 0

    count = 0
    for f in cache_dir.iterdir():
        if f.is_file():
            f.unlink()
            count += 1
    return count


def get_cache_size(cache_dir: Optional[str] = None) -> str:
    """获取缓存目录大小

    Returns:
        人类可读的大小字符串
    """
    cache_dir = Path(cache_dir) if cache_dir else Path.home() / ".trading_agent_cache"
    if not cache_dir.exists():
        return "0 B"

    total = sum(f.stat().st_size for f in cache_dir.iterdir() if f.is_file())
    for unit in ["B", "KB", "MB", "GB"]:
        if total < 1024:
            return f"{total:.1f} {unit}"
        total /= 1024
    return f"{total:.1f} TB"