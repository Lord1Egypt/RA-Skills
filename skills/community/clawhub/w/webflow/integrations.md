# Webflow Integrations

## Forms

**Native forms:**
- Work out of the box for email notifications
- Limited to 2,500 submissions/month (Business plan)

**Form notifications fail silently.** Test with real email before launch.

**Webhook alternative:**
1. Form Settings → Add Webhook
2. Point to Zapier/Make/n8n/custom endpoint
3. Parse form data in webhook handler

**Connect to CRM without Zapier:**
```html
<!-- Custom form action -->
<form action="https://your-crm.com/api/leads" method="POST">
  <!-- Hidden field for API routing -->
  <input type="hidden" name="source" value="webflow-landing">
</form>
```

## Analytics

**Google Analytics 4:**
1. Project Settings → Custom Code
2. Paste GA4 tag in `<head>` section
3. Verify in GA4 Real-Time reports

**Conversion tracking:**
```javascript
// On form submit success
gtag('event', 'generate_lead', {
  'event_category': 'form',
  'event_label': 'contact_form'
});
```

**Don't use Webflow's built-in analytics** for serious tracking. It's basic page views only.

## Third-Party Embeds

**Chat widgets (Intercom, Crisp, Drift):**
- Add script to Site Settings → Custom Code → Footer
- NOT in page embeds (loads multiple times)

**Payment forms (Stripe):**
- Use Stripe.js embed in custom code block
- Style to match site via Stripe's appearance API

**Calendar booking (Calendly, Cal.com):**
- Inline embed: paste iframe in embed block
- Popup: use their script + trigger button

## Common Embed Issues

**Script loading order:**
- Dependencies in `<head>`, execution scripts in footer
- Use `defer` or `async` attributes appropriately

**Embed breaks on publish:**
- Webflow sanitizes some HTML
- Wrap in `<div>` container
- Check browser console for errors

**Mobile responsiveness:**
- Embedded iframes need responsive wrapper
```html
<div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;">
  <iframe style="position:absolute;top:0;left:0;width:100%;height:100%;"></iframe>
</div>
```
