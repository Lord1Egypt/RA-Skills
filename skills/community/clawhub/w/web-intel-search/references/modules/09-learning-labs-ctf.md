# M9 - Learning Labs, CTF & Training

**Purpose:** Find the right practice environment, challenge, course, or certification for a
specific skill gap, and convert practice into reusable methodology.

**Triggers:** lab, CTF, training, practice, learn, HTB, Hack The Box, TryHackMe, PortSwigger
Academy, VulnHub, PentesterLab, OverTheWire, Root-Me, picoCTF, CTFtime, certification, OSCP,
OSWE, OSEP, eJPT, PNPT, BTL1, blue team lab, range, vulnerable app.

**Process contract:** Always run the Universal Search Loop (Section 1) and the Process Compliance
Gate (Section 0.5). This module supplies sources and queries only.

---

## Primary sources

### Web / appsec
| Platform | Notes |
|---|---|
| **PortSwigger Web Security Academy** | Free, high-quality labs for web vulns |
| **OWASP Juice Shop** | Modern vulnerable web app |
| **DVWA / WebGoat / Mutillidae** | Classic vulnerable apps |
| **PentesterLab** | Exercises and badges |
| **Root-Me** | Broad challenge set |
| **HackThisSite** | Beginner-friendly |

### Offensive labs and ranges
| Platform | Notes |
|---|---|
| **Hack The Box** | Machines, challenges, Academy, Pro Labs |
| **TryHackMe** | Guided rooms, beginner-friendly |
| **VulnHub** | Downloadable VMs |
| **OffSec Proving Grounds** | OSCP-style practice |
| **VulnLab** | AD/cloud labs |
| **EchoCTF** | Continuous CTF |
| **DockerLabs** | Docker-based challenges |
| **HackMyVM** | Community VMs |
| **PentesterLab** | Web-focused |

### CTF and competitions
- **CTFtime** (`ctftime.org`) - calendar, writeups, ratings.
- **picoCTF** - beginner CTF.
- **DEF CON CTF**, **Google CTF**, **PlaidCTF**, **HTB Cyber Apocalypse**.
- **SANS Holiday Hack Challenge** - free seasonal.
- **CTF archives** on GitHub (`ctf-writeups`).

### Blue team / defensive
- **Blue Team Labs Online**, **CyberDefenders**, **LetsDefend**.
- **SANS** courses and free resources.
- **malware-traffic-analysis.net** - pcaps, malware samples, and traffic-analysis exercises;
  handle samples only in an isolated lab.
- **Detection Engineering** labs (Sigma, Atomic Red Team).
- **Microsoft Learn** security paths, **AWS Skill Builder**, **Google Cloud Skills Boost**.

### Certifications
- Offensive: OSCP/OSWE/OSEP (OffSec), eJPT/eCPPT (INE), PNPT (TCM), CRTP/CRTO.
- Defensive: BTL1/BTL2 (Security Blue Team), GCIH/GCIA (GIAC), CCD (CyberDefenders).
- Cloud: AWS Security Specialty, Azure AZ-500, GCP Professional Security.
- AppSec: CSSLP, GWAPT, Burp Suite Certified Practitioner.

---

## Query recipes

```text
# Platform-specific
site:portswigger.net/web-security "SQL injection"
site:hackthebox.com "machine" "writeup"
site:tryhackme.com "room" "walkthrough"
site:ctftime.org "writeup" "pwn"
site:pentesterlab.com "exercise"
site:overthewire.org "bandit"

# Skill-gap search
"practice" "SSRF" lab
"vulnerable application" "GraphQL" docker
"AD lab" "Kerberoasting" practice
"cloud security" lab AWS
"blue team" lab "detection"
site:malware-traffic-analysis.net "pcap"

# CTF writeups
"CTF writeup" "web" "2025"
"picoCTF" writeup "forensics"
"HTB" "writeup" "privilege escalation"
site:github.com "ctf-writeups"

# Certifications
"OSCP" "practice" "Proving Grounds"
"PNPT" vs "OSCP"
"BTL1" review
"Burp Suite Certified Practitioner" exam
```

---

## Workflow

1. **Define the skill gap and level.** Beginner, intermediate, advanced; web, AD, cloud, binary,
   blue team.
2. **Choose a platform** that matches the gap and provides feedback.
3. **Attempt before reading the writeup.** Timebox; record what you tried.
4. **Read the writeup only after the attempt.** Extract the technique, not just the answer.
5. **Reproduce in your own lab.** Rebuild the vulnerable setup; vary the conditions.
6. **Document a reusable playbook.** Preconditions, discovery, exploitation concept, detection,
   fix.
7. **Repeat with spaced practice.** Revisit after a week; try a variant.
8. **Track progress** against a skills matrix (e.g., OWASP WSTG, ATT&CK).

---

## What to extract

| Field | Example |
|---|---|
| Skill | SSRF via PDF generator |
| Lab | PortSwigger lab "SSRF with blacklist" |
| Prerequisites | URL fetch feature, internal network |
| Technique | DNS rebinding / redirect bypass |
| Detection | outbound request logs |
| Defense | allowlist, metadata blocking |
| Confidence | A (reproduced in lab) |

---

## Pitfalls

- **Spoiling yourself.** Reading writeups first reduces learning.
- **Platform rules.** Do not share flags, solutions, or private machine details.
- **Outdated labs.** Some VMs are old and no longer represent real systems.
- **Tutorial hell.** Watching without doing does not build skill.
- **Certification chasing.** Certs validate baseline knowledge, not real-world judgment.
- **Legal boundaries.** Labs are authorized; the internet is not.

---

## Ethics

- Stay within platform terms of service.
- Do not attack other users, infrastructure, or the platform.
- Do not share flags or paid content.
- Use skills lawfully and ethically; get authorization for real targets.

---

## Output contract

```
module:        M9 Labs/CTF
objective:     close skill gap <X> at level <Y>
authorization: lab/platform only
sources_used:  platform, challenge, writeup URL + date, mapped to the claim it supports
sources_read:  URLs opened but excluded, with reason (off-scope, stale, duplicate, low confidence, inaccessible, discovery only)
findings:      technique, prerequisites, detection, defense
pivots:        M2 writeups, M4 cheatsheet, M6 secure code
caveats:       lab realism, platform rules, confidence
```
