# Data Manifest

This file lists all data assets bundled with the `rocom` skill. All files are **read-only** static JSON containing public game statistics from Bilibili WIKI.

##  Data Directory (`/data`)

| File | Type | Description | Security Status |
| :--- | :--- | :--- | :--- |
| `pets.json` | Static JSON | List of 490+ pets with basic attributes. |  Safe / Read-only |
| `pets_detail_all.json` | Static JSON | Detailed stats, skills, and evolution chains. |  Safe / Read-only |
| `skills.json` | Static JSON | List of 490+ skills with power/cost. |  Safe / Read-only |
| `items.json` | Static JSON | Inventory of 1700+ items and materials. |  Safe / Read-only |
| `dungeons.json` | Static JSON | Dungeon rewards and challenge limits. |  Safe / Read-only |
| `regions.json` | Static JSON | Regional pet distribution and zones. |  Safe / Read-only |
| `formations.json` | Static JSON | Recommended team compositions. |  Safe / Read-only |
| `meta.json` | Static JSON | Versioning and last sync timestamp. |  Safe / Read-only |

##  Security Verification
*   **No Executable Code:** None of these files contain scripts or executable logic.
*   **No External Links:** No URLs or network endpoints are stored in these files.
*   **No Credentials:** No API keys, tokens, or personal data are included.
