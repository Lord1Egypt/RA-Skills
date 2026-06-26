#!/usr/bin/env python3
"""
Stock Price Query Script
查询 A 股（沪深）、港股、美股的实时行情数据。
使用腾讯财经公开 HTTP 接口 (qt.gtimg.cn) 获取数据，直接调用，无需任何配置。
支持单只查询和批量查询（逗号分隔多只股票）。

用法:
    python3 stock_query.py <stock_code> [market]
    python3 stock_query.py <code1,code2,code3>

参数:
    stock_code: 股票代码，如 600519, AAPL, 00700；批量查询用逗号分隔
    market:     可选，市场标识 (sh/sz/hk/us)，批量查询时不适用（自动识别）

示例:
    python3 stock_query.py 600519
    python3 stock_query.py 600519 sh
    python3 stock_query.py AAPL us
    python3 stock_query.py 00700 hk
    python3 stock_query.py 600519,00700,AAPL
"""

import sys
import json
import re
import time
import urllib.request
import urllib.error

VERSION = "1.1.4"

# 输入校验正则：股票代码允许字母、数字和前导点号（美股指数如 .IXIC），最长 10 字符
VALID_CODE_PATTERN = re.compile(r'^\.?[A-Za-z0-9]{1,10}$')
# 市场标识白名单
VALID_MARKETS = {"sh", "sz", "hk", "us"}

# 港股指数代码集合（纯字母但属于港股，需特殊处理避免误判为美股）
HK_INDEX_CODES = {"HSI", "HSCEI", "HSTECH", "HSCCI", "HSCEI"}
# 美股指数代码集合（以 . 开头）
US_INDEX_CODES = {".IXIC", ".DJI", ".INX"}


def validate_input(code: str, market: str | None) -> str | None:
    """校验输入参数，防止注入攻击。返回 None 表示合法，否则返回错误信息。"""
    if not VALID_CODE_PATTERN.match(code):
        return (
            f"非法的股票代码 '{code}'。"
            "股票代码仅允许字母和数字，长度 1-10 位。"
        )
    if market is not None and market not in VALID_MARKETS:
        return (
            f"非法的市场标识 '{market}'。"
            f"仅支持: {', '.join(sorted(VALID_MARKETS))}。"
        )
    return None


def detect_market(code: str) -> str:
    """根据股票代码自动识别市场"""
    code = code.strip().upper()

    # 已带市场前缀
    if code.startswith("SH"):
        return "sh"
    if code.startswith("SZ"):
        return "sz"
    if code.startswith("HK"):
        return "hk"

    # 美股指数（以 . 开头，如 .IXIC .DJI .INX）
    if code.startswith("."):
        return "us"

    # 港股指数（纯字母但属于港股，如 HSI HSCEI）
    if code in HK_INDEX_CODES:
        return "hk"

    # 纯英文字母 -> 美股
    if re.match(r'^[A-Z]{1,5}$', code):
        return "us"

    # 纯数字判断
    digits = re.sub(r'[^0-9]', '', code)
    if len(digits) == 6:
        if digits.startswith('6'):
            return "sh"
        elif digits.startswith(('0', '3')):
            return "sz"
        else:
            return "sh"
    elif 1 <= len(digits) <= 5:
        return "hk"

    return "unknown"


def clean_code(code: str) -> str:
    """清理股票代码，去除市场前缀"""
    code = code.strip().upper()
    for prefix in ["SH", "SZ", "HK"]:
        if code.startswith(prefix):
            return code[len(prefix):]
    return code


def build_tencent_symbol(code: str, market: str) -> str:
    """构建腾讯财经 API 的股票符号"""
    code = clean_code(code)
    if market == "sh":
        return f"sh{code}"
    elif market == "sz":
        return f"sz{code}"
    elif market == "hk":
        # 港股指数（纯字母如 HSI、HSCEI）不需要补零
        if code.upper() in HK_INDEX_CODES:
            return f"hk{code.upper()}"
        return f"hk{code.zfill(5)}"
    elif market == "us":
        return f"us{code.upper()}"
    return code


def parse_stock(raw: str, code: str, market: str) -> dict:
    """解析腾讯财经 API 返回的行情数据（各市场格式统一）

    通用字段索引:
    [1]:  名称
    [2]:  代码
    [3]:  当前价格
    [4]:  昨收
    [5]:  今开
    [6]:  成交量（手/股）
    [30]: 时间
    [31]: 涨跌额
    [32]: 涨跌幅(%)
    [33]: 最高
    [34]: 最低
    [37]: 成交额
    """
    parts = raw.split("~")
    if len(parts) < 35:
        return {"status": "error", "message": "数据解析失败，返回数据不完整"}

    name = parts[1].strip()
    if not name:
        return {
            "status": "error",
            "message": f"未找到股票 {clean_code(code)}，请检查代码是否正确",
        }

    current_price = float(parts[3]) if parts[3] else 0
    prev_close = float(parts[4]) if parts[4] else 0
    open_price = float(parts[5]) if parts[5] else 0
    volume_raw = parts[6].strip() if parts[6] else "0"
    volume = int(float(volume_raw))

    time_str = parts[30].strip() if len(parts) > 30 and parts[30] else ""
    change = float(parts[31]) if len(parts) > 31 and parts[31] else 0
    change_pct = float(parts[32]) if len(parts) > 32 and parts[32] else 0
    high = float(parts[33]) if len(parts) > 33 and parts[33] else 0
    low = float(parts[34]) if len(parts) > 34 and parts[34] else 0
    amount_raw = parts[37].strip() if len(parts) > 37 and parts[37] else "0"
    amount = float(amount_raw) if amount_raw else 0

    # A 股成交量单位为手（1 手 = 100 股），成交额单位为万元
    if market in ("sh", "sz"):
        volume = volume * 100
        amount = amount * 10000

    display_code = clean_code(code)
    if market == "hk":
        # 港股指数不补零
        if display_code.upper() not in HK_INDEX_CODES:
            display_code = display_code.zfill(5)
        else:
            display_code = display_code.upper()
    elif market == "us":
        display_code = display_code.upper()

    # 扩展字段：市盈率 [39]、总市值 [45]（部分市场可用）
    pe_ratio = None
    market_cap = None
    if len(parts) > 39 and parts[39].strip():
        try:
            pe_ratio = round(float(parts[39]), 2)
        except (ValueError, IndexError):
            pass
    if len(parts) > 45 and parts[45].strip():
        try:
            market_cap = round(float(parts[45]), 2)
        except (ValueError, IndexError):
            pass

    result = {
        "code": display_code,
        "name": name,
        "market": market,
        "current_price": current_price,
        "change": change,
        "change_percent": change_pct,
        "open": open_price,
        "high": high,
        "low": low,
        "prev_close": prev_close,
        "volume": volume,
        "amount": amount,
        "time": time_str,
        "status": "success",
    }
    if pe_ratio is not None:
        result["pe_ratio"] = pe_ratio
    if market_cap is not None:
        result["market_cap"] = market_cap
    return result


def fetch_stock(code: str, market: str, retry: bool = True) -> dict:
    """获取股票实时行情"""
    symbol = build_tencent_symbol(code, market)
    url = f"https://qt.gtimg.cn/q={symbol}"

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw = resp.read().decode("gbk", errors="ignore")

        # 检查返回数据是否为空
        if '=""' in raw or not raw.strip():
            return {
                "status": "error",
                "message": f"未找到股票 {clean_code(code)}，请检查代码是否正确",
            }

        return parse_stock(raw, code, market)

    except urllib.error.HTTPError as e:
        if e.code == 429 and retry:
            time.sleep(1)
            return fetch_stock(code, market, retry=False)
        return {"status": "error", "message": f"HTTP 请求失败: {e.code} {e.reason}"}
    except urllib.error.URLError as e:
        return {"status": "error", "message": f"网络请求失败: {str(e.reason)}"}
    except Exception as e:
        return {"status": "error", "message": f"查询异常: {str(e)}"}


def fetch_batch(codes: list[str]) -> list[dict]:
    """批量获取多只股票的实时行情（单次 HTTP 请求）"""
    # 为每只股票识别市场并构建符号
    code_market_pairs = []
    symbol_list = []
    for code in codes:
        market = detect_market(code)
        code_market_pairs.append((code, market))
        if market != "unknown":
            symbol_list.append(build_tencent_symbol(code, market))
        else:
            symbol_list.append(None)

    # 过滤有效符号，构建批量请求 URL
    valid_symbols = [s for s in symbol_list if s is not None]
    if not valid_symbols:
        return [
            {
                "status": "error",
                "code": c,
                "message": "无法识别该股票代码，请确认后重试。"
                           "支持 A 股（6 位数字）、港股（5 位数字）、美股（英文字母）。",
            }
            for c, _ in code_market_pairs
        ]

    url = f"https://qt.gtimg.cn/q={','.join(valid_symbols)}"

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read().decode("gbk", errors="ignore")
    except urllib.error.HTTPError as e:
        return [{"status": "error", "message": f"HTTP 请求失败: {e.code} {e.reason}"}]
    except urllib.error.URLError as e:
        return [{"status": "error", "message": f"网络请求失败: {str(e.reason)}"}]
    except Exception as e:
        return [{"status": "error", "message": f"查询异常: {str(e)}"}]

    # 解析响应：按 v_<symbol>="data" 格式提取每只股票的数据
    # 响应格式: v_sh600519="1~贵州茅台~..."; v_usAAPL="200~苹果~...";
    response_map = {}
    for match in re.finditer(r'v_([a-zA-Z0-9.]+)="([^"]*)"', raw):
        resp_symbol = match.group(1)
        resp_data = match.group(2)
        response_map[resp_symbol.lower()] = resp_data

    # 按原始输入顺序，用 symbol 从 response_map 中取对应数据
    results = []
    for i, (code, market) in enumerate(code_market_pairs):
        if market == "unknown":
            results.append({
                "status": "error",
                "code": clean_code(code),
                "message": f"无法识别股票代码 {code}，请确认后重试。",
            })
            continue

        symbol = symbol_list[i]
        resp_data = response_map.get(symbol.lower()) if symbol else None

        if resp_data is None or not resp_data.strip():
            results.append({
                "status": "error",
                "code": clean_code(code),
                "message": f"未找到股票 {clean_code(code)}，请检查代码是否正确",
            })
        else:
            results.append(parse_stock(resp_data, code, market))

    return results


def main():
    if len(sys.argv) >= 2 and sys.argv[1] in ("--version", "-V"):
        print(f"stock_query.py {VERSION}")
        sys.exit(0)

    if len(sys.argv) < 2:
        print(json.dumps(
            {"status": "error", "message": "用法: python3 stock_query.py <stock_code> [market]\n"
                                           "批量: python3 stock_query.py <code1,code2,code3>"},
            ensure_ascii=False,
        ))
        sys.exit(1)

    raw_input = sys.argv[1].strip()

    # 判断是否为批量查询（包含逗号）
    if "," in raw_input:
        codes = [c.strip() for c in raw_input.split(",") if c.strip()]
        if len(codes) > 20:
            print(json.dumps(
                {"status": "error", "message": "批量查询最多支持 20 只股票"},
                ensure_ascii=False,
            ))
            sys.exit(1)

        # 逐个校验每个代码
        for c in codes:
            validation_error = validate_input(c, None)
            if validation_error:
                print(json.dumps(
                    {"status": "error", "message": f"股票代码 '{c}' 校验失败: {validation_error}"},
                    ensure_ascii=False,
                ))
                sys.exit(1)

        results = fetch_batch(codes)
        print(json.dumps(results, ensure_ascii=False, indent=2))

        # 如果全部失败则退出码 1
        if all(r.get("status") != "success" for r in results):
            sys.exit(1)
    else:
        # 单只查询（保持原有逻辑）
        code = raw_input
        market = sys.argv[2].strip().lower() if len(sys.argv) > 2 else None

        # 输入安全校验：仅允许字母、数字和白名单市场标识
        validation_error = validate_input(code, market)
        if validation_error:
            print(json.dumps(
                {"status": "error", "message": validation_error},
                ensure_ascii=False,
            ))
            sys.exit(1)

        if not market:
            market = detect_market(code)

        if market == "unknown":
            print(json.dumps(
                {
                    "status": "error",
                    "message": "无法识别该股票代码，请确认后重试。"
                               "支持 A 股（6 位数字）、港股（5 位数字）、美股（英文字母）。",
                },
                ensure_ascii=False,
            ))
            sys.exit(1)

        result = fetch_stock(code, market)
        print(json.dumps(result, ensure_ascii=False, indent=2))

        if result.get("status") != "success":
            sys.exit(1)


if __name__ == "__main__":
    main()
