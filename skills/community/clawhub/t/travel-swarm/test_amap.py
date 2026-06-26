import asyncio
import os
import requests
from dotenv import load_dotenv
load_dotenv()

# 直接HTTP调用高德API（不依赖复杂模块）
AMAP_KEY = os.getenv("AMAP_API_KEY")

async def test():
    print("=" * 50)
    print("【测试1】高德天气API")
    print("=" * 50)
    
    # 天气查询
    url = f"https://restapi.amap.com/v3/weather/weatherInfo"
    resp = requests.get(url, params={"city": "北京", "key": AMAP_KEY}, timeout=10)
    print("请求URL:", resp.url)
    print("状态码:", resp.status_code)
    print("返回数据:", resp.text[:500])
    
    print("\n" + "=" * 50)
    print("【测试2】高德POI搜索")
    print("=" * 50)
    
    # POI搜索
    url2 = "https://restapi.amap.com/v3/place/text"
    resp2 = requests.get(url2, params={
        "keywords": "故宫",
        "city": "北京",
        "offset": 3,
        "key": AMAP_KEY
    }, timeout=10)
    print("请求URL:", resp2.url)
    print("状态码:", resp2.status_code)
    print("返回数据:", resp2.text[:800])

if __name__ == "__main__":
    asyncio.run(test())