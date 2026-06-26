# Security Notes

## Credential handling

Use runtime environment variables or host secret management.

Supported optional variables:
- `EBAY_APP_ID`
- `EBAY_CERT_ID`
- `EBAY_DEV_ID`
- `EBAY_USER_TOKEN`
- `PSA_API_KEY`

Do not:
- hardcode secrets in scripts
- store secrets in the skill package
- instruct users to place secrets in home-directory dotfiles for this skill

## Data handling

- Prefer local processing and minimal retention.
- Request only the credentials needed for the task at hand.
- Do not claim external verification unless a live integration was actually used.

## Marketplace safety

- Prefer official APIs over scraping.
- Respect rate limits and terms of service.
- Avoid automated marketplace actions unless they are explicitly implemented, documented, and approved.
