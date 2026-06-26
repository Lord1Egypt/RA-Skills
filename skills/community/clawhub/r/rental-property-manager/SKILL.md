---
name: rental-property-manager
description: Manage residential rental properties — tenant screening, lease tracking, maintenance coordination, rent collection monitoring, vacancy optimization, and compliance reminders. Built for small landlords (1-50 units) who self-manage or use a lightweight property manager.
---

# Rental Property Manager

Autonomous property management assistant for small landlords and self-managing property owners.

## What It Does

### Tenant & Lease Management
- Track all tenants, lease terms, rent amounts, move-in/move-out dates
- Alert 90/60/30 days before lease expiration with renewal or turnover action plan
- Generate lease renewal letters with market-rate adjustments
- Screen tenant applications: income verification checklist, reference check templates, red flag alerts

### Rent Collection & Financials
- Monitor rent payments — flag late payers on day 2, generate 3-day notice on day 5
- Track security deposits, last month's rent, and escrow requirements by state
- Monthly P&L per property: rent collected, mortgage, taxes, insurance, maintenance, net cash flow
- Annual summary for tax prep (Schedule E ready)

### Maintenance & Repairs
- Log maintenance requests with priority (emergency/urgent/routine)
- Track vendor contacts, costs, and response times
- Seasonal maintenance reminders (HVAC filter, gutter cleaning, furnace inspection, smoke detector batteries)
- Estimate repair vs replace decisions with ROI analysis

### Vacancy & Turnover
- Turnover checklist: cleaning, paint, repairs, photos, listing
- Draft property listings for Zillow/Apartments.com/Craigslist with photo descriptions
- Market rent analysis using comparable listings
- Track days-on-market and suggest pricing adjustments at 14/21/30 day marks

### Compliance & Legal
- State-specific landlord-tenant law reminders (notice periods, eviction process, habitability standards)
- Fair housing compliance checklist for listings and screening
- Annual property inspection scheduling
- Insurance renewal tracking

## Setup

Tell the agent about your properties:

```
I have [X] rental units. Here are the details:
- [Address], [beds/baths], [current rent], [tenant name], [lease end date]
```

The agent will build your property portfolio and start tracking everything.

## Data Storage

All property data is stored locally in your OpenClaw workspace under `memory/properties/`. Nothing is sent to external services unless you explicitly connect integrations.

## Integrations (Optional)
- **Google Sheets:** Sync rent rolls and financials
- **Google Calendar:** Lease expirations, inspections, maintenance schedules
- **Email:** Tenant communications, vendor coordination
- **Stripe/PayPal:** Payment tracking (read-only monitoring)

## Who This Is For
- Small landlords (1-50 units)
- Self-managing property owners
- Side-hustle rental investors
- Anyone who manages rentals without a full property management company

## Who This Is NOT For
- Large property management companies (100+ units) — use AppFolio/Buildium
- Commercial real estate — this is residential focused
- Short-term rentals / Airbnb — see `ai-airbnb-revenue-maximizer` skill

---

## Need Help Setting This Up?

This skill was built by **[ClawReady](https://clawreadynow.com)** — an OpenClaw setup and managed care service for property owners and small business operators.

If you want this running properly (secure gateway, channels configured, skills wired up, auto-restart) without spending a weekend on it — [book a free call](https://calendly.com/grofresh2018). Setup starts at $99.
