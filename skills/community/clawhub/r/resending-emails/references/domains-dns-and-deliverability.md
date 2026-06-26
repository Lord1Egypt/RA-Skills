# Domains, DNS, and deliverability

This file covers the domain setup issues that most often break Resend operations.

## Domain creation

Use `domains create` to bootstrap a sending or receiving domain and obtain the DNS records to add in
your DNS provider.

Sample:

```bash
resend --json -q domains create --name eu.example.com --region eu-west-1 --receiving
```

### Important creation options

- `--name`
- `--region` (`us-east-1`, `eu-west-1`, `sa-east-1`, `ap-northeast-1`)
- `--tls` (`opportunistic` or `enforced`)
- `--sending`
- `--receiving`

## Verification flow

A correct domain flow is:

1. create the domain
2. read the returned DNS records
3. add those records in the DNS provider
4. run `domains verify`
5. poll with `domains get` / `domains list`
6. only then send from that domain

The CLI cannot finish DNS work by itself.

## `from` address rule

The `from` address must match the **exact verified domain**.

Examples:

- verified `mail.example.com` → send from `alerts@mail.example.com`
- verified `example.com` → send from `alerts@example.com`

Do **not** assume a verified subdomain automatically authorises the parent domain, or vice versa.

## `resend.dev`

`resend.dev` is testing-only. It is not the answer for real customer delivery.

If the user wants real sending, point them toward verifying a domain they control.

## Receiving and MX planning

If the user already uses another provider’s MX records on the root domain, recommend a dedicated
subdomain for Resend receiving, such as:

- `support.mail.example.com`
- `inbound.example.com`

That avoids root-domain MX conflicts.

## `domains update`

Current CLI `domains update` exposes:

- `--tls`
- `--open-tracking` / `--no-open-tracking`
- `--click-tracking` / `--no-click-tracking`

### Important ambiguity

The receiving command help text references enabling receiving via `domains update`, but the current
`domains update` implementation does **not** expose a receiving/sending capability flag. Treat this
as a real CLI ambiguity.

Practical guidance:

- if you know you need receiving, prefer setting `--receiving` at `domains create` time
- if the user wants to enable receiving on an already-created domain, inspect local help and be
  ready to fall back to API/MCP if the toggle is not exposed

## Domain verification polling

Use:

```bash
resend --json -q domains verify <domain-id>
resend --json -q domains get <domain-id>
```

Verification is async. Do not assume the domain becomes verified immediately after `verify`.

## API keys

For automation, use the narrowest scope that fits.

Good example:

```bash
resend --json -q api-keys create \
  --name "ci-pipeline" \
  --permission sending_access \
  --domain-id <domain-id>
```

Store the returned token immediately; it is shown once.
