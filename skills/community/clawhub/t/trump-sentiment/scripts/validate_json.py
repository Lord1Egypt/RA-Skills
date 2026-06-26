import json, sys

with open(r"C:\Users\gold3\.openclaw\workspace\skills\trump-sentiment\scripts\analyze_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Items: {len(data)}")
for item in data[:3]:
    print(f"  - {item['title'][:60]}")
