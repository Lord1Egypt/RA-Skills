# Secret Patterns Reference

Extended reference of secret patterns detected by the scanner, organized by provider/type.

## Pattern Categories

### Cloud Providers
| Provider | Pattern | Example |
|----------|---------|---------|
| AWS Access Key | `AKIA[0-9A-Z]{16}` | AKIAIOSFODNN7EXAMPLE |
| AWS Secret Key | 40-char base64 after `aws_secret_access_key=` | wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY |
| GCP API Key | `AIza[0-9A-Za-z_-]{35}` | AIzaSyA1234567890abcdefghijklmnopqrstuv |
| GCP Service Account | JSON with `"type": "service_account"` | — |
| Azure Storage Key | 88-char base64 after `AccountKey=` | — |

### Payment Processors
| Provider | Pattern | Example |
|----------|---------|---------|
| Stripe Secret | `sk_live_[0-9a-zA-Z]{24,}` | sk_live_4eC39HqLyjWDarjtT1zdp7dc |
| Stripe Publishable | `pk_live_[0-9a-zA-Z]{24,}` | pk_live_... |

### Communication
| Provider | Pattern | Example |
|----------|---------|---------|
| Slack Webhook | `https://hooks.slack.com/services/T.../B.../...` | — |
| Discord Webhook | `https://discord.com/api/webhooks/...` | — |
| Telegram Bot | `\d{8,10}:[A-Za-z0-9_-]{35}` | 123456789:ABCdefGHIjklMNOpqrsTUVwxyz12345 |
| SendGrid | `SG\.[...]{22}\.[...]{43}` | — |
| Twilio | `SK[0-9a-fA-F]{32}` | — |
| Mailgun | `key-[0-9a-zA-Z]{32}` | — |

### AI/ML
| Provider | Pattern | Example |
|----------|---------|---------|
| OpenAI (legacy) | `sk-[...]{20,}T3BlbkFJ[...]{20,}` | — |
| OpenAI (project) | `sk-proj-[...]{40,}` | — |

### Version Control
| Provider | Pattern | Example |
|----------|---------|---------|
| GitHub PAT | `gh[pousr]_[A-Za-z0-9_]{36,}` | ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx |
| GitHub OAuth | `gho_[A-Za-z0-9]{36}` | — |

## Remediation Guide

### For Each Severity Level

**HIGH — Immediate action required:**
1. Rotate the credential immediately
2. Check access logs for unauthorized use
3. Move to environment variable or secrets manager
4. Add file pattern to `.gitignore`
5. If committed to git: use `git filter-branch` or BFG Repo-Cleaner

**MEDIUM — Review and fix:**
1. Verify if the credential is real or placeholder
2. Move to environment variable if real
3. Consider using a secrets manager (Vault, AWS Secrets Manager, etc.)

**LOW — Track and plan:**
1. Replace placeholder credentials with proper env var references
2. Update documentation to use example placeholders (e.g., `YOUR_API_KEY_HERE`)
3. Add pre-commit hooks to prevent future leaks

### Environment Variable Best Practices
- Use `.env` files for local development (add to `.gitignore`)
- Use secrets manager for production
- Never set defaults for secret env vars in code
- Use `required: true` validation for secret config values
