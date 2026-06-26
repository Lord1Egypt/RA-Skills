"""全量A股股票列表 — 多重策略 + 内置兜底"""

from typing import List, Tuple


# 已知A股代码范围
_CODE_RANGES = [
    ("600", 0, 999, "上海主板"),     # 600000-600999
    ("601", 0, 999, "上海主板"),     # 601000-601999
    ("603", 0, 999, "上海主板"),     # 603000-603999
    ("605", 0, 999, "上海主板"),     # 605000-605999
    ("688", 0, 999, "科创板"),       # 688000-688999
    ("000", 0, 999, "深圳主板"),     # 000000-000999
    ("001", 0, 999, "深圳主板"),     # 001000-001999
    ("002", 0, 999, "中小板"),       # 002000-002999
    ("003", 0, 999, "深圳"),         # 003000-003999
    ("300", 0, 999, "创业板"),       # 300000-300999
    ("301", 0, 999, "创业板"),       # 301000-301999
]


def generate_all_codes() -> List[str]:
    """生成所有可能的A股代码（约16000个）"""
    codes = []
    for prefix, start, end, _ in _CODE_RANGES:
        for i in range(start, end + 1):
            code = prefix + str(i).zfill(3)
            codes.append(code)
    return codes


def validate_via_sina(codes_batch: List[str]) -> List[Tuple[str, str]]:
    """通过Sina API验证哪些代码真实存在，并获取名称"""
    import requests
    headers = {"Referer": "http://finance.sina.com.cn"}
    valid = []

    # 分段查询
    for i in range(0, len(codes_batch), 50):
        batch = codes_batch[i:i + 50]
        sina_codes = ",".join(
            f"sh{c}" if c[:3] in ("600","601","603","605","688","689") else f"sz{c}"
            for c in batch
        )
        try:
            resp = requests.get(f"http://hq.sinajs.cn/list={sina_codes}",
                               headers=headers, timeout=10)
            resp.encoding = "gbk"
            for line in resp.text.strip().split("\n"):
                if "hq_str_" not in line:
                    continue
                parts = line.split('="')
                if len(parts) < 2:
                    continue
                data_str = parts[1].rstrip('";')
                fields = data_str.split(",")
                if len(fields) < 3 or not fields[0]:
                    continue
                var_name = parts[0].replace("var hq_str_", "").strip()
                code = var_name.replace("sh", "").replace("sz", "")
                name = fields[0]
                close = fields[3] if len(fields) > 3 else "0"
                if close and float(close) > 0:
                    valid.append((code, name))
        except Exception:
            pass

    return valid


def build_stock_list(save_path: str = None) -> List[Tuple[str, str]]:
    """
    构建并缓存A股全量股票列表

    策略:
    1. 尝试baostock（最快）
    2. 失败则通过Sina API遍历已知代码范围验证
    3. 最终落盘为CSV缓存
    """
    import os
    import json

    # 尝试从缓存加载
    if save_path and os.path.exists(save_path):
        try:
            with open(save_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    # Strategy 1: baostock
    try:
        import baostock as bs
        from datetime import date, timedelta
        bs.login()
        ref_date = (date.today() - timedelta(days=2)).strftime("%Y-%m-%d")
        rs = bs.query_all_stock(ref_date)
        stocks = []
        while rs.next():
            stocks.append(rs.get_row_data())
        bs.logout()

        result = []
        for s in stocks:
            code = s[0].lower()
            if not (code.startswith("sh.6") or code.startswith("sz.0") or code.startswith("sz.3")):
                continue
            if s[1] != "1":
                continue
            result.append((s[0].replace("sh.", "").replace("sz.", ""), s[2]))

        if result:
            print(f"[StockList] baostock: {len(result)} stocks")
            if save_path:
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                with open(save_path, "w", encoding="utf-8") as f:
                    json.dump(result, f, ensure_ascii=False)
            return result
    except Exception as e:
        print(f"[StockList] baostock failed: {e}")

    # Strategy 2: Sina API probe (generate all codes and validate)
    print("[StockList] Generating code ranges...")
    all_codes = generate_all_codes()
    # Only probe 000xxx-003xxx, 600xxx-605xxx, 002xxx, 300xxx for speed
    probe_codes = (
        [c for c in all_codes if c.startswith(("600","601","603"))][:3000] +
        [c for c in all_codes if c.startswith(("000","001","002","003"))][:3000] +
        [c for c in all_codes if c.startswith(("300","301"))][:2000] +
        [c for c in all_codes if c.startswith(("605","688"))][:1000]
    )

    # Deduplicate
    probe_codes = list(dict.fromkeys(probe_codes))

    print(f"[StockList] Probing {len(probe_codes)} codes via Sina...")
    result = validate_via_sina(probe_codes)
    print(f"[StockList] Sina probe: {len(result)} valid stocks")

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False)

    return result
