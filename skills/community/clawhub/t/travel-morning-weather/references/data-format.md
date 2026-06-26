# Data Format — travel-plan.json

**文件路径**: `memory/travel-plan.json`

## Schema

```json
{
  "default_location": "Your City, Country",
  "daily_locations": {
    "2026-05-10": "Paris, France",
    "2026-05-11": "Paris, France",
    "2026-05-12": "Lyon, France"
  }
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `default_location` | string | 非旅行时的默认天气查询地点 |
| `daily_locations` | object | 日期→地点映射，key 格式 `YYYY-MM-DD`，value 格式 `City, Country` |

## 更新命令

```bash
# 添加日期范围
python3 skills/travel-morning-weather/scripts/update-travel-plan.py \
  --start 2026-05-10 --end 2026-05-12 --location "Paris, France"

# 添加单个日期
python3 skills/travel-morning-weather/scripts/update-travel-plan.py \
  --date 2026-05-15 --location "Lyon, France"

# 删除日期
python3 skills/travel-morning-weather/scripts/update-travel-plan.py \
  --remove 2026-05-10

# 设置默认地点
python3 skills/travel-morning-weather/scripts/update-travel-plan.py \
  --set-default "Your City, Country"
```

## ⚠️ 安全规则

- **禁止用 `write` 覆盖**此文件（违反 P0-D 铁律）
- 必须用 `exec` + Python 脚本或 `edit` 精确修改
