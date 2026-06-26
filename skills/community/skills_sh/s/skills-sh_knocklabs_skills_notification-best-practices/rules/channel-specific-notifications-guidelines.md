---
title: Channel-specific notification guidelines
description: Detailed specifications and best practices for email, push, SMS, in-app, and chat notifications
tags:
  - notifications
  - channels
  - email
  - push-notifications
  - sms
  - in-app
  - slack
  - teams
  - character-limits
  - formatting
category: notification-best-practices
last_updated: 2026-01-23
---

# Channel-specific notification guidelines

## Quick reference table

| Channel | Max Length | Structure | Tone | Images | Links |
|---------|-----------|-----------|------|--------|-------|
| **Email** | Subject: ~60 chars<br>Body: No limit | Subject + Preheader + Greeting + Core message + CTA + Signature | Professional, informative, personalized | Yes (optimize for mobile) | Yes (multiple) |
| **SMS** | 160 chars (GSM7)<br>70 chars (with emoji) | Clear CTA up front + context | Concise, direct, action-oriented | No | Yes (one short link) |
| **In-app** | ~60-80 chars per message | Short headline + body + CTA button | Helpful, contextual, minimal | Yes (small icons) | Yes (CTA buttons) |
| **Push** | iOS: ~178 chars total<br>Android: ~305 chars total | Short hook + 1-line CTA | Urgent, clear, concise | No (small icons only) | Yes (1 link max) |
| **Chat apps** | No limit, keep concise | Contextual header + brief message + optional button | Conversational, friendly, informative | Yes (thumbnails) | Yes (buttons or inline) |

## Email notifications

### Subject lines
**Guidelines:**
- Maximum ~60 characters before truncation
- Front-load the most important information
- Include specific details (names, numbers, items)
- Avoid spam triggers (excessive caps, multiple exclamation points)

**Examples:**
```
📄 Invoice #4521 paid by Acme Corp
👥 3 new candidates applied for Senior Engineer role
💾 Your export of Q4 customer data is ready
```

### Preview text
**Guidelines:**
- Maximum ~90 characters on desktop, ~35 on mobile
- Complement the subject line, don't repeat it
- Include actionable information or next steps
- Write complete thoughts that make sense even if truncated

**Examples:**
```
👀 Review their feedback and approve changes directly from this email
⏳ You have 24 hours left to claim your early bird discount. Register now
💬 Sarah Chen and 2 others are waiting for your input on the roadmap
```

### Email body content
**Guidelines:**
- **Greeting**: Use recipient's name when available
- **Primary message**: State the notification reason in the first sentence
- **Context**: Provide relevant details (but keep it scannable)
- **Call-to-action**: Make buttons/links obvious and descriptive
- **Footer**: Include unsubscribe and preference options

**Example:**
```
Hi {{user.name}},

{{actor.name}} requested access to the {{resource.name}} dashboard.

**Request details:**
- Access level requested: Editor
- Reason: "Need to update Q4 metrics"
- Expires: 7 days from approval

[Approve Request] [Deny Request]

You can manage all pending requests in your [team settings].
```

## Push notifications

### Character limits
**iOS**: 4 lines total (~50 chars for title, ~175 for body)
**Android**: 7 lines total (~65 chars for title, ~240 for body)

**Note**: These limits vary by device model, screen size, and user settings. Use conservative limits to ensure messages display properly across all devices.

### Guidelines
- Lead with the user benefit or required action
- Include specific details (names, amounts, items)
- Ensure the message makes sense without opening the app
- Adhere to character limits by device type

### Examples
```
👍 Expense report approved
Sarah approved your expense report for $234.50

📈 Your weekly report is ready
There was a 15% increase in conversions

🚨 Inventory alert
The Blue Widget stock is below your reorder point (12 units)
```

## SMS notifications

### Character limits
**160 characters** for GSM7 encoding
**70 characters** if any character requires UCS-2 encoding (like emojis)

**Critical**: When an SMS contains even a single character not supported by GSM7, the entire message switches to UCS-2 encoding, reducing the character limit from 160 to 70.

### Guidelines
- Identify your service (if not obvious from sender)
- State the key information
- Include action if needed
- Always provide opt-out instructions for marketing messages
- Adhere to character limits

### Examples
```
🔐 Knock: Your password reset code is 445-892. Valid for 10 minutes.

💰 Payment of $125.00 received from ABC Corp for Invoice #4412. View details: [link]

🎗️ Appointment reminder: Dr. Smith tomorrow (Jan 5) at 2:30 PM. Reply C to confirm.
```

## In-app notifications

### Notification feed
A persistent collection of notifications accessible through a dedicated interface element (bell icon or sidebar).

**Guidelines:**
- Include timestamp (relative when recent: "2 hours ago")
- Support scanning with consistent structure
- Group related notifications when possible
- Mark read/unread states clearly

**Structure:**
```
[Avatar] **Actor** action object
Supplementary details
[Timestamp] [Secondary action]
```

**Examples:**
```
💬 Sarah Chen commented on your design proposal
"Love the new navigation approach!"
2 hours ago • View comment

✅ Team Alpha completed sprint planning
15 story points across 8 tasks
Yesterday at 3:47 PM • View sprint

🆕 3 new applicants for Senior Engineer role
Marcus Liu and 2 others applied
Oct 23 • Review applications
```

### Toast notifications
Brief, temporary messages that appear on screen and disappear automatically.

**Guidelines:**
- ~60-80 chars per message (varies by UI)
- Single, clear message
- Avoid multiple actions
- Auto-dismiss after 5-7 seconds for non-critical messages

**Examples:**
```
👉 "Settings saved successfully"
👉 "Jason Lee started reviewing your pull request"
👉 "Export complete: 2,847 records processed"
```

## Chat app notifications

Used in Slack or Microsoft Teams, blending the richness of email with the immediacy of push.

### Guidelines
- Use `*bold*` for emphasis
- Include `@mentions` when appropriate
- Leverage emojis for visual scanning 🎯
- Use code blocks for technical information
- For Slack, create sections with Block Kit for complex messages

### Examples
```
🚨 **Production alert**
CPU usage exceeded 90% on server `api-prod-02`
Current: 94% | Duration: 5 minutes

🎉 **New customer signup!**

**Company**: Acme Corporation
**Plan**: Enterprise ($499/month)
**Users**: 50 seats

The sales team has been notified. View full details in the customer dashboard.
```