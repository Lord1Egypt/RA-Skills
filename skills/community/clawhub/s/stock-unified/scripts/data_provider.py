#!/usr/bin/env python3
"""
data_provider — UnifiedStock 适配层
为 risk_watch.py 提供 dp 对象（market_index, sector_top, realtime）
"""
import os, sys, json, subprocess, re

SCRIPT = os.path.join(os.path.dirname(__file__), "unified_stock.py")

def _run(*args):
    """调用 unified_stock.py CLI 并解析 JSON 输出"""
    try:
        cmd = [sys.executable, SCRIPT] + list(args) + ["--json"]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        out = r.stdout.strip()
        # 尝试提取首个 { } JSON 块
        m = re.search(r"\{.*\}", out, re.DOTALL)
        if m:
            return json.loads(m.group())
        # fallback: 尝试解析整段输出
        for line in out.splitlines():
            line = line.strip()
            if line.startswith("{"):
                return json.loads(line)
        return {"error": f"parse fail: {out[:200]}"}
    except Exception as e:
        return {"error": str(e)}

class DataProvider:
    def market_index(self):
        """大盘行情 → {change_pct, price}"""
        data = _run("--market-index")
        if "error" in data:
            # 尝试从实时行情拿上证指数
            sh = _run("--realtime", "000001")
            if isinstance(sh, dict) and "000001" in sh:
                q = sh["000001"]
                return {"price": q.get("price", 0), "change_pct": q.get("change_pct", 0)}
            return data
        # unified_stock.py --market-index 可能返回 {sz, sh, cyb}
        for key in ("sh", "上证", "index"):
            if key in data:
                return data[key]
        # 整体返回
        return data

    def sector_top(self, n=5):
        """板块排行 → {industry: [{change_pct, name, ...}]}"""
        data = _run("--sector-top", str(n))
        if isinstance(data, list):
            return {"industry": data}
        if isinstance(data, dict):
            # 可能已经有 industry key
            if "industry" in data or "list" in data:
                return data
            return {"industry": [data]}
        return {"industry": [], "error": "no data"}

    def realtime(self, codes):
        """批量实时行情 → {code: {price, change_pct, ...}}"""
        if not codes:
            return {}
        # 支持单个字符串或列表
        if isinstance(codes, str):
            codes = [codes]
        data = _run("--realtime", ",".join(codes))
        if "error" in data:
            return {}
        # 确保返回 dict of dict
        if isinstance(data, dict):
            return data
        return {}

dp = DataProvider()
