---
name: statistical-arbitrage
description: >
  統計套利（配對交易）專業策略 - 計算動態對沖比率、執行回測並生成完整報告。
  支持港股（.HK）、美股（無後綴或預設）、A股（.SS/.SZ）等多市場。
  Use when: 用戶說「分析統計套利策略」、「幫我回測AAPL和GOOGL」、「配對交易回測」。
  NOT for: 單股票分析、趨勢交易、期貨套利、股票掃描。
metadata:
  openclaw:
    emoji: "📊"
    requires:
      bins: ["python3"]
---

# 統計套利（配對交易）專業策略

本 Skill 提供完整的統計套利（配對交易）策略分析框架，適用於港股、美股、A股等多個市場。自動執行協整檢驗、動態對沖比率計算、回測績效評估，並生成專業圖表報告。

## 核心功能

1. **多市場支持**
   - 港股：`.HK` 後綴（如 `1398.HK`, `0939.HK`）
   - 美股：無後綴或預設（如 `AAPL`, `GOOGL`, `MSFT`）
   - A股：`.SS`（上交所）`.SZ`（深交所）

2. **智能參數配置**
   - 默認參數已優化，支持自定義調整
   - 入場閾值、出場閾值、止損線可配置

3. **完整分析流程**
   - 數據下載與清洗（自動過濾假交易日）
   - 協整關係檢驗（ADF + Johansen）
   - 靜態/動態對沖比率計算
   - Z-Score 信號生成
   - 回測執行與績效評估

4. **專業輸出**
   - 6種專業圖表（PNG格式）
   - HTML互動報告
   - CSV 數據導出
   - 績效摘要（夏普比率、最大回撤、Calmar比率等）

## When to Run

### 觸發場景
- **直接請求**："幫我分析 AAPL 和 GOOGL 的統計套利策略"
- **參數配置**："用入場閾值2.5回測1398.HK和0939.HK"
- **時間範圍**："分析2020年到現在的TSLA和NVDA配對交易"

### 非觸發場景
- 單一股票技術分析
- 基本面估值
- 期貨或加密貨幣套利
- 高頻交易策略

## Workflow

### 步驟1：解析用戶意圖
AI 解析用戶輸入，提取：
- 股票代碼對（支持多種格式）
- 時間範圍（默認：2020-01-01 至今日）
- 參數配置（可選）

### 步驟2：環境檢查與依賴安裝
```bash
# 檢查 Python 環境
python3 --version

# 安裝必要套件（如果缺失）
pip install yfinance pandas numpy statsmodels matplotlib --quiet
```

### 步驟3：執行策略分析
```bash
# 運行主腳本
python3 scripts/statistical_arbitrage.py \
  --stock1 <股票1> \
  --stock2 <股票2> \
  --start <開始日期> \
  --end <結束日期> \
  --entry <入場閾值> \
  --exit <出場閾值> \
  --stop <止損閾值> \
  --capital <初始資金> \
  --output <輸出目錄>
```

### 步驟4：生成報告與圖表
腳本自動生成：
1. `1_Price_Comparison.png` - 股票價格走勢對比
2. `2_Normalized_Price.png` - 標準化價格
3. `3_ZScore_Signals.png` - Z-Score時序圖與交易信號
4. `4_Equity_Drawdown.png` - 回測資金曲線與回撤
5. `5_Monthly_PnL.png` - 每月損益熱力圖
6. `6_Beta_Distribution.png` - 動態對沖比率分布
7. `report.html` - 互動式HTML報告
8. `raw_data.csv`, `trades.csv`, `metrics.csv` - 原始數據導出

### 步驟5：返回結果
AI 整理分析結果，包括：
- 協整檢驗結果（p值、是否顯著）
- 對沖比率（β值）
- 當前Z-Score與交易信號
- 回測績效摘要
- 圖表預覽與下載連結

## Output Format

### 文本輸出格式
```
📊 統計套利分析報告
──────────────────────
股票對：AAPL vs GOOGL
時間範圍：2020-01-01 至 2026-03-23
共同交易日：1,519天

🔬 協整檢驗
- p值：0.0021 ✅ 顯著
- R²：0.852

📐 對沖比率
- 靜態 β：1.0234
- 動態 β範圍：[0.95, 1.08]

🎯 當前信號
- Z-Score：-1.24
- 狀態：接近做多區域（閾值±2.0）

📈 回測績效（測試集）
- 總回報：+8.52%
- 年化回報：+1.42%
- 夏普比率：0.68
- 最大回撤：-3.21%
- 勝率：52.0%
- 交易次數：24

💾 報告已生成：
- 圖表目錄：/path/to/output/
- HTML報告：/path/to/output/report.html
```

### 錯誤處理
- 股票代碼無效 → 提示正確格式
- 數據下載失敗 → 建議檢查網絡或代碼
- 無協整關係 → 建議其他股票對
- 參數不合理 → 提供默認值建議

## Configuration

### 默認參數
```json
{
  "start_date": "2020-01-01",
  "end_date": "今天",
  "train_ratio": 0.7,
  "entry_threshold": 2.0,
  "exit_threshold": 0.5,
  "stop_loss": 3.5,
  "window_size": 60,
  "transaction_cost": 0.0015,
  "initial_capital": 100000,
  "position_size": 0.5
}
```

### 可調整參數
| 參數 | 描述 | 建議範圍 |
|------|------|----------|
| entry_threshold | Z-Score入場閾值 | 1.5–3.0 |
| exit_threshold | Z-Score出場閾值 | 0.3–1.0 |
| stop_loss | 止損閾值 | 3.0–5.0 |
| window_size | 動態β計算窗口 | 30–90天 |
| transaction_cost | 交易成本（單邊） | 0.001–0.003 |

## Examples

### 示例1：基本分析（美股）
```
User: Analyze AAPL vs GOOGL statistical arbitrage
AI: Running analysis for AAPL vs GOOGL...
    Period: 2020-01-01 to 2026-03-23
    Entry: +/-2.0, Exit: +/-0.5, Stop: +/-3.5
    (Results: p-value, Z-Score, Sharpe, etc.)
```

### 示例2：自定義參數（港股）
```
User: 幫我用入場2.5、止損4.0回測1398.HK和0939.HK
AI: 好的，使用入場閾值2.5、止損4.0回測1398.HK和0939.HK...
    (分析完成，輸出報告)
```

### 示例3：指定時間範圍
```
User: Analyze TSLA and NVDA from 2022
AI: Analyzing TSLA vs NVDA (2022-01-01 to today)...
    (Analysis complete with full report)
```

## Dependencies

### 系統依賴
- Python 3.8+
- pip（Python包管理器）

### Python包
- yfinance：股票數據下載
- pandas：數據處理
- numpy：數值計算
- statsmodels：統計檢驗
- matplotlib：圖表生成

### 自動安裝
如果缺少依賴，Skill會自動嘗試安裝：
```bash
pip install yfinance pandas numpy statsmodels matplotlib
```

## Troubleshooting

### 常見問題
1. **數據下載失敗**
   - 檢查網絡連接
   - 確認股票代碼正確
   - 嘗試縮短時間範圍

2. **依賴安裝失敗**
   - 確保Python 3.8+
   - 使用 `pip install --upgrade pip`
   - 嘗試單獨安裝每個包

3. **無協整關係**
   - 嘗試不同股票對
   - 調整時間範圍
   - 考慮行業相關性

4. **圖表生成失敗**
   - 檢查matplotlib安裝
   - 確保有寫入權限
   - 嘗試減少數據量

### 調試命令
```bash
# 檢查環境
python3 --version
pip list | grep -E "yfinance|pandas|statsmodels|matplotlib"

# 手動測試
python3 scripts/statistical_arbitrage.py --stock1 AAPL --stock2 GOOGL
```

## Security Notes

- 所有數據處理在本地進行
- 不收集或上傳用戶數據
- 股票數據來自公開API（yfinance）
- 腳本開源可審計

---

**版本**：1.0.3  
**更新日期**：2026-03-28  
**作者**：統計套利策略團隊  
**支持**：通過OpenClaw對話獲取幫助
