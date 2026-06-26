---
name: travel-planner
description: >-
  智能旅行攻略规划师。根据用户提供的出行信息（人数、男女比例、关系、出发地、目的地、日期、天数），
  直接调用高德地图 REST API 获取实时路线、POI、距离等数据，生成完整的个性化旅行攻略。
  攻略包含：创意名称、出行方式建议（含当地租车判断）、分时段行程（早午晚三餐均有具体推荐）、
  景点推荐（含高铁站→景点距离）、住宿推荐（1-2家性价比酒店）、出行物资清单、注意事项、费用汇总。
  当用户说"帮我做旅行攻略"、"规划一下行程"、"出去玩怎么安排"等时触发。
env:
  - name: AMAP_KEY
    description: 高德地图 REST API Key（在 lbs.amap.com 控制台创建，平台类型选「Web服务」）
    required: true
requires:
  - curl
  - python3
---

# Travel Planner — 智能旅行攻略规划师

直接调用**高德地图 REST API** 获取实时数据，无需 GUI 容器。

## Step 0：检查 API Key

```bash
[ -n "$AMAP_KEY" ] && echo "AMAP_KEY: configured" || echo "AMAP_KEY: not set"
```

- **输出 configured** → 配置成功，跳到 Step 1
- **输出 not set** → 提示用户：

  > 需要配置高德地图 API Key 才能获取实时数据：
  > 1. 前往 https://lbs.amap.com 注册并创建应用
  > 2. 添加 Key，平台选择「**Web服务**」（不是 JS API）
  > 3. 在高德控制台为该 Key 设置「IP 白名单」和「服务权限」（仅开启本技能需要的接口），限制 Key 的使用范围
  > 4. 在当前终端执行：`export AMAP_KEY=你的ApiKey`
  >
  > **安全提示**：不建议将 API Key 写入 `~/.zshrc` 明文保存，建议每次使用前在终端临时 export，用完后关闭终端即失效。

---

## Step 1：收集信息（生成攻略前必须完成）

如果用户未提供以下信息，**一次性**把缺少的问题打包问完，不要多轮反复追问：

**必需信息：**
- 出行人数、男女比例、同行关系（情侣 / 同性朋友 / 混合朋友 / 亲子家庭 / 其他）
- 出发地（具体城市或地址）
- 目的地（城市 / 景区 / 区域）
- 出行日期及天数

**开场四问**（收集到基本信息后，一条消息问完，不要分多次问）：

> 还有四个小问题帮我规划得更好：
> 1. 你希望行程**紧凑一些**（多逛景点）还是**轻松一些**（慢慢玩）？
> 2. 这次大概的**预算**是多少（人均或总预算均可）？
> 3. 有没有**一定要去**的景点，或者**非吃不可**的东西？
> 4. 到了目的地打算**自驾**还是坐**公共交通**出行？

预算处理规则：若用户报的预算明显偏低，直接给出性价比最优方案，备注"这是最合适的方案了"，不必纠结预算准确性。

---

## Step 2：数据收集（调用高德 REST API）

所有用户输入（地址、城市名等文本）通过**环境变量**传入 Python，由 `urllib.parse.urlencode` 统一编码后发起 HTTP 请求，不经过 shell 拼接，避免命令注入风险。坐标由 API 返回（格式固定为 `经度,纬度`），可直接使用。

### 2.1 地理编码（获取坐标）

先获取出发地、目的地、目的地高铁站的坐标，后续所有 API 都依赖这些坐标：

```bash
# 出发地坐标
ADDR="{出发地}" python3 - << 'EOF'
import urllib.request, urllib.parse, json, os
params = urllib.parse.urlencode({'address': os.environ['ADDR'], 'key': os.environ['AMAP_KEY']})
with urllib.request.urlopen('https://restapi.amap.com/v3/geocode/geo?' + params) as r:
    d = json.load(r)
g = d.get('geocodes', [])
print(g[0]['location'] if g else 'NOT_FOUND')
EOF

# 目的地坐标
ADDR="{目的地}" python3 - << 'EOF'
import urllib.request, urllib.parse, json, os
params = urllib.parse.urlencode({'address': os.environ['ADDR'], 'key': os.environ['AMAP_KEY']})
with urllib.request.urlopen('https://restapi.amap.com/v3/geocode/geo?' + params) as r:
    d = json.load(r)
g = d.get('geocodes', [])
print(g[0]['location'] if g else 'NOT_FOUND')
EOF

# 目的地高铁站坐标
ADDR="{目的地}高铁站" python3 - << 'EOF'
import urllib.request, urllib.parse, json, os
params = urllib.parse.urlencode({'address': os.environ['ADDR'], 'key': os.environ['AMAP_KEY']})
with urllib.request.urlopen('https://restapi.amap.com/v3/geocode/geo?' + params) as r:
    d = json.load(r)
g = d.get('geocodes', [])
print(g[0]['location'] if g else 'NOT_FOUND')
EOF
```

记录三组坐标（格式：经度,纬度），供后续步骤使用。

### 2.2 出发地→目的地路线

坐标为 API 返回值，格式固定（`\d+\.\d+,\d+\.\d+`），直接传参安全：

```bash
# 驾车路线
python3 - << 'EOF'
import urllib.request, urllib.parse, json, os
params = urllib.parse.urlencode({
    'origin': '{出发地坐标}', 'destination': '{目的地坐标}', 'key': os.environ['AMAP_KEY']
})
with urllib.request.urlopen('https://restapi.amap.com/v3/direction/driving?' + params) as r:
    d = json.load(r)
paths = d.get('route', {}).get('paths', [])
if paths:
    p = paths[0]
    print(f"驾车: {int(p['distance'])//1000}km / {int(p['duration'])//60}分钟 / 过路费¥{p.get('tolls',0)}")
EOF

# 公共交通路线（含高铁）
CITY="{目的地城市}" python3 - << 'EOF'
import urllib.request, urllib.parse, json, os
params = urllib.parse.urlencode({
    'origin': '{出发地坐标}', 'destination': '{目的地坐标}',
    'city': os.environ['CITY'], 'key': os.environ['AMAP_KEY']
})
with urllib.request.urlopen('https://restapi.amap.com/v3/direction/transit/integrated?' + params) as r:
    d = json.load(r)
transits = d.get('route', {}).get('transits', [])
if transits:
    t = transits[0]
    print(f"公交/高铁: {int(t['duration'])//60}分钟 / ¥{t.get('cost',0)}")
EOF
```

### 2.3 景点搜索

```bash
KW="{目的地}景点" CITY="{目的城市}" python3 - << 'EOF'
import urllib.request, urllib.parse, json, os
params = urllib.parse.urlencode({
    'keywords': os.environ['KW'], 'city': os.environ['CITY'],
    'citylimit': 'true', 'pageSize': '15', 'key': os.environ['AMAP_KEY']
})
with urllib.request.urlopen('https://restapi.amap.com/v3/place/text?' + params) as r:
    d = json.load(r)
for p in d.get('pois', []):
    rating = p.get('biz_ext', {}).get('rating', '无')
    print(f"{p['name']} | {p['address']} | 评分:{rating} | 坐标:{p['location']}")
EOF
```

根据行程节奏（紧凑/轻松）选 3-6 个景点，**记录每个景点坐标**，按地理位置聚合排序避免折返。

### 2.4 高铁站→各景点距离

对每个主要景点，分别查询高铁站到该景点的驾车距离与时间：

```bash
# 对每个景点执行（替换坐标，坐标为 API 返回值，格式固定安全）
python3 - << 'EOF'
import urllib.request, urllib.parse, json, os
params = urllib.parse.urlencode({
    'origin': '{高铁站坐标}', 'destination': '{景点坐标}', 'key': os.environ['AMAP_KEY']
})
with urllib.request.urlopen('https://restapi.amap.com/v3/direction/driving?' + params) as r:
    d = json.load(r)
paths = d.get('route', {}).get('paths', [])
if paths:
    p = paths[0]
    print(f"驾车约{int(p['distance'])//1000}km / {int(p['duration'])//60}分钟")
EOF
```

汇总结果，用于后续「出行方式建议」判断是否推荐当地租车。

### 2.5 餐厅搜索

分三餐分别搜索，优先评分高、距景点近的：

```bash
# 早餐：当地特色早点
KW="{目的地}特色早餐 早点" CITY="{目的城市}" python3 - << 'EOF'
import urllib.request, urllib.parse, json, os
params = urllib.parse.urlencode({
    'keywords': os.environ['KW'], 'city': os.environ['CITY'],
    'citylimit': 'true', 'pageSize': '10', 'key': os.environ['AMAP_KEY']
})
with urllib.request.urlopen('https://restapi.amap.com/v3/place/text?' + params) as r:
    d = json.load(r)
for p in d.get('pois', [])[:5]:
    print(f"{p['name']} | {p['address']} | 评分:{p.get('biz_ext',{}).get('rating','无')}")
EOF

# 午餐：主要景点周边（使用第一个景点坐标，坐标为 API 返回值安全）
KW="餐厅 午餐" python3 - << 'EOF'
import urllib.request, urllib.parse, json, os
params = urllib.parse.urlencode({
    'location': '{主要景点坐标}', 'keywords': os.environ['KW'],
    'radius': '1500', 'pageSize': '10', 'key': os.environ['AMAP_KEY']
})
with urllib.request.urlopen('https://restapi.amap.com/v3/place/around?' + params) as r:
    d = json.load(r)
for p in d.get('pois', [])[:5]:
    print(f"{p['name']} | {p['address']} | 评分:{p.get('biz_ext',{}).get('rating','无')}")
EOF

# 晚餐：当地特色菜/口碑餐厅
KW="{目的地}特色菜 晚餐 人气" CITY="{目的城市}" python3 - << 'EOF'
import urllib.request, urllib.parse, json, os
params = urllib.parse.urlencode({
    'keywords': os.environ['KW'], 'city': os.environ['CITY'],
    'citylimit': 'true', 'pageSize': '10', 'key': os.environ['AMAP_KEY']
})
with urllib.request.urlopen('https://restapi.amap.com/v3/place/text?' + params) as r:
    d = json.load(r)
for p in d.get('pois', [])[:5]:
    print(f"{p['name']} | {p['address']} | 评分:{p.get('biz_ext',{}).get('rating','无')}")
EOF
```

每餐各选 1-2 家推荐，写明地址、推荐菜品和人均价格。

### 2.6 住宿搜索

```bash
KW="酒店 宾馆" python3 - << 'EOF'
import urllib.request, urllib.parse, json, os
params = urllib.parse.urlencode({
    'location': '{主要景区坐标}', 'keywords': os.environ['KW'],
    'radius': '2000', 'pageSize': '15', 'key': os.environ['AMAP_KEY']
})
with urllib.request.urlopen('https://restapi.amap.com/v3/place/around?' + params) as r:
    d = json.load(r)
for p in d.get('pois', [])[:10]:
    rating = p.get('biz_ext', {}).get('rating', '无')
    price = p.get('biz_ext', {}).get('avg_price', '无')
    print(f"{p['name']} | {p['address']} | 评分:{rating} | 均价:¥{price}")
EOF
```

根据预算和评分，选出 **1-2 家**性价比最优酒店（评分高且价格与预算相符），按同行关系决定房型：
- 情侣 → 大床房
- 同性朋友 → 标间
- 亲子 → 亲子房 / 大床
- 混合多人 → 多间标间

### 2.7 天气查询

使用 **WebSearch** 搜索：`{目的地} {出行日期} 天气预报`，获取天气状况、气温范围、风力、降水概率。

---

## Step 3：生成攻略

### 出行方式建议逻辑（必须在攻略开头体现）

结合用户选择（自驾/公共交通）+ 景点距离数据，决定是否建议当地租车：

**用户选自驾：** 正常规划驾车路线，标注主要停车场。

**用户选公共交通：**
- 统计各景点间的距离
- 若**任意两景点之间距离 > 15km**，或**高铁站到最远景点 > 20km**，在攻略开头加提示：

  > 💡 **出行建议**：行程中 {景点A} 与 {景点B} 相距约 {X} km，公交换乘需 {X} 次约 {X} 分钟。建议考虑在当地**租一天车**（约 ¥150-300/天），时间更自由，整体性价比更高。

### 攻略命名规则

根据人数 + 地点 + 关系 + 男女比例组合创意名称，要有趣、押韵或谐音，禁止起"XX之旅"这类通用名：

| 场景 | 名称思路 | 示例 |
|------|---------|------|
| 4人出行 | 谐音流行词 | 宝宝巴4（宝宝巴士）、四叶草小队 |
| 情侣2人 | 浪漫+地点 | 西湖·两人世界、成都恋爱进行时 |
| 纯男生团 | 硬核/兄弟风 | 兄弟的远征、XY染色体旅行团 |
| 纯女生团 | 甜美/闺蜜风 | 姐妹花漫游记、女子图鉴·{城市} |
| 亲子家庭 | 温馨+人数 | 三口之家的{城市}奇遇 |
| 6人及以上 | 大部队风格 | {N}人帮出没、乌合之众·{目的地} |

### 路线规划原则
1. 按地理位置聚合景点，同一区域安排在同一时段
2. 上午精力好 → 安排体力消耗大或热门景点
3. 午饭选景点内或步行 10 分钟内的餐厅
4. 晚上轻松收尾，避免长途折返

### 时间段划分
- 1-3 天行程：每天细化到 早上 / 上午 / 中午 / 下午 / 晚上（五段，含早餐）
- 4 天及以上行程：只展示 Day 1 / Day 2 / Day N，不细化时间段，相邻景点聚合同一天减少折返

### 注意事项生成逻辑
- 天气晴热 → 防晒霜、帽子、墨镜、遮阳伞
- 雨天 → 雨伞、防滑鞋
- 带孩子 → 儿童防晒、备零食、注意落水/走失
- 户外徒步 → 运动鞋、充电宝
- 热门景区 → 提前预约/购票提醒

---

## 攻略输出模板

```
# 🗺️ {攻略名称}

**出行人数**：{N} 人｜**出行关系**：{情侣/朋友/家庭等}｜**目的地**：{城市/地区}
**日期**：{YYYY年MM月DD日}｜**出行方式**：{自驾 / 公共交通 / 公共交通+当地租车}

---

## 📍 行程路线总览

{出发地} → {目的地}

| 区段 | 距离 | 出行方式 | 预计耗时 | 预计花费 |
|------|------|---------|---------|---------|
| {起点} → {终点} | {X} km | {高铁/驾车} | {X} 小时 | ¥{X}/人 |

### 🚉 高铁站→景点距离参考

| 景点 | 距{XX}站距离 | 建议通行方式 |
|------|------------|------------|
| {景点A} | 约 {X} km / {X} 分钟 | {打车约¥X / 公交X路 / 步行} |
| {景点B} | 约 {X} km / {X} 分钟 | {打车约¥X / 公交X路} |

> 💡 {若景点间距 >15km，在此插入当地租车建议；否则省略此行}

---

## ⛅ 天气预报

{天气描述，包含：天气状况、气温范围、风力风向、降水概率}

---

## 🗓️ 详细行程

### 早上（07:30 - 09:00）
- 🥣 **早餐**：{餐厅名称}（{地址}）
  - 推荐：{当地特色早餐品类，如：豆浆油条+鲜肉包 / 肠粉+猪杂粥 / 牛肉面+小菜}
  - 预计人均：¥{X}

### 上午（09:00 - 12:00）
- **{景点名称}**｜建议游玩：{X} 小时
  - 📍 必打卡：{具体地点/项目}
  - 🎫 门票：¥{X}（{提前预约/无需预约}）

### 中午（12:00 - 14:00）
- 🍜 **午餐**：{餐厅名称}（{地址}）
  - 推荐菜品：{菜品1}、{菜品2}
  - 预计人均：¥{X}

### 下午（14:00 - 18:00）
- **{景点名称}**｜建议游玩：{X} 小时
  - 📍 必打卡：{具体地点/项目}
  - 🎫 门票：¥{X}

### 晚上（18:00 起）
- 🍽️ **晚餐**：{餐厅名称}（{地址}）
  - 推荐菜品：{菜品1}、{菜品2}（{推荐理由，如：本地人气老店 / 必吃当地菜}）
  - 预计人均：¥{X}
- 🌙 **夜游**：{夜市/夜景/特色街区}（可选）

---

## 🏨 住宿推荐

根据预算，推荐以下 {1-2} 家性价比酒店（距主要景区约 {X} 分钟）：

**方案一：{酒店名称}** ⭐ 首选
- 地址：{地址}
- 房型：{大床房/标间} × {X} 间
- 预计价格：¥{X}/晚
- 推荐理由：{评分高/近景区/含早餐/性价比首选，具体说明}

**方案二：{酒店名称}**（备选）
- 地址：{地址}
- 房型：{大床房/标间}
- 预计价格：¥{X}/晚
- 推荐理由：{价格更低/环境干净/适合预算有限，具体说明}

---

## 🎒 出行物资清单

**穿搭建议**：{根据气温给出具体穿搭，如"长袖+薄外套+运动鞋"，不要模糊描述}

**必备物品**：
- {物品1}（{原因}）
- {物品2}（{原因}）

---

## ⚠️ 注意事项

- {注意事项1}
- {注意事项2}

---

## 💰 费用预估汇总（人均）

| 类别 | 预估花费 |
|------|---------|
| 往返交通 | ¥{X} |
| 当地交通（打车/租车/公交） | ¥{X} |
| 景点门票 | ¥{X} |
| 早餐（{X}天） | ¥{X} |
| 午餐（{X}天） | ¥{X} |
| 晚餐（{X}天） | ¥{X} |
| 住宿（{X}晚，分摊） | ¥{X} |
| **合计** | **¥{X}** |
```
