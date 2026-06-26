# Stock Quant Manager - Scoring Rules (v12 - 2026-03-08)

## Core Task
Scan specific industries (New Energy, Power, Semiconductor, Medicine, AI, Robotics, Military, Gold/Silver) and score stocks based on 6 modules.

## Scoring System (Cumulative)

### Module 1: Technical Indicators (Momentum)
- **1.1 MACD Gold Cross:** Previous day MACD (DIF crosses up DEA). [+3]
- **1.2 Magic Nine:** Price closing lower for 8 or 9 consecutive days (bottom signal). [+5]
- **1.3 Mean Reversion:** 5-day MA at lowest point in last 20 days. [+5]

### Module 2: Market Sentiment (Fund Flow)
- **2.1 Aggressive Buy:** Total market up > 65% AND Volume > 1.15x previous day. [+3]
- **2.2 Long-term Watch:** Market down > 7 days, Volume shrinking, Up ratio 45-55%. [-5]
- **2.3 High Volatility (高位震荡):** > 30% of pool stocks have daily amplitude > 3% (2 days). [-5 for ALL]

### Module 3: Market Trend (Environment)
- **3.1 Counter-trend Oversold:** Market index down > 1% in last 3 days. [+3]
- **3.2 Pro-trend Overheated:** Market index up > 1% in last 3 days. [-3]

### Module 4: Industry Theme (Potential)
- **4.1 Outlook Up (景气向上):** Industry in top 10% (inflow/policy support). [+3]
- **4.2 Outlook Down (景气向下):** Industry in bottom 10% (outflow/correction). [-3]

### Module 5: News/Sentiment (Info Gain)
- **5.1 Major Positive:** National policy, big order, earnings beat (last 24h). [+5]
- **5.2 Major Negative (重大利空):** Regulation, major shareholder selling, negative news (last 24h). [-10]
- **5.3 Sudden Positive (突发利好):** War, conflict, earthquake (reconstruction), sudden policy (last 48h). [+6]
- **5.4 Sudden Negative (突发利空):** Pandemic, disaster, negative sudden event (last 48h). [-6]

### Module 6: Industry Selection (Post-Analysis)
- **6.1 Industry Selection (行业优选):** Most frequent industry in Top 200 stocks (after modules 1-5). [+6 for ALL in that industry]

## Final Recommendation Logic
4. 最终输出：
4.1 筛选出总分[评分]最高的 前 3 名。
4.2 除去前3名，再严格按照[评分]的排名段：4-10名，分类别输出符合的股票。
4.3 标签过滤：输出结果中，**保留所有命中的加分项标签，必须去除所有扣分项的标签**（例如：“景气向下”、“高位震荡”等负面标签不可出现），不再限制只展示3个。

### # 输出要求
请直接给出最终分析结果，格式如下：
【 🔔AI投资研究院-每日量化选股 [当日日期+时间]】
【核心选股池 (精选1000)】

🏆 总分TOP3：
1. [股票名称] [代码] 评分：[总得分] [命中标签]
2. [股票名称] [代码] 评分：[总得分] [命中标签]
3. [股票名称] [代码] 评分：[总得分] [命中标签]

🎉 4-10名：
1. [股票名称] [代码] 评分：[总得分] [命中标签]
2. [股票名称] [代码] 评分：[总得分] [命中标签]
3. [股票名称] [代码] 评分：[总得分] [命中标签]
4. ...

📈 今日最有潜力上涨行业板块：[行业优选名称]

## Industries
New Energy, Power, Semiconductor, Medicine, AI, Robotics, Military, Gold/Silver.
