"""
测试 tencentmap-map-assistant-skill 所有方法
"""
import sys
import os
import json
import time

# 从同级 scripts 目录导入（skill 内部测试）
_script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _script_dir)
from tmap_client import TmapClient, TmapError

client = TmapClient()
results = []

def test(name, fn):
    start = time.time()
    try:
        data = fn()
        elapsed = round(time.time() - start, 2)
        status = data.get("status", "N/A")
        count = data.get("count", len(data.get("data", [])))
        msg = f"✅ {name}  status={status}  count={count}  ({elapsed}s)"
        print(msg)
        results.append({"name": name, "ok": True, "status": status, "msg": msg})
        # 只打印前500字符，避免刷屏
        print("   返回摘要:", json.dumps(data, ensure_ascii=False)[:300])
    except TmapError as e:
        elapsed = round(time.time() - start, 2)
        msg = f"❌ {name}  TmapError code={e.code} msg={e.message}  ({elapsed}s)"
        print(msg)
        results.append({"name": name, "ok": False, "error": msg})
    except Exception as e:
        elapsed = round(time.time() - start, 2)
        msg = f"❌ {name}  异常: {e}  ({elapsed}s)"
        print(msg)
        results.append({"name": name, "ok": False, "error": msg})

print("=" * 60)
print("Key 来源:", client.key_source)
print("=" * 60)

# 1. geocoder — 地址解析
test("geocoder", lambda: client.geocoder("深圳市腾讯滨海大厦"))

# 2. regeocoder — 逆地址解析
test("regeocoder", lambda: client.regeocoder(22.540601, 113.93397, get_poi=False))

# 3. poi_sug — 关键词提示
test("poi_sug", lambda: client.poi_sug("黄鹤楼", region="武汉"))

# 4. poi_search — 地点搜索（按城市）
test("poi_search(城市)", lambda: client.poi_search("黄鹤楼", region="武汉"))

# 5. poi_search — 地点搜索（按坐标）
test("poi_search(坐标)", lambda: client.poi_search("咖啡", location="22.540601,113.93397"))

# 6. poi_nearby — 周边搜索
test("poi_nearby", lambda: client.poi_nearby("咖啡", location="22.540601,113.93397", radius=1000))

# 7. poi_detail — POI 详情（用一个真实 POI ID）
# 先从 poi_search 拿一个真实 ID
try:
    r = client.poi_search("黄鹤楼", region="武汉")
    pois = r.get("data") or []
    if pois:
        poi_id = pois[0].get("id") or pois[0].get("uid", "")
        print(f"  拿到 POI ID: {poi_id}")
        test("poi_detail", lambda: client.poi_detail(poi_id))
    else:
        print("❌ poi_detail  无法获取测试 POI ID，跳过")
except Exception as e:
    print(f"❌ poi_detail  准备失败: {e}")

# 8. direction — 驾车路线
test("direction(driving)", lambda: client.direction("深圳北站", "深圳湾口岸", mode="driving"))

# 9. direction — 步行路线
test("direction(walking)", lambda: client.direction("深圳北站", "深圳湾口岸", mode="walking"))

# 10. direction — 骑行路线
test("direction(bicycling)", lambda: client.direction("深圳北站", "深圳湾口岸", mode="bicycling"))

# 11. direction — 公交路线
test("direction(transit)", lambda: client.direction("深圳北站", "深圳湾口岸", mode="transit"))

# 12. ip_location — IP 定位
test("ip_location", lambda: client.ip_location())

# 13. district_list — 行政区划列表
test("district_list", lambda: client.district_list())

# 14. district_search — 行政区划搜索
test("district_search", lambda: client.district_search("深圳"))

# 15. district_children — 下级区划（用深圳 id）
try:
    r = client.district_search("深圳")
    dists = (r.get("result") or [[]])[0]  # 二维数组，取 result[0]
    if dists:
        pid = dists[0].get("id", "")
        print(f"  深圳 id: {pid}")
        test("district_children", lambda: client.district_children(pid))
    else:
        print("❌ district_children  无法获取父级 ID，跳过")
except Exception as e:
    print(f"❌ district_children  准备失败: {e}")

# 16. distance_matrix — 距离矩阵
test("distance_matrix", lambda: client.distance_matrix(
    from_list=["22.540601,113.93397"],
    to_list=["22.550000,113.940000", "22.530000,113.920000"],
    mode="driving"
))

# 17. weather — 实时天气（用 adcode）
test("weather(adcode)", lambda: client.weather(adcode="440300", type="now"))

# 18. weather — 实时天气（用坐标）
test("weather(location)", lambda: client.weather(location="22.540601,113.93397", type="now"))

# 19. travel_guide — AI 旅游攻略（耗时较长，放最后）
print("\n⏳ travel_guide 开始（约 30-50 秒）...")
test("travel_guide", lambda: client.travel_guide("武汉3天精华游"))

# 汇总
print("\n" + "=" * 60)
print("汇总")
print("=" * 60)
ok = sum(1 for r in results if r["ok"])
total = len(results)
for r in results:
    tag = "✅" if r["ok"] else "❌"
    print(f"  {tag} {r['name']}")
print(f"\n通过: {ok}/{total}")
