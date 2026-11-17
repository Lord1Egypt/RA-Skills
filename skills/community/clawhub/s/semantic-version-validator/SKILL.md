---
name: semantic-version-validator
description: "Validate semantic versioning (SemVer) strings and recommend the correct version bump (MAJOR/MINOR/PATCH) based on change type.适用于版本校驗、changelog 分級與發布前檢查。"
---

# Semantic Version Validator

驗證版本字串是否符合 SemVer 2.0.0，並根據變更類型推薦正確的版本 bump。

## 規則

### 1. 格式驗證

```
MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]
```

- **MAJOR**：0-99999999 的數字，不可為負
- **MINOR**：0-99999999 的數字，不可為負
- **PATCH**：0-99999999 的數字，不可為負
- **PRERELEASE**：可選，由 `.` 分隔的識別字串（例如 `alpha.1`、`beta.2`、`rc.1`）
- **BUILD**：可選，由 `.` 分隔的識別字串

### 2. Bump 規則

| 變更類型 | Bump | 範例 |
|---|---|---|
| 破壞性 API 變更 | MAJOR | 1.0.0 → 2.0.0 |
| 新功能（向後相容） | MINOR | 1.0.0 → 1.1.0 |
| Bug 修復 | PATCH | 1.0.0 → 1.0.1 |
| 預覽版本 | 附加 prerelease | 1.0.0 → 1.0.1-alpha.1 |

### 3. 預覽版本規則

預覽版本識別字必須只包含 ASCII 字母數字和連字號 `[0-9A-Za-z-]`。
預覽版本比較：數字識別字 < 字母識別字，數字識別字之間做數值比較。

### 4. 約束

- 0.y.z 表示初始開發階段，任何版本都可能變更
- 1.0.0 定義公開 API
- 版本號遞增時，MAJOR/MINOR/PATCH 各自歸零
