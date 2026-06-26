# Event Page Setup Guide

## Overview

The event landing page is a static HTML form at `site/commercial/index.html` (or similar path on your hostinger/YOUR_DOMAIN deployment). It submits directly to a Supabase Edge Function which registers the lead in Renatus Back Office.

## Page Structure

### Registration Form Fields
- `firstName` (required)
- `lastName` (required)
- `email` (required)
- `phone` (required)
- `website` (honeypot — hidden, must be empty)
- `source_page` (auto-populated from `window.location.href`)

### Submit Endpoint
```
POST https://<PROJECT_REF>.supabase.co/submit-renatus-registration
```

### Request Body
```json
{
  "firstName": "Jane",
  "lastName": "Smith",
  "email": "jane@example.com",
  "phone": "(555) 555-5555",
  "website": "",
  "source_page": "https://YOUR_DOMAIN/commercial/"
}
```

### Success Response
```json
{
  "ok": true,
  "eventId": "0817966f-b9bb-448e-bbb8-b4160115bcc8",
  "eventName": "Commercial Core - Live Education",
  "registrationId": "...",
  "leadId": "...",
  "guestUserId": "...",
  "registeredSessions": ["Session Name 1", "Session Name 2"]
}
```

### Error Response
```json
{ "error": "Error message", "details": "optional details" }
```

## Setting Up a New Event Page

### 1. Copy the Template
Copy `site/commercial/index.html` to a new directory, e.g., `site/<event-slug>/index.html`

### 2. Update the Edge Function URL
In the `<script>` section, update:
```javascript
const EDGE_URL = 'https://<PROJECT_REF>.supabase.co/submit-renatus-registration';
```

### 3. Update Event Details
Update the visible event details in the HTML (date, location, speakers, description).

### 4. Update the Event ID
Either:
- Set `RENATUS_EVENT_ID` secret in Supabase (affects all form submissions)
- Add `eventId` field to the form and pass it in the payload

### 5. Get the Event GUID from Renatus
1. Log into `backoffice.myrenatus.com`
2. Navigate to Events
3. Open the event
4. Copy the event GUID from the URL or API response

### 6. Verify Registration Flow
Submit a test registration and confirm:
- Lead appears in `funnel_leads` table
- Lead appears in Renatus Back Office
- Email confirmation is sent by Renatus

## Customizing the Landing Page

### Styling
The page uses CSS custom properties for easy theming:
```css
:root {
  --bg: #0f172a;
  --card: #111827;
  --accent: #22c55e;
  --text: #e5e7eb;
}
```

### Adding a Second Event (In-Person Option)
Modify the `feesPayload` to include multiple sessions, or use separate event pages with different event IDs.

### Redirect to Confirmation Page
After successful form submission:
```javascript
if (resp.ok) {
  window.location.href = '/confirmation.html';
}
```

## Hosting Options

### Option A: Deploy with your hosting scripts
```bash
python3 scripts/deploy_hostinger.py
```

### Option B: Manual FTP Upload
Upload `site/commercial/` directory to your web host's `public_html/` or equivalent.

### Option C: Subdirectory on Existing Site
Upload to `public_html/commercial/` — page will be at `https://yourdomain.com/commercial/`

## Confirmation Page
After successful registration, redirect users to a confirmation page. The confirmation page shows event details and next steps. See `site/confirmation.html` for the template.

## Troubleshooting

### "Registration could not be completed"
- Check browser console for specific error
- Verify Supabase Edge Function URL is correct
- Check Supabase function logs in the dashboard

### Lead not appearing in Renatus
- Verify `RENATUS_USERNAME` and `RENATUS_PASSWORD` secrets are set
- Check function logs for authentication errors (401 = bad credentials)
- Confirm event GUID is valid and event is published in Renatus

### Public sessions not found
- Event may only have education-gated sessions
- Check `isPublicEligibleSession` in the edge function — sessions requiring IMA, Xtream Education, or other credentials are excluded
- Contact Renatus to create a public-eligible session for the event
