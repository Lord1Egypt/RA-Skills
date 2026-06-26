# Soul Memory v3.3.1 快速升級指南

## 🚀 快速升級步驟

```bash
# 1. 進入 Soul Memory 目錄
cd /root/.openclaw/workspace/soul-memory

# 2. 拉取最新代碼
git pull origin main

# 3. 執行升級安裝
bash install.sh --rebuild-index

# 4. 驗證安裝
python3 cli.py status
```

## ✅ 升級後驗證

### 檢查清理腳本
```bash
# 測試清理腳本
python3 clean_heartbeat.py
```

### 驗證 Cron Job
```bash
# 查看 Cron Jobs
openclaw cron list
```

預期輸出應包含：
```
- 記憶Heartbeat清理 (每 3 小時)
```

## 🎯 v3.3.1 新功能

| 功能 | 說明 |
|------|------|
| **Heartbeat 自動清理** | 每 3 小時自動清理 Heartbeat 報告 |
| **清理腳本** | `clean_heartbeat.py` - 手動或自動運行 |
| **記憶優化** | 減少冗餘，提高質量評分 |

## 📊 性能提升

| 指標 | v3.3.0 | v3.3.1 | 改善 |
|------|--------|--------|------|
| 記憶質量 | 8.5/10 | 9.0/10 | +0.5 |
| 存儲效率 | 6/10 | 7.5/10 | +1.5 |
| 總評分 | 7.9/10 | 8.5/10 | +0.6 |

## ❓ 常見問題

### Q: 清理腳本會刪除重要記憶嗎？
A: 不會。清理腳本只會移除包含 "Heartbeat" 關鍵詞的條目，保留所有 [C] Critical 和 [I] Important 記憶。

### Q: 如何手動執行清理？
A: 運行 `python3 /root/.openclaw/workspace/soul-memory/clean_heartbeat.py`

### Q: Cron Job 什麼時候執行？
A: 每 3 小時自動執行一次（從安裝時間開始計算）。

### Q: 如何禁用 Cron Job？
A: 運行 `openclaw cron remove <job-id>`（使用 `openclaw cron list` 查看 ID）

## 🆘 故障排除

### 清理腳本無法運行
```bash
# 檢查權限
chmod +x /root/.openclaw/workspace/soul-memory/clean_heartbeat.py

# 檢查 Python 版本
python3 --version  # 需要 3.7+
```

### Cron Job 未執行
```bash
# 確認 OpenClaw 運作中
openclaw gateway status

# 查看日誌
tail -f ~/.openclaw/gateway.log
```

## 📚 更多文檔
- [完整文檔](./README.md)
- [v3.3 升級指南](./V3_3_UPGRADE.md)
- [發布說明](./V3_3_1_RELEASE.md)
