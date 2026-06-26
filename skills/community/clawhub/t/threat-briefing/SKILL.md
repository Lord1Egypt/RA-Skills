---
name: threat-briefing
description: Generate a daily or weekly cybersecurity threat briefing from open sources. Covers new vulnerabilities, active exploits, ransomware campaigns, APT activity, and industry-relevant threats.
triggers:
  - threat briefing
  - cyber news
  - security briefing
  - daily threats
  - weekly intel
---

# Threat Briefing

Generate a concise, actionable cybersecurity threat briefing.

## Briefing Structure

### Header
```
# Cybersecurity Threat Briefing
**Date:** [today's date]
**Period:** Last 24-48 hours | Last 7 days
**Analyst:** [agent name]
**TLP:** WHITE
```

### Priority Alerts (if any)
Active exploits or critical vulnerabilities requiring immediate action.
Include: CVE ID, affected systems, exploitation status, patch availability.

### Top Stories (5-10 items)
For each story:
```
### [N]. [Headline]
**Category:** Vulnerability | Ransomware | APT | Supply Chain | Policy | Tool Release
**Relevance:** Higher-Ed | SMB | Enterprise | All
**Summary:** [2-3 sentences]
**Action Required:** [Yes/No] - [what to do if yes]
**Source:** [URL]
```

### Vulnerability Watch
New CVEs with CVSS >= 7.0 relevant to common stacks:
- Linux/Ubuntu
- Windows Server
- Network equipment (Cisco, Fortinet, Palo Alto)
- Web frameworks (Node.js, Python, PHP)
- Cloud services (AWS, Azure, GCP)

### Threat Actor Activity
Any notable APT or criminal group activity in the reporting period.
Map to MITRE ATT&CK where possible.

### Recommendations
Prioritized action items for a small-to-mid security team:
1. [Highest priority action]
2. [Second priority]
3. [Third priority]

## Tailoring
- For higher-ed: emphasize student data (FERPA), research IP, BYOD risks
- For SMB: emphasize ransomware, business email compromise, supply chain
- For SOC operators: emphasize detection rules, IOCs, hunting queries

## Sources to Reference
Prefer: CISA KEV, NVD, BleepingComputer, The Record, Krebs on Security, Dark Reading, SecurityWeek, Mandiant/Google TAG, Microsoft MSRC
