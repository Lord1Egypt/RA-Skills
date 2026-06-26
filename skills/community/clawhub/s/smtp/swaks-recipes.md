# swaks Recipes - SMTP

Documentation-only examples. Use placeholder hosts, domains, and addresses. Do not paste real secrets into files.

## EHLO and capability probe

```bash
swaks --server smtp.example.com --port 587 --quit-after EHLO
```

Use this first to see whether STARTTLS and auth are even offered.

## STARTTLS probe on port 587

```bash
swaks \
  --server smtp.example.com \
  --port 587 \
  --tls \
  --from sender@example.com \
  --to canary@example.net \
  --quit-after RCPT
```

Use this to prove TLS and envelope acceptance before a full body send.

## Implicit TLS probe on port 465

```bash
swaks \
  --server smtp.example.com \
  --port 465 \
  --tls-on-connect \
  --from sender@example.com \
  --to canary@example.net \
  --quit-after RCPT
```

Use this when the provider expects TLS immediately on connect.

## Minimal canary send

```bash
swaks \
  --server smtp.example.com \
  --port 587 \
  --tls \
  --from sender@example.com \
  --to canary@example.net \
  --header "Subject: SMTP canary" \
  --body "Plain-text canary for SMTP validation."
```

Use the smallest useful message first. Save the queue ID or message ID.

## TLS certificate inspection

```bash
openssl s_client -starttls smtp -connect smtp.example.com:587 -crlf -quiet
```

Use this when TLS mode, hostname, or certificate validation looks wrong.
