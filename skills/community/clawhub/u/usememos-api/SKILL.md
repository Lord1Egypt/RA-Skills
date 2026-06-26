---
name: usememos-api
version: "1.0.3"
description: Interact with UseMemos instance — a lightweight, self-hosted memo hub. Create, search, list memos and upload attachments.
tags: ["memos", "notes", "self-hosted", "knowledge-base", "attachments"]
homepage: https://github.com/minstn/usememos
source: https://github.com/minstn/usememos
metadata:
  openclaw:
    requires:
      env:
        - USEMEMOS_URL
        - USEMEMOS_TOKEN
      bins:
        - python3
    primaryEnv: USEMEMOS_TOKEN
---

# UseMemos

## Setup

Create a `.env` file in the skill directory (`skills/usememos/.env`):
```
USEMEMOS_URL=http://192.168.0.157:5230
USEMEMOS_TOKEN=your_access_token_here
```

Get your ```USEMEMOS_TOKEN``` from UseMemos instance, login and go to: **Settings > My Account > Access Tokens**, create one there, do not forget to assign expiration (i use **Never** to avoid troubles, but hey there are also arguments against that)

**Note:** All scripts automatically load the `.env` file from the skill directory. No need to export variables manually.

## Scripts

| Script | Usage | Description |
|--------|-------|-------------|
| `create_memo.py` | `<content> [visibility]` | Create a memo (visibility: PRIVATE/PROTECTED/PUBLIC) |
| `list_memos.py` | `[limit] [tag]` | List recent memos (default: 10) |
| `search_memos.py` | `<query> [limit]` | Search memos by content |
| `upload_attachment.py` | `<filepath> [filename] [type]` | Upload a file attachment |
| `upload_and_link_attachment.py` | `<memo_id> <filepath> [filename] [type]` | Upload and link attachment to a memo |
| `memo_comments.py` | `<list\|add\|delete> [args...]` | Manage comments on a memo |

All scripts are in `scripts/` and run with `python3 scripts/<script>`.

## Examples

```bash
# Create a memo with tags
python3 scripts/create_memo.py "Meeting notes from standup #work"

# List recent memos
python3 scripts/list_memos.py 5

# Search memos
python3 scripts/search_memos.py "website redesign"

# Upload attachment standalone
python3 scripts/upload_attachment.py photo.jpg "sale_photo.jpg" "image/jpeg"

# Create memo then attach a file
python3 scripts/create_memo.py "Sale: Stromer Charger #eBike #income"
# Use the memo ID from output:
python3 scripts/upload_and_link_attachment.py <memo_id> charger_photo.jpg

# Add a comment to a memo
python3 scripts/memo_comments.py add <memo_id> "Looks great!"

# List comments on a memo
python3 scripts/memo_comments.py list <memo_id>

# Delete a comment
python3 scripts/memo_comments.py delete <comment_id>
```

## Notes

- Memo IDs are short IDs like `3UZ7uBbHsLEAwdYE5HKhjd` (not `memos/3UZ7uBbHsLEAwdYE5HKhjd`)
- Tags use `#tag` syntax inline in memo content
- Default MIME type for attachments is `image/jpeg`; pass the type explicitly for other files. Normally this will be done automatically by openclaw, but sometimes will require some tweaking/

## API Reference

See [references/api.md](references/api.md) for endpoint documentation.
