#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票估值查询脚本
用法: python3 query_valuation.py <股票代码>
示例: python3 query_valuation.py 600519.SH
      python3 query_valuation.py 00700.HK
      python3 query_valuation.py 000001.SZ
"""

import sys
import json
import os
import re
import urllib.request
import urllib.error

# ─── 配置 ────────────────────────────────────────────────────────────────────

API_URL = "https://tz.smxqx.tech/api/stock/valuation/detail"
API_VERSION = "2.5"
# 优先从环境变量读取，fallback 到内置公共 Token
AUTH_TOKEN = os.environ.get(
    "STOCK_VALUATION_AUTH",
    "b0a590b5-6371-4665-b041-0b97cc553f6d"
)

TIMEOUT = 20  # 秒

# 估值标签图标
TAG_ICONS = {
    "低估": "🟢",
    "适中": "🟡",
    "合理": "🟡",
    "高估": "🔴",
}

# 估值方法类型映射
METHOD_NAME_MAP = {
    "pe":   "市盈率估值",
    "pb":   "市净率估值",
    "ps":   "市销率估值",
    "peg":  "PEG 估值",
    "fcff": "自由现金流折现",
    "sv":   "股东价值折现",
}

# 交易所名称映射
EXCHANGE_MAP = {
    "SSE":  "上交所（沪市）",
    "SZSE": "深交所（深市）",
    "HKEX": "港交所（港股）",
    "HK":   "港交所（港股）",
    "HKSE": "港交所（港股）",
}

# ─── 工具函数 ─────────────────────────────────────────────────────────────────

def validate_code(code: str) -> bool:
    """验证股票代码格式：{数字}.{SH|SZ|HK}"""
    pattern = r"^\d{3,6}\.(SH|SZ|HK)$"
    return bool(re.match(pattern, code.strip().upper()))


def normalize_code(code: str) -> str:
    """
    规范化股票代码：
    - 港股（.HK）左补零到 5 位（接口要求 00700.HK 格式）
    - A 股（.SH/.SZ）左补零到 6 位
    """
    code = code.strip().upper()
    if "." not in code:
        return code
    symbol, market = code.rsplit(".", 1)
    if market == "HK":
        symbol = symbol.zfill(5)
    else:
        symbol = symbol.zfill(6)
    return f"{symbol}.{market}"


def fmt_num(value, decimal: int = 2, suffix: str = "") -> str:
    """格式化数字，处理 None / 空字符串 / 字符串类型"""
    if value is None or str(value).strip() == "":
        return "—"
    try:
        n = float(str(value).replace(",", ""))
        return f"{n:,.{decimal}f}{suffix}"
    except (ValueError, TypeError):
        return str(value)


def fmt_change(value) -> str:
    """为涨跌幅字符串添加图标"""
    if not value or value == "—":
        return str(value)
    s = str(value).strip().lstrip("+")
    try:
        n = float(s.rstrip("%"))
        if n > 0:
            return f"📈 +{s}" if not s.startswith("+") else f"📈 {s}"
        elif n < 0:
            return f"📉 {s}"
        else:
            return f"➡️  {s}"
    except ValueError:
        return s


def strip_html(text: str) -> str:
    """去除简单 HTML 标签（如 <i>）"""
    if not text:
        return ""
    return re.sub(r"<[^>]+>", "", text)

# ─── 接口调用 ─────────────────────────────────────────────────────────────────

def query_valuation(code: str) -> dict:
    """POST 请求估值接口，返回解析后的 JSON"""
    payload = json.dumps({"code": code.upper()}).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "v": API_VERSION,
        "auth": AUTH_TOKEN,
    }
    req = urllib.request.Request(
        API_URL,
        data=payload,
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        return {"_error": f"HTTP {e.code}: {e.reason}", "_detail": body}
    except urllib.error.URLError as e:
        return {"_error": f"网络错误: {e.reason}"}
    except json.JSONDecodeError:
        return {"_error": "接口返回数据格式异常，无法解析"}
    except Exception as e:
        return {"_error": f"未知错误: {e}"}


def extract_data(result: dict):
    """从接口响应中提取 data 字段，失败时返回 None 和错误信息"""
    if "_error" in result:
        return None, result["_error"]

    # 标准格式：{ code: 0, data: {...} }
    if "data" in result and isinstance(result["data"], dict):
        api_code = result.get("code")
        if api_code not in (0, "0", 200, "200", None):
            msg = result.get("msg") or result.get("message") or f"接口返回错误码 {api_code}"
            return None, msg
        return result["data"], None

    # 直接返回数据字段（无外层包装）
    if "name" in result and "price" in result:
        return result, None

    msg = result.get("msg") or result.get("message") or json.dumps(result, ensure_ascii=False)[:200]
    return None, msg

# ─── 渲染报告 ─────────────────────────────────────────────────────────────────

def render_report(data: dict) -> str:
    lines = []

    # ── 股票基本信息 ────────────────────────────────────────────
    code        = data.get("code", "—")
    name        = data.get("name", "未知")
    exchange    = EXCHANGE_MAP.get(data.get("exchange", ""), data.get("exchange", "—"))
    industry    = data.get("industry", "—")
    trade_date  = data.get("trade_date", "—")
    currency    = "HK$" if code.upper().endswith(".HK") else "¥"

    lines.append(f"## 📊 {name}（{code}）")
    lines.append(f"> 交易所：{exchange}　｜　行业：{industry}　｜　数据时间：{trade_date}")
    lines.append("")

    # ── 行情概览 ────────────────────────────────────────────────
    price        = fmt_num(data.get("price"), 2)
    daily_chg    = fmt_change(data.get("daily_price_change"))
    yearly_chg   = fmt_change(data.get("yearly_price_change"))
    total_mv     = fmt_num(data.get("total_mv"), 2, " 亿元")
    total_share  = fmt_num(data.get("total_share"), 2, " 亿股")

    lines.append("### 💰 行情概览")
    lines.append("| 项目 | 数值 |")
    lines.append("|------|------|")
    lines.append(f"| 当前股价 | {currency}{price} |")
    lines.append(f"| 日涨跌幅 | {daily_chg} |")
    lines.append(f"| 年初至今 | {yearly_chg} |")
    lines.append(f"| 当前市值 | {total_mv} |")
    lines.append(f"| 总股本   | {total_share} |")
    lines.append("")

    # ── 估值指标 ────────────────────────────────────────────────
    pe_ttm  = fmt_num(data.get("pe_ttm"), 2)
    pb      = fmt_num(data.get("pb"), 2)
    ps_ttm  = fmt_num(data.get("ps_ttm"), 2)
    dv      = data.get("dv_ratio", "—") or "—"

    lines.append("### 📐 当前估值指标")
    lines.append("| 指标 | 数值 |")
    lines.append("|------|------|")
    lines.append(f"| 市盈率 PE（TTM） | {pe_ttm} |")
    lines.append(f"| 市净率 PB        | {pb} |")
    lines.append(f"| 市销率 PS（TTM） | {ps_ttm} |")
    lines.append(f"| 股息率           | {dv} |")
    lines.append("")

    # ── 综合估值结论（来自 sum 对象） ──────────────────────────
    sum_obj = data.get("sum") or {}
    if isinstance(sum_obj, dict) and sum_obj:
        sum_p   = fmt_num(sum_obj.get("sum_p"), 2)
        sum_v   = fmt_num(sum_obj.get("sum_v"), 2, " 亿元")
        margin  = sum_obj.get("margin", "—") or "—"
        tag     = sum_obj.get("tag", "—") or "—"
        tag_icon = TAG_ICONS.get(tag, "⚪")
        sum_desc = strip_html(sum_obj.get("desc", ""))

        lines.append("### 🎯 综合估值判断")
        lines.append(f"**结论：{tag_icon} {tag}**")
        lines.append("")
        lines.append("| 项目 | 数值 |")
        lines.append("|------|------|")
        lines.append(f"| 合理股价 | {currency}{sum_p} |")
        lines.append(f"| 合理市值 | {sum_v} |")
        lines.append(f"| 安全边际 | {margin} |")
        lines.append("")

        if sum_desc:
            lines.append(f"> {sum_desc}")
            lines.append("")

        # ── 各估值方法汇总（sum.list） ────────────────────────
        method_list = sum_obj.get("list", [])
        if method_list:
            lines.append("### 📋 各估值方法明细")
            lines.append("| 估值方法 | 合理股价 | 合理市值 | 参与综合 |")
            lines.append("|----------|----------|----------|----------|")
            for item in method_list:
                m_type    = item.get("type", "")
                m_name    = item.get("name") or METHOD_NAME_MAP.get(m_type, m_type)
                m_price   = fmt_num(item.get("price"), 2)
                m_value   = fmt_num(item.get("value"), 2, " 亿")
                m_apply   = "✅ 是" if item.get("apply", True) else "⛔ 否"
                lines.append(f"| {m_name} | {currency}{m_price} | {m_value} | {m_apply} |")
            lines.append("")

    # ── PE 分位信息（如有） ─────────────────────────────────────
    pe_pct = data.get("pe_ttm_pct") or {}
    if isinstance(pe_pct, dict) and pe_pct.get("desc"):
        lines.append("### 📈 PE 历史分位")
        lines.append(strip_html(pe_pct.get("desc", "")))
        lines.append("")

    # ── PB 分位信息（如有） ─────────────────────────────────────
    pb_pct = data.get("pb_pct") or {}
    if isinstance(pb_pct, dict) and pb_pct.get("desc"):
        lines.append("### 📈 PB 历史分位")
        lines.append(strip_html(pb_pct.get("desc", "")))
        lines.append("")

    # ── 免责声明 ────────────────────────────────────────────────
    lines.append("---")
    lines.append("> ⚠️ **免责声明**：以上数据仅供参考，不构成任何投资建议。投资有风险，决策需谨慎。")

    return "\n".join(lines)

# ─── 主函数 ──────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("❌ 错误：请提供股票代码", file=sys.stderr)
        print("", file=sys.stderr)
        print("用法: python3 query_valuation.py <股票代码>", file=sys.stderr)
        print("示例:", file=sys.stderr)
        print("  python3 query_valuation.py 600519.SH   # 贵州茅台", file=sys.stderr)
        print("  python3 query_valuation.py 00700.HK    # 腾讯控股", file=sys.stderr)
        print("  python3 query_valuation.py 000001.SZ   # 平安银行", file=sys.stderr)
        sys.exit(1)

    code = sys.argv[1].strip().upper()

    # 格式校验
    if not validate_code(code):
        print(f"❌ 股票代码格式不正确：{code}", file=sys.stderr)
        print("", file=sys.stderr)
        print("正确格式：", file=sys.stderr)
        print("  沪市 A 股：600519.SH（贵州茅台）", file=sys.stderr)
        print("  深市 A 股：000001.SZ（平安银行）", file=sys.stderr)
        print("  港    股：00700.HK （腾讯控股）", file=sys.stderr)
        sys.exit(1)

    # 规范化代码（自动补零）
    code = normalize_code(code)

    # 查询
    result = query_valuation(code)
    data, err = extract_data(result)

    if err:
        print(f"❌ 查询失败：{err}", file=sys.stderr)
        sys.exit(1)

    # 输出报告
    print(render_report(data))


if __name__ == "__main__":
    main()
