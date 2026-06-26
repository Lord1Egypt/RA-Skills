# 🧠⚡🎯 IMEA Skill - 快速開始

**IMEA** = Integrated Memory Evolution Action  
**版本：** v1.0  
**授權：** MIT（免費開源）

---

## 🚀 5 分鐘快速開始

### 1. 安裝

```bash
clawhub install vicompany/imea-skill
```

### 2. 配置 Agent

喺你嘅 `config.json` 中加入：

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
    "before_action": "scripts/memory-check.sh"
  },
  "heartbeat": {
    "checkMemory": true
  }
}
```

### 3. 重啟 Agent

```bash
openclaw gateway restart
```

### 4. 測試

```bash
bash scripts/memory-check.sh "測試"
```

---

## 📊 核心功能

| 功能 | 說明 |
|------|------|
| **行動前搜索記憶** | 自動檢查 L1+L2+L3 |
| **避免重複犯錯** | Recurrence-Count ≥3 熔斷 |
| **WAL Protocol** | 關鍵信息預寫入 |
| **強制使用機制** | before_action hook |
| **監控指標** | 記憶搜索率、WAL 記錄率 |

---

## 🎯 使用示例

### 示例 1：收到任務

```bash
# 行動前自動執行
bash scripts/memory-check.sh "ClawHub 上架"

# 輸出：
# ✅ 找到 WAL 記錄
# ✅ 無類似錯誤
# ✅ 無高重複錯誤
```

### 示例 2：避免錯誤

```bash
# 如果之前犯過錯
bash scripts/memory-check.sh "上架"

# 輸出：
# 🚨 發現重複錯誤（Recurrence-Count: 3）
# ⚠️ 熔斷機制觸發！需要用戶確認！
```

---

## 📈 監控

**每日檢查：**

```bash
# 檢查 L1 有無今日記錄
ls memory-l1-daily/$(date +%Y-%m-%d).md

# 檢查 WAL 有無更新
tail SESSION-STATE.md

# 檢查錯誤記錄
cat .learnings/ERRORS.md | tail -10
```

---

## 🚨 常見問題

### Q: memory-check.sh 無找到記錄？

**A:** 正常！新任務無記錄係好事。繼續執行但需記錄 WAL。

### Q: 點樣知道有無重複錯誤？

**A:** 腳本會自動檢查 Recurrence-Count，≥3 會熔斷。

### Q: 熔斷後點恢復？

**A:** 
1. 用戶審批
2. 修復問題
3. 測試驗證
4. 恢復運行

---

## 📚 完整文檔

- [SKILL.md](SKILL.md) - 完整技能文檔
- [docs/USAGE.md](docs/USAGE.md) - 使用指南
- [config/triple-memory-system.md](config/triple-memory-system.md) - 三層記憶詳解

---

## 🙏 致謝

多謝 OpenClaw Community 同 ClawHub！

---

**🎉 開始使用：bash scripts/memory-check.sh "開始"**
