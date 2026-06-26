# save-to-email

A small open-source skill for sending HTML emails through the Resend API.

## What it does

- provides a reusable Codex/Claude skill
- sends email with a simple shell command
- keeps secrets out of the repository

## Repository layout

```text
save-to-email/
├── SKILL.md
├── README.md
├── .env.example
└── scripts/
    └── send-email.sh
```

## Configuration

1. Create a local `.env` file in the repository root.
2. Add these values:

```bash
RESEND_API_KEY=your_resend_api_key
RESEND_FROM="Your Name <sender@yourdomain.com>"
```

## Usage

```bash
./scripts/send-email.sh "recipient@example.com" "Subject" "<p>Hello</p>"
```

## Parameters

- `recipient`: target email address
- `subject`: email subject
- `html`: HTML body content

## Notes

- The script auto-loads `.env` when present.
- `RESEND_FROM` must be a sender verified in your Resend account.
- This repository intentionally excludes API keys and private sender identities.
