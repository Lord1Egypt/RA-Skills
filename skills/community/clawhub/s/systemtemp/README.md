# SystemTemp - 系統溫度監控工具

## 📦 基本資訊

- **名稱**: `SystemTemp`
- **版本**: `1.0.0`
- **類型**: 系統溫度監控與告警工具
- **主指令**: `temp`

## 🎯 功能特色

✅ **即時監控** - 查看所有感測器溫度狀態  
✅ **CPU 追蹤** - 專門監控 CPU 相關溫度  
✅ **歷史查詢** - 查詢過去一小時/24 小時/7 天記錄  
✅ **告警系統** - 可設定溫度閾值自動告警  
✅ **報表統計** - 生成日/週/月報表  
✅ **視覺化狀態** - 圖示顯示溫度健康狀況  

## 📋 使用方式

### 即時溫度查詢
```bash
temp                           # 顯示所有感測器
temp all                       # 完整狀態
temp cpu                       # CPU 溫度
temp sensors                   # 感測器列表
temp sensors -v                # 詳細模式
```

### 歷史查詢
```bash
temp history 1h               # 過去一小時
temp history 24h              # 過去 24 小時
temp history 7d               # 過去 7 天
temp max                      # 最高溫度統計
```

### 告警管理
```bash
temp alert enable 80          # 設定閾值 80°C
temp alert disable            # 停用告警
temp alert status             # 查看狀態
```

### 報表生成
```bash
temp report                   # 今日報表
temp report weekly            # 週報
temp report monthly           # 月報
```

## 📁 檔案結構

```
SystemTemp/
├── temp                    # 主指令包裝器
├── temp.js                 # 核心功能腳本
├── SKILL.md                # 技能說明
├── setup.sh                # 安裝腳本
├── package.json            # NPM 配置
└── data/                   # 運行時數據
    ├── systemTemp.log      # 溫度日誌
    ├── systemTemp.md       # README 說明
    ├── reports/            # 報表目錄
    └── config/
        └── tempAlerts.json # 告警設定
```

## 🚀 安裝方式

### 方法 1: 使用 OpenClaw
```bash
cd /home/ckk/.openclaw/workspace/skills/system-temp
./setup.sh
```

### 方法 2: 直接執行
```bash
cd /home/ckk/.openclaw/workspace/skills/system-temp
./temp help
```

### 方法 3: 複製腳本
```bash
cp /home/ckk/.openclaw/workspace/skills/system-temp/temp /usr/local/bin/
cp /home/ckk/.openclaw/workspace/skills/system-temp/temp.js /usr/local/bin/
```

## 🎮 範例對話

### 即時查詢
```
使用者：系統溫度多少？
助理：   🌡️ 系統溫度監控

1. acpitz           72°C / 161°F 🟡
2. acpitz           66°C / 150°F 🟡
3. acpitz           71°C / 159°F 🟡

📊 平均溫度：69°C (溫度偏高)
🟡 狀態：溫度偏高 (平均：69°C)
```

### CPU 溫度
```
使用者：檢查 CPU 溫度
助理：   🔥 CPU 溫度

1. acpitz: 72°C / 161°F
2. acpitz: 66°C / 150°F

CPU 狀態：正常
```

### 歷史查詢
```
使用者：過去一小時溫度變化
助理：   📈 歷史溫度記錄

⏰ 2026-05-01 15:30
🌡️ 平均溫度：69°C

⏰ 2026-05-01 15:45
🌡️ 平均溫度：71°C

📊 統計：
   最高：71°C
   最低：69°C
   平均：70°C
```

### 告警設定
```
使用者：設定溫度超過 80°C 就警告
助理：   ✅ 告警已啟用，閾值：80°C

使用者：系統溫度多少？
助理：   🌡️ 系統溫度監控
1. acpitz           85°C / 185°F 🔥
...
⚠️ 告警：已超過 80°C 閾值！
```

## 📊 溫度狀態指標

| 平均溫度 | 狀態 | 說明 |
|---------|------|------|
| < 65°C | ✅ 正常 | 運作理想 |
| 65-75°C | 🟡 偏高 | 建議檢查 |
| 75-85°C | ⚠️ 高溫 | 需關注 |
| > 85°C | 🔥 危險 | 立即處理 |

## ⚙️ 排程整合

可與已有排程配合：
```bash
# 每小時記錄
0 * * * * /home/ckk/.openclaw/workspace/skills/system-temp/temp >> /tmp/temp.log 2>&1
```

## 📝 注意事項

- 溫度感測器因硬體而異
- 持續高溫可能表示散熱問題
- 建議設定適當告警閾值
- 定期查看溫度變化趨勢

## 📞 支援

- **說明**: `temp help`
- **問題**: 檢查日誌 `~/openclaw_workspace/data/systemTemp.log`
- **配置**: `~/openclaw_workspace/config/tempAlerts.json`

---

**系統溫度，一清二楚！** 🌡️

_最後更新：2026-05-01 15:50_
