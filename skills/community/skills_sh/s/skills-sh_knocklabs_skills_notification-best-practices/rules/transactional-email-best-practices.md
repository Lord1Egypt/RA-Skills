---
title: Transactional email best practices
description: Comprehensive guide to deliverability, templates, localization, and dynamic content for transactional emails
tags:
  - email
  - transactional-email
  - deliverability
  - email-templates
  - localization
  - personalization
  - dynamic-content
  - email-design
  - spf
  - dkim
  - dmarc
category: notification-best-practices
last_updated: 2026-01-23
---

# Transactional email best practices

## Deliverability best practices

### Use a subdomain
Send transactional emails from a subdomain to prevent damaging your primary domain's reputation. Always use different subdomains for transactional vs. marketing emails.

**Why it matters**: Marketing emails are more likely to be flagged as spam. Separating them protects your critical transactional messages.

**Avoid**: Look-a-like domains (spammers use these, and email providers penalize them)

**Domain warming**: Each new subdomain must be warmed up by slowly increasing sending volume over time.

### Don't use no-reply emails
No-reply emails signal one-way communication and decrease trust with mailbox providers. Receiving replies actually improves your domain health.

### Avoid link and open tracking when possible
While valuable for marketing emails, link tracking and open tracking can hurt deliverability for transactional emails like notifications and magic links if the link doesn't contain your domain.

### Keep emails small and accessible
- **Gmail size limit**: 102KB (content is clipped after this)
- **Include plain text version**: Ensures accessibility for all email clients
- **Minimize images**: Helps with both size and accessibility

### Maintain a clean email list
Only send to recipients who've requested to receive emails:
- Don't send to unsubscribers
- Remove non-engaged recipients
- Remove spam complaint addresses
- Set up automated workflows to track bounces (hard or soft) and remove those recipients

### Send consistently
Mailbox providers are suspicious of sudden volume changes. To send thousands of emails regularly:
- Warm up your domain by sending consistently ahead of time
- Avoid sudden spikes in volume
- Inconsistent sending leads to bounce rates and reputation damage

## Email template best practices

### Use componentized templates
Modern transactional email requires a componentized approach that mirrors frontend development best practices.

**Basic hierarchy:**
```html
<!-- Email Layout (the frame) -->
<html>
  <head>
    {{ styles }}
  </head>
  <body>
    {{ header_partial }}
    
    <div class="content">
      {{ content }}  <!-- Your template content goes here -->
    </div>
    
    {{ footer_partial }}
  </body>
</html>
```

**Individual template:**
```html
<!-- Password Reset Template -->
<h1>Reset your password</h1>
<p>Hi {{ user.name }},</p>
<p>Click the link below to reset your password:</p>
<a href="{{ reset_link }}" class="button button-primary">
  Reset Password
</a>
```

**Benefits:**
- **Consistency**: Update header once, it changes everywhere
- **Maintainability**: No hunting through 50 templates to update a logo
- **Flexibility**: Different layouts for different email types

### Build a partial system
Partials are reusable chunks of email content that can be included across multiple templates.

**Reusable UI component example:**
```html
<!-- _button.liquid partial -->
<table class="button-wrapper">
  <tr>
    <td class="button {{ variant | default: 'primary' }}">
      <a href="{{ url }}">{{ text }}</a>
    </td>
  </tr>
</table>

<!-- Usage in template -->
{% include '_button' url: product_url, text: "View Order", variant: "secondary" %}
```

**Dynamic content block example:**
```html
<!-- _order_summary.liquid partial -->
<div class="order-summary">
  <h3>Order #{{ order.number }}</h3>
  <ul class="item-list">
    {% for item in order.items %}
      <li>
        <span class="item-name">{{ item.name }}</span>
        <span class="item-quantity">× {{ item.quantity }}</span>
        <span class="item-price">{{ item.price | currency }}</span>
      </li>
    {% endfor %}
  </ul>
  <div class="order-total">
    Total: {{ order.total | currency }}
  </div>
</div>
```

## Localization best practices

### Use translation keys
Organize content into hierarchical JSON structures for easy language swapping.

**Translation files:**
```json
// translations/en.json
{
  "password_reset": {
    "subject": "Reset your password",
    "greeting": "Hi {{name}},",
    "body": "We received a request to reset your password.",
    "cta": "Reset Password",
    "expiry_warning": "This link expires in {{hours}} hours.",
    "footer": "If you didn't request this, please ignore this email."
  }
}

// translations/es.json
{
  "password_reset": {
    "subject": "Restablecer tu contraseña",
    "greeting": "Hola {{name}},",
    "body": "Recibimos una solicitud para restablecer tu contraseña.",
    "cta": "Restablecer Contraseña",
    "expiry_warning": "Este enlace expira en {{hours}} horas.",
    "footer": "Si no solicitaste esto, ignora este correo."
  }
}
```

**Template usage:**
```html
<h1>{{ "password_reset.subject" | t }}</h1>
<p>{{ "password_reset.greeting" | t: name: user.first_name }}</p>
<p>{{ "password_reset.body" | t }}</p>
<a href="{{ reset_url }}">
  {{ "password_reset.cta" | t }}
</a>
<p class="warning">
  {{ "password_reset.expiry_warning" | t: hours: 24 }}
</p>
```

## Dynamic content best practices

### Conditional logic
Adapt content based on user behavior and account status.

**Example:**
```html
{% if user.is_premium %}
  <div class="premium-banner">
    <h3>Thanks for being a Premium member!</h3>
    <p>You saved {{ order.premium_discount | currency }} on this order.</p>
  </div>
{% elsif user.trial_ending_soon %}
  <div class="trial-banner">
    <h3>Your trial ends in {{ user.trial_days_left }} days</h3>
    <a href="{{ upgrade_url }}">Upgrade to keep your benefits</a>
  </div>
{% endif %}

<!-- Dynamic CTAs based on user state -->
{% case user.onboarding_step %}
{% when 'profile_incomplete' %}
  <a href="{{ complete_profile_url }}" class="button">
    Complete Your Profile
  </a>
{% when 'payment_pending' %}
  <a href="{{ add_payment_url }}" class="button">
    Add Payment Method
  </a>
{% else %}
  <a href="{{ dashboard_url }}" class="button">
    Go to Dashboard
  </a>
{% endcase %}
```

### Usage statistics
Share relevant metrics and insights in transactional emails.

**Example:**
```html
<!-- Weekly summary email -->
<div class="usage-stats">
  <h2>Your week at a glance</h2>
  
  <div class="stat-grid">
    <div class="stat">
      <span class="value">{{ stats.tasks_completed }}</span>
      <span class="label">Tasks completed</span>
      <span class="change {{ stats.tasks_change_class }}">
        {{ stats.tasks_change }}% vs last week
      </span>
    </div>
    
    <div class="stat">
      <span class="value">{{ stats.time_saved | format_duration }}</span>
      <span class="label">Time saved</span>
    </div>
  </div>
  
  <!-- Personalized insight -->
  {% if stats.most_productive_day %}
    <p class="insight">
      💡 You're most productive on {{ stats.most_productive_day }}s. 
      Consider scheduling important work then!
    </p>
  {% endif %}
</div>
```

### Behavioral personalization
Use browsing history and user data for relevant recommendations.

**Example:**
```html
<!-- In an order confirmation email -->
{% if related_products.size > 0 %}
  <div class="recommendations">
    <h3>You might also like</h3>
    <div class="product-grid">
      {% for product in related_products limit: 3 %}
        <div class="product-card">
          <img src="{{ product.image_url }}" alt="{{ product.name }}">
          <h4>{{ product.name }}</h4>
          <p>{{ product.price | currency }}</p>
          
          <!-- Smart messaging based on user history -->
          {% if product.id in user.previously_viewed %}
            <span class="badge">Previously viewed</span>
          {% elsif product.discount > 0 %}
            <span class="badge">{{ product.discount }}% off</span>
          {% endif %}
        </div>
      {% endfor %}
    </div>
  </div>
{% endif %}
```

## Mobile optimization

### Design considerations
- Use single-column layouts
- Minimum button size: 44x44 pixels
- Minimum font size: 14px
- Keep images under 1MB
- Maintain 80:20 text-to-image ratio

### Testing requirements
- Test across major email clients (Gmail, Outlook, Apple Mail)
- Test on multiple device sizes
- Verify subject line and preview text truncation
- Check CTA button functionality
- Ensure images load properly