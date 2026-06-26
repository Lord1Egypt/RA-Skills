# 統計套利（配對交易）專業策略 Skill

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue.svg)](https://clawhub.com)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-green.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

專業的統計套利（配對交易）策略分析工具，支持港股、美股、A股等多個市場。自動執行協整檢驗、動態對沖比率計算、回測績效評估，並生成專業圖表報告。

## ✨ 核心功能

### 📊 多市場支持
- **港股**：`.HK` 後綴（如 `1398.HK`, `0939.HK`）
- **美股**：無後綴或預設（如 `AAPL`, `GOOGL`, `MSFT`）
- **A股**：`.SS`（上交所）`.SZ`（深交所）
- **其他**：加拿大（`.TO`）、歐洲市場

### 🔬 完整分析流程
1. **數據下載**：自動下載股票歷史數據
2. **協整檢驗**：ADF + Johansen 協整關係檢驗
3. **對沖比率**：靜態與動態對沖比率計算
4. **信號生成**：Z-Score 標準化信號
5. **回測執行**：完整交易回測與績效評估
6. **報告生成**：專業圖表 + HTML 互動報告

### 📈 專業輸出
- **6種專業圖表**（PNG格式）
- **HTML互動報告**（可在瀏覽器查看）
- **Excel數據導出**（原始數據 + 交易記錄）
- **績效摘要**（夏普比率、最大回撤、Calmar比率等）

## 🚀 快速開始

### 安裝方式
```bash
# 通過 ClawHub 安裝
npx clawhub@latest install statistical-arbitrage

# 或手動安裝
git clone https://github.com/your-repo/statistical-arbitrage-skill.git
cd statistical-arbitrage-skill
pip install -r requirements.txt
```

### 基本使用
在 OpenClaw 中直接對話：

```
用戶：幫我分析 AAPL 和 GOOGL 的統計套利策略

AI：正在分析 AAPL 和 GOOGL 的統計套利策略...
     時間範圍：2020-01-01 至 2026-03-23
     參數：入場閾值±2.0，出場閾值±0.5，止損±3.5
     （分析完成，輸出報告）
```

### 命令行使用
```bash
python scripts/statistical_arbitrage.py \
  --stock1 AAPL \
  --stock2 GOOGL \
  --start 2020-01-01 \
  --end 2026-03-23 \
  --entry 2.0 \
  --exit 0.5 \
  --stop 3.5 \
  --capital 100000 \
  --output ./my_report
```

## 📋 使用示例

### 示例1：港股銀行股分析
```
用戶：分析工行和建行的配對交易

AI：正在分析 1398.HK 和 0939.HK...
     協整檢驗：p值=0.0009 ✅ 顯著
     對沖比率：β=0.9954
     當前Z-Score：-0.68（無信號）
     回測年化：+0.29%，夏普：0.142
```

### 示例2：美股科技股分析
```
用戶：用入場2.5、止損4.0回測TSLA和NVDA

AI：使用自定義參數分析 TSLA 和 NVDA...
     協整檢驗：p值=0.0123 ✅ 顯著  
     當前Z-Score：-2.31 🚨 做多信號
     回測年化：+3.21%，夏普：0.89
```

### 示例3：指定時間範圍
```
用戶：分析2022年到現在的騰訊和阿里的配對交易

AI：分析 0700.HK 和 9988.HK (2022-01-01至今)...
     協整檢驗：p值=0.0456 ✅ 顯著
     當前Z-Score：1.87（接近做空區域）
```

## 🛠️ 參數配置

### 默認參數
| 參數 | 默認值 | 描述 |
|------|--------|------|
| `entry_threshold` | 2.0 | Z-Score入場閾值 |
| `exit_threshold` | 0.5 | Z-Score出場閾值 |
| `stop_loss` | 3.5 | Z-Score止損閾值 |
| `window_size` | 60 | 動態β計算窗口 |
| `transaction_cost` | 0.0015 | 單邊交易成本 |
| `initial_capital` | 100,000 | 初始資金 |
| `position_size` | 0.5 | 單次倉位比例 |

### 參數建議範圍
- **入場閾值**：1.5–3.0（值越大，信號越少但質量越高）
- **出場閾值**：0.3–1.0（值越小，持倉時間越短）
- **止損閾值**：3.0–5.0（風險控制）
- **動態窗口**：30–90天（市場變化速度）

## 📊 輸出文件

分析完成後生成以下文件：

```
stat_arb_output/
├── 1_價格走勢對比.png
├── 2_標準化價格.png
├── 3_ZScore信號圖.png
├── 4_權益曲線與回撤.png
├── 5_月度損益熱力圖.png
├── 6_Beta分布圖.png
├── report.html              # 互動式HTML報告
├── raw_data.csv             # 原始數據
├── trades.csv               # 交易記錄
└── metrics.csv              # 績效指標
```

### 圖表說明
1. **價格走勢對比**：兩股票價格走勢對比圖
2. **標準化價格**：以起始日為基準的標準化價格
3. **Z-Score信號圖**：Z-Score時序圖與交易信號標記
4. **權益曲線與回撤**：資金曲線與最大回撤可視化
5. **月度損益熱力圖**：各月份損益顏色編碼
6. **Beta分布圖**：動態對沖比率分布

## 🔧 技術細節

### 算法原理
1. **協整檢驗**：使用 Engle-Granger 兩步法檢驗長期均衡關係
2. **對沖比率**：OLS回歸計算靜態β，滾動窗口計算動態β
3. **Z-Score標準化**：`(價差 - 均值) / 標準差`
4. **交易信號**：
   - Z < -entry_threshold：做多價差（買股票1，賣股票2）
   - Z > entry_threshold：做空價差（賣股票1，買股票2）
   - |Z| < exit_threshold：平倉
   - |Z| > stop_loss：止損平倉

### 績效指標
- **總回報**：策略總收益率
- **年化回報**：年化收益率
- **夏普比率**：風險調整後收益
- **最大回撤**：最大資金回撤幅度
- **Calmar比率**：年化收益 / 最大回撤
- **勝率**：盈利交易比例
- **盈虧比**：平均盈利 / 平均虧損

## 📝 使用限制

### 數據限制
- 依賴 yfinance API，數據質量取決於 Yahoo Finance
- 港股假期可能產生假交易日（自動過濾）
- 最少需要100個共同交易日

### 策略限制
- 僅適用於存在長期均衡關係的股票對
- 不適用於趨勢明顯的單邊市場
- 高波動期可能觸發頻繁止損

### 系統要求
- Python 3.8+
- 至少4GB RAM
- 穩定的網絡連接

## 🚨 風險提示

1. **回測不代表未來表現**：歷史績效不保證未來收益
2. **過擬合風險**：參數可能過度優化歷史數據
3. **交易成本**：實際交易成本可能高於假設
4. **流動性風險**：極端市場條件下可能無法成交
5. **數據延遲**：實盤數據可能有延遲

**僅供參考，不構成投資建議**

## 🤝 貢獻指南

歡迎貢獻代碼、報告問題或提出建議：

1. Fork 本項目
2. 創建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

## 📄 許可證

本項目採用 MIT 許可證 - 查看 [LICENSE](LICENSE) 文件了解詳情。

## 📞 支持

如有問題或建議：

- 在 OpenClaw 中直接提問
- 提交 [GitHub Issue](https://github.com/your-repo/statistical-arbitrage-skill/issues)
- 查看 [在線文檔](https://your-docs-site.com)

---

**版本**：1.0.0  
**更新日期**：2026-03-23  
**作者**：統計套利策略團隊  
**官網**：[https://your-website.com](https://your-website.com)