"""amap.py — 高德地图 Web 服务 API 统一入口

覆盖高德 v3/v4 后端 HTTP 接口：地点搜索、POI 详情、周边搜索、路径规划
（步行/驾车/公交/骑行）、地理编码/逆编码、天气、IP 定位、行政区划、距离测量、
静态地图。所有调用走统一 .env 里的 AMAP_KEY（Web 服务类型）。

CLI（子命令均输出纯 JSON）：
  amap.py text        --keywords <词>      [--city 北京市] [--type 050000] [--offset 20]
  amap.py around      --location "lng,lat" [--radius 1000] [--type 050000]
  amap.py detail      --id <poi_id>
  amap.py route       <walking|driving|transit|bicycling>
                     --origin "lng,lat"    --destination "lng,lat"
                     [--city 010]          [--strategy 0]
  amap.py geocode     --address <结构化地址>        [--city 北京市]
  amap.py regeo       --location "lng,lat" [--extensions all]
  amap.py weather     --city <adcode>       [--extensions base|all]   # adcode 不是中文！
  amap.py ip          [--ip <ipv4>]
  amap.py district    [--keywords 北京市]  [--subdistrict 2]
  amap.py distance    --origins "lng,lat|lng,lat" --destination "lng,lat"
  amap.py staticmap   --location "lng,lat" --zoom 16 --size 600*400 [--markers ""] [--save path]

清华常用场景：
  amap.py text --keywords "清华大学第六教学楼"
  amap.py around --location "116.326,40.003" --radius 800 --type 050000   # 主楼附近餐饮
  amap.py route walking --origin "116.326,40.003" --destination "116.333,40.000"
  amap.py weather --city 110108                       # 清华所在海淀区
  amap.py geocode --address "北京市海淀区清华大学"
  amap.py staticmap --location "116.326,40.003" --zoom 16 --save tmp/map.png

KEY 获取：lbs.amap.com → 注册 → 控制台创建应用 → 添加 Web 服务 Key。
详细：见 SKILL.md 的"KEY 申请"章节。
"""
import sys
import os
import json
import time
import argparse
import urllib.parse
import urllib.request
import socket

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "shared", "scripts"))
import common

ENV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".env")
BASE = "https://restapi.amap.com"
TIMEOUT = 15  # 单次 HTTP 超时
USER_AGENT = "tsinghua-campus-skill/1.0"  # 高德不要求 mailto（是 OpenAlex 要求）


def _load_key():
    """从统一 .env 读取 AMAP_KEY。"""
    if not os.path.exists(ENV_PATH):
        common.output_json({"status": "error", "message": f"统一配置 {ENV_PATH} 不存在。请复制 .env.example 为 .env 并填写。", "needs": "env"})
        sys.exit(1)
    try:
        env = open(ENV_PATH, encoding="utf-8").read()
    except Exception as e:
        common.output_json({"status": "error", "message": f"读 .env 失败: {e}"})
        sys.exit(1)
    key = ""
    for line in env.splitlines():
        line = line.strip()
        if line.startswith("AMAP_KEY="):
            key = line.split("=", 1)[1].strip()
            break
    if not key:
        common.output_json({
            "status": "error",
            "message": "AMAP_KEY 未配置。",
            "how_to_get": "lbs.amap.com → 注册开发者 → 应用管理 → 创建新应用 → 添加 Key，服务平台选【Web 服务】（不是 Web 端/JS API）。免费版每日 5000 次个人调用额度。",
            "needs": "amap_key",
        })
        sys.exit(1)
    return key


def _http_get(path, params, key=None):
    """GET 调用高德 Web Service。返回 (status_code, json_body_or_text)。"""
    if key is None:
        key = _load_key()
    if "key" not in params:
        params["key"] = key
    params.setdefault("output", "JSON")
    qs = urllib.parse.urlencode(params)
    url = f"{BASE}{path}?{qs}"
    common.log(f"[amap] GET {path} {dict((k, v) for k, v in params.items() if k != 'key')}")
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            body = r.read().decode("utf-8", errors="replace")
            code = r.status
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace") if e.fp else ""
        code = e.code
    except (urllib.error.URLError, socket.timeout) as e:
        common.output_json({"status": "error", "error": "network", "message": f"网络失败: {e}", "url": url})
        sys.exit(1)
    try:
        data = json.loads(body)
    except Exception:
        common.output_json({"status": "error", "error": "parse", "message": "返回非 JSON", "body": body[:300], "code": code})
        sys.exit(1)
    if str(data.get("status")) != "1":
        msg = data.get("info", "未知错误") + f" (infocode={data.get('infocode')})"
        common.output_json({
            "status": "error",
            "error": "amap_api",
            "message": msg,
            "data": data,
            "hint": "常见原因：city 必须传 adcode 而非中文名；key 类型必须是 Web 服务；参数顺序",
        })
        sys.exit(1)
    return data


def _save_or_return(data, save_path=None, url_field=None):
    """如指定 save_path，把 data 里 url_field 对应 URL 下载到本地。"""
    if not save_path:
        return data
    if url_field and url_field in data:
        url = data[url_field]
        try:
            with urllib.request.urlopen(url, timeout=TIMEOUT) as r:
                with open(save_path, "wb") as f:
                    f.write(r.read())
            data["saved_to"] = save_path
        except Exception as e:
            data["save_error"] = str(e)
    return data


# ============ 子命令 ============

def cmd_text(args):
    """关键字搜索 POI。"""
    data = _http_get("/v3/place/text", {
        "keywords": args.keywords,
        "city": args.city or "",
        "types": args.type or "",
        "offset": str(args.offset),
        "page": str(args.page),
        "extensions": "base",
    })
    common.output_json({"status": "ok", "type": "text", "count": data.get("count"), "pois": data.get("pois", [])})


def cmd_around(args):
    """周边搜索（圆周内 POI）。返回 amap 原始数据 + 轻量过滤选项。

    过滤原则：脚本只做"数据维度"的朴素筛选，**不做业务判断**（如"这是不是清华食堂"由 AI 自行判定）。

    --type       amap POI 分类码（050000=餐饮 050500=咖啡 141201=高校 等）
    --name-contains  AI 自传关键词（如"清华"/"食堂"/"面馆"），仅做朴素子串匹配
    --exclude-name  AI 自传排除关键词
    --max-count   限制返回数量（避免 AI 一次性处理太多）
    """
    data = _http_get("/v3/place/around", {
        "location": args.location,
        "radius": str(args.radius),
        "types": args.type or "",
        "offset": str(args.offset),
        "page": str(args.page),
        "extensions": "base",
    })
    pois = data.get("pois", [])
    notes = []
    # 朴素子串过滤（AI 传词，自己决定怎么筛）
    if args.name_contains:
        keywords = [k.strip() for k in args.name_contains.split(",") if k.strip()]
        before = len(pois)
        pois = [p for p in pois if any(k in p.get("name", "") for k in keywords)]
        notes.append(f"name_contains={keywords}: {before}→{len(pois)}")
    if args.exclude_name:
        keywords = [k.strip() for k in args.exclude_name.split(",") if k.strip()]
        before = len(pois)
        pois = [p for p in pois if not any(k in p.get("name", "") for k in keywords)]
        notes.append(f"exclude_name={keywords}: {before}→{len(pois)}")
    if args.max_count and len(pois) > args.max_count:
        notes.append(f"max_count 截断: {len(pois)}→{args.max_count}")
        pois = pois[: args.max_count]
    common.output_json({
        "status": "ok",
        "type": "around",
        "query": {
            "location": args.location,
            "radius_m": args.radius,
            "type_filter": args.type or None,
            "name_contains": args.name_contains or None,
            "exclude_name": args.exclude_name or None,
            "max_count": args.max_count,
        },
        "total_before_filter": data.get("count"),
        "total_after_filter": len(pois),
        "filter_notes": notes,
        "hint_to_ai": "POI 含 name/type/typecode/keytag/address/location；由你决定哪个是清华食堂（建议用 campus-dining 拿官方清单 + 比对）",
        "pois": pois,
    })


def cmd_detail(args):
    """POI ID 查详情。"""
    data = _http_get("/v3/place/detail", {"id": args.id, "extensions": "all"})
    common.output_json({"status": "ok", "type": "detail", "pois": data.get("pois", [])})


# ============ 清华数据快照（本地只读）============
# 路径：amap/data/tsinghua_canteens.json
# 注意：本快照仅供 AI 查询，**不参与召回过滤**。
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
CANTEENS_FILE = os.path.join(DATA_DIR, "tsinghua_canteens.json")
ORGS_FILE = os.path.join(DATA_DIR, "tsinghua_orgs.json")
BUILDINGS_FILE = os.path.join(DATA_DIR, "tsinghua_buildings.json")


def _load_snapshot(filename, kind_label):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        common.output_json({"status": "error", "error": "no_snapshot", "message": f"快照缺失: {path}"})
        sys.exit(1)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _haversine_m(lng1, lat1, lng2, lat2):
    """两点球面距离（米）。"""
    from math import radians, sin, cos, asin, sqrt
    R = 6371000
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
    a = sin((lat2 -lat1) / 2) ** 2 + cos(lat1) * cos(lat2) * sin((lng2 -lng1) / 2) ** 2
    return 2 * R * asin(sqrt(a))


def cmd_campus_dining(args):
    """清华食堂数据查询（只读本地快照）。

    本命令**不**做召回过滤——只把清华官方食堂清单（学生食堂 + 教工餐厅 + 特色餐厅）
    交给 AI；由 AI 决定如何与 amap POI 比对、按距离排序、组合回答。

    用法：
      campus-dining                              → 列全部清华食堂（带官方名/坐标/电话/简介）
      campus-dining --category 学生食堂         → 只列学生食堂
      campus-dining --near "lng,lat" --radius 800 → 附距离（按距离排序），AI 自己截断
    """
    snap = _load_snapshot("tsinghua_canteens.json", "食堂")
    canteens = snap.get("canteens", [])
    if args.category:
        canteens = [c for c in canteens if c["category"] == args.category]
    # 附距离（仅 --near 时）
    if args.near:
        try:
            lng, lat = map(float, args.near.split(","))
        except ValueError:
            common.output_json({"status": "error", "message": "--near 格式: 'lng,lat'"})
            sys.exit(1)
        radius = args.radius or 1500
        enriched = []
        for c in canteens:
            if not c.get("location"):
                enriched.append({**c, "distance_m": None})
                continue
            clng, clat = map(float, c["location"].split(","))
            d = _haversine_m(lng, lat, clng, clat)
            enriched.append({**c, "distance_m": int(d)})
        enriched.sort(key=lambda x: (x.get("distance_m") is None, x.get("distance_m") or 0))
        canteens = enriched
    by_cat = {}
    for c in canteens:
        by_cat[c["category"]] = by_cat.get(c["category"], 0) + 1
    common.output_json({
        "status": "ok",
        "type": "campus_dining",
        "snapshot_date": snap.get("snapshot_date"),
        "snapshot_source": snap.get("snapshot_source"),
        "data_expiry_hint": snap.get("data_expiry_hint"),
        "query_center": args.near,
        "radius_m": args.radius if args.near else None,
        "category_filter": args.category,
        "category_counts": by_cat,
        "total": len(canteens),
        "canteens": canteens,
        "hint_to_ai": "本快照是清华官方饮食服务中心数据；与 amap around 结果比对，自己决定哪些是用户要的食堂",
    })


def cmd_campus_orgs(args):
    """清华机构数据查询（院系/系/研究院/书院/中心/实验室）。只读快照。

    用法：
      campus-orgs                                      → 列全部清华机构
      campus-orgs --category 学院|系|研究院|书院|中心|实验室|其他|非实体学院
      campus-orgs --name-contains "AI"                → AI 自传关键词朴素子串匹配
      campus-orgs --limit 5                            → AI 限制返回前 N 条
    """
    snap = _load_snapshot("tsinghua_orgs.json", "机构")
    orgs = snap.get("institutions", [])
    if args.category:
        orgs = [o for o in orgs if o["type"] == args.category]
    if args.name_contains:
        keywords = [k.strip() for k in args.name_contains.split(",") if k.strip()]
        orgs = [o for o in orgs if any(k in o["name"] for k in keywords)]
    if args.limit and len(orgs) > args.limit:
        orgs = orgs[: args.limit]
    by_type = {}
    for o in orgs:
        by_type[o["type"]] = by_type.get(o["type"], 0) + 1
    common.output_json({
        "status": "ok",
        "type": "campus_orgs",
        "snapshot_date": snap.get("snapshot_date"),
        "snapshot_source": snap.get("snapshot_source"),
        "data_expiry_hint": snap.get("data_expiry_hint"),
        "filters": {"category": args.category or None, "name_contains": args.name_contains or None, "limit": args.limit},
        "type_counts": by_type,
        "total": len(orgs),
        "institutions": orgs,
        "hint_to_ai": "本快照是清华官方院系设置；URL 可直接访问获取更多介绍；坐标由 AI 自行用 amap text 拿",
    })


def cmd_campus_buildings(args):
    """清华校内建筑 + 周边建筑查询（只读本地快照）。

    用法：
      campus-buildings                                → 列全部（校内+周边）
      campus-buildings --scope campus                 → 只校内
      campus-buildings --scope surrounding            → 只周边
      campus-buildings --category 四大建筑|教学楼|...  → 按 category 过滤
      campus-buildings --name-contains "图书馆"        → AI 自传关键词
    """
    snap = _load_snapshot("tsinghua_buildings.json", "建筑")
    campus = snap.get("campus_buildings", [])
    surrounding = snap.get("surrounding_buildings", [])
    if args.scope == "campus":
        items = [{"scope": "campus", **b} for b in campus]
    elif args.scope == "surrounding":
        items = [{"scope": "surrounding", **b} for b in surrounding]
    else:
        items = [{"scope": "campus", **b} for b in campus] + [{"scope": "surrounding", **b} for b in surrounding]
    if args.category:
        items = [b for b in items if b.get("category") == args.category]
    if args.name_contains:
        keywords = [k.strip() for k in args.name_contains.split(",") if k.strip()]
        items = [b for b in items if any(k in b.get("name", "") or k in b.get("use", "") for k in keywords)]
    by_scope = {}
    for b in items:
        by_scope.setdefault(b["scope"], {}).__setitem__(b.get("category", "未知"), 0)
    common.output_json({
        "status": "ok",
        "type": "campus_buildings",
        "snapshot_date": snap.get("snapshot_date"),
        "snapshot_source": snap.get("snapshot_source"),
        "data_expiry_hint": snap.get("data_expiry_hint"),
        "filters": {"scope": args.scope or "all", "category": args.category or None, "name_contains": args.name_contains or None},
        "scope_counts": {"campus": len(campus), "surrounding": len(surrounding)},
        "total": len(items),
        "buildings": items,
        "hint_to_ai": "建筑无坐标字段（官方页通常不给坐标）；需坐标时 AI 自行用 amap text 搜名称补全",
    })


def cmd_route(args):
    """路径规划（4 种 mode 走不同 endpoint）。"""
    if args.mode == "walking":
        path = "/v3/direction/walking"
    elif args.mode == "driving":
        path = "/v3/direction/driving"
    elif args.mode == "transit":
        path = "/v3/direction/transit/integrated"
    elif args.mode == "bicycling":
        path = "/v4/direction/bicycling"
    else:
        common.output_json({"status": "error", "message": f"未知 mode: {args.mode}"})
        sys.exit(1)
    params = {"origin": args.origin, "destination": args.destination}
    if args.city:
        params["city"] = args.city
    if args.strategy:
        params["strategy"] = str(args.strategy)
    data = _http_get(path, params)
    # 提取主要信息（distance/duration + polyline）
    out = {"status": "ok", "type": "route", "mode": args.mode, "route": data.get("route", {})}
    paths = (data.get("route") or {}).get("paths") or (data.get("route") or {}).get("transits")
    if paths:
        out["paths_count"] = len(paths)
    common.output_json(out)


def cmd_geocode(args):
    """地址→坐标（地理编码）。"""
    data = _http_get("/v3/geocode/geo", {
        "address": args.address,
        "city": args.city or "",
    })
    common.output_json({"status": "ok", "type": "geocode", "count": data.get("count"), "geocodes": data.get("geocodes", [])})


def cmd_regeo(args):
    """坐标→地址（逆地理）。"""
    data = _http_get("/v3/geocode/rego", {
        "location": args.location,
        "extensions": args.extensions,
        "radius": str(args.radius),
    })
    common.output_json({"status": "ok", "type": "regeo", "regeocode": data.get("regeocode", {})})


def cmd_weather(args):
    """天气查询（city 必须传 adcode，如北京 110000、海淀 110108）。"""
    data = _http_get("/v3/weather/weatherInfo", {
        "city": args.city,
        "extensions": args.extensions,
    })
    if args.extensions == "all":
        common.output_json({"status": "ok", "type": "weather_forecast", "data": data.get("forecasts", [{}])[0] if data.get("forecasts") else data})
    else:
        common.output_json({"status": "ok", "type": "weather_live", "data": data.get("lives", [{}])[0] if data.get("lives") else data})


def cmd_ip(args):
    """IP 定位（仅国内 IPv4）。"""
    params = {}
    if args.ip:
        params["ip"] = args.ip
    data = _http_get("/v3/ip", params)
    common.output_json({"status": "ok", "type": "ip", "data": data.get("province") and data or data})


def cmd_district(args):
    """行政区划（全国/省/市/区）。"""
    data = _http_get("/v3/config/district", {
        "keywords": args.keywords or "",
        "subdistrict": str(args.subdistrict),
        "extensions": "base",
    })
    common.output_json({"status": "ok", "type": "district", "districts": data.get("districts", [])})


def cmd_distance(args):
    """测量两点/多点之间的距离（type=1:距离 2:驾车 3:步行）。"""
    data = _http_get("/v3/distance", {
        "origins": args.origins,
        "destination": args.destination,
        "type": str(args.type),
    })
    common.output_json({"status": "ok", "type": "distance", "results": data.get("results", [])})


def cmd_staticmap(args):
    """静态地图（返回 URL，可选保存到本地）。"""
    params = {
        "location": args.location,
        "zoom": str(args.zoom),
        "size": args.size,
    }
    if args.markers:
        params["markers"] = args.markers
    if args.labels:
        params["labels"] = args.labels
    if args.paths:
        params["paths"] = args.paths
    # staticmap 返回图片（PNG），不是 JSON
    key = _load_key()
    params["key"] = key
    qs = urllib.parse.urlencode(params)
    url = f"{BASE}/v3/staticmap?{qs}"
    if not args.save:
        # 仅返回 URL
        common.output_json({"status": "ok", "type": "staticmap_url", "url": url, "hint": "用 --save path.png 直接保存到本地"})
        return
    try:
        with urllib.request.urlopen(url, timeout=TIMEOUT) as r:
            body = r.read()
        if body[:8] == b"\x89PNG\r\n\x1a\n" or body[:3] == b"\xff\xd8\xff":
            with open(args.save, "wb") as f:
                f.write(body)
            common.output_json({"status": "ok", "type": "staticmap", "saved_to": os.path.abspath(args.save), "bytes": len(body)})
        else:
            # 可能是错误 JSON
            try:
                err = json.loads(body.decode("utf-8", errors="replace"))
                common.output_json({"status": "error", "error": "amap_api", "data": err})
                sys.exit(1)
            except Exception:
                common.output_json({"status": "error", "error": "unknown", "body": body[:300]})
                sys.exit(1)
    except Exception as e:
        common.output_json({"status": "error", "error": "fetch", "message": str(e)})
        sys.exit(1)


# ============ 入口 ============

def main():
    ap = argparse.ArgumentParser(description="高德地图 Web 服务 API 统一入口（查询、周边、路径、天气、地理编码等）")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("text", help="关键字搜索 POI（例：清华大学第六教学楼）")
    p.add_argument("--keywords", required=True)
    p.add_argument("--city", default="", help="城市名或 adcode（清华常用 110000/北京市）")
    p.add_argument("--type", default="", help="POI 分类码（餐饮 050000、教育 141201 等）")
    p.add_argument("--offset", type=int, default=20)
    p.add_argument("--page", type=int, default=1)
    p.set_defaults(func=cmd_text)

    p = sub.add_parser("around", help="周边搜索（清华校内找餐饮、便利店）")
    p.add_argument("--location", required=True, help="中心坐标 lng,lat")
    p.add_argument("--radius", type=int, default=1000, help="半径米（默认 1000）")
    p.add_argument("--type", default="", help="amap POI 分类码（餐饮 050000/咖啡 050500 等）")
    p.add_argument("--name-contains", default="", help="逗号分隔多个关键词，只保留 name 含任一关键词的 POI")
    p.add_argument("--exclude-name", default="", help="逗号分隔多个排除关键词")
    p.add_argument("--max-count", type=int, default=0, help="限制返回数量（0=不限制）")
    p.add_argument("--offset", type=int, default=20)
    p.add_argument("--page", type=int, default=1)
    p.set_defaults(func=cmd_around)

    p = sub.add_parser("detail", help="POI 详情")
    p.add_argument("--id", required=True)
    p.set_defaults(func=cmd_detail)

    p = sub.add_parser("route", help="路径规划")
    p.add_argument("mode", choices=["walking", "driving", "transit", "bicycling"])
    p.add_argument("--origin", required=True, help="起点 lng,lat")
    p.add_argument("--destination", required=True, help="终点 lng,lat")
    p.add_argument("--city", default="", help="adcode 或 citycode（transit 必填）")
    p.add_argument("--strategy", type=int, default=0, help="0-推荐/1-最快/2-最少换乘/...")
    p.set_defaults(func=cmd_route)

    p = sub.add_parser("geocode", help="地址→坐标")
    p.add_argument("--address", required=True)
    p.add_argument("--city", default="")
    p.set_defaults(func=cmd_geocode)

    p = sub.add_parser("regeo", help="坐标→地址")
    p.add_argument("--location", required=True)
    p.add_argument("--extensions", default="base", choices=["base", "all"])
    p.add_argument("--radius", type=int, default=1000)
    p.set_defaults(func=cmd_regeo)

    p = sub.add_parser("weather", help="天气（city 必须是 adcode，如 110000）")
    p.add_argument("--city", required=True, help="adcode（不是中文名）")
    p.add_argument("--extensions", default="base", choices=["base", "all"], help="base=实况，all=预报")
    p.set_defaults(func=cmd_weather)

    p = sub.add_parser("ip", help="IP 定位（仅国内 IPv4）")
    p.add_argument("--ip", default="")
    p.set_defaults(func=cmd_ip)

    p = sub.add_parser("district", help="行政区划")
    p.add_argument("--keywords", default="")
    p.add_argument("--subdistrict", type=int, default=2)
    p.set_defaults(func=cmd_district)

    p = sub.add_parser("distance", help="距离测量")
    p.add_argument("--origins", required=True, help="多点用 | 分隔")
    p.add_argument("--destination", required=True)
    p.add_argument("--type", type=int, default=1, choices=[1, 2, 3])
    p.set_defaults(func=cmd_distance)

    p = sub.add_parser("staticmap", help="静态地图（PNG）")
    p.add_argument("--location", required=True)
    p.add_argument("--zoom", type=int, default=15)
    p.add_argument("--size", default="600*400")
    p.add_argument("--markers", default="", help="标注点")
    p.add_argument("--labels", default="")
    p.add_argument("--paths", default="")
    p.add_argument("--save", default="", help="保存到本地 PNG 路径")
    p.set_defaults(func=cmd_staticmap)

    p = sub.add_parser("campus-dining", help="清华食堂数据查询（基于本地快照 data/tsinghua_canteens.json）")
    p.add_argument("--category", default="", choices=["学生食堂", "教工餐厅", "特色餐厅"],
                   help="按类别过滤（清华饮食服务中心官方三类）")
    p.add_argument("--near", default="", help="中心坐标 lng,lat；与 --radius 一起按距离过滤")
    p.add_argument("--radius", type=int, default=1500, help="附近半径米（默认 1500）")
    p.add_argument("--refresh", action="store_true", help="（占位）从清华官方页重新爬数据并更新快照")
    p.set_defaults(func=cmd_campus_dining)

    p = sub.add_parser("campus-orgs", help="清华机构数据查询（院系/系/研究院/书院/中心/实验室，本地快照）")
    p.add_argument("--category", default="", help="按 type 过滤（学院/系/研究院/书院/中心/实验室/其他/非实体学院）")
    p.add_argument("--name-contains", default="", help="逗号分隔多个关键词，朴素子串匹配")
    p.add_argument("--limit", type=int, default=0, help="限制返回前 N 条（0=不限制）")
    p.set_defaults(func=cmd_campus_orgs)

    p = sub.add_parser("campus-buildings", help="清华校内建筑 + 周边建筑查询（本地快照）")
    p.add_argument("--scope", default="", choices=["campus", "surrounding"],
                   help="范围：campus=校内 only / surrounding=周边 only / 不传=全部")
    p.add_argument("--category", default="", help="按 category 过滤（四大建筑/校园核心/教学楼/历史建筑/景观/周边园区/写字楼/...）")
    p.add_argument("--name-contains", default="", help="逗号分隔多个关键词，朴素子串匹配 name/use")
    p.set_defaults(func=cmd_campus_buildings)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:
        common.log(f"[amap] 未捕获异常: {e}")
        common.output_json({"status": "error", "error": "unexpected", "message": f"脚本异常: {str(e)[:200]}"})
        sys.exit(1)
