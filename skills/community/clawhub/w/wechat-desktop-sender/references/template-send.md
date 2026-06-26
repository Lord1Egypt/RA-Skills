# Template Variable Send

Use `scripts/wechat_send_template_campaign.py` when all recipients share one template but each row provides different variable values.

## CSV example

```csv
contact,name,company
文件传输助手,Koi,小文AI
李义,义哥,Core突击龙虾
```

Run:

```bash
python scripts/wechat_send_template_campaign.py --csv template_contacts.csv --template "{name}你好，我是Koi，关于{company}这边和你打个招呼。" --verify-title
```

## JSON example

```json
[
  {"contact": "文件传输助手", "name": "Koi", "company": "小文AI"},
  {"contact": "李义", "name": "义哥", "company": "Core突击龙虾"}
]
```

Run:

```bash
python scripts/wechat_send_template_campaign.py --json template_contacts.json --template "{name}你好，我是Koi，关于{company}这边和你打个招呼。" --verify-title
```

## Output

Version 2 output includes:
- per-recipient rendered message
- `missing_fields`
- `status`
- `retry_recommended`
- `sent_at`
- top-level aggregate summary
