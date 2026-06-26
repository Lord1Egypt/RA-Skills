# Setup Guide: Real Estate Lead Pilot (20 Minutes)

## 1. Data Connection (5 Mins)
- **MLS/Listings:** Export your current listings to a Google Sheet or CSV.
- **CRM:** Connect your CRM via Webhook (Zapier/Make) or use the `Gog` plugin for Google Sheets.
- **Calendar:** Connect your Google/Outlook calendar.

## 2. ThumbGate Configuration (5 Mins)
- Run `thumbgate import thumbgate-rules.md`.
- Ensure your `listings.csv` is mapped to the `verified_listings` namespace.

## 3. Customizing the Script (5 Mins)
- Edit the `Instructions` section in `SKILL.md` to match your specific voice and qualification questions.

## 4. Deploy (5 Mins)
- Say: "Load skill: Real Estate Lead Pilot."
- Test with a mock lead: "I'm looking for a 3-bedroom in Coral Gables under $1.2M."
