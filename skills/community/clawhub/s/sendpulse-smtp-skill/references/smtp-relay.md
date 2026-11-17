# SMTP relay — classic SMTP protocol connection

Use the relay when the sending side already speaks SMTP and can't easily call a
REST API: PHPMailer, nodemailer, Python `smtplib`, WordPress/CMS mail plugins,
CRMs, desktop mail clients, legacy apps. Same prerequisites as the API: activated
account + verified sender ([setup.md](setup.md)).

## Connection settings

| Setting | Value |
|---|---|
| Host | `smtp-pulse.com` |
| Port | **465** (SSL, recommended) · alternatives: **2525**, **587** (use when 465 is blocked) |
| Encryption | SSL for 465 |
| Auth | required (LOGIN) |
| Login | your SendPulse account email |
| Password | the SMTP password from the dashboard |

Copy the exact live values from **SMTP → Settings → General** in the dashboard —
that page is authoritative for your account (host/port/login/password).

Rules that still apply over relay:

- `From` must be a **verified sender** on your corporate domain, otherwise the
  message is rejected.
- Recipients on the unsubscribe blocklist are silently dropped.
- Hourly/monthly volume limits of your plan apply.
- Port 25 is commonly blocked by hosting providers — prefer 465.

## PHPMailer (PHP)

```php
use PHPMailer\PHPMailer\PHPMailer;

$mail = new PHPMailer(true);
$mail->isSMTP();
$mail->Host       = 'smtp-pulse.com';
$mail->Port       = 465;
$mail->SMTPSecure = 'ssl';
$mail->SMTPAuth   = true;
$mail->Username   = getenv('SENDPULSE_SMTP_LOGIN');
$mail->Password   = getenv('SENDPULSE_SMTP_PASSWORD');

$mail->setFrom('noreply@myshop.com', 'My Shop');   // verified sender!
$mail->addAddress('jane@example.com', 'Jane');
$mail->Subject = 'Order confirmed';
$mail->isHTML(true);
$mail->Body    = '<h1>Thanks!</h1><p>Your order #1234 is confirmed.</p>';
$mail->AltBody = 'Thanks! Your order #1234 is confirmed.';
$mail->send();
```

## Nodemailer (Node.js)

```js
const nodemailer = require('nodemailer');

const transporter = nodemailer.createTransport({
  host: 'smtp-pulse.com',
  port: 465,
  secure: true, // SSL
  auth: {
    user: process.env.SENDPULSE_SMTP_LOGIN,
    pass: process.env.SENDPULSE_SMTP_PASSWORD,
  },
});

await transporter.sendMail({
  from: '"My Shop" <noreply@myshop.com>', // verified sender!
  to: 'jane@example.com',
  subject: 'Order confirmed',
  html: '<h1>Thanks!</h1><p>Your order #1234 is confirmed.</p>',
  text: 'Thanks! Your order #1234 is confirmed.',
});
```

## smtplib (Python)

```python
import os, smtplib
from email.message import EmailMessage

msg = EmailMessage()
msg["Subject"] = "Order confirmed"
msg["From"] = "My Shop <noreply@myshop.com>"  # verified sender!
msg["To"] = "jane@example.com"
msg.set_content("Thanks! Your order #1234 is confirmed.")
msg.add_alternative("<h1>Thanks!</h1><p>Your order #1234 is confirmed.</p>",
                    subtype="html")

with smtplib.SMTP_SSL("smtp-pulse.com", 465) as smtp:
    smtp.login(os.environ["SENDPULSE_SMTP_LOGIN"],
               os.environ["SENDPULSE_SMTP_PASSWORD"])
    smtp.send_message(msg)
```

## WordPress / CMS plugins

Any "SMTP mailer" plugin (e.g. WP Mail SMTP, Post SMTP) works: choose "Other
SMTP", enter host `smtp-pulse.com`, port `465`, encryption SSL, authentication
on, the login/password from the dashboard, and a verified From address.

## Relay vs REST API — help the user choose

| | SMTP relay | REST API |
|---|---|---|
| Integration effort | Zero if the app already sends SMTP | Small HTTP client |
| Message id / status lookup | No (track via webhooks/statistics only) | Yes — `id` returned, `GET /smtp/emails/{id}` |
| Templates with variables | No (render yourself) | Yes (`template.id` + `variables`) |
| Blocklist management | Dashboard only | Full API (`/smtp/unsubscribe*`) |
| Best for | Plugins, legacy apps, mail clients | New code, anything needing tracking |

Recommendation: relay to get running today; REST API for anything you build from
scratch. Troubleshooting relay errors (535 auth, timeouts, 550): see
[errors.md](errors.md), section 5.
