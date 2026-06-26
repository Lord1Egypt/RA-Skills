---
name: travel-planner
description: 为用户生成个性化旅游攻略。当用户要求"做一份旅游攻略"、"帮我规划X天X晚的旅行"、"生成某地旅游行程"、"制定旅游计划"时使用此技能。支持国内外各大城市，自动搜索景点/酒店/美食，计算交通路线，生成Word文档并发送给用户。
---

# Travel Planner - 旅游攻略生成技能

## 功能概述

为用户生成完整旅游攻略，包含：
- 景点、酒店、美食推荐（来自网络搜索）
- 精确交通路线规划（来自百度地图API）
- 按时间顺序排列的详细行程表
- Word文档直接发送给用户

## 使用流程

### Step 1: 检查API密钥

检查 MEMORY.md 或 TOOLS.md 中是否已有百度AK：
- 如果有：直接使用
- 如果没有：询问用户是否提供百度地图开放平台的AK（用于地理编码和路线规划）

### Step 2: 收集用户需求

询问确认以下信息：
1. **目的地**：哪个城市？
2. **天数**：X天X晚？
3. **旅游主题/人群**：年轻人/亲子/家庭/商务？主题偏好？
4. **特殊要求**：要少走路/景点集中/人气高/购物游/文化游？

### Step 3: 网络搜索

使用 multi-search-engine（通过 web_fetch + Bing URL）搜索：
- `{城市} + {天数} + 旅游攻略 + 景点推荐`
- `{城市} + 必吃美食 + 网红餐厅`
- `{城市} + 年轻人 + 热门景点`
- `{城市} + {天数} + 住宿推荐 + 酒店`

参考搜索关键词：
```
# 景点攻略
{城市} {天数} 旅游攻略 景点 2024/2025
{城市} 必去景点 排行榜 年轻人
{城市} 小众景点 网红打卡

# 美食住宿
{城市} 特色美食 必吃 餐厅推荐
{城市} 住宿推荐 酒店 位置

# 交通
{城市} 机场/车站 到 市中心 交通方式
```

### Step 4: 地理编码

使用百度地图开放平台 API 获取每个地点坐标：

```
地理编码API:
https://api.map.baidu.com/geocoding/v3/?address={地点}&output=json&ak={AK}

驾⻋路线API:
https://api.map.baidu.com/direction/v2/driving?origin={lat,lng}&destination={lat,lng}&ak={AK}

公交路线API:
https://api.map.baidu.com/direction/v2/transit?origin={lat,lng}&destination={lat,lng}&ak={AK}
```

### Step 5: 智能排程

将景点按以下原则分组：
1. **地理距离近的放同一天**
2. **考虑游览时间**（每个大景点约1-3小时）
3. **考虑交通时间**（同一区域景点间尽量<30分钟）
4. **不要排太满**，留出吃饭、休息、拍照时间
5. **早晚穿插**，不要全是同类型景点

### Step 6: 生成Word文档

使用 Python `python-docx` 库生成攻略文档，包含：

1. **封面信息**：目的地 + 天数 + 主题
2. **每日行程表**：时间 | 活动 | 地点 | 游览时长 | 交通
3. **交通总览表**：路线 | 距离 | 方式 | 用时 | 费用
4. **住宿推荐表**：区域 | 酒店类型 | 优点
5. **美食推荐表**：类型 | 推荐店铺 | 人均
6. **实用Tips**：建议、注意事项、必备app

### Step 7: 发送文件

使用 `message` 工具通过飞书发送Word文件给用户。

### Step 8: 免责声明

提醒用户：
> 📌 **免责声明**：地点、交通信息来源于百度地图开放平台，住宿、饮食推荐仅供参考。建议出发前参考小红书、携程等平台做进一步细化攻略。

---

## 百度API使用方法

### 地理编码（地址→坐标）

```bash
curl "https://api.map.baidu.com/geocoding/v3/?address={地址}&output=json&ak={AK}"
```

返回：`{ status: 0, result: { location: { lng: 经度, lat: 纬度 } } }`

### 公交路线规划

```bash
curl "https://api.map.baidu.com/direction/v2/transit?origin={lat},{lng}&destination={lat},{lng}&ak={AK}"
```

返回：`{ status: 0, result: { routes: [{ distance: 距离(米), duration: 时间(秒), price: 费用 }] } }`

### 驾⻋路线规划

```bash
curl "https://api.map.baidu.com/direction/v2/driving?origin={lat},{lng}&destination={lat},{lng}&ak={AK}"
```

---

## 智能排程算法

```
输入：景点列表、游玩天数
输出：每日行程安排

步骤：
1. 将景点按地理坐标聚类（距离<3公里的归为一组）
2. 优先选择人气高、交通便利的景点作为核心
3. 将景点组分配到各天，遵循：
   - 同区域景点尽量放同一天
   - 每天不超过3个大景点
   - 每个大景点间交通时间<30分钟
4. 在景点间插入餐厅（步行10分钟以内优先）
5. 考虑酒店位置，选择最方便的一组
```

---

## 输出模板

见 references/output-template.md
