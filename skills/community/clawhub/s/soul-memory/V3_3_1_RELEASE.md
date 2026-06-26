# Soul Memory v3.3.1 Release Notes

## 📦 Release Information
- **Version**: v3.3.1  
- **Release Date**: 2026-02-27
- **Previous Version**: v3.3.0

## 🎯 What's New in v3.3.1

### 🆕 New Feature: Heartbeat Automatic Cleanup
- **Heartbeat 清理腳本** (`clean_heartbeat.py`)
  - 自動清理記憶中的 Heartbeat 報告
  - 減少記憶冗餘和污染
  - 支持多種 Heartbeat 格式識別
  - 自動壓縮多餘空行

- **Cron Job 集成**
  - 每 3 小時自動執行清理
  - 配置由 `install.sh` 自動設定
  - 報告清理統計

### 🔧 Improvements
- 減少 Heartbeat 自我重複問題
- 提高記憶質量評分（預計 8.5/10 → 9.0/10）
- 節省存儲空間

## 📊 Migration from v3.3.0

```bash
# 升級至 v3.3.1
cd /root/.openclaw/workspace/soul-memory
git pull origin main
bash install.sh --rebuild-index
```

## 🔗 Related Issues
- Solves: Heartbeat 自我重複污染記憶
- Improves: 記憶存儲效率
- Enhances: 系統評分（7.9/10 → 8.5/10+）

## 💾 New Files
- `clean_heartbeat.py` - Heartbeat 清理腳本
- `V3_3_1_RELEASE.md` - 本發布說明文件
