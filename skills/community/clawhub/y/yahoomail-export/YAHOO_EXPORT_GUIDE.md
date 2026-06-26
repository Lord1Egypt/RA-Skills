# Yahoo Mail IMAP Export: Lessons Learned

## Overview

Downloading ~132,000 emails from a Yahoo Mail account via IMAP. This document captures the pitfalls, workarounds, and working solution.

## The Problem

Yahoo Mail's web interface shows 128K+ emails and 9GB of storage. Standard IMAP access only sees a fraction of this.

## Yahoo IMAP Limitations

### 1. SELECT Cap: 10,000 Messages

`imap.mail.yahoo.com` limits `SELECT` (and `EXAMINE`) to **10,000 visible messages**, regardless of actual mailbox size.

```
STATUS INBOX: 131,966 messages
SELECT INBOX: 10,000 messages (capped)
```

This is a **hard server-side limit**. Sequence numbers above 10,000 return `BAD [CLIENTBUG] FETCH Bad sequence in the command`.

### 2. SEARCH Cap: 1,000 Results

Server capability `MESSAGELIMIT=1000` limits `SEARCH` results to 1,000 UIDs per query. Wide searches (e.g., `SINCE "01-Jan-2000"`) hit this cap. Narrow date-range searches return real counts.

### 3. Export Server: 100,000 Messages

`export.imap.mail.yahoo.com` is Yahoo's recommended server for bulk downloads. It lifts the SELECT cap to **100,000 messages**:

```
STATUS INBOX: 100,000 messages (export server)
SEARCH ALL: 100,000 UIDs returned
FETCH seq 50000: Works
FETCH seq 120000: BAD (still capped at 100K)
```

### 4. FETCH on Export Server is Slow

Single-message `FETCH RFC822` on the export server is extremely slow (seconds per message). Batch fetches (`FETCH 1:500 (RFC822)`) hang indefinitely. This makes the export server impractical for direct download of large folders.

### 5. UIDs Are Not Sequential

Message UIDs do not start at 1. In testing:
- Sequence number 1 → UID 648311
- Sequence number 10000 → UID 658525

This means you cannot use UID ranges to "page through" older messages.

## What Doesn't Work

### ❌ Direct IMAP Download of 100K+ Folder

```python
m.select('"INBOX"', readonly=True)  # Returns 10000
# Can only FETCH seq 1-10000, rest are inaccessible
```

### ❌ UID-Based Pagination

UIDs are not sequential and start at arbitrary numbers. Searching `UID 1:10000` returns empty results because UIDs start at ~648311.

### ❌ COPY + DELETE + EXPUNGE

```python
m.copy("1:10000", "export1")  # Returns OK
m.store("1:10000", '+FLAGS', '\\Deleted')
m.expunge()
# Result: export1 gets ~100 messages, not 10000
# Messages are LOST
```

This approach silently loses messages. Do not use.

### ❌ Wide Date-Range Searches

```python
m.search(None, 'SINCE "01-Jan-2000"')  # Returns only 1000 UIDs (cap)
```

## What Works

### ✅ MOVE Command (Small Batches)

Yahoo supports the IMAP `MOVE` extension. It's atomic and reliable for batches up to ~9,000 messages:

```python
# Always move seq 1:N (they shift after each MOVE)
m._simple_command('MOVE', '1:1000', 'export1')  # OK
m._simple_command('MOVE', '1:1000', 'export1')  # OK (next 1000)
# ... repeat up to ~9000 total
# At 10,000: SERVERBUG - MOVE Server error
```

**Key insight**: After each MOVE, sequence numbers shift. Always use `seq 1:N` for the next batch.

**Rate limit**: Yahoo returns `SERVERBUG` at ~9,000 messages per MOVE session. Use 8,999 as batch size.

### ✅ Narrow Date-Range SEARCH + FETCH (Slow)

```python
m.search(None, 'SINCE "01-Jan-2025" BEFORE "01-Feb-2025"')  # Returns real count
# Then FETCH each UID individually
```

Works but slow. Only useful for verification, not bulk download.

### ✅ The Folder Rotation Strategy

The working solution:

1. **Create export folders** (export1, export2, export3)
2. **MOVE 8,999 messages** from INBOX to next available export folder
3. **Download the export folder** (now under 10K, accessible via standard IMAP)
4. **Clear the export folder** (delete all messages)
5. **Rotate to next export folder**
6. **Repeat** until INBOX is empty

```
INBOX (131K) → export1 (8999) → download → clear
             → export2 (8999) → download → clear
             → export3 (8999) → download → clear
             → export1 (8999) → download → clear
             → ... until INBOX is empty
```

## Working Script

See `purge_cycle.py` for the implementation. Key parameters:

```python
EXPORT_FOLDERS = ["export1", "export2", "export3"]
MOVE_BATCH = 8999  # Yahoo errors at 10000
```

## Cron Schedule

Set up a cron job to run one cycle every 15 minutes:

```bash
openclaw cron create \
  --name "email-purge-cycle" \
  --every 15m \
  --message "Run: cd ~/email-purge && python3 scripts/purge_cycle.py" \
  --session isolated \
  --model "moonshot/kimi-k2.5" \
  --no-deliver
```

## Performance

- **MOVE**: ~1000 messages per 25 seconds (1000 per MOVE call)
- **DOWNLOAD**: ~1 message per second (FETCH RFC822 on regular server)
- **Total cycle time**: ~3-4 hours per 8999 messages (mostly download time)
- **Estimated total**: 132K / 8999 = ~15 cycles × 4 hours = ~60 hours

## Configuration

### IMAP Settings

```
Regular:  imap.mail.yahoo.com:993 (10K cap)
Export:   export.imap.mail.yahoo.com:993 (100K cap)
Auth:     Plain password (app password for Yahoo Account Key)
```

### Folder Structure

```
~/email-purge/
├── eml/           # Downloaded .eml files
│   ├── INBOX/
│   ├── export1/
│   ├── export2/
│   ├── export3/
│   ├── Sent/
│   ├── Draft/
│   ├── Bulk/
│   ├── Personal/
│   └── Archive/
├── metadata/      # JSONL metadata files
├── logs/          # Download and cycle logs
└── scripts/       # All Python scripts
```

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `BAD [CLIENTBUG] FETCH Bad sequence` | Sequence number > visible limit | Use export server or smaller folders |
| `[SERVERBUG] MOVE Server error` | Too many messages in one MOVE session | Reduce batch size to 8999 |
| `socket error: [Errno 32] Broken pipe` | IMAP connection timeout | Reconnect and resume |
| `ssl.SSLError: [SSL: BAD_LENGTH]` | Yahoo SSL quirk | Use export server or reconnect |

### Reconnection Strategy

```python
try:
    m.logout()
except:
    pass
time.sleep(2)
m = imaplib.IMAP4_SSL(HOST, 993)
m.login(EMAIL, PASS)
```

## Lessons Learned

1. **Always check STATUS before SELECT** — STATUS gives real count, SELECT may be capped
2. **Test with small batches first** — COPY claimed OK but lost messages; MOVE actually works
3. **Sequence numbers shift after MOVE** — always use `seq 1:N`, not fixed ranges
4. **Export server ≠ fast server** — it has higher caps but slower FETCH
5. **Yahoo rate limits are soft** — `SERVERBUG` at ~9K, not a hard crash
6. **Document everything** — these quirks are not documented by Yahoo
7. **The web interface uses a different API** — IMAP is always a subset of what the web shows

## Future Improvements

- [ ] Parallel downloads across export folders
- [ ] Resume capability (track downloaded sequences)
- [ ] Metadata extraction during download (not after)
- [ ] Integration with email analysis/triage pipeline
- [ ] Support for other providers (Gmail, Outlook) with similar limits

Now, what to do with those messages?  That's another story involving a GPU, a local small model running under ollama, and a local vector database 
running under the same gpu to sort through all those emails and find anything important.

---

*Last updated: 2026-05-03*

