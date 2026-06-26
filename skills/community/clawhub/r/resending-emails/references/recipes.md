# Recipes

These are concise end-to-end CLI-native playbooks.

## 1. Transactional send with retry safety

1. prepare HTML file if needed
2. run `emails send`
3. include `--idempotency-key`
4. verify with `emails get`

```bash
resend --json -q emails send \
  --from "Acme <alerts@example.com>" \
  --to alice@example.com \
  --subject "Welcome" \
  --html-file ./newsletter.html \
  --idempotency-key welcome-001
```

## 2. Scheduled password reset

1. choose `emails send`
2. use explicit ISO timestamp
3. keep returned email ID
4. use `emails update` or `emails cancel` if needed

## 3. Batch shipment notifications

1. build `batch-emails.json`
2. lint the file
3. run `emails batch`
4. chunk if more than 100 items

```bash
python3 scripts/resend_cli.py lint-batch ./batch-emails.json
resend --json -q emails batch --file ./batch-emails.json --idempotency-key shipments-001
```

## 4. Sending + receiving domain

1. `domains create --receiving`
2. add DNS records in the DNS provider
3. `domains verify`
4. poll with `domains get`
5. only then send or receive

## 5. Local webhook loop

1. open a tunnel to the local port
2. run `webhooks listen --url ... --forward-to ...`
3. collect events for a bounded time
4. stop the process cleanly

## 6. Inbound mailbox processor

1. create receiving-capable domain/subdomain
2. create webhook including `email.received`
3. on each event, call `emails receiving get`
4. fetch attachments when needed
5. reply using `emails send` with threading headers

## 7. Subscription model for newsletters

1. `topics create`
2. `segments create`
3. `contacts create` with properties and segment IDs
4. `broadcasts create` with `--topic-id`
5. `broadcasts send` or `broadcasts create --send`

## 8. Domain-scoped CI token

```bash
resend --json -q api-keys create \
  --name "ci-token" \
  --permission sending_access \
  --domain-id <domain-id>
```

## 9. Hosted template lifecycle

1. `templates create`
2. `templates publish`
3. if the user needs hosted-template sends, check the current local CLI help
4. if direct send-by-template is still missing, fall back deliberately

## 10. Multi-account operations

Use explicit profiles:

```bash
resend --profile staging --json -q doctor
resend --profile production --json -q domains list
```
