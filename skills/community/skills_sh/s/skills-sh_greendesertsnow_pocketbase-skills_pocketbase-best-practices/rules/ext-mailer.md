---
title: Send Email via app.NewMailClient, Never the Default example.com Sender
impact: HIGH
impactDescription: Default sender is no-reply@example.com; shipping it bounces every email and damages your SMTP reputation
tags: mailer, email, smtp, $mails, extending, templates
---

## Send Email via app.NewMailClient, Never the Default example.com Sender

PocketBase ships with a mailer accessible through `app.NewMailClient()` (Go) or `$app.newMailClient()` (JS). It reads the SMTP settings configured in **Admin UI → Settings → Mail settings**, or falls back to a local `sendmail`-like client if SMTP is not configured. Two things bite people: (1) the default `Meta.senderAddress` is `no-reply@example.com` - shipping with that bounces every email and poisons your sender reputation; (2) there is no connection pooling, so long-lived mail client handles are **not** safe to share across requests - create one per send.

**Incorrect (default sender, shared client, no error handling):**

```go
// ❌ Default sender is example.com, and this mailer instance is captured
//    for the process lifetime - SMTP connections go stale
var mailer = app.NewMailClient()

app.OnRecordAfterCreateSuccess("orders").BindFunc(func(e *core.RecordEvent) error {
    msg := &mailer.Message{
        From:    mail.Address{Address: "no-reply@example.com"}, // ❌
        To:      []mail.Address{{Address: e.Record.GetString("email")}},
        Subject: "Order confirmed",
        HTML:    "<p>Thanks</p>",
    }
    mailer.Send(msg) // ❌ error swallowed
    return e.Next()
})
```

**Correct (sender from settings, per-send client, explicit error path):**

```go
import (
    "net/mail"
    pbmail "github.com/pocketbase/pocketbase/tools/mailer"
)

app.OnRecordAfterCreateSuccess("orders").BindFunc(func(e *core.RecordEvent) error {
    // IMPORTANT: resolve the sender from settings at send-time, not at
    // startup - an admin can change it live from the UI
    meta := e.App.Settings().Meta
    from := mail.Address{
        Name:    meta.SenderName,
        Address: meta.SenderAddress,
    }

    msg := &pbmail.Message{
        From:    from,
        To:      []mail.Address{{Address: e.Record.GetString("email")}},
        Subject: "Order confirmed",
        HTML:    renderOrderEmail(e.Record), // your template function
    }

    // Create the client per send - avoids stale TCP sessions
    if err := e.App.NewMailClient().Send(msg); err != nil {
        e.App.Logger().Error("order email send failed",
            "err",      err,
            "recordId", e.Record.Id,
        )
        // Do NOT return the error - a failed email should not roll back the order
    }
    return e.Next()
})
```

```javascript
// JSVM - $mails global exposes message factories
onRecordAfterCreateSuccess((e) => {
    const meta = $app.settings().meta;

    const message = new MailerMessage({
        from: {
            address: meta.senderAddress,
            name:    meta.senderName,
        },
        to:      [{ address: e.record.get("email") }],
        subject: "Order confirmed",
        html:    `<p>Thanks for order ${e.record.id}</p>`,
    });

    try {
        $app.newMailClient().send(message);
    } catch (err) {
        $app.logger().error("order email send failed", "err", err, "id", e.record.id);
        // swallow - do not rollback the order
    }
    e.next();
}, "orders");
```

**Templated emails via the built-in verification/reset templates:**

```go
// PocketBase has baked-in templates for verification, password reset, and
// email change. Trigger them via apis.*Request helpers rather than building
// your own message:
//   apis.RecordRequestPasswordReset(app, authRecord)
//   apis.RecordRequestVerification(app, authRecord)
//   apis.RecordRequestEmailChange(app, authRecord, newEmail)
//
// These use the templates configured in Admin UI → Settings → Mail templates.
```

**Rules:**
- **Always change `Meta.SenderAddress`** before shipping. In development, use Mailpit or MailHog; in production, use a verified domain that matches your SPF/DKIM records.
- **Resolve the sender from `app.Settings().Meta` at send-time**, not at startup. Settings are mutable from the admin UI.
- **Create the client per send** (`app.NewMailClient()` / `$app.newMailClient()`). It is cheap - it re-reads the SMTP settings each time, so config changes take effect without a restart.
- **Never return a send error from a hook** unless the user's action genuinely depends on the email going out. Email failure is common (transient SMTP, address typo) and should not roll back a business transaction.
- **Log failures with context** (record id, recipient domain) so you can grep them later. PocketBase does not retry failed sends.
- **For bulk sending, queue it**. The mailer is synchronous - looping `Send()` over 10k records blocks the request. Push to a cron-drained queue collection instead.
- **Template rendering**: Go users should use `html/template`; JS users can use template literals or pull in a tiny template lib. PocketBase itself only renders templates for its baked-in flows.

Reference: [Go Mailer](https://pocketbase.io/docs/go-sending-emails/) · [JS Mailer](https://pocketbase.io/docs/js-sending-emails/)
