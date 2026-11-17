# M5 - Red Team & Adversary Emulation

**Purpose:** Find methodologies, threat-actor profiles, ATT&CK techniques, emulation plans,
tooling documentation, OPSEC guidance, and detection mappings for authorized red-team and
purple-team work.

**Triggers:** red team, redteam, adversary emulation, C2, command and control, ATT&CK, OPSEC,
initial access, lateral movement, persistence, privilege escalation, credential access,
exfiltration, purple team, threat actor, TTP, emulation plan, TIBER-EU, CBEST, AI red teaming,
LLM red team, DFIR, detection engineering.

**Process contract:** Always run the Universal Search Loop (Section 1) and the Process Compliance
Gate (Section 0.5). This module supplies sources and queries only.

---

## Primary sources

### Frameworks and knowledge bases
| Source | Use |
|---|---|
| **MITRE ATT&CK** (`attack.mitre.org`) | Techniques, groups, software, mitigations, detections |
| **MITRE D3FEND** | Defensive countermeasures |
| **CAPEC** | Attack patterns |
| **Atomic Red Team** (`github.com/redcanaryco/atomic-red-team`) | Test procedures per technique |
| **Red Team Notes** (`ired.team`) | Practitioner techniques |
| **Internal All The Things** | AD and internal pentest |
| **HackTricks** | Technique references |
| **PayloadsAllTheThings** | Payload references |
| **Sigma** (`github.com/SigmaHQ/sigma`) | Detection rules |
| **TIBER-EU / CBEST** | Threat-led penetration testing frameworks |
| **The Hacker Recipes** (`thehacker.recipes`) | AD, Exchange, and internal pentest guides |

### Threat actor and campaign research
- MITRE ATT&CK groups and software pages.
- Vendor research: Mandiant, CrowdStrike, Unit 42, Microsoft MSTIC, Google TAG, Talos, Recorded
  Future, SentinelLabs, Volexity, ESET, Kaspersky GReAT.
- Practitioner/team blogs: SpecterOps (`specterops.io/blog`), TrustedSec (`trustedsec.com/blog`),
  Bishop Fox (`bishopfox.com/blog`), harmj0y (`blog.harmj0y.net`), ADSecurity (`adsecurity.org`),
  0xdf (`0xdf.gitlab.io`), Nuclear'Atk (`lcx.cc`). Check author, date, and lab preconditions.
- CISA advisories and AA/IR publications.
- Threat-intel platforms: **OpenCTI** (`github.com/opencti-platform/opencti`, STIX2, MISP
  connector) and **MISP** for correlated reports and observables.
- CTI source index: `github.com/hslatman/awesome-threat-intelligence`.
- **The DFIR Report** (`thedfirreport.com`) - real-world intrusion case studies with TTPs, IOCs,
  and detection opportunities.
- Ransomware tracking: **ransomware.live** (`ransomware.live`) and **RansomLook**
  (`ransomlook.io`) - group/victim/leak-site monitoring with APIs; **ransomwatch**
  (`github.com/joshhighet/ransomwatch`) - open-source leak-site monitor.
- Conference talks (DEF CON, Black Hat, BSides) and lab writeups.

### Tooling documentation
- C2 frameworks: Cobalt Strike docs, Sliver, Mythic, Havoc, Brute Ratel (documentation and
  licensing only).
- AI/LLM red teaming: `github.com/0xMrNiko/Awesome-Red-Teaming` (AI red teaming, fuzzing,
  methodology).
- Initial access: phishing simulation platforms, payload delivery docs (authorized only).
- Discovery/credential access/lateral movement: official docs for the tools you are licensed to use.
- OPSEC: infrastructure separation, redirectors, malleable profiles, logging hygiene.
- Detection content: Sigma, `elastic/detection-rules`, Splunk Security Content
  (`research.splunk.com`), Sentinel KQL, Chronicle, Suricata.
- **Detections Digest** (`detections-digest.rulecheck.io`) - weekly digest of rule changes across
  50+ public detection repositories.
- **SOC Prime Threat Detection Marketplace** (`socprime.com`) and **Uncoder.IO** (`uncoder.io`) -
  commercial rule aggregation and cross-SIEM translation; verify licensing.

---

## Query recipes

```text
# Technique and procedure
site:attack.mitre.org "T1059" "Command and Scripting Interpreter"
site:attack.mitre.org "groups" "APT29"
site:github.com/redcanaryco/atomic-red-team "T1059"
site:ired.team "lateral movement"
site:book.hacktricks.xyz "active directory" "kerberos"
site:thehacker.recipes "kerberos"

# Emulation plans
"adversary emulation plan" "APT29"
"emulation plan" "FIN7"
"red team" "engagement" "rules of engagement"
"threat-led penetration testing" TIBER-EU
"CBEST" "threat intelligence" pentest

# OPSEC and infrastructure
"red team" OPSEC checklist
"C2" "redirector" "OPSEC"
"malleable profile" "Cobalt Strike" detection
"payload" "evasion" "EDR" (authorized research)

# Detection and purple team
site:github.com/SigmaHQ/sigma "T1059"
site:github.com/elastic/detection-rules "T1059"
site:research.splunk.com "T1059"
site:detections-digest.rulecheck.io "Sigma"
site:socprime.com "Sigma" "T1059"
"purple team" exercise template
"detection engineering" "ATT&CK"
"atomic red team" "detection" "test"

# Threat actor research
"APT29" TTPs
"FIN7" "initial access"
"ransomware" "TTP" "MITRE"
site:thedfirreport.com "ransomware"
site:ransomware.live "group"
site:ransomlook.io "group"

# AI and LLM red teaming
"AI red teaming" "LLM" methodology
site:github.com/0xMrNiko/Awesome-Red-Teaming
site:genai.owasp.org "Agentic" "red team"
```

---

## Workflow

1. **Define the objective and threat model.** Which adversary, sector, and technique scope?
2. **Map to ATT&CK.** Select techniques and sub-techniques; record IDs.
3. **Find an emulation plan.** Prefer vendor/CISA/community plans with procedures and cleanup.
4. **Check legal and licensing.** RoE, authorization, tool licenses, data handling.
5. **Design infrastructure and OPSEC.** Separate identities, redirectors, logging, and scope.
6. **Define detection/telemetry first.** What should the blue team see? Which logs?
7. **Execute only in the authorized environment.** Log every action; have a rollback plan.
8. **Document TTPs, detections, and gaps.** Feed results into detection engineering.
9. **Debrief and purge.** Remove artifacts, revoke access, deliver the report (M12).

---

## What to extract

| Field | Example |
|---|---|
| Technique | T1059.001 PowerShell |
| Procedure | encoded command via scheduled task |
| Prerequisites | domain user, execution policy bypass |
| Telemetry | 4688, 4104, Sysmon 1/3/11 |
| Detection | Sigma rule + SIEM query |
| OPSEC | avoid command-line logging, use signed binaries? |
| Cleanup | remove task, delete payload |
| Confidence | B (ATT&CK + vendor research) |

---

## Pitfalls

- **Legal risk.** Red-team activity without written authorization is a crime.
- **Destructive techniques.** Ransomware simulation, wipers, and data destruction require extreme
  care and explicit approval.
- **Attribution leakage.** Reusing personal infrastructure or accounts exposes the operator.
- **Tool licensing.** Some C2 frameworks require licenses; do not use pirated builds.
- **Detection-blind exercises.** Without telemetry, the exercise produces little defensive value.
- **Scope creep.** Pivoting into third-party cloud services or acquired companies is common.
- **Hype.** Vendor marketing may overstate technique efficacy.

---

## Ethics

- Written authorization, defined scope, and rules of engagement are mandatory.
- Prefer non-destructive procedures; simulate impact rather than cause it.
- Protect collected credentials and data; minimize and delete.
- Coordinate with the blue team and respect safety controls.
- Do not publish operational details that enable real-world harm.

---

## Output contract

```
module:        M5 Red Team
objective:     emulation/detection plan for <threat actor/technique>
authorization: written RoE / lab only
sources_used:  ATT&CK, Atomic Red Team, vendor research, Sigma, mapped to the claim it supports
sources_read:  URLs opened but excluded, with reason (off-scope, stale, duplicate, low confidence, inaccessible, discovery only)
findings:      technique map, procedures, telemetry, detections, gaps
pivots:        M10 research, M9 labs, M12 report
caveats:       licensing, destructive steps excluded, scope limits
```
