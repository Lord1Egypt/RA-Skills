"""语义化改写测试：跑全部 13 个 API，打印 text 字段"""
import sys
sys.path.insert(0, "scripts")

from tmap_client import TmapClient

c = TmapClient()

def test(label, fn, *args, **kwargs):
    print(f"\n{'='*60}")
    print(f"【{label}】")
    print(f"{'='*60}")
    try:
        r = fn(*args, **kwargs)
        print(r)
    except Exception as e:
        print(f"❌ 错误: {e}")


# 1. 地址解析
test("geocoder - 完整地址", c.geocoder, "北京市朝阳区阜通东大街6号")
test("geocoder - 模糊名称", c.geocoder, "腾讯滨海大厦")

# 2. 逆地址解析
test("regeocoder", c.regeocoder, 22.540601, 113.93397)

# 3. 地点搜索（城市）
test("poi_search - 黄鹤楼", c.poi_search, "黄鹤楼", region="武汉", page_size=3)

# 4. 周边搜索
test("poi_nearby - 咖啡", c.poi_nearby, "咖啡", location="22.540601,113.93397")

# 5. 关键词提示
test("poi_sug - 天安门", c.poi_sug, "天安门", region="北京")

# 6. POI 详情
test("poi_detail - 黄鹤楼", c.poi_detail, "16294309905749563320")

# 7. 驾车路线
test("direction - driving", c.direction, "深圳北站", "深圳湾口岸", "driving")

# 8. 步行路线
test("direction - walking", c.direction, "22.540601,113.93397", "22.542734,113.929728", "walking")

# 9. 骑行路线
test("direction - bicycling", c.direction, "22.540601,113.93397", "22.542734,113.929728", "bicycling")

# 10. 公交路线
test("direction - transit", c.direction, "深圳北站", "深圳湾口岸", "transit")

# 11. IP 定位
test("ip_location", c.ip_location)

# 12. 行政区划
test("district_list", c.district_list)

# 13. 两点间距离
test("distance_matrix - driving", c.distance_matrix,
     "22.540601,113.93397", "22.610,114.030", "driving")
test("distance_matrix - walking", c.distance_matrix,
     "22.540601,113.93397", "22.610,114.030", "walking")

# 14. 天气
test("weather - now", c.weather, adcode="440305", type="now")
test("weather - future", c.weather, adcode="110000", type="future")

print("\n\n✅ 测试完成")
