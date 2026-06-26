---
name: school-run
description: Manages the School Run Schedule Google Sheet. Use when reading or updating the school run drop-off schedule for Damian and Zachary (date, responsible person, marks).
---

# School Run Sheet Management

This skill provides direct CLI access to the School Run Schedule Google Sheet: `1BCXLhckPWkpnTaRXPNF9j6c2ldWh5MeZ5KgVQVvOyt4`.

## Column Structure (MAR 2026 sheet)

- **Column A:** Date
- **Column B:** Who is responsible for dropping Damian and Zachary off at school
- **Column C:** Marks/Remarks

## Usage Guidelines

- Always check current data before appending or updating.
- Use `gws sheets spreadsheets values get` to inspect specific dates.
- Use `gws sheets spreadsheets values update` to modify existing rows.
- **Dry-run first** for any write operation.

## Command Templates

### Read Schedule for a Date (e.g., Row 11)
```bash
env GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=/home/websterlinus615/.config/gws/service-account.json \
gws sheets spreadsheets values get \
--params '{"spreadsheetId": "1BCXLhckPWkpnTaRXPNF9j6c2ldWh5MeZ5KgVQVvOyt4", "range": "MAR 2026!A11:C11"}'
```

### Update Marks for a Date
```bash
env GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=/home/websterlinus615/.config/gws/service-account.json \
gws sheets spreadsheets values update \
--params '{"spreadsheetId": "1BCXLhckPWkpnTaRXPNF9j6c2ldWh5MeZ5KgVQVvOyt4", "range": "MAR 2026!C11", "valueInputOption": "USER_ENTERED"}' \
--json '{"values": [["NEW_MARKS"]]}'
```

## Troubleshooting

- If API errors occur, verify `spreadsheetId` and sheet tab name ("MAR 2026").
- Ensure `service-account.json` is accessible in `~/.config/gws/`.
