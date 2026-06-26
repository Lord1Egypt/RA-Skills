# SnapPwd CLI Usage

## Installation

```bash
npm install -g @snappwd/cli
```

## Commands

### Share a Secret

```bash
snappwd put "your-secret-here"
```

Output:
```
https://snappwd.io/g/abc123def456...#encryption-key...
```

### Share a File

```bash
snappwd put-file ./path/to/file
```

Examples:
```bash
# Share an .env file
snappwd put-file ./.env

# Share an SSH key
snappwd put-file ~/.ssh/id_rsa

# Share a config file
snappwd put-file ./config/credentials.json
```

### Retrieve a Secret

```bash
snappwd get "https://snappwd.io/g/abc123...#key..."
```

### Peek at Secret Metadata

View metadata without destroying the secret:

```bash
snappwd peek "https://snappwd.io/g/abc123...#key..."
```

## Options

| Flag | Description |
|------|-------------|
| `--api-url <url>` | Use a custom SnapPwd service instance |
| `--ttl <seconds>` | Set time-to-live for the secret |
| `--help` | Show help |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `SNAPPWD_API_URL` | Default API URL for self-hosted instances |

## Self-Hosting

Point the CLI to your own SnapPwd service:

```bash
export SNAPPWD_API_URL="https://secrets.your-domain.com/api/v1"
snappwd put "Internal secret"
```

## Output Formats

The CLI outputs the full secure link including the encryption key in the URL fragment:

```
https://snappwd.io/g/<uuid>#<base58-encoded-key>
```

- The UUID identifies the encrypted secret on the server
- The key (after `#`) is the AES-256 encryption key, never sent to the server