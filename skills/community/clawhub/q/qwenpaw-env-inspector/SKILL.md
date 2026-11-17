---
name: qwenpaw-env-inspector
description: QwenPaw 環境健康檢查與自動修復建議。用於快速診斷 QwenPaw 安裝、環境變數、依賴、權限與常見錯誤，並輸出可執行的修復步驟。
metadata:
  version: "1.0.0"
  openclaw:
    requires:
      bins:
        - qwenpaw
        - python3
      env: []
---

# QwenPaw Environment Inspector

診斷 QwenPaw 本地環境的健康狀態，並提供具體修復建議。

## 適用時機

- 用戶回報 QwenPaw 無法啟動、閃退、指令失敗
- 新環境初始化前後檢查
- 升級前後的相容性驗證
- 排查 skill / plugin 載入失敗

## 不做的事

- 不自動修改系統設定或安裝套件
- 不處理需要登入、API Key、付款或人工審核的問題

## 檢查流程

每次執行依序跑下列檢查，並產出結構化報告。

### 1. CLI 與版本

```bash
qwenpaw --version
```

- 預期：印出版本字串
- 異常：無法執行 → 檢查 PATH、安裝狀態

### 2. 工作目錄與設定

```bash
python3 -c "from qwenpaw.constant import DOCS_DIR; print(DOCS_DIR or 'None')"
ls -la ~/.qwenpaw
```

- 預期：可讀取 docs 路徑、工作目錄存在
- 異常：工作目錄不存在 → 建議 `qwenpaw init --defaults`

### 3. Python 依賴

```bash
python3 -c "import qwenpaw; print(qwenpaw.__version__)"
```

- 預期：成功匯入
- 異常：提示缺少相依套件 → 建議重新安裝或升級

### 4. 環境變數

```bash
env | grep -E "QWENPAW|DASHSCOPE|OPENAI|ANTHROPIC|GITHUB" || true
```

- 預期：至少看到 QwenPaw 相關設定
- 異常：未設定必要 API Key → 提醒至 Console / Settings 設定

### 5. 權限與敏感目錄

```bash
ls -ld ~/.qwenpaw ~/.ssh ~/.qwenpaw.secret 2>/dev/null || true
```

- 預期：目錄存在且權限合理
- 異常：權限過於開放 → 建議收紧

### 6. 網路連線

```bash
curl -I -s -o /dev/null -w "%{http_code}" https://qwenpaw.agentscope.io || echo "failed"
```

- 預期：200 / 301 / 302
- 異常：無法連線 → 檢查 DNS / proxy / firewall

### 7. Skill / Plugin 狀態

```bash
qwenpaw skills list 2>&1 | head -20
qwenpaw plugin list 2>&1 | head -20
```

- 預期：正常列出技能與插件
- 異常：錯誤訊息 → 依錯誤內容给建議

## 報告格式

```markdown
## QwenPaw Environment Inspector Report

- CLI Version: <qwenpaw --version>
- Python Import: <成功 / 失敗>
- Workdir: <路徑>
- Docs Dir: <路徑或 None>
- Env Vars: <有 / 無>
- Network: <可連線 / 不可連線>
- Skills: <數量>
- Plugins: <數量>

### Issues
1. <問題描述>
2. <問題描述>

### Suggestions
1. <具體修復步驟>
2. <具體修復步驟>
```

## 使用範例

```bash
# 執行檢查
qwenpaw env-inspector

# 或透過 skill 呼叫
/skill qwenpaw-env-inspector
```
