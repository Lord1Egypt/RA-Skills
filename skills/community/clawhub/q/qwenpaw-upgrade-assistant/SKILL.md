---
name: qwenpaw-upgrade-assistant
description: QwenPaw 升級檢查與相容性驗證。用於檢查目前版本、查找最新版本、驗證升級相容性，並提供升級步驟與回滾建議。
metadata:
  version: "1.0.0"
  openclaw:
    requires:
      bins:
        - qwenpaw
        - python3
        - curl
      env: []
---

# QwenPaw Upgrade Assistant

檢查 QwenPaw 版本、驗證升級相容性，並提供安全升級步驟。

## 適用時機

- 升級前檢查
- 版本相容性驗證
- 升級失敗後回滾
- 檢查是否有相依套件需同步更新

## 不做的事

- 不自動執行升級
- 不處理需要登入、API Key 或付費的升級流程
- 不修改系統套件管理器設定

## 檢查流程

每次執行依序跑下列檢查，並產出結構化報告。

### 1. 目前版本

```bash
qwenpaw --version
```

- 預期：印出版本字串
- 異常：無法執行 → 檢查 PATH、安裝狀態

### 2. 最新版本

```bash
curl -s https://pypi.org/pypi/qwenpaw/json | python3 -c "import sys, json; print(json.load(sys.stdin)['info']['version'])"
```

- 預期：取得 PyPI 最新版本
- 異常：網路問題 → 提示稍後再試

### 3. 升級差異

```bash
curl -s https://qwenpaw.agentscope.io/release-notes 2>/dev/null | head -100
```

- 預期：可取得 release notes
- 異常：無法連線 → 跳過此步驟

### 4. 相容性檢查

- 檢查目前自訂技能、插件、MCP 設定是否與目標版本相容
- 檢查已過期或移除的功能

### 5. 備份建議

- 升級前確認已備份重要資料
- 提供備份指令

## 報告格式

```markdown
## QwenPaw Upgrade Assistant Report

- Current Version: <目前版本>
- Latest Version: <最新版本>
- Upgrade Available: <是 / 否>
- Breaking Changes: <有 / 無>

### Compatibility
- Skills: <相容 / 不相容>
- Plugins: <相容 / 不相容>
- MCP: <相容 / 不相容>

### Steps
1. <備份步驟>
2. <升級步驟>
3. <驗證步驟>
```

## 使用範例

```bash
# 執行檢查
qwenpaw upgrade-check
```
