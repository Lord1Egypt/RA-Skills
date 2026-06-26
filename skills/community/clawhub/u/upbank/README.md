# Up Bank API

Read-only access to Up Bank account data via the official API.

## Features

- **Accounts** — View all accounts and balances
- **Transactions** — Browse and search transaction history
- **Categories** — Explore spending categories
- **Tags** — View all tags
- **Attachments** — Access transaction attachments
- **Webhooks** — Review webhook configurations and logs

## Requirements

- Up Bank account
- Personal Access Token from the Up app

## Installation

```bash
openclaw skills install upbank
```

Or manually copy this folder to your workspace skills directory.

## Configuration

Set the `UP_API_TOKEN` environment variable with your Personal Access Token:

```bash
export UP_API_TOKEN="your-token-here"
```

## Security

- **Read-only** — No write operations permitted
- **JIT Access** — Requires explicit approval per request
- **Time-based** — Tokens expire; re-authenticate after 1 hour

## Rate Limits

Respect Up Bank's rate limits. If you hit 429, wait before retrying.

## License

MIT