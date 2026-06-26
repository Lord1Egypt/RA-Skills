# 🧠⚡🎯 Integrated Memory Evolution Action (IMEA)

**版本：** v1.0  
**作者：** Vicompany AI Team  
**授權：** MIT（免費開源）  
**ClawHub:** `vicompany/imea-skill`

---

## 📦 技能概述

**IMEA** 整合咗三個核心系統：

1. **🧠 三層記憶系統** - L1/L2/L3 存儲架構
2. **⚡ 自進化引擎** - 持續改進 + 錯誤學習
3. **🎯 行動模式** - 強制使用機制 + Before Action Checklist

**目標：** 讓所有 Agent 擁有完整嘅記憶、進化、行動能力，唔會再失憶、唔會重複犯錯、唔會無行動。

---

## 🚀 快速開始

### 安裝

```bash
clawhub install vicompany/imea-skill
```

### 配置

喺你嘅 Agent 配置文件（`config.json`）中加入：

```json
{
  "skills": [
    "proactive-agent",
    "self-improvement",
    "openclaw-self-improvement",
    "ontology",
    "auto-memory-save",
    "memory-auto-summarizer"
  ],
  "hooks": {
    "on_session_end": "skills/auto-memory-save/src/auto-saver.py",
    "before_action": "scripts/memory-check.sh"
  },
  "memory": {
    "enabled": true,
    "maxTokens": 4000
  },
  "heartbeat": {
    "enabled": true,
    "intervalMinutes": 5,
    "checkMemory": true
  }
}
```

### 使用

**每次行動前：**

```bash
bash scripts/memory-check.sh "<任務關鍵詞>"
```

---

## 📊 核心組件

### 1️⃣ 三層記憶系統

| 層級 | 目錄 | 用途 | 保留期 |
|------|------|------|--------|
| **L1** | `memory-l1-daily/` | 日常對話記錄 | 7 日 |
| **L2** | `memory-l2-events/` | 重大事件 | 永久 |
| **L3** | `memory-l3-longterm/` | 長期記憶 | 永久 |

### 2️⃣ 自進化引擎

- **proactive-agent** - 主動代理 + WAL Protocol
- **self-improvement** - 持續改進 + 錯誤學習
- **openclaw-self-improvement** - OpenClaw 自進化循環
- **ontology** - 知識圖譜

### 3️⃣ 行動模式

- **Before Action Checklist** - 5 步檢查
- **WAL Protocol** - Write-Ahead Logging
- **熔斷機制** - Recurrence-Count ≥3 自動熔斷
- **監控指標** - 記憶搜索率、WAL 記錄率、L1 寫入率

---

## 🔧 使用流程

```
收到任務
    ↓
執行 memory-check.sh 搜索記憶
    ↓
讀取 L1+L2+L3 相關記錄
    ↓
提取教訓（避免重複錯誤）
    ↓
執行任務（記錄 WAL）
    ↓
完成任務（寫入 L1）
    ↓
每日 23:00 → 分類 → L2
    ↓
每週日 23:59 → 歸檔 → L3
```

---

## 📈 監控指標

| 指標 | 目標 | 熔斷閾值 |
|------|------|----------|
| 記憶搜索率 | 100% | <80% |
| WAL 記錄率 | 100% | <80% |
| L1 寫入率 | 100% | <80% |
| 錯誤重複率 | 0% | ≥3 |

---

## 🚨 異常處理

**熔斷機制：**
- Recurrence-Count ≥3 → 自動熔斷，報告用戶
- 記憶搜索率 <80% → 警告 → 熔斷
- WAL 記錄率 <80% → 警告 → 熔斷
- L1 寫入率 <80% → 警告 → 熔斷

**恢復流程：**
1. 用戶審批
2. 修復問題
3. 測試驗證
4. 恢復運行
5. 記錄教訓

---

## 📝 文件結構

```
workspace/
├── memory-l1-daily/              # L1：日常記憶
├── memory-l2-events/             # L2：重大事件
├── memory-l3-longterm/           # L3：長期記憶
├── SESSION-STATE.md              # WAL：活躍工作記憶
├── .learnings/
│   ├── LEARNINGS.md              # 學習記錄
│   ├── ERRORS.md                 # 錯誤記錄
│   └── FEATURE_REQUESTS.md       # 功能請求
├── scripts/
│   └── memory-check.sh           # 記憶檢查腳本
└── config/
    ├── triple-memory-system.md   # 三層記憶配置
    └── agent-memory-certificate.md  # 強制使用證書
```

---

## 🎯 使用場景

### 場景 1：收到新任務

```bash
# 1. 搜索記憶
bash scripts/memory-check.sh "ClawHub 上架"

# 2. 讀取教訓
cat .learnings/ERRORS.md | grep -A5 "上架"

# 3. 執行任務（記錄 WAL）
# 4. 完成記錄（寫入 L1）
```

### 場景 2：避免重複錯誤

```bash
# 1. 檢查重複錯誤
bash scripts/memory-check.sh "重複錯誤"

# 2. 如果 Recurrence-Count ≥3 → 熔斷
# 3. 如果無重複 → 繼續執行
```

---

## 📚 相關文檔

- [完整使用指南](docs/USAGE.md)
- [三層記憶系統詳解](config/triple-memory-system.md)
- [強制使用證書](config/agent-memory-certificate.md)
- [快速開始](README.md)

---

## 🔄 版本歷史

### v1.0 (2026-04-05)
- ✅ 初始版本
- ✅ 整合三層記憶系統 + 自進化引擎 + 行動模式
- ✅ 提供強制使用機制
- ✅ 提供監控指標 + 熔斷機制

---

## 📄 授權

MIT License - 免費開源，歡迎使用！

---

## 🙏 致謝

- OpenClaw Community
- ClawHub Skill Marketplace
- Vicompany AI Team

---

**🎉 IMEA Skill - 讓 Agent 唔會再失憶！**
