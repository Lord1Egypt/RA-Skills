---
name: uplo-cybersecurity
description: AI-powered cybersecurity knowledge management. Search threat intelligence, vulnerability assessments, incident response plans, and compliance documentation with structured extraction.
---

# UPLO Cybersecurity — Threat-Informed Defense Intelligence

Security teams drown in telemetry but starve for context. Your SIEM fires alerts, your vuln scanner produces CVE lists, your pen testers write reports, and your compliance team maintains control matrices — all in separate silos. UPLO Cybersecurity creates a searchable institutional memory across threat intelligence, incident post-mortems, vulnerability management, policy documentation, and compliance evidence so your SOC analysts, IR team, and CISO can make faster, better-informed decisions.

## Session Start

Your clearance level matters more in cybersecurity than almost any other domain. Load your identity first — it determines whether you can access active incident details, threat intelligence marked TLP:RED, or audit findings under remediation.

```
get_identity_context
```

Check operational directives. In security, these include active threat advisories, emergency patching mandates, and incident response activation orders:

```
get_directives
```

## When to Use

- Triaging a new alert and need to check if this IOC (indicator of compromise) matches a previously investigated incident
- Preparing a board-level cybersecurity risk briefing and need to synthesize vulnerability trends, incident metrics, and control maturity across the program
- An auditor asks for evidence that a specific NIST CSF control is implemented — you need to find the policy, the technical implementation record, and the last test result
- Investigating whether a newly disclosed CVE affects your environment by cross-referencing the vulnerability with your asset inventory documentation
- Writing an incident post-mortem and need to reference the runbook that was followed, the timeline decisions made, and similar past incidents
- Evaluating a vendor's SOC 2 report against your third-party risk management criteria
- Checking whether the firewall change request aligns with the network segmentation architecture documented in the last assessment

## Example Workflows

### Incident Response Investigation

The SOC escalates a potential data exfiltration alert involving an internal server communicating with a known C2 domain.

```
search_with_context query="command and control C2 communication indicators previous incidents exfiltration"
```

Pull the incident response runbook for data exfiltration scenarios:

```
search_knowledge query="incident response playbook data exfiltration containment steps"
```

Check if the affected server is documented in the asset inventory with its classification:

```
search_knowledge query="server srv-db-prod-07 asset classification data sensitivity network segment"
```

After containment, log the investigation:

```
log_conversation summary="Investigated potential data exfil alert on srv-db-prod-07; C2 domain matched TI report from October; followed exfil IR playbook; server classified as hosting PII" topics='["incident-response","data-exfiltration","C2","PII"]' tools_used='["search_with_context","search_knowledge"]'
```

### Compliance Evidence Assembly

The organization is undergoing a SOC 2 Type II audit and needs to assemble evidence for the CC6 (Logical and Physical Access Controls) criteria.

```
search_knowledge query="access control policy role-based access management RBAC documentation"
```

```
search_with_context query="access review evidence quarterly user access certification results exceptions"
```

```
search_knowledge query="MFA multi-factor authentication implementation evidence configuration"
```

Export the organizational context to show the auditor the team structure and system ownership:

```
export_org_context
```

## Key Tools for Cybersecurity

**search_with_context** — Security investigations are inherently graph problems. A single alert can connect to asset inventory records, previous incident reports, threat intelligence, and network architecture documentation. Example: `search_with_context query="lateral movement techniques detected incidents Active Directory compromise"`

**search_knowledge** — Fast retrieval for specific security artifacts: a named runbook, a particular CVE assessment, a policy document. When you know what you need, this is faster than graph traversal. Example: `search_knowledge query="CVE-2024-3094 xz backdoor impact assessment"`

**get_directives** — Security directives are time-critical. Emergency patch mandates, threat hunting directives after a new APT disclosure, and incident response activation orders all surface here. Checking directives during an active incident could reveal that the CISO has already issued containment instructions.

**flag_outdated** — Stale security documentation is dangerous. A firewall rule matrix from before the last network redesign, an incident response plan listing a phone tree with departed employees, or a risk register with last year's threat landscape — all need flagging.

**report_knowledge_gap** — When you cannot find documentation for a critical control (e.g., no evidence of database encryption at rest), the gap itself is a finding. Reporting it creates a trackable item.

**log_conversation** — In cybersecurity, logging is not optional. Every investigation session, every threat assessment, every compliance evidence review should be logged. These logs are themselves audit evidence.

## Tips

- Use CVE identifiers, MITRE ATT&CK technique IDs (e.g., T1059.001), and TLP designations as search terms. The extraction engine indexes these as structured fields.
- Classification tiers in cybersecurity map roughly to TLP: `public` = TLP:CLEAR, `internal` = TLP:GREEN, `confidential` = TLP:AMBER, `restricted` = TLP:RED. If a threat intel query returns no results, verify your clearance supports the expected TLP level.
- Incident post-mortems are the single most valuable document type in a security knowledge base. When writing them, include structured fields (MITRE techniques, affected assets, detection source, time-to-contain) that the extraction engine can index.
- Network diagrams and architecture documents are often extracted as text descriptions of topology. Query for specific network segments or system names rather than expecting visual diagram retrieval.
