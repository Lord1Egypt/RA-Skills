# VetKey Encryption and Access Control

## Overview

VetKey supports:

- Local encryption and decryption of raw bytes
- Kind5 encrypted posts
- Deterministic backup and restore flows
- Access grants that let other identities decrypt authorized Kind5 posts

Use plain-language summaries when speaking to the user. Daemon internals are implementation details and should stay invisible in normal conversation.

## IBE commands

### Encrypt and sign as Kind5

```bash
zcloak-ai vetkey encrypt-sign --text "Secret message" --json
zcloak-ai vetkey encrypt-sign --file ./secret.pdf --tags '[["p","<ai_id>"],["t","topic"]]' --json
```

Typical output:

```json
{"event_id":"...","ibe_identity":"...","kind":5,"content_hash":"..."}
```

After a Kind5 post is published:

1. Remind the user that the post is encrypted
2. Explain that only the author can decrypt it by default
3. Ask whether the user wants to grant decryption access to anyone else

### Decrypt a Kind5 post

```bash
zcloak-ai vetkey decrypt --event-id "EVENT_ID" --json
zcloak-ai vetkey decrypt --event-id "EVENT_ID" --output ./decrypted.pdf
```

### Encrypt only

```bash
zcloak-ai vetkey encrypt-only --text "Hello" --json
zcloak-ai vetkey encrypt-only --file ./secret.pdf --public-key "HEX..." --ibe-identity "ai_id:hash:ts" --json
```

### Get IBE public key

```bash
zcloak-ai vetkey pubkey --json
```

## Backup workflow

When encrypting a folder for backup, always compress the folder first and then encrypt the single archive file. Do not encrypt folder contents one by one.

Example flow:

```bash
tar -czf my-skill.tar.gz my-skill/
```

```json
{"id":1,"method":"encrypt","params":{"input_file":"my-skill.tar.gz","output_file":"backup/my-skill.tar.gz.enc"}}
```

Restore flow:

```json
{"id":1,"method":"decrypt","params":{"input_file":"backup/my-skill.tar.gz.enc","output_file":"restored/my-skill.tar.gz"}}
```

```bash
tar -xzf restored/my-skill.tar.gz -C restored/
```

The same identity PEM plus the same key name yields the same AES key, so backups remain recoverable.

## Kind5 access control

Grant or revoke decryption access for Kind5 posts.

### Grant access

```bash
zcloak-ai vetkey grant --grantee <grantee_ai_id> --json
zcloak-ai vetkey grant --grantee <grantee_ai_id> --event-ids=EVENT_ID1,EVENT_ID2 --json
zcloak-ai vetkey grant --grantee <grantee_ai_id> --duration=30d --json
zcloak-ai vetkey grant --grantee <grantee_ai_id> --event-ids=EVENT_ID1 --duration=1y --json
```

Duration formats:

- `30d`
- `24h`
- `6m`
- `1y`
- `permanent`

After a successful grant:

1. Show the user the complete event ID or IDs
2. Tell the user to send those event IDs to the authorized person
3. Explain that the grantee can give the event ID to their own agent and decrypt normally

### Revoke access

```bash
zcloak-ai vetkey revoke --grant-id 42 --json
```

### List grants

```bash
zcloak-ai vetkey grants-out --json
zcloak-ai vetkey grants-in --json
```

### Grantee decryption note

Once authorized, the grantee decrypts using the standard decrypt command and the shared event ID. No special flag is required.
