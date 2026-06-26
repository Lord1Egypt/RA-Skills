#!/usr/bin/env python3
"""Production orchestration pipeline for strategy generation/backtesting."""

from __future__ import annotations

import argparse
import io
import ipaddress
import json
import os
import platform
import signal
import re
import shutil
import socket
import subprocess
import sys
import time
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
from urllib.error import URLError
from urllib.parse import quote, urlencode, urlparse
from urllib.request import Request, urlopen

try:
    from dateutil.relativedelta import relativedelta
except ImportError:
    relativedelta = None  # type: ignore[assignment,misc]

from data_capability_guard import evaluate_requirement

PROJECT_ROOT = Path(os.getenv("QUANTCLAW_ROOT", "") or os.getenv("QMT_PROJECT_ROOT", "") or str(Path(__file__).resolve().parents[1])).resolve()
BACKTESTS_DIR = PROJECT_ROOT / "backtests"
STRATEGIES_DIR = PROJECT_ROOT / "strategies"
RUNS_DIR = BACKTESTS_DIR / "orchestrator_runs"
RUNS_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_PYTHON_BIN = os.getenv("PYTHON_BIN", sys.executable or "python3")
MONITOR_SERVER = BACKTESTS_DIR / "monitor_server.py"
BACKTEST_RUNNER = BACKTESTS_DIR / "backtest_runner.py"
STATE_VERSION = 1
MONITOR_BIND_HOST = os.getenv("ORCH_MONITOR_BIND_HOST", "0.0.0.0")
DEFAULT_REPORT_PUBLIC_DIR = (BACKTESTS_DIR / "public_reports").resolve()


def now_iso() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def atomic_json_write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)


def read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(str(path))
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_symbol(raw: str) -> str:
    val = raw.strip().upper()
    if re.fullmatch(r"\d{6}", val):
        if val.startswith("6") or val.startswith("900"): return f"{val}.SSE" #沪市主板+B股
        if val.startswith(("83", "43", "87", "920")): return f"{val}.BSE" #北交所
        return f"{val}.SZSE"
    for old, new in {".SH": ".SSE", ".SS": ".SSE", ".SZ": ".SZSE", ".BJ": ".BSE"}.items():
        if val.endswith(old): return val[:-len(old)] + new
    if re.fullmatch(r"\d{6}\.(SSE|SZSE|BSE)", val): return val #已是标准格式
    return "" #非合法代码返回空，防止池名/中文名穿透


def read_env_value_from_files(key: str, candidates: list[Path]) -> str:
    for path in candidates:
        if not path.exists():
            continue
        try:
            for line in path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                if k.strip() == key:
                    return v.strip().strip('"').strip("'")
        except Exception:
            continue
    return ""


def extract_token_from_chat(text: str) -> str:
    """从用户对话文本中提取疑似qgdata token"""
    m = QGDATA_TOKEN_RE.search(text or "")
    return m.group(0) if m else ""

def resolve_qgdata_token(explicit_token: str, chat_text: str = "") -> tuple[str, str]:
    """解析token → (token, source)。source: user_arg|user_chat|env|shared"""
    if explicit_token and len(explicit_token.strip()) >= 20:
        return explicit_token.strip(), "user_arg"
    chat_token = extract_token_from_chat(chat_text)
    if chat_token:
        return chat_token, "user_chat"
    env_token = os.getenv("QGDATA_TOKEN", "")
    if env_token:
        return env_token, "env"
    file_token = read_env_value_from_files("QGDATA_TOKEN", [PROJECT_ROOT / ".env", Path.home() / ".openclaw" / ".env", Path("/opt/.env")])
    if file_token:
        return file_token, "env"
    return QGDATA_SHARED_TOKEN, "shared"


def resolve_monitor_public_base(explicit_base: str) -> str:
    """解析监控公网基址（优先显式参数，其次环境变量/配置文件/控制台URL推导）"""
    if explicit_base and explicit_base.strip():
        return explicit_base.strip().rstrip("/")
    env_base = os.getenv("MONITOR_PUBLIC_BASE", "").strip()
    if env_base:
        return env_base.rstrip("/")
    file_base = read_env_value_from_files(
        "MONITOR_PUBLIC_BASE",
        [PROJECT_ROOT / ".env", Path.home() / ".openclaw" / ".env", Path("/opt/.env")],
    ).strip()
    if file_base:
        return file_base.rstrip("/")
    control_url = (
        os.getenv("OPENCLAW_CONTROL_URL", "").strip()
        or read_env_value_from_files(
            "OPENCLAW_CONTROL_URL",
            [PROJECT_ROOT / ".env", Path.home() / ".openclaw" / ".env", Path("/opt/.env")],
        ).strip()
    )
    if control_url:
        try:
            pu = urlparse(control_url)
            if pu.scheme in ("http", "https") and pu.hostname:
                port = f":{pu.port}" if pu.port else ""
                return f"{pu.scheme}://{pu.hostname}{port}"
        except Exception:
            pass
    return ""


from qg_constants import QGDATA_RECHARGE_URL, QGDATA_SHARED_TOKEN, QGDATA_TOKEN_RE, mask_token, classify_qgdata_error, qg_call, qg_throttle


def resolve_symbols_by_name(requirement: str, token: str) -> tuple[list[str], str]:
    """按中文名解析股票代码→(代码列表, 警告信息)"""
    candidates = re.findall(r"[\u4e00-\u9fff]{2,10}", requirement)
    if not candidates: return [], ""
    stop_words = {"策略","回测","买入","卖出","上穿","下穿","均线","日线","分钟","执行","自动","编排","监控","链接","股价","股票","交易","选股","市场","全市场","组合","轮动","设计","低于","高于","每天","每周","每月","以上","以下","成分股","龙虎榜","涨停","跌停"}
    _sw_re = re.compile("|".join(re.escape(w) for w in sorted(stop_words, key=len, reverse=True)))
    names = [c for c in candidates if _sw_re.sub("", c)]
    if not names: return [], ""
    if not token: return [], f"检测到股票名称「{'、'.join(names[:3])}」但未配置数据Token。请到 {QGDATA_RECHARGE_URL} 获取Token"
    try:
        import qgdata as qg
        qg.set_token(token); pro = qg.pro_api(timeout=8.0)
        df = qg_call(lambda: pro.stock_basic(exchange="", list_status="L", fields="ts_code,name"))
        if df is None or len(df) == 0:
            return [], f"qgdata API 返回空数据（查询股票名「{'、'.join(names[:3])}」），可能Token额度不足。充值地址: {QGDATA_RECHARGE_URL}"
        all_rows = [(str(r["name"]), str(r["ts_code"])) for _, r in df.iterrows()]
        out, seen = [], set()
        for name in names:
            exact = [ts for nm, ts in all_rows if nm == name]
            if exact: s = normalize_symbol(exact[0]);
            else:
                fuzzy = [ts for nm, ts in all_rows if name in nm]
                s = normalize_symbol(fuzzy[0]) if len(fuzzy) == 1 else ""
            if s and s not in seen: seen.add(s); out.append(s)
        return out, ""
    except Exception as exc:
        _, user_msg = classify_qgdata_error(exc)
        return [], f"按名称查询股票失败: {user_msg}"


# ─── 板块/指数/概念 静态映射（全部经 pro.ths_index() 实际查询验证） ───
THS_SECTOR_MAP: dict[str, str] = {
    "人工智能": "885728.TI", "新能源汽车": "885431.TI", "芯片": "885756.TI",
    "光伏": "885531.TI", "锂电池": "885710.TI", "白酒": "885525.TI",
    "军工": "885700.TI", "数字经济": "885976.TI", "机器人": "885517.TI",
    "储能": "885921.TI", "消费电子": "885800.TI", "华为概念": "885806.TI",
    "鸿蒙": "885923.TI", "ChatGPT": "886031.TI", "AIGC": "886019.TI",
    "6G": "886037.TI", "物联网": "885312.TI", "元宇宙": "885934.TI",
    "氢能源": "885823.TI", "碳中和": "885919.TI", "工业母机": "885930.TI",
    "特高压": "885425.TI", "充电桩": "885461.TI", "无人驾驶": "885736.TI",
    "智能穿戴": "885454.TI", "信创": "886013.TI", "低空经济": "886067.TI",
    "飞行汽车": "886066.TI", "数据要素": "886041.TI", "量子科技": "885730.TI",
    "算力": "885957.TI",
    "银行": "881155.TI", "券商": "881157.TI", "保险": "881156.TI",
    "房地产": "881153.TI", "钢铁": "881112.TI", "煤炭": "881105.TI",
    "建材": "881115.TI", "化工": "881109.TI", "电力": "881145.TI",
    "石油": "881180.TI", "水泥": "884060.TI", "农业": "881101.TI",
    "医疗": "881175.TI", "家电": "881131.TI", "纺织服装": "881136.TI",
    "传媒": "881164.TI", "计算机": "881130.TI", "通信": "881129.TI",
    "汽车": "881125.TI", "汽车零部件": "881126.TI", "机械": "881117.TI",
    "建筑": "881116.TI", "零售": "881158.TI", "社会服务": "881179.TI",
    "综合": "881165.TI", "环保": "881181.TI", "半导体": "881121.TI",
    "沪深300": "883300.TI", "中证500": "883304.TI", "上证50": "883301.TI",
}
THS_SECTOR_ALIASES: dict[str, str] = { #同义词→标准关键词
    "新能源": "新能源汽车", "医药": "医疗", "量子计算": "量子科技",
    "食品饮料": "白酒", "证券": "券商", "eVTOL": "飞行汽车",
    "东数西算": "算力", "第三代半导体": "半导体",
}
_SECTOR_KEYS_DESC = sorted(list(THS_SECTOR_MAP.keys()) + list(THS_SECTOR_ALIASES.keys()), key=len, reverse=True) #按长度降序，最长优先匹配
INDEX_KW_MAP: dict[str, dict] = { #指数成分股双路径映射
    "沪深300": {"ths": "883300.TI", "em_code": "000300", "approx": 300},
    "中证500": {"ths": "883304.TI", "em_code": "000905", "approx": 500},
    "上证50":  {"ths": "883301.TI", "em_code": "000016", "approx": 50},
    "中证1000": {"ths": None, "em_code": "000852", "approx": 1000},
    "创业板指": {"ths": None, "em_code": "399006", "approx": 100},
}
_SECTOR_CACHE_DIR = BACKTESTS_DIR / ".sector_cache"
_SECTOR_SUFFIX_RE = re.compile(r"([\u4e00-\u9fa5A-Za-z0-9]{2,8})(板块|行业|概念|主题|赛道|题材|成分股)")
_SECTOR_CONTEXT_RE = re.compile(r"(?:板块|行业|概念|主题|赛道|题材|成分股|股|选股|轮动|龙头|指数)") #2字符key需后跟此上下文
_SECTOR_EXCLUDE_WORDS = re.compile(r"^(?:一个|这个|那个|某个|每个|各个|整个|全部|所有|多个|最近|过去|设计|做一个|选一个|找一个|每天|每周|每月|本月|本周|本季|今年|去年|回测|策略)")
_SECTOR_ONLY_DIGITS_RE = re.compile(r"^[\d.]+$")


def _sector_cache_read(code: str) -> list[str] | None:
    """读取按日缓存的板块成分股，None=无缓存"""
    _SECTOR_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    today_str = date.today().strftime("%Y%m%d")
    cache_file = _SECTOR_CACHE_DIR / f"{code}_{today_str}.json"
    if cache_file.exists():
        try:
            return json.loads(cache_file.read_text("utf-8"))
        except Exception:
            pass
    return None


def _sector_cache_write(code: str, symbols: list[str]) -> None:
    """写入按日缓存，同时清理过期文件（保留最近3天）"""
    _SECTOR_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    today_str = date.today().strftime("%Y%m%d")
    cache_file = _SECTOR_CACHE_DIR / f"{code}_{today_str}.json"
    try:
        cache_file.write_text(json.dumps(symbols, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass
    try: #清理3天前的缓存
        cutoff = (date.today() - timedelta(days=3)).strftime("%Y%m%d")
        for f in _SECTOR_CACHE_DIR.glob(f"{code}_*.json"):
            d = f.stem.split("_")[-1]
            if d < cutoff:
                f.unlink(missing_ok=True)
    except Exception:
        pass


def _ths_member_symbols(ts_code: str, token: str) -> list[str]:
    """调用 ths_member 获取成分股代码列表（已 normalize）"""
    import qgdata as qg
    qg.set_token(token); pro = qg.pro_api(timeout=15)
    df = qg_call(lambda: pro.ths_member(ts_code=ts_code, fields="ts_code,con_code,con_name,is_new"))
    if df is None or df.empty:
        return []
    active = df[df["is_new"] == "Y"] if "is_new" in df.columns and not df[df["is_new"] == "Y"].empty else df
    return [s for s in (normalize_symbol(str(c)) for c in active["con_code"].tolist() if c) if s]


def _resolve_index_members_em(index_code: str) -> list[str]:
    """东方财富公开API获取指数成分股（降级路径，无额度限制）"""
    all_codes: list[str] = []; page = 1
    while True:
        url = (
            f"https://datacenter-web.eastmoney.com/api/data/v1/get?"
            f"reportName=RPT_INDEX_COMPONENT&columns=SECURITY_CODE%2CINDEX_CODE"
            f"&filter=%28INDEX_CODE%3D%22{index_code}%22%29"
            f"&pageSize=500&pageNumber={page}&sortColumns=SECURITY_CODE&sortTypes=1"
        )
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=15) as resp:
            body = json.loads(resp.read().decode("utf-8", errors="ignore"))
        result = body.get("result") or {}
        rows = result.get("data") or []
        for r in rows:
            sc = str(r.get("SECURITY_CODE", "")).zfill(6)
            suffix = "SSE" if sc.startswith("6") else "SZSE"
            all_codes.append(f"{sc}.{suffix}")
        total_pages = result.get("pages", 1)
        if page >= total_pages:
            break
        page += 1
    return all_codes


def _resolve_index_members(kw: str, info: dict, token: str) -> tuple[list[str], str]:
    """指数成分股双路径：ths_member主 → 东方财富降级"""
    ths_code, em_code = info.get("ths"), info["em_code"]
    cached = _sector_cache_read(ths_code or em_code)
    if cached:
        print(f"[pool] 指数「{kw}」成分股命中缓存({len(cached)}只)")
        return cached, ""
    if ths_code and token: #主路径
        try:
            syms = _ths_member_symbols(ths_code, token)
            if syms:
                _sector_cache_write(ths_code, syms)
                print(f"[pool] 指数「{kw}」→ths_member({ths_code})={len(syms)}只")
                return syms, ""
        except Exception as e:
            code, msg = classify_qgdata_error(e)
            print(f"[WARN] 指数「{kw}」ths_member失败({code}): {msg}，降级到公开接口")
    try: #降级路径
        syms = _resolve_index_members_em(em_code)
        if syms:
            _sector_cache_write(ths_code or em_code, syms)
            print(f"[pool] 指数「{kw}」→东方财富公开API={len(syms)}只")
            return syms, ""
        return [], f"指数「{kw}」成分股获取为空"
    except Exception as e:
        return [], f"指数「{kw}」成分股获取失败: {e}"


def _extract_sector_name(txt: str) -> str | None:
    """从需求文本提取板块/行业/概念关键词，最长匹配优先"""
    txt_norm = re.sub(r"\s+", "", txt)
    for key in _SECTOR_KEYS_DESC: #步骤1：静态映射key+别名key最长子串匹配
        if key not in txt_norm:
            continue
        if len(key) <= 2: #2字符短key需后跟板块上下文词，防止"综合表现"误匹配"综合"行业
            idx = txt_norm.index(key) + len(key)
            after = txt_norm[idx:idx + 4] if idx < len(txt_norm) else ""
            if not _SECTOR_CONTEXT_RE.match(after):
                continue
        return THS_SECTOR_ALIASES.get(key, key)
    m = _SECTOR_SUFFIX_RE.search(txt_norm) #步骤2：正则提取带后缀的板块名
    if m:
        name = m.group(1)
        if len(name) < 2 or _SECTOR_EXCLUDE_WORDS.match(name) or _SECTOR_ONLY_DIGITS_RE.match(name):
            return None
        canonical = THS_SECTOR_ALIASES.get(name, name)
        if canonical in THS_SECTOR_MAP:
            return canonical
        return name #可能需要API模糊搜索
    return None


def _resolve_sector_members(sector_name: str, token: str) -> tuple[list[str], str]:
    """板块/行业/概念成分股解析：静态映射→缓存→API模糊搜索"""
    ts_code = THS_SECTOR_MAP.get(sector_name)
    if ts_code: #静态映射命中
        cached = _sector_cache_read(ts_code)
        if cached:
            print(f"[pool] 板块「{sector_name}」命中缓存({len(cached)}只)")
            return cached, ""
        if not token:
            return [], f"检测到「{sector_name}」板块但未配置数据Token。请到 {QGDATA_RECHARGE_URL} 获取Token"
        try:
            syms = _ths_member_symbols(ts_code, token)
            if syms:
                _sector_cache_write(ts_code, syms)
                print(f"[pool] 板块「{sector_name}」→ths_member({ts_code})={len(syms)}只")
                return syms, ""
            return [], f"板块「{sector_name}」({ts_code})成分股为空"
        except Exception as e:
            code, msg = classify_qgdata_error(e)
            return [], f"板块「{sector_name}」获取失败: {msg}"
    if not token: #API模糊搜索需要token
        return [], f"检测到「{sector_name}」板块但未配置数据Token。请到 {QGDATA_RECHARGE_URL} 获取Token"
    try: #静态映射未命中→API模糊搜索
        import qgdata as qg
        qg.set_token(token); pro = qg.pro_api(timeout=15)
        best_code, best_name = None, None
        for tp in ("N", "I"):
            df = qg_call(lambda: pro.ths_index(exchange="A", type=tp, fields="ts_code,name"))
            if df is None or df.empty:
                continue
            exact = df[df["name"] == sector_name]
            if not exact.empty:
                best_code = str(exact.iloc[0]["ts_code"]); best_name = str(exact.iloc[0]["name"]); break
            contains = df[df["name"].str.contains(sector_name, na=False)]
            if not contains.empty and best_code is None:
                best_code = str(contains.iloc[0]["ts_code"]); best_name = str(contains.iloc[0]["name"])
        if not best_code:
            return [], ""
        syms = _ths_member_symbols(best_code, token)
        if syms:
            _sector_cache_write(best_code, syms)
            print(f"[pool] 板块「{sector_name}」→API搜索到「{best_name}」({best_code})={len(syms)}只")
        return syms, ""
    except Exception as e:
        code, msg = classify_qgdata_error(e)
        return [], f"板块「{sector_name}」搜索失败: {msg}"


_BSE_KW_RE = re.compile(r"北交所|北证|BSE|北京证券交易所", re.IGNORECASE) #北交所关键词

def _filter_bse(syms: list[str], txt: str) -> tuple[list[str], int]:
    """用户未提及北交所时剔除.BSE/.BJ标的→(过滤后列表, 剔除数)"""
    if _BSE_KW_RE.search(txt): return syms, 0
    kept = [s for s in syms if not s.endswith((".BSE", ".BJ"))]
    return kept, len(syms) - len(kept)

def _resolve_stock_pool(txt: str, token: str, max_stocks: int = 500) -> tuple[list[str], str]:
    """统一股票池解析入口→(代码列表, 警告信息)。优先级：指数→板块→全市场关键词"""
    txt_norm = re.sub(r"\s+", "", txt)
    for kw, info in INDEX_KW_MAP.items(): #第1级：指数关键词
        if kw in txt_norm:
            syms, warn = _resolve_index_members(kw, info, token)
            if syms or warn:
                syms, n_bse = _filter_bse(syms, txt)
                if n_bse: warn = (warn + f" " if warn else "") + f"(已剔除{n_bse}只北交所标的，需开通北交所权限请明确指定)"
                return syms, warn
    sector_name = _extract_sector_name(txt) #第2级：板块/行业/概念
    if sector_name and sector_name not in INDEX_KW_MAP:
        syms, warn = _resolve_sector_members(sector_name, token)
        if syms or warn:
            syms, n_bse = _filter_bse(syms, txt)
            if n_bse: warn = (warn + f" " if warn else "") + f"(已剔除{n_bse}只北交所标的，需开通北交所权限请明确指定)"
            return syms, warn
    pool_kw = {"全市场": "", "沪深主板": "主板", "创业板": "创业板", "科创板": "科创板"} #第3级：市场关键词
    matched = ""
    for kw in pool_kw:
        if kw in txt_norm:
            matched = kw; break
    if not matched:
        return [], ""
    if not token:
        return [], f"检测到「{matched}」选股但未配置数据Token，无法获取股票列表。请到 {QGDATA_RECHARGE_URL} 获取Token"
    try:
        import qgdata as qg
        qg.set_token(token); pro = qg.pro_api(timeout=10)
        df = qg_call(lambda: pro.stock_basic(exchange="", list_status="L", fields="ts_code,name,market"))
        if df is None or len(df) == 0:
            return [], f"「{matched}」选股：qgdata API 返回空数据，可能Token额度不足。充值地址: {QGDATA_RECHARGE_URL}"
        if matched == "科创板": df = df[df["market"] == "科创板"]
        elif matched == "创业板": df = df[df["market"] == "创业板"]
        else: df = df[df["market"].isin(["主板", "创业板"])]
        try: cap = max(1, int(os.getenv("QC_POOL_MAX_STOCKS", str(max_stocks)) or max_stocks))
        except Exception: cap = max_stocks
        ts_codes = df["ts_code"].tolist()
        if len(ts_codes) > cap:
            try:
                mv = None
                for i in range(7):
                    _td = (datetime.now() - timedelta(days=i)).strftime("%Y%m%d")
                    mv = qg_call(lambda: pro.daily_basic(trade_date=_td, fields="ts_code,total_mv"))
                    if mv is not None and not mv.empty: break
                if mv is not None and not mv.empty:
                    mv = mv.drop_duplicates("ts_code").set_index("ts_code")
                    df = df.copy(); df["_mv"] = df["ts_code"].map(mv["total_mv"])
                    ts_codes = df.sort_values("_mv", ascending=False, na_position="last")["ts_code"].head(cap).tolist()
                else: ts_codes = ts_codes[:cap]
            except Exception: ts_codes = ts_codes[:cap]
        syms = [s for s in (normalize_symbol(str(c)) for c in ts_codes) if s]
        syms, n_bse = _filter_bse(syms, txt)
        bse_msg = f"(已剔除{n_bse}只北交所标的，需开通北交所权限请明确指定)" if n_bse else ""
        return syms, bse_msg
    except Exception as exc:
        code, user_msg = classify_qgdata_error(exc)
        return [], f"「{matched}」选股失败: {user_msg}"

# ─── 日期关键词解析（双保险第二层：正则兜底） ───
_CN_NUM: dict[str, float] = {"一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十": 10, "半": 0.5}
_CN_NUM_RE = re.compile("|".join(re.escape(k) for k in _CN_NUM))


def _cn_to_num(txt: str) -> str:
    """将中文数字替换为阿拉伯数字，'半'→'0.5'"""
    return _CN_NUM_RE.sub(lambda m: str(_CN_NUM[m.group()]), txt)


def _parse_date_range(txt: str) -> tuple[str, str] | None:
    """从需求文本提取日期范围→("YYYYMMDD","YYYYMMDD") 或 None"""
    today = date.today()
    t = _cn_to_num(re.sub(r"\s+", "", txt))
    fmt = lambda d: d.strftime("%Y%m%d")  # noqa: E731
    def _sub_months(d: date, n: int) -> date:
        if relativedelta:
            return d - relativedelta(months=n)
        return d - timedelta(days=n * 30)
    def _sub_years(d: date, n: int) -> date:
        if relativedelta:
            return d - relativedelta(years=n)
        return d - timedelta(days=n * 365)
    m = re.search(r"(\d{8})\s*[-~至到]\s*(\d{8})", t) #P1: YYYYMMDD-YYYYMMDD
    if m:
        try:
            s = datetime.strptime(m.group(1), "%Y%m%d").date()
            e = datetime.strptime(m.group(2), "%Y%m%d").date()
            return fmt(s), fmt(e)
        except ValueError:
            pass
    m = re.search(r"(\d{4})-(\d{1,2})-(\d{1,2})\s*[-~至到]\s*(\d{4})-(\d{1,2})-(\d{1,2})", txt) #P1b: YYYY-MM-DD ~ YYYY-MM-DD
    if m:
        try:
            s = date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
            e = date(int(m.group(4)), int(m.group(5)), int(m.group(6)))
            return fmt(s), fmt(e)
        except ValueError:
            pass
    m = re.search(r"从?(\d{4})年(\d{1,2})月.*?[到至](\d{4})年(\d{1,2})月", t) #P2: 从YYYY年M月到YYYY年M月
    if m:
        try:
            s = date(int(m.group(1)), int(m.group(2)), 1)
            e_y, e_m = int(m.group(3)), int(m.group(4))
            if e_m == 12: e = date(e_y, 12, 31)
            else: e = date(e_y, e_m + 1, 1) - timedelta(days=1)
            return fmt(s), fmt(e)
        except ValueError:
            pass
    m = re.search(r"(\d{4})年以来", t) #P3: YYYY年以来
    if m:
        return fmt(date(int(m.group(1)), 1, 1)), fmt(today)
    if "今年以来" in t: #P4
        return fmt(date(today.year, 1, 1)), fmt(today)
    if "去年以来" in t: #P5
        return fmt(date(today.year - 1, 1, 1)), fmt(today)
    if "本月以来" in t: #P6
        return fmt(today.replace(day=1)), fmt(today)
    if "本季度以来" in t: #P7
        q_month = ((today.month - 1) // 3) * 3 + 1
        return fmt(date(today.year, q_month, 1)), fmt(today)
    m = re.search(r"(?:最近|近|过去)\s*(\d+(?:\.\d+)?)\s*年0\.5", t) #P13: 最近N年半（'半'已被_cn_to_num转为0.5）
    if m:
        n = float(m.group(1))
        return fmt(_sub_months(today, int(n * 12 + 6))), fmt(today)
    m = re.search(r"(?:最近|近|过去)\s*(\d+(?:\.\d+)?)\s*年", t) #P8: 最近N年
    if m:
        n = float(m.group(1))
        if n == 0.5:
            return fmt(_sub_months(today, 6)), fmt(today)
        return fmt(_sub_years(today, int(n))), fmt(today)
    m = re.search(r"(?:最近|近|过去)\s*(\d+(?:\.\d+)?)\s*(?:个月|月)", t) #P9: 最近N个月
    if m:
        return fmt(_sub_months(today, int(float(m.group(1))))), fmt(today)
    m = re.search(r"(?:最近|近|过去)\s*(\d+(?:\.\d+)?)\s*周", t) #P10: 最近N周
    if m:
        return fmt(today - timedelta(weeks=int(float(m.group(1))))), fmt(today)
    m = re.search(r"(?:最近|近|过去)\s*(\d+)\s*(?:天|个交易日)", t) #P11: 最近N天
    if m:
        return fmt(today - timedelta(days=int(m.group(1)))), fmt(today)
    if re.search(r"(?:最近|近).*?0.5\s*年", t): #P12: 最近半年（中文'半'已转为0.5）
        return fmt(_sub_months(today, 6)), fmt(today)
    return None


def _extract_symbols_from_source(source: str) -> list[str]:
    """从策略源码提取硬编码的 vt_symbol 列表（如 '600519.SH'），用于与 parsed['symbols'] 对齐"""
    hits = re.findall(r'["\'](\d{6})\.(SH|SZ|SSE|SZSE|BSE|BJ)["\']', source)
    seen, out = set(), []
    for code, suffix in hits:
        vt = normalize_symbol(f"{code}.{suffix}")
        if vt and vt not in seen: seen.add(vt); out.append(vt)
    return out

def parse_requirement(requirement: str, symbols_override: Optional[str], token: str = "") -> Dict[str, Any]:
    txt = requirement.strip(); pool_warn = ""
    symbol_matches = re.findall(r"(?<!\d)(\d{6}\.(?:SZSE|SSE|SZ|SH|SS)|\d{6})(?!\d)", txt, flags=re.IGNORECASE)
    symbols = [s for s in (normalize_symbol(m) for m in symbol_matches) if s]
    if symbols_override:
        symbols = [s for s in (normalize_symbol(x) for x in symbols_override.split(",") if x.strip()) if s] #过滤空值（池名/中文名）
    pool_api_failed = False
    if not symbols:
        name_syms, name_warn = resolve_symbols_by_name(txt, token)
        if name_syms: symbols = name_syms
        elif name_warn: pool_warn = name_warn; print(f"[WARN] {name_warn}")
    if not symbols:
        pool, pw = _resolve_stock_pool(txt, token)
        if pool: symbols = pool
        elif pw: pool_warn = pool_warn or pw; pool_api_failed = True; print(f"[ERROR] {pw}")
        else: symbols = ["000001.SZSE"]
    if not symbols: symbols = ["000001.SZSE"]

    ma_kw = ["均线", "上穿", "下穿", "金叉", "死叉", "SMA", "sma", "EMA", "ema", "日线交叉", "移动平均"]
    is_ma = any(k in txt for k in ma_kw) or bool(re.search(r'\bMA\b(?!CD)', txt))
    result: Dict[str, Any] = {"symbols": symbols}
    if pool_warn: result["pool_warning"] = pool_warn
    if pool_api_failed: result["data_blocked"] = True
    if is_ma: #双均线专属参数，仅供内置兜底模板使用，不暴露给监控页
        windows = [int(m.group(1)) for m in re.finditer(r"(\d+)\s*日", txt)]
        if len(windows) >= 2: fw, sw = sorted(windows[:2])
        elif len(windows) == 1: fw, sw = max(5, windows[0] // 2), windows[0]
        else: fw, sw = 5, 10
        result["_ma_fallback"] = {"fast_window": fw, "slow_window": sw}

    min_match = re.search(r"(\d+)\s*分钟|(\d+)\s*min", txt, re.IGNORECASE)
    if any(k in txt for k in ["60分钟", "小时", "hour", "1h", "60min"]):
        interval = "HOUR"
    elif min_match:
        mins = int(min_match.group(1) or min_match.group(2))
        interval = {5: "5MIN", 15: "15MIN", 30: "30MIN", 1: "MINUTE"}.get(mins, "5MIN")
    elif "分钟" in txt:
        interval = "5MIN"
    elif "周" in txt and any(k in txt for k in ["周线", "周级别", "每周", "周K"]):
        interval = "WEEKLY"
    else:
        interval = "DAILY"
    _direction = "bearish" if any(k in txt for k in ["下穿", "死叉"]) else "bullish" #仅兜底模板用
    _strong_kw = ["轮动", "组合", "多标的", "portfolio", "多只", "全市场", "等权", "仓位分配"] #任一即portfolio
    _weak_kw = ["排序", "筛选", "选股", "调仓", "排列", "持仓周期"] #需配合pool上下文
    _pool_re = re.compile(r"板块|成分股|指数|行业|概念|股票池")
    _has_strong = any(k in txt for k in _strong_kw) or bool(re.search(r"前\d+名", txt))
    _has_pool = bool(_pool_re.search(txt))
    _has_weak = any(k in txt for k in _weak_kw)
    mode = "portfolio" if (len(symbols) > 1 or _has_strong or (_has_pool and _has_weak)) else "cta"
    if mode == "portfolio" and interval == "WEEKLY": #引擎驱动不支持WEEKLY，自动降为DAILY（策略内部可用pro.weekly()取周线数据）
        interval = "DAILY"; print("[parse] portfolio+WEEKLY → 引擎驱动降为DAILY（周线数据策略可通过pro.weekly()直接获取）")
    result.update({"interval": interval, "mode": mode})
    result.setdefault("_ma_fallback", {})["direction"] = _direction #兜底模板专属
    dr = _parse_date_range(txt) #日期关键词兜底解析
    if dr:
        result["start"], result["end"] = dr
        print(f"[parse] 日期关键词解析: {dr[0]} ~ {dr[1]}")
    return result


DEFAULT_MONITOR_PORTS = [8767]  # 白名单端口，必须在防火墙/安全组中放通


def pick_free_port(candidates: Optional[list[int]] = None) -> int:
    ports = candidates or DEFAULT_MONITOR_PORTS
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if sock.connect_ex(("127.0.0.1", port)) != 0:
                return port
    tried = ",".join(str(p) for p in ports)
    raise RuntimeError(f"白名单端口均被占用({tried})，请释放端口或通过 ORCH_MONITOR_PORT_CANDIDATES 扩展白名单")

def _is_port_busy(port: int, host: str = "127.0.0.1") -> bool:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.8); return sock.connect_ex((host, int(port))) == 0
    except Exception: return False

def _read_monitor_state_by_port(port: int, timeout: float = 0.8) -> Optional[Dict[str, Any]]:
    try:
        with urlopen(f"http://127.0.0.1:{int(port)}/api/state", timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="ignore"))
            return data if isinstance(data, dict) else None
    except Exception: return None

def _kill_port_process(port: int) -> bool:
    if not _is_port_busy(port): return True
    for _ in range(3):
        try: subprocess.run(f"lsof -ti:{int(port)} | xargs -r kill -9 2>/dev/null || fuser -k {int(port)}/tcp 2>/dev/null", shell=True, timeout=5, capture_output=True, text=True)
        except Exception: pass
        time.sleep(0.4)
        if not _is_port_busy(port): return True
    return False

def try_reclaim_done_monitor_ports(candidates: list[int]) -> list[int]:
    reclaimed = []
    for p in candidates:
        if not _is_port_busy(p): continue
        st = _read_monitor_state_by_port(p)
        if not st: continue
        done = bool(st.get("done")) or str(st.get("status", "")).lower() in {"done", "failed", "completed"}
        if done and _kill_port_process(p): reclaimed.append(p)
    return reclaimed


def monitor_get(base_url: str, path: str, timeout: float = 3.0) -> Optional[str]:
    try:
        with urlopen(f"{base_url}{path}", timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="ignore")
    except Exception:
        return None


def monitor_post(base_url: str, path: str, payload: Dict[str, Any], timeout: float = 5.0) -> bool:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = Request(
        f"{base_url}{path}",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(req, timeout=timeout):
            return True
    except URLError:
        return False


def monitor_step(base_url: str, *, step: str, status: str, title: str, msg: str, run_id: str) -> None:
    qs = urlencode({"step": step, "status": status, "title": title, "msg": msg, "run_id": run_id})
    monitor_get(base_url, f"/api/step?{qs}", timeout=2.0)


def probe_monitor_url(url: str, timeout: float = 2.0) -> Tuple[bool, str]:
    """Best-effort reachability probe for returned monitor URLs."""
    try:
        with urlopen(url, timeout=timeout) as resp:
            if 200 <= getattr(resp, "status", 200) < 500:
                return True, ""
            return False, f"http_status={getattr(resp, 'status', 'unknown')}"
    except Exception as exc:
        parsed = urlparse(url)
        host = parsed.hostname or ""
        port = parsed.port or (443 if parsed.scheme == "https" else 80)
        if host:
            try:
                with socket.create_connection((host, port), timeout=timeout):
                    return False, f"http_error:{exc}"
            except Exception as sock_exc:
                return False, f"connect_error:{sock_exc}"
        return False, f"url_error:{exc}"


def _is_local_mode(resolved_base: str = "") -> bool:
    """根据已解析的 base URL 判定是否为本地部署模式；空值 + Windows 也视为本地"""
    if os.getenv("MONITOR_LOCAL_MODE", "").strip().lower() in {"1", "true", "yes", "on"}: return True #显式强制本地模式
    val = (resolved_base or "").strip()
    if not val: return platform.system() == "Windows" #未解析出任何 base 且 Windows→本地
    host = urlparse(val).hostname or ""
    return platform.system() == "Windows" and host in {"127.0.0.1", "localhost", "0.0.0.0"} #仅Windows默认认定localhost

def validate_monitor_public_base(base: str) -> Tuple[bool, str]:
    val = (base or "").strip().rstrip("/")
    local = _is_local_mode(val)
    if not val:
        if local: return True, "local_mode"
        return False, "MONITOR_PUBLIC_BASE is required"
    parsed = urlparse(val)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        return False, "MONITOR_PUBLIC_BASE must be a valid http(s) base URL"
    host = parsed.hostname or ""
    if host in {"0.0.0.0", "127.0.0.1", "localhost"}:
        if local: return True, "local_mode"
        return False, "MONITOR_PUBLIC_BASE must be publicly reachable (not localhost/0.0.0.0)"
    try:
        ip = ipaddress.ip_address(host)
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_unspecified:
            if local: return True, "local_mode"
            return False, "MONITOR_PUBLIC_BASE points to a non-public IP"
    except ValueError:
        pass
    return True, ""


def validate_strategy_file(filepath: str) -> Tuple[bool, str]:
    """校验策略文件路径安全性：必须在 STRATEGIES_DIR 内且为 .py 文件"""
    p = Path(filepath).resolve()
    if not p.suffix == ".py":
        return False, f"strategy file must be .py, got: {p.suffix}"
    if not p.exists():
        return False, f"strategy file not found: {p}"
    try:
        if not str(p).startswith(str(STRATEGIES_DIR.resolve())):
            return False, f"strategy file must be under {STRATEGIES_DIR}, got: {p}"
    except Exception as exc:
        return False, f"path resolution error: {exc}"
    return True, ""


def detect_strategy_class(filepath: Path) -> str:
    """从策略文件中自动检测 Strategy 类名"""
    try:
        content = filepath.read_text(encoding="utf-8")
        classes = re.findall(r"^class\s+(\w*Strategy\w*)\s*[\(:]", content, re.MULTILINE)
        return classes[0] if classes else ""
    except Exception:
        return ""


_IMPORT_REWRITES = [ #(正则, 替换目标) — 自动修正LLM生成的错误import路径
    (re.compile(r"from\s+vnpy\.app\.cta_strategy\s+import\s+"), "from vnpy_ctastrategy import "),
    (re.compile(r"from\s+vnpy\.app\.portfolio_strategy\s+import\s+"), "from vnpy_portfoliostrategy import "),
    (re.compile(r"from\s+vnpy\.app\.\w+\s+import\s+"), "from vnpy_ctastrategy import "), #兜底
]

def _autofix_imports(source: str, mode: str = "cta") -> tuple[str, list[str]]:
    """自动修复已知错误import路径，返回(修复后源码, 修复日志列表)"""
    fixes = []
    for pat, repl in _IMPORT_REWRITES:
        if pat.search(source):
            old_line = pat.search(source).group()
            if mode == "portfolio" and "vnpy_ctastrategy" in repl: repl = repl.replace("vnpy_ctastrategy", "vnpy_portfoliostrategy")
            source = pat.sub(repl, source)
            fixes.append(f"{old_line.strip()} → {repl.strip()}")
    return source, fixes

def _lint_strategy(source: str, filename: str, mode: str = "cta") -> None:
    """策略代码静态检查——在py_compile之后、submit之前执行。blocker=必崩抛异常，warning=仅日志(运行时有兜底)"""
    warnings, blockers = [], []
    source_no_comment = "\n".join(line.split("#")[0] for line in source.splitlines())
    # ── 通用 blocker：错误包路径 ──
    if "vnpy.trading." in source:
        blockers.append("错误包路径 vnpy.trading.*，应为 vnpy.trader.*")
    if re.search(r"from\s+vnpy\.app\.", source):
        blockers.append("错误包路径 vnpy.app.*，此环境应使用 vnpy_ctastrategy/vnpy_portfoliostrategy")
    if "am.ma(" in source:
        blockers.append("vnpy无am.ma()方法，应使用am.sma()")
    if mode == "portfolio" and re.search(r"from\s+vnpy_portfoliostrategy\s+import\s+.*\bSignal\b", source):
        blockers.append("无效导入 Signal（vnpy_portfoliostrategy 不提供该符号）")
    if re.search(r'pro\.(ths_member|ths_index|dc_member|tdx_member|dc_index|tdx_index)\s*\(', source):
        blockers.append("策略内禁止调用板块API(ths_member等)，成分股由引擎通过--symbols自动传入")
    if mode == "portfolio" and re.search(r'self\.vt_symbols\s*=[^=]', source):
        blockers.append("Portfolio策略禁止覆盖self.vt_symbols，必须使用引擎传入的列表")
    # ── blocker/warning：am.sma(n, 1) 第二参数误传整数——LLM高频错误，1被解读为array=True返回numpy数组 ──
    _am_int_pat = re.compile(r'(?:self\.)?am\.(?:sma|ema|rsi|cci|atr)\s*\([^)]*,\s*\d+\s*\)')
    _am_int_matches = list(_am_int_pat.finditer(source_no_comment))
    if _am_int_matches:
        _msg = "am.sma/ema/rsi/cci/atr(n, 1)第二参数是array:bool而非偏移量，1=True会返回numpy数组。取前值请用self.prev_xxx=self.xxx模式暂存"
        _all_safe = True
        for m in _am_int_matches:
            line = source_no_comment[:m.end()].rsplit('\n', 1)[-1] + source_no_comment[m.end():].split('\n', 1)[0]
            if not re.search(r'\)\s*\[', line[line.find(m.group()):]):
                assign_m = re.search(r'(\w+)\s*=\s*' + re.escape(m.group()), source_no_comment)
                if assign_m:
                    vname = assign_m.group(1)
                    if not (re.search(rf'(?:float|int)\s*\([^)]*\b{re.escape(vname)}\b', source_no_comment) or re.search(rf'\b{re.escape(vname)}\b\s*\[', source_no_comment)):
                        _all_safe = False; break
                else:
                    _all_safe = False; break
        if _all_safe:
            warnings.append(_msg + "（检测到标量提取兜底，降级为告警）")
        else:
            blockers.append(_msg)
    # ── blocker：bar.close/open/high/low 应为 bar.close_price 等 ──
    if re.search(r'\bbar\.(close|open|high|low)\b(?!_price)', source_no_comment):
        blockers.append("BarData属性应为bar.close_price/open_price/high_price/low_price，不是bar.close/open/high/low")
    # ── blocker：__init__ 签名参数不足（CTA/Portfolio均需self+4个参数，不管有没有继承模板类） ──
    init_m = re.search(r'def\s+__init__\s*\(([^)]*)\)', source)
    if init_m:
        params = [p.strip() for p in init_m.group(1).split(',') if p.strip()]
        if len(params) < 5:
            sig = "(self, cta_engine, strategy_name, vt_symbol, setting)" if mode == "cta" else "(self, strategy_engine, strategy_name, vt_symbols, setting)"
            blockers.append(f"策略__init__需要{sig}共5个参数，当前仅{len(params)}个")
    # ── blocker：CTA策略缺少on_init（抽象方法，缺失则无法实例化） ──
    if mode == "cta" and "CtaTemplate" in source and "def on_init" not in source:
        blockers.append("CTA策略必须实现on_init(self)方法，否则无法实例化(abstract method)")
    if mode == "portfolio" and "StrategyTemplate" in source and "def on_init" not in source:
        blockers.append("Portfolio策略必须实现on_init(self)方法，否则无法实例化(abstract method)")
    # ── blocker：裸引用vt_symbols而非self.vt_symbols（排除__init__体+函数签名+super调用） ──
    _bare_vt = False
    _cur_func = ""
    for line in source_no_comment.splitlines():
        stripped = line.strip()
        fn_m = re.match(r'def\s+(\w+)\s*\(', stripped)
        if fn_m: _cur_func = fn_m.group(1); continue
        if _cur_func == '__init__': continue
        if stripped.startswith('class '): continue
        if 'super().__init__' in stripped: continue
        if 'vt_symbols' in stripped and 'self.vt_symbols' not in stripped:
            _bare_vt = True; break
    if _bare_vt:
        blockers.append("裸引用vt_symbols应为self.vt_symbols（方法体内无此局部变量会NameError）")
    # ── blocker：strategy内使用不存在的get_bars方法 ──
    if re.search(r'self\.get_bars\s*\(', source_no_comment):
        blockers.append("不存在self.get_bars()方法——CTA用self.load_bar(N)，Portfolio用self.load_bars(days)")
    # ── blocker：numpy数组变量直接参与and/or布尔运算（排除[-N]/len()/float()等标量提取场景） ──
    _am_vars = set()
    for m in re.finditer(r'(\w+)\s*=\s*(?:self\.)?am\.(?:sma|ema|rsi|cci|atr|boll|keltner|donchian|macd)\s*\(([^)]*)\)', source_no_comment):
        vname, args = m.group(1), m.group(2)
        if 'array' in args and 'True' in args:
            full_assign = m.group(0)
            if not re.search(r'\)\s*\[', source_no_comment[m.end()-1:m.end()+5]):
                _am_vars.add(vname)
    for var in _am_vars:
        for line in source_no_comment.splitlines():
            if re.search(rf'\b(?:and|or)\b', line) and re.search(rf'\b{re.escape(var)}\b', line):
                if re.search(rf'(?:len|float|int)\s*\(\s*(?:self\.)?{re.escape(var)}\b', line): continue
                if re.search(rf'(?:self\.)?{re.escape(var)}\s*\[', line): continue
                if re.search(rf'(?:self\.)?{re.escape(var)}\s+is\s+(?:None|not)', line): continue
                blockers.append(f"变量{var}来自am.xxx(array=True)返回numpy数组，不能用Python and/or做布尔运算——改用[-1]取标量或numpy逻辑运算")
                break
        if blockers and blockers[-1].startswith(f"变量{var}"): break
    # ── 模式相关 warning ──
    if mode == "cta":
        if "ArrayManager" in source and "update_bar" not in source:
            warnings.append("使用了ArrayManager但未调用am.update_bar(bar)——运行时会自动注入兜底")
        if "on_bar" in source and "self.am" in source and "ArrayManager" not in source and "__init__" in source:
            warnings.append("引用了self.am但可能未初始化ArrayManager")
        if "load_bars(" in source and "CtaTemplate" in source:
            warnings.append("CTA策略应用load_bar(N)而非load_bars(days)——运行时会自动降级")
    elif mode == "portfolio":
        if "ArrayManager" in source and "update_bar" not in source:
            warnings.append("使用了ArrayManager但未调用am.update_bar(bar)——运行时会自动注入兜底")
        if "load_bar(" in source and "StrategyTemplate" in source:
            warnings.append("Portfolio策略应用load_bars(days)而非load_bar(N)——运行时会自动降级")
        if "self.pos" in source and "get_pos" not in source:
            warnings.append("Portfolio策略应用self.get_pos(vt_symbol)而非self.pos")
    if "fixed_size" in source and "= 1" in source:
        warnings.append("fixed_size=1是玩具逻辑，应按资金动态计算")
    if re.findall(r'["\'](\d{6})\.(SH|SZ)["\']', source_no_comment):
        warnings.append("标的代码应使用vnpy格式(.SSE/.SZSE)而非qgdata格式(.SH/.SZ)——运行时会自动转换")
    if re.search(r'(?:start_date|end_date|begin_date)\s*=\s*["\']20\d{6}["\']', source):
        warnings.append("策略内不建议硬编码日期，回测区间由--start/--end参数控制")
    if mode == "portfolio" and re.search(r'self\.capital\b', source):
        in_params = False
        for line in source.splitlines():
            stripped = line.strip()
            if stripped.startswith("parameters") and "=" in stripped: in_params = True
            if in_params:
                if "]" in stripped: in_params = False
                continue
            if "self.capital" in stripped:
                warnings.append("请用self.available_cash替代self.capital(固定值)——运行时会自动注入兜底")
                break
    # ── blocker：direction.name == "BUY"/"SELL" 误用vnpy枚举（应为"LONG"/"SHORT"） ──
    if re.search(r'direction\.name\s*==\s*["\'](?:BUY|SELL|Buy|Sell)["\']', source_no_comment):
        blockers.append('direction.name=="BUY"/"SELL"错误——vnpy的Direction枚举是LONG/SHORT，应改为direction==Direction.LONG或direction.name=="LONG"')
    if re.search(r'direction\s*==\s*["\'](?:BUY|SELL|LONG|SHORT|买入|卖出)["\']', source_no_comment):
        blockers.append('direction=="BUY"字符串比较错误——direction是Direction枚举，应用direction==Direction.LONG比较')
    # ── warning：on_trade中手动覆盖self.pos（engine自动管理pos，手动覆盖易冲突） ──
    _in_on_trade = False
    for line in source_no_comment.splitlines():
        stripped = line.strip()
        if re.match(r'def\s+on_trade\s*\(', stripped): _in_on_trade = True; continue
        if _in_on_trade and re.match(r'def\s+\w+\s*\(', stripped): _in_on_trade = False
        if _in_on_trade and re.search(r'self\.pos\s*=(?!=)', stripped):
            warnings.append("on_trade中手动赋值self.pos会覆盖引擎自动仓位管理——CTA策略引擎已自动跟踪pos，除非明确需要自定义逻辑否则应删除")
            break
    if warnings:
        print(f"[lint] 策略({filename}){len(warnings)}个告警(运行时兜底):\n" + "\n".join(f"  ⚠ {w}" for w in warnings))
    if blockers:
        msg = f"策略({filename}){len(blockers)}个阻断(必崩):\n" + "\n".join(f"  ✗ {w}" for w in blockers)
        print(f"[lint] {msg}")
        raise ValueError(msg)


def _validate_result(summary: dict, report_data: dict, mode: str = "cta") -> list:
    """回测结果语义校验——不阻断，返回 warning 列表"""
    warnings = []
    stats = summary.get("stats", {})
    trades = report_data.get("trades", [])
    total_trade = int(stats.get("total_trade_count", 0))
    if total_trade == 0: #零交易检测
        warnings.append("策略未产生任何交易（0笔），可能参数窗口过大或信号逻辑有误")
    if trades and total_trade > 0: #单边信号检测
        dirs = {t.get("direction", "").upper() for t in trades}
        has_long = bool(dirs & {"BUY", "LONG", "买入"})
        has_short = bool(dirs & {"SELL", "SHORT", "卖出"})
        if has_long and not has_short:
            warnings.append(f"策略仅有买入({total_trade}笔)无任何卖出——可能存在仓位管理bug或卖出条件永不触发")
        elif has_short and not has_long:
            warnings.append(f"策略仅有卖出({total_trade}笔)无任何买入——可能存在信号逻辑bug")
    wr = stats.get("winning_rate") #胜率极端值检测
    if wr is not None:
        try:
            wr_f = float(wr)
            if total_trade >= 5 and wr_f >= 100.0:
                warnings.append(f"胜率100%（{total_trade}笔交易），可能存在未来函数或逻辑漏洞")
            elif total_trade >= 10 and wr_f == 0.0:
                warnings.append(f"胜率0%（{total_trade}笔交易），策略逻辑可能存在严重问题")
        except (ValueError, TypeError): pass
    return warnings


def _preflight_strategy_import(module_name: str, python_bin: str) -> None:
    """预导入策略模块：在启动回测前捕获ImportError/ModuleNotFoundError。"""
    cmd = [
        python_bin,
        "-c",
        (
            "import sys,importlib;"
            f"sys.path.insert(0,{json.dumps(str((PROJECT_ROOT / 'vnpy_qmt').resolve()))});"
            f"sys.path.insert(0,{json.dumps(str((PROJECT_ROOT / 'strategies').resolve()))});"
            f"importlib.import_module({json.dumps(module_name)})"
        ),
    ]
    subprocess.run(cmd, check=True, cwd=str(PROJECT_ROOT))

class EngineCompatError(Exception):
    """引擎兼容性不支持"""

def _validate_engine_compat(mode: str, interval: str) -> None:
    """引擎兼容性前置闸门：在启动runner前拦截已知不支持组合。"""
    iv = (interval or "").upper()
    if mode == "portfolio" and iv == "WEEKLY":
        raise EngineCompatError("Portfolio引擎驱动不支持WEEKLY，请用--interval DAILY；周线指标可在策略内通过pro.weekly()获取，调仓日按weekday判断")


def normalize_public_base(base: str) -> str:
    return (base or "").strip().rstrip("/")


def public_url(base: str, name: str) -> str:
    return f"{normalize_public_base(base)}/{name}" if normalize_public_base(base) else ""


def publish_static_reports(
    *,
    run_id: str,
    output_prefix: str,
    report_public_base: str,
    report_public_dir: str,
) -> Tuple[Dict[str, str], str]:
    base = normalize_public_base(report_public_base)
    if not base:
        return {}, "REPORT_PUBLIC_BASE not configured"
    try:
        target_dir = Path(report_public_dir).expanduser().resolve() if report_public_dir else DEFAULT_REPORT_PUBLIC_DIR
        target_dir.mkdir(parents=True, exist_ok=True)
        published: Dict[str, str] = {}
        mapping = {
            f"{output_prefix}_report.html": f"{run_id}_report.html",
            f"{output_prefix}.html": f"{run_id}.html",
            f"{output_prefix}_replay.html": f"{run_id}_replay.html",
            f"{output_prefix}_summary.json": f"{run_id}_summary.json",
            f"{output_prefix}.png": f"{run_id}.png",
        }
        for src_name, dst_name in mapping.items():
            src = BACKTESTS_DIR / src_name
            if not src.exists():
                continue
            dst = target_dir / dst_name
            shutil.copy2(src, dst)
            published[dst_name] = public_url(base, dst_name)
        return published, ""
    except Exception as exc:
        return {}, str(exc)


def generate_report_html(*, run_id: str, report_data: Dict, summary: Dict, strategy_code: str = "", parsed: Dict = None) -> str:
    """生成自包含持久化报告 HTML（Tab分区 + 指标置顶 + echarts 图表）"""
    import html as _html
    stats = report_data.get("stats", summary.get("stats", {}))
    dates_json = json.dumps(report_data.get("dates", []), ensure_ascii=False)
    navs_json = json.dumps(report_data.get("navs", []))
    bench_json = json.dumps(report_data.get("bench", []))
    trades_json = json.dumps(report_data.get("trades", []), ensure_ascii=False)
    stats_json = json.dumps(stats, ensure_ascii=False)
    code_escaped = _html.escape(strategy_code or "")
    p = parsed or {}
    meta = {k: str(v) for k, v in {**p, "run_id": run_id}.items() if v and not k.startswith("_")}
    for _skip_k in ("pool_warning", "data_blocked"): meta.pop(_skip_k, None)
    meta_json = json.dumps(meta, ensure_ascii=False)
    return f'''<!DOCTYPE html>
<html lang="zh"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>回测报告 - {run_id}</title>
<script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11/build/styles/atom-one-light.min.css">
<script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11/build/highlight.min.js"></script>
<script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11/build/languages/python.min.js"></script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:system-ui,-apple-system,sans-serif;background:#f8fafc;color:#1e293b;min-height:100vh}}
.hdr{{background:linear-gradient(135deg,#1e40af,#3b82f6);color:#fff;padding:28px 32px}}
.hdr h1{{font-size:24px;font-weight:800}}.hdr .sub{{font-size:13px;opacity:.8;margin-top:6px;font-family:monospace}}
.mx{{max-width:1200px;margin:0 auto;padding:24px 20px}}
.metrics{{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:14px;margin-bottom:24px}}
.mc{{background:#fff;border-radius:14px;padding:18px;text-align:center;border:1px solid #e2e8f0;box-shadow:0 1px 3px rgba(0,0,0,.04)}}
.mc .lb{{font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:.5px;font-weight:600}}
.mc .vl{{font-size:24px;font-weight:800;margin-top:6px}}
.mc .vl.pos{{color:#dc2626}}.mc .vl.neg{{color:#16a34a}}.mc .vl.neu{{color:#475569}}
.tabs{{display:flex;gap:4px;background:#fff;border-radius:12px;padding:4px;border:1px solid #e2e8f0;margin-bottom:20px}}
.tab{{padding:10px 20px;border-radius:8px;border:none;background:transparent;cursor:pointer;font-size:14px;font-weight:600;color:#64748b;transition:all .2s}}
.tab.active{{background:#2563eb;color:#fff;box-shadow:0 2px 8px rgba(37,99,235,.25)}}
.tab:hover:not(.active){{background:#f1f5f9}}
.panel{{display:none;background:#fff;border-radius:14px;border:1px solid #e2e8f0;padding:24px;box-shadow:0 1px 3px rgba(0,0,0,.04)}}
.panel.active{{display:block}}
.chart-box{{width:100%;height:400px}}
.chart-box2{{width:100%;height:280px;margin-top:20px}}
.tt{{width:100%;border-collapse:collapse;font-size:13px}}
.tt th{{background:#f8fafc;color:#64748b;font-weight:600;text-align:left;padding:12px 14px;border-bottom:2px solid #e2e8f0;font-size:11px;text-transform:uppercase}}
.tt td{{padding:12px 14px;border-bottom:1px solid #f1f5f9}}
.tt tr:hover{{background:#f8fafc}}
.tt .buy{{color:#dc2626;font-weight:600}}.tt .sell{{color:#16a34a;font-weight:600}}
.pn{{display:flex;justify-content:center;gap:6px;margin-top:14px}}
.pn button{{padding:6px 12px;border:1px solid #e2e8f0;background:#fff;border-radius:6px;cursor:pointer;font-size:12px}}
.pn button.act{{background:#2563eb;color:#fff;border-color:#2563eb}}
pre.cb{{background:#fafafa;margin:0;padding:16px;font-size:13px;max-height:500px;overflow:auto;line-height:1.7;border-radius:0 0 10px 10px;border:1px solid #e2e8f0;border-top:none}}
pre.cb code{{font-family:'Cascadia Code','Fira Code','Consolas',monospace}}
.code-bar{{display:flex;align-items:center;gap:8px;padding:10px 16px;background:#f1f5f9;border-radius:10px 10px 0 0;border:1px solid #e2e8f0;border-bottom:none;font-size:12px;color:#64748b}}
.code-bar .sp{{flex:1}}
.cbtn{{padding:4px 12px;border:1px solid #cbd5e1;border-radius:6px;background:#fff;font-size:12px;color:#475569;cursor:pointer;transition:all .15s;display:inline-flex;align-items:center;gap:4px}}
.cbtn:hover{{background:#f1f5f9;border-color:#94a3b8;color:#1e293b}}
.cbtn:active{{transform:scale(.96)}}
.cbtn.copied{{background:#dcfce7;border-color:#86efac;color:#16a34a}}
.info-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:12px}}
.info-item{{background:#f8fafc;border-radius:10px;padding:14px;border:1px solid #e2e8f0}}
.info-item .ik{{font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:.5px;font-weight:600}}
.info-item .iv{{font-size:14px;font-weight:600;margin-top:6px;color:#1e293b;word-break:break-all}}
.ft{{text-align:center;padding:24px;font-size:12px;color:#94a3b8}}
</style></head><body>
<div class="hdr"><h1>回测报告</h1><div class="sub">run: {run_id} | generated: {now_iso()}</div></div>
<div class="mx">
<div class="metrics" id="metricsRow"></div>
<div class="tabs" id="tabBar">
  <button class="tab active" data-t="equity">收益分析</button>
  <button class="tab" data-t="trades">交易明细</button>
  <button class="tab" data-t="code">策略代码</button>
  <button class="tab" data-t="info">运行信息</button>
</div>
<div class="panel active" id="p-equity"><div class="chart-box" id="eqChart"></div><div class="chart-box2" id="dayChart"></div></div>
<div class="panel" id="p-trades"><div id="tradeArea"></div><div class="pn" id="tradeNav"></div></div>
<div class="panel" id="p-code"><div class="code-bar">📄 策略代码<span class="sp"></span><button class="cbtn" id="cpBtn" onclick="_cpCode()">📋 复制代码</button><button class="cbtn" onclick="_svCode()">💾 保存策略</button></div><pre class="cb"><code class="language-python">{code_escaped}</code></pre></div>
<div class="panel" id="p-info"><div class="info-grid" id="infoGrid"></div></div>
</div>
<div class="ft">Generated by QuantClaw | {run_id}</div>
<script>
const D={dates_json},N={navs_json},B={bench_json},T={trades_json},S={stats_json},M={meta_json};
/* --- metrics --- */
(function(){{
const fmt={{total_return:['总收益率',1],annual_return:['年化收益',1],max_ddpercent:['最大回撤',1],sharpe_ratio:['夏普比率',0],total_trade_count:['交易次数',0],winning_rate:['胜率',1],profit_days:['盈利天数',0],loss_days:['亏损天数',0]}};
let h='';for(const[k,[lb,isPct]] of Object.entries(fmt)){{const v=S[k];if(v===undefined)continue;
const n=typeof v==='number';let d=n?(isPct?v.toFixed(2)+'%':v.toFixed(2)):v;
const c=n?(v>=0?'pos':'neg'):'neu';h+='<div class="mc"><div class="lb">'+lb+'</div><div class="vl '+c+'">'+d+'</div></div>'}}
document.getElementById('metricsRow').innerHTML=h}})();
/* --- tabs --- */
document.querySelectorAll('.tab').forEach(b=>b.onclick=function(){{
document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));b.classList.add('active');
document.querySelectorAll('.panel').forEach(p=>p.classList.remove('active'));
document.getElementById('p-'+b.dataset.t).classList.add('active')}});
/* --- equity chart --- */
(function(){{
const ch=echarts.init(document.getElementById('eqChart'));
ch.setOption({{animation:true,tooltip:{{trigger:'axis'}},legend:{{data:['策略净值','沪深300基准'],top:10,right:16}},
grid:{{left:64,right:32,top:52,bottom:48}},
xAxis:{{type:'category',data:D,axisLabel:{{color:'#94a3b8',fontSize:11}},boundaryGap:false}},
yAxis:{{type:'value',name:'净值',min:'dataMin',axisLabel:{{color:'#64748b',formatter:v=>v.toFixed(2)}},splitLine:{{lineStyle:{{color:'#f1f5f9'}}}}}},
series:[{{name:'策略净值',type:'line',data:N,smooth:.25,lineStyle:{{width:3,color:'#2563eb'}},areaStyle:{{color:{{type:'linear',x:0,y:0,x2:0,y2:1,colorStops:[{{offset:0,color:'rgba(37,99,235,.12)'}},{{offset:1,color:'rgba(37,99,235,0)'}}]}}}},symbol:'none'}},
{{name:'沪深300基准',type:'line',data:B,smooth:.25,lineStyle:{{width:2,color:'#dc2626',type:'dashed'}},symbol:'none'}}]}});
const dc=echarts.init(document.getElementById('dayChart'));
const dd=[],dl=[];for(let i=1;i<N.length&&i<D.length;i++){{const p=N[i-1]||1;dd.push(((N[i]-p)/p*100).toFixed(3));dl.push(D[i])}}
dc.setOption({{animation:true,tooltip:{{trigger:'axis'}},grid:{{left:56,right:24,top:36,bottom:48}},
xAxis:{{type:'category',data:dl,axisLabel:{{color:'#94a3b8',fontSize:10}}}},
yAxis:{{type:'value',name:'日收益%',axisLabel:{{color:'#64748b',formatter:v=>v.toFixed(2)+'%'}},splitLine:{{lineStyle:{{color:'#f1f5f9'}}}}}},
series:[{{type:'bar',data:dd.map(v=>parseFloat(v)),itemStyle:{{color:function(p){{return p.data>=0?'#dc2626':'#16a34a'}}}},barWidth:'60%'}}]}});
window.addEventListener('resize',()=>{{ch.resize();dc.resize()}})
}})();
/* --- trades --- */
(function(){{
let pg=1;const ps=15;
function render(){{
const s=(pg-1)*ps,page=T.slice(s,s+ps);
let h='<table class="tt"><thead><tr><th>日期</th><th>标的</th><th>方向</th><th>价格</th><th>数量</th><th>金额</th><th>盈亏</th></tr></thead><tbody>';
page.forEach(t=>{{const ib=t.direction==='买入'||t.direction==='BUY';const pnl=t.pnl||'';const ps=pnl?(parseFloat(pnl)>=0?'color:#dc2626;font-weight:600':'color:#16a34a;font-weight:600'):'';const sym=t.symbol||'';h+='<tr><td>'+t.date+'</td><td>'+sym+'</td><td class="'+(ib?'buy':'sell')+'">'+(ib?'买入':'卖出')+'</td><td>'+t.price+'</td><td>'+t.volume+'</td><td>'+t.amount+'</td><td style="'+ps+'">'+pnl+'</td></tr>'}});
h+='</tbody></table>';document.getElementById('tradeArea').innerHTML=h||'<div style="color:#94a3b8;text-align:center;padding:40px">暂无交易记录</div>';
const tp=Math.ceil(T.length/ps),nav=document.getElementById('tradeNav');
if(tp>1){{let p='';for(let i=1;i<=tp;i++)p+='<button class="'+(i===pg?'act':'')+'" onclick="window._tp('+i+')">'+i+'</button>';nav.innerHTML=p}}else nav.innerHTML=''}}
window._tp=function(n){{pg=n;render()}};render()
}})();
/* --- info --- */
(function(){{
const _km={{symbols:'标的',interval:'K线周期',mode:'策略模式',requirement:'需求描述',run_id:'运行ID',fast_window:'快线周期',slow_window:'慢线周期',direction:'方向',k_period:'K周期',d_period:'D周期',rsi_period:'RSI周期',boll_window:'布林窗口',macd_fast:'MACD快线',macd_slow:'MACD慢线',atr_period:'ATR周期'}};
const _vm={{DAILY:'日线','5MIN':'5分钟','15MIN':'15分钟','30MIN':'30分钟',HOUR:'小时线',WEEKLY:'周线',cta:'CTA单标的',portfolio:'Portfolio组合',bullish:'看涨',bearish:'看跌'}};
let h='';for(const[k,v] of Object.entries(M))h+='<div class="info-item"><div class="ik">'+(_km[k]||k)+'</div><div class="iv">'+(_vm[v]||v)+'</div></div>';
document.getElementById('infoGrid').innerHTML=h||'<div style="color:#94a3b8">无额外信息</div>'}})();
hljs.highlightAll();
function _cpCode(){{const c=document.querySelector('#p-code code');const t=c?c.textContent:'';const b=document.getElementById('cpBtn');function _ok(){{b.classList.add('copied');b.textContent='✓ 已复制';setTimeout(()=>{{b.classList.remove('copied');b.textContent='📋 复制代码'}},1500)}}function _fb(){{const ta=document.createElement('textarea');ta.value=t;ta.style.cssText='position:fixed;left:-9999px';document.body.appendChild(ta);ta.select();document.execCommand('copy');document.body.removeChild(ta);_ok()}}if(navigator.clipboard&&navigator.clipboard.writeText){{navigator.clipboard.writeText(t).then(_ok).catch(_fb)}}else{{_fb()}}}}
function _svCode(){{const c=document.querySelector('#p-code code');const t=c?c.textContent:'';const fn=(M.run_id||'strategy')+'_strategy.py';const bl=new Blob([t],{{type:'text/x-python'}});const a=document.createElement('a');a.href=URL.createObjectURL(bl);a.download=fn;a.click();URL.revokeObjectURL(a.href)}}
</script></body></html>'''


class RunStore:
    def __init__(self, run_id: str):
        self.run_id = run_id
        self.run_dir = RUNS_DIR / run_id
        self.state_file = self.run_dir / "state.json"
        self.run_log = self.run_dir / "worker.log"
        self.monitor_log = self.run_dir / "monitor.log"

    def init_state(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        self.run_dir.mkdir(parents=True, exist_ok=True)
        state = {
            "version": STATE_VERSION,
            "run_id": self.run_id,
            "created_at": now_iso(),
            "updated_at": now_iso(),
            "status": "submitted",
            "payload": payload,
            "steps": {},
            "process": {},
            "artifacts": {},
            "errors": [],
        }
        atomic_json_write(self.state_file, state)
        return state

    def load(self) -> Dict[str, Any]:
        return read_json(self.state_file)

    def save(self, state: Dict[str, Any]) -> None:
        state["updated_at"] = now_iso()
        atomic_json_write(self.state_file, state)

    def mark_step(self, state: Dict[str, Any], name: str, status: str, detail: str = "") -> None:
        state["steps"][name] = {"status": status, "detail": detail, "at": now_iso()}
        self.save(state)

    def append_error(self, state: Dict[str, Any], message: str) -> None:
        state["errors"].append({"at": now_iso(), "message": message})
        self.save(state)


def start_process(command: list[str], log_path: Path, env: Optional[Dict[str, str]] = None) -> subprocess.Popen:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    f = log_path.open("a", encoding="utf-8")
    return subprocess.Popen(
        command,
        cwd=str(PROJECT_ROOT),
        env=env or os.environ.copy(),
        stdout=f,
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )


def _lot_size_for_symbol(code: str) -> int:
    """根据A股代码确定最小交易单位：科创板688xxx→200股，其余→100股"""
    digits = "".join(c for c in code if c.isdigit())[:6]
    return 200 if digits.startswith("688") else 100


def strategy_source(class_name: str, fast: int, slow: int, author: str, direction: str) -> str:
    return f'''"""Auto-generated MA cross strategy — 动态全仓 + 交易所合规手数"""
from vnpy_ctastrategy import CtaTemplate
from vnpy_ctastrategy.base import StopOrder
from vnpy.trader.object import BarData, TradeData, OrderData
from vnpy.trader.utility import ArrayManager


def _calc_volume(symbol: str, price: float, capital: float) -> int:
    """按资金全仓计算合规手数：主板/创业板100股整数倍，科创板(688)200起+1股递增"""
    digits = "".join(c for c in symbol if c.isdigit())[:6]
    if digits.startswith("688"):
        vol = int(capital / price)
        return max(vol, 200) if vol >= 200 else 0
    else:
        vol = int(capital / price / 100) * 100
        return max(vol, 100) if vol >= 100 else 0


class {class_name}(CtaTemplate):
    author = "{author}"
    fast_window = {fast}
    slow_window = {slow}
    direction_hint = "{direction}"

    parameters = ["fast_window", "slow_window", "direction_hint"]
    variables = ["fast_ma", "slow_ma"]

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)
        self.am = ArrayManager(size=self.slow_window + 5)
        self.fast_ma = 0.0
        self.slow_ma = 0.0
        self.prev_fast = 0.0
        self.prev_slow = 0.0

    def on_init(self):
        self.load_bar(self.slow_window + 20)

    def on_start(self):
        pass

    def on_stop(self):
        pass

    def on_bar(self, bar: BarData):
        self.am.update_bar(bar)
        if not self.am.inited:
            return

        self.cancel_all()
        self.prev_fast = self.fast_ma
        self.prev_slow = self.slow_ma
        self.fast_ma = self.am.sma(self.fast_window)
        self.slow_ma = self.am.sma(self.slow_window)

        cross_up = self.prev_fast <= self.prev_slow and self.fast_ma > self.slow_ma
        cross_down = self.prev_fast >= self.prev_slow and self.fast_ma < self.slow_ma

        cash = getattr(self, 'available_cash', 1000000)  #引擎注入的可用现金
        if self.pos == 0 and cross_up:
            vol = _calc_volume(self.vt_symbol, bar.close_price, cash)
            if vol > 0:
                self.buy(bar.close_price * 1.31, vol)
        elif self.pos > 0 and cross_down:
            self.sell(bar.close_price * 0.69, abs(self.pos))

        self.put_event()

    def on_trade(self, trade: TradeData):
        self.put_event()

    def on_order(self, order: OrderData):
        pass

    def on_stop_order(self, stop_order: StopOrder):
        pass
'''


def portfolio_strategy_source(class_name: str, fast: int, slow: int, author: str, direction: str, vt_symbols: list[str]) -> str:
    syms_str = json.dumps(vt_symbols)
    return f'''"""Auto-generated Portfolio MA cross strategy — 多标的组合 + 动态全仓 + 交易所合规手数"""
from vnpy_portfoliostrategy import StrategyTemplate
from vnpy.trader.object import BarData
from vnpy.trader.utility import ArrayManager


def _calc_volume(symbol: str, price: float, capital: float) -> int:
    """按资金动态计算合规手数：主板/创业板100股整数倍，科创板(688)200起+1股递增"""
    digits = "".join(c for c in symbol if c.isdigit())[:6]
    if digits.startswith("688"):
        vol = int(capital / price)
        return max(vol, 200) if vol >= 200 else 0
    else:
        vol = int(capital / price / 100) * 100
        return max(vol, 100) if vol >= 100 else 0


class {class_name}(StrategyTemplate):
    author = "{author}"
    fast_window = {fast}
    slow_window = {slow}
    capital = 1000000.0
    direction_hint = "{direction}"

    parameters = ["fast_window", "slow_window", "capital", "direction_hint"]
    variables = []

    def __init__(self, strategy_engine, strategy_name, vt_symbols, setting):
        super().__init__(strategy_engine, strategy_name, vt_symbols, setting)
        self.vt_symbols = {syms_str}
        self.ams: dict[str, ArrayManager] = {{s: ArrayManager(size=self.slow_window + 5) for s in self.vt_symbols}}
        self.prev_fast: dict[str, float] = {{s: 0.0 for s in self.vt_symbols}}
        self.prev_slow: dict[str, float] = {{s: 0.0 for s in self.vt_symbols}}

    def on_init(self):
        self.load_bars(self.slow_window + 20)

    def on_start(self):
        pass

    def on_stop(self):
        pass

    def on_bars(self, bars: dict[str, BarData]):
        cash = getattr(self, 'available_cash', getattr(self, 'capital', 1000000))
        per_capital = cash / max(len(self.vt_symbols), 1)
        for vt_symbol in self.vt_symbols:
            bar = bars.get(vt_symbol)
            if not bar:
                continue
            am = self.ams[vt_symbol]
            am.update_bar(bar)
            if not am.inited:
                continue

            prev_f = self.prev_fast.get(vt_symbol, 0.0)
            prev_s = self.prev_slow.get(vt_symbol, 0.0)
            fast_ma = am.sma(self.fast_window)
            slow_ma = am.sma(self.slow_window)
            self.prev_fast[vt_symbol] = fast_ma
            self.prev_slow[vt_symbol] = slow_ma

            cross_up = prev_f <= prev_s and fast_ma > slow_ma
            cross_down = prev_f >= prev_s and fast_ma < slow_ma

            pos = self.get_pos(vt_symbol)
            if pos == 0 and cross_up:
                vol = _calc_volume(vt_symbol, bar.close_price, per_capital)
                if vol > 0:
                    self.buy(vt_symbol, bar.close_price * 1.31, vol)
            elif pos > 0 and cross_down:
                self.sell(vt_symbol, bar.close_price * 0.69, abs(pos))

        self.put_event()
'''


def wait_monitor_ready(base_url: str, timeout_sec: int = 20) -> bool:
    deadline = time.time() + timeout_sec
    while time.time() < deadline:
        if monitor_get(base_url, "/api/health", timeout=1.5) is not None:
            return True
        time.sleep(0.5)
    return False


def cmd_submit(args: argparse.Namespace) -> int:
    resolved_monitor_public_base = resolve_monitor_public_base(args.monitor_public_base)
    ok, err = validate_monitor_public_base(resolved_monitor_public_base)
    if not ok:
        print(
            json.dumps(
                {
                    "status": "config_missing",
                    "error": err,
                    "next_action": "请先配置公网 MONITOR_PUBLIC_BASE，或配置 OPENCLAW_CONTROL_URL 让系统自动推导（例如 https://your-control-host）",
                },
                ensure_ascii=False,
            )
        )
        return 1

    run_id = args.run_id or datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    store = RunStore(run_id)
    if store.state_file.exists():
        print(json.dumps({"status": "error", "error": f"run_id already exists: {run_id}"}, ensure_ascii=False))
        return 1

    resolved_token, token_source = resolve_qgdata_token(args.token, args.requirement)
    print(f"[token] source={token_source}, token={mask_token(resolved_token)}")
    parsed = parse_requirement(args.requirement, args.symbols, resolved_token)
    if parsed.get("data_blocked"):
        _err = parsed.get("pool_warning", "数据服务不可用")
        _is_quota = any(k in str(_err) for k in ["额度已达上限", "额度不足", "quota", "rate limit", "too many requests", "429"])
        _next = f"请配置有效Token或到 {QGDATA_RECHARGE_URL} 充值后重试"
        if _is_quota and token_source == "shared":
            _next = f"今日免费额度已用完（1次/天）。升级数据套餐可解除限制：{QGDATA_RECHARGE_URL}"
        print(json.dumps({"status": "data_auth_failed", "error": _err, "next_action": _next, "token_source": token_source}, ensure_ascii=False))
        return 2
    cap = evaluate_requirement(args.requirement).to_dict()
    if not cap.get("ok", False):
        print(
            json.dumps(
                {
                    "status": cap.get("status", "clarification_needed"),
                    "message": "需求与当前数据能力不匹配，未启动后台编排。",
                    "capability_check": cap,
                },
                ensure_ascii=False,
            )
        )
        return 2
    raw_candidates = args.monitor_port_candidates or os.getenv("ORCH_MONITOR_PORT_CANDIDATES", "")
    candidate_ports: list[int] = []
    if raw_candidates:
        for tok in raw_candidates.split(","):
            tok = tok.strip()
            if tok:
                try: candidate_ports.append(int(tok))
                except ValueError: pass
    try:
        if args.monitor_port:
            monitor_port = args.monitor_port
            if _is_port_busy(monitor_port):
                st = _read_monitor_state_by_port(monitor_port)
                if st and (bool(st.get("done")) or str(st.get("status", "")).lower() in {"done", "failed", "completed"}):
                    _kill_port_process(monitor_port)
        else:
            pool = candidate_ports or DEFAULT_MONITOR_PORTS
            try: monitor_port = pick_free_port(pool)
            except RuntimeError:
                reclaimed = try_reclaim_done_monitor_ports(pool)
                if reclaimed: monitor_port = pick_free_port(pool)
                else: raise
    except RuntimeError as exc:
        print(json.dumps({
            "status": "port_unavailable",
            "error": str(exc),
            "monitor_port_candidates": (candidate_ports or DEFAULT_MONITOR_PORTS),
            "next_action": "存在进行中的监控占用端口；可等待运行结束，或扩展 ORCH_MONITOR_PORT_CANDIDATES（例如 8761,8767）",
        }, ensure_ascii=False))
        return 1
    monitor_base = f"http://127.0.0.1:{monitor_port}"
    _local = _is_local_mode(resolved_monitor_public_base)
    _effective_base = resolved_monitor_public_base.rstrip('/') if resolved_monitor_public_base else "http://127.0.0.1"
    _pu = urlparse(_effective_base if "://" in _effective_base else f"http://{_effective_base}") #规范化，避免 base 已含端口/路径导致 URL 畸形
    _host = _pu.hostname or "127.0.0.1"
    _host_fmt = f"[{_host}]" if ":" in _host and not _host.startswith("[") else _host
    _scheme = _pu.scheme or "http"
    monitor_url = f"{_scheme}://{_host_fmt}:{monitor_port}/runs/{run_id}"
    monitor_url_local = f"http://127.0.0.1:{monitor_port}/runs/{run_id}"
    report_public_base = normalize_public_base(args.report_public_base)
    _report_prefix = f"run_{run_id}"
    _report_base_via_monitor = f"{_scheme}://{_host_fmt}:{monitor_port}/reports"
    report_url = public_url(report_public_base, f"{run_id}.html") or f"{_report_base_via_monitor}/{_report_prefix}_report.html"
    report_replay_url = public_url(report_public_base, f"{run_id}_replay.html") or f"{_report_base_via_monitor}/{_report_prefix}_replay.html"
    report_summary_url = public_url(report_public_base, f"{run_id}_summary.json") or f"{_report_base_via_monitor}/{_report_prefix}_summary.json"
    public_reachable = False
    public_probe_error = "probe_pending"
    strategy_file = ""
    strategy_module = args.strategy_module
    strategy_class = args.strategy_class
    if args.strategy_file:
        sf_ok, sf_err = validate_strategy_file(args.strategy_file)
        if not sf_ok:
            print(json.dumps({"status": "error", "error": sf_err, "next_action": "请检查策略文件路径"}, ensure_ascii=False))
            return 1
        strategy_file = str(Path(args.strategy_file).resolve())
        if not strategy_module:
            strategy_module = Path(strategy_file).stem
        if not strategy_class:
            strategy_class = detect_strategy_class(Path(strategy_file))
            if not strategy_class:
                print(json.dumps({"status": "error", "error": f"无法在 {strategy_file} 中检测到 Strategy 类", "next_action": "请通过 --strategy-class 显式指定"}, ensure_ascii=False))
                return 1

    payload = {
        "requirement": args.requirement,
        "parsed": parsed,
        "capability_check": cap,
        "monitor_port": monitor_port,
        "monitor_base": monitor_base,
        "monitor_url": monitor_url,
        "monitor_url_local": monitor_url_local,
        "monitor_public_base": resolved_monitor_public_base,
        "monitor_public_reachable": public_reachable,
        "monitor_public_probe_error": public_probe_error,
        "report_public_base": report_public_base,
        "report_public_dir": args.report_public_dir,
        "report_url": report_url,
        "report_replay_url": report_replay_url,
        "report_summary_url": report_summary_url,
        "start": args.start or parsed.get("start", ""),
        "end": args.end or parsed.get("end", ""),
        "interval": (args.interval or parsed["interval"]).upper(),
        "capital": args.capital,
        "rate": args.rate,
        "slippage": args.slippage,
        "size": args.size,
        "pricetick": args.pricetick,
        "title": args.title,
        "python_bin": args.python_bin or DEFAULT_PYTHON_BIN,
        "qgdata_token_present": bool(resolved_token),
        "qgdata_token_source": token_source,
        "timeout_sec": args.timeout_sec,
        "strategy_file": strategy_file,
        "strategy_module": strategy_module,
        "strategy_class": strategy_class,
    }
    state = store.init_state(payload)

    monitor_cmd = [
        payload["python_bin"],
        str(MONITOR_SERVER),
        "--host",
        MONITOR_BIND_HOST,
        "--port",
        str(monitor_port),
        "--run-id",
        run_id,
    ]
    mon_proc = start_process(monitor_cmd, store.monitor_log)
    state["process"]["monitor_pid"] = mon_proc.pid
    store.save(state)
    if not wait_monitor_ready(monitor_base):
        store.append_error(state, "monitor server failed to start")
        state["status"] = "failed"
        store.save(state)
        print(json.dumps({"status": "error", "error": "monitor startup failed", "run_id": run_id}, ensure_ascii=False))
        return 1

    if _local: #本地模式：probe localhost 即可，不要求公网可达
        public_reachable, public_probe_error = probe_monitor_url(monitor_url_local, timeout=3.0)
        if not public_reachable: #连本地都不通，说明 monitor 启动失败
            try: mon_proc.kill()
            except Exception: pass
            state["status"] = "failed"
            store.append_error(state, f"monitor本地不可达: {public_probe_error}")
            store.save(state)
            print(json.dumps({"status": "error", "error": f"monitor 启动异常（本地不可达）: {public_probe_error}", "monitor_port": monitor_port}, ensure_ascii=False))
            return 1
    else: #云端模式：公网 probe
        public_reachable, public_probe_error = probe_monitor_url(monitor_url, timeout=3.0)
        if not public_reachable:
            try: mon_proc.kill()
            except Exception: pass
            state["status"] = "failed"
            store.append_error(state, f"monitor公网不可达: {public_probe_error}")
            store.save(state)
            print(json.dumps({
                "status": "config_missing",
                "error": f"monitor_url 公网不可达: {monitor_url} ({public_probe_error})",
                "monitor_port": monitor_port,
                "next_action": f"请确认: 1) MONITOR_PUBLIC_BASE 指向正确的公网地址; 2) 防火墙/安全组已放通端口 {monitor_port}; 3) 运行 config-doctor 一键诊断: python3 pipeline_orchestrator.py config-doctor",
            }, ensure_ascii=False))
            return 1
    payload["monitor_public_reachable"] = public_reachable
    payload["monitor_public_probe_error"] = public_probe_error
    state["payload"] = payload
    store.save(state)

    _req_display = {k: v for k, v in parsed.items() if not k.startswith("_")} #排除 _ma_fallback 等内部字段
    monitor_post(monitor_base, "/api/requirement", {"requirement": args.requirement, **_req_display, "run_id": run_id})
    if parsed.get("pool_warning"):
        monitor_step(monitor_base, step="1", status="warning", title="数据源警告", msg=parsed["pool_warning"], run_id=run_id)
    monitor_step(monitor_base, step="1", status="success", title="需求确认", msg="监控页面已启动", run_id=run_id)
    store.mark_step(state, "monitor", "success", "monitor started and requirement posted")

    worker_cmd = [payload["python_bin"], str(Path(__file__).resolve()), "worker", "--run-id", run_id]
    worker_env = os.environ.copy()
    if resolved_token:
        worker_env["QGDATA_TOKEN"] = resolved_token
        worker_env["QGDATA_TOKEN_SOURCE"] = token_source
    worker_proc = start_process(worker_cmd, store.run_log, env=worker_env)
    state["process"]["worker_pid"] = worker_proc.pid
    state["status"] = "running"
    store.save(state)

    # ── 同步等待预检（compile→lint→dryrun）完成再返回 ──
    _pf_base = 180
    _pf_extra = int(os.getenv("PRECHECK_TIMEOUT_SEC", "0"))
    if parsed.get("mode") == "portfolio": _pf_base = 300 #portfolio数据量大，dryrun更久
    _pf_deadline = time.time() + max(_pf_base, _pf_extra)
    _pf_ok = False
    _worker_gone = False
    def _resolve_sf() -> str: #预检失败时回填strategy_file（自动生成分支submit时strategy_file为空）
        if strategy_file: return strategy_file
        try: return store.load().get("artifacts", {}).get("strategy_file", "")
        except Exception: return ""
    while time.time() < _pf_deadline:
        time.sleep(0.5)
        raw = monitor_get(monitor_base, "/api/state", timeout=2.0)
        if raw:
            try: ms = json.loads(raw)
            except Exception: ms = {}
            steps = ms.get("steps", {})
            err = ms.get("error")
            if steps.get("3", {}).get("status") == "success" or steps.get("4", {}).get("status") in ("running", "success"): #dryrun通过 or 回测已启动
                _pf_ok = True; break
            if err and err.get("error_type"): #compile/lint/dryrun失败
                try: mon_proc.kill(); mon_proc.wait()
                except Exception: pass
                print(json.dumps({
                    "status": err["error_type"], "run_id": run_id,
                    "error": err.get("message", ""), "traceback": err.get("traceback", "")[:2000],
                    "strategy_file": _resolve_sf(), "next_action": "读取错误信息和策略文件，修复后重新submit",
                }, ensure_ascii=False))
                return 1
        if worker_proc.poll() is not None:
            if _worker_gone: break #已等过一轮grace period仍无结果
            _worker_gone = True; continue #再poll一次让最后的HTTP到达monitor
    if not _pf_ok: #超时或worker异常退出
        try: mon_proc.kill(); mon_proc.wait()
        except Exception: pass
        try: worker_proc.kill(); worker_proc.wait()
        except Exception: pass
        print(json.dumps({
            "status": "timeout_error", "run_id": run_id,
            "error": "预检超时（编译/静态检查/冒烟测试未在限定时间内完成）",
            "strategy_file": _resolve_sf(), "next_action": "检查策略代码是否有死循环或网络依赖",
        }, ensure_ascii=False))
        return 1

    submit_result = {
        "status": "accepted",
        "run_id": run_id,
        "monitor_url": monitor_url,
        "monitor_url_local": monitor_url_local,
        "monitor_public_base": resolved_monitor_public_base,
        "monitor_public_reachable": public_reachable,
        "monitor_public_probe_error": public_probe_error,
        "report_url": report_url,
        "report_replay_url": report_replay_url,
        "report_summary_url": report_summary_url,
        "state_file": str(store.state_file),
        "worker_pid": worker_proc.pid,
        "token_source": token_source,
    }
    if parsed.get("pool_warning"): submit_result["pool_warning"] = parsed["pool_warning"]
    print(json.dumps(submit_result, ensure_ascii=False))
    return 0


def cmd_worker(args: argparse.Namespace) -> int:
    qgdata_token = os.getenv("QGDATA_TOKEN", "") or resolve_qgdata_token("")[0]
    store = RunStore(args.run_id)
    state = store.load()
    payload = state["payload"]
    run_id = state["run_id"]
    monitor_base = payload["monitor_base"]
    parsed = payload["parsed"]
    output_prefix = f"run_{run_id}"

    def _structured_error(state_: Dict, error_type: str, step: str, message: str, tb: str = "") -> None:
        """保存结构化错误到 state"""
        state_["errors"].append({"at": now_iso(), "error_type": error_type, "step": step, "message": message, "traceback": tb[:4000]})
        store.save(state_)
        monitor_post(monitor_base, "/api/error", {"error_type": error_type, "step": step, "message": message, "traceback": tb[:2000]})
        monitor_get(monitor_base, f"/api/log?{urlencode({'msg': f'[{error_type}] {step}: {message}'})}", timeout=2.0)

    def _fail_report(state_: Dict, error_msg: str) -> None:
        """失败时也生成最小 report HTML"""
        try:
            code = ""
            sf = state_.get("artifacts", {}).get("strategy_file", "") or state_.get("artifacts", {}).get("strategy_snapshot", "")
            if sf and Path(sf).exists():
                try: code = Path(sf).read_text(encoding="utf-8")
                except Exception: pass
            fail_data = {"dates": [], "navs": [], "bench": [], "trades": [], "stats": {}}
            fail_summary = {"stats": {"error": error_msg}}
            html = generate_report_html(run_id=run_id, report_data=fail_data, summary=fail_summary, strategy_code=code, parsed=parsed)
            rpath = BACKTESTS_DIR / f"{output_prefix}_report.html"
            rpath.write_text(html, encoding="utf-8")
            state_["artifacts"]["report_html"] = str(rpath)
            published, _ = publish_static_reports(run_id=run_id, output_prefix=output_prefix, report_public_base=payload.get("report_public_base", ""), report_public_dir=payload.get("report_public_dir", ""))
            if published:
                state_["artifacts"]["report_public_urls"] = published
                payload["report_url"] = published.get(f"{run_id}_report.html", payload.get("report_url", ""))
                state_["payload"] = payload
            store.save(state_)
        except Exception:
            pass

    try:
        ext_strategy_file = payload.get("strategy_file", "")
        if ext_strategy_file and Path(ext_strategy_file).exists():
            monitor_step(monitor_base, step="2", status="running", title="策略加载", msg="加载外部策略文件", run_id=run_id)
            module_name = payload.get("strategy_module", "") or Path(ext_strategy_file).stem
            class_name = payload.get("strategy_class", "") or detect_strategy_class(Path(ext_strategy_file))
            snapshot_path = store.run_dir / "strategy_snapshot.py"
            shutil.copy2(ext_strategy_file, snapshot_path)
            state["artifacts"]["strategy_snapshot"] = str(snapshot_path)
            strategy_file_path = Path(ext_strategy_file)
            source = strategy_file_path.read_text(encoding="utf-8")
            bt_mode = parsed.get("mode", "cta")
            source, import_fixes = _autofix_imports(source, bt_mode)
            if import_fixes: strategy_file_path.write_text(source, encoding="utf-8"); print(f"[autofix] import修正: {'; '.join(import_fixes)}")
            subprocess.run([payload["python_bin"], "-m", "py_compile", str(strategy_file_path)], check=True, cwd=str(PROJECT_ROOT))
            _lint_strategy(source, strategy_file_path.name, bt_mode)
            _preflight_strategy_import(module_name, payload["python_bin"])
            monitor_post(monitor_base, "/api/code", {"filename": strategy_file_path.name, "content": source})
            monitor_step(monitor_base, step="2", status="success", title="策略加载", msg=f"外部策略已加载: {strategy_file_path.name}", run_id=run_id)
            state["artifacts"]["strategy_file"] = ext_strategy_file
            state["status"] = "code_ready"
            store.mark_step(state, "strategy_generation", "success", f"external: {strategy_file_path.name}")
            code_syms = _extract_symbols_from_source(source) #兜底：检测策略源码是否硬编码了标的（违反股票池契约）
            if code_syms:
                merged = list(dict.fromkeys(parsed["symbols"] + code_syms))
                if len(merged) > len(parsed["symbols"]):
                    print(f"[warn] 策略源码硬编码了{len(code_syms)}个标的(应由--symbols传入)，兜底合并: {len(parsed['symbols'])}→{len(merged)}")
                    parsed["symbols"] = merged; payload["parsed"] = parsed; state["payload"] = payload; store.save(state)
        else:
            bt_mode = parsed.get("mode", "cta")
            monitor_step(monitor_base, step="2", status="running", title="策略生成", msg=f"正在生成{bt_mode.upper()}策略代码", run_id=run_id)
            module_name = f"auto_ma_{run_id}".lower()
            class_name = "AutoMaCrossStrategy" if bt_mode == "cta" else "AutoPortfolioStrategy"
            strategy_file_path = STRATEGIES_DIR / f"{module_name}.py"
            _maf = parsed.get("_ma_fallback", {})
            fw, sw = _maf.get("fast_window", 5), _maf.get("slow_window", 10)
            _dir = _maf.get("direction", "bullish")
            if bt_mode == "portfolio":
                source = portfolio_strategy_source(class_name, fw, sw, "quant-strategy-assistant", _dir, [s for s in (normalize_symbol(x) for x in parsed["symbols"]) if s])
            else:
                source = strategy_source(class_name, fw, sw, "quant-strategy-assistant", _dir)
            source, import_fixes = _autofix_imports(source, bt_mode)
            if import_fixes: print(f"[autofix] import修正: {'; '.join(import_fixes)}")
            strategy_file_path.write_text(source, encoding="utf-8")
            subprocess.run([payload["python_bin"], "-m", "py_compile", str(strategy_file_path)], check=True, cwd=str(PROJECT_ROOT))
            _lint_strategy(source, strategy_file_path.name, bt_mode)
            _preflight_strategy_import(module_name, payload["python_bin"])
            monitor_post(monitor_base, "/api/code", {"filename": strategy_file_path.name, "content": source})
            monitor_step(monitor_base, step="2", status="success", title="策略生成", msg=f"策略已生成: {strategy_file_path.name}", run_id=run_id)
            state["artifacts"]["strategy_file"] = str(strategy_file_path)
            store.mark_step(state, "strategy_generation", "success", strategy_file_path.name)

        _validate_engine_compat(parsed.get("mode", "cta"), payload["interval"])

        # ── dry run: 采样标的 + K线冒烟测试 ──
        _am_size = 50 #默认预热长度
        _sf = state.get("artifacts", {}).get("strategy_file", "")
        if _sf and Path(_sf).exists():
            _src = Path(_sf).read_text(encoding="utf-8", errors="replace")
            _m = re.search(r'ArrayManager\s*\(\s*(?:size\s*=\s*)?(\d+)', _src)
            if _m: _am_size = max(_am_size, int(_m.group(1)))
        _dry_max_bars = _am_size + 20 #预热+至少20根交易K线触发策略逻辑
        _dry_sym_limit = 5
        _dry_syms = parsed["symbols"][:_dry_sym_limit] if len(parsed["symbols"]) > _dry_sym_limit else parsed["symbols"]
        monitor_step(monitor_base, step="3", status="running", title="冒烟测试", msg=f"采样{len(_dry_syms)}只标的×{_dry_max_bars}根K线验证", run_id=run_id)
        _dry_cmd = [payload["python_bin"], str(BACKTEST_RUNNER),
            "--strategy", module_name, "--class", class_name,
            "--symbols", ",".join(_dry_syms), "--mode", parsed.get("mode", "cta"),
            "--interval", payload["interval"], "--capital", str(payload["capital"]),
            "--rate", str(payload["rate"]), "--slippage", str(payload["slippage"]),
            "--size", str(payload["size"]), "--pricetick", str(payload["pricetick"]),
            "--max-bars", str(_dry_max_bars), "--run-id", f"{run_id}_dryrun"]
        if payload.get("start"): _dry_cmd.extend(["--start", payload["start"]])
        if payload.get("end"): _dry_cmd.extend(["--end", payload["end"]])
        if qgdata_token: _dry_cmd.extend(["--token", qgdata_token])
        _dry_env = {**os.environ, "QUANTCLAW_ROOT": str(PROJECT_ROOT), "QMT_PROJECT_ROOT": str(PROJECT_ROOT)}
        _dry_log = store.run_dir / "dryrun.log"
        _dry_proc = start_process(_dry_cmd, _dry_log, env=_dry_env)
        _dry_timeout = 120
        _dry_t0 = time.time()
        while _dry_proc.poll() is None:
            if time.time() - _dry_t0 > _dry_timeout: _dry_proc.kill(); break
            time.sleep(1)
        _dry_proc.wait() #reap子进程，确保returncode不为None
        _dry_ret = _dry_proc.returncode
        if _dry_ret != 0:
            _dry_output = _dry_log.read_text(encoding="utf-8", errors="replace")[-2000:] if _dry_log.exists() else ""
            _dry_tb = ""; _dry_msg = f"dry run exit code={_dry_ret}"
            for line in reversed(_dry_output.splitlines()):
                line = line.strip()
                if line and ("Error" in line or "error" in line) and not line.startswith("["):
                    _dry_msg = line[:200]; break
            for i, line in enumerate(_dry_output.splitlines()):
                if "Traceback" in line: _dry_tb = "\n".join(_dry_output.splitlines()[i:]); break
            _structured_error(state, "dryrun_error", "strategy_dryrun", _dry_msg, _dry_tb)
            state["status"] = "failed"
            _fail_report(state, _dry_msg)
            monitor_step(monitor_base, step="3", status="failed", title="冒烟测试失败", msg=_dry_msg[:200], run_id=run_id)
            store.save(state)
            return 1
        monitor_step(monitor_base, step="3", status="success", title="冒烟测试通过", msg=f"{len(_dry_syms)}只标的×{_dry_max_bars}根K线无异常", run_id=run_id)
        print(f"[dry-run] 通过 ({len(_dry_syms)}只标的×{_dry_max_bars}根K线, {int(time.time()-_dry_t0)}秒)")

        monitor_step(monitor_base, step="4", status="running", title="回测执行", msg="回测已启动", run_id=run_id)
        cmd = [
            payload["python_bin"],
            str(BACKTEST_RUNNER),
            "--strategy",
            module_name,
            "--class",
            class_name,
            "--symbols",
            ",".join(parsed["symbols"]),
            "--mode",
            parsed.get("mode", "cta"),
            "--interval",
            payload["interval"],
            "--capital",
            str(payload["capital"]),
            "--rate",
            str(payload["rate"]),
            "--slippage",
            str(payload["slippage"]),
            "--size",
            str(payload["size"]),
            "--pricetick",
            str(payload["pricetick"]),
            "--output",
            output_prefix,
            "--title",
            payload["title"] or f"Auto MA Cross {run_id}",
            "--monitor-port",
            str(payload["monitor_port"]),
            "--run-id",
            run_id,
            "--monitor-keepalive-sec",
            "5",
        ]
        if payload.get("start"):
            cmd.extend(["--start", payload["start"]])
        if payload.get("end"):
            cmd.extend(["--end", payload["end"]])
        if qgdata_token:
            cmd.extend(["--token", qgdata_token])

        run_log_path = store.run_dir / "backtest.log"
        proc = start_process(cmd, run_log_path, env={**os.environ, "QUANTCLAW_ROOT": str(PROJECT_ROOT), "QMT_PROJECT_ROOT": str(PROJECT_ROOT)})
        state["process"]["backtest_pid"] = proc.pid
        store.save(state)

        timeout_sec = int(payload.get("timeout_sec", 1200))
        deadline = time.time() + timeout_sec
        while True:
            ret = proc.poll()
            if ret is not None:
                if ret != 0:
                    raise RuntimeError(f"backtest runner exit code={ret}")
                break
            if time.time() > deadline:
                proc.kill()
                raise TimeoutError(f"backtest timeout after {timeout_sec}s")
            time.sleep(2)

        monitor_step(monitor_base, step="4", status="success", title="回测执行", msg="回测进程已结束", run_id=run_id) #与前端时间线 td3 对齐（此前仅有 running 无 success）
        summary_path = BACKTESTS_DIR / f"{output_prefix}_summary.json"
        if summary_path.exists():
            summary = read_json(summary_path)
            state["artifacts"]["summary_file"] = str(summary_path)
            state["artifacts"]["summary"] = summary
            report_data_path = BACKTESTS_DIR / f"{output_prefix}_report_data.json"
            report_data = read_json(report_data_path) if report_data_path.exists() else {}
            result_warnings = _validate_result(summary, report_data, parsed.get("mode", "cta")) #Step5: 结果校验
            if result_warnings:
                state["result_warnings"] = result_warnings
                warn_msg = "结果校验告警:\n" + "\n".join(f"  ⚠ {w}" for w in result_warnings)
                print(f"[validate] {warn_msg}", flush=True)
                monitor_post(monitor_base, "/api/log", {"msg": warn_msg})
                monitor_post(monitor_base, "/api/result_warnings", {"warnings": result_warnings})
                monitor_step(monitor_base, step="5", status="warning", title="结果校验", msg=f"发现{len(result_warnings)}个告警", run_id=run_id)
            else:
                monitor_step(monitor_base, step="5", status="success", title="结果校验", msg="校验通过", run_id=run_id)
            strategy_code = "" #Step6: 生成报告
            sf = state["artifacts"].get("strategy_file", "")
            if sf and Path(sf).exists():
                try: strategy_code = Path(sf).read_text(encoding="utf-8")
                except Exception: pass
            report_html = generate_report_html(run_id=run_id, report_data=report_data, summary=summary, strategy_code=strategy_code, parsed=parsed)
            report_html_path = BACKTESTS_DIR / f"{output_prefix}_report.html"
            report_html_path.write_text(report_html, encoding="utf-8")
            state["artifacts"]["report_html"] = str(report_html_path)
            published_reports, publish_err = publish_static_reports(
                run_id=run_id,
                output_prefix=output_prefix,
                report_public_base=payload.get("report_public_base", ""),
                report_public_dir=payload.get("report_public_dir", ""),
            )
            if published_reports:
                state["artifacts"]["report_public_urls"] = published_reports
                payload["report_url"] = published_reports.get(f"{run_id}_report.html", published_reports.get(f"{run_id}.html", payload.get("report_url", "")))
                payload["report_replay_url"] = published_reports.get(f"{run_id}_replay.html", payload.get("report_replay_url", ""))
                payload["report_summary_url"] = published_reports.get(f"{run_id}_summary.json", payload.get("report_summary_url", ""))
                state["payload"] = payload
            elif publish_err and publish_err != "REPORT_PUBLIC_BASE not configured":
                store.append_error(state, f"report publish warning: {publish_err}")
            report_url_final = payload.get("report_url", "")
            monitor_post(monitor_base, "/api/report_urls", {
                "report_url": report_url_final,
                "report_replay_url": payload.get("report_replay_url", ""),
                "report_summary_url": payload.get("report_summary_url", ""),
            })
            monitor_step(monitor_base, step="6", status="success", title="报告生成", msg="回测完成，结果已生成", run_id=run_id)
            store.mark_step(state, "result", "success", str(summary_path))
        else:
            store.mark_step(state, "result", "running", "summary pending")

        state["status"] = "completed"
        store.save(state)
        return 0
    except subprocess.CalledProcessError as exc:
        import traceback as _tb
        state["status"] = "failed"
        _structured_error(state, "compile_error", "strategy_generation", str(exc), _tb.format_exc())
        _fail_report(state, str(exc))
        monitor_step(monitor_base, step="9", status="failed", title="编译失败", msg=str(exc)[:200], run_id=run_id)
        store.save(state)
        return 1
    except EngineCompatError as exc:
        import traceback as _tb
        state["status"] = "failed"
        _structured_error(state, "compat_error", "engine_compatibility", str(exc), _tb.format_exc())
        _fail_report(state, str(exc))
        monitor_step(monitor_base, step="9", status="failed", title="引擎兼容性不支持", msg=str(exc)[:200], run_id=run_id)
        store.save(state)
        return 1
    except ValueError as exc:
        import traceback as _tb
        state["status"] = "failed"
        _structured_error(state, "lint_error", "strategy_generation", str(exc), _tb.format_exc())
        _fail_report(state, str(exc))
        monitor_step(monitor_base, step="9", status="failed", title="静态检查失败", msg=str(exc)[:200], run_id=run_id)
        store.save(state)
        return 1
    except TimeoutError as exc:
        import traceback as _tb
        state["status"] = "failed"
        _structured_error(state, "timeout_error", "backtest_execution", str(exc), _tb.format_exc())
        _fail_report(state, str(exc))
        monitor_step(monitor_base, step="9", status="failed", title="回测超时", msg=str(exc)[:200], run_id=run_id)
        store.save(state)
        return 1
    except RuntimeError as exc:
        import traceback as _tb
        tb_str = _tb.format_exc()
        etype = "data_error" if any(k in str(exc) for k in ["0 bars", "无数据", "data", "token"]) else "runtime_error"
        state["status"] = "failed"
        _structured_error(state, etype, "backtest_execution", str(exc), tb_str)
        _fail_report(state, str(exc))
        monitor_step(monitor_base, step="9", status="failed", title="执行失败", msg=str(exc)[:200], run_id=run_id)
        store.save(state)
        return 1
    except Exception as exc:
        import traceback as _tb
        state["status"] = "failed"
        _structured_error(state, "runtime_error", "unknown", str(exc), _tb.format_exc())
        _fail_report(state, str(exc))
        monitor_step(monitor_base, step="9", status="failed", title="执行失败", msg=str(exc)[:200], run_id=run_id)
        store.save(state)
        return 1
    finally:
        done_ok = monitor_post(monitor_base, "/api/done", {})
        mon_pid = state.get("process", {}).get("monitor_pid")
        # done 回调成功时保留短窗口供用户查看失败日志；仅在回调失败时兜底强杀，防泄漏。
        if mon_pid and not done_ok:
            try: os.kill(mon_pid, 15)
            except OSError: pass


def cmd_status(args: argparse.Namespace) -> int:
    state = RunStore(args.run_id).load()
    payload = state.get("payload", {})
    if isinstance(payload, dict) and not payload.get("report_url"):
        monitor_url = payload.get("monitor_url", "")
        if monitor_url and "/runs/" in monitor_url:
            base = monitor_url.split("/runs/", 1)[0]
            prefix = f"run_{state.get('run_id', args.run_id)}"
            payload["report_url"] = f"{base}/reports/{prefix}_report.html"
            payload["report_replay_url"] = f"{base}/reports/{prefix}_replay.html"
            payload["report_summary_url"] = f"{base}/reports/{prefix}_summary.json"
            state["payload"] = payload
    errors = state.get("errors", [])
    if errors:
        last = errors[-1]
        state["last_error"] = {"error_type": last.get("error_type", "unknown"), "step": last.get("step", ""), "message": last.get("message", str(last))}
    print(json.dumps(state, ensure_ascii=False, indent=2))
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    runs = sorted(RUNS_DIR.glob("*/state.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    payload = []
    for p in runs[: args.limit]:
        st = read_json(p)
        payload.append(
            {
                "run_id": st["run_id"],
                "status": st.get("status"),
                "updated_at": st.get("updated_at"),
                "monitor_url": st.get("payload", {}).get("monitor_url"),
                "report_url": st.get("payload", {}).get("report_url")
                or (
                    f"{st.get('payload', {}).get('monitor_url', '').split('/runs/', 1)[0]}/reports/run_{st['run_id']}_report.html"
                    if "/runs/" in st.get("payload", {}).get("monitor_url", "")
                    else ""
                ),
            }
        )
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Quant strategy orchestration pipeline")
    sub = parser.add_subparsers(dest="cmd", required=True)

    submit = sub.add_parser("submit", help="Submit a run and return monitor URL immediately")
    submit.add_argument("--requirement", required=True, help="Natural language strategy requirement")
    submit.add_argument("--run-id", default="", help="Optional custom run id")
    submit.add_argument("--symbols", default="", help="Optional symbols CSV override")
    submit.add_argument("--monitor-port", type=int, default=0, help="Optional fixed monitor port")
    submit.add_argument(
        "--monitor-port-candidates",
        default=os.getenv("ORCH_MONITOR_PORT_CANDIDATES", ",".join(str(p) for p in DEFAULT_MONITOR_PORTS)),
        help="白名单端口CSV（必须在防火墙放通），默认 8767",
    )
    submit.add_argument("--monitor-public-base", default=os.getenv("MONITOR_PUBLIC_BASE", ""))
    submit.add_argument("--report-public-base", default=os.getenv("REPORT_PUBLIC_BASE", ""))
    submit.add_argument("--report-public-dir", default=os.getenv("REPORT_PUBLIC_DIR", str(DEFAULT_REPORT_PUBLIC_DIR)))
    submit.add_argument("--python-bin", default=DEFAULT_PYTHON_BIN)
    submit.add_argument("--token", default="")
    submit.add_argument("--start", default="")
    submit.add_argument("--end", default="")
    submit.add_argument("--interval", default="")
    submit.add_argument("--capital", type=float, default=1000000)
    submit.add_argument("--rate", type=float, default=0.0003)
    submit.add_argument("--slippage", type=float, default=0.01)
    submit.add_argument("--size", type=float, default=1)
    submit.add_argument("--pricetick", type=float, default=0.01)
    submit.add_argument("--title", default="")
    submit.add_argument("--timeout-sec", type=int, default=int(os.getenv("ORCH_BACKTEST_TIMEOUT_SEC", "1200")))
    submit.add_argument("--strategy-file", default="", help="Pre-generated strategy .py file path (Shift-Left mode)")
    submit.add_argument("--strategy-module", default="", help="Strategy module name (default: derived from file)")
    submit.add_argument("--strategy-class", default="", help="Strategy class name (default: auto-detect from file)")

    worker = sub.add_parser("worker", help="Internal worker command")
    worker.add_argument("--run-id", required=True)

    status = sub.add_parser("status", help="Read run state")
    status.add_argument("--run-id", required=True)

    ls_cmd = sub.add_parser("list", help="List recent runs")
    ls_cmd.add_argument("--limit", type=int, default=20)

    sub.add_parser("config-doctor", help="一键诊断所有必需配置项")
    qmt_chk = sub.add_parser("qmt-check", help="检测 QMT 环境（自动发现路径+连接测试）")
    qmt_chk.add_argument("--account-id", default="", help="资金账号（可选，留空读环境变量）")

    probe_cmd = sub.add_parser("probe", help="独立探针：连接 QMT + 下单/撤单验证")
    probe_cmd.add_argument("--symbol", default="600519.SSE", help="探针标的（默认贵州茅台）")
    probe_cmd.add_argument("--account-id", default="", help="资金账号")
    probe_cmd.add_argument("--mock", action="store_true", help="Linux mock 模式")

    trade_cmd = sub.add_parser("trade", help="启动实盘/模拟交易（需 Windows + QMT）")
    trade_cmd.add_argument("--run-id", default="", help="回测 run_id（从中提取策略信息）")
    trade_cmd.add_argument("--strategy-file", default="", help="策略文件（与 run-id 二选一）")
    trade_cmd.add_argument("--strategy-class", default="")
    trade_cmd.add_argument("--symbols", default="")
    trade_cmd.add_argument("--mode", default="cta", choices=["cta", "portfolio"])
    trade_cmd.add_argument("--interval", default="", help="留空则从 run_id 解析，兜底 DAILY")
    trade_cmd.add_argument("--capital", type=float, default=1000000)
    trade_cmd.add_argument("--mock", action="store_true", help="Linux mock 模式")
    trade_cmd.add_argument("--account-id", default="", help="资金账号（留空读 QMT_ACCOUNT_ID 环境变量）")
    trade_cmd.add_argument("--token", default="")

    trade_stop_cmd = sub.add_parser("trade-stop", help="停止交易")
    trade_stop_cmd.add_argument("--run-id", required=True)

    opt = sub.add_parser("optimize", help="参数优化（穷举/遗传算法）")
    opt.add_argument("--strategy-file", required=True, help="策略文件路径")
    opt.add_argument("--strategy-class", required=True, help="策略类名")
    opt.add_argument("--symbols", required=True, help="标的代码（如 600519.SSE）")
    opt.add_argument("--optimize-params", required=True, help='优化参数JSON: {"target":"sharpe_ratio","params":{"fast_window":[5,30,5]}}')
    _d_end = datetime.now().strftime("%Y%m%d")
    _d_start = (datetime.now() - timedelta(days=365)).strftime("%Y%m%d")
    opt.add_argument("--start", default=_d_start)
    opt.add_argument("--end", default=_d_end)
    opt.add_argument("--interval", default="DAILY")
    opt.add_argument("--capital", type=float, default=1000000)
    opt.add_argument("--rate", type=float, default=0.0003)
    opt.add_argument("--slippage", type=float, default=0.01)
    opt.add_argument("--size", type=float, default=1)
    opt.add_argument("--pricetick", type=float, default=0.01)
    opt.add_argument("--top-n", type=int, default=10, help="返回前N组最优参数")

    return parser


def cmd_config_doctor(_args: argparse.Namespace) -> int:
    """逐项校验所有环境配置，输出 PASS/FAIL/WARN 清单"""
    results: list[Dict[str, str]] = []
    all_ok = True

    def _check(name: str, ok: bool, val: str, hint: str):
        nonlocal all_ok
        status = "PASS" if ok else "FAIL"
        if not ok:
            all_ok = False
        results.append({"check": name, "status": status, "value": val or "(空)", "hint": hint})

    def _warn(name: str, val: str, hint: str):
        results.append({"check": name, "status": "WARN", "value": val or "(空)", "hint": hint})

    root = os.getenv("QUANTCLAW_ROOT", "") or os.getenv("QMT_PROJECT_ROOT", "")
    root_ok = bool(root) and Path(root).is_dir() and (Path(root) / "backtests" / "pipeline_orchestrator.py").exists()
    _check("QUANTCLAW_ROOT", root_ok, root, "项目根目录，应包含 backtests/pipeline_orchestrator.py（也接受 QMT_PROJECT_ROOT）" if not root_ok else "OK")

    py = os.getenv("PYTHON_BIN", "") or DEFAULT_PYTHON_BIN
    py_ok = shutil.which(py) is not None
    _check("PYTHON_BIN", py_ok, py, f"找不到 {py}，请安装或修正路径" if not py_ok else "OK")

    mpb = resolve_monitor_public_base("")
    mpb_valid, mpb_err = validate_monitor_public_base(mpb)
    _local_doc = _is_local_mode(mpb)
    if _local_doc:
        _check("MONITOR_PUBLIC_BASE", True, mpb or "(本地模式，自动使用 127.0.0.1)", "本地部署模式，无需公网地址")
    else:
        _check("MONITOR_PUBLIC_BASE", mpb_valid, mpb or "(空)", mpb_err if not mpb_valid else "OK")

    ports_raw = os.getenv("ORCH_MONITOR_PORT_CANDIDATES", ",".join(str(p) for p in DEFAULT_MONITOR_PORTS))
    ports = [int(x) for x in ports_raw.split(",") if x.strip().isdigit()]
    if _local_doc: #本地模式跳过公网端口连通性测试
        _warn("端口公网可达", ports_raw, "本地模式，跳过公网端口探测（仅需浏览器访问 127.0.0.1）")
    elif mpb_valid and ports:
        port_results = []
        for p in ports:
            try:
                with socket.create_connection((urlparse(mpb).hostname or "", p), timeout=2.0):
                    port_results.append((p, True, ""))
            except Exception as e:
                port_results.append((p, False, str(e)))
        any_ok = any(ok for _, ok, _ in port_results)
        detail = "; ".join(f"{p}={'通' if ok else '不通('+err+')'}" for p, ok, err in port_results)
        _check("端口公网可达", any_ok, detail, "请在安全组/防火墙放通这些端口" if not any_ok else "OK")
    else:
        _warn("端口公网可达", ports_raw, "需先修复 MONITOR_PUBLIC_BASE 才能测试端口连通性")

    token, token_src = resolve_qgdata_token("")
    token_ok = bool(token)
    if token_ok:
        try:
            import qgdata as qg  # type: ignore
            qg.set_token(token)
            pro = qg.pro_api(timeout=5.0)
            df = qg_call(lambda: pro.stock_basic(exchange="", list_status="L", fields="ts_code", limit=1))
            token_ok = df is not None and len(df) > 0
            _check("QGDATA_TOKEN", token_ok, f"{mask_token(token)}(来源:{token_src})", "Token 校验通过" if token_ok else f"Token 无效或接口无权限，请到 {QGDATA_RECHARGE_URL} 确认套餐或充值")
        except Exception as e:
            _check("QGDATA_TOKEN", False, f"{mask_token(token)}(来源:{token_src})", f"Token 校验异常: {e}。充值/获取: {QGDATA_RECHARGE_URL}")
    else:
        _check("QGDATA_TOKEN", False, "", f"未配置，前往 {QGDATA_RECHARGE_URL} 获取")

    ctrl = os.getenv("OPENCLAW_CONTROL_URL", "") or read_env_value_from_files("OPENCLAW_CONTROL_URL", [PROJECT_ROOT / ".env", Path.home() / ".openclaw" / ".env"])
    if ctrl:
        _warn("OPENCLAW_CONTROL_URL", ctrl, "已配置（用于自动推导 MONITOR_PUBLIC_BASE）")
    else:
        _warn("OPENCLAW_CONTROL_URL", "", "未配置（可选，可用于自动推导公网基址）")

    rpb = os.getenv("REPORT_PUBLIC_BASE", "")
    rpd = os.getenv("REPORT_PUBLIC_DIR", str(DEFAULT_REPORT_PUBLIC_DIR))
    if rpb:
        _warn("REPORT_PUBLIC_BASE", rpb, "已配置")
    else:
        _warn("REPORT_PUBLIC_BASE", "", "未配置（可选，用于持久化报告公网链接）")
    rpd_ok = Path(rpd).is_dir() or not rpb
    if rpb and not rpd_ok:
        _check("REPORT_PUBLIC_DIR", False, rpd, "目录不存在，请创建或修正")
    else:
        _warn("REPORT_PUBLIC_DIR", rpd, "OK" if rpd_ok else "目录不存在")

    env_file = PROJECT_ROOT / ".env"
    if env_file.exists():
        _warn(".env 文件", str(env_file), "已存在")
    else:
        example = PROJECT_ROOT.parent / ".env.example"
        hint = f"不存在。建议: cp {example} {env_file} 然后编辑" if example.exists() else "不存在。建议创建 .env 文件配置环境变量"
        _warn(".env 文件", str(env_file), hint)

    print("\n" + "=" * 60)
    print("  QuantClaw Config Doctor")
    print("  https://gitee.com/GuojinQuant/quant-claw")
    print("=" * 60)
    for r in results:
        icon = {"PASS": "✓", "FAIL": "✗", "WARN": "⚠"}[r["status"]]
        print(f"\n  {icon} [{r['status']}] {r['check']}")
        print(f"    值: {r['value']}")
        print(f"    {r['hint']}")
    print("\n" + "-" * 60)
    if all_ok:
        print("  所有必需项通过 ✓  可以正常运行")
    else:
        fail_count = sum(1 for r in results if r["status"] == "FAIL")
        print(f"  {fail_count} 项未通过，请按提示修复后重新运行:")
        print(f"  python3 {Path(__file__).name} config-doctor")
        print(f"\n  详细配置指南: https://gitee.com/GuojinQuant/quant-claw#第四步配置环境变量")
    print("=" * 60 + "\n")
    return 0 if all_ok else 1


def cmd_optimize(args: argparse.Namespace) -> int:
    """参数优化：穷举遍历参数组合，返回最优参数集（JSON）"""
    strategy_file = Path(args.strategy_file).resolve()
    if not strategy_file.exists():
        print(json.dumps({"status": "error", "error": f"策略文件不存在: {strategy_file}"}, ensure_ascii=False))
        return 1
    try:
        opt_cfg = json.loads(args.optimize_params)
    except json.JSONDecodeError as e:
        print(json.dumps({"status": "error", "error": f"optimize-params JSON 解析失败: {e}"}, ensure_ascii=False))
        return 1
    target = opt_cfg.get("target", "sharpe_ratio")
    param_ranges = opt_cfg.get("params", {})
    if not param_ranges:
        print(json.dumps({"status": "error", "error": "params 为空，需指定至少一个参数范围 {\"name\": [start, end, step]}"}, ensure_ascii=False))
        return 1
    vnpy_qmt_path = PROJECT_ROOT / "vnpy_qmt"
    for p in [str(vnpy_qmt_path), str(STRATEGIES_DIR), str(strategy_file.parent)]:
        if p not in sys.path:
            sys.path.insert(0, p)
    try:
        import importlib
        mod = importlib.import_module(strategy_file.stem)
        cls_name = args.strategy_class
        if not hasattr(mod, cls_name):
            low = cls_name.lower()
            hit = [n for n in dir(mod) if n.lower() == low]
            cls_name = hit[0] if hit else cls_name
        strategy_cls = getattr(mod, cls_name)
    except Exception as e:
        print(json.dumps({"status": "error", "error": f"策略导入失败: {e}"}, ensure_ascii=False))
        return 1
    try:
        from vnpy_ctastrategy.backtesting import BacktestingEngine
        from vnpy.trader.optimize import OptimizationSetting
        from vnpy.trader.constant import Interval
        from vnpy.trader.setting import SETTINGS
        qgdata_token = os.getenv("QGDATA_TOKEN", "") or resolve_qgdata_token("")[0]
        if qgdata_token:
            SETTINGS["datafeed.name"] = "qg"
            SETTINGS["datafeed.password"] = qgdata_token
        vt_symbol = args.symbols.split(",")[0].strip()
        interval = getattr(Interval, args.interval)
        start_dt = datetime.strptime(args.start, "%Y%m%d")
        end_dt = datetime.strptime(args.end, "%Y%m%d")
        engine = BacktestingEngine()
        engine.set_parameters(vt_symbol=vt_symbol, interval=interval, start=start_dt, end=end_dt,
            rate=args.rate, slippage=args.slippage, size=args.size, pricetick=args.pricetick, capital=args.capital)
        engine.add_strategy(strategy_cls, {})
        engine.load_data()
        bar_count = len(getattr(engine, "history_data", []) or [])
        if bar_count == 0:
            print(json.dumps({"status": "error", "error": "数据库无缓存数据，请先运行一次回测以下载并缓存行情数据"}, ensure_ascii=False))
            return 1
        setting = OptimizationSetting()
        setting.set_target(target)
        for name, rng in param_ranges.items():
            setting.add_parameter(name, rng[0], rng[1], rng[2])
        total_combinations = len(setting.generate_settings())
        use_ga = opt_cfg.get("algorithm", "bf") == "ga"
        results = engine.run_ga_optimization(setting, output=False) if use_ga else engine.run_optimization(setting, output=False)
        top_n = min(args.top_n, len(results))
        formatted = []
        for setting_dict, target_val, stats in results[:top_n]:
            key_stats = {}
            for k in ["total_return", "annual_return", "max_ddpercent", "sharpe_ratio", "total_trade_count", "winning_rate"]:
                v = stats.get(k)
                if v is not None:
                    key_stats[k] = round(float(v), 4) if isinstance(v, float) else v
            formatted.append({"params": setting_dict, target: round(float(target_val), 6) if target_val else 0, "stats": key_stats})
        output = {"status": "completed", "target_metric": target, "algorithm": "ga" if use_ga else "bf",
            "total_combinations": total_combinations, "bar_count": bar_count, "top_n": top_n,
            "results": formatted, "best": formatted[0] if formatted else None}
        print(json.dumps(output, ensure_ascii=False, indent=2, default=str))
        return 0
    except Exception as e:
        import traceback
        print(json.dumps({"status": "error", "error": f"{type(e).__name__}: {e}", "traceback": traceback.format_exc()[-500:]}, ensure_ascii=False))
        return 1


def _auto_discover_qmt_path() -> str:
    """自动发现 QMT 安装目录，复用 trade_runner 同一实现保持一致"""
    from trade_runner import auto_discover_qmt_path
    return auto_discover_qmt_path()

def cmd_qmt_check(args: argparse.Namespace) -> int:
    """检测 QMT 环境：自动发现路径 + 尝试连接验证 QMT 终端是否在线"""
    import platform as _plat
    result: Dict[str, Any] = {"platform": _plat.system(), "xtquant": False, "qmt_path": "", "qmt_path_ok": False,
        "qmt_connected": False, "account_id": "", "ready": False, "hint": ""}
    if _plat.system() != "Windows":
        result["hint"] = "当前为非 Windows 环境，模拟/实盘需在 Windows + QMT 下运行"
        print(json.dumps(result, ensure_ascii=False, indent=2)); return 1
    _orig_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        import xtquant; result["xtquant"] = True  # type: ignore  # noqa: F401
    except ImportError: pass
    finally: sys.stdout = _orig_stdout
    if not result["xtquant"]:
        result["hint"] = "缺少 xtquant 库，需安装 miniQMT SDK"
        print(json.dumps(result, ensure_ascii=False, indent=2)); return 1
    qmt_path = _auto_discover_qmt_path()
    result["qmt_path"] = qmt_path
    result["qmt_path_ok"] = bool(qmt_path) and (Path(qmt_path) / "userdata_mini").is_dir()
    if not result["qmt_path_ok"]:
        result["hint"] = "未找到 QMT 安装路径（自动扫描和 QMT_PATH 环境变量均未命中），请确认 QMT 已安装"
        print(json.dumps(result, ensure_ascii=False, indent=2)); return 1
    try: #尝试连接验证 QMT 终端是否运行
        from xtquant.xttrader import XtQuantTrader
        _session = int(time.time() * 1000) % 999999
        _trader = XtQuantTrader(str(Path(qmt_path) / "userdata_mini"), _session)
        _trader.start()
        if _trader.connect() == 0:
            result["qmt_connected"] = True
            try: _trader.stop(); del _trader
            except: pass
        else:
            result["hint"] = "QMT 安装目录已找到，但终端未运行。请先打开 QMT 并以极简模式登录"
            print(json.dumps(result, ensure_ascii=False, indent=2)); return 1
    except Exception as e:
        result["hint"] = f"QMT 连接测试异常: {e}"
        print(json.dumps(result, ensure_ascii=False, indent=2)); return 1
    account_id = getattr(args, "account_id", "") or os.getenv("QMT_ACCOUNT_ID", "")
    result["account_id"] = ("***" + account_id[-4:]) if len(account_id) > 4 else ("已配置" if account_id else "")
    if not account_id:
        result["hint"] = "QMT 已连接，但缺少资金账号。请通过 --account-id 或 QMT_ACCOUNT_ID 环境变量提供"
        result["qmt_connected"] = True #连接OK但缺账号
        print(json.dumps(result, ensure_ascii=False, indent=2)); return 1
    result["ready"] = True
    result["hint"] = "✅ QMT 环境就绪（路径自动发现，终端已连接，账号已配置）"
    print(json.dumps(result, ensure_ascii=False, indent=2)); return 0


def cmd_probe(args: argparse.Namespace) -> int:
    """独立探针：连接 QMT → 下100股 → 撤单，验证下单链路（不依赖策略）"""
    import platform as _plat, subprocess as _sp
    is_mock = args.mock or _plat.system() != "Windows"
    qmt_path = _auto_discover_qmt_path()
    account_id = args.account_id or os.getenv("QMT_ACCOUNT_ID", "")
    if not is_mock and not qmt_path:
        print(json.dumps({"status": "error", "error": "未找到 QMT 路径"}, ensure_ascii=False)); return 1
    if not is_mock and not account_id:
        print(json.dumps({"status": "error", "error": "缺少资金账号 --account-id / QMT_ACCOUNT_ID"}, ensure_ascii=False)); return 1
    probe_dir = RUNS_DIR / f"probe_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    probe_dir.mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, str(BACKTESTS_DIR / "trade_runner.py"),
        "--probe-only", "--symbols", args.symbol, "--state-dir", str(probe_dir)]
    if qmt_path: cmd.extend(["--qmt-path", qmt_path])
    if account_id: cmd.extend(["--account-id", account_id])
    if is_mock: cmd.append("--mock")
    result = _sp.run(cmd, capture_output=True, text=True, timeout=60, cwd=str(BACKTESTS_DIR))
    state_file = probe_dir / "trade_state.json"
    if state_file.exists():
        state = read_json(state_file)
        state["stdout_tail"] = result.stdout.strip().split("\n")[-10:]
        print(json.dumps(state, ensure_ascii=False, indent=2))
        return 0 if state.get("probe_ok") or state.get("status") == "probe_done" else 1
    print(json.dumps({"status": "error", "error": "探针进程未产生状态文件", "stdout": result.stdout[-500:], "stderr": result.stderr[-500:]}, ensure_ascii=False))
    return 1

def cmd_trade(args: argparse.Namespace) -> int:
    """启动实盘/模拟交易"""
    import platform as _plat, subprocess as _sp
    strategy_file = args.strategy_file; strategy_class = args.strategy_class; symbols = args.symbols; mode = args.mode; interval = args.interval
    if args.run_id: #从回测结果提取策略信息
        store = RunStore(args.run_id)
        if not store.state_file.exists():
            print(json.dumps({"status": "error", "error": f"run_id {args.run_id} 不存在"}, ensure_ascii=False)); return 1
        state = store.load()
        if state.get("status") != "completed":
            print(json.dumps({"status": "error", "error": f"run_id {args.run_id} 状态为 {state.get('status')}，需要 completed"}, ensure_ascii=False)); return 1
        sf = state.get("artifacts", {}).get("strategy_file", "")
        if sf and Path(sf).exists(): strategy_file = sf
        parsed = state.get("payload", {}).get("parsed", {})
        if not strategy_class: strategy_class = parsed.get("class_name", "")
        if not symbols: symbols = parsed.get("symbols", "")
        if isinstance(symbols, list): symbols = ",".join(symbols)
        if not mode: mode = parsed.get("mode", "cta")
        if not interval: interval = parsed.get("interval", "")
    if not interval: interval = "DAILY" #最终兜底
    if not strategy_file or not strategy_class or not symbols:
        print(json.dumps({"status": "error", "error": "缺少 --strategy-file/--strategy-class/--symbols（或通过 --run-id 提供）"}, ensure_ascii=False)); return 1
    if not Path(strategy_file).exists():
        print(json.dumps({"status": "error", "error": f"策略文件不存在: {strategy_file}"}, ensure_ascii=False)); return 1
    is_mock = args.mock or _plat.system() != "Windows"
    qmt_path = _auto_discover_qmt_path()
    account_id = getattr(args, "account_id", "") or os.getenv("QMT_ACCOUNT_ID", "")
    if _plat.system() != "Windows" and not args.mock:
        print(json.dumps({"status": "platform_redirect", "hint": "模拟/实盘交易需在 Windows + QMT 环境运行", "mock_available": True,
            "command": f'python "{BACKTESTS_DIR / "pipeline_orchestrator.py"}" trade --run-id {args.run_id or ""} --strategy-file "{strategy_file}" --strategy-class {strategy_class} --symbols "{symbols}"'}, ensure_ascii=False))
        return 0
    trade_dir = RUNS_DIR / f"trade_{args.run_id or datetime.now().strftime('%Y%m%d_%H%M%S')}"
    trade_dir.mkdir(parents=True, exist_ok=True)
    token = args.token or resolve_qgdata_token("")[0]
    cmd = [sys.executable, str(BACKTESTS_DIR / "trade_runner.py"),
        "--strategy-file", str(Path(strategy_file).resolve()), "--strategy-class", strategy_class,
        "--symbols", symbols, "--mode", mode, "--interval", interval,
        "--capital", str(args.capital), "--state-dir", str(trade_dir),
        "--datafeed-token", token]
    if qmt_path: cmd.extend(["--qmt-path", qmt_path])
    if account_id: cmd.extend(["--account-id", account_id])
    if is_mock: cmd.append("--mock")
    log_file = trade_dir / "trade.log"
    p_log = open(log_file, "w", encoding="utf-8")
    proc = _sp.Popen(cmd, stdout=p_log, stderr=_sp.STDOUT, cwd=str(BACKTESTS_DIR))
    p_log.close() #Popen 已 dup fd，父进程立即释放
    print(json.dumps({"status": "trading_started", "pid": proc.pid, "trade_dir": str(trade_dir),
        "log_file": str(log_file), "mock": is_mock, "strategy_class": strategy_class, "symbols": symbols}, ensure_ascii=False))
    return 0


def cmd_trade_stop(args: argparse.Namespace) -> int:
    """停止交易：写 _stop_flag 文件（跨平台）+ SIGTERM（Linux）"""
    import platform as _plat
    trade_dir = RUNS_DIR / f"trade_{args.run_id}"
    sf = trade_dir / "trade_state.json"
    if not sf.exists():
        print(json.dumps({"status": "error", "error": f"交易状态文件不存在: {sf}"}, ensure_ascii=False)); return 1
    state = read_json(sf)
    pid = state.get("pid")
    if not pid:
        print(json.dumps({"status": "error", "error": "未找到交易进程 PID"}, ensure_ascii=False)); return 1
    stop_flag = trade_dir / "_stop_flag"
    stop_flag.write_text("stop", encoding="utf-8") #跨平台通用
    if _plat.system() != "Windows": #Linux/Mac 额外发 SIGTERM 加速
        try: os.kill(pid, signal.SIGTERM)
        except ProcessLookupError: pass
        except Exception: pass
    print(json.dumps({"status": "stop_requested", "pid": pid, "method": "file_signal" if _plat.system() == "Windows" else "file_signal+SIGTERM"}, ensure_ascii=False))
    return 0


def main() -> int:
    args = build_parser().parse_args()
    if args.cmd == "submit":
        return cmd_submit(args)
    if args.cmd == "worker":
        return cmd_worker(args)
    if args.cmd == "status":
        return cmd_status(args)
    if args.cmd == "list":
        return cmd_list(args)
    if args.cmd == "config-doctor":
        return cmd_config_doctor(args)
    if args.cmd == "qmt-check":
        return cmd_qmt_check(args)
    if args.cmd == "probe":
        return cmd_probe(args)
    if args.cmd == "trade":
        return cmd_trade(args)
    if args.cmd == "trade-stop":
        return cmd_trade_stop(args)
    if args.cmd == "optimize":
        return cmd_optimize(args)
    return 1


if __name__ == "__main__":
    sys.exit(main())
