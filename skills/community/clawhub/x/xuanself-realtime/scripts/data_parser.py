"""
data_parser.py — xuanself-realtime v3.0
数据解析核心模块（实战验证版）

经验：2026-04-09 调试发现 SerpAPI 采集的 JSON 中 market 字段是
Python repr 格式（单引号 dict），json.loads() 直接失败。
解决：先用 json.loads()，失败则用 ast.literal_eval() 兜底。

使用示例：
    from data_parser import smart_json, smart_list, smart_dict, SmartData, fu, clean_bom

    raw = json.load(open("xuanself_raw.json"))
    data = SmartData(raw)
    ecom = data.ecommerce()
    market = data.market()
"""

import ast, json, os


def smart_json(s):
    """智能解析：优先 JSON，兜底 ast.literal_eval（处理单引号 Python repr）"""
    if not s or str(s).strip() in ("None", "[]", "{}"):
        return None
    try:
        return json.loads(s)
    except Exception:
        pass
    try:
        return ast.literal_eval(s)
    except Exception:
        return None


def smart_list(s):
    """安全返回 list"""
    if not s:
        return []
    r = smart_json(s)
    return r if isinstance(r, list) else []


def smart_dict(s):
    """安全返回 dict"""
    if not s:
        return {}
    r = smart_json(s)
    return r if isinstance(r, dict) else {}


def clean_bom(fp):
    """清理 UTF-8-BOM（write_to_file 工具写入的文件带 BOM）"""
    if not os.path.exists(fp):
        return
    with open(fp, "rb") as f:
        raw = f.read()
    if raw.startswith(b"\xef\xbb\xbf"):
        with open(fp, "wb") as f:
            f.write(raw[3:])


def fu(v):
    """格式化美元金额：$113.6M / $250.0M / $1.2B"""
    if not v and v != 0:
        return "N/A"
    try:
        v = float(v)
    except (ValueError, TypeError):
        return "N/A"
    if v >= 1e9:
        return "${:.1f}B".format(v / 1e9)
    if v >= 1e6:
        return "${:.1f}M".format(v / 1e6)
    if v >= 1e3:
        return "${:.0f}K".format(v / 1e3)
    return "${:,.0f}".format(v)


def normalize(text):
    """清洗文本中的管道符和多余换行"""
    if not text:
        return ""
    return str(text).replace("|", " ").replace("\n", " ").strip()


class SmartData:
    """数据容器，自动解析 raw JSON"""

    def __init__(self, raw: dict):
        self._raw = raw or {}

    def _g(self, key):
        return self._raw.get(key)

    def ecommerce(self) -> list:
        return smart_list(self._g("ecommerce"))

    def market(self) -> dict:
        return smart_dict(self._g("market"))

    def vk(self) -> list:
        return smart_list(self._g("vk"))

    def telegram(self) -> list:
        raw_tg = self._g("telegram")
        if not raw_tg:
            return []
        d = smart_json(raw_tg) if isinstance(raw_tg, str) else raw_tg
        if isinstance(d, dict):
            return d.get("google_site_results", [])
        return d if isinstance(d, list) else []

    def news(self) -> list:
        return smart_list(self._g("news"))

    def tender(self) -> list:
        return smart_list(self._g("tender"))

    def competitor(self) -> list:
        return smart_list(self._g("competitor"))

    def pricing(self) -> list:
        return smart_list(self._g("pricing"))

    def insurance(self) -> list:
        return smart_list(self._g("insurance"))

    def registration(self) -> list:
        return smart_list(self._g("registration"))

    def medical_research(self) -> list:
        return smart_list(self._g("medical_research"))

    def channel(self) -> list:
        return smart_list(self._g("channel"))

    def import_substitution(self) -> list:
        return smart_list(self._g("import_substitution"))

    def raw(self) -> dict:
        """返回原始 dict"""
        return self._raw
