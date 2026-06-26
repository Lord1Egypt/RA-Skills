# Playbooks

## 参数速查表
| 目标 | 推荐排序 | 推荐半径 | 常用约束 |
|---|---|---|---|
| 赶车/赶机 | `distance_asc` | 1-3km（车站）/2-8km（机场） | `hotel-stars`、`max-price` |
| 逛商圈 | `rate_desc`（再做距离约束） | 0.8-2km | `hotel-stars`、`max-price` |
| 景点游玩 | `distance_asc` | 1-5km | `max-price`、入住日期 |
| 参会商务 | `distance_asc` | 1-4km | `hotel-stars`、`max-price` |

## Playbook A：高铁枢纽（赶车优先）
- **适用**：到站晚、次日早班车、希望步行/短打车到车站。
- **输入建议**：
  - 地标：`<城市> + 火车站/高铁站`（如“杭州东站”）
  - 半径：`1-3km`
  - 偏好：`distance_asc` + `hotel-stars 3,4` + 价格上限
- **命令模板**：

```bash
flyai search-poi --city-name "<城市>" --keyword "<高铁站名称>" --category "地标建筑"
flyai search-hotels --dest-name "<城市>" --poi-name "<高铁站名称>" --check-in-date <yyyy-mm-dd> --check-out-date <yyyy-mm-dd> --sort distance_asc --hotel-stars "3,4" --max-price <预算>
```

## Playbook B：商圈夜生活（步行便利优先）
- **适用**：逛街、餐饮、夜生活，要求回酒店方便。
- **输入建议**：
  - 地标：核心商圈（如“太古里”“国贸”“新天地”）
  - 半径：`0.8-2km`
  - 偏好：评分优先，可接受轻微溢价
- **命令模板**：

```bash
flyai search-poi --city-name "<城市>" --keyword "<商圈名称>" --category "市集"
flyai search-hotels --dest-name "<城市>" --poi-name "<商圈名称>" --check-in-date <yyyy-mm-dd> --check-out-date <yyyy-mm-dd> --sort rate_desc --hotel-stars "4,5" --max-price <预算>
```

## Playbook C：景点打卡（游玩效率优先）
- **适用**：核心景点停留 1-2 天，追求多次往返便利。
- **输入建议**：
  - 地标：景区主入口或核心景点名
  - 半径：`1-5km`（按景区面积调整）
  - 偏好：距离优先 + 预算约束
- **命令模板**：

```bash
flyai search-poi --city-name "<城市>" --keyword "<景点名称>" --category "城市观光"
flyai search-hotels --dest-name "<城市>" --poi-name "<景点名称>" --check-in-date <yyyy-mm-dd> --check-out-date <yyyy-mm-dd> --sort distance_asc --max-price <预算>
```

## Playbook D：机场红眼航班（休息恢复优先）
- **适用**：深夜到达或清晨起飞，需快速入住并保证睡眠质量。
- **输入建议**：
  - 地标：机场名称（如“浦东机场”“白云机场”）
  - 半径：`2-8km`（机场范围大，建议适度放宽）
  - 偏好：`distance_asc` + 中高评分 + 预算上限
- **命令模板**：

```bash
flyai search-poi --city-name "<城市>" --keyword "<机场名称>" --category "地标建筑"
flyai search-hotels --dest-name "<城市>" --poi-name "<机场名称>" --check-in-date <yyyy-mm-dd> --check-out-date <yyyy-mm-dd> --sort distance_asc --hotel-stars "3,4,5" --max-price <预算>
```

## Playbook E：会展中心参会（通勤稳定优先）
- **适用**：展会/会议连续多天，强调准时与通勤确定性。
- **输入建议**：
  - 地标：会展中心名称（如“国家会展中心”）
  - 半径：`1-4km`
  - 偏好：距离优先 + 评分优先 + 商务配套
- **命令模板**：

```bash
flyai search-poi --city-name "<城市>" --keyword "<会展中心名称>" --category "展览馆"
flyai search-hotels --dest-name "<城市>" --poi-name "<会展中心名称>" --check-in-date <yyyy-mm-dd> --check-out-date <yyyy-mm-dd> --sort distance_asc --hotel-stars "4,5" --max-price <预算>
```
