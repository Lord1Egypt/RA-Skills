import json, urllib.request, time

# 查2024.10之后新出现的ETF名称
codes_2025 = [
    "513190", "562660", "562590", "513810", "513910", "588800",
    "159573", "159523", "159562", "562560", "562700", "159563",
    "159510", "159326", "159547", "159627", "562570", "159620",
    "512050", "588820", "589000", "589010", "159201", "159381",
    "159301", "159367", "159368", "588170", "159323", "159731",
    "518850", "516650", "159666", "159601", "513230", "562550",
    "159985"
]

codes_2025 = list(set(codes_2025))

for code in codes_2025:
    try:
        if code.startswith('5'):
            secid = f"1.{code}"
        else:
            secid = f"0.{code}"
        
        url = f"https://push2.eastmoney.com/api/qt/stock/get?secid={secid}&fields=f57,f58"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        resp = urllib.request.urlopen(req, timeout=5)
        data = json.loads(resp.read().decode())
        if data.get('data'):
            print(f"{code}: {data['data'].get('f58', 'N/A')}")
        else:
            print(f"{code}: 未找到(secid={secid})")
    except Exception as e:
        print(f"{code}: 查询失败")
    time.sleep(0.1)
