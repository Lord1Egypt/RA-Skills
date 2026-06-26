---
title: Notification template examples
description: Ready-to-use notification templates for common use cases across all channels with implementation guidelines
tags:
  - notifications
  - templates
  - examples
  - code-samples
  - liquid
  - email-templates
  - push-templates
  - sms-templates
  - implementation
category: notification-best-practices
last_updated: 2026-01-23
---

# Notification template examples

## Starter templates for common use cases

### New user signup (email)

```liquid
Subject: {{actor.name}} joined your {{workspace.name}} workspace

Hi {{user.name}},

{{actor.name}} ({{actor.email}}) just joined your workspace as {{actor.role}}.

{{#if pending_approval}}
This user is pending approval. You can:
[Approve Access] [Deny Access]
{{else}}
They now have access to:
- {{list_of_permissions}}
{{/if}}

Manage team permissions anytime in [workspace settings].
```

**When to use**: Team collaboration products, workspace management

**Key elements**:
- Clear identification of who joined
- Role and permissions context
- Conditional approval flow
- Link to management tools

---

### Payment received (SMS)

```
Payment confirmed: ${{amount}} from {{customer.name}} for Invoice #{{invoice.number}}. Balance: ${{remaining_balance}}
```

**When to use**: Payment processing, invoicing systems

**Key elements**:
- Transaction confirmation
- Specific amounts
- Reference numbers
- Remaining balance context

---

### Collaboration activity (in-app)

```liquid
{{actor.name}} {{action}} {{object.type}} "{{object.name}}"
{{#if comment}}"{{comment}}"{{/if}}
{{timestamp}}
```

**When to use**: Any collaborative product (docs, design, project management)

**Key elements**:
- Actor-action-object structure
- Optional comment/message
- Timestamp for context
- Scannable format

---

### System alert (push)

```
{{alert.severity}} alert: {{alert.title}}
{{alert.description}}
[View details] [Acknowledge]
```

**When to use**: DevOps tools, monitoring systems, critical alerts

**Key elements**:
- Severity level
- Clear title and description
- Multiple action options
- Urgency indicators

---

### Password reset (email)

```liquid
Subject: Reset your password

Hi {{user.name}},

We received a request to reset your password for {{app.name}}.

[Reset Password]

This link expires in {{expiry.hours}} hours.

If you didn't request this, you can safely ignore this email. Your password won't change until you create a new one via the link above.

For security, this link can only be used once.
```

**When to use**: Authentication flows, security events

**Key elements**:
- Clear purpose statement
- Prominent CTA
- Expiration information
- Security reassurance
- Single-use clarification

---

### Order confirmation (email)

```liquid
Subject: Order #{{order.number}} confirmed

Hi {{customer.name}},

Thanks for your order! We're preparing it for shipment.

**Order summary**
Order #{{order.number}}
Date: {{order.date}}

{% for item in order.items %}
- {{item.name}} ({{item.quantity}}) - {{item.price | currency}}
{% endfor %}

**Subtotal**: {{order.subtotal | currency}}
**Shipping**: {{order.shipping | currency}}
**Total**: {{order.total | currency}}

**Shipping to:**
{{shipping.address}}

Track your order: [link]
View full details: [link]

Questions? Reply to this email or visit our help center.
```

**When to use**: E-commerce, marketplaces, order processing

**Key elements**:
- Order reference number
- Itemized list
- Pricing breakdown
- Shipping details
- Action links
- Support information

---

### Weekly digest (email)

```liquid
Subject: Your weekly summary: {{stats.highlight}}

Hi {{user.name}},

Here's what happened in {{app.name}} this week.

**Activity**
- {{stats.actions}} actions completed
- {{stats.collaborators}} team members active
- {{stats.items}} new items created

**Top performing**
{{#each top_items}}
- {{this.name}}: {{this.metric}}
{{/each}}

**This week's insights**
{{#if insights}}
{{insights.message}}
{{/if}}

[View Full Dashboard]

---
Prefer daily summaries? [Update preferences]
```

**When to use**: Activity summaries, productivity tools, analytics platforms

**Key elements**:
- Timeframe clarity
- Key metrics upfront
- Personalized insights
- Dashboard access
- Preference management

---

### Mention notification (chat)

```
**{{actor.name}}** mentioned you in **{{context.location}}**

> {{message.preview}}

[View conversation] [Reply]
```

**When to use**: Collaboration tools, team chat, social features

**Key elements**:
- Who mentioned you
- Where it happened
- Message preview
- Quick action buttons

---

### Scheduled maintenance (multiple channels)

**Email version:**
```liquid
Subject: Scheduled maintenance: {{date}} at {{time}}

Hi {{user.name}},

We'll be performing scheduled maintenance on {{date}} from {{time_start}} to {{time_end}} {{timezone}}.

**What to expect:**
- {{app.name}} will be unavailable during this window
- All data is safe and will be preserved
- No action required on your part

**Why we're doing this:**
{{maintenance.reason}}

Questions? Our team is here to help: [contact support]

We appreciate your patience as we improve {{app.name}}.
```

**SMS Version:**
```
{{app.name}} maintenance {{date}} {{time_start}}-{{time_end}} {{timezone}}. Service will be unavailable. No action needed. Details: [link]
```

**When to use**: System maintenance, planned downtime

**Key elements**:
- Clear timeframe with timezone
- Expected impact
- Reassurance
- Contact information

---

### Trial ending (email)

```liquid
Subject: Your trial ends in {{days_remaining}} days

Hi {{user.name}},

Your {{app.name}} trial ends on {{trial_end_date}}.

**What you've accomplished:**
- {{stats.metric1}}: {{stats.value1}}
- {{stats.metric2}}: {{stats.value2}}
- {{stats.metric3}}: {{stats.value3}}

Continue your progress by upgrading to {{plan.name}}.

**{{plan.name}} includes:**
- {{feature.1}}
- {{feature.2}}
- {{feature.3}}

[Upgrade Now] [Compare Plans]

Questions about upgrading? [Schedule a call with our team]

Don't want to upgrade? Your account will automatically convert to our free plan on {{trial_end_date}}.
```

**When to use**: SaaS trials, freemium conversions

**Key elements**:
- Days remaining
- Value demonstration
- Plan benefits
- Multiple CTAs
- Fallback option

---

### Comment/reply (in-app)

```liquid
{{actor.name}} replied to your comment

"{{comment.text}}"

In: {{context.item_name}}
{{timestamp}}

[Reply] [View thread]
```

**When to use**: Discussion threads, document comments, feedback systems

**Key elements**:
- Clear action (replied)
- Comment preview
- Context/location
- Quick actions

---

### Feature announcement (email)

```liquid
Subject: New: {{feature.name}}

Hi {{user.name}},

We built something you asked for: {{feature.name}}.

**What it does:**
{{feature.description}}

**Why you'll love it:**
{{#each benefits}}
- {{this.benefit}}
{{/each}}

**How to use it:**
{{feature.instructions}}

[Try it now]

**Example:**
{{feature.example}}

We'd love to hear what you think. Reply to this email with feedback.
```

**When to use**: Product updates, feature launches

**Key elements**:
- Feature name and description
- Clear benefits
- Usage instructions
- Examples
- Feedback loop

---

### Failed payment (email + SMS)

**Email version:**
```liquid
Subject: Payment failed for {{subscription.name}}

Hi {{user.name}},

We couldn't process your payment for {{subscription.name}}.

**What happened:**
{{error.message}}

**What you need to do:**
Update your payment method to continue your subscription.

[Update Payment Method]

If you don't update your payment method by {{deadline}}, your account will be downgraded to the free plan.

**Need help?** Our team is here: [contact support]
```

**SMS Version:**
```
{{app.name}}: Payment failed for {{subscription.name}}. Update payment method to avoid service interruption: [link]
```

**When to use**: Subscription billing, payment processing

**Key elements**:
- Clear problem statement
- Specific error
- Action required
- Deadline
- Consequences
- Support access

## Template variables best practices

### Common variable patterns

**User context:**
```liquid
{{user.name}}
{{user.email}}
{{user.role}}
{{user.timezone}}
{{user.preferences.*}}
```

**Actor context:**
```liquid
{{actor.name}}
{{actor.avatar_url}}
{{actor.email}}
```

**Object context:**
```liquid
{{object.type}}
{{object.name}}
{{object.id}}
{{object.url}}
```

**Timestamp formatting:**
```liquid
{{timestamp}}  // "2 hours ago"
{{timestamp | date: "full"}}  // "January 23, 2026 at 2:30 PM"
{{timestamp | date: "short"}}  // "Jan 23"
```

**Conditional logic:**
```liquid
{{#if condition}}
  Show this content
{{else}}
  Show alternative
{{/if}}

{{#each items}}
  {{this.property}}
{{/each}}
```

## Fallback strategies

### Handle missing data
```liquid
{{user.name | default: "there"}}
{{object.name | default: "item"}}
{{stats.value | default: 0}}
```

### Graceful degradation
```liquid
{{#if user.avatar_url}}
  <img src="{{user.avatar_url}}" />
{{else}}
  <div class="avatar-fallback">{{user.initials}}</div>
{{/if}}
```

### Error states
```liquid
{{#if error}}
  <div class="error-message">
    {{error.friendly_message | default: "Something went wrong. Please try again."}}
  </div>
{{/if}}
```