---
name: ssq-prediction
description: AI Investment Research - Double Color Ball (双色球) Prediction. Fetches historical data, applies Contextual Quantum-like Bayesian Network (CQ-BN) model, and sends Top 10 recommendations to Feishu. Use when user asks for "ssq prediction" or "双色球预测".
metadata:
  openclaw:
    requires:
      bins:
        - openclaw
    env:
      - name: FEISHU_SSQ_GROUP_ID
        description: "Feishu group ID to deliver the prediction report. If not set, output is shown in chat."
        required: false
---

# Double Color Ball Prediction (SSQ)

This skill automates the prediction of Double Color Ball (双色球) lottery numbers using a "Contextual Quantum-like Bayesian Network" (CQ-BN) model simulation.

## Dependencies

- **`openclaw` CLI**: Required for Feishu message delivery. This is provided by the OpenClaw platform itself.
- **Feishu authentication**: This skill uses OpenClaw's existing Feishu integration (already configured at the platform level). No additional credentials or tokens are required.
- **`FEISHU_SSQ_GROUP_ID`** *(optional)*: Set this environment variable to your target Feishu group ID to enable automatic delivery. If not set, the report is output directly in the current chat session.

## Configuration

| Variable | Required | Description |
|---|---|---|
| `FEISHU_SSQ_GROUP_ID` | No | Feishu group ID for report delivery |

## Workflow

1. **Data Acquisition**
   - Fetch recent 200 periods of SSQ historical data from:
     ```
     https://datachart.500.com/ssq/history/newinc/history.php?start=24001&end=24200
     ```
   - Adjust `start` and `end` parameters dynamically to retrieve the most recent 200 periods.

2. **Model Execution (CQ-BN Simulation)**
   - **Context**: You are a quantum physicist building a mathematical model.
   - **Logic**:
     - **Interference Term**: Calculate "constructive interference" zones between red balls.
     - **Hilbert Space Mapping**: Map red balls (1–33) to a Hilbert space; identify high-energy "potential wells".
     - **Phase Collapse**: Predict the "collapse point" of probability waves for the next draw.
   - **Refinement**:
     - Generate an initial **Top 20** combinations.
     - Analyze frequency of numbers in the Top 20 to find the "resonance" set (most frequent numbers).
     - Re-combine high-frequency numbers to form a final **Top 10**.

3. **Output Formatting**

   Generate a report with the following structure:

   ```
   【 🔔AI投资研究院-双色球预测 [YYYY-MM-DD]】

   ### 【上下文相关量子贝叶斯网络模型 (Contextual Quantum-like Bayesian Network, CQ-BN)】

   **模型运行报告：**
   - 数据已映射至 Hilbert 空间
   - 在 [区间] 检测到量子干涉
   - 概率波坍缩点预测完成

   **Top 10 推荐组合：**
   1. 红球：[R1]、[R2]、[R3]、[R4]、[R5]、[R6]，蓝球：[B1]
   2. ...

   ⚠️ 风险提示：量子概率坍缩具有随机性，模型结果仅供数学研究参考，不构成绝对投资建议。请理性购彩。
   ```

4. **Delivery**
   - If `FEISHU_SSQ_GROUP_ID` is set, send the report to that Feishu group via OpenClaw's built-in Feishu integration:
     ```bash
     openclaw message send --channel feishu --target "$FEISHU_SSQ_GROUP_ID" --message "<report>"
     ```
   - Authentication is handled by OpenClaw's platform-level Feishu configuration — no extra tokens needed.
   - If `FEISHU_SSQ_GROUP_ID` is not set, output the report directly in the current chat session.
