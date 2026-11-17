# spec-coverage.yaml：涵蓋度常駐檔案

## 它是什麼

一份跟著專案走的常駐檔案，記錄 41 個考量項目各自的狀態。**不是每次重新推導的報告**，而是持續增量維護的狀態表。

它存在的理由：把「已經考量過」變成可稽核的證據，而不是靠信任。同時它把空洞內容擠出文件正文 —— 沒內容的項目不寫進規格書，改以狀態呈現。

副作用是它同時成為下一輪工作清單：掃一遍 `tbd` 與 `missing`，就知道還缺什麼。

放在 `software-spec/spec-coverage.yaml`，納入版本控制。

---

## Schema

```yaml
project: <專案代號>
updated: <YYYY-MM-DD>
spec_version: <對應的規格版本>

items:
  <項目代號>:
    status: confirmed | draft | tbd | n/a | missing
    file: <相對路徑>            # confirmed / draft 必填
    anchor: <#錨點>             # 選填，指向章節內特定位置
    note: <說明>                # tbd / n/a / draft 必填
    owner: <負責決定的人>        # tbd 必填
    blocks: [<項目代號>, ...]    # 選填，此項未決會卡住哪些項目
```

---

## 各狀態的填寫規則

### confirmed

使用者明確確認過的內容。必填 `file`。

```yaml
  S09:
    status: confirmed
    file: 02-business-design/09-business-rules.md
```

### draft

已寫入文件但未經確認。必填 `file` 與 `note`，`note` 要寫清楚**還缺什麼**，不要只寫「待確認」。

```yaml
  S13:
    status: draft
    file: 03-requirements/13-requirements.md
    note: FR-001~FR-012 已列出，FR-009 與 FR-011 尚無驗收標準
```

### tbd

知道需要，但尚未決定。**不寫進文件**。必填 `note` 與 `owner`。

`note` 必須具體到「需要誰決定什麼」，而不是重述項目名稱。

```yaml
  S28:
    status: tbd
    note: 是否引入 Redis 作為訊息狀態快取？決定後會影響 S17 架構圖與 S33 部署
    owner: <技術負責人>
    blocks: [S33]
```

```yaml
❌ note: Cache 策略待定
✅ note: 是否引入 Redis？決定後影響 S17 架構圖與 S33 部署
```

### n/a

本專案不適用。**必填理由。** 不寫理由的 `n/a` 一律視為無效 —— 這條規則的目的是擋住「為了省事跳過」。

```yaml
  S31:
    status: n/a
    note: 本系統不處理任何檔案上傳，附件由外部平台託管
```

### missing

尚未討論過。由你**主動標記**，這是這份檔案最主要的價值 —— 使用者不會知道自己漏了什麼。

```yaml
  S34:
    status: missing
    note: 尚未討論備份與復原，建議上線前補
```

`missing` 與 `tbd` 的差別：`tbd` 是**已經意識到但還沒決定**，`missing` 是**根本還沒被提起**。

---

## 維護規則

1. **每次文件寫入或修改，同一次任務內更新此檔案。** 不允許「先寫文件、之後再補 coverage」。
2. **只做增量更新，不重建整個檔案。** 重建會遺失 `n/a` 的理由與 `tbd` 的 owner。
3. **項目只能改狀態，不能刪除。** 使用者說「這個不用做」時，改成 `n/a` 加理由，而不是移除條目 —— 否則三個月後沒人記得為什麼沒做。
4. **`tbd` 被解決時**：改為 `confirmed` 或 `draft`、補上 `file`、清除 `owner` 與 `blocks`，並同步更新 S06 的 Open Questions 清單。
5. **`updated` 欄位每次都要改。**

---

## 完整範例

```yaml
project: <專案代號>
updated: 2026-08-17
spec_version: 0.4.0

items:
  S01: { status: confirmed, file: 01-business/01-background.md }
  S02: { status: confirmed, file: 01-business/02-glossary.md }
  S03: { status: missing, note: Persona 尚未定義 }
  S04: { status: confirmed, file: 01-business/04-goals.md }
  S05: { status: draft, file: 01-business/05-business-model.md, note: 收費模式僅列出方向，未定價 }
  S06:
    status: confirmed
    file: 01-business/06-assumptions.md
    note: 含第三方平台的審核與限額限制
  S08: { status: confirmed, file: 02-business-design/08-data-model.md }
  S09: { status: confirmed, file: 02-business-design/09-business-rules.md }
  S10:
    status: draft
    file: 02-business-design/10-state-machines.md
    note: 訊息狀態機已完成，訂單狀態機未定義
  S13:
    status: draft
    file: 03-requirements/13-requirements.md
    note: FR-001~FR-012 已列出，FR-009 與 FR-011 尚無 AC
  S14:
    status: tbd
    note: 效能與可用性目標未量化，卡住 S17 架構與 S28 快取決策
    owner: <產品負責人>
    blocks: [S17, S28]
  S15:
    status: missing
    note: 尚未界定哪些欄位屬個資，涉及顧客對話內容，建議優先處理
  S16:
    status: tbd
    note: 雲端供應商與運算模型未定（Lambda / ECS / Workers），決定前無法定案架構
    owner: <技術負責人>
    blocks: [S17, S21, S33]
  S22:
    status: tbd
    note: 模型選型與 fallback 策略未定，需確認成本上限
    owner: <技術負責人>
    blocks: [S38]
  S31:
    status: n/a
    note: 本系統不處理檔案上傳，附件由外部平台託管
  S34: { status: missing, note: 尚未討論備份與復原，建議上線前補 }
  S38:
    status: tbd
    note: AI 評測基準線需在 S22 模型選型後才能定義
    owner: <技術負責人>
```

未列出的項目視同 `missing`，但**建議明確列出**所有 41 項 —— 一份看得見全貌的檔案才有稽核價值。

---

## 產出摘要

每次任務結束時，從此檔案摘要出三段回報（格式見 SKILL.md）：本次寫入、受影響、仍缺。

不要把整份 YAML 貼進回應 —— 只摘要本次有變動的項目，以及 `tbd` / `missing` 中最該優先處理的兩三項。
