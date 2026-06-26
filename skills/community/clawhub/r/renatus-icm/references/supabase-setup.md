# Supabase Setup for Renatus ICM

## Overview

Supabase project: `YOUR_PROJECT_NAME` (EU-West-1 — or any region)

Stores lead registrations from the public event landing page and exposes an admin export endpoint for ICMs to download leads.

## 1. Link and Push Migrations

```bash
cd supabase
supabase link --project-ref <PROJECT_REF>
supabase db push --include-all
```

## 2. Deploy Edge Functions

```bash
supabase functions deploy submit-renatus-registration --project-ref <PROJECT_REF>
supabase functions deploy lead-admin-export --project-ref <PROJECT_REF>
supabase functions deploy capture-lead --project-ref <PROJECT_REF>
supabase functions deploy stripe-webhook --project-ref <PROJECT_REF>
```

## 3. Set Required Secrets

```bash
supabase secrets set \
  RENATUS_USERNAME="<renatus_backoffice_email>" \
  RENATUS_PASSWORD="<renatus_backoffice_password>" \
  RENATUS_EVENT_ID="<default_event_guid>" \
  SUPABASE_URL="https://<PROJECT_REF>.supabase.co" \
  SUPABASE_SERVICE_ROLE_KEY="<service_role_key>" \
  LEAD_ADMIN_TOKEN="<secure_random_token_for_admin_export>" \
  --project-ref <PROJECT_REF>
```

## 4. Key Tables

### funnel_leads
```sql
create table if not exists public.funnel_leads (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  source_page text,
  name text,
  email text,
  company text,
  notes text,
  cta_type text,
  metadata jsonb not null default '{}'::jsonb
);
```

### funnel_leads metadata field
Contains: `event_id`, `registration_id`, `lead_id`, `guest_user_id`, `registered_sessions`, `phone`

## 5. Key Edge Functions

### submit-renatus-registration
- **URL:** `https://<PROJECT_REF>.functions.supabase.co/submit-renatus-registration`
- **Method:** POST
- **Auth:** Public (honeypot + Turnstile bot protection)
- **Session eligibility:** Auto-detects public-eligible sessions (no IMA/education requirements)
- **Response:** `{ ok, eventId, eventName, registrationId, leadId, guestUserId, registeredSessions }`

### lead-admin-export
- **URL:** `https://<PROJECT_REF>.functions.supabase.co/lead-admin-export`
- **Method:** GET
- **Auth:** `x-admin-token: <LEAD_ADMIN_TOKEN>` header
- **Params:** `?partner=<optional_partner_slug>&limit=<1-500>`
- **Response:** `{ ok, count, rows: [...] }`

## 6. Configure Stripe Webhook (Optional)

Endpoint: `https://<PROJECT_REF>.functions.supabase.co/stripe-webhook`
Listen for: `checkout.session.completed`

## 7. Verify End-to-End

1. Submit lead form at `/commercial/index.html`
2. Confirm row in `funnel_leads`
3. Verify lead in Renatus Back Office
4. Export: `curl -H "x-admin-token: $TOKEN" "https://<REF>.functions.supabase.co/lead-admin-export?limit=10"`

## Required Secrets Reference

| Variable | Required | Description |
|---|---|---|
| `RENATUS_USERNAME` | Yes | Renatus back office email |
| `RENATUS_PASSWORD` | Yes | Renatus back office password |
| `RENATUS_EVENT_ID` | No | Default event GUID |
| `SUPABASE_URL` | Yes | Project URL |
| `SUPABASE_SERVICE_ROLE_KEY` | Yes | Service role key |
| `LEAD_ADMIN_TOKEN` | Yes (export) | Admin export bearer token |
| `STRIPE_SECRET_KEY` | Payments | Stripe secret key |
| `STRIPE_WEBHOOK_SECRET` | Payments | Stripe webhook secret |
| `TURNSTILE_SECRET_KEY` | No | Cloudflare Turnstile |
