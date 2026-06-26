---
name: SystemTemp
description: "系統溫度監控工具 - 監控系統溫度、CPU 狀態、風扇轉速等硬體資訊"
homepage: https://clawhub.ai/skills/systemtemp
metadata:
  {
    "openclaw":
      {
        "emoji": "🌡️",
        "requires": { "bins": ["node"] },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "SystemTemp",
              "bins": ["temp"],
              "label": "Install SystemTemp (Node.js)",
            },
          ],
      },
  }
---

# Skill: SystemTemp - 系統溫度監控工具

## 概述
監控系統溫度、CPU 狀態、風扇轉速等硬體資訊的完整解決方案。

## 使用時機
- 查詢當前系統溫度
- 監控 CPU 溫度變化
- 檢查風扇狀態
- 歷史溫度查詢
- 溫度閾值告警設定
- 建立監控報表

## 核心指令

### 1. 即時溫度 (`temp`)
```bash
temp
temp all
temp cpu
```
- 顯示所有溫度感測器
- 顯示 CPU 相關溫度
- 顯示平均溫度

### 2. 感測器列表 (`temp sensors`)
```bash
temp sensors
temp sensors -v
```
- 列出所有可用感測器
- 詳細模式顯示詳細資訊

### 3. 歷史溫度 (`temp history`)
```bash
temp history 1h
temp history 24h
temp history 7d
temp max
```
- 查詢過去小時/天的溫度記錄
- 查詢最高溫度

### 4. 告警設定 (`temp alert`)
```bash
temp alert enable 80
temp alert disable
temp alert status
```
- 設定告警閾值（°C）
- 啟用/停用告警
- 查看告警狀態

### 5. 報表 (`temp report`)
```bash
temp report
temp report weekly
temp report monthly
```
- 生成今日溫度報表
- 週報/月報統計

## 儲存方式
- 即時數據：RAM
- 歷史記錄：`~/openclaw_workspace/data/systemTemp.log`
- 告警設定：`~/openclaw_workspace/config/tempAlerts.json`
- 報表：`~/openclaw_workspace/data/reports/`

## 溫度指標

| 指標 | 正常範圍 | 警示範圍 | 危險範圍 |
|------|---------|---------|---------|
| CPU 溫度 | 40-60°C | 60-80°C | >80°C |
| 晶片組 | 35-55°C | 55-75°C | >75°C |
| 平均溫度 | 40-65°C | 65-85°C | >85°C |

## 例句範例

### 即時查詢
- 「系統溫度多少？」
- 「檢查 CPU 溫度」
- 「所有感測器狀態」
- 「平均溫度是多少？」

### 感測器管理
- 「列出所有溫度感測器」
- 「詳細感測器資訊」
- 「哪些感測器超過 70°C？」

### 歷史查詢
- 「過去一小時溫度變化」
- 「今天最高溫度何時？」
- 「昨天溫度記錄」
- 「過去 7 天最高溫度」

### 告警設定
- 「設定溫度超過 80°C 就警告」
- 「停用溫度告警」
- 「告警狀態為何？」

### 報表查詢
- 「今日溫度報表」
- 「這週溫度統計」
- 「本月溫度報告」

## 注意事項
- 溫度感測器因硬體而異
- 持續高溫可能表示散熱問題
- 定期檢查溫度變化趨勢
- 避免在密閉環境長時間高負載運行
