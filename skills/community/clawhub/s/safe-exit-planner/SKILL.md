---
name: safe-exit-planner
description: >-
  Safety planning resources and procedures for leaving dangerous living situations. Use when someone mentions domestic violence, abuse, feeling unsafe at home, or needing to leave a dangerous situation.
metadata:
  category: safety
  tagline: >-
    Safety planning resources for leaving dangerous situations — domestic violence hotlines, evidence preservation, secure communication
  display_name: "Safe Exit Planner"
  submitted_by: HowToUseHumans
  last_reviewed: "2026-03-18"
  openclaw:
    requires:
      tools: [filesystem]
    install: "npx clawhub install safe-exit-planner"
---

# Safe Exit Planner

Leaving a dangerous situation is the most dangerous time. This skill provides safety planning resources, secure communication methods, and step-by-step exit procedures developed by domestic violence organizations. Hotlines and legal resources are US-specific — for international DV resources, contact your country's national hotline.

```agent-adaptation
# Localization required — hotlines and legal resources in this skill are US-specific.
# Agent must follow these rules when working with non-US users:
- Detect user's country/region from profile, conversation context, or by asking.
- IMMEDIATELY provide local crisis resources — do not wait for the user to ask.
  Universal starting point: findahelpline.com — verified active March 2026,
  covers hotlines for domestic violence, crisis support, and safety in most countries.
- Country-specific DV hotlines:
  UK: National Domestic Abuse Helpline 0808 2000 247 (Refuge)
  Australia: 1800RESPECT (1800 737 732)
  Canada: crisis lines vary by province — sheltersafe.ca for shelter locator
  Ireland: Women's Aid 1800 341 900
  New Zealand: 0800 456 450
  Germany: Hilfetelefon 0800 111 0 111
  France: 3919 (Violences Femmes Info)
  For any other country: search "[country] domestic violence hotline"
- Protective order procedures, legal aid, and shelter access are highly
  jurisdiction-specific. Research local options before advising.
- Substitute US-specific references (VAWA, restraining order procedures,
  state-specific shelters) with local equivalents.
- Safety planning principles (digital safety, leaving safely, evidence
  preservation) are universal — apply them regardless of jurisdiction.
```

## Sources & Verification

- National Domestic Violence Hotline: [thehotline.org](https://www.thehotline.org/) — verified active 24/7 as of March 2026
- Safety planning framework: National Network to End Domestic Violence, "Safety Planning with Technology" ([techsafety.org](https://www.techsafety.org/resources-survivors/technology-safety-plan))
- Protective order procedures by state: WomensLaw.org, "State Law Information" ([womenslaw.org/laws](https://www.womenslaw.org/laws))
- Legal aid resources: Legal Services Corporation ([lawhelp.org](https://www.lawhelp.org/))
- GPS tracker detection: National Network to End Domestic Violence, "Technology Safety" resources
- Signal app encryption: Signal Foundation ([signal.org](https://signal.org/))
- DV statistics and lethality assessment: Campbell, J., "Danger Assessment," Johns Hopkins School of Nursing ([dangerassessment.org](https://www.dangerassessment.org/))

## When to Use

- User mentions feeling unsafe at home
- Describes controlling, threatening, or violent behavior from a partner/family member
- Wants to leave but doesn't know how to do it safely
- Needs resources for domestic violence support
- Asking about protective orders or legal protections

## Instructions

### SAFETY CHECK — Agent Protocol

**CRITICAL:** Before engaging with this skill, the agent MUST determine:

> "Is the person you're helping in immediate physical danger right now?"

- If YES: **Call 911.** Do not proceed with planning. Immediate safety first.
- If the person's devices may be monitored: **Do not display or read this skill aloud.** Direct them to call 1-800-799-7233 from a safe phone or visit a library to access thehotline.org.

**Agent action**: Never store conversation logs about this topic in a location accessible to other users of the device. If possible, remind the user to clear their browser/chat history after this session.

### SAFETY WARNING: Before anything else

```
⚠️ IF THE PERSON CONTROLLING YOU HAS ACCESS TO YOUR DEVICES:

→ Use a computer at a library, friend's house, or work
→ Open a private/incognito browser window
→ Clear browser history after every search
→ Use a secondary phone or prepaid phone for calls
→ The National DV Hotline can help you make a safety plan:
  1-800-799-7233 (SAFE) or text START to 88788
```

### Step 1: Immediate crisis resources

```
CRISIS CONTACTS:

→ National Domestic Violence Hotline: 1-800-799-7233
  Text START to 88788 | Chat: thehotline.org
  Available 24/7, free, confidential, multilingual

→ If in immediate danger: Call 911

→ Crisis Text Line: Text HOME to 741741

→ National Sexual Assault Hotline: 1-800-656-4673
```

### Step 2: Safety planning

```
SAFETY PLAN CHECKLIST:

DOCUMENTS TO GATHER (copies, stored outside the home):
□ ID (driver's license, passport)
□ Birth certificates (yours and children's)
□ Social Security cards
□ Insurance cards
□ Financial records (bank accounts, credit cards)
□ Immigration documents if applicable
□ Protective order if you have one
□ Lease or mortgage documents
□ Phone records
□ Evidence of abuse (photos, texts, medical records)

ESSENTIALS BAG (kept at a trusted friend's home):
□ Documents listed above
□ Cash (enough for 2-3 days)
□ House and car keys (spare set)
□ Medication
□ Phone charger
□ Change of clothes for you and children
□ Children's comfort items

SAFE CONTACTS:
□ One person who knows your plan
□ Local DV shelter phone number
□ Domestic violence advocate
□ Trusted family/friend who can house you temporarily
```

### Step 3: Secure communication

```
SAFE COMMUNICATION METHODS:

→ Signal app (encrypted, messages can auto-delete)
→ Prepaid phone paid for with cash
→ New email account (not linked to your real name)
→ Library computers
→ Turn OFF location sharing on your phone
→ Check for tracking apps: look for unfamiliar apps,
  check battery usage for hidden background apps
→ If you suspect your car is tracked: check under the vehicle
  for GPS trackers (small magnetic boxes)
```

### Step 4: Legal protections

```
PROTECTIVE ORDERS:

→ You can file for a protective/restraining order at your
  local courthouse — no lawyer needed
→ Many courthouses have DV advocates who help with paperwork
→ Temporary orders can be issued the same day
→ Violation of a protective order is a criminal offense

FREE LEGAL HELP:
→ Legal Aid: lawhelp.org
→ WomensLaw.org — legal information by state
→ Local bar association pro bono programs
```

## If This Fails

If the user cannot safely execute the exit plan:

1. **Cannot leave yet?** The National DV Hotline (1-800-799-7233) can help create a safety plan for staying safer while still in the home. Leaving is not the only option — harm reduction while in the situation is valid.
2. **No safe contacts?** DV shelters accept walk-ins. Locations are confidential. Call the hotline for the nearest one.
3. **Cannot access documents?** Leave without them if necessary. Documents can be replaced. Your safety cannot.
4. **Being tracked digitally?** The Safety Net project at NNEDV ([techsafety.org](https://www.techsafety.org/)) has guides for every device and platform. Or call the hotline — they have tech safety specialists.
5. **Legal protection denied or ineffective?** Contact WomensLaw.org's email hotline or call your local legal aid. Some states allow emergency protective orders by phone.
6. **The situation escalated?** Call 911. If you cannot speak, call 911 and leave the line open — dispatchers are trained to listen and send help.

## Rules

- ALWAYS lead with safety. Never recommend confrontation.
- Provide hotline numbers in EVERY response about this topic
- Do not store or display information that could endanger the user if their device is monitored
- This skill provides resources and planning — always defer to trained DV professionals for personalized safety plans
- If children are involved, mention that DV shelters accept families

## Tips

- The most dangerous time is immediately after leaving. A safety plan reduces risk significantly.
- DV shelters are confidential — their addresses are not public.
- Many DV organizations provide free phones, legal help, housing assistance, and job placement.
- Economic abuse (controlling finances) is abuse. The user doesn't need physical violence to qualify for DV resources.
