"""
DEV（测试环境）日志搜索助手脚本
用法：由 SKILL.md 驱动，不要直接调用；各子命令通过 CLI 参数区分。
"""
import argparse
import json
import re
import sys
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from pathlib import Path

CACHE_DIR = Path.home() / ".DEV_SKILL" / "dev-find-log"
SERVICES_FILE = CACHE_DIR / "services.json"
SERVICES_TTL = 300  # 5 分钟
HOST = "https://devtool.flightroutes24.com"

# ── 工具函数 ──────────────────────────────────────────────────────────────────

def load_config():
    defaults = {
        "profile": "DEV",
        "user": "dev-agentskill",
        "gray": "zzr",
        "webVersion": "1.0.0",
        "sshToken": "",
    }
    config_file = CACHE_DIR / "config.json"
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    if config_file.exists():
        try:
            overrides = json.loads(config_file.read_text(encoding="utf-8"))
            defaults.update({k: v for k, v in overrides.items() if v is not None and v != ""})
        except Exception:
            pass
    return defaults


def headers(cfg):
    h = {
        "Content-Type": "application/json",
        "profile": cfg["profile"],
        "user": cfg["user"],
        "webVersion": cfg.get("webVersion", "1.0.0"),
    }
    if cfg.get("gray"):
        h["gray"] = cfg["gray"]
    return h


def get(cfg, path, timeout=30, stream=False):
    import urllib.request
    url = HOST + path
    req = urllib.request.Request(url, headers=headers(cfg))
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        if stream:
            return resp.read()
        return json.loads(resp.read().decode("utf-8"))


def post(cfg, path, body, timeout=300):
    import urllib.request
    url = HOST + path
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers(cfg), method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        text = resp.read().decode("utf-8")
        return json.loads(text) if text.strip() else {}


# ── 服务列表加载 ───────────────────────────────────────────────────────────────

def load_services(force_refresh=False):
    """加载服务列表，5 分钟内有缓存则复用，否则从接口刷新。"""
    cfg = load_config()
    need_refresh = force_refresh
    if not need_refresh:
        if not SERVICES_FILE.exists() or time.time() - SERVICES_FILE.stat().st_mtime >= SERVICES_TTL:
            need_refresh = True
    if need_refresh:
        data = get(cfg, "/ssh/searchService")
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        SERVICES_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        data = json.loads(SERVICES_FILE.read_text(encoding="utf-8"))
    return data


# ── 服务匹配 ───────────────────────────────────────────────────────────────────

def match_services(keyword: str, services: list) -> dict:
    """
    根据关键词匹配服务列表。

    精确匹配：keyword 中的所有词均出现在 label/value/keyWord 中。
    模糊候选：按命中词数从多到少排序，返回前 5 个，供用户选择。

    返回:
        {
          "matched": [...],   # 精确匹配到的服务 value 列表
          "candidates": [...] # 若精确匹配为空，返回最相似的 5 个服务对象
        }
    """
    kw_lower = keyword.lower()
    words = kw_lower.split()

    exact = []
    scored = []
    for s in services:
        haystack = " ".join([
            s.get("label", ""),
            s.get("value", ""),
            s.get("keyWord", ""),
        ]).lower()
        hit_count = sum(1 for w in words if w in haystack)
        if hit_count == len(words):
            exact.append(s["value"])
        elif hit_count > 0:
            scored.append((hit_count, s))

    if exact:
        return {"matched": exact, "candidates": []}

    # 无精确匹配，按命中词数降序取前 5
    scored.sort(key=lambda x: -x[0])
    candidates = [s for _, s in scored[:5]]
    return {"matched": [], "candidates": candidates}


def cmd_match(args):
    """子命令：匹配服务，输出 JSON 结果供 agent 判断。"""
    services = load_services(args.refresh)
    result = match_services(args.keyword, services)
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ── services（列表查看）────────────────────────────────────────────────────────

def cmd_services(args):
    services = load_services(args.refresh)
    print(f"共 {len(services)} 个服务", file=sys.stderr)
    if args.keyword:
        kw = args.keyword.lower()
        services = [s for s in services
                    if kw in s.get("label","").lower()
                    or kw in s.get("keyWord","").lower()
                    or kw in s.get("value","").lower()]
    print(json.dumps(services, ensure_ascii=False, indent=2))


# ── parse-time ────────────────────────────────────────────────────────────────

def parse_time(text: str) -> dict:
    """
    从 traceId / requestId 文本中解析 CST（UTC+8）时间，与前端 parseTimestampAndService 一致。

    长时间戳（末尾 ≥13 位数字，取前 13 位作毫秒 epoch，UTC 转 CST）：
      web_export_xxx.178280764031703170 → 1782807640317ms → 2026-06-30 16:20:40 CST

    短时间戳（字母/下划线后跟 12 位 YYMMDDHHmmss，本身即 CST）：
      web_export_xxx_260630162040yyy → 2026-06-30 16:20:40 CST

    startDate 直接等于解析出的日志时间（不减分钟），服务端 matchLogFile 以此精确定位文件。
    """
    CST_OFFSET = timedelta(hours=8)
    text = text.strip()

    # 长时间戳
    m = re.match(r"^.*?[\.\d]*\.(\d+)$", text)
    if m:
        digits = m.group(1)
        if len(digits) >= 13:
            ms = int(digits[:13])
            dt_cst = datetime(1970, 1, 1) + timedelta(milliseconds=ms) + CST_OFFSET
            ts = dt_cst.strftime("%Y-%m-%d %H:%M:%S")
            return {"startDate": ts, "logTime": ts, "parsedFrom": "longTimestamp"}

    # 短时间戳
    m = re.match(r"^.*[_a-zA-Z]+(\d{12}).*$", text)
    if m:
        try:
            dt_cst = datetime.strptime("20" + m.group(1), "%Y%m%d%H%M%S")
            ts = dt_cst.strftime("%Y-%m-%d %H:%M:%S")
            return {"startDate": ts, "logTime": ts, "parsedFrom": "shortTimestamp"}
        except ValueError:
            pass

    return {"startDate": None, "logTime": None, "parsedFrom": None}


def cmd_parse_time(args):
    print(json.dumps(parse_time(args.text), ensure_ascii=False))


# ── traceId / 交易链路（DEV 测试环境）──────────────────────────────────────────

DEV_SUFFIX_PATTERN = re.compile(r"[-_](deve|deva|devb|devf|devc)(?:[_-]|$)", re.I)

# supplierChannel → DEV 底层 adapter 服务名前缀（不含环境后缀）
CHANNEL_TO_ADAPTER_PREFIX = {
    "NDC": "ndcAdapter",
    "OTA": "otaAdapter",
    "GDS": "amadeusAdapter",
    "SPIDER": "spiderAdapter",
    "API": "apiAdapter",
}

ROUTING_BEAN_TO_ADAPTER_PREFIX = {
    "domesticDealService": "otaAdapter-domestic",
    "domesticdealservice": "otaAdapter-domestic",
    "otaDealService": "otaAdapter",
    "otadealservice": "otaAdapter",
    "ndcDealService": "ndcAdapter",
    "ndcdealservice": "ndcAdapter",
    "amadeusDealService": "amadeusAdapter",
    "amadeusdealservice": "amadeusAdapter",
}

# 用户指定某服务泳道标签时，仅该服务走特殊实例，未指定的仍用 trace 默认后缀（deve）
KNOWN_SERVICE_BASES = [
    "adapter_ota",
    "adapter_route",
    "adapter_api",
    "otaAdapter-domestic",
    "ndcAdapter",
    "otaAdapter",
    "amadeusAdapter",
    "sabreAdapter",
    "spiderAdapter",
    "apiAdapter",
    "export",
    "b2b",
    "agg",
    "order",
]

ROLE_ALIASES = {
    "ota": "adapter_ota",
    "ndc": "ndcAdapter",
    "amadeus": "amadeusAdapter",
    "sabre": "sabreAdapter",
    "spider": "spiderAdapter",
    "api": "adapter_api",
}

ADAPTER_PREFIX_OVERRIDE_KEYS = {
    "ndcAdapter": ("ndcAdapter", "ndc"),
    "otaAdapter": ("adapter_ota", "ota", "otaAdapter"),
    "otaAdapter-domestic": ("adapter_ota", "ota", "otaAdapter-domestic", "otaAdapter"),
    "amadeusAdapter": ("amadeusAdapter", "amadeus"),
    "sabreAdapter": ("sabreAdapter", "sabre"),
    "spiderAdapter": ("spiderAdapter", "spider"),
    "apiAdapter": ("apiAdapter", "api", "adapter_api"),
}


def _sorted_bases() -> list[str]:
    return sorted(KNOWN_SERVICE_BASES, key=len, reverse=True)


def looks_like_full_service(name: str) -> bool:
    if not name:
        return False
    for base in _sorted_bases():
        if name == base or name.startswith(f"{base}_") or name.startswith(f"{base}-"):
            return True
    return False


def normalize_lane_role(role: str) -> str:
    role = (role or "").strip()
    if not role:
        return role
    return ROLE_ALIASES.get(role.lower(), role)


def lane_value_to_service(role: str, value: str, default_suffix: str) -> str:
    """将 role + 标签值解析为完整 DEV 服务名。"""
    role = normalize_lane_role(role)
    value = (value or "").strip()
    if not value:
        return resolve_dev_service(role, default_suffix)
    if looks_like_full_service(value):
        return value
    if role == "adapter_ota":
        return f"adapter_ota_{value}"
    if role.startswith("otaAdapter-domestic"):
        return f"otaAdapter-domestic_{value}"
    if role.startswith("otaAdapter"):
        return f"otaAdapter_{value}"
    return f"{role}_{value}"


def parse_lane_token(token: str) -> tuple[str, str] | None:
    """解析 ota=ztC / ota_ztC / adapter_ota_ztC / agg_zzr 等。"""
    token = (token or "").strip()
    if not token:
        return None
    if "=" in token:
        role, val = token.split("=", 1)
        role = normalize_lane_role(role.strip())
        val = val.strip()
        if role and val:
            return role, val
        return None
    if looks_like_full_service(token):
        for base in _sorted_bases():
            if token == base:
                return base, token
            if token.startswith(f"{base}_"):
                return base, token[len(base) + 1 :]
            if token.startswith(f"{base}-"):
                return base, token[len(base) + 1 :]
    for base in _sorted_bases() + list(ROLE_ALIASES.keys()):
        prefix = f"{base}_"
        if token.lower().startswith(prefix.lower()):
            return normalize_lane_role(base), token[len(prefix) :]
    return None


def parse_lane_overrides(
    lane_args: list | None = None,
    extra: list | None = None,
    default_suffix: str = "deve",
) -> tuple[dict[str, str], list[str]]:
    """
    解析用户指定的服务泳道覆盖。
    返回 (role -> 完整服务名, 未能解析为泳道的额外服务名列表)。
    """
    overrides: dict[str, str] = {}
    remaining: list[str] = []

    for token in (lane_args or []) + (extra or []):
        parsed = parse_lane_token(token)
        if not parsed:
            remaining.append(token)
            continue
        role, val = parsed
        full = lane_value_to_service(role, val, default_suffix)
        overrides[role] = full
        overrides[normalize_lane_role(role)] = full

    return overrides, remaining


def resolve_with_lane(
    base: str,
    default_suffix: str,
    overrides: dict[str, str],
    services: list | None = None,
) -> str:
    """未在 overrides 中指定的服务，仍走 default_suffix（通常 deve）。"""
    keys = [base, normalize_lane_role(base)]
    alias = ROLE_ALIASES.get(base.lower())
    if alias:
        keys.append(alias)
    for key in keys:
        if key in overrides:
            return overrides[key]
    return resolve_dev_service(base, default_suffix, services)


def resolve_adapter_by_prefix(
    prefix: str,
    default_suffix: str,
    overrides: dict[str, str],
    domestic: bool = False,
) -> str:
    """底层 adapter：仅当用户指定了对应服务标签时才走特殊实例。"""
    lookup_prefix = prefix
    if prefix.startswith("otaAdapter"):
        lookup_prefix = "otaAdapter-domestic" if domestic else "otaAdapter"
    keys = ADAPTER_PREFIX_OVERRIDE_KEYS.get(lookup_prefix, (lookup_prefix,))
    for key in keys:
        if key in overrides:
            return overrides[key]
    return _adapter_prefix_to_dev_service(lookup_prefix, default_suffix)


def normalize_ota_tag(tag: str | None) -> str | None:
    """兼容旧 --ota-tag，等价于 --lane ota=ztC。"""
    if not tag:
        return None
    t = tag.strip()
    if t.lower().startswith("ota_"):
        t = t[4:]
    return t or None


def extract_dev_suffix(text: str, override: str | None = None) -> str:
    """从 traceId 提取 DEV 环境后缀，如 dev_web_b2b-deve_snake-xxx → deve。"""
    if override:
        return override.lower()
    m = DEV_SUFFIX_PATTERN.search(text)
    if m:
        return m.group(1).lower()
    return "deve"


def infer_purchaser(text: str) -> str | None:
    """从 traceId 推断采购侧服务基名（不含环境后缀）。"""
    t = text.lower()
    if "web_export" in t:
        return "export"
    if "web_b2b" in t:
        return "b2b"
    if text.startswith("web_export_"):
        return "export"
    if text.startswith("web_b2b_"):
        return "b2b"
    return None


def _service_values(services: list) -> set[str]:
    return {s.get("value", "") for s in services}


def resolve_dev_service(base: str, suffix: str, services: list | None = None) -> str:
    """将基名解析为 DEV 实际服务名，如 b2b + deve → b2b_deve。"""
    if not base:
        return base
    if base.endswith(f"_{suffix}") or base.endswith(f"-{suffix}"):
        return base
    candidate = f"{base}_{suffix}"
    if services:
        values = _service_values(services)
        if candidate in values:
            return candidate
        matched = match_services(base, services)["matched"]
        for v in matched:
            if v.endswith(f"_{suffix}"):
                return v
        if matched:
            return matched[0]
    return candidate


def resolve_adapter_api_services(suffix: str, services: list | None = None) -> list[str]:
    """DEV 默认供应入口：adapter_api_{suffix}，默认 adapter_api_deve（不 fallback 到其他实例）。"""
    return [f"adapter_api_{suffix}"]


def _lane_suffix_from_prefixed_service(service: str, prefix: str) -> str | None:
    if service.startswith(f"{prefix}_"):
        return service[len(prefix) + 1 :]
    return None


def resolve_platform_services(suffix: str, services: list | None = None) -> list[str]:
    """DEV 平台侧：agg + adapter_route（无 deal 分层）。"""
    agg = resolve_dev_service("agg", suffix, services)
    adapter_route = resolve_dev_service("adapter_route", suffix, services)
    return [agg, adapter_route]


def build_trace_services(
    text: str,
    with_order: bool = False,
    extra: list | None = None,
    dev_suffix: str | None = None,
    lane: list | None = None,
    ota_tag: str | None = None,
) -> dict:
    """构建 DEV 交易场景第一轮并行搜索的服务列表。"""
    all_services = load_services()
    suffix = extract_dev_suffix(text, dev_suffix)

    lane_args = list(lane or [])
    normalized_ota = normalize_ota_tag(ota_tag)
    if normalized_ota:
        lane_args.append(f"ota={normalized_ota}")

    overrides, extra = parse_lane_overrides(lane_args, extra, suffix)

    purchaser_base = infer_purchaser(text)
    purchaser_svc = (
        resolve_with_lane(purchaser_base, suffix, overrides, all_services)
        if purchaser_base else None
    )

    services: list[str] = []
    if purchaser_svc:
        services.append(purchaser_svc)

    if "agg" in overrides:
        agg_svc = overrides["agg"]
        services.append(agg_svc)
        lane = _lane_suffix_from_prefixed_service(agg_svc, "agg") or suffix
        adapter_route = overrides.get("adapter_route") or resolve_with_lane(
            "adapter_route", lane, overrides, all_services
        )
        if adapter_route not in services:
            services.append(adapter_route)
    else:
        services.extend(resolve_platform_services(suffix, all_services))

    if "adapter_api" in overrides:
        services.append(overrides["adapter_api"])
    else:
        services.extend(resolve_adapter_api_services(suffix, all_services))

    if with_order:
        order_svc = resolve_with_lane("order", suffix, overrides, all_services)
        if order_svc not in services:
            services.append(order_svc)

    for s in extra:
        if s not in services:
            services.append(s)

    # 去重保序
    seen = set()
    deduped = []
    for s in services:
        if s not in seen:
            seen.add(s)
            deduped.append(s)

    return {
        "devSuffix": suffix,
        "laneOverrides": overrides,
        "purchaser": purchaser_base,
        "purchaserService": purchaser_svc,
        "services": deduped,
        "withOrder": with_order,
    }


def is_meaningful_hit(results) -> bool:
    """排除 devtool 空结果 / NPE 字符串误报。"""
    if not results:
        return False
    if isinstance(results, str):
        bad = ("java.lang.NullPointerException", "搜索服务为空", "搜索结果为空")
        return results.strip() not in bad and len(results.strip()) > 20
    if isinstance(results, list):
        return len(results) > 0
    return True


def quote_search_text(text: str) -> str:
    if not (text.startswith('"') and text.endswith('"')):
        return f'"{text}"'
    return text


def resolve_search_time(text: str, start_date: str | None) -> tuple[str | None, dict | None]:
    if start_date:
        return start_date, None
    parsed = parse_time(text)
    if parsed["startDate"]:
        return parsed["startDate"], parsed
    return None, None


def run_search(cfg, *, execute_id: str, text: str, services: list, option: str = "",
               pipeline: str = "", start_date: str | None = None, end_date: str | None = None) -> list:
    body = {
        "text": quote_search_text(text),
        "option": option or "",
        "pipelineHandle": pipeline or "",
        "service": services,
        "startDate": start_date or None,
        "endDate": end_date or None,
        "concurrentSearch": True,
        "executeId": execute_id,
        "executeTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    if cfg.get("sshToken"):
        body["sshToken"] = cfg["sshToken"]
    return post(cfg, "/sse/syncSearchLog", body, timeout=300)


def search_one_service(cfg, execute_id: str, text: str, service: str, option: str,
                       start_date: str | None, end_date: str | None) -> dict:
    try:
        results = run_search(
            cfg,
            execute_id=execute_id,
            text=text,
            services=[service],
            option=option,
            start_date=start_date,
            end_date=end_date,
        )
        return {"service": service, "results": results, "error": None}
    except Exception as e:
        return {"service": service, "results": [], "error": str(e)}


def parallel_search_services(cfg, execute_id: str, text: str, services: list, option: str,
                             start_date: str | None, end_date: str | None,
                             max_workers: int = 5) -> dict:
    """按服务并行发起多次 search，共享同一 executeId。"""
    workers = min(max(len(services), 1), max_workers)
    out = {"executeId": execute_id, "services": {}}
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {
            pool.submit(search_one_service, cfg, execute_id, text, svc, option, start_date, end_date): svc
            for svc in services
        }
        for fut in as_completed(futures):
            item = fut.result()
            out["services"][item["service"]] = {
                "results": item["results"],
                "error": item["error"],
                "hit": is_meaningful_hit(item["results"]),
            }
    return out


# ── search ────────────────────────────────────────────────────────────────────

def cmd_search(args):
    cfg = load_config()
    execute_id = args.execute_id or str(uuid.uuid4())

    start_date, parsed = resolve_search_time(args.text, args.start_date)
    if parsed:
        print(f"自动解析时间：logTime={parsed['logTime']}，startDate={start_date}（{parsed['parsedFrom']}）",
              file=sys.stderr)

    body_services = args.service
    print(f"开始同步搜索，executeId={execute_id}，服务={body_services}，超时 300s...", file=sys.stderr)

    try:
        results = run_search(
            cfg,
            execute_id=execute_id,
            text=args.text,
            services=body_services,
            option=args.option or "",
            pipeline=args.pipeline or "",
            start_date=start_date,
            end_date=args.end_date,
        )
    except Exception as e:
        print(f"ERROR: 搜索失败: {e}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(results, ensure_ascii=False, indent=2))


def cmd_search_batch(args):
    """并行搜索多个服务，每个服务独立请求，共享 executeId。"""
    cfg = load_config()
    execute_id = args.execute_id or str(uuid.uuid4())
    start_date, parsed = resolve_search_time(args.text, args.start_date)
    if parsed:
        print(f"自动解析时间：logTime={parsed['logTime']}，startDate={start_date}（{parsed['parsedFrom']}）",
              file=sys.stderr)

    services = args.service
    print(f"并行搜索 {len(services)} 个服务：{services}，executeId={execute_id}，超时 300s/服务...",
          file=sys.stderr)

    result = parallel_search_services(
        cfg, execute_id, args.text, services,
        option=args.option or "",
        start_date=start_date,
        end_date=args.end_date or None,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_trace_search(args):
    """交易场景第一轮：按 traceId 推断 DEV 服务并并行搜索。"""
    cfg = load_config()
    execute_id = args.execute_id or str(uuid.uuid4())
    plan = build_trace_services(
        args.text,
        with_order=args.with_order,
        extra=args.supplier or [],
        dev_suffix=args.dev_suffix,
        lane=args.lane or [],
        ota_tag=args.ota_tag,
    )
    services = plan["services"]

    if not plan["purchaser"]:
        print("WARN: 无法从 traceId 推断采购侧服务，将搜索平台侧 + adapter_api", file=sys.stderr)
    else:
        print(
            f"DEV 环境后缀={plan['devSuffix']}，采购侧={plan['purchaserService']}",
            file=sys.stderr,
        )

    start_date, parsed = resolve_search_time(args.text, args.start_date)
    if parsed:
        print(f"自动解析时间：logTime={parsed['logTime']}，startDate={start_date}（{parsed['parsedFrom']}）",
              file=sys.stderr)

    print(f"交易链路并行搜索：{services}，executeId={execute_id}", file=sys.stderr)
    search_result = parallel_search_services(
        cfg, execute_id, args.text, services,
        option=args.option or "",
        start_date=start_date,
        end_date=args.end_date or None,
    )
    output = {
        "plan": plan,
        "executeId": execute_id,
        "search": search_result["services"],
        "nextStep": (
            "读取 adapter_route / agg 日志中的 supplierChannel / 路由 Bean，"
            "用 infer-supplier 推断底层 adapter（如 ndcAdapter_deve）；"
            "若 adapter_route 失败或 supplierSearchRs 为空，必须 search-batch 继续查底层供应；"
            "供应底层 HTTP 问题须 download + extract-reqresp 输出 req/resp"
            if not args.supplier else None
        ),
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


# ── 供应侧推断 / 底层报文提取 ─────────────────────────────────────────────────

PLATFORM_SUPPLIER_SIGNALS = [
    "303200006", "3032", "301001033",
    "deal.verify result", "deal.order result",
    "ufo verify", "HttpClientService",
    "Post url=", "responseContent=",
    "舱位售罄", "无运价", "supplierChannel", "supplierCode=",
    "domesticDealService", "OtaBusinessService",
]


def _adapter_prefix_to_dev_service(prefix: str, suffix: str, gds: str | None = None) -> str:
    """将 adapter 前缀转为 DEV 服务名，如 ndcAdapter + deve → ndcAdapter_deve。"""
    if prefix == "amadeusAdapter" and gds and gds not in ("AMADEUS", "1A"):
        if "SABRE" in gds:
            prefix = "sabreAdapter"
    if prefix.startswith("otaAdapter-domestic"):
        return f"otaAdapter-domestic_{suffix}"
    return f"{prefix}_{suffix}"


def infer_supplier_from_text(
    text: str,
    dev_suffix: str | None = None,
    lane: list | None = None,
    ota_tag: str | None = None,
) -> dict:
    """从 adapter_route / agg 日志推断 DEV 底层 adapter 服务与触发信号。"""
    suffix = dev_suffix or extract_dev_suffix(text)
    lane_args = list(lane or [])
    normalized_ota = normalize_ota_tag(ota_tag)
    if normalized_ota:
        lane_args.append(f"ota={normalized_ota}")
    overrides, _ = parse_lane_overrides(lane_args, None, suffix)

    services: list[str] = []
    reasons: list[str] = []

    for bean, prefix in ROUTING_BEAN_TO_ADAPTER_PREFIX.items():
        if bean in text:
            domestic = "domestic" in prefix
            svc = resolve_adapter_by_prefix(prefix, suffix, overrides, domestic=domestic)
            if svc not in services:
                services.append(svc)
            reasons.append(f"路由 Bean: {bean} → {svc}")

    channel_match = re.search(r'"supplierChannel"\s*:\s*"(\w+)"', text, re.I)
    gds_match = re.search(r'"gdsType"\s*:\s*"([^"]+)"', text, re.I)
    supplier_code = re.search(r'"supplierCode"\s*:\s*"(\w+)"', text, re.I)
    if not supplier_code:
        supplier_code = re.search(r'supplierCode[=:]\s*"?(\w+)"?', text, re.I)

    channel = channel_match.group(1).upper() if channel_match else None
    gds = gds_match.group(1).upper() if gds_match else None

    if channel:
        prefix = CHANNEL_TO_ADAPTER_PREFIX.get(channel)
        if channel == "GDS" and gds in ("AMADEUS", "1A"):
            prefix = "amadeusAdapter"
        elif channel == "GDS" and gds and "SABRE" in gds:
            prefix = "sabreAdapter"
        if prefix:
            svc = resolve_adapter_by_prefix(
                prefix, suffix, overrides, domestic="domestic" in prefix
            )
            if svc not in services:
                services.append(svc)
            reasons.append(f"supplierChannel={channel}" + (f", gdsType={gds}" if gds else "") + f" → {svc}")

    else:
        api_svc = resolve_with_lane("adapter_api", suffix, overrides)
        if api_svc not in services:
            services.append(api_svc)
        reasons.append(f"DEV 默认供应入口: {api_svc}")

    if not services:
        fallback = [
            resolve_with_lane("adapter_api", suffix, overrides),
            _adapter_prefix_to_dev_service("apiAdapter", suffix),
        ]
        services.extend(fallback)
        reasons.append(f"无法从日志推断，兜底 {fallback}")

    # 去重保序
    seen = set()
    deduped = []
    for s in services:
        if s not in seen:
            seen.add(s)
            deduped.append(s)

    signals = [s for s in PLATFORM_SUPPLIER_SIGNALS if s.lower() in text.lower()]
    adapter_route_fail = any(
        k in text
        for k in (
            "supplierSearchRs is empty",
            "adapter search return failed",
            "contextSnapshot is null",
            "adapter search return supplierSearchRs is empty",
        )
    )
    need_dig = bool(signals) or adapter_route_fail or bool(deduped)

    return {
        "devSuffix": suffix,
        "laneOverrides": overrides,
        "supplierServices": deduped,
        "reasons": reasons,
        "supplierCode": supplier_code.group(1) if supplier_code else None,
        "supplierChannel": channel,
        "gdsType": gds,
        "platformSignals": signals,
        "adapterRouteFailed": adapter_route_fail,
        "needSupplierDig": need_dig,
    }


def _read_text_source(args) -> str:
    if args.file:
        path = Path(args.file)
        if not path.exists():
            print(f"ERROR: 文件不存在: {path}", file=sys.stderr)
            sys.exit(1)
        return path.read_text(encoding="utf-8", errors="replace")
    if args.text:
        return args.text
    print("ERROR: 必须提供 --file 或 --text", file=sys.stderr)
    sys.exit(1)


def cmd_infer_supplier(args):
    text = _read_text_source(args)
    result = infer_supplier_from_text(
        text,
        dev_suffix=args.dev_suffix,
        lane=args.lane or [],
        ota_tag=args.ota_tag,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


def _extract_json_after_marker(line: str, marker: str) -> str | None:
    idx = line.find(marker)
    if idx < 0:
        return None
    payload = line[idx + len(marker):].strip()
    if payload.startswith("="):
        payload = payload[1:].strip()
    if not payload:
        return None
    if payload[0] in "{[":
        return payload
    m = re.search(r'(\{.*\}|\[.*\])', payload)
    return m.group(1) if m else payload


def _extract_post_url(line: str) -> str | None:
    m = re.search(r'Post url=(.+?)(?:,\s*Request:|$)', line)
    if not m:
        return None
    raw = m.group(1).strip()
    http_m = re.search(r'(https?://[^\s,]+)', raw)
    return http_m.group(1) if http_m else raw


def _strip_xmdt(payload: str) -> str:
    """去掉 #XMDT#{ traceId=...}#XMDT# 包装，保留 JSON 正文。"""
    if "#XMDT#" not in payload:
        return payload.strip()
    parts = payload.split("#XMDT#")
    for part in reversed(parts):
        part = part.strip()
        if part.startswith("{") or part.startswith("["):
            return part
    return payload.strip()


def extract_reqresp_from_log(content: str, trace_hint: str = "") -> list[dict]:
    """从供应侧 download 日志中提取 HTTP 请求/响应。"""
    entries = []
    current = None

    def flush():
        nonlocal current
        if current and (current.get("url") or current.get("request") or current.get("response")):
            if current.get("request"):
                current["request"] = _strip_xmdt(current["request"])
            if current.get("response"):
                current["response"] = _strip_xmdt(current["response"])
            entries.append(current)
        current = None

    for line in content.splitlines():
        if trace_hint and trace_hint not in line:
            if not any(k in line for k in ("Post url=", "responseContent=", "ufo verify", "Request:")):
                continue

        if "Post url=" in line or "Post url =" in line:
            flush()
            current = {"url": _extract_post_url(line), "method": "POST", "request": None, "response": None, "rawLines": [line]}
            req = _extract_json_after_marker(line, "Request:")
            if req:
                current["request"] = req
            continue

        if current is None and ("ufo verify request" in line.lower()):
            flush()
            current = {"url": None, "method": None, "request": None, "response": None, "rawLines": [line]}
            req = _extract_json_after_marker(line, "ufo verify request is")
            if not req:
                req = _extract_json_after_marker(line, "ufo verify request")
            if req:
                current["request"] = req
            continue

        if "responseContent=" in line:
            if current is None:
                current = {"url": None, "method": None, "request": None, "response": None, "rawLines": []}
            resp = _extract_json_after_marker(line, "responseContent=")
            if resp:
                current["response"] = resp
            current["rawLines"].append(line)
            flush()
            continue

        if current is not None and "ufo verify response" in line.lower():
            resp = _extract_json_after_marker(line, "ufo verify response")
            if resp:
                current["response"] = resp
            current["rawLines"].append(line)
            flush()
            continue

        if current is not None:
            current["rawLines"].append(line)

    flush()
    return entries


def cmd_extract_reqresp(args):
    path = Path(args.file)
    if not path.exists():
        print(f"ERROR: 文件不存在: {path}", file=sys.stderr)
        sys.exit(1)
    content = path.read_text(encoding="utf-8", errors="replace")
    entries = extract_reqresp_from_log(content, trace_hint=args.trace or "")
    output = {
        "file": str(path),
        "traceHint": args.trace or None,
        "count": len(entries),
        "entries": entries,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


# ── download ──────────────────────────────────────────────────────────────────

def cleanup_old_files(max_age_days=7):
    """清理 CACHE_DIR 下超过指定天数的子目录（每次下载后调用，避免临时文件堆积）。"""
    if not CACHE_DIR.exists():
        return
    cutoff = time.time() - max_age_days * 86400
    removed = 0
    for entry in CACHE_DIR.iterdir():
        if entry.is_dir():
            try:
                if entry.stat().st_mtime < cutoff:
                    import shutil
                    shutil.rmtree(entry, ignore_errors=True)
                    removed += 1
            except Exception:
                pass
    if removed:
        print(f"已清理 {removed} 个超过 {max_age_days} 天的临时目录", file=sys.stderr)


def cmd_download(args):
    cfg = load_config()
    out_dir = CACHE_DIR / args.execute_id
    out_dir.mkdir(parents=True, exist_ok=True)

    safe_name = re.sub(r"[^a-zA-Z0-9\-_]", "_", args.service + "-" + args.server) + ".log"
    out_file = out_dir / safe_name

    path = f"/sse/downloadLog?executeId={args.execute_id}&service={args.service}&server={args.server}"
    print(f"下载日志文件：{path}", file=sys.stderr)

    try:
        data = get(cfg, path, timeout=120, stream=True)
        out_file.write_bytes(data)
        print(f"已保存至：{out_file}")
    except Exception as e:
        print(f"ERROR: 下载失败: {e}", file=sys.stderr)
        sys.exit(1)

    # 下载完成后清理超过一周的临时文件
    cleanup_old_files(max_age_days=7)


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="DEV 测试环境日志搜索工具")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # match（服务匹配，替代原来 services --keyword 的角色）
    p = sub.add_parser("match", help="根据关键词匹配服务，输出精确匹配或候选列表")
    p.add_argument("keyword")
    p.add_argument("--refresh", action="store_true")

    # services（查看完整列表）
    p = sub.add_parser("services", help="获取/查看服务列表")
    p.add_argument("--keyword", help="过滤关键字")
    p.add_argument("--refresh", action="store_true")

    # parse-time
    p = sub.add_parser("parse-time", help="从文本解析 CST 时间")
    p.add_argument("text")

    # search
    p = sub.add_parser("search", help="同步搜索日志，可一次传多个 --service（最多 5 个，超时 300s）")
    p.add_argument("--text", required=True)
    p.add_argument("--service", required=True, nargs="+")
    p.add_argument("--option", default="")
    p.add_argument("--pipeline", default="")
    p.add_argument("--start-date")
    p.add_argument("--end-date")
    p.add_argument("--execute-id")

    # search-batch（按服务并行，共享 executeId）
    p = sub.add_parser("search-batch", help="并行搜索多个服务（每个服务独立请求，共享 executeId）")
    p.add_argument("--text", required=True)
    p.add_argument("--service", required=True, nargs="+")
    p.add_argument("--option", default="")
    p.add_argument("--start-date")
    p.add_argument("--end-date")
    p.add_argument("--execute-id")

    # trace-search（交易场景第一轮并行）
    p = sub.add_parser("trace-search", help="交易场景：按 traceId 推断服务并并行搜索")
    p.add_argument("--text", required=True)
    p.add_argument("--with-order", action="store_true", help="生单/支付/申请出票时追加 order")
    p.add_argument("--supplier", nargs="*", help="额外服务或泳道标签，如 agg_zzr / ota_ztC / adapter_ota_ztC")
    p.add_argument("--lane", action="append", help="服务泳道覆盖，可重复，如 ota=ztC、agg=zzr；未指定的服务仍用 deve")
    p.add_argument("--ota-tag", help="兼容旧参数，等价 --lane ota=ztC")
    p.add_argument("--option", default="")
    p.add_argument("--start-date")
    p.add_argument("--end-date")
    p.add_argument("--execute-id")
    p.add_argument("--dev-suffix", help="DEV 环境后缀，默认从 traceId 解析（如 deve）")

    # infer-supplier（从 adapter_route 日志推断供应侧）
    p = sub.add_parser("infer-supplier", help="从 adapter_route / agg 日志推断 DEV 底层 adapter 服务")
    p.add_argument("--file", help="日志文件路径")
    p.add_argument("--text", help="日志文本（与 --file 二选一）")
    p.add_argument("--dev-suffix", help="DEV 环境后缀，默认从 traceId/日志解析（如 deve）")
    p.add_argument("--lane", action="append", help="服务泳道覆盖，可重复，如 ota=ztC、ndc=zzr；未指定的仍 deve")
    p.add_argument("--ota-tag", help="兼容旧参数，等价 --lane ota=ztC")

    # extract-reqresp（从供应侧日志提取 HTTP 请求/响应）
    p = sub.add_parser("extract-reqresp", help="从供应侧 download 日志提取底层 HTTP 请求/响应")
    p.add_argument("--file", required=True, help="供应侧日志文件路径")
    p.add_argument("--trace", default="", help="traceId 片段，用于过滤相关行")

    # download
    p = sub.add_parser("download", help="下载日志文件到本地")
    p.add_argument("--execute-id", required=True)
    p.add_argument("--service", required=True)
    p.add_argument("--server", required=True)

    args = parser.parse_args()
    {
        "match": cmd_match,
        "services": cmd_services,
        "parse-time": cmd_parse_time,
        "search": cmd_search,
        "search-batch": cmd_search_batch,
        "trace-search": cmd_trace_search,
        "infer-supplier": cmd_infer_supplier,
        "extract-reqresp": cmd_extract_reqresp,
        "download": cmd_download,
    }[args.cmd](args)


if __name__ == "__main__":
    main()
