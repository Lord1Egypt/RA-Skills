"""
tencentmap-map-assistant-skill · 客户端

封装腾讯位置服务 C 端能力：
- 旅游攻略 travel_guide → 含小程序入口图（二维码）
- 地点搜索 / POI 详情 / 周边 / 路线 → 数据
- 地址坐标互转 / 输入补全 / IP 定位 / 行政区划 / 距离矩阵 → 数据

key 策略：
- 检测顺序：用户传入参数 → ~/.tencentmap/tempkey.json
- 当前 key 遇错误时自动按候选池优先级轮询切换下一个
- 所有 key 均失败时抛出 TmapError，列出每个 key 的失败原因
- 若候选池为空 → 抛出异常，由 AI 引导用户通过 tempkey 流程申请临时 Key
"""

import os
import json
import time
import base64
import hashlib
import hmac
import random
import string
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import requests


# ============================================================
# 常量
# ============================================================

# 创建指南/二维码网关签名密钥
_SIGN_SECRET = "cd0da99c92037580fc272060da23d384"

# 运营固定 user_id（攻略入库使用）
_OPERATION_USER_ID = "50000000002"

# 服务端点
_WS_BASE = "https://apis.map.qq.com"           # 正式 key 通道
_A2A_URL = "https://h5gw.map.qq.com/aichat/v1/a2a"   # AI 旅游攻略 A2A（服务端 AI 服务，独立通道）
# 旅游攻略保存并出二维码（保存+出码合一接口，正式公网域名）
_TG_SAVE_QR_URL = "https://h5gw.map.qq.com/travelguide/saveandgenqrcode"

# 小程序原始 ID
_MINI_PROGRAM_USERNAME = "gh_ff25a9b4394d"

# 请求超时
_TIMEOUT = 60
_A2A_TIMEOUT = 300  # SSE 长连接

# 地点搜索/输入提示富信息字段（评分、人均、营业时间）
_RICH_ADDED_FIELDS = "star_level,avg_price,opening_hours"

# ============================================================
# 语义化改写 — 辅助函数
# ============================================================

def _fmt_distance(meters: float) -> str:
    """距离格式化：>=1000米 → 约X.X公里，否则 X米"""
    m = float(meters)
    if m >= 1000:
        return f"约{m/1000:.1f}公里"
    return f"{m:.0f}米"


def _fmt_duration(minutes: float) -> str:
    """时长格式化：>=60分钟 → X小时X分钟，否则 X分钟"""
    m = int(minutes)
    if m >= 60:
        h, r = divmod(m, 60)
        return f"{h}小时{r}分钟" if r else f"{h}小时"
    return f"{m}分钟"


def _safe_get(d: Dict[str, Any], *keys, default=""):
    """安全取值链：_safe_get(obj, 'a', 'b', 'c') → obj[a][b][c] or default"""
    for k in keys:
        if not isinstance(d, dict):
            return default
        d = d.get(k, default if k == keys[-1] else {})
    return d


def _fmt_wind(wind_power: str) -> str:
    """风力格式化：已含"级"或特殊值（微风）直接返回，否则补"级" """
    if not wind_power:
        return ""
    if wind_power in ("微风", "无风") or wind_power.endswith("级"):
        return wind_power
    return f"{wind_power}级"


def _fmt_tmap_error(code: int, message: str) -> str:
    """API 报错格式化。详细指引见 references/error-codes.md。"""
    return f"[{code}] {message}"


# ============================================================
# Key 持久化：统一存于 ~/.tencentmap/tempkey.json（唯一 key 源）
# ============================================================

def _collect_tempkeys() -> List[Tuple[str, str]]:
    """从 ~/.tencentmap/tempkey.json 收集所有当前可用的 Key，返回候选列表。

    该文件是唯一的持久化 key 源，位于用户主目录、跨地图 skill 共享、卸载 skill 不丢失。
    结构：{"__manual__": {"key": ...}, "<phone>": {"key": ..., "expire_time": ..., "status": ...}}

    顺序：__manual__（用户手动指定，永久有效）排在最前，其后是申请记录（按文件内出现顺序，
    逐条做expire_time 过期检查）。不做去重与重排序。

    :return: [(key, source), ...] — source 为 "manual" / "tempkey"；无可用 Key 时返回空列表
    """
    candidates: List[Tuple[str, str]] = []
    tempkey_path = os.path.join(os.path.expanduser("~"), ".tencentmap", "tempkey.json")
    if not os.path.exists(tempkey_path):
        return candidates
    try:
        with open(tempkey_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return candidates
        # 1) 手动指定的 key 排最前，永久有效（除非被显式标记 expired）
        manual = data.get("__manual__")
        if isinstance(manual, dict) and manual.get("key") and manual.get("status") != "expired":
            candidates.append((manual["key"], "manual"))
        # 2) 申请记录：以手机号为 key，按 expire_time 做过期检查，逐条追加
        for phone, entry in data.items():
            if phone == "__manual__" or not isinstance(entry, dict):
                continue
            key = entry.get("key")
            expire_str = entry.get("expire_time", "")
            status = entry.get("status", "active")
            if not key or not expire_str or status == "expired":
                continue
            # 检查是否过期（支持 "YYYY-MM-DD HH:MM:SS" 和 "YYYY-MM-DD" 两种格式）
            for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
                try:
                    expire_dt = datetime.strptime(expire_str, fmt)
                    if datetime.now() < expire_dt:
                        candidates.append((key, "tempkey"))
                    break  # 解析成功，无论是否过期都跳到下一条
                except ValueError:
                    continue
    except Exception:
        pass
    return candidates


def _read_legacy_dotenv_key() -> Optional[str]:
    """向后兼容：读取旧版 skill 包内 .env 的 TMAP_KEY，仅用于一次性迁移。

    """
    skill_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_path = os.path.join(skill_root, ".env")
    if not os.path.exists(env_path):
        return None
    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                s = line.strip()
                if s.startswith("TMAP_KEY") and "=" in s:
                    v = s.partition("=")[2].strip().strip('"').strip("'")
                    if v:
                        return v
    except Exception:
        pass
    return None


def _collect_keys(passed_key: Optional[str]) -> List[Tuple[str, str]]:
    """按 用户传入 → tempkey.json 顺序收集全部候选 Key。

    不做去重与重排序，保持来源优先级顺序。

    :return: [(key, source), ...] — source 为 "argument" / "manual" / "tempkey"
             / "migrated"；无任何可用 Key 时返回空列表
    """
    candidates: List[Tuple[str, str]] = []
    if passed_key:
        candidates.append((passed_key, "argument"))
    # tempkey.json 是唯一持久化 key 源（含过期检查）
    candidates.extend(_collect_tempkeys())
    # 向后兼容：以上均无 key 时，旧版 skill 包内 .env 若有 key，一次性迁移进 tempkey.json
    if not candidates:
        legacy_key = _read_legacy_dotenv_key()
        if legacy_key:
            save_key_to_dotenv(legacy_key)
            candidates.append((legacy_key, "migrated"))
    return candidates


def _mask_key(key: str) -> str:
    """Key 掩码：前 8 位 + **** + 后 4 位，用于对外提示时避免明文暴露。

    掩码规则与 tempkey-guide.md 中Key 展示规则一致。
    """
    if not key:
        return ""
    if len(key) <= 12:
        return key[:4] + "****"
    return f"{key[:8]}****{key[-4:]}"



_KEY_SOURCE_LABELS = {
    "argument": "调用时传入",
    "manual": "手动指定",
    "tempkey": "已申请的临时 Key",
    "migrated": "旧版 .env 迁移",
}


def _source_label(source: str) -> str:
    """来源标识→ 面向用户的中文说明。"""
    return _KEY_SOURCE_LABELS.get(source, source)


def save_key_to_dotenv(key: str) -> str:
    """把用户提供的正式 key 持久化为当前生效 Key。

    写入 ~/.tencentmap/tempkey.json 的 "__manual__" 槽位（手动指定，永久有效，
    优先于申请记录）。函数名保留以兼容既有调用。

    :return: tempkey.json 文件绝对路径
    """
    tempkey_path = os.path.join(os.path.expanduser("~"), ".tencentmap", "tempkey.json")
    records = {}
    if os.path.exists(tempkey_path):
        try:
            with open(tempkey_path, "r", encoding="utf-8") as f:
                records = json.load(f)
        except Exception:
            records = {}
    if not isinstance(records, dict):
        records = {}
    records["__manual__"] = {"key": key, "status": "active", "source": "manual"}
    os.makedirs(os.path.dirname(tempkey_path), exist_ok=True)
    with open(tempkey_path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    return tempkey_path


# ============================================================
# TmapClient
# ============================================================

class TmapClient:
    """腾讯位置服务地图助手客户端。

    用法：
        # 1) 客户已配置 tempkey → 直接用
        client = TmapClient()

        # 2) 客户传入 Key → 本次会话优先使用
        client = TmapClient(key="XXX-XXX-XXX-XXX-XXX-XXX")

        # 3) 客户未配置且无 tempkey → 初始化成功但调用时报错，AI 引导 tempkey 流程
        client = TmapClient()

    如需固定使用某个 Key → 调用 save_key_to_dotenv("<key>") 写入 __manual__，之后自动生效。

    Key 候选池：初始化时把各来源的 key 收进 self._key_pool，默认使用第一个。
    调用中若当前 key 不可用，自动按优先级轮询切换下一个 Key，所有 Key 均失败时才抛出 TmapError。
    """

    def __init__(
        self,
        key: Optional[str] = None,
        qrcode_dir: Optional[str] = None,
    ):
        self._key_pool = _collect_keys(key)       # [(key, source), ...] 有序候选池
        self._key_idx = 0                         # 当前使用的候选下标
        if self._key_pool:
            self.key, self.key_source = self._key_pool[0]
        else:
            self.key = None                       # None 表示无可用Key
            self.key_source = "none"              # 'argument'/'manual'/'tempkey'/'migrated'/'none'

        if qrcode_dir is None:
            qrcode_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "qrcodes")
        self.qrcode_dir = qrcode_dir
        os.makedirs(self.qrcode_dir, exist_ok=True)

        # 成品 markdown / json 落盘目录（让 Agent 走文件路径，原样输出）
        self.output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "outputs")
        os.makedirs(self.output_dir, exist_ok=True)

    # ------------------------------------------------------------
    # 私有：底层调用
    # ------------------------------------------------------------

    def _rich_params(self) -> Dict[str, Any]:
        """富信息字段参数（评分 star_level / 人均 avg_price / 营业时间 opening_hours）。"""
        return {"get_rich": 1, "added_fields": _RICH_ADDED_FIELDS}

    def _place_search_get(self, path: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """地点搜索类请求：先带富信息参数，若所有 Key 均因 113（无 get_rich 权限）失败，
        自动去掉 get_rich / added_fields 重试一次，只返回基础字段（名称 / 坐标 / 地址）。
        """
        try:
            return self._ws_get(path, params)
        except TmapError as e:
            if e.code == 113:
                fallback = {k: v for k, v in params.items()
                            if k not in ("get_rich", "added_fields")}
                return self._ws_get(path, fallback)
            raise

    def _ws_get(self, path: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """通用 WebService GET，走 apis.map.qq.com 正式通道。

        按候选池优先级自动轮询 Key：当前 Key 报错时自动切换下一个，
        所有 Key 均不可用时才抛出 TmapError（异常信息中列出每个 Key 的失败原因）。

        113（功能未授权）与其他错误一样走轮询——_place_search_get 仅在所有 Key
        均因 113 失败时才捕获并做同 Key 去富信息降级重试。

        :raises TmapError: 候选池为空、或所有 Key 均调用失败时抛出
        """
        if not self._key_pool:
            raise TmapError(-1,
                "未检测到可用的 API Key。可按 tempkey-guide.md 流程申请 AI 场景临时体验 Key"
                "（手机号验证，1 年有效，5000 次/天），或前往 https://lbs.qq.com 控制台"
                "为账号分配正式额度后重试。",
                path, {})

        params = {k: v for k, v in params.items() if v is not None and v != ""}
        url = f"{_WS_BASE}{path}"

        errors: List[Dict[str, Any]] = []
        for idx, (candidate_key, candidate_source) in enumerate(self._key_pool):
            self._key_idx = idx
            self.key, self.key_source = candidate_key, candidate_source

            try:
                r = requests.get(url, params={**params, "key": candidate_key},
                                 timeout=_TIMEOUT)
                r.raise_for_status()
                data = r.json()
                if data.get("status") == 0:
                    if idx != 0 and errors:
                        failed_info = "；".join(
                            f"{_mask_key(e['key'])}（{_source_label(e['source'])}）→ {e['code']} {e['msg']}"
                            for e in errors
                        )
                        print(f"[TmapClient] 以下 Key 不可用：{failed_info}")
                        print(f"[TmapClient] 已自动切换至 {_mask_key(candidate_key)}"
                              f"（来源：{_source_label(candidate_source)}）")
                    return data

                # 错误记入失败列表，继续轮询下一个 Key
                errors.append({
                    "key": candidate_key,
                    "source": candidate_source,
                    "code": data.get("status"),
                    "msg": data.get("message", "unknown error"),
                })
            except requests.RequestException as e:
                errors.append({
                    "key": candidate_key,
                    "source": candidate_source,
                    "code": -1,
                    "msg": str(e),
                })

        # 所有候选 Key 均已尝试失败
        self.key, self.key_source = None, "none"
        last = errors[-1]
        lines = [f"已依次尝试 {len(errors)} 个 Key，均不可用："]
        for e in errors:
            lines.append(
                f"  · {_mask_key(e['key'])}（来源：{_source_label(e['source'])}）"
                f" → {e['code']} {e['msg']}"
            )
        detail = "\n".join(lines)
        raise TmapError(last["code"], detail, path, {})

    def _sign_headers(self, markdown_b64: str, qimei36: str) -> Dict[str, str]:
        """生成 saveandgenqrcode 接口的 HMAC-SHA256 签名头。

        签名串按字母序拼接（markdown_content 用 base64 原值，不再哈希）：
            markdown_content=<b64>&nonce=<16位>&qimei36=<>&timestamp=<秒>
        X-Sign = HMAC-SHA256(签名串, _SIGN_SECRET)
        """
        timestamp = str(int(time.time()))
        nonce = "".join(random.choices(string.ascii_letters + string.digits, k=16))
        sign_str = (
            f"markdown_content={markdown_b64}"
            f"&nonce={nonce}"
            f"&qimei36={qimei36}"
            f"&timestamp={timestamp}"
        )
        sign = hmac.new(_SIGN_SECRET.encode(), sign_str.encode(), hashlib.sha256).hexdigest()
        return {
            "X-Timestamp": timestamp,
            "X-Nonce": nonce,
            "X-Sign": sign,
            "tmap-userid": _OPERATION_USER_ID,
            "Content-Type": "application/json",
        }

    def _a2a_stream(self, query: str, lat: float, lng: float) -> Dict[str, Any]:
        """A2A 旅游攻略 SSE 长连接，聚合 plan_summary + plan_days。"""
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "message/stream",
            "params": {
                "message": {
                    "role": "user",
                    "parts": [{"kind": "text", "text": query}],
                    "metadata": {
                        "brand": "oppo",
                        "device_id": "skill-" + uuid_hex(16),
                        "latitude": lat,
                        "longitude": lng,
                        "osVersion": "16.1",
                        "theme": "light",
                        "traceId": uuid_hex(16),
                    },
                }
            },
        }
        headers = {
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        }
        url = f"{_A2A_URL}?key=none&apptag=lbs_ai_chat_a2a"
        with requests.post(url, json=payload, headers=headers, stream=True, timeout=_A2A_TIMEOUT) as r:
            r.raise_for_status()
            raw = b""
            for chunk in r.iter_content(chunk_size=None):
                raw += chunk

        # SSE 必须按 \n\n 切事件，不能用 iter_lines
        text = raw.decode("utf-8", errors="replace")
        plan_summary = None
        plan_days: List[Dict[str, Any]] = []
        for blk in text.split("\n\n"):
            if not blk.strip():
                continue
            data_lines = [l[5:].lstrip() for l in blk.split("\n") if l.startswith("data:")]
            if not data_lines:
                continue
            try:
                ev = json.loads("\n".join(data_lines))
            except Exception:
                continue
            res = ev.get("result", {})
            if res.get("kind") != "artifact-update":
                continue
            art = res.get("artifact", {})
            name = art.get("name", "")
            for p in art.get("parts", []):
                if "data" not in p:
                    continue
                if name == "plan_summary":
                    plan_summary = p["data"]
                elif name == "plan_day":
                    plan_days.append(p["data"])

        if plan_summary is None and not plan_days:
            raise TmapError(-1, "A2A 未返回攻略数据，可能是 query 不含明确目的地或服务端限流", "a2a", {})

        return {"plan_summary": plan_summary, "plan_days": plan_days}

    def _build_markdown(self, plan_days: List[Dict[str, Any]], city: str, title: str) -> str:
        """A2A plan_days → 旅游攻略保存接口要求的 markdown 格式。"""
        total_pois = sum(len(d.get("items", [])) for d in plan_days)
        n_days = len(plan_days)

        def link(p: Dict[str, Any], day: int, num: int) -> str:
            name = p["location_name"]
            poi_id = p["poi_uid"]
            lat = int(round(float(p["latitude"]) * 1e6))
            lng = int(round(float(p["longitude"]) * 1e6))
            return f"[{name}](city={city}&day={day}&poi_id={poi_id}&num={num}&lat={lat}&lng={lng}&type=1&source=fix)"

        lines: List[str] = [
            f"### {title}",
            f"{n_days}天～{total_pois}个地点",
            "由腾讯地图 AI 攻略生成",
            "",
            "### 📋 行程总览",
        ]
        for di, day in enumerate(plan_days, 1):
            pois = day.get("items", [])
            arrow = " -> ".join(link(p, di, ni) for ni, p in enumerate(pois, 1))
            lines.append(f"Day {di}：{arrow}")
        lines.append("")
        lines.append("### 📖 行程详情")
        for di, day in enumerate(plan_days, 1):
            lines.append(f"#### Day {di}：{day.get('day_title', f'第{di}天')}")
            pois = day.get("items", [])
            arrow = " -> ".join(link(p, di, ni) for ni, p in enumerate(pois, 1))
            lines.append(arrow)
            lines.append("")
        return "\n".join(lines)

    def _save_and_gen_qrcode(self, query: str, markdown: str, save_name: Optional[str] = None) -> Dict[str, Any]:
        """调 saveandgenqrcode：保存攻略并生成小程序二维码（一步完成）。

        返回 {"travel_guide_id", "qr_code"(data URI), "qr_path"(本地PNG), "expire_seconds"}。
        """
        markdown_b64 = base64.b64encode(markdown.encode("utf-8")).decode("ascii")
        qimei36 = "skill_" + uuid_hex(16)
        body = {
            "user_id": _OPERATION_USER_ID,
            "user_query": query,
            "markdown_content": markdown_b64,
            "json_content": "",
            "is_check": False,
            "sync_save_route": True,   # 同步校验 POI ID 真实性（耗时 +3-5s，内容更准）
            "qimei36": qimei36,
            "env_version": "release",
        }
        headers = self._sign_headers(markdown_b64, qimei36)
        r = requests.post(_TG_SAVE_QR_URL, json=body, headers=headers, timeout=_TIMEOUT * 2)
        r.raise_for_status()
        resp = r.json()
        if resp.get("code") != 0:
            raise TmapError(resp.get("code"), resp.get("msg", "save&gen qrcode failed"), "saveandgenqrcode", resp)
        data = resp["data"]
        tg_id = data["travel_guide_id"]
        qr = data["qr_code"]
        # 二维码落盘
        png_b64 = qr.split(",", 1)[1] if qr.startswith("data:image/png;base64,") else qr
        fname = save_name or f"travel_guide_{tg_id}.png"
        qr_path = os.path.join(self.qrcode_dir, fname)
        with open(qr_path, "wb") as f:
            f.write(base64.b64decode(png_b64))
        return {
            "travel_guide_id": tg_id,
            "qr_code": qr,
            "qr_path": qr_path,
            "expire_seconds": data.get("expire_seconds"),
        }

    # ------------------------------------------------------------
    # 旅游攻略 — 含腾讯地图小程序入口图（二维码）
    # ------------------------------------------------------------

    def travel_guide(self, query: str, lat: float = 30.572815, lng: float = 104.066801) -> Dict[str, Any]:
        """生成 AI 旅游攻略并入库出腾讯地图小程序入口图。

        :param query: 用户原始 query，例如 "武汉5天精华游"
        :param lat/lng: 用户当前位置（用于 A2A 上下文，不影响目的地）
        :return: {summary, days, travel_guide_id, qr_code, qr_path, mini_program_username}
        """
        a2a = self._a2a_stream(query, lat, lng)
        summary = a2a["plan_summary"] or {}
        days = a2a["plan_days"]
        title = summary.get("summary_title") or query

        # 从第一个 POI 推城市
        city = ""
        for d in days:
            for it in d.get("items", []):
                city = it.get("city_name", "")
                if city:
                    break
            if city:
                break

        markdown = self._build_markdown(days, city or "未知", title)
        saved = self._save_and_gen_qrcode(query, markdown)
        tg_id = saved["travel_guide_id"]

        result = {
            "title": title,
            "summary": summary,
            "days": days,
            "city": city,
            "travel_guide_id": tg_id,
            "qr_code": saved["qr_code"],
            "qr_path": saved["qr_path"],
            "expire_seconds": saved["expire_seconds"],
            "mini_program_username": _MINI_PROGRAM_USERNAME,
        }

        # 强制落盘（utf-8）—— 让 Agent 走文件路径原样输出，不靠自己拼 markdown
        json_path = os.path.join(self.output_dir, f"{tg_id}.json")
        md_path = os.path.join(self.output_dir, f"{tg_id}.md")
        result_for_json = {k: v for k, v in result.items() if k != "qr_code"}
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(result_for_json, f, ensure_ascii=False, indent=2)
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(self.format_for_reply(result))
        result["output_json"] = json_path
        result["output_markdown"] = md_path
        return result

    # ------------------------------------------------------------
    # 地图指南生成（独立能力）—— 接收POI列表，自动构建Markdown并出二维码
    # ------------------------------------------------------------

    def generate_map_guide(
        self,
        pois: List[Dict[str, Any]],
        city: str,
        title: str = "我的指南",
        query: str = "",
        description: str = "",
    ) -> Dict[str, Any]:
        """将POI列表生成腾讯地图小程序指南（含二维码）。

        本方法自动将POI列表转换为标准Markdown格式，然后调用
        generate_guide_from_markdown() 生成指南。

        :param pois: POI列表，每个POI应包含：
            - name: 名称（必须）
            - poi_id: POI ID（必须，先从 poi_search() 获取真实 ID）
            - lat: 纬度（float，会被自动转成 1e6 整数）
            - lng: 经度（float，会被自动转成 1e6 整数）
            - day: 天数分组（可选，默认1）
            - num: 序号（可选，默认按输入顺序自动编号）
            - type: POI类型（可选，默认1）
            - search_query: 搜索关键词（可选，type=2时使用）
            - inday: 散点所属天数（可选）
        :param city: 城市名称（必须，否则保存接口无法解析）
        :param title: 指南标题（可选，默认"我的指南"）
        :param query: 用户原始查询（可选，用于攻略入库备注）
        :param description: 行程/路线描述文本（可选），会插入到输出 markdown 正文中，
            确保用户看到路线规划详情和二维码两部分内容
        :return: {travel_guide_id, qr_code, qr_path, mini_program_username, output_markdown}
        """
        if not query:
            query = title

        markdown = self._build_markdown_from_pois(pois, city, title)
        return self.generate_guide_from_markdown(markdown, query=query, description=description)

    def _build_markdown_from_pois(
        self,
        pois: List[Dict[str, Any]],
        city: str,
        title: str = "我的指南",
    ) -> str:
        """将POI列表转换为保存接口要求的markdown格式。

        严格按照腾讯地图小程序指南保存接口的markdown解析规则构建，
        city 必须存在，lat/lng 自动乘以 1e6 转为整数。

        :param pois: POI列表
        :param city: 城市名称（必须）
        :param title: 指南标题
        :return: 标准Markdown格式字符串
        """
        lines: List[str] = [
            f"### {title}(plan=1)",
            "",
            "### 我的指南",
        ]
        for i, poi in enumerate(pois, 1):
            name = poi.get("name", f"点位{i}")
            day = poi.get("day", 1)
            num = poi.get("num", i)
            poi_id = poi.get("poi_id", "")
            lat = poi.get("lat", 0)
            lng = poi.get("lng", 0)
            lat_int = int(round(lat * 1e6))
            lng_int = int(round(lng * 1e6))
            ptype = poi.get("type", 1)
            search_query = poi.get("search_query", "")
            inday = poi.get("inday", 0)

            params = f"city={city}&day={day}&num={num}&poi_id={poi_id}&lat={lat_int}&lng={lng_int}&type={ptype}"
            if search_query:
                params += f"&search_query={search_query}"
            if inday > 0:
                params += f"&inday={inday}"
            lines.append(f"[{name}]({params})")
        return "\n".join(lines)

    # ------------------------------------------------------------
    # 生成地图指南（独立能力）—— 接收标准 Markdown，直接保存并出二维码
    # ------------------------------------------------------------

    def generate_guide_from_markdown(self, markdown: str, query: str = "", description: str = "") -> Dict[str, Any]:
        """将标准 Markdown 格式的指南内容保存入库，并生成腾讯地图小程序入口二维码。

        本方法直接调用 saveandgenqrcode 接口，跳过 A2A 攻略生成步骤。
        适用于：用户已提供地点列表，直接生成地图指南并跳转手图的场景。

        :param markdown: 标准 Markdown 格式字符串，点位链接格式为
            [点位名](city=城市&day=天数&num=序号&poi_id=POI_ID&lat=纬度&lng=经度&type=类型)
            指南标题格式为 ### [指南名称](plan=1)
        :param query: 用户原始输入（用于攻略入库备注），默认空串
        :param description: 行程/路线描述文本（可选），会嵌入输出 markdown 正文，
            确保用户同时看到路线规划和二维码
        :return: {travel_guide_id, qr_code, qr_path, mini_program_username, output_markdown}
        """
        if not query:
            query = "地图指南"

        saved = self._save_and_gen_qrcode(query, markdown)
        tg_id = saved["travel_guide_id"]

        result = {
            "title": query,
            "travel_guide_id": tg_id,
            "qr_code": saved["qr_code"],
            "qr_path": saved["qr_path"],
            "expire_seconds": saved["expire_seconds"],
            "mini_program_username": _MINI_PROGRAM_USERNAME,
        }

        # 落盘成品 markdown（含二维码图片语法）
        md_path = os.path.join(self.output_dir, f"{tg_id}.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(self._wrap_markdown_with_qrcode(markdown, saved["qr_path"], description))
        result["output_markdown"] = md_path
        return result

    @staticmethod
    def _wrap_markdown_with_qrcode(markdown: str, qr_path: str, description: str = "") -> str:
        """在 Markdown 末尾附加小程序二维码图片语法。

        输出给用户看的是 description（路线详情）+ 二维码。
        POI 技术链接不再展示，仅供保存接口解析。

        输出结构：description 正文 + 二维码 + 扫码引导
        """
        lines: List[str] = []
        if description:
            lines.append(description.strip())
            if len(description.strip()) < 20:
                lines.append("")
                lines.append("> ⚠️ 行程描述过短，请补充各段距离和时间信息")
            lines.append("")
        lines.append(f"![腾讯地图小程序入口图]({qr_path})")
        lines.append("")
        lines.append("👆 微信扫码即可将以上行程保存到腾讯地图小程序，手机直接导航。")
        return "\n".join(lines)

    # ------------------------------------------------------------
    # 把 result 渲染成「可直接贴给用户」的成品 markdown（含末尾二维码）
    # ------------------------------------------------------------

    @staticmethod
    def format_for_reply(result: Dict[str, Any]) -> str:
        """把 travel_guide 的返回 dict 渲染成可直接发给用户的成品 markdown。

        按 A2A 攻略 item 的真实字段组织（无 rich 评分/人均字段）：
        location_name / location_desc(含时段) / location_position(地址) /
        review(推荐理由) / location_intro / tips / image_url。
        末尾附腾讯地图小程序入口二维码。Agent 拿到后原样作为回复正文即可。
        """
        if not result:
            return ""
        title = result.get("title", "旅行攻略")
        days = result.get("days", []) or []
        qr_path = result.get("qr_path", "")
        city = result.get("city", "")

        lines: List[str] = []
        lines.append(f"# {title}")
        if city:
            lines.append(f"目的地：**{city}** · 共 {len(days)} 天 · 由腾讯地图 AI 生成")
        lines.append("")

        for di, day in enumerate(days, 1):
            day_title = day.get("day_title", f"第 {di} 天")
            day_desc = day.get("day_desc", "")
            lines.append(f"## Day {di}：{day_title}")
            if day_desc:
                lines.append(f"> {day_desc}")
            lines.append("")
            for pi, poi in enumerate(day.get("items", []), 1):
                name = poi.get("location_name", "")
                desc = poi.get("location_desc", "")
                addr = poi.get("location_position", "")
                review = poi.get("review", "")
                intro = poi.get("location_intro", "")
                tips = poi.get("tips") or []

                lines.append(f"**{pi}. {name}**")
                if desc:
                    lines.append(f"- ⏰ {desc}")
                if addr:
                    lines.append(f"- 📍 {addr}")
                if review:
                    lines.append(f"- 💡 {review}")
                elif intro:
                    lines.append(f"- 💡 {intro}")
                for tip in tips:
                    if tip:
                        lines.append(f"- 📌 {tip}")
                lines.append("")

        if qr_path:
            lines.append("---")
            lines.append(f"![腾讯地图小程序入口图]({qr_path})")
            lines.append("")
            lines.append("👆 扫码进入腾讯地图小程序，可联动小程序继续完善攻略、与朋友共同编辑行程、规划多人出行。")

        return "\n".join(lines)

    # ------------------------------------------------------------
    # 语义化改写 — 格式方法（参考 MCP format=0 并增强）
    # ------------------------------------------------------------

    @staticmethod
    def _format_geocoder(raw: Dict[str, Any]) -> str:
        """地址 → 坐标 语义化文本"""
        r = raw.get("result", {})
        if not r:
            return "未解析到结果"
        loc = r.get("location", {})
        comp = r.get("address_components", {})
        ad = r.get("ad_info", {})
        lines = [
            f"纬度（latitude）：{loc.get('lat', '')}",
            f"经度（longitude）：{loc.get('lng', '')}",
            f"省（province）：{comp.get('province', '')}",
            f"市（city）：{comp.get('city', '')}",
            f"区（district）：{comp.get('district', '')}",
            f"行政区划代码（adcode）：{ad.get('adcode', '')}",
        ]
        rel = r.get("reliability", 0)
        if rel >= 9:
            lines.append("转换（解析）精度：门址/楼栋")
        elif rel >= 7:
            lines.append("转换（解析）精度：小区、大厦")
        elif rel >= 5:
            lines.append("转换（解析）精度：道路")
        elif rel >= 1:
            lines.append("转换（解析）精度：区县")
        return "\n".join(lines)

    @staticmethod
    def _format_regeocoder(raw: Dict[str, Any]) -> str:
        """坐标 → 地址 语义化文本"""
        r = raw.get("result", {})
        if not r:
            return "未解析到结果"
        comp = r.get("address_component", {}) or r.get("address_components", {})
        lines = [
            f"坐标所在地址（address）：{r.get('address', '')}",
            f"省（province）：{comp.get('province', '')}",
            f"市（city）：{comp.get('city', '')}",
            f"区（district）：{comp.get('district', '')}",
        ]
        ref = r.get("address_reference", {}) or r.get("formatted_addresses", {})
        if isinstance(ref, dict):
            town = _safe_get(ref, "town", "title")
            biz = _safe_get(ref, "business_area", "title")
            lm = _safe_get(ref, "landmark_l1", "title") or _safe_get(ref, "landmark_l2", "title")
            if town:
                lines.append(f"乡镇/街道（town）：{town}")
            if biz:
                lines.append(f"商圈（business area）：{biz}")
            if lm:
                lines.append(f"地标（landmark）：{lm}")
        return "\n".join(lines)

    @staticmethod
    def _format_poi_list(raw: Dict[str, Any]) -> str:
        """POI 列表（search / nearby / sug 共用）语义化文本

        覆盖 MCP 遗漏的 rich 字段：star_level → ⭐，avg_price → 人均¥X，opening_hours → 营业时间
        """
        count = raw.get("count", 0)
        data = raw.get("data", []) or []
        shown = min(len(data), 10)
        lines = [f"找到约{count}条结果，以下为其中{shown}条", ""]
        for i, poi in enumerate(data[:10], 1):
            lines.append(f"({i}) {poi.get('title', '')}")
            lines.append(f"地址：{poi.get('address', '')}")
            lines.append(f"地点ID（POI ID）：{poi.get('id', '')}")
            ad = poi.get("ad_info", {}) or {}
            province = ad.get("province") or poi.get("province", "")
            city = ad.get("city") or poi.get("city", "")
            district = ad.get("district") or poi.get("district", "")
            if province or city or district:
                if province:
                    lines.append(f"省：{province}")
                if city:
                    lines.append(f"市：{city}")
                if district:
                    lines.append(f"区：{district}")
            cat = poi.get("category", "")
            if cat:
                lines.append(f"类型：{cat}")
            loc = poi.get("location", {})
            if loc:
                lines.append(f"纬度：{loc.get('lat', '')}")
                lines.append(f"经度：{loc.get('lng', '')}")
            dist = poi.get("_distance")
            if dist is not None:
                lines.append(f"距离：{_fmt_distance(dist)}")
            # rich 字段（MCP 没有，skill 补上）
            rich_parts = []
            star = poi.get("star_level")
            if star is not None:
                rich_parts.append(f"⭐{star}")
            avg = poi.get("avg_price")
            if avg is not None and avg > 0:
                rich_parts.append(f"人均¥{avg}")
            hours = poi.get("opening_hours")
            if hours:
                rich_parts.append(f"营业时间：{hours}")
            if rich_parts:
                lines.append("  ".join(rich_parts))
            lines.append("")
        return "\n".join(lines)

    @staticmethod
    def _format_poi_detail(raw: Dict[str, Any]) -> str:
        """POI 详情 语义化文本"""
        data = raw.get("data", []) or []
        if not data:
            return "未找到该POI详情"
        poi = data[0]
        lines = [
            "找到1条结果",
            f"(1) {poi.get('title', '')}",
            f"地址：{poi.get('address', '')}",
            f"地点ID（POI ID）：{poi.get('id', '')}",
        ]
        ad = poi.get("ad_info", {}) or {}
        province = ad.get("province") or poi.get("province", "")
        city = ad.get("city") or poi.get("city", "")
        district = ad.get("district") or poi.get("district", "")
        if province or city or district:
            if province:
                lines.append(f"省：{province}")
            if city:
                lines.append(f"市：{city}")
            if district:
                lines.append(f"区：{district}")
        cat = poi.get("category", "")
        if cat:
            lines.append(f"类型：{cat}")
        loc = poi.get("location", {})
        if loc:
            lines.append(f"纬度：{loc.get('lat', '')}")
            lines.append(f"经度：{loc.get('lng', '')}")
        star = poi.get("star_level")
        if star is not None:
            lines.append(f"评分：⭐{star}")
        avg = poi.get("avg_price")
        if avg is not None and avg > 0:
            lines.append(f"人均消费：¥{avg}")
        hours = poi.get("opening_hours")
        if hours:
            lines.append(f"营业时间：{hours}")
        tel = poi.get("tel")
        if tel:
            lines.append(f"电话：{tel}")
        return "\n".join(lines)

    @staticmethod
    def _format_direction(raw: Dict[str, Any], mode: str) -> str:
        """路线规划（driving/walking/bicycling/transit 共用）语义化文本"""
        result = raw.get("result", {})
        routes = result.get("routes", []) or []
        if not routes:
            return "未规划出路线"

        if mode == "transit":
            return TmapClient._format_transit_direction(routes)

        r = routes[0]
        dist = r.get("distance", 0)
        dur = r.get("duration", 0)
        parts = [
            f"路线总距离：{_fmt_distance(dist)}",
            f"路线预估用时：{_fmt_duration(dur)}",
        ]
        if mode == "driving":
            toll = r.get("toll", 0)
            lights = r.get("traffic_light_count", 0)
            taxi_fare = r.get("taxi_fare", {})
            if isinstance(taxi_fare, dict):
                taxi = taxi_fare.get("fare", 0)
            else:
                taxi = 0
            route_id = r.get("route_id", "")
            parts.append(f"过路费：¥{toll}")
            if taxi:
                parts.append(f"预估打车费：¥{taxi}")
            if lights:
                parts.append(f"红绿灯：{lights}个")
            if route_id:
                parts.append(f"路线ID（route_id）：{route_id}")
        # 途经道路
        roads = []
        for step in r.get("steps", []):
            rd = step.get("road_name", "")
            if rd and rd not in roads:
                roads.append(rd)
        if roads:
            parts.append(f"途经道路：{'、'.join(roads[:10])}")
        # 路况（仅 driving）
        if mode == "driving":
            level_map = {0: "畅通", 1: "缓行", 2: "拥堵", 3: "无路况", 4: "严重拥堵"}
            level_buckets: Dict[str, int] = {}
            for seg in r.get("speed", []):
                    lv = level_map.get(seg.get("level", 3), "无路况")
                    level_buckets[lv] = level_buckets.get(lv, 0) + seg.get("distance", 0)
            if level_buckets:
                road_str = "，".join(f"{_fmt_distance(d)} {k}" for k, d in level_buckets.items())
                parts.append(f"路况：{road_str}")
        return "，".join(parts)

    @staticmethod
    def _format_transit_direction(routes: List[Dict[str, Any]]) -> str:
        """公交路线专用格式化（人文化时间/距离）"""
        lines = [f"为您找到{len(routes)}条乘坐方案", ""]
        for i, r in enumerate(routes[:5], 1):
            dur = r.get("duration", 0)
            walk_dist = 0
            station_count = 0
            bus_lines: List[str] = []
            steps_text: List[str] = []
            total_fee = r.get("price", 0)
            for step in r.get("steps", []):
                if step.get("mode") == "WALKING":
                    walk_dist += step.get("distance", 0)
                    for ws in step.get("steps", []):
                        ins = ws.get("instruction", "")
                        if ins:
                            steps_text.append(ins)
                elif step.get("mode") == "TRANSIT":
                    for bl in step.get("lines", []):
                        station_count += bl.get("station_count", 0)
                        bus_lines.append(bl.get("title", ""))
                        geton = bl.get("geton", {})
                        getoff = bl.get("getoff", {})
                        steps_text.append(
                            f"乘坐{bl.get('title', '')}，"
                            f"{geton.get('title', '')}上车，"
                            f"经过{bl.get('station_count', 0)}站到达"
                            f"{getoff.get('title', '')}"
                        )
            fee_str = f"，预估费用{total_fee/100:.2f}元" if total_fee > 0 else ""
            lines.append(
                f"方案{i}：用时{_fmt_duration(dur)}，总步行{_fmt_distance(walk_dist)}，"
                f"共{station_count}站{fee_str}"
            )
            lines.append(f"乘坐线路：{'、'.join(bus_lines)}")
            lines.append("详细换乘方案：")
            for s in steps_text:
                lines.append(s)
            lines.append("")
        return "\n".join(lines)

    @staticmethod
    def _format_weather(raw: Dict[str, Any], wt: str = "now") -> str:
        """天气（now / future）语义化文本"""
        r = raw.get("result", {})
        if wt == "now":
            rt = (r.get("realtime") or [{}])[0]
            province = rt.get("province", "")
            city = rt.get("city", "")
            district = rt.get("district", "")
            # 省/市/区三级去重（直辖市 province == city，避免"北京市北京市"）
            loc_parts = []
            if province:
                loc_parts.append(province)
            if city and city != province:
                loc_parts.append(city)
            if district and district not in (province, city):
                loc_parts.append(district)
            location = "".join(loc_parts)
            info = rt.get("infos", {})
            return (
                f"{location}当前天气情况为：{info.get('weather', '')},"
                f"气温{info.get('temperature', '')}℃, "
                f"{info.get('wind_direction', '')}({_fmt_wind(info.get('wind_power', ''))})，"
                f"湿度: {info.get('humidity', '')}%"
            )
        # future
        fc = r.get("forecast", []) or []
        if not fc:
            return "暂无天气预报数据"
        f0 = fc[0]
        infos = f0.get("infos", [])
        province = f0.get("province", "")
        city = f0.get("city", "")
        # 直辖市去重（province == city 时只留一次）
        location = city if city == province else f"{province}{city}"
        lines = [f"{location}未来{len(infos)}天天气预报"]
        for info in infos:
            date = info.get("date", "")
            week = info.get("week", "")
            lines.append(f"{date}({week})")
            for half, label in [("day", "白天"), ("night", "夜晚")]:
                h = info.get(half, {})
                if h:
                    lines.append(
                        f"{label}：{h.get('weather', '')},"
                        f"气温{h.get('temperature', '')}℃, "
                        f"{h.get('wind_direction', '')}({_fmt_wind(h.get('wind_power', ''))})，"
                        f"湿度: {h.get('humidity', '')}%"
                    )
        return "\n".join(lines)

    @staticmethod
    def _format_ip_location(raw: Dict[str, Any]) -> str:
        """IP 定位 语义化文本"""
        r = raw.get("result", {})
        if not r:
            return "未获取到IP定位信息"
        ad = r.get("ad_info", {}) or r.get("location", {})
        if isinstance(ad, dict) and "lat" in ad:
            loc = ad
            ad = r.get("ad_info", {}) or {}
        else:
            loc = r.get("location", {})
        lines = [
            f"国家/地区: {ad.get('nation', '')}",
            f"国家/地区代码: {ad.get('nation_code', '')}",
            f"省（province）：{ad.get('province', '')}",
            f"市（city）：{ad.get('city', '')}",
            f"区/县（district）：{ad.get('district', '')}",
            f"行政区划代码(adcode): {ad.get('adcode', '')}",
            f"纬度: {loc.get('lat', '')}",
            f"经度: {loc.get('lng', '')}",
        ]
        return "\n".join(lines)

    @staticmethod
    def _get_district_level(adcode: str) -> str:
        """根据行政区划代码推断行政级别"""
        if not adcode or len(adcode) < 6:
            return ""
        if adcode.endswith("0000"):
            return "省/直辖市"
        elif adcode.endswith("00"):
            return "地级市"
        else:
            return "区/县/县级市"

    @staticmethod
    def _format_district(raw: Dict[str, Any], header: str = "") -> str:
        """行政区划（list/children/search 共用）语义化文本

        header: 描述性头部，如"全国省级行政区" / "搜索「朝阳」"
        """
        result = raw.get("result", []) or []
        if isinstance(result, list) and len(result) > 0 and isinstance(result[0], list):
            districts = result[0]
        else:
            districts = result
        if not districts:
            return "未找到行政区划数据"

        total = len(districts)
        shown = min(total, 20)

        # 统计级别分布
        level_count: dict = {}
        for d in districts:
            lv = TmapClient._get_district_level(d.get("id", ""))
            level_count[lv] = level_count.get(lv, 0) + 1
        level_str = "，".join(f"{v}个{k}" for k, v in level_count.items())

        # 头部
        header_line = f"{header}共 {total} 个行政区划（{level_str}）" if header else f"共 {total} 个行政区划（{level_str}）"
        lines = [header_line]
        if total > shown:
            lines.append(f"（仅展示前 {shown} 条）")
        lines.append("")

        # 列表项：名称 + 级别 + ID
        for i, d in enumerate(districts[:shown], 1):
            name = d.get("fullname", "") or d.get("name", "")
            did = d.get("id", "")
            lv = TmapClient._get_district_level(did)
            label = f"{name}（{lv}）" if lv else name
            lines.append(f"{i}. {label}  |  ID: {did}")

        return "\n".join(lines)

    @staticmethod
    def _format_distance_matrix(raw: Dict[str, Any]) -> str:
        """距离矩阵 语义化文本"""
        r = raw.get("result", {})
        rows = r.get("rows", []) or []
        if not rows or not rows[0].get("elements"):
            return "未计算出距离"
        elem = rows[0]["elements"][0]
        dist = elem.get("distance", 0)
        dur = elem.get("duration", 0)
        return f"距离{_fmt_distance(dist)}，预计用时{_fmt_duration(dur / 60)}"

    def poi_search(
        self,
        keyword: str,
        region: Optional[str] = None,
        location: Optional[str] = None,
        page_size: int = 10,
        page_index: int = 1,
        raw: bool = False,
    ) -> Dict[str, Any]:
        """POI 关键词搜索（按城市或中心点）。

        返回 ≥2 个结果时，必须紧接着调用 generate_map_guide() 生成小程序指南。

        :param keyword: 搜索词，必填
        :param region: 城市/区域，例如 "深圳" / "武汉"
        :param location: 中心点 "lat,lng"，与 region 二选一
        :param page_size: 每页 1-20，默认 10
        :param page_index: 页码，默认 1
        :param raw: 为 True 时返回原始 JSON，默认返回语义化文本
        :return: 语义化文本或原始 JSON
        """
        if not region and not location:
            raise ValueError("region 和 location 至少传一个")

        boundary = f"region({region})" if region else f"nearby({location},5000)"
        params = {
            "keyword": keyword,
            "boundary": boundary,
            "page_size": min(page_size, 20),
            "page_index": page_index,
        }
        params.update(self._rich_params())
        data = self._place_search_get("/ws/place/v1/search", params)
        if raw:
            return data
        return self._format_poi_list(data)

    def poi_detail(self, poi_id: str, raw: bool = False) -> Dict[str, Any]:
        """根据 POI ID 取详情。

        :param poi_id: POI 唯一 ID（来自 poi_search/poi_sug 返回，或 A2A 攻略里的 poi_uid）
        :param raw: 为 True 时返回原始 JSON，默认返回语义化文本
        :return: 语义化文本或原始 JSON
        """
        data = self._ws_get("/ws/place/v1/detail", {"id": poi_id})
        if raw:
            return data
        return self._format_poi_detail(data)

    def poi_nearby(
        self,
        keyword: str,
        location: str,
        radius: int = 1000,
        page_size: int = 10,
        page_index: int = 1,
        raw: bool = False,
    ) -> Dict[str, Any]:
        """周边搜索（圆形范围）。

        :param keyword: 搜索词，必填，例如 "咖啡" / "加油站"
        :param location: 中心点 "lat,lng"，必填
        :param radius: 半径，米，取值 10-1000（官方上限 1000）
        :param page_size: 每页 1-20，默认 10
        :param page_index: 页码，默认 1
        :param raw: 为 True 时返回原始 JSON，默认返回语义化文本
        :return: 语义化文本或原始 JSON
        """
        radius = max(10, min(int(radius), 1000))
        params = {
            "keyword": keyword,
            "boundary": f"nearby({location},{radius},1)",
            "page_size": min(page_size, 20),
            "page_index": page_index,
        }
        params.update(self._rich_params())
        data = self._place_search_get("/ws/place/v1/search", params)
        if raw:
            return data
        return self._format_poi_list(data)


    def direction(
        self,
        from_addr: str,
        to_addr: str,
        mode: str = "driving",
        region: Optional[str] = None,
        raw: bool = False,
    ) -> Dict[str, Any]:
        """路线规划。先把起终点地址/景点名转坐标，再调腾讯路线接口。

        调用本方法后，必须紧接着调用 generate_map_guide() 生成小程序指南。
        路线详情和小程序指南必须同时出现在回复中，不可只给路线不给指南。

        :param from_addr: 起点地址 / POI 名 / "lat,lng"
        :param to_addr: 终点地址 / POI 名 / "lat,lng"
        :param mode: driving / transit / walking / bicycling，默认 driving
        :param region: 城市名，辅助把"象鼻山"这类景点名解析到正确城市
        :param raw: 为 True 时返回原始 JSON，默认返回语义化文本
        :return: 语义化文本或原始 JSON
        """
        if mode not in ("driving", "transit", "walking", "bicycling"):
            raise ValueError(f"mode 必须是 driving/transit/walking/bicycling, got {mode}")

        f_loc = self._resolve_location(from_addr, region=region)
        t_loc = self._resolve_location(to_addr, region=region)
        params = {
            "from": f"{f_loc['lat']},{f_loc['lng']}",
            "to": f"{t_loc['lat']},{t_loc['lng']}",
        }
        if mode == "driving":
            params["get_speed"] = 1
            params["added_fields"] = "route_id"
        data = self._ws_get(f"/ws/direction/v1/{mode}", params)
        if raw:
            return data
        return self._format_direction(data, mode)

    # ------------------------------------------------------------
    # 数据型原子能力（无跳转）
    # ------------------------------------------------------------

    def geocoder(self, address: str, policy: int = 1, raw: bool = False) -> Dict[str, Any]:
        """地址 / 地标名 / POI 名 → 坐标。

        :param address: 地址或地点名。可含城市更准；不含城市时靠 policy=1 兜底。
        :param policy: 解析策略。0=标准（地址须含城市，否则报 348）；
                       1=宽松（默认，允许无城市，支持景点/地标/POI 名，如"象鼻山"）。
        :param raw: 为 True 时返回原始 JSON，默认返回语义化文本
        :return: 语义化文本或原始 JSON
        """
        data = self._ws_get("/ws/geocoder/v1", {
            "address": address,
            "policy": policy,
        })
        if raw:
            return data
        return self._format_geocoder(data)

    def regeocoder(self, lat: float, lng: float, get_poi: bool = False,
                   raw: bool = False) -> Dict[str, Any]:
        """坐标 → 地址（可选返周边 POI）。

        :param raw: 为 True 时返回原始 JSON，默认返回语义化文本
        :return: 语义化文本或原始 JSON
        """
        data = self._ws_get("/ws/geocoder/v1", {
            "location": f"{lat},{lng}",
            "get_poi": 1 if get_poi else 0,
        })
        if raw:
            return data
        return self._format_regeocoder(data)

    def poi_sug(self, keyword: str, region: Optional[str] = None,
                location: Optional[str] = None, raw: bool = False) -> Dict[str, Any]:
        """关键词输入补全。

        :param raw: 为 True 时返回原始 JSON，默认返回语义化文本
        :return: 语义化文本或原始 JSON
        """
        params = {
            "keyword": keyword,
            "region": region,
            "location": location,
        }
        params.update(self._rich_params())
        data = self._place_search_get("/ws/place/v1/suggestion", params)
        if raw:
            return data
        return self._format_poi_list(data)

    def ip_location(self, ip: Optional[str] = None, raw: bool = False) -> Dict[str, Any]:
        """IP 定位（不传则定位调用方 IP）。

        :param raw: 为 True 时返回原始 JSON，默认返回语义化文本
        :return: 语义化文本或原始 JSON
        """
        params = {}
        if ip:
            params["ip"] = ip
        data = self._ws_get("/ws/location/v1/ip", params)
        if raw:
            return data
        return self._format_ip_location(data)

    def district_list(self, raw: bool = False) -> Dict[str, Any]:
        """全国行政区划列表（省级）。

        :param raw: 为 True 时返回原始 JSON，默认返回语义化文本
        :return: 语义化文本或原始 JSON
        """
        data = self._ws_get("/ws/district/v1/list", {})
        if raw:
            return data
        return self._format_district(data, "全国省级行政区")

    def district_children(self, parent_id: str, raw: bool = False) -> Dict[str, Any]:
        """根据父级 ID 获取下级行政区划。

        :param raw: 为 True 时返回原始 JSON，默认返回语义化文本
        :return: 语义化文本或原始 JSON
        """
        data = self._ws_get("/ws/district/v1/getchildren", {"id": parent_id})
        if raw:
            return data
        return self._format_district(data, f"区划 {parent_id} 下辖")

    def district_search(self, keyword: str, raw: bool = False) -> Dict[str, Any]:
        """关键词搜索行政区划。

        :param raw: 为 True 时返回原始 JSON，默认返回语义化文本
        :return: 语义化文本或原始 JSON
        """
        data = self._ws_get("/ws/district/v1/search", {"keyword": keyword})
        if raw:
            return data
        return self._format_district(data, f"搜索「{keyword}」")

    def distance_matrix(
        self,
        origin: str,
        dest: str,
        mode: str = "driving",
        raw: bool = False,
    ) -> Dict[str, Any]:
        """两点间距离计算。

        :param origin: 起点坐标 "lat,lng"
        :param dest: 终点坐标 "lat,lng"
        :param mode: driving/walking/bicycling
        :param raw: 为 True 时返回原始 JSON，默认返回语义化文本
        :return: 语义化文本或原始 JSON
        """
        data = self._ws_get("/ws/distance/v1/matrix", {
            "mode": mode,
            "from": origin,
            "to": dest,
        })
        if raw:
            return data
        return self._format_distance_matrix(data)

    def weather(self, adcode: Optional[str] = None, location: Optional[str] = None,
                type: str = "now", raw: bool = False) -> Dict[str, Any]:
        """天气查询。adcode 与 location 二选一。

        :param adcode: 行政区划代码，如北京 "110000"
        :param location: 坐标 "lat,lng"
        :param type: "now" 实时天气 / "future" 预报，默认 now
        :param raw: 为 True 时返回原始 JSON，默认返回语义化文本
        :return: 语义化文本或原始 JSON
        """
        if not adcode and not location:
            raise ValueError("adcode 和 location 至少传一个")
        params: Dict[str, Any] = {"type": type}
        if adcode:
            params["adcode"] = adcode
        if location:
            params["location"] = location
        data = self._ws_get("/ws/weather/v1", params)
        if raw:
            return data
        return self._format_weather(data, type)

    def coord_translate(
        self,
        locations: Any,
        type: int = 1,
        raw: bool = False,
    ) -> Any:
        """坐标系转换 → 统一转为腾讯地图使用的 GCJ-02 坐标。

        调用官方 /ws/coord/v1/translate 接口。单次最多 100 个点。

        :param locations: 待转坐标，支持三种入参：
            - 字符串："lat,lng" 或 "lat1,lng1;lat2,lng2"（官方原生格式）
            - 单点元组/列表：(lat, lng)
            - 多点列表：[(lat1, lng1), (lat2, lng2), ...]
        :param type: 输入坐标类型。1=GPS(WGS-84)，2=sogou 经纬度，3=baidu，
            4=mapbar，5=[默认]GCJ-02（等于不转），6=sogou 墨卡托。GPS 转腾讯用 1。
        :param raw: True 返回原始 JSON，默认返回与入参形态一致的坐标结构。
        :return:
            - raw=True：官方原始 JSON
            - 单点入参：{"lat": .., "lng": ..}
            - 多点入参：[{"lat": .., "lng": ..}, ...]
        """
        # 归一化入参
        single = False
        if isinstance(locations, str):
            loc_str = locations.strip()
        else:
            # 单点 (lat, lng)
            if (
                isinstance(locations, (list, tuple))
                and len(locations) == 2
                and all(isinstance(x, (int, float)) for x in locations)
            ):
                pts = [tuple(locations)]
                single = True
            elif isinstance(locations, (list, tuple)):
                pts = [tuple(p) for p in locations]
            else:
                raise ValueError(
                    "locations 需为 'lat,lng[;lat,lng]' 字符串，或 (lat,lng) / [(lat,lng),...]"
                )
            if len(pts) > 100:
                raise ValueError("coord_translate 单次最多 100 个点")
            loc_str = ";".join(f"{lat},{lng}" for lat, lng in pts)

        data = self._ws_get("/ws/coord/v1/translate", {
            "locations": loc_str,
            "type": type,
        })
        if raw:
            return data

        out = [{"lat": p["lat"], "lng": p["lng"]} for p in data.get("locations", [])]
        if single and out:
            return out[0]
        return out

    # ------------------------------------------------------------
    # 内部辅助
    # ------------------------------------------------------------

    def _resolve_location(self, addr: str, region: Optional[str] = None) -> Dict[str, float]:
        """地址 / POI 名 / 'lat,lng' → {lat, lng}

        优先级：① 已是坐标直接用 → ② geocoder 结构化地址解析
        → ③ 回退 poi_sug/poi_search（景点名、店名等非标准地址走这条）。
        """
        # ① 已经是 "lat,lng"
        addr_clean = addr.strip()
        if "," in addr_clean:
            parts = addr_clean.split(",")
            if len(parts) == 2:
                try:
                    lat = float(parts[0].strip())
                    lng = float(parts[1].strip())
                    return {"lat": lat, "lng": lng}
                except (ValueError, TypeError):
                    pass
        # ② 地址/地点名解析（geocoder 默认 policy=1，支持景点名）
        #    有 region 时拼到地址前，消除同名歧义（如"象鼻山"→"桂林象鼻山"）
        addr_for_geo = addr_clean
        if region and not addr_clean.startswith(region) and region not in addr_clean:
            addr_for_geo = f"{region}{addr_clean}"
        try:
            geo = self.geocoder(addr_for_geo, raw=True)
            loc = (geo.get("result") or {}).get("location", {})
            if loc.get("lat") is not None and loc.get("lng") is not None:
                return {"lat": loc["lat"], "lng": loc["lng"]}
        except TmapError:
            pass  # 极少数解析不了的，转 POI 搜索兜底
        # ③ POI 搜索兜底：sug 优先（更宽容），再 search
        for finder in (
            lambda: self.poi_sug(addr, region=region, raw=True).get("data", []),
            lambda: self.poi_search(addr, region=region, page_size=1, raw=True).get("data", []),
        ):
            try:
                pois = finder()
            except Exception:
                pois = []
            if pois:
                loc = pois[0].get("location") or {}
                if isinstance(loc, str) and "," in loc:  # sug 的 location 可能是字符串
                    try:
                        lat, lng = [float(x) for x in loc.split(",")]
                        return {"lat": lat, "lng": lng}
                    except Exception:
                        pass
                if loc.get("lat") is not None and loc.get("lng") is not None:
                    return {"lat": loc["lat"], "lng": loc["lng"]}
        raise TmapError(348, _fmt_tmap_error(348, f"无法解析地址/地点：{addr}（请补充城市或换更具体的名称）"), "/_resolve_location", {})


# ============================================================
# 异常 & 工具
# ============================================================

class TmapError(Exception):
    def __init__(self, code: Any, message: str, api: str, raw: Any):
        self.code = code
        self.message = message
        self.api = api
        self.raw = raw
        super().__init__(f"[{api}] code={code} msg={message}")


def uuid_hex(n: int = 16) -> str:
    return "".join(random.choices("0123456789abcdef", k=n))


# ============================================================
# CLI（开发自测用）
# ============================================================

if __name__ == "__main__":
    import sys
    c = TmapClient()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "geocoder"
    if cmd == "geocoder":
        print(json.dumps(c.geocoder("深圳市腾讯滨海大厦", raw=True), ensure_ascii=False, indent=2))
    elif cmd == "regeocoder":
        print(json.dumps(c.regeocoder(22.540601, 113.93397, get_poi=True, raw=True), ensure_ascii=False, indent=2))
    elif cmd == "poi_search":
        print(json.dumps(c.poi_search("黄鹤楼", region="武汉", raw=True), ensure_ascii=False, indent=2))
    elif cmd == "poi_detail":
        print(json.dumps(c.poi_detail("7025968886543661739", raw=True), ensure_ascii=False, indent=2))
    elif cmd == "poi_nearby":
        print(json.dumps(c.poi_nearby("咖啡", location="22.540601,113.93397", radius=1000, raw=True), ensure_ascii=False, indent=2))
    elif cmd == "poi_sug":
        print(json.dumps(c.poi_sug("黄鹤楼", region="武汉", raw=True), ensure_ascii=False, indent=2))
    elif cmd == "ip":
        print(json.dumps(c.ip_location(raw=True), ensure_ascii=False, indent=2))
    elif cmd == "district_list":
        print(json.dumps(c.district_list(raw=True), ensure_ascii=False, indent=2))
    elif cmd == "direction":
        print(json.dumps(c.direction("深圳北站", "深圳湾口岸", "driving", raw=True), ensure_ascii=False, indent=2))
    elif cmd == "travel_guide":
        print(json.dumps(c.travel_guide(sys.argv[2] if len(sys.argv) > 2 else "武汉5天精华游"), ensure_ascii=False, indent=2))
    else:
        print(f"unknown cmd: {cmd}")
