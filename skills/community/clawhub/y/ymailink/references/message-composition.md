# Message Composition Reference

ymailink uses standard RFC 822 message format for composing emails. Messages are plain text with headers followed by a body, separated by a blank line.

## Basic Message Structure

An email message consists of **headers** followed by a blank line and then the **body**:

```
From: sender@example.com
To: recipient@example.com
Subject: Hello World

This is the message body.
```

## Headers

Common headers:
- `From`: Sender address
- `To`: Primary recipient(s)
- `Cc`: Carbon copy recipients
- `Bcc`: Blind carbon copy recipients
- `Subject`: Message subject
- `Reply-To`: Address for replies (if different from From)
- `In-Reply-To`: Message-ID being replied to (for threading)
- `References`: Chain of Message-IDs in the thread

### Address Formats

Single address:
```
To: user@example.com
```

Address with display name:
```
To: John Doe <john@example.com>
To: "John Doe" <john@example.com>
```

Multiple recipients:
```
To: user1@example.com, user2@example.com, "Jane" <jane@example.com>
```

## Plain Text Body

Simple plain text email:
```
From: alice@example.com
To: bob@example.com
Subject: Plain Text Example

Hello, this is a plain text email.
No special formatting needed.

Best,
Alice
```

## Reply Format

When replying, the original message is quoted with `>` prefix:
```
From: bob@example.com
To: alice@example.com
Subject: Re: Plain Text Example
In-Reply-To: <original-message-id@example.com>
References: <original-message-id@example.com>

Thanks for the message!

> Hello, this is a plain text email.
> No special formatting needed.
>
> Best,
> Alice
```

## Forward Format

When forwarding, the original message is included with a separator:
```
From: bob@example.com
To: charlie@example.com
Subject: Fwd: Plain Text Example

---------- Forwarded message ----------
From: alice@example.com
To: bob@example.com
Subject: Plain Text Example
Date: 2025-01-15 10:30:00

Hello, this is a plain text email.
No special formatting needed.

Best,
Alice
```

## Composing Methods

### Interactive Compose (opens $EDITOR)

Write a new message:
```bash
ymailink mail write
```

With preset headers:
```bash
ymailink mail write --headers "To:recipient@example.com" --headers "Subject:Hello"
```

Reply to a message:
```bash
ymailink mail reply 42
ymailink mail reply 42 --all   # reply to all recipients
```

Forward a message:
```bash
ymailink mail forward 42
```

### Send from File or Stdin

Send a pre-composed message file:
```bash
ymailink mail send message.txt
```

Send from stdin:
```bash
cat << 'EOF' | ymailink mail send -
From: you@example.com
To: recipient@example.com
Subject: Test Message

Hello from ymailink!
EOF
```

### Template Workflow (Programmatic)

Generate a template, edit it, then send:
```bash
# Generate blank template
ymailink template write > msg.txt

# Generate reply template with quoted original
ymailink template reply 42 > reply.txt

# Generate forward template
ymailink template forward 42 > fwd.txt

# Edit the template file...
$EDITOR msg.txt

# Send the template
ymailink template send msg.txt

# Or from stdin
cat msg.txt | ymailink template send -
```

### Save as Draft

Save a message to the Drafts folder without sending:
```bash
ymailink template save msg.txt
cat msg.txt | ymailink template save -
```

## Tips

- The `From` header is automatically filled from the account config if omitted.
- Save and exit the editor to send; exit without saving to cancel.
- Use `template write` + `template send` for non-interactive automation workflows.
- Message IDs in `In-Reply-To` and `References` enable proper threading.
- ymailink handles MIME encoding automatically when sending.
