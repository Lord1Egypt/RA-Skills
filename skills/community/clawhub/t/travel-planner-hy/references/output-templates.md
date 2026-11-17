# 方案输出模板

以下为中文示例，按用户语言与实际需求选择和翻译；不要求固定语言或收集所有可选信息。

---

## 模板1：方案总览

```markdown
# 🗺️ {destination} 旅行方案

> 📅 {startDate} → {endDate} | {days}天{days-1}晚 | 👥 {travelers}人
> 💰 预算区间：{budgetMin} - {budgetMax}元 | 🏷️ {preferences badges}

---
```

---

## 模板2：预算明细与比价

```markdown
## 💰 预算明细

### 预算分配

| 项目 | 金额 | 占比 | 说明 |
|------|------|------|------|
| 🚄 交通 | {transportCost}元 | {transportPct}% | 往返+当地交通 |
| 🏨 住宿 | {accommodationCost}元 | {accommodationPct}% | {hotelNights}晚 |
| 🎫 门票 | {ticketCost}元 | {ticketPct}% | {numAttractions}个景点 |
| 🍜 餐饮 | {mealCost}元 | {mealPct}% | 三餐+小吃 |
| 📦 其他 | {otherCost}元 | {otherPct}% | 纪念品等 |
| **合计** | **{totalCost}元** | **100%** |

### 三档方案推荐

| 项目 | 💰 经济型 | 👍 舒适型 | 💎 豪华型 |
|------|-----------|-----------|-----------|
| 交通 | 公共交通 | 高铁+打车 | 飞机+专车 |
| 住宿 | 青旅/民宿 | 连锁酒店 | 高星酒店 |
| 门票 | 免费景点为主 | 正常景点 | VIP/快速通道 |
| 餐饮 | 小吃/简餐 | 当地特色餐厅 | 米其林/高档餐厅 |
| **总计** | **约{ecoTotal}元** | **约{comfTotal}元** | **约{luxTotal}元** |

> 💡 **推荐：{recommendedTier}方案**
```

---

## 模板3：每日详细行程

```markdown
---
### 🗓️ 第{n}天 — {date}（{weekday}）

**{time}** 🚶 **{from} → {to}**
- 交通：{mode}（{duration}，{cost}）

**{time}** 🎯 **{attractionName}**
- ⭐ 评分：{rating}
- 💰 门票：{ticketPrice}元
- ⏰ 建议游玩：{duration}
- 📍 {description}
- 💡 {tip}

**{time}** 🍜 **午餐 — {suggestion}**

**{time}** ☕ **午休**

**{time}** 🎯 **{afternoonAttraction}**

**{time}** 🍽️ **晚餐 — {dinnerSuggestion}**

**{time}** 🌙 **{eveningActivity}**

**当日费用小计：🚇交通{transportCost} + 🎫门票{ticketCost} + 🍜餐饮{mealCost} = 💰{dayTotal}元**

#### ⚠️ 第{n}天注意事项
- 🌤️ 天气：{weatherNote}
- 👔 着装：{clothingNote}
- 📱 预约：{reservationNote}
- 💡 小贴士：{tip}
```

---

## 模板4：行程总表

```markdown
## 📋 行程总表

| 日期 | 上午 | 下午 | 晚上 | 住宿 |
|------|------|------|------|------|
| 第1天 | {morning} | {afternoon} | {evening} | 🏨 {hotel} |
| 第2天 | ... | ... | ... | ... |
```

---

## 模板5：住宿推荐

```markdown
## 🏨 住宿推荐

### 推荐区域

| 区域 | 特点 | 参考价格 | 推荐指数 |
|------|------|----------|----------|
| {area1} | {char} | {price}元/晚 | ⭐⭐⭐⭐ |

### 具体推荐

| 酒店 | 区域 | 评分 | 价格 | 推荐理由 |
|------|------|------|------|----------|
| {hotelName} | {area} | ⭐{rating} | ¥{price}/晚 | {reason} |

> 💡 建议提前{days}天预订
```

---

## 模板6：交通方案汇总

```markdown
## 🚄 交通方案

### 大交通（出发地↔目的地）

| 方式 | 耗时 | 参考价格 | 推荐 |
|------|------|----------|------|
| 🚄 高铁 | {duration} | ¥{price} | 推荐理由 |
| ✈️ 飞机 | {duration} | ¥{price} | 适用场景 |

### 当地交通

| 方式 | 费用/天 | 说明 |
|------|---------|------|
| 🚇 地铁 | {cost} | {note} |
| 🚕 打车 | {cost} | {note} |
```

---

## 模板7：必备物品清单

```markdown
## 🎒 必备物品清单

### 📄 证件
- [ ] 身份证/护照
- [ ] 学生证
- [ ] 酒店预订确认

### 👔 衣物（{season}出行）
- [ ] {items}

### 🧴 日用护理
- [ ] 防晒霜（SPF50+）
- [ ] 雨伞
- [ ] 常用药品

### 🎯 活动装备
- {activityItems}
```

---

## 模板8：安全应急

```markdown
## ⚠️ 当地注意事项

### 紧急联系方式
| 类型 | 号码 |
|------|------|
| 🚓 报警 | 110 |
| 🚑 急救 | 120 |
| 🔥 火警 | 119 |

### 旅行提示
- {tips}
```

---

## 模板9：前后对比（compare子命令）

```markdown
## 🔄 方案调整对比

| 项目 | 调整前 | 调整后 |
|------|--------|--------|
| 总天数 | {before.days} | {after.days} |
| 景点数 | {before.count} | {after.count} |
| 预估费用 | ¥{before.cost} | ¥{after.cost} |

### 每日对比
{对比内容}
```

---

## 模板10：第三方平台跳转清单

可选提供已验证的途牛或 12306 公开首页快捷入口。不要生成支付按钮、待付款页、付款倒计时或订单状态文案。HTML 的 platformUrls 仅接受 references/usage.md 中的固定公开首页；在链接旁说明由用户到第三方平台自行搜索。
