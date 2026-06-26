# Personalized Send

Use `scripts/wechat_send_campaign.py` when each contact needs a different message.

## CSV format

Create a UTF-8 CSV file with at least `contact,message` columns.

```csv
contact,message
张三,你好张三，今晚 8 点开会。
李四,你好李四，资料我已经发你了。
文件传输助手,这是给自己做测试的消息。
```

Run:

```bash
python scripts/wechat_send_campaign.py --csv contacts_messages.csv --verify-title
```

## JSON format

```json
[
  {"contact": "张三", "message": "你好张三，今晚 8 点开会。"},
  {"contact": "李四", "message": "你好李四，资料我已经发你了。"}
]
```

Run:

```bash
python scripts/wechat_send_campaign.py --json contacts_messages.json --verify-title
```

## Notes

- Uses the same desktop WeChat send path as single-send and batch-send
- Runs in serial order
- Writes a summary JSON to `wechat_automation_logs/`
- Supports `--stop-on-error` if the run should abort on first failure
- Version 2 summary JSON adds `status`, `retry_recommended`, `sent_at`, and top-level aggregate summary
