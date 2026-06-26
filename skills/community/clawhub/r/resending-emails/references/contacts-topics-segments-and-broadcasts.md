# Contacts, topics, segments, and broadcasts

This file covers Resend's CLI surface for subscription modelling and campaign delivery.

## Model the data correctly

### Contact properties

Use contact properties for profile data and segmentation inputs.

Examples:

- plan
- company
- country
- signup source

### Topics

Topics are recipient-facing preference categories.

Examples:

- Product Updates
- Security Alerts
- Weekly Digest

A topic's `default_subscription` matters. Choose it intentionally.

### Segments

Segments are sender-controlled targeting groups.

Examples:

- beta users
- German customers
- enterprise plan
- trial users from the last 14 days

### Global unsubscribe vs topic subscriptions

These are different layers:

- global unsubscribed = no broadcasts at all
- topic subscription = whether a contact wants a specific category

Do not collapse them into the same boolean.

## `topics create`

Good example:

```bash
resend --json -q topics create \
  --name "Product Updates" \
  --description "Feature launches and important product news" \
  --default-subscription opt_in
```

## `segments create`

Good example:

```bash
resend --json -q segments create --name "Beta Users"
```

## `contacts create`

Good example:

```bash
resend --json -q contacts create \
  --email jane@example.com \
  --first-name Jane \
  --last-name Smith \
  --properties '{"plan":"pro","company":"Acme"}' \
  --segment-id <segment-id>
```

Notes:

- `first-name` and `last-name` map to standard properties
- `--properties` expects a JSON string
- `--unsubscribed` is a team-wide opt-out from broadcasts

## Broadcasts

Use broadcasts for campaign-style sends to a segment.

### `broadcasts create`

This creates a draft, or sends immediately with `--send`.

Key options:

- `--from`
- `--subject`
- `--segment-id`
- one of `--html`, `--html-file`, `--text`
- optional `--topic-id`
- optional `--send`
- optional `--scheduled-at`

Sample draft:

```bash
resend --json -q broadcasts create \
  --from hello@example.com \
  --subject "Weekly Update" \
  --segment-id <segment-id> \
  --html-file ./broadcast.html \
  --topic-id <topic-id>
```

### Scheduling broadcasts

Broadcast scheduling explicitly accepts both:

- ISO 8601
- natural language (for example `tomorrow at 9am ET`, `in 1 hour`)

That makes broadcasts a good CLI-native place to use human-friendly schedule strings.

### `broadcasts send`

Use this to send or schedule a draft broadcast later.

Important caveat:

- only broadcasts created via the API/CLI can be sent this way; dashboard-created broadcasts are not
  currently sendable programmatically through this command

## Audiences

For new designs, prefer **segments + topics + contacts** over deprecated audiences.
