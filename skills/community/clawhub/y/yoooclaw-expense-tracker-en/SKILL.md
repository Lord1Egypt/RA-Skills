---
name: yoooclaw-expense-tracker-en
description: Extract personal consumption transactions (takeaway, express delivery, payment, shopping, taxi, gas, credit card repayment, transfer, etc.) from mobile phone notifications, summarize them by category and time, and give the total amount. Trigger: How much you spent/expense/consumption/bill/expense/expenditure/this week/this month/last month/recently/today + spend/money/consumption/how much you spent on takeout/how much you spent on a taxi/how much gas you paid/how much you paid.
---

# Expense Tracker

## Target

For **individual** users: Your mobile phone is filled with bank text messages, WeChat/Alipay payment notifications, takeout orders, taxi vouchers, and various payment success reminders. This skill extracts these "money-related" notifications, summarizes them according to the two dimensions of **category** and **time**, and gives the **total expenditure**.

Users set summary preferences through the "What to focus on" field of the installation pop-up window, such as: weekly summary, focusing on dining and travel, focusing only on large purchases, etc.

No assumptions are made about specific payment habits, cards or merchants - **all identified from notification data**.

## Data loading strategy

- **First get the notification storage directory through `openclaw ntf storage-path`** (use the Bash tool to run this command, stdout is the absolute path of the directory). All subsequent notification files are directly in this directory and named `YYYY-MM-DD.json`.
- **File naming**: `YYYY-MM-DD.json`, one file per day, including all App notifications on that day
- **Loading priority**: ① The path specified by the user in the prompt > ② `<storage-path>/<YYYY-MM-DD>.json`
- **Time window (dynamically determined according to user's request)**:
  - "How much did you spend today" → Only files corresponding to today's date
  - "How much did you spend yesterday" → Only files corresponding to yesterday's date
  - "This week/this week" → Monday 00:00 to present
  - "Last week" → last Monday to last Sunday
  - "This month/this month" → from the 1st of the current month to the present
  - "Last month" → from the 1st of the previous month to the end of the previous month
  - "Last" / "Last few days" → Default is the last 7 days
  - "last N days" → last N days
  - The user gives a specific date range (such as "5/1-5/7") → strictly as specified by the user
  - Scheduled tasks are determined based on the summary period in "What to Focus on": such as "Weekly Summary" → the past 7 days, "Monthly Summary" → the current month to date- Skip non-existent files without reporting errors
- If `openclaw ntf storage-path` is not available, prompt the user to provide the data path
- If the user specifies a category in the question (such as "How much did you spend on **takeout** this week"), perform category filtering after loading and then display it.

## Input data schema

JSON array, each item:
```json
{"appName":"com.tencent.xin","title":"Group name or contact name","content":"Message content","timestamp":"2026-04-22T10:30:00.000+08:00","appDisplayName":"WeChat"}
```

- `appDisplayName` distinguishes sources: WeChat / SMS / Alipay / UnionPay / Meituan / Ele.me / Didi Chuxing / Email, etc.
- `title` is the sender ("Industrial and Commercial Bank of China", "China Merchants Bank Credit Card", "Meituan Waimai", merchant name, contact name)
- `content` usually contains an amount field (¥X.XX / X.XX Yuan / RMB X.XX)

## Core logic

### 1. Amount signal recognition

Scan all notifications to identify "payment has occurred" events. Key signals:

- **Bank/Credit Card SMS**: Contains "Consumption/Payment/Debit/Cash Withdrawal/Repayment/POS/Online Banking/Quick Payment ¥X.XX"
- **Payment platform notification** (Alipay, WeChat Pay, Union QuickPass): payment successful/transfer received/receipt/refund
- **Takeaway order** (Meituan, Ele.me, etc.): Order paid/delivered + actual payment amount
- **Taxi/Travel**: end of trip + actual payment
- **Gas**: Gas station electronic invoice/gas card deduction SMS
- **Life payment**: "Payment successful" notification for water/electricity/gas/property/broadband/phone recharge
- **Express delivery fee**: Cainiao Station/Fengchao pickup fee, overtime storage fee
- **Online shopping order confirmation** (Taobao / JD.com / Pinduoduo / Vipshop, etc.): Payment success notification
- **Shopping mall/offline card swiping**: POS consumption in bank SMS
- **Transfer**: WeChat transfer and Alipay transfer to individuals (**marked separately**, not mixed with consumption)
- **Refund/Cashback/Red Packet Return**: Included in the corresponding category as a **negative value**, affecting the category and total amount

Each event extracts: `{time, source App, merchant/title, amount, category, remarks}`.### 2. Automatic classification of categories

| Emoji | Category | Typical sources |
|---|---|---|
| 🍱 | Food and beverage delivery | Meituan / Ele.me / Credit card payment at restaurants / Coffee and milk tea |
| 📦 | Express Logistics | Cainiao / Fengchao / SF Shipping / Pickup Fee |
| 🏠 | Living payment | Water, electricity and gas / Property / Broadband / Telephone bill |
| 🚗 | Transportation | Didi/Amap Taxi/Subway/High Speed Rail/Refueling |
| 🛒 | Shopping | Taobao / JD.com / Pinduoduo / Shopping mall credit card |
| 💳 | Credit card repayment | Credit card repayment SMS, loan deduction |
| 🔁 | Transfer | WeChat/Alipay transfer to individuals (**separate statistics from consumption**) |
| 🎓 | Education | Training institutions / Extracurricular class payment |
| 💊 | Medical | Hospital / Pharmacy / Physical Examination |
| 🎁 | Others | Not clearly classified as above |

If the category cannot be determined, it will be classified as 🎁 Others, **don’t force it**.

If the user specifies key categories in "What to focus on" (such as "Focus on dining and travel"), these categories will be placed at the top and highlighted in the output.

### 3. Remove duplicates

The same transaction is often pushed repeatedly by multiple notifications (bank SMS + payment platform app + merchant applet). Deduplication rules:
- **Amounts are exactly the same + Merchant keywords overlap** → Treat as the same transaction, retain the one with the most complete information (Prioritize bank SMS > Payment platform > Merchant notification)
- Don't count "pending payment reminder" and "payment successful" twice

### 4. Output view (switch according to user's request)

**A. Overview mode** ("How much you spent recently/How much you spent today/How much you spent this week")
Both segments are given by category + by date.

**B. Single category model** ("How much did you spend on takeaways this week / How much did you spend on taxi rides this month")
Only display this category and list details by date.

See the output template below for details.

## Filter rules

- **Marketing/Coupon/Sum Discount Push** ("Save X Yuan immediately", "Discount Y when you spend X Yuan", "X Yuan red envelope to be received", "Cash back X Yuan activity") → Discard. **Only look at actual payments. **
- **Bill Generation Reminder** ("Your credit card bill has been generated ¥X, repayment date...") → Not included in "how much you spent"; if the user asks "how much more to repay", it will be listed separately; the main process of this skill is **not included in the total amount**.
- **If there is no amount or merchant** in the quota/balance change notification → be included in the "To be confirmed" section and will not be included in the total amount.- **Changes in stock/fund/financial management income** → Not counted as consumption, discarded.
- **Pure operational push, new product recommendations, and live broadcast previews from Xiaohongshu/Pinduoduo/Douyin** → Discard.
- **Refunds marked separately**: Presented in the form of `(Refund -¥X.XX)` at the end of the entry and offset the total amount.
- **Personal transfers are separated into blocks**: WeChat/Alipay transfers to family and friends are placed in the "🔁Transfer" block, **not included in the "Total Consumption Expenditure"**, but the "Total Transfers" are given separately.

## Output template

### A. Overview mode

```
💰 Consumption summary (YYYY-MM-DD ~ YYYY-MM-DD)

Total expenditure: ¥X,XXX.XX (N transactions in total)
Total transfers (excluding expenses): ¥X,XXX.XX (M transactions)

━━ By Category ━━

  🍱 Catering takeaway ¥XXX.XX (N items)
  🛒 Shopping ¥XXX.XX (N items)
  🚗 Travel and transportation ¥XXX.XX (N transactions)
  🏠 Living payment ¥XXX.XX (N transactions)
  📦 Express logistics ¥XX.XX (N items)
  💳 Credit card repayment ¥XXX.XX (N transactions)
  ...

━━ By date ━━

  M/D (week X)¥XXX.XX
    🍱 Meituan Takeout ¥XX.XX <store name>
    🚗 Didi Taxi ¥XX.XX <route/starting point>
    🛒 Taobao ¥XX.XX <product name>
  M/D (week X)¥XXX.XX
    ...

━━ To be confirmed ━━ (if any)
  ☐ <Source>: <Original Abstract>, Amount Unidentified
```

### B. Single category mode

```
🍱 Catering takeaway (YYYY-MM-DD ~ YYYY-MM-DD)

Total: ¥XXX.XX (N pens)

  M/D (week X)
    Meituan Takeout ¥XX.XX <store name>
    Luckin ¥XX.XX
  M/D (week X)
    Are you hungry ¥XX.XX <store name>
  ...
```

## Quality Constraints

- Payment/debit/order notifications containing amount keywords (¥ / yuan / RMB / `\d+\.\d{2}`) should be extracted and classified **100%**
- **Duplication removal**: The same transaction cannot be counted twice (typical counterexample: bank SMS + Alipay App notifies ¥38.50 Meituan payment at the same time)
- **Self-consistent total amount**: Total by category = Total by date = "Total expenditure" at the top
- Use a negative amount to offset the refund, and indicate "(Refund)" in the remarks- **Don't make it up**: If there is no amount or merchant in the notice, don't fill it in, put it in "To be confirmed"
- Strictly segment transfers and consumption to avoid counting money transferred to relatives and friends as "spent"
