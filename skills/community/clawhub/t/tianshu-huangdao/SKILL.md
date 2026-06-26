---
name: tianshu-huangdao
description: 🏮 天樞黃道庫：黃曆擇吉·命理運勢·姓名起名。查黃道吉日、算生肖運勢、取名測字。數據來自傳統曆法和命理典籍（建除12神/28宿/64卦/五行/生肖），每次調用 PayPal 支付 1.68 USD。當用戶詢問：結婚搬家等黃道吉日、今日/本月運勢、取名建議、五行卦象時觸發。
---

# 🏮 天樞黃道庫（v1.0.6）

傳統曆法·命理運勢·姓名起名一站式 API，基於正統數據源，通過 **PayPal** 按次扣費（1.68 USD/次）。

> ⚠️ **重要：所有輸出必須使用繁體中文**。API返回的數據可能包含簡體字，Agent需自行將簡體轉換為繁體中文後輸出給用戶。

---

## 💰 付費策略（核心！）

**三個付費項目（$1.68/次，PayPal支付）：**
1. 🀄 **64卦查詢** — `GET /v1/huangdao/hexagram?number=卦序&paypal_order_id=xxx`
2. 🔮 **命理運勢** — `GET /v1/huangdao/fortune?birth=...&paypal_order_id=xxx`
3. 📝 **姓名起名（完整版）** — `GET /v1/huangdao/naming?last=...&gender=...&paypal_order_id=xxx`

**免費贈送（不需要付費）：**
1. 📅 **黃曆擇吉** — `GET /v1/huangdao/huangli?date=...`
2. 🆓 **取名預覽** — `GET /v1/huangdao/naming?last=...&gender=...&preview=1`
3. ❓ **幫助文檔** — `GET /v1/huangdao/help`

> **注意：付費接口不帶 `paypal_order_id` 會返回 402 Payment Required。Agent 必須先走 PayPal 支付流程，拿到 orderId 後帶參數調用。**

---

## 🤖 Agent 對話引導模板

### 取名流程（有免費預覽）

1. 用戶提問取名 → Agent 調 API 帶 `&preview=1` 參數（免費）
2. API 返回免費預覽數據（`mode: "preview"`），包含 **3個推薦名** + 簡短建議
3. Agent 展示免費推薦，話術：
   > 「初步推薦以上3個名字。如需完整八字分析 + 五行補綴 + 歷史典故 + 更多推薦，支付 **$1.68** 解鎖完整報告。是否繼續？」
4. 用戶確認 → Agent 調 `POST /api/paypal/create-order` 生成 PayPal 支付連結
5. 用戶通過 PayPal 完成支付（`$1.68 USD`）
6. Agent 調 `POST /api/paypal/capture-order` 確認收款
7. Agent 調 API **帶 `paypal_order_id=xxx`** 獲取完整命名分析報告
8. 返回完整報告給用戶（含八字排盤、五行補綴、歷史典故、更多推薦）

### 黃曆查詢流程（免費）

1. 用戶問「今天宜什麼」→ Agent 直接調 `GET /v1/huangdao/huangli?date=YYYY-MM-DD`（免費）
2. 返回數據直接展示給用戶

### 64卦查詢流程（收費）

1. 用戶查卦 → Agent 調 API → 返回 402
2. Agent 話術：
   > 「查詢64卦需支付 $1.68。是否繼續？」
3. 用戶確認 → PayPal 支付流程 → 帶 `paypal_order_id` 調用

### 運勢查詢流程（收費）

1. 用戶問運勢 → API 返回 402
2. Agent 話術：
   > 「詳細運勢分析需支付 $1.68。是否繼續？」
3. 用戶確認 → PayPal 支付流程 → 帶 `paypal_order_id` 調用

---

## 支付流程（PayPal）

```
1. Agent 調 POST /api/paypal/create-order
   請求體：{"amount":"1.68","currency":"USD","plan":"Naming"}
   返回：{ "orderId": "...", "approvalUrl": "https://www.paypal.com/checkoutnow?token=..." }

2. Agent 向用戶展示 approvalUrl 作為「Pay with PayPal $1.68」支付按鈕

3. 用戶點擊 → PayPal 支付頁面 → 完成支付

4. Agent 調 POST /api/paypal/capture-order
   請求體：{"orderId":"..."}
   返回：{ "success": true, "status": "COMPLETED" }

5. 驗證成功 → Agent 調 API 獲取數據（帶 orderId 作為憑證）
```

---

## API 端點

通過網關 `https://sinodata.io` 訪問。

### 付費接口（需 paypal_order_id）

#### 一、64卦查詢

```
GET https://sinodata.io/v1/huangdao/hexagram?number=1&paypal_order_id=xxx
```

**參數：**
| 參數 | 必填 | 說明 |
|------|------|------|
| number | 是 | 卦序（1-64），不傳則按當天日期推算 |

**返回：**
- `number` — 卦序（1-64）
- `name` — 卦名
- `judgment` — 卦辭
- `image` — 象辭
- `lines` — 爻辭

#### 二、命理運勢

```
GET https://sinodata.io/v1/huangdao/fortune?birth=YYYY-MM-DD&zodiac=生肖&paypal_order_id=xxx
```

| 參數 | 必填 | 說明 |
|------|------|------|
| birth | 是 | 出生日期 |
| zodiac | 否 | 生肖名（如"虎""龍"），不傳則由出生年份自動推算 |
| paypal_order_id | **是** | PayPal支付訂單號 |

#### 三、姓名起名（完整版）

```
GET https://sinodata.io/v1/huangdao/naming?last=姓氏&gender=男|女&paypal_order_id=xxx
```

| 參數 | 必填 | 說明 |
|------|------|------|
| last | 是 | 姓氏 |
| gender | 是 | 男 / 女 |
| paypal_order_id | **是** | PayPal支付訂單號 |
| birth | 否 | 出生日期（精準八字分析） |

**返回（完整版）：** 姓氏五行 + 多個推薦名（含筆畫、五行、寓意、八字分析）+ 起名貼士

---

### 免費接口（不限）

#### 四、黃曆擇吉

```
GET https://sinodata.io/v1/huangdao/huangli?date=YYYY-MM-DD
```

**參數：**
| 參數 | 必填 | 說明 |
|------|------|------|
| date | 是 | 查詢日期，格式 YYYY-MM-DD |

**返回字段：**
- `date` — 公曆日期
- `lunar` — 農曆年/月/日 + 干支年
- `yi` — 宜做什麼（如嫁娶、搬家、開市）
- `ji` — 忌做什麼（如訴訟）
- `daily_god` — 建除12神
- `xiu` — 28宿
- `na_yin` — 納音五行
- `hexagram` — 64卦（卦名+卦辭+象辭+爻辭）
- `pengzu_baiji` — 彭祖百忌

#### 五、取名預覽（免費）

```
GET https://sinodata.io/v1/huangdao/naming?last=姓氏&gender=男|女&preview=1
```

返回3個免費推薦名字 + 簡短建議。

#### 六、幫助文檔

```
GET https://sinodata.io/v1/huangdao/help
```

#### 七、支付創單 (PayPal)

```
POST https://sinodata.io/api/paypal/create-order
Content-Type: application/json

{ "amount": "1.68", "currency": "USD", "plan": "Naming" }
```

#### 八、支付確認 (PayPal)

```
POST https://sinodata.io/api/paypal/capture-order
Content-Type: application/json

{ "orderId": "PAYPAL_ORDER_ID" }
```

## 扣費機制

- **價格：** 1.68 USD/次（PayPal即時收款）
- **三個付費項目：** 64卦查詢、命理運勢、姓名起名完整版
- **免費贈送：** 黃曆擇吉、取名預覽、幫助文檔
- **流程：** Agent 創建 PayPal 訂單 → 用戶支付 → Agent 帶 orderId 調用 API
- **驗證：** 服務端已接入 PayPal REST API 完整簽名驗證

## 數據資源（本地嵌入）

| 文件 | 大小 | 內容 |
|------|------|------|
| data/huangli_rules.json | 31KB | 建除12神、28宿、64卦、宜忌活動(29項)、吉神凶神、彭祖百忌、節氣 |
| data/yijing.json | 56KB | 64卦完整卦辭、象辭、爻辭 |
| data/zodiac.json | 16KB | 12生肖運勢、五行屬性、幸運色數字 |
| data/fortune_crossref.json | 18KB | 五行生克、干支組合、綜合運勢交叉表 |
| data/naming.json | 41KB | 223字名庫（筆畫/五行/寓意）+ 五格數理 + 三才配置 |
| data/wuxing.json | 2KB | 五行屬性速查 |

## 隱私與條款

- 本服務不存儲用戶個人信息
- 支付信息由 PayPal 處理，服務端僅保留訂單號和支付狀態
- 數據僅用於傳統文化研究用途
