# README.md - 股票查詢技能

## 功能
查詢指定股票代碼的30天每日股價資料。

## 快速開始

### 安裝依賴
```bash
pip install yfinance pandas
```

### 使用方法
```bash
python stock_query.py [股票代碼]
```

### 範例
```bash
# 查詢台積電 (美股代碼)
python stock_query.py TSM

# 查詢港股
python stock_query.py 0001.HK

# 查詢A股
python stock_query.py 000001.SZ
```

## 輸出格式
返回包含以下欄位的CSV檔案：
- Date（日期）
- Open（開盤價）
- High（最高價）
- Low（最低價）
- Close（收盤價）
- Volume（成交量）
- Dividends（股利）
- Stock Splits（股票分割）

## 支援的股票市場
- 美股 (AAPL, TSM, etc.)
- 港股 (0001.HK, 0005.HK, etc.)
- A股 (000001.SZ, 600519.SS, etc.)