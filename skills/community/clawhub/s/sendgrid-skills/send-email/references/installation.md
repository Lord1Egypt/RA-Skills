# Installation (SendGrid SDK)

**Live-send safety:** these examples send real email through SendGrid and may incur charges. Obtain approval for the sender, all To/CC/BCC recipients, exact subject/body, template data and attachments before running them. Recipient data, content and attachments go to SendGrid and recipients. Minimize personal data; never include secrets, regulated data or sensitive files without authorization. Read only approved attachment/HTML files. Use a Mail Send-only API key from the environment and never print it. Use recipients you control for approved tests; example addresses are placeholders, not delivery approval.

## Optional repository helpers

The repository send helpers require Bash 3.2+, curl and jq 1.6+ (`--rawfile`); HTML file input also requires `realpath`. Check `jq --version` before using them. jq reads each field through a descriptor to preserve UTF-8 without putting message content in child-process arguments. These helpers are optional in a standalone subskill installation. The self-contained cURL examples below require Bash and curl, but do not use jq or sibling scripts.

## Node.js / TypeScript

```bash
pnpm add @sendgrid/mail
```

```ts
import sgMail from '@sendgrid/mail';
sgMail.setApiKey(process.env.SENDGRID_API_KEY!);
```

## Python

```bash
pip install sendgrid
```

```py
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
```

## Go

```bash
go get github.com/sendgrid/sendgrid-go
```

```go
import (
  "os"
  "github.com/sendgrid/sendgrid-go"
  "github.com/sendgrid/sendgrid-go/helpers/mail"
)

sg := sendgrid.NewSendClient(os.Getenv("SENDGRID_API_KEY"))
```

## PHP

```bash
composer require sendgrid/sendgrid
```

## Ruby

```bash
gem install sendgrid-ruby
```

## Java

```xml
<dependency>
  <groupId>com.sendgrid</groupId>
  <artifactId>sendgrid-java</artifactId>
  <version>4.10.3</version>
</dependency>
```

## C# (.NET)

```bash
dotnet add package SendGrid
```

## cURL

These self-contained Bash examples stream JSON on stdin and the validated key through a curl config descriptor. They disable default curl config, bypass environment proxies, use HTTPS with TLS verification, do not follow redirects, and do not retry. Keep shell history, environment access and output private; these are not a local-process privacy sandbox.

**Live POST:** sends message data to SendGrid and attempts delivery. Approve recipients and content first.

```bash
# Bash subshell: errors stop this example without exiting an interactive shell.
(
  if [[ ! "$SENDGRID_API_KEY" =~ ^[A-Za-z0-9._-]+$ ]]; then
    echo "Error: SENDGRID_API_KEY is missing or contains unsupported characters" >&2
    exit 1
  fi
  response=$(curl --disable -sS --connect-timeout 10 --max-time 60 \
    --proto =https --noproxy '*' -w '\n%{http_code}' \
    -X POST https://api.sendgrid.com/v3/mail/send \
    --config <(printf 'header = "Authorization: Bearer %s"\n' "$SENDGRID_API_KEY") \
    -H 'Content-Type: application/json' --data-binary @- <<'JSON'
{"personalizations":[{"to":[{"email":"test@example.com"}]}],"from":{"email":"support@example.com"},"subject":"Hello","content":[{"type":"text/plain","value":"Hi"}]}
JSON
  ) || {
    status=$?
    echo "Error: request to SendGrid failed (curl exit $status); delivery status is unknown. Do not retry automatically." >&2
    exit "$status"
  }
  code=${response##*$'\n'}
  if [[ "$code" != 202 ]]; then
    printf 'Error: SendGrid returned HTTP %s\n' "$code" >&2
    exit 1
  fi
  echo 'Email queued for delivery (HTTP 202)'
)
```

## Templates (Dynamic)

Dynamic templates are referenced by `template_id` and optional `dynamic_template_data`.
See: <https://docs.sendgrid.com/ui/sending-email/how-to-send-an-email-with-dynamic-templates>
