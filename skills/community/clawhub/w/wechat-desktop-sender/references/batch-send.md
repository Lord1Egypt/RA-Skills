# Batch Send

## Direct contacts list

```bash
python scripts/wechat_send_batch.py --to "张三,李四,文件传输助手" --message "晚上 8 点开会"
```

## Contacts from file

Create `contacts.txt` with one contact/group per line.

```text
张三
李四
文件传输助手
```

Run:

```bash
python scripts/wechat_send_batch.py --contacts-file contacts.txt --message "晚上 8 点开会"
```

## Main flags

- `--message` required
- `--delay` per-chat UI step delay
- `--between` pause between contacts
- `--verify-title` verify current title
- `--stop-on-error` stop immediately on failure
- `--log-dir` custom log directory

## Output

The script writes logs plus a summary JSON under `wechat_automation_logs/`.

Version 2 summary structure includes:

- `summary.total`
- `summary.success`
- `summary.failed`
- `summary.verified`
- `summary.retry_recommended`
- per-recipient fields like:
  - `status` (`sent_verified` / `sent_unverified` / `failed`)
  - `retry_recommended`
  - `sent_at`
  - `error`
