---
name: skill-security-vet
description: 技能安全審核 - 整合本地掃描 + VirusTotal 雲端威脅情報
metadata:
  openclaw:
    requires:
      bins: ["bun"]
    install:
      - id: bun
        kind: bun
        label: "Bun (已安裝)"
---

# Skill Security Vet - 技能安全審核系統

整合本地安全掃描 + VirusTotal 雲端威脅情報，自動審核已安裝技能的安全性。

## 功能

- 🔍 **本地掃描** - 檢測危險函數和模式
- ☁️ **VirusTotal 掃描** - 雲端 70+ 防毒引擎比對
- 📊 **風險評級** - 高/中/低/資訊 四級分類
- 🔑 **API Key 管理** - 安全儲存 VirusTotal API Key

## 掃描項目

### 🔴 高風險 (本地)
- `eval()`, `new Function()` - 動態程式碼執行
- `child_process.exec()` - 系統命令執行
- `process.exit()` - 強制終止進程
- 敏感路徑存取 (`/etc/passwd`, `~/.ssh/`, etc.)

### ☁️ VirusTotal 檢測
- 70+ 防毒引擎掃描結果
- 惡意軟體家族分類
- 威脅評級分數

## 使用方式

### 首次設定 VirusTotal API Key
```bash
skill-security-vet config --api-key <YOUR_VT_API_KEY>
```

### 取得 VirusTotal API Key
1. 前往 https://virustotal.com
2. 註冊/登入帳號
3. 進入 Profile → API Key
4. 複製 API Key

### 掃描所有技能（含 VirusTotal）
```bash
skill-security-vet scan --vt
```

### 只做本地掃描
```bash
skill-security-vet scan
```

### 掃描特定技能
```bash
skill-security-vet scan github,slack --vt
```

### 只顯示高風險
```bash
skill-security-vet scan --severity=high --vt
```

## 輸出範例

```
🔍 技能安全審核系統 v2.0
📁 掃描目錄: ~/.opencode/skill
🎯 目標技能: 78 個
☁️ VirusTotal: 已啟用
──────────────────────────────────────────────────

✅ github - 安全
   ☁️ VT: 0/70 防毒引擎標記 (安全)
   
⚠️ unknown-skill - 警告
   🟡 [本地] 缺少 SKILL.md 描述文件
   ☁️ VT: 0/70 防毒引擎標記 (安全)

🔴 suspicious-skill - 危險
   🔴 [本地] 發現 eval() 動態程式碼執行
   ☁️ VT: 45/70 防毒引擎標記 ⚠️ 惡意!

──────────────────────────────────────────────────
📊 審核報告摘要
   總計: 78 個技能
   ✅ 安全: 75 個
   ⚠️ 警告: 2 個
   🔴 危險: 1 個
☁️ VirusTotal 掃描: 78 個
   ✅ 雲端安全: 77 個
   ⚠️ 雲端可疑: 0 個
   🔴 雲端惡意: 1 個
```

## 安全建議

| 等級 | 說明 | 建議 |
|------|------|------|
| 🔴 雙重危險 | 本地+VT 都危險 | 立即移除 |
| 🔴 本地危險 | 本地掃描發現問題 | 建議移除 |
| ⚠️ 雲端可疑 | VT 標記為可疑 | 需要審核 |
| ✅ 安全 | 全部通過 | 正常使用 |

## 注意事項

- VirusTotal 公開 API 限制：每分鐘 4 次請求
- 免費 API Key 足夠日常使用
- 建議定期執行安全掃描
- 發現高風險請立即審核原始碼
