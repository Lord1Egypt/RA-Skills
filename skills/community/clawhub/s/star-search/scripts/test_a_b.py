"""公网 API 测试 — 精简版（按层分段）"""
import urllib.request, urllib.error, json, time

BASE = "https://search.token-star.cn"
results = []

def test(name, method, path, body=None, expect_status=200, expect_min_results=0, timeout=8):
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
        ok = (r.status == expect_status) and (
            expect_min_results == 0 or
            (j and j.get("count", 0) >= expect_min_results)
        )
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
        print(f"  ❌ {name:35s} {type(e).__name__}  {elapsed:6.0f}ms  {str(e)[:80]}")

print("="*70)
print("[A] 健康 + 端点 (3)")
print("="*70)
test("health", "GET", "/v1/health")
test("engines", "GET", "/v1/engines")
test("modes", "GET", "/v1/modes")

print("\n" + "="*70)
print("[B] 11 mode 全量（每 mode 1 query）")
print("="*70)
modes = ["quick", "deep", "dev", "news", "global", "policy", "stock",
         "tech_news", "finance", "weixin", "all"]
for mode in modes:
    test(f"mode={mode}", "POST", "/v1/search",
         body={"query": "华为", "mode": mode, "top": 3}, timeout=10)

# 总结
ok = sum(1 for r in results if r[0])
total = len(results)
print(f"\n{'='*70}")
print(f"A+B: {ok}/{total} 通过 ({100*ok//total}%)")
print("="*70)
