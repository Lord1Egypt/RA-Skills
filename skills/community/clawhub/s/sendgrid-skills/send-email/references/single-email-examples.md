# Single Email Examples (SendGrid)

**Live-send safety:** these examples send real email through SendGrid and may incur charges. Obtain approval for the sender, all To/CC/BCC recipients, exact subject/body, template data and attachments before running them. Recipient data, content and attachments go to SendGrid and recipients. Minimize personal data; never include secrets, regulated data or sensitive files without authorization. Read only approved attachment/HTML files. Use a Mail Send-only API key from the environment and never print it. Use recipients you control for approved tests; example addresses are placeholders, not delivery approval.

## Node.js / TypeScript

```ts
import sgMail from '@sendgrid/mail';

sgMail.setApiKey(process.env.SENDGRID_API_KEY!);

await sgMail.send({
  from: 'Support <support@example.com>',
  to: ['test@example.com'],
  cc: ['cc@example.com'],
  bcc: ['bcc@example.com'],
  replyTo: 'support@example.com',
  subject: 'SendGrid test',
  text: 'Plain text body',
  html: '<p>HTML body</p>',
  attachments: [
    {
      filename: 'hello.txt',
      content: Buffer.from('hello').toString('base64'),
      type: 'text/plain',
      disposition: 'attachment',
    }
  ]
});
```

### Dynamic Template (Node)

```ts
await sgMail.send({
  from: 'Support <support@example.com>',
  to: ['test@example.com'],
  templateId: 'd-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
  dynamicTemplateData: { first_name: 'Vince' }
});
```

## Python

```py
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Cc, Bcc, ReplyTo, Attachment, FileContent, FileName, FileType, Disposition

message = Mail(
    from_email=Email('support@example.com'),
    to_emails=To('test@example.com'),
    subject='SendGrid test',
    plain_text_content='Plain text body',
    html_content='<p>HTML body</p>'
)
message.add_cc(Cc('cc@example.com'))
message.add_bcc(Bcc('bcc@example.com'))
message.reply_to = ReplyTo('support@example.com')

attachment = Attachment(
    FileContent('aGVsbG8='),
    FileName('hello.txt'),
    FileType('text/plain'),
    Disposition('attachment')
)
message.add_attachment(attachment)

sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
response = sg.send(message)
```

### Dynamic Template (Python)

```py
message = Mail(
    from_email='support@example.com',
    to_emails='test@example.com'
)
message.template_id = 'd-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
message.dynamic_template_data = {'first_name': 'Vince'}

sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
sg.send(message)
```

## cURL

These self-contained Bash examples stream JSON on stdin and the validated key through a curl config descriptor. They disable default curl config, bypass environment proxies, use HTTPS with TLS verification, do not follow redirects, and do not retry. Keep shell history, environment access and output private; these are not a local-process privacy sandbox.

**Live POST:** the following commands send to every listed To/CC/BCC recipient. Review the exact content and attachment before approving.

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
{"personalizations":[{"to":[{"email":"test@example.com"}],"cc":[{"email":"cc@example.com"}],"bcc":[{"email":"bcc@example.com"}]}],"from":{"email":"support@example.com"},"reply_to":{"email":"support@example.com"},"subject":"SendGrid test","content":[{"type":"text/plain","value":"Plain text body"},{"type":"text/html","value":"<p>HTML body</p>"}],"attachments":[{"content":"aGVsbG8=","type":"text/plain","filename":"hello.txt","disposition":"attachment"}]}
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

### Dynamic Template (cURL)

**Live POST:** approve the selected template, recipient and template data first.

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
{"from":{"email":"support@example.com"},"personalizations":[{"to":[{"email":"test@example.com"}],"dynamic_template_data":{"first_name":"Vince"}}],"template_id":"d-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"}
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
