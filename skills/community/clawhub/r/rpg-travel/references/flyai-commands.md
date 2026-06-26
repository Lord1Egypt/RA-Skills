# FlyAI 命令参考

## search-flight — 机票搜索

```bash
flyai search-flight \
  --origin "[出发城市]" \
  --destination "[目的地城市]" \
  --dep-date [YYYY-MM-DD] \
  --sort-type 3
```

### 常用参数
| 参数 | 说明 | 示例 |
|------|------|------|
| `--origin` | 出发城市 | `"上海"` |
| `--destination` | 目的地 | `"京都"` |
| `--dep-date` | 出发日期 | `2026-04-05` |
| `--dep-date-start` | 出发日期范围起 | `2026-04-01` |
| `--dep-date-end` | 出发日期范围止 | `2026-04-07` |
| `--back-date` | 回程日期 | `2026-04-07` |
| `--sort-type` | 排序：1价高→低 3价低→高 4耗时短 | `3` |
| `--max-price` | 最高价 | `2000` |
| `--seat-class-name` | 舱位 | `"经济舱"` |

## search-hotels — 酒店搜索

```bash
flyai search-hotels \
  --dest-name "[目的地]" \
  --check-in-date [YYYY-MM-DD] \
  --check-out-date [YYYY-MM-DD]
```

### 常用参数
| 参数 | 说明 | 示例 |
|------|------|------|
| `--dest-name` | 目的地 | `"京都"` |
| `--key-words` | 关键词 | `"清水寺附近"` |
| `--poi-name` | 景点名称（搜附近酒店） | `"清水寺"` |
| `--check-in-date` | 入住日期 | `2026-04-05` |
| `--check-out-date` | 退房日期 | `2026-04-07` |
| `--sort` | 排序：price_asc/price_desc/rate_desc | `price_asc` |
| `--max-price` | 最高价/晚 | `500` |
| `--hotel-types` | 酒店类型 | `"酒店,民宿,客栈"` |
| `--hotel-stars` | 星级 1~5 | `"3,4,5"` |

## search-poi — 景点搜索

```bash
flyai search-poi \
  --city-name "[城市名]"
```

### 常用参数
| 参数 | 说明 | 示例 |
|------|------|------|
| `--city-name` | 城市名 | `"京都"` |
| `--keyword` | 关键词 | `"寺庙"` |
| `--category` | 景点类型 | `"人文古迹"` |
| `--poi-level` | 景点等级 1-5 | `5` |

### 景点类型（category）
自然风光、山湖田园、森林丛林、峡谷瀑布、沙滩海岛、沙漠草原、人文古迹、古镇古村、历史古迹、园林花园、宗教场所、公园乐园、主题乐园、水上乐园、影视基地、动物园、植物园、海洋馆、体育场馆、演出赛事、剧院剧场、博物馆、纪念馆、展览馆、地标建筑、市集、文创街区、城市观光、户外活动、滑雪、漂流、冲浪、潜水、露营、温泉

## fliggy-fast-search — 极速搜索

```bash
flyai fliggy-fast-search \
  --query "[自然语言搜索词]"
```

### 适用场景
- 搜索美食/特色体验（如"京都拉面"、"大阪烧"）
- 搜索旅行产品（如"京都一日游"、"和服体验"）
- 模糊搜索不确定分类的内容

---

## 飞猪链接生成规则

所有 FlyAI 命令返回的 JSON 结果中，提取 `itemId` 字段拼接飞猪链接：

```
https://market.fliggy.com/item.htm?itemId={itemId}
```

### 字段提取优先级

1. **`itemId`** — 直接拼接（最高优先级）
2. **`item_id`** — 同上
3. **`url`** — 直接使用返回的完整 URL
4. **兜底** — 用关键词拼接搜索页 URL

### 兜底搜索页 URL 模板

| 类型 | URL 模板 |
|------|---------|
| 航班 | `https://www.fliggy.com/flight/list.htm?depCityName={出发城市}&arrCityName={目的地}&depDate={日期}` |
| 酒店 | `https://www.fliggy.com/hotel/list.htm?cityName={城市}&keyword={酒店名}` |
| 景点/门票 | `https://www.fliggy.com/ticket/list.htm?keyword={景点名}` |
| 美食/体验 | `https://www.fliggy.com/search/list.htm?keyword={关键词}` |

### 注意事项
- 如果 FlyAI 返回结果中没有 `itemId` 字段，使用兜底方案
- 每个可购买项必须附带链接（即使只是搜索页）
- 链接在 HTML 中展示为「飞猪购买」按钮 + 「复制链接」按钮
