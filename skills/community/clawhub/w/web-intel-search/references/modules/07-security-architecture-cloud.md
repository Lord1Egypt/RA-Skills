# M7 - Security Architecture, Cloud & Design Review

**Purpose:** Find reference architectures, control frameworks, zero-trust patterns, cloud security
guidance, and design-review checklists to evaluate or design a secure system.

**Triggers:** security architecture, architect security, zero trust, cloud security, AWS/Azure/GCP
security, reference architecture, NIST, CIS, ISO 27001, segmentation, defense in depth, design
review, security controls, shared responsibility, landing zone, network architecture.

**Process contract:** Always run the Universal Search Loop (Section 1) and the Process Compliance
Gate (Section 0.5). This module supplies sources and queries only.

---

## Primary sources

### Frameworks and standards
| Source | Use |
|---|---|
| **NIST CSF 2.0** | Govern, Identify, Protect, Detect, Respond, Recover |
| **NIST SP 800-53** | Control catalog |
| **NIST SP 800-207** | Zero trust architecture |
| **NIST SP 800-171** | CUI protection |
| **NIST SP 800-190** | Container security |
| **NIST SP 800-204** | Microservices security |
| **CIS Controls v8** | Prioritized safeguards |
| **CIS Benchmarks** | Product hardening |
| **ISO/IEC 27001/27002** | ISMS and controls |
| **CSA CCM / STAR** | Cloud controls |
| **PCI DSS** | Payment card scope |
| **SOC 2** | Trust services criteria |
| **SABSA / TOGAF** | Architecture frameworks |

### Cloud provider guidance
- **AWS**: Well-Architected Security Pillar, Security Reference Architecture, Landing Zone
  Accelerator, IAM best practices, Organizations/SCP, GuardDuty/Security Hub.
- **Azure**: Well-Architected Framework (Security), Microsoft Cloud Security Benchmark, Azure
  Landing Zone, Entra ID, Defender for Cloud.
- **GCP**: Architecture Framework (Security), security best practices, VPC Service Controls,
  Cloud IAM, Security Command Center.
- **Kubernetes**: NSA/CISA hardening guide, CIS Kubernetes Benchmark, Pod Security Standards.
- **Containers**: NIST 800-190, Docker/OCI security docs, image signing (cosign), SBOM.

### Offensive cloud knowledge bases
- **Hacking The Cloud** (`hackingthe.cloud`) - AWS/Azure/GCP/AI/LLM attack and defense techniques.
- **pathfinding.cloud** (`pathfinding.cloud`, `github.com/DataDog/pathfinding.cloud`) - AWS IAM
  privilege-escalation paths with detection mappings and labs.

---

## Query recipes

```text
# Zero trust
site:nist.gov "800-207" zero trust
"zero trust architecture" reference
"zero trust" "identity" "policy enforcement point"
"zero trust" "maturity model" CISA

# Cloud security
site:docs.aws.amazon.com "security pillar" "well-architected"
site:learn.microsoft.com "well-architected" "security"
site:cloud.google.com/architecture "security" "best practices"
"AWS landing zone" security controls
"Azure landing zone" "security"
"GCP" "VPC Service Controls" design
site:hackingthe.cloud "privilege escalation"
site:pathfinding.cloud "iam:PassRole"

# Controls and benchmarks
site:cisecurity.org "benchmark" "AWS"
site:nist.gov "800-53" "access control"
"ISO 27001" "Annex A" controls
"CSA CCM" "cloud controls matrix"

# Architecture review
"security architecture review" checklist
"design review" "threat model" "security"
"defense in depth" architecture pattern
"network segmentation" "microsegmentation" design
"shared responsibility model" cloud
"security reference architecture" example

# Kubernetes / containers
"NSA CISA" Kubernetes hardening
"CIS Kubernetes Benchmark" "Pod Security"
"container security" "image signing" "SBOM"
```

---

## Workflow

1. **Understand the business and system context.** Assets, data classification, actors, compliance,
   availability requirements.
2. **Map the architecture.** Components, data flows, trust boundaries, identities, network zones,
   third parties.
3. **Select frameworks.** Map to NIST CSF/800-53, CIS, ISO 27001, and cloud-specific guidance.
4. **Identify risks.** Threat model (M6), attack paths, single points of failure, excessive trust,
   data exposure.
5. **Find reference patterns.** Zero trust, landing zones, segmentation, least privilege, encryption,
   logging, resilience.
6. **Assess gaps.** Compare current vs target state; rate by risk and effort.
7. **Design controls.** Preventive, detective, responsive; map to owners and evidence.
8. **Review trade-offs.** Cost, latency, operability, compliance, migration path.
9. **Deliver a roadmap.** Quick wins, medium-term, strategic; include verification.

---

## What to extract

| Field | Example |
|---|---|
| Control | NIST AC-6 least privilege |
| Cloud mapping | AWS IAM permissions boundaries + SCP |
| Pattern | centralized identity + per-workload roles |
| Anti-pattern | long-lived access keys in CI |
| Evidence | IAM Access Analyzer, Config rules |
| Risk | High |
| Confidence | B (framework + vendor docs) |

---

## Pitfalls

- **Compliance is not security.** Passing an audit does not mean resisting attack.
- **Shared responsibility confusion.** Misconfigured customer-side controls are common.
- **Legacy constraints.** Not every pattern fits an existing monolith.
- **Region and data residency.** Encryption and replication choices have legal impact.
- **Control sprawl.** Too many tools without ownership and response processes.
- **Ignoring identity.** Most cloud incidents involve identity and credentials.
- **Static design.** Architectures drift; review continuously.

---

## Ethics

- Architecture guidance is defensive and generally safe to share.
- Respect confidentiality of designs and diagrams.
- Do not expose customer data or internal endpoints in examples.
- Base recommendations on authoritative sources, not vendor marketing.

---

## Output contract

```
module:        M7 Security Architecture
objective:     design/review <system> against <framework>
authorization: owner/architect authorization
sources_used:  NIST/CIS/ISO + cloud provider docs + reference architectures, mapped to the claim it supports
sources_read:  URLs opened but excluded, with reason (off-scope, stale, duplicate, low confidence, inaccessible, discovery only)
findings:      control mapping, gaps, patterns, anti-patterns, roadmap
pivots:        M6 threat model, M12 report, M11 vendor guidance
caveats:       business constraints, compliance scope, unverified assumptions
```
