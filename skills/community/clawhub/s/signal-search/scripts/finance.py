"""scripts/finance.py - 金融源（东方财富 push2，B1）。

产品原生检索域：用户搜「某公司近半年股市波动 / 股价 / 财报」时，由 connector 路由到此，
直接打东方财富 push2 接口族（实时行情 / 近半年 K 线 / 资金流），把**结构化数据**构为
source_type="finance" 文档进入质量层（M51 锚定 / SBA 打分）。

反爬核心：东方财富封 Python 客户端的 TLS(JA3) 指纹，故强制走**系统 curl 子进程**
（scrape._fetch_system_curl）绕过指纹封禁；失败时若调用方注入 `web_fetch` 则兜底抓东财网页，
否则记 warning。库内自包含、零金融第三方依赖。
"""

import json
import re
from typing import Any, Callable, Dict, List, Optional, Tuple
from urllib.parse import quote as _urlencode

import scrape

_CODE_PAT = re.compile(r"(?:sh|sz|bj)\s*(\d{6})|(\d{6})")
_REFERER = "https://quote.eastmoney.com/"
_F10_REFERER = "https://emweb.securities.eastmoney.com/"

# 财报意图触发词（命中则在行情 doc 之外追加独立财报 doc）
_REPORT_KW = [
    "财报",
    "营收",
    "利润",
    "资产负债",
    "现金流",
    "业绩",
    "季报",
    "年报",
    "中报",
    "一季报",
    "三季报",
    "每股收益",
    "净利润",
    "roe",
    "ROE",
]

# 开箱即用：常见 A 股名称→代码静态别名表（网络解析失败时的零依赖兜底；仅含歧义低的全称）。
# 仅 A 股 6 位代码（_secid 假定 0/3/6/8/4/9 开头），不含港股以免 secid 逻辑错位。
_NAME_ALIAS = {
    "贵州茅台": "600519",
    "茅台": "600519",
    "宁德时代": "300750",
    "比亚迪": "002594",
    "中国平安": "601318",
    "招商银行": "600036",
    "工商银行": "601398",
    "五粮液": "000858",
    "伊利股份": "600887",
    "美的集团": "000333",
    "格力电器": "000651",
    "东方财富": "300059",
    "中信证券": "600030",
    "京东方A": "000725",
    "海康威视": "002415",
    "立讯精密": "002475",
    "隆基绿能": "601012",
    "三一重工": "600031",
    "药明康德": "603259",
    "迈瑞医疗": "300760",
    "长江电力": "600900",
    "中芯国际": "688981",
    "汇川技术": "300124",
    "顺丰控股": "002352",
    "万华化学": "600309",
    "洋河股份": "002304",
    "平安银行": "000001",
    "兴业银行": "601166",
    "农业银行": "601288",
    "中国石油": "601857",
    "中国石化": "600028",
    "中国移动": "600941",
    "泸州老窖": "000568",
    "紫金矿业": "601899",
    "北方华创": "002371",
    "中国中免": "601888",
    "国电南瑞": "600406",
    "海尔智家": "600690",
    "福耀玻璃": "600660",
    "韦尔股份": "603501",
    "山西汾酒": "600809",
    "陕西煤业": "601225",
    "片仔癀": "600436",
    "通威股份": "600438",
    "歌尔股份": "002241",
}


def _parse_stock_code(query: str) -> Optional[str]:
    """从查询抽取 6 位股票代码（可带 sh/sz/bj 前缀）；优先带前缀的，否则任意 6 位数字。"""
    q = query or ""
    m = re.search(r"(?:sh|sz|bj)\s*(\d{6})", q, re.I)
    if m:
        return m.group(1)
    m = re.search(r"(?<!\d)(\d{6})(?!\d)", q)
    if m:
        return m.group(1)
    return None


def _secid(code: str) -> str:
    """沪/科创(6,9 开头) → 1.{code}；深/创业/北交(0,3,8,4) → 0.{code}。"""
    return f"1.{code}" if code[0] in "69" else f"0.{code}"


def _quote_url(code: str) -> str:
    prefix = "sh" if code[0] in "69" else "sz"
    return f"https://quote.eastmoney.com/{prefix}{code}.html"


def _resolve_name(name: str, cfg: Dict[str, Any]) -> Optional[str]:
    """名称→代码：先查静态别名表（零依赖、开箱即用），再打东财搜索前缀接口（系统 curl）。"""
    key = (name or "").strip()
    if key in _NAME_ALIAS:
        return _NAME_ALIAS[key]
    # 子串命中（如"贵州茅台股票"/"分析贵州茅台最近5年财报"）→ 取最长匹配，降低歧义
    hit = None
    for k, v in _NAME_ALIAS.items():
        if k in key and (hit is None or len(k) > len(hit[0])):
            hit = (k, v)
    if hit:
        return hit[1]
    try:
        url = (
            f"https://push2.eastmoney.com/api/qt/search/prefix?query={_urlencode(name)}"
            f"&type=1&count=5"
        )
        headers = scrape._coherent_headers()
        headers["Referer"] = _REFERER
        status, body, _ = scrape._fetch_system_curl(url, headers, None, 10)
        if status != 200 or not body:
            return None
        data = json.loads(body)
        for item in (data.get("data") or {}).get("list") or []:
            code = str(item.get("code") or "")
            if len(code) == 6 and code.isdigit():
                return code
    except Exception:
        return None
    return None


def _push2_get(url: str, timeout: int = 12) -> Tuple[int, Optional[dict]]:
    """经系统 curl 取 push2 JSON；返回 (status, parsed_dict|None)。"""
    headers = scrape._coherent_headers()
    headers["Referer"] = _REFERER
    status, body, _ = scrape._fetch_system_curl(url, headers, None, timeout)
    if status != 200 or not body:
        return status, None
    try:
        return 200, json.loads(body)
    except Exception:
        return status, None


def _num(v) -> Optional[float]:
    """push2 字段为字符串/数字混用；统一转 float，失败/缺失返回 None。"""
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _fmt_field(v, scale: float = 1.0, suffix: str = "") -> str:
    """还原 push2 放大字段并格式化：scale=100 表示 ×100 整型(分→元 / 百分点→%)。

    缺失返回占位符 '—'；统一 2 位小数（价格/百分比展示规范）。
    """
    n = _num(v)
    if n is None:
        return "—"
    n = n / scale
    return f"{n:.2f}{suffix}"


def _fmt_yuan(v) -> str:
    """金额（元）→ 亿/万/元 自适应展示；缺失返回占位符。"""
    n = _num(v)
    if n is None:
        return "—"
    if abs(n) >= 1e8:
        return f"{n / 1e8:.2f} 亿元"
    if abs(n) >= 1e4:
        return f"{n / 1e4:.2f} 万元"
    return f"{n:.2f} 元"


def _fmt_pct(v) -> str:
    """比率型百分比（东财 YSTZ/SJLTZ/ROE 已是百分数，如 10.67 表示 +10.67%）；缺失占位。"""
    n = _num(v)
    if n is None:
        return "—"
    return f"{n:.2f}%"


def _fmt_num(v) -> str:
    n = _num(v)
    if n is None:
        return "—"
    return f"{n:.2f}"


def _build_doc(
    code: str, secid: str, quote_url: str, q_data: dict, k_data: dict, f_data: dict
) -> Dict[str, Any]:
    d = (q_data or {}).get("data") or {}
    name = d.get("f58") or ""
    # push2 行情字段为整型放大值：价格(f43/f60)与换手率(f168)经 ÷100 还原（东财字段口径，
    # 来源: cnblogs 行情字段说明 / CocoLoop 技能常量表 2026）。
    # f170(市盈率TTM)/f116(总市值) 在不同字段集口径不一（有源标 f170=涨幅、PE 在 f162/f163），
    # 暂按原始值展示并标注，待用户确认口径后再归一化，避免臆造 ÷100 写出错数。
    price = _fmt_field(d.get("f43"), 100, " 元")
    prev_close = _fmt_field(d.get("f60"), 100, " 元")
    turnover = _fmt_field(d.get("f168"), 100, "%")
    pe = _fmt_field(d.get("f170"))  # 口径待核实
    mktcap = _fmt_field(d.get("f116"))  # 口径待核实

    klines: List[str] = []
    if k_data and k_data.get("data"):
        for row in (k_data["data"].get("klines") or [])[-10:]:
            p = row.split(",")
            if len(p) >= 11:
                # f51=日期 f52=开 f53=收 f54=高 f55=低 f56=量 f57=额 f58=振幅 f59=涨跌幅 f60=涨跌额 f61=换手率
                klines.append(f"{p[0]} 收{p[2]} 涨跌幅{p[8]}% 换手{p[10]}%")

    fflow: List[str] = []
    if f_data and f_data.get("data"):
        for row in (f_data["data"].get("klines") or [])[-5:]:
            p = row.split(",")
            if len(p) >= 7:
                fflow.append(f"{p[0]} 主力净流入{p[1]}")

    lines = [
        f"# 东方财富行情：{name}({code})",
        f"最新价: {price}  昨收: {prev_close}  换手: {turnover}  市盈率TTM: {pe}  总市值: {mktcap}",
        "## 近半年日K（末10交易日）",
        "\n".join(klines) or "（无）",
        "## 主力资金流（末5交易日）",
        "\n".join(fflow) or "（无）",
    ]
    return {
        "url": quote_url,
        "text": "\n".join(lines),
        "snippet": "\n".join(lines)[:240],
        "engine": "eastmoney",
        "source_type": "finance",
        "landing_resolved": True,
        "secid": secid,
        "code": code,
        "name": name,
        # D3 结构化引用字段（导出 BibTeX 时优先用 key / stock_code，纯 web 源退化为 URL）
        "citation": {
            "key": f"eastmoney-{code}",
            "stock_code": code,
            "name": name,
            "source": "eastmoney-push2",
        },
    }


def _report_intent(q: str) -> bool:
    """查询是否要求财报明细（营收/利润/资产负债/业绩等）。"""
    ql = (q or "").lower()
    return any(k.lower() in ql for k in _REPORT_KW)


def _f10_get(url: str, timeout: int = 12) -> Tuple[int, Optional[dict]]:
    """f10 财报接口经系统 curl 取 JSON（独立 Referer，绕 TLS 封禁）。"""
    headers = scrape._coherent_headers()
    headers["Referer"] = _F10_REFERER
    status, body, _ = scrape._fetch_system_curl(url, headers, None, timeout)
    if status != 200 or not body:
        return status, None
    try:
        return 200, json.loads(body)
    except Exception:
        return status, None


def _fetch_report(
    code: str, cfg: Dict[str, Any], web_fetch: Optional[Callable]
) -> Tuple[Optional[Dict[str, Any]], List[str]]:
    """东方财富 f10 业绩报表：最新一期摘要 + 近年（年度）序列，用于趋势/多年分析。

    取 pageSize=40 覆盖近年各报告期 → 过滤年报(报告期 12-31) → 取最近 5 个年度，
    输出逐年 营业收入/归母净利润/同比/EPS/ROE 序列；顶层保留最新一期摘要（可为单季）。
    趋势解读/CAGR 由调用方 LLM 完成（"调用方注入"哲学），库只给多年数字序列。
    返回 (doc|None, warnings)。主接口失败且无 web_fetch 兜底时返回 (None, warn)。
    """
    warnings: List[str] = []
    url = (
        "https://datacenter-web.eastmoney.com/api/data/v1/get"
        "?reportName=RPT_LICO_FN_CPD"
        "&columns=SECURITY_CODE,SECURITY_NAME_ABBR,REPORTDATE,"
        "TOTAL_OPERATE_INCOME,YSTZ,PARENT_NETPROFIT,SJLTZ,BASIC_EPS,WEIGHTAVG_ROE,PARENT_BIPS"
        f"&filter=(SECURITY_CODE=%22{code}%22)&pageSize=40&sortColumns=REPORTDATE&sortTypes=-1"
    )
    st, j = _f10_get(url)
    rows = (j.get("result") or {}).get("data") or [] if j else []
    if not rows:
        # 主接口被反爬拦截 → 若调用方注入 web_fetch 则兜底抓 f10 页面（退化：原文未结构化）
        if web_fetch:
            try:
                html = web_fetch(
                    f"https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/Index?"
                    f"type=web&code={'S' if code[0] in '69' else 'SZ'}{code}"
                )
                if html:
                    return {
                        "url": (
                            f"https://emweb.securities.eastmoney.com/PC_HSF10/"
                            f"NewFinanceAnalysis/Index?type=web&code="
                            f"{'S' if code[0] in '69' else 'SZ'}{code}"
                        ),
                        "text": f"# 东方财富 f10 财报页（接口被拦截，原始页未结构化）\n{str(html)[:2000]}",
                        "engine": "eastmoney-f10",
                        "source_type": "finance_report",
                        "landing_resolved": True,
                        "secid": f"{'1' if code[0] in '69' else '0'}.{code}",
                        "code": code,
                        "name": "",
                        "snippet": "",
                        "citation": {
                            "key": f"eastmoney-f10-{code}",
                            "stock_code": code,
                            "name": "",
                            "source": "eastmoney-f10-web",
                        },
                    }, warnings
            except Exception:
                pass
        warnings.append("东方财富 f10 财报接口暂不可用（可能为反爬拦截），且未注入 web_fetch 兜底")
        return None, warnings
    # 取最新报告期（接口默认未必按日期倒序，安全起见自排序）
    rows.sort(key=lambda r: str(r.get("REPORTDATE", "")), reverse=True)
    latest = rows[0]
    name = latest.get("SECURITY_NAME_ABBR") or ""
    # 年度序列：报告期以 -12-31 结尾视为年报，取最近 5 个年度（多年趋势分析）
    annual = [r for r in rows if str(r.get("REPORTDATE", ""))[5:10] == "12-31"][:5]
    lines = [
        f"# 东方财富 f10 财报（业绩报表）：{name}({code})",
        f"最新报告期: {str(latest.get('REPORTDATE', ''))[:10]}",
        f"营业收入: {_fmt_yuan(latest.get('TOTAL_OPERATE_INCOME'))}（同比 {_fmt_pct(latest.get('YSTZ'))}）",
        f"归母净利润: {_fmt_yuan(latest.get('PARENT_NETPROFIT'))}（同比 {_fmt_pct(latest.get('SJLTZ'))}）",
        f"基本每股收益: {_fmt_num(latest.get('BASIC_EPS'))} 元  加权平均ROE: "
        f"{_fmt_pct(latest.get('WEIGHTAVG_ROE'))}  每股净资产: {_fmt_num(latest.get('PARENT_BIPS'))} 元",
        "",
        "近年年度业绩（单位：亿元 / 元；同比%）：",
    ]
    for r in annual:
        rd = str(r.get("REPORTDATE", ""))[:10]
        lines.append(
            f"- {rd}：营收 {_fmt_yuan(r.get('TOTAL_OPERATE_INCOME'))}（同比 {_fmt_pct(r.get('YSTZ'))}）"
            f" | 归母净利润 {_fmt_yuan(r.get('PARENT_NETPROFIT'))}（同比 {_fmt_pct(r.get('SJLTZ'))}）"
            f" | EPS {_fmt_num(r.get('BASIC_EPS'))} | ROE {_fmt_pct(r.get('WEIGHTAVG_ROE'))}"
        )
    text = "\n".join(lines)
    prefix = "S" if code[0] in "69" else "SZ"
    f10_url = (
        f"https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/Index?"
        f"type=web&code={prefix}{code}"
    )
    return {
        "url": f10_url,
        "text": text,
        "snippet": text[:240],
        "engine": "eastmoney-f10",
        "source_type": "finance_report",
        "landing_resolved": True,
        "secid": f"{'1' if code[0] in '69' else '0'}.{code}",
        "code": code,
        "name": name,
        "citation": {
            "key": f"eastmoney-f10-{code}",
            "stock_code": code,
            "name": name,
            "source": "eastmoney-f10",
        },
    }, warnings


def fetch(
    query: str, cfg: Dict[str, Any] = None, web_fetch: Optional[Callable] = None
) -> Tuple[List[Dict[str, Any]], List[str]]:
    """金融源取数。返回 (docs, warnings)。

    - 解析代码/名称 → secid；打 push2 行情/K线(lmt=120≈近半年)/资金流。
    - 命中财报意图词（财报/营收/利润/业绩…）→ 额外追加 f10 业绩报表 doc（营收/净利/同比/EPS/ROE）。
    - 主传输（系统 curl）失败 → 若 web_fetch 注入则兜底抓东财网页；否则记 warning 返回空。
    """
    warnings: List[str] = []
    q = (query or "").strip()

    code = _parse_stock_code(q) or _resolve_name(q, cfg or {})
    if not code:
        return [], ["未能从查询中识别股票代码/名称，请提供代码（如 600519）后重试"]

    secid = _secid(code)
    quote_url = _quote_url(code)

    q_status, q_data = _push2_get(
        f"https://push2.eastmoney.com/api/qt/stock/get?secid={secid}"
        f"&fields=f43,f44,f45,f46,f57,f58,f60,f116,f117,f168,f169,f170"
    )
    k_status, k_data = _push2_get(
        f"https://push2his.eastmoney.com/api/qt/stock/kline/get?secid={secid}"
        f"&fields1=f1,f2,f3,f4,f5,f6&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61"
        f"&klt=101&fqt=1&lmt=120&end=20500101&beg=0"
    )
    f_status, f_data = _push2_get(
        f"https://push2.eastmoney.com/api/qt/stock/fflow/daykline/get?secid={secid}"
        f"&fields1=f1,f2,f3,f4&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61"
        f"&lmt=120&klt=101"
    )

    docs: List[Dict[str, Any]] = []
    if q_data and q_data.get("data"):
        docs.append(_build_doc(code, secid, quote_url, q_data, k_data, f_data))
    elif web_fetch:
        try:
            html = web_fetch(quote_url)
            if html:
                docs.append(
                    {
                        "url": quote_url,
                        "text": str(html),
                        "engine": "eastmoney",
                        "source_type": "finance",
                        "landing_resolved": True,
                        "secid": secid,
                        "code": code,
                        "citation": {
                            "key": f"eastmoney-{code}",
                            "stock_code": code,
                            "name": "",
                            "source": "eastmoney-web",
                        },
                    }
                )
        except Exception:
            pass

    # 财报明细（触发词命中时追加独立 doc）
    if _report_intent(q):
        rdoc, rwarns = _fetch_report(code, cfg or {}, web_fetch)
        if rdoc:
            docs.append(rdoc)
        warnings.extend(rwarns)

    if not docs:
        warnings.append(
            "东方财富接口暂时不可用（可能为反爬拦截），且未注入 web_fetch 兜底，返回空结果"
        )
    return docs, warnings
