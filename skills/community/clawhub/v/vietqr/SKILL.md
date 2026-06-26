---
name: vietqr
description: Generate VietQR payment image URLs for Vietnamese bank transfers from bank/account details. Use when users ask to create a VietQR link, return a markdown QR preview, or validate VietQR bank/account/amount input.
---

# VietQR

Use the bundled script when the user wants a VietQR payment link or markdown QR preview:

```bash
python3 "{baseDir}/scripts/vietqr.py" --bank <bank> --account <account>
```

Optional flags:

- `--amount <positive_int|k_suffix>` (examples: `10000`, `10k`, `25K`, `2.5k`)
- `--amount <vn_amount>` also supports Vietnamese shorthand and separators (examples: `200.000`, `1,5tr`, `2tr`, `50k`, `500kđ`)
- `--note "<transfer note>"`
- `--account-name "<account holder>"`
- `--template <template>` (default: `compact2`)
- `--markdown` (print `![VietQR](...)`)
- `--list-banks` (print built-in bank aliases like `vcb`, `mb`, `bidv`, `vietinbank`)

Workflow:

1. Ask only for the missing bank, account, amount, or note fields needed for the user's request.
2. Normalize human input before calling the script.
   - Convert shorthand amounts like `10k`, `2.5k`, `1,5tr`, `2tr`, or `200.000` into whole VND amounts.
   - Translate common bank nicknames or abbreviations (including Vietnamese forms with accents) into the bank string the script should receive.
   - Prefer using a clear official bank name when there is any ambiguity.
3. Run the script instead of hand-building the URL.
4. Return the generated URL directly, or the markdown image form when the user wants something they can paste into chat/docs.
5. For chat surfaces that do not render markdown images inline, prefer returning the raw URL.

Keep the script layer small and predictable. Do not rely on the script to understand every human shorthand if the agent can normalize it first.

If the script exits with `Invalid input: ...`, return that reason clearly and ask only for the incorrect field.
