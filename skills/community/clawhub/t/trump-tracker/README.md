# Trump Tracker & Unreliable Predictor (川普动态监控与不靠谱模型)

## 📖 简介 / Introduction
这是一个专为关注特朗普（Donald Trump）全球动态而设计的智能技能包。它不仅能实时抓取最新的新闻动态，还会应用一个幽默且基于情感分析的“不靠谱模型”来预测言论的执行概率与市场冲击。

This is an AI-powered skill designed to track Donald Trump's global dynamics. It not only captures real-time news but also applies a humorous, sentiment-based "Unreliable Model" to predict the execution probability and market impact of his statements.

---

## 🚀 核心功能 / Core Features
- **🌍 实时监控 (Real-time Monitoring)**: 自动对主流全球新闻源进行采样。 (Auto-sampling global news feeds.)
- **📊 预测模型 (Predictive Model)**: 基于 12+ 种独家“风格关键词”及 TextBlob 情感分析。 (Based on 12+ signature keywords and TextBlob sentiment analysis.)
- **🌐 双语输出 (Bilingual Output)**: 针对所有分析结果提供中英双语对照。 (Provides English & Chinese reports for all analysis.)

---

## 📝 运行结果示例 / Example Output

```text
==================================================
🇺🇸 川普不靠谱模型 / Trump Unreliable Model (v1.0)
==================================================
[*] 已捕获到 3 条最新动态，正在进行预测分析...
[*] Captured 3 updates, running predictive analysis...

📊 动态 1 / Update 1:
   📢 Title: Trump takes executive action to pay TSA workers, blames 'Democrat Chaos'
   ├─ 不靠谱指数 / Unreliability: 50.5
   ├─ 预期执行率 / Exec Probability: 49.5%
   ├─ 市场冲击力 / Market Impact: ⚖️ 常规变动 (⚖️ Routine Fluctuations)
   └─ 模型点评 / AI Comment:
      [CN]: 中规中矩：看起来像是个认真写的推特/言论。
      [EN]: Standard: Seems like a carefully drafted tweet or statement.
------------------------------------------------------------
📊 动态 2 / Update 2:
   📢 Title: Trump extends Iran deadline to April 6, says talks are 'going very well'
   ├─ 不靠谱指数 / Unreliability: 60.8
   ├─ 预期执行率 / Exec Probability: 39.2%
   ├─ 市场冲击力 / Market Impact: ⚖️ 常规变动 (⚖️ Routine Fluctuations)
   └─ 模型点评 / AI Comment:
      [CN]: 中度不靠谱：逻辑极其跳跃，存在反转可能。
      [EN]: Moderately Unreliable: Wild logical leaps, high possibility of reversal.
------------------------------------------------------------
```

---

## 🛠️ 安装与运行 / Usage
你可以直接运行一键安装脚本来配置所需依赖： (Run the one-click installer to set up everything:)

```bash
python install_deps.py
```

执行分析命令： (Run the analysis command:)

```bash
python scripts/trump_predictor.py
```

