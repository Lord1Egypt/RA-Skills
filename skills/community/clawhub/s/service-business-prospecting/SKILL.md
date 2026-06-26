---
name: service-business-prospecting
description: "Daily lead generation for local US service businesses (HVAC, Plumbing, Dental, Med Spa, etc.). Generates qualified leads with verified contact info, ready for Ventured Brands AI automation sales outreach."
---

# Service Business Prospecting

## Overview

This skill runs a daily 6am lead-generation job for Ventured Brands, who sells AI automation (missed-call text-back, AI receptionist, review automation, full-stack bundles) to local US service businesses.

## Objective

Produce a fresh batch of ~25 qualified, contactable leads in one US metro for one of the four target industries, saved as a daily-dated CSV that drops cleanly into the AI_Automation_Lead_Tracker.xlsx.

## Target Industries (4)

| Industry | Slug |
|----------|------|
| HVAC / Plumbing / Electrical | hvac-plumbing-electrical |
| Med Spa / Dental / Chiro | med-spa-dental-chiro |
| Auto Detail / Repair | auto-detail-repair |
| Cleaning / Landscaping / Pest Control | cleaning-landscaping-pest |

## Pitch Angles (4)

| Pitch | Description |
|-------|-------------|
| Missed-Call Text-Back | Automated text back when they miss a call |
| AI Receptionist | Virtual front desk AI |
| Review Automation | Automated review requests |
| Full-Stack Bundle | All AI products combined |

## ICP (Ideal Customer Profile)

**Target:**
- Local US service businesses (not chains/franchises)
- 2-10 employees
- Established (2+ years in business)
- Has Google/Yelp presence
- Not already using AI competitors

**NOT Target:**
- Chains (Servicemaster, etc.)
- Solo operators
- New businesses (<1 year)
- Enterprise/commercial only

## Day Rotation

| Day | Industry-City |
|-----|--------------|
| Monday | HVAC/Plumbing/Electrical - Phoenix, AZ |
| Tuesday | Med Spa/Dental/Chiro - Scottsdale, AZ |
| Wednesday | Auto Detail/Repair - Dallas, TX |
| Thursday | Cleaning/Landscaping/Pest - Austin, TX |
| Friday | HVAC/Plumbing/Electrical - Tampa, FL |
| Saturday | Med Spa/Dental/Chiro - Miami, FL |
| Sunday | Cleaning/Landscaping/Pest - Atlanta, GA |

## Scoring Rubric

| TIER | Criteria | Points |
|-----|----------|--------|
| **A** | Phone + Email + Website + Owner Name | 4/4 |
| **B** | Phone + Website (no email) | 3/4 |
| **C** | Phone only OR partial info | 1-2/4 |
| **D** | No phone / Uncontactable | 0/4 |

## Workflow (9 Steps)

### Step 1: Check Rotation
- Read today's day-of-week
- Get industry-city combo from rotation table
- Check last 7 days of output to avoid repeats

### Step 2: WebSearch - Business Discovery
Search queries per industry:
- "[Industry type] [City] AZ phone number address"
- "[Industry type] [City] AZ owner name email"
- "[Industry type] [City] AZ yelp reviews"

Get minimum 10 real businesses. NEVER fabricate.

### Step 3: ICP Filtering
Remove:
- Chains/franchises (name includes "Mister", "Merry", "ServiceMaster", "College")
- New businesses (<2 years)
- Commercial-only

### Step 4: Contact Enrichment
For each lead:
- Extract phone number (primary)
- Find email from website/Facebook
- Get owner/contact name
- Verify address

### Step 5: Scoring
Assign Tier A/B/C/D based on contact completeness.

### Step 6: Pitch Assignment
Match to best pitch angle:
- Has receptionist/front desk → AI Receptionist
- Has reviews → Review Automation
- Small biz → Missed-Call Text-Back
- Enterprise-ready → Full-Stack Bundle

### Step 7: Build Output
Create CSV with columns:
```
Company Name, Owner/Contact, Phone, Email, Address, City, State, Zip, Industry, Pitch Angle, Tier, Status, Last Contacted, Notes, Source
```

### Step 8: Quality Check
- Verify 10+ leads have phones
- Report email yield
- Flag any data gaps

### Step 9: Save Output
Save to:
```
<outputs-folder>/daily-leads/<YYYY-MM-DD>-<industry-slug>-<city-slug>.csv
```

Also save notes.md with summary.

## Data Quality Rules

- NEVER fabricate businesses, owner names, phone numbers, or emails
- If WebSearch returns <10 real leads, report the shortfall
- All leads must be real, verifiable businesses
- Email must be from website/Facebook (not guessed)

## Tracker Vocabulary (Reference)

**Industry values:**
- "HVAC"
- "Plumbing"  
- "Electrical"
- "Med Spa"
- "Dental"
- "Chiro"
- "Auto Detail"
- "Auto Repair"
- "Cleaning"
- "Landscaping"
- "Pest Control"

**Pitch Angle values:**
- "Missed-Call Text-Back"
- "AI Receptionist"
- "Review Automation"
- "Full-Stack Bundle"

**Status values:**
- "Not Contacted"
- "Attempted"
- "Connected"
- "Qualified"
- "Proposal Sent"
- "Closed Won"
- "Closed Lost"

## Output Files

1. **CSV** - `2026-04-28-med-spa-dental-chiro-scottsdale.csv`
2. **Notes** - `notes.md` with:
   - Industry+City used
   - Sources checked
   - Count by tier
   - Email yield
   - Data quality caveats