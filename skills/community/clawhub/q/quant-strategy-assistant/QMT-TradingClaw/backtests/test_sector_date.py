#!/usr/bin/env python3
"""板块/指数解析 + 日期解析 + lint 新增项 单元测试"""
import sys, os, json, re
from datetime import date, timedelta
from pathlib import Path
from unittest.mock import patch, MagicMock
sys.path.insert(0, str(Path(__file__).resolve().parent))
os.environ.setdefault("QUANTCLAW_ROOT", str(Path(__file__).resolve().parents[1]))

from pipeline_orchestrator import (
    THS_SECTOR_MAP, THS_SECTOR_ALIASES, INDEX_KW_MAP, _SECTOR_KEYS_DESC,
    _extract_sector_name, _parse_date_range, _lint_strategy,
    _resolve_index_members_em, _sector_cache_read, _sector_cache_write,
    normalize_symbol,
)

passed, failed = 0, 0
def check(name, cond):
    global passed, failed
    if cond: passed += 1; print(f"  ✓ {name}")
    else: failed += 1; print(f"  ✗ {name}")

# ═══════════ 板块名提取测试 ═══════════
print("\n=== 板块名提取 ===")
check("T1: '银行板块均线策略' → 银行", _extract_sector_name("银行板块均线策略") == "银行")
check("T2: '人工智能板块中的半导体' → 人工智能", _extract_sector_name("人工智能板块中的半导体") == "人工智能")
check("T3: '设计一个行业轮动策略' → None（不误提取'一个'）", _extract_sector_name("设计一个行业轮动策略") is None)
check("T4: '最近三周行业表现' → None（不误提取'三周'）", _extract_sector_name("最近三周行业表现") is None)
check("T5: '做一个关于新能源的策略' → 新能源汽车（别名）", _extract_sector_name("做一个关于新能源的策略") == "新能源汽车")
check("T6: '沪深300成分股中的银行股' → 沪深300", _extract_sector_name("沪深300成分股中的银行股") == "沪深300")
check("T7: '贵州茅台上穿10日均线' → None", _extract_sector_name("贵州茅台上穿10日均线") is None)
check("T8: '半导体行业龙头' → 半导体", _extract_sector_name("半导体行业龙头") == "半导体")
check("T9: '医药概念轮动' → 医疗（别名）", _extract_sector_name("医药概念轮动") == "医疗")
check("T10: 'AIGC板块' → AIGC", _extract_sector_name("AIGC板块") == "AIGC")
check("T11: '每个行业龙头' → None（排除'每个'）", _extract_sector_name("每个行业龙头") is None)
check("T12: '新能源汽车概念' → 新能源汽车（完整匹配优先于'新能源'）", _extract_sector_name("新能源汽车概念") == "新能源汽车")

# ═══════════ 静态映射完整性测试 ═══════════
print("\n=== 静态映射完整性 ===")
check("T13: THS_SECTOR_MAP 至少60条", len(THS_SECTOR_MAP) >= 60)
check("T14: 所有 value 以 .TI 结尾", all(v.endswith(".TI") for v in THS_SECTOR_MAP.values()))
check("T15: 指数成分 883300/883304/883301 存在", all(k in THS_SECTOR_MAP for k in ["沪深300", "中证500", "上证50"]))
check("T16: 别名映射条目≥8", len(THS_SECTOR_ALIASES) >= 8)
check("T17: _SECTOR_KEYS_DESC 按长度降序", all(len(_SECTOR_KEYS_DESC[i]) >= len(_SECTOR_KEYS_DESC[i+1]) for i in range(len(_SECTOR_KEYS_DESC)-1)))

# ═══════════ 指数关键词映射测试 ═══════════
print("\n=== 指数关键词映射 ===")
check("T18: INDEX_KW_MAP 包含5个指数", len(INDEX_KW_MAP) == 5)
check("T19: 沪深300有ths和em_code", INDEX_KW_MAP["沪深300"]["ths"] == "883300.TI" and INDEX_KW_MAP["沪深300"]["em_code"] == "000300")
check("T20: 中证1000无ths", INDEX_KW_MAP["中证1000"]["ths"] is None)
check("T21: 创业板指有em_code", INDEX_KW_MAP["创业板指"]["em_code"] == "399006")

# ═══════════ 日期解析测试 ═══════════
print("\n=== 日期解析 ===")
today = date.today()
fmt = lambda d: d.strftime("%Y%m%d")

try:
    from dateutil.relativedelta import relativedelta as _rd
    has_rd = True
except ImportError:
    has_rd = False

r = _parse_date_range("最近1年均线交叉")
check("T22: '最近1年均线交叉' → 有结果", r is not None)
if r:
    if has_rd: exp = fmt(today - _rd(years=1))
    else: exp = fmt(today - timedelta(days=365))
    check("T22b: start 正确", r[0] == exp)
    check("T22c: end=today", r[1] == fmt(today))

r = _parse_date_range("最近三周走势")
check("T23: '最近三周走势' → 有结果", r is not None)
if r:
    check("T23b: start=today-21", r[0] == fmt(today - timedelta(weeks=3)))

r = _parse_date_range("今年以来的表现")
check("T24: '今年以来' → 有结果", r is not None)
if r:
    check("T24b: start=YYYY0101", r[0] == fmt(date(today.year, 1, 1)))

r = _parse_date_range("去年以来")
check("T25: '去年以来'", r is not None and r[0] == fmt(date(today.year-1, 1, 1)))

r = _parse_date_range("最近半年")
check("T26: '最近半年' → 有结果", r is not None)
if r:
    if has_rd: exp = fmt(today - _rd(months=6))
    else: exp = fmt(today - timedelta(days=183))
    check("T26b: start 约6月前", r[0] == exp)

r = _parse_date_range("过去3个月")
check("T27: '过去3个月' → 有结果", r is not None)
if r:
    if has_rd: exp = fmt(today - _rd(months=3))
    else: exp = fmt(today - timedelta(days=90))
    check("T27b: start 正确", r[0] == exp)

r = _parse_date_range("2024年以来")
check("T28: '2024年以来' → (20240101, today)", r == ("20240101", fmt(today)))

r = _parse_date_range("本月以来")
check("T29: '本月以来'", r is not None and r[0] == fmt(today.replace(day=1)))

r = _parse_date_range("本季度以来")
check("T30: '本季度以来'", r is not None)
if r:
    q = ((today.month - 1) // 3) * 3 + 1
    check("T30b: 季度首日", r[0] == fmt(date(today.year, q, 1)))

r = _parse_date_range("贵州茅台上穿10日均线")
check("T31: 无日期关键词 → None", r is None)

r = _parse_date_range("最近一年半的走势")
check("T32: '最近一年半' → 有结果", r is not None)
if r:
    if has_rd: exp = fmt(today - _rd(months=18))
    else: exp = fmt(today - timedelta(days=548))
    check("T32b: start 约18月前", r[0] == exp)

r = _parse_date_range("20240101-20241231")
check("T33: 精确区间 YYYYMMDD-YYYYMMDD", r == ("20240101", "20241231"))

r = _parse_date_range("从2023年6月到2024年3月")
check("T34: 从YYYY年M月到YYYY年M月", r is not None and r[0] == "20230601")

r = _parse_date_range("近100天")
check("T35: '近100天'", r is not None and r[0] == fmt(today - timedelta(days=100)))

# ═══════════ lint 新增检查测试 ═══════════
print("\n=== lint 新增检查 ===")

def lint_raises(source, mode="cta"):
    try: _lint_strategy(source, "test.py", mode); return False
    except ValueError: return True

def lint_warns(source, mode="cta"):
    import io, contextlib
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            _lint_strategy(source, "test.py", mode)
    except ValueError:
        pass
    return "告警" in buf.getvalue()

check("T36: pro.ths_member() → blocker", lint_raises('df = pro.ths_member(ts_code="883300.TI")'))
check("T37: pro.dc_member() → blocker", lint_raises('df = pro.dc_member (ts_code="x")'))
check("T38: self.vt_symbols=[...] portfolio → blocker", lint_raises('self.vt_symbols = ["600519.SSE"]', mode="portfolio"))
check("T39: self.vt_symbols==[...] 比较 → 不触发blocker", not lint_raises('if self.vt_symbols == ["600519.SSE"]: pass', mode="portfolio"))
check("T40: '600519.SH' → warning", lint_warns('x = "600519.SH"'))
check("T41: start_date='20240101' → warning", lint_warns('start_date = "20240101"'))
check("T42: self.capital portfolio → warning", lint_warns('vol = self.capital / price', mode="portfolio"))
check("T43: self.capital cta → 不触发", not lint_warns('vol = self.capital / price', mode="cta"))
check("T44: parameters=['capital'] portfolio → 不触发capital warning", not lint_warns('parameters = [\n    "capital",\n]\nclass Foo:\n    pass', mode="portfolio"))

# ═══════════ 缓存读写测试 ═══════════
print("\n=== 缓存读写 ===")
test_code = "__test_cache__"
test_syms = ["000001.SZSE", "600036.SSE"]
_sector_cache_write(test_code, test_syms)
cached = _sector_cache_read(test_code)
check("T45: 缓存写入后可读取", cached == test_syms)
# 清理
for f in Path(os.environ.get("QUANTCLAW_ROOT", ".")).joinpath("backtests/.sector_cache").glob(f"{test_code}_*.json"):
    f.unlink(missing_ok=True)

# ═══════════ normalize_symbol 基本测试 ═══════════
print("\n=== normalize_symbol ===")
check("T46: 600519.SH → 600519.SSE", normalize_symbol("600519.SH") == "600519.SSE")
check("T47: 000001.SZ → 000001.SZSE", normalize_symbol("000001.SZ") == "000001.SZSE")
check("T48: 600519.SSE 不变", normalize_symbol("600519.SSE") == "600519.SSE")

check("T51: 920009.BJ → 920009.BSE", normalize_symbol("920009.BJ") == "920009.BSE")
check("T52: 830799.BJ → 830799.BSE", normalize_symbol("830799.BJ") == "830799.BSE")
check("T53: 920009纯数字 → 920009.BSE", normalize_symbol("920009") == "920009.BSE")
check("T54: 430090纯数字 → 430090.BSE", normalize_symbol("430090") == "430090.BSE")
check("T55: 900901(B股)纯数字 → 900901.SSE", normalize_symbol("900901") == "900901.SSE")
check("T56: 870199纯数字 → 870199.BSE", normalize_symbol("870199") == "870199.BSE")

# ═══════════ 东方财富公开API解析测试 ═══════════
print("\n=== 东方财富公开API（实际网络调用） ===")
try:
    syms = _resolve_index_members_em("000016")  # 上证50
    check("T49: 上证50成分股≈50只", 40 <= len(syms) <= 60)
    check("T50: 成分股格式正确(.SSE/.SZSE)", all(s.endswith((".SSE", ".SZSE")) for s in syms))
except Exception as e:
    print(f"  ⚠ T49-T50 跳过(网络不可达): {e}")

# ═══════════ 汇总 ═══════════
print(f"\n{'='*40}")
print(f"通过: {passed}  失败: {failed}")
sys.exit(1 if failed else 0)
