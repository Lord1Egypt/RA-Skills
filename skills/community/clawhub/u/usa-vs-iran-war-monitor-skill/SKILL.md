---
name: "USA vs Iran War Monitor Skill"
version: 0.1.0
slug: "usa-vs-iran-war-monitor-skill"
description: "Monitor public USA-Iran war-risk news with verified sources, escalation indicators, civilian-safety context, and no-rumor safeguards."
category: "News & Safety"
tags:
  - "openclaw"
  - "usa-iran"
  - "war-monitor"
  - "osint"
  - "safety"
generated: "2026-06-03"
---

# USA vs Iran War Monitor Skill

## Purpose

Use this skill to track public information about USA-Iran conflict risk, military escalation, diplomacy, sanctions, cyber activity, shipping disruption, energy-market impact, and civilian-safety updates.

The skill is for situational awareness and defensive planning only. It does not predict war with certainty, encourage violence, target people, or provide operational military advice.

## When to use

Use this skill when the user asks for:

- USA vs Iran war updates.
- Gulf / Kuwait / GCC safety implications from USA-Iran tensions.
- Red Sea, Strait of Hormuz, Iraq, Syria, Yemen, Israel, or Gulf escalation context tied to USA-Iran risk.
- Cyber threat updates connected to Iran, US entities, critical infrastructure, hacktivists, or retaliation claims.
- A short Telegram/X-ready alert draft about public developments.
- A daily/weekly conflict-risk brief.
- A rumor check before sharing war news.

## Core safety rules

1. Use only public, legal sources.
2. Do not reveal private locations, troop movements, live tactical details, or instructions that could help violence.
3. Do not amplify unverified attack claims; label them as unconfirmed until verified by reliable sources.
4. Separate facts, assessments, and rumors clearly.
5. Avoid inflammatory language, hate, or collective blame against Americans, Iranians, Arabs, Jews, Muslims, or any civilian group.
6. Focus on civilian safety, business continuity, cyber defense, and source verification.
7. Do not give real trading or investment advice based on war news. If markets are mentioned, frame it as risk context only.
8. Do not suggest cyber retaliation, hacking, doxxing, disruption, or unauthorized testing.

## Recommended source tiers

### Tier 1: official / primary

- White House, US Department of Defense, US State Department, CENTCOM.
- Iranian government or military statements, clearly labeled as official claims.
- Kuwait, GCC, UN, IAEA, IMO, and embassy advisories.
- Official airline, maritime, energy, and civil-defense notices.

### Tier 2: reliable reporting / specialist context

- Reuters, AP, AFP, BBC, Al Jazeera, Financial Times, The Wall Street Journal, New York Times, Washington Post.
- Defense and security specialists with clear sourcing such as Janes, IISS, CSIS, RUSI, ACLED, ISW, Recorded Future, Mandiant, Microsoft Threat Intelligence, CISA.

### Tier 3: social media / OSINT leads

- Verified journalist posts, satellite imagery analysts, maritime trackers, flight trackers, local eyewitness media.
- Treat as leads, not confirmed facts, until cross-checked.

## Verification checklist

Before producing a confident alert, check:

1. What exactly happened?
2. Where did it happen?
3. When did it happen? Include timezone.
4. Who is making the claim?
5. Is there independent confirmation from at least two credible sources?
6. Is the source primary, reliable media, or social-media-only?
7. Could old footage, mistranslation, propaganda, or satire be involved?
8. Is there a direct Kuwait/GCC/cyber/business safety impact?
9. What is still unknown?
10. What confidence percentage is justified?

## Escalation indicators

Track these indicators, but do not overstate them:

- Direct US-Iran military strike or confirmed casualties.
- Attack on US bases, ships, embassies, or personnel linked to Iran-backed actors.
- Strike on Iranian territory or senior Iranian personnel.
- Closure/threats around Strait of Hormuz or major shipping lanes.
- Embassy evacuation, travel advisory escalation, airline route suspension.
- Major cyber activity against energy, finance, telecom, government, or critical infrastructure.
- UN Security Council emergency meeting, IAEA escalation, sanctions escalation.
- Oil/gas disruption, tanker incidents, insurance/shipping warnings.
- Regional spillover involving Iraq, Syria, Yemen, Lebanon, Israel, Kuwait, Saudi Arabia, UAE, Bahrain, or Qatar.

## Risk labels

Use a simple label:

- GREEN: routine tension; no confirmed escalation.
- YELLOW: credible warning, limited incident, or unverified attack claim.
- ORANGE: confirmed incident with regional/cyber/business impact.
- RED: direct military exchange, confirmed major casualties, or official emergency advisory.

## Output format: short alert

```text
🚨 USA-Iran Watch — [DATE/TIME + TZ]
Risk: [GREEN/YELLOW/ORANGE/RED]
Confidence: [xx%]

What happened:
- [1-2 factual bullets]

Why it matters:
- [Kuwait/GCC/cyber/business impact]

Action now:
- [defensive/civilian-safe step]

Source:
[link]
```

## Output format: daily brief

```text
USA-Iran War-Risk Brief — [DATE]
Overall risk: [GREEN/YELLOW/ORANGE/RED]
Confidence: [xx%]

1. Military/security
- [fact + source]

2. Diplomacy/sanctions
- [fact + source]

3. Cyber risk
- [defensive note + source]

4. Kuwait/GCC impact
- [travel, business, energy, shipping, cyber, public safety]

5. Watch next
- [2-4 indicators]

Bottom line:
[one short assessment]
```

## Cyber-defense add-on

If USA-Iran tensions rise, recommend defensive steps only:

- Review MFA coverage for admin, email, VPN, cloud, and social accounts.
- Patch internet-facing systems and VPN appliances.
- Monitor phishing themes tied to war/news/aid/embassy/travel alerts.
- Increase logging for authentication, endpoint, DNS, and cloud access.
- Review incident-response contacts and backup restore readiness.
- Warn staff not to open sensational war videos, attachments, or urgent donation links.

Never recommend offensive cyber action or retaliation.

## Rumor-control wording

Use this when evidence is weak:

```text
I’m treating this as unconfirmed for now. I found the claim, but not enough reliable independent confirmation yet. Best action: wait for official or major-wire confirmation before sharing.
```

## Kuwait/GCC public-safety wording

```text
For Kuwait/GCC readers: this is a monitoring update, not a panic alert. Follow official advisories, avoid spreading unverified clips, keep travel plans flexible, and make sure business cyber defenses are ready for phishing or disruption attempts.
```

## Example prompts

- Check today’s USA-Iran war-risk news and give me a short confidence-rated brief.
- Is this USA-Iran attack claim real or just a rumor? Verify sources and tell me if I should share it.
- Prepare an Arabic X/Twitter alert for Q8 Cyber Partner about USA-Iran cyber risk, defensive only.
- Summarize Kuwait/GCC impact if USA-Iran tensions escalate this week.

## Support / Donate

If this skill helps your workflow, you can support maintenance here:

- PayPal: https://www.paypal.com/donate/?hosted_button_id=MJHCRZA9Z4X7Y
