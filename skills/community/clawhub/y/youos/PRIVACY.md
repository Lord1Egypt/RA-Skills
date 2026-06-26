# YouOS Privacy Policy

YouOS is a local-first personal AI email copilot. Your privacy is the foundation of its design.

## What data is collected

- **Sent email text**: The body text of your sent Gmail messages, used to learn your writing style
- **Email metadata**: Sender addresses, subject lines, timestamps — used for retrieval and context
- **Your edits**: When you review and edit a draft in the YouOS web UI, both the generated draft and your edited version are saved as a feedback pair for fine-tuning

## Where data is stored

All data is stored **locally on your machine** in a SQLite database:

```
~/Projects/youos/var/youos.db
```

No data is synced to any cloud service, remote database, or third-party storage.

## What leaves your machine

- **LLM API calls** (optional): When generating draft replies before the local model is trained, YouOS sends the inbound email text and retrieved context to an LLM API (Claude by default) to produce a draft. This is the only data that leaves your machine.
- **After local model training**: Once you have enough feedback pairs and the local Qwen model is fine-tuned, all generation happens on-device. No data leaves your machine at all.
- **You control the fallback**: Set `model.fallback: none` in `youos_config.yaml` to disable all external API calls. YouOS will only use the local model.

## What does NOT happen

- No telemetry or analytics of any kind
- No usage tracking or crash reporting
- No cloud sync or backup
- No data shared with Anthropic, OpenAI, or any other provider (beyond the optional LLM API calls described above)
- No advertising or profiling
- No email content is ever stored outside your local filesystem

## How to delete everything

**Option 1: Delete the database**
```bash
rm ~/Projects/youos/var/youos.db
```

**Option 2: Delete all YouOS data**
```bash
rm -rf ~/Projects/youos/var/
rm -rf ~/Projects/youos/data/
rm -rf ~/Projects/youos/models/adapters/latest/
rm ~/Projects/youos/configs/persona_analysis.json
```

**Option 3: Remove YouOS entirely**
```bash
rm -rf ~/Projects/youos
```

## Data retention

YouOS does not automatically delete any data. Your corpus grows over time as new emails are ingested. You can manually purge old data by deleting and re-creating the database, or by running SQL queries against the local SQLite file.

## Contact

YouOS is open source. If you have privacy questions or concerns, open an issue at https://github.com/DrBaher/youos.
