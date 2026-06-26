# 调研提示词模板集

把这些模板直接粘到小红书 MCP / WebSearch / WebFetch 的 query，能大幅提高命中率。

---

## 🔴 小红书 MCP（`search_feeds`）

### 基础信息类
```
<目的地> 攻略 最新 <月份>
<目的地> <季节> 天气 穿搭
<目的地> 物价 消费水平
<目的地> 几天合适 深度游
<目的地> <人数> 玩法
```

### 避坑 / 真实反馈类（**价值最高**）
```
<目的地> 避坑 雷点
<目的地> 不要去 后悔
<目的地> 被宰 防宰
<景点名> 真实体验 打卡还是深度
<酒店名> 真实住宿体验
```

### 特定体验类
```
<目的地> 自由潜 船潜 费用
<目的地> 自驾 租车 推荐
<目的地> 跳伞 价格 对比
<目的地> 浮潜 一日游 靠谱
<目的地> 滑翔伞 天气 季节
```

### 当季 / 时效类
```
<目的地> 签证 <年份>
<目的地> 入境 最新规定
<目的地> <月份> 台风 雨季
<目的地> 淡季 旺季 对比
```

### 读懂小红书的信号

| 信号 | 判断 |
|------|------|
| 发帖 ≥3 个月前的"最新攻略" | ❌ 过期 |
| 正文全是图没文字 | ❌ 水贴 |
| 评论区全是"姐妹怎么约" | ⚠️ 广告软文 |
| 评论区有大量真实吐槽 | ✅ 可信 |
| 博主只有旅行类发文 | ✅ 专业 |
| 博主天天发不同目的地 | ⚠️ 代发广告号 |
| 正文出现"xxx机构""xxx老师" | ⚠️ 软植入 |

**建议工作流**：
1. `search_feeds` 先看标题列表，挑发布时间近 + 标题具体的 5-8 篇
2. `get_feed_detail` 逐篇打开正文 + 评论
3. 评论区信号 > 正文，真实经历往往藏在楼中楼

---

## 🟡 WebSearch / WebFetch

### 酒店比价
```
<酒店名> site:agoda.com
<酒店名> site:booking.com
<酒店名> official website
<目的地> best hotel <预算> per night
<酒店名> reviews tripadvisor
```

### 交通
```
<A>→<B> ferry schedule <年份>
<A>→<B> flight comparison
<渡轮公司> official booking
<城市> airport to <区域> distance time
<国家> train pass tourist
```

### 签证 / 入境
```
<国家> visa policy <国籍> <年份> site:gov
中华人民共和国驻<国家>大使馆 最新提醒
<国家> tourist visa requirements
<国家> e-visa official
```

### 一日游 / 活动
```
<活动名> <目的地> klook
<活动名> <目的地> getyourguide
<活动名> operator reviews reddit
<活动名> <目的地> tripadvisor top rated
```

### 美食 / 餐厅
```
<餐厅名> <目的地> google reviews
<目的地> <菜系> must try
best <cuisine> restaurant <city> tripadvisor
<city> food blogger local recommendation
```

### 天气与季节
```
<目的地> weather <月份> historical
<目的地> rainy season months
<目的地> typhoon season
<目的地> best time to visit
```

---

## 🟢 地图 API 提示词（google-maps-api / 其他）

### 必查项
- `directions(origin, destination, mode=driving, alternatives=true)` 对比多条路线
- `places_nearby(location, radius=5000, type=restaurant, rank=rating)` 周边美食
- `distance_matrix` 批量算 N 个酒店到 M 个景点的距离
- `geocoding` 把酒店名字转成坐标用于 Leaflet 画点

### 常见场景

**场景 1：选住宿位置**
```
查 10 个候选酒店到 5 个必去景点的 distance_matrix，
按 "平均时间升序" 排，取前 3 做深度比较
```

**场景 2：自驾路线优化**
```
对比 A→B→C→D 和 A→C→B→D 两条路线，
分别调 directions，看 total duration 和 total distance
```

**场景 3：找沿途补给**
```
route 的 waypoint 附近 5km 内，places_nearby(type=gas_station)
每隔 150km 给自己画一个加油标记
```

---

## 📋 信息收集标准化输出

每个决策点都要有一个**对比表**，列清：

| 选项 | 价格 | 优点 | 缺点 | 数据来源 |
|------|------|------|------|----------|
| A | ¥XXX | 近 | 贵 | Agoda / 小红书 |
| B | ¥YYY | 便宜 | 远 | Booking |

**决策理由**单独列出来，写清楚为什么选 A 不选 B。后续复盘时能看到"当时为什么这么定"。

---

## ⚠️ 调研红线

1. **不信无日期的"最新"** —— 永远看发布时间
2. **不信单源** —— 至少 2 个独立来源交叉验证
3. **敏感信息脱敏** —— 对外分享的攻略不写具体确认号、信用卡尾号
4. **价格换算** —— 始终标本币 + CNY，用当日汇率（备注查询日期）
5. **尊重时效** —— 半年前的票价/班次只能参考，必须官网 double check
6. **警惕 AI 生成的"攻略"** —— 小红书 2024 年后大量 AI 水文，用"具体地名 + 具体费用 + 具体体验"作为真人鉴别信号
