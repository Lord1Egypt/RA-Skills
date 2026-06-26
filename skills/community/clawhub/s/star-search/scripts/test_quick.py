"""公网 API 测试 — 最快版"""
import urllib.request, urllib.error, json, time

BASE = "https://search.token-star.cn"
results = []

def test(name, method, path, body=None, expect_status=200, timeout=5):
    url = f"{BASE}{path}"
    t0 = time.time()
    try:
        if method == "GET":
            req = urllib.request.Request(url)
        else:
            req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                          headers={"Content-Type": "application/json"})
        r = urllib.request.urlopen(req, timeout=timeout)
        elapsed = (time.time() - t0) * 1000
        data = r.read().decode()
        j = json.loads(data) if data else None
        ok = (r.status == expect_status)
        results.append((ok, name, r.status, elapsed, j))
        marker = "✅" if ok else "❌"
        cnt = j.get("count", "?") if j and isinstance(j, dict) else "?"
        print(f"  {marker} {name:35s} HTTP {r.status}  {elapsed:6.0f}ms  count={cnt}")
    except urllib.error.HTTPError as e:
        elapsed = (time.time() - t0) * 1000
        body = e.read().decode()[:200]
        results.append((False, name, e.code, elapsed, None))
        print(f"  ❌ {name:35s} HTTP {e.code}  {elapsed:6.0f}ms  {body[:80]}")
    except Exception as e:
        elapsed = (time.time() - t0) * 1000
        results.append((False, name, "ERR", elapsed, None))
        print(f"  ❌ {name:35s} {type(e).__name__}  {elapsed:6.0f}ms  {str(e)[:60]}")

# 5 个超快测
test("health", "GET", "/v1/health")
test("engines", "GET", "/v1/engines")
test("modes", "GET", "/v1/modes")
test("quick mode", "POST", "/v1/search", body={"query": "test", "mode": "quick", "top": 3})
test("tech_news mode (fast)", "POST", "/v1/search", body={"query": "test", "mode": "tech_news", "top": 3})

ok = sum(1 for r in results if r[0])
total = len(results)
print(f"\n{ok}/{total} 通过")
