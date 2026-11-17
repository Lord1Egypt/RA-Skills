# SimpleERP journal tables (`*_JNL`)

Journal tables store **change history** for their corresponding base table (when naming follows `TABLE` → `TABLE_JNL`). They are defined in `simpleerp-api/db/TABLES.sql` alongside the base table.

## Typical columns

| Column | Role |
|--------|------|
| `JNL_ID` | Surrogate key for the journal row (identity). |
| `JNL_ACTION` | Single-character action code (e.g. insert/update/delete—confirm values in your environment). |
| `ACTION_BY` | Who performed the change (often default `'ADMIN'` in DDL). |
| `ACTION_DATE` | When the journal row was recorded. |
| `MODULE`, `ACTION` | Optional application context strings. |
| `SID` | Optional session identifier. |
| *(mirrored columns)* | Same business columns as the base table at the time of the change (PK/FKs, status, amounts, etc.). |

Not every journal has identical columns; always grep the DDL for the specific `*_JNL` table.

## Discovering the pair

1. Open [table-index.md](table-index.md) for all `*_JNL` names.
2. For column-level DDL: `grep -- "DDL for Table YOUR_TABLE_JNL" simpleerp-api/db/TABLES.sql` (or search in the IDE).

## Example queries (read-only)

Recent changes to a journal (adjust table/column names):

```sql
SELECT JNL_ID, JNL_ACTION, ACTION_BY, ACTION_DATE, MODULE, ACTION
  FROM SIMPLEERP.ACCOUNT_MGR_JNL
 ORDER BY ACTION_DATE DESC
 FETCH FIRST 50 ROWS ONLY;
```

Correlate a live row with history (example pattern—use the real PK column names from DDL):

```sql
SELECT j.*
  FROM SIMPLEERP.ACCOUNT_MGR_JNL j
 WHERE j.ACCOUNT_MGR_ID = :id
 ORDER BY j.ACTION_DATE DESC;
```

Use **bind variables** (`:id`) where possible; avoid string-concatenated user input. The skill’s **`run-sql.mjs` is query-only** and does not accept bound parameters in argv—keep literals safe or use SQLcl for parameterized sessions.

## Changes to data

The **simpleerp-db** skill is for **read-only queries** only. Journals are usually filled by **triggers** when rows change through the application or other tools. To **insert, update, or delete** data, use a DBA client (SQLcl, SQL*Plus) or your application’s normal workflows—not `run-sql.mjs`.
