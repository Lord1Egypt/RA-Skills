# flyai search-train 命令参考

## 参数速查

| 参数 | 说明 | 示例 |
|------|------|------|
| `--origin` | 出发城市/车站（必填） | `"北京"` |
| `--destination` | 目的地城市/车站 | `"上海"` |
| `--dep-date` | 出发日期 | `2026-04-03` |
| `--dep-date-start/end` | 出发日期范围 | `2026-04-03` ~ `2026-04-05` |
| `--back-date` | 回程日期 | `2026-04-10` |
| `--back-date-start/end` | 回程日期范围 | `2026-04-10` ~ `2026-04-12` |
| `--journey-type` | 1=直达, 2=中转 | `2` |
| `--seat-class-name` | 坐席，逗号分隔（二等座/一等座/商务座/硬卧/软卧） | `"硬卧,软卧"` |
| `--transport-no` | 车次号，逗号分隔 | `"G71,G73"` |
| `--transfer-city` | 中转城市，逗号分隔 | `"长沙,武汉"` |
| `--dep-hour-start/end` | 出发时段 0-24 | `12h` ~ `18h` |
| `--arr-hour-start/end` | 到达时段 0-24 | `6` ~ `22` |
| `--total-duration-hour` | 最大总时长（小时） | `8` |
| `--max-price` | 最高价格（元） | `800` |
| `--sort-type` | 1=价高→低, 2=推荐, 3=价低→高, 4=时短→长, 5=时长→短, 6=出发早, 7=出发晚, 8=直达优先 | `4` |

## 参数映射规则（重要）

用户明确提到的查询条件**必须**对应到相应参数：
- 用户说"硬卧" → `--seat-class-name "硬卧"`（⚠️ 中转查询不支持此参数，需 Step 2c 单独查询）
- 用户说"G71" → `--transport-no "G71"`
- 用户说“下午出发” → `--dep-hour-start 12h --dep-hour-end 18h`
- 用户说"8小时以内" → `--total-duration-hour 8`
- 用户说"不超过500块" → `--max-price 500`

## 返回数据结构

```json
{
  "data": {
    "itemList": [{
      "adultPrice": "¥553.0",
      "journeys": [{
        "segments": [{
          "depCityName": "北京", "depStationName": "北京南",
          "depDateTime": "2026-04-03 08:00:00",
          "arrCityName": "上海", "arrStationName": "上海虹桥",
          "arrDateTime": "2026-04-03 12:28:00",
          "duration": "268分钟",
          "marketingTransportNo": "G11",
          "seatClassName": "二等座"
        }],
        "totalDuration": "268分钟"
      }],
      "jumpUrl": "https://..."
    }]
  }
}
```

关键字段：`itemList` 方案列表、`segments[]` 每段行程、`jumpUrl` 预订链接（必须展示）、`totalDuration` 总时长
