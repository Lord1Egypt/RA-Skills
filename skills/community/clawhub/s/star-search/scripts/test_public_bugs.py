"""公网 API 全面测试 — 找 bug"""
import urllib.request
import urllib.error
import json
import time
import sys

BASE = "https://search.token-star.cn"
results = []

def test(name, method, path, body=None, expect_status=200, expect_min_results=1):
    url = f"{BASE}{path}"
    t0 = time.time()
    try:
        if method == "GET":
            req = urllib.request.Request(url)
        else:  # POST
            req = urllib.request.Request(
                url, data=json.dumps(body).encode(),
                headers={"Content-Type": "application/json"}
            )
        r = urllib.request.urlopen(req, timeout=20)
        elapsed = (time.time() - t0) * 1000
        status = r.status
        data = r.read().decode()
        try:
            j = json.loads(data)
        except:
            j = None
        ok_status = (status == expect_status)
        ok_min = True
        if j and "count" in j:
            ok_min = j["count"] >= expect_min_results
        ok = ok_status and ok_min
        results.append((ok, name, status, elapsed, j, None))
        marker = "✅" if ok else "❌"
        cnt = j.get("count", "?") if j else "?"
        print(f"  {marker} {name:35s} HTTP {status}  {elapsed:6.0f}ms  count={cnt}")
        return j
    except urllib.error.HTTPError as e:
        elapsed = (time.time() - t0) * 1000
        body = e.read().decode()[:200]
        results.append((False, name, e.code, elapsed, None, body))
        print(f"  ❌ {name:35s} HTTP {e.code}  {elapsed:6.0f}ms  {body[:100]}")
        return None
    except Exception as e:
        elapsed = (time.time() - t0) * 1000
        results.append((False, name, "ERR", elapsed, None, str(e)[:200]))
        print(f"  ❌ {name:35s} {type(e).__name__}  {elapsed:6.0f}ms  {str(e)[:100]}")
        return None

print("="*70)
print("Star Search v16.2 公网 API 全量测试")
print("="*70)

# === 健康检查 ===
print("\n[1] 健康检查")
test("health", "GET", "/v1/health", expect_status=200, expect_min_results=0)
test("health-no-suffix", "GET", "/v1/health/", expect_status=200, expect_min_results=0)

# === 端点枚举 ===
print("\n[2] 端点枚举")
test("engines", "GET", "/v1/engines", expect_status=200, expect_min_results=0)
test("modes", "GET", "/v1/modes", expect_status=200, expect_min_results=0)

# === 11 个 mode 全部测 ===
print("\n[3] 11 个 mode 全量测试")
modes = [
    "quick", "deep", "dev", "news", "global", "policy", "stock",
    "tech_news", "finance", "weixin", "all"
]
for mode in modes:
    body = {"query": "华为", "mode": mode, "top": 3}
    test(f"mode={mode:10s}", "POST", "/v1/search", body=body, expect_min_results=0)

# === 边界 / 异常 ===
print("\n[4] 边界 / 异常测试")
test("空 query", "POST", "/v1/search", body={"query": "", "mode": "deep"}, expect_min_results=0)
test("无 mode", "POST", "/v1/search", body={"query": "test"}, expect_min_results=0)
test("不存在的 mode", "POST", "/v1/search", body={"query": "test", "mode": "fake_mode"}, expect_min_results=0)
test("无 body", "POST", "/v1/search", body={}, expect_min_results=0)
test("top=0", "POST", "/v1/search", body={"query": "test", "top": 0}, expect_min_results=0)
test("top=100", "POST", "/v1/search", body={"query": "test", "top": 100}, expect_min_results=0)
test("长 query 100字", "POST", "/v1/search", body={"query": "华" * 100, "mode": "deep"}, expect_min_results=0)
test("特殊字符", "POST", "/v1/search", body={"query": "AI & ML <script>alert(1)</script>", "mode": "global"}, expect_min_results=0)
test("SQL 注入", "POST", "/v1/search", body={"query": "'; DROP TABLE--", "mode": "deep"}, expect_min_results=0)

# === 中文 / 英文 / emoji / 数字 ===
print("\n[5] 输入变体")
test("纯中文", "POST", "/v1/search", body={"query": "人工智能", "mode": "deep"}, expect_min_results=0)
test("纯英文", "POST", "/v1/search", body={"query": "artificial intelligence", "mode": "global"}, expect_min_results=0)
test("中日英混", "POST", "/v1/search", body={"query": "Apple iPhone 中国 销售", "mode": "deep"}, expect_min_results=0)
test("emoji", "POST", "/v1/search", body={"query": "🎉🚀 测试", "mode": "deep"}, expect_min_results=0)
test("阿拉伯数字", "POST", "/v1/search", body={"query": "2026 高考", "mode": "news"}, expect_min_results=0)

# === HTTP method 检查 ===
print("\n[6] HTTP method 错误")
test("GET 访问 POST 端点", "GET", "/v1/search", expect_status=405, expect_min_results=0)
test("404 路径", "GET", "/v1/xxx", expect_status=404, expect_min_results=0)
test("根路径", "GET", "/", expect_status=404, expect_min_results=0)

# === /v1/search/refresh ===
print("\n[7] refresh 端点")
test("refresh 正常", "POST", "/v1/search/refresh", body={"query": "华为", "mode": "tech_news", "top": 3}, expect_min_results=0)
test("refresh 无 body", "POST", "/v1/search/refresh", expect_min_results=0)

# === 性能 / 并发 ===
print("\n[8] 性能 (3 次同 query 看缓存)")
for i in range(3):
    test(f"perf-{i+1}", "POST", "/v1/search",
         body={"query": "perf test 性能", "mode": "deep", "top": 5}, expect_min_results=0)

# === CORS / 安全 ===
print("\n[9] CORS / 安全 headers")
req = urllib.request.Request(f"{BASE}/v1/health")
try:
    r = urllib.request.urlopen(req, timeout=5)
    headers = dict(r.headers)
    print(f"  Headers:")
    for k in ["Access-Control-Allow-Origin", "Content-Type", "Server", "X-Frame-Options", "Content-Security-Policy", "Strict-Transport-Security"]:
        v = headers.get(k, "(none)")
        print(f"    {k:35s} {v[:80]}")
except Exception as e:
    print(f"  ❌ {e}")

# === 总览 ===
print("\n" + "="*70)
ok = sum(1 for r in results if r[0])
total = len(results)
print(f"结果: {ok}/{total} 通过 ({100*ok//total}%)")
print("="*70)

# 列出失败的
fails = [r for r in results if not r[0]]
if fails:
    print("\n❌ 失败用例:")
    for ok_, name, status, elapsed, data, err in fails:
        print(f"  {name}: {err or data}")
