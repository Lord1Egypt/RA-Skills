"""Shared request identity, live pricing, and envelope validation."""
import json
import hashlib
import os
import tempfile
from pathlib import Path
import urllib.parse
import urllib.request

IDENTITY = json.loads(Path(__file__).with_name("client_identity.json").read_text(encoding="utf-8"))
USER_AGENT = "{slug}/{version} (source={channel})".format(**IDENTITY)


def identity_headers():
    return {"User-Agent": USER_AGENT, "X-WM-Source": IDENTITY["slug"],
            "X-Source": IDENTITY["channel"]}


def product_path(product):
    path = product.get("publicPath", "/")
    if path.startswith("/openapi/"):
        return path.rstrip("/")
    return ("/openapi/" + product["slug"] + "/" + path.lstrip("/")).rstrip("/")


def failure(payload):
    """Only walk protocol envelopes, never arbitrary application data."""
    current = payload
    for _ in range(5):
        if not isinstance(current, dict):
            return ""
        code = current.get("code")
        status = current.get("statusCode", 200)
        if current.get("ok") is False or code not in (None, "", "OK", "ok", 0, 200) or (isinstance(status, int) and status >= 400):
            detail = current.get("body") if isinstance(current.get("body"), dict) else current
            return "{}: {} (requestId={})".format(detail.get("code", code or status),
                detail.get("message", "API request failed"), detail.get("requestId", current.get("requestId", "")))
        if "statusCode" in current and "body" in current:
            current = current["body"]
        elif isinstance(current.get("data"), dict) and any(k in current["data"] for k in ("code", "statusCode", "ok")):
            current = current["data"]
        else:
            return ""
    return ""


def catalog(root, api_key=""):
    path = "/api/v1/products" if api_key else "/api/v1/public/products"
    headers = {**identity_headers(), "Accept": "application/json"}
    if api_key:
        headers["X-API-Key"] = api_key
    items = []
    for page in range(1, 101):
        req = urllib.request.Request(root.rstrip("/") + path + "?pageSize=100&page=" + str(page), headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            payload = json.load(response)
        error = failure(payload)
        if error:
            raise ValueError(error)
        data = payload.get("data", {})
        batch = data.get("items")
        if not isinstance(batch, list):
            raise ValueError("Invalid product catalog")
        items.extend(batch)
        total = (data.get("pagination") or {}).get("total", data.get("total"))
        if len(batch) < 100 or (isinstance(total, int) and len(items) >= total):
            return items
    raise ValueError("Product catalog pagination did not terminate")


def price_micros(product, params):
    params = dict(params)
    adjustment = 0
    quantity = 1
    for definition in product.get("parameters") or []:
        name = definition["name"]
        if name not in params and definition.get("default") not in (None, ""):
            params[name] = definition["default"]
        if name not in params:
            continue
        value = params[name]
        if definition.get("billByQuantity") or definition.get("unitPriceMicros", 0) > 0:
            if not isinstance(value, list) or not value:
                raise ValueError("Billing quantity must be a nonempty list: " + name)
            quantity = len(value)
        text = str(value).lower() if isinstance(value, bool) else str(value)
        adjustment = max(adjustment, (definition.get("valuePriceAdjustmentsBps") or {}).get(text, 0))
        if isinstance(value, str):
            url = urllib.parse.urlparse(value)
            short = ((url.hostname == "mp.weixin.qq.com" and url.path.startswith("/s/")) or
                     (url.hostname in ("weixin.qq.com", "www.weixin.qq.com") and url.path.startswith("/sph/")))
            if short:
                adjustment = max(adjustment, definition.get("shortLinkPriceAdjustmentBps", 0))
    for group in product.get("parameterGroups") or []:
        for name in group.get("parameters", []):
            if name in params:
                adjustment = max(adjustment, (group.get("priceAdjustmentsBps") or {}).get(name, 0))
    return int(product["priceMicros"]) * quantity * (10000 + adjustment) // 10000


def snapshot(path, scope, data):
    """Compare only complete, same-scope results and replace atomically."""
    scope_hash = hashlib.sha256(json.dumps(scope, sort_keys=True).encode()).hexdigest()
    target = Path(path)
    previous = json.loads(target.read_text(encoding="utf-8")) if target.exists() else None
    if previous and previous.get("scope") != scope_hash:
        raise ValueError("快照对应其他账号、端点或筛选条件，请换一个快照路径")
    def indexed(value):
        rows = value if isinstance(value, list) else next((value[k] for k in ("items", "accounts", "list", "records", "results", "videos") if isinstance(value, dict) and isinstance(value.get(k), list)), [value])
        result = {}
        for row in rows:
            key = next((str(row[k]) for k in ("objectId", "articleId", "id", "url", "accountId") if isinstance(row, dict) and row.get(k)), json.dumps(row, sort_keys=True, ensure_ascii=False))
            result[key] = row
        return result
    current = indexed(data)
    old = indexed(previous["data"]) if previous else {}
    partial = isinstance(data, dict) and data.get("partial")
    diff = {"baseline": previous is None, "new": len(current.keys() - old.keys()),
            "changed": sum(current[k] != old[k] for k in current.keys() & old.keys()),
            "notReturned": len(old.keys() - current.keys()), "partial": bool(partial)}
    if not partial:
        target.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=target.parent, delete=False) as f:
            json.dump({"scope": scope_hash, "data": data}, f, ensure_ascii=False)
            temporary = f.name
        os.replace(temporary, target)
    return diff


def estimate_plan(plan, root="https://api.we-media.cn", api_key=""):
    products = {product_path(p): p for p in catalog(root, api_key)}
    items = []
    for call in plan:
        path = call["path"].rstrip("/")
        count = int(call.get("count", 1))
        if count < 1:
            raise ValueError("Call count must be positive")
        unit = price_micros(products[path], call.get("params", {}))
        items.append({"path": path, "count": count, "unitMicros": unit, "totalMicros": unit * count})
    return {"items": items, "totalYuan": sum(i["totalMicros"] for i in items) / 1000000,
            "priceSource": "account_catalog" if api_key else "public_catalog"}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Read current prices for a JSON request plan; no paid calls.")
    parser.add_argument("--plan", required=True, help='JSON list: [{"path":"/openapi/...","params":{},"count":1}]')
    args = parser.parse_args()
    key = next((os.environ.get(n, "") for n in ("WM_API_KEY", "MANGYUN_API_KEY", "MANGE_API_KEY") if os.environ.get(n)), "")
    print(json.dumps(estimate_plan(json.loads(Path(args.plan).read_text(encoding="utf-8")), api_key=key), ensure_ascii=False, indent=2))
