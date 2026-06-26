# Provider Profiles - SMTP

Use this file as the baseline for `~/smtp/provider-profiles.md`.

Keep only providers the user actually uses and add notes only after a real test confirms them.

| Provider | Host | Port | TLS mode | Auth note | Sender identity note |
|----------|------|------|----------|-----------|----------------------|
| Google Workspace or Gmail | `smtp.gmail.com` | `587` | STARTTLS | App password or approved relay path only | From should match the authorized account or delegated alias |
| Microsoft 365 | `smtp.office365.com` | `587` | STARTTLS | Modern auth policies may block legacy username-password flow | Shared mailboxes and aliases need explicit send rights |
| Amazon SES SMTP | `email-smtp.<region>.amazonaws.com` | `587` or `465` | STARTTLS or implicit TLS | Use SES SMTP credentials, not AWS root credentials | MAIL FROM domain and DKIM alignment matter for placement |
| Mailgun | `smtp.mailgun.org` | `587` or `465` | STARTTLS or implicit TLS | Use the SMTP credential issued for the domain | From should stay inside the sending domain unless routed intentionally |
| Postmark | `smtp.postmarkapp.com` | `587` or `2525` | STARTTLS | Server token or SMTP token only | Sender signature must already be approved |
| Fastmail | `smtp.fastmail.com` | `465` or `587` | implicit TLS or STARTTLS | App password recommended | Alias support depends on configured identities |

Profile notes to keep:
- which host and port actually worked
- whether STARTTLS was advertised
- auth mechanism used successfully
- whether the visible From matched auth identity cleanly
- any provider-specific rejection or rate-limit pattern
