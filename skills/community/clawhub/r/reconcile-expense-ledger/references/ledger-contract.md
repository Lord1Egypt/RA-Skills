# Ledger contract

## Workbook layout

Preserve existing names/layout when migrating. For new ledgers use 交易明细, 分类与账户, 对账记录, 修改历史 and 账本信息. Keep metadata (ledger UUID, schema version, revision, timezone, export baseline reference) distinct from business fields. Preserve every unrelated sheet and custom user column. Do not populate real ledgers with example transactions.

## Transaction fields

Editable helper fields: date (ISO YYYY-MM-DD), merchant, description, amount (positive decimal string), currency (currency code), category, account, type (expense/refund/income/transfer/card_payment), notes.

System fields: transaction_id, created_at, updated_at, source, deleted (boolean), operation_id, statement_match_id, reconciliation_status; optional parent_id/split_group_id. Protect system fields in ordinary upload merges. Explicit delete requests use the mutation workflow rather than trusting an edited system cell. The helper does not merge split structure or extra user columns: inspect those separately and preserve them unless an authorized change requires editing.

Map actual user column names to this contract; normalize native Excel dates/numbers. Missing editable fields normalize to empty strings, so extract complete rows rather than patches. Match IDs, never row position. If IDs do not exist, establish a mapping from available fields; ask about ambiguity before assigning IDs. Never collapse two real equal-amount purchases automatically.

Use user-customizable categories, initially 餐饮、日常采购、交通、住房、水电通讯、购物、旅行、医疗、教育、娱乐、订阅、其他、待分类. Do not collect full card numbers, CVVs or credentials.

## Merge inputs and decisions

BASE, CURRENT and INCOMING are objects with a transactions array of complete normalized rows with unique transaction_id. Verify matching ledger identity and recover the actual BASE independently before invoking the helper. BASE is the common export ancestor, CURRENT the latest persisted main ledger and INCOMING the offline edited copy.

The helper accepts incoming-only field edits, preserves current-only edits, accepts equal concurrent edits, and holds different concurrent values. It preserves current-only additions, flags missing uploaded rows as possible deletions, blocks automatic resurrection and flags same-ID different additions. It proposes editable business values only. It does not authorize writes, handle explicit deletions, prove identity or deduplicate similar purchases. Inspect those separately.

Without a verified BASE, hold ambiguous two-way edits/deletions; import only clear new rows under user authorization after duplicate screening. Self-reported upload revision or timestamps do not prove precedence. Retain the current version guard until final writeback.

## Amounts, refunds and splits

Use positive decimal values with explicit type. Store original and posted dates/currencies separately where needed. A refund reduces net spending; income does not; transfers/card payments are excluded. Normalize signed bank amounts according to the actual statement convention, not a global assumption. Store FX source/date when conversion is requested.

The summary helper expects flat posting rows, not both parent and split children. Exclude parent rows, carry account/currency/type to children, and verify their sum equals parent amount exactly. Treat partial extracted statements or unresolved currency/type as incomplete, not a valid zero.

## Example requests

- 今天用 Gold 买菜花了 36.80 美元。 Read the ledger, infer 日常采购, resolve account or mark 待确认, append, audit, verify and save.
- 把 TX-123 改成 25.36 美元。 Change the uniquely identified row, invalidate incompatible statement match, audit and save.
- 我改了 Excel，核查后更新。 Recover baseline, compare, apply authorized nonconflicting changes, ask about conflicts/missing rows.
- 删除 TX-123。 Recoverably delete the exact row without redundant approval; recalculate summaries.
- 核对这张信用卡账单。 Check extraction and matching, report differences without appending unless asked.
- 分析本月开销。 Calculate from fresh actual ledger by currency and plot without changing transactions.
