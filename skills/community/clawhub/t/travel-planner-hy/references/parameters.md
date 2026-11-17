# 参数字段定义与自然语言解析规则

## 1. 参数字段完整定义

### 必填字段

| 字段 | 类型 | 说明 | 校验规则 |
|------|------|------|----------|
| `destination` | string | 目的地（城市/地区/国家） | 可识别的地理名称 |
| `days` | number | 旅行天数 | ≥1，≤30 |
| `travelers` | number | 旅行人数 | ≥1，≤20 |

### 选填字段

| 字段 | 类型 | 枚举/范围 | 说明 |
|------|------|-----------|------|
| `budget` | string | 如"3000-5000" | 总预算范围（元） |
| `departureDate` | string | 日期或"端午""国庆" | 出发日期 |
| `preferences` | string[] | 美食/自然/人文/购物/亲子/休闲/探险/网红打卡/摄影 | 兴趣偏好标签 |
| `includeSpots` | string[] | 景点名称列表 | 必去景点 |
| `excludeSpots` | string[] | 景点名称列表 | 排除景点 |
| `pace` | string | leisurely/moderate/packed | 节奏偏好 |
| `departureCity` | string | 城市名 | 出发城市 |
| `accommodation` | string | budget/comfort/luxury | 住宿偏好 |
| `diet` | string | — | 饮食禁忌 |

### 衍生字段（自动计算）

| 字段 | 计算方式 |
|------|----------|
| `estimatedTicketBudget` | 总预算 × 10-15% |
| `estimatedMealBudget` | 总预算 × 20-25% |
| `estimatedAccommodationBudget` | 总预算 × 30-40% |
| `estimatedTransportBudget` | 总预算 × 15-20% |

---

## 2. 自然语言解析规则

### 正则提取规则（优先级最高）

**天数提取：**
```
(\d+)[-~—至到]\d+\s*天    → 取中间值
(\d+)\s*天                  → 天数
\d+日游                    → 天数
```

**人数提取：**
```
(\d+)[-~—至到]\d+\s*人    → 取中间值
(\d+)\s*人                  → 人数
(\d+)大(\d+)小            → 分别存储adults/children
```

**预算提取：**
```
预算(\d+)[-~—至到](\d+)\s*元?  → 预算区间
预算(\d+)\s*元(以内|左右|上下)? → 单点预算
人均(\d+)[-~—至到](\d+)\s*元   → 人均预算（×人数=总预算）
```

**日期提取：**
```
(端午|五一|国庆|春节|清明|中秋|元旦) → 节假日→当年公历日期
(\d{4})年(\d{1,2})月(\d{1,2})日    → 绝对日期
(\d{1,2})月(\d{1,2})号?            → 当年日期
(今天|明天|后天|这周末)              → 相对日期
```

**偏好提取：**
```
(美食|吃货|吃)              → 美食
(自然|风光|爬山|徒步)      → 自然
(人文|历史|古迹|博物馆)     → 人文
(购物|逛街)                 → 购物
(亲子|小孩|带孩子)          → 亲子
(休闲|放松|度假)            → 休闲
(网红|打卡|拍照|出片)       → 网红打卡
```

**包含/排除提取：**
```
(想去|必去|包括)[：:]\s*(.+?)(?=。|$|，) → includeSpots（按、/,分割）
(不去|排除|避开)[：:]\s*(.+?)(?=。|$|，) → excludeSpots
```

### LLM 兜底策略

正则提取后仍缺失2个以上必填字段时，使用 LLM 推断：

```json
{
  "destination": null,
  "days": null,
  "travelers": null,
  "budget": null,
  "departureDate": null,
  "preferences": [],
  "includeSpots": [],
  "excludeSpots": [],
  "pace": "moderate",
  "departureCity": null
}
```

### 缺失字段默认值

| 缺失字段 | 默认值 | 说明 |
|----------|--------|------|
| destination | — | **必须询问** |
| days | — | **必须询问** |
| travelers | 2 | 默认两人出行 |
| budget | "待确认" | 标记需确认 |
| preferences | 休闲+美食 | 保守默认 |
| pace | moderate | 适中节奏 |

---

## 3. 确认卡片模板

```markdown
📋 方案参数确认

### 目的地
**{destination}**

### 行程概览
| 项目 | 详情 |
|------|------|
| 🗓️ 天数 | **{days}天** |
| 👥 人数 | **{travelers}人**（{adults}大{children}小）|
| 💰 预算 | **{budget}元**（{budgetStatus}）|
| 📅 出发日期 | **{departureDate}** |
| 🚀 出发地 | **{departureCity}**（或"待定"）|
| 🏨 住宿偏好 | **{accommodation}** |
| 🏃 节奏 | **{paceDesc}** |

### 兴趣偏好
{preferences badges}

### 指定景点
✅ **必去：** {includeSpots 或 "无"}
❌ **避开：** {excludeSpots 或 "无"}

### 饮食禁忌
{diet 或 "无"}

---

> 以上参数是否准确？如需修改请告诉我，确认后开始为您规划行程 🚀
```