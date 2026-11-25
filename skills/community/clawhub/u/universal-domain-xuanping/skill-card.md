## Description:

Performs a read-only, evidence-based eight-dimension risk review of a domain and adds a deterministic I-Ching reading for entertainment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openmsg88](https://clawhub.ai/user/openmsg88)

### License/Terms of Use:

MIT-0

## Use Case:

Domain owners and developers can use this skill to review DNS, TLS, HTTP headers, exposed subdomains, page content, registration age, and compliance-publicity evidence. It produces risk hints rather than legal conclusions, and its hexagram reading is for entertainment only.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Domain checks may reach internal network services, and incomplete checks may appear conclusive.

Mitigation: Run only where outbound requests to private or internal addresses are blocked, and treat results as preliminary when checks are incomplete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/openmsg88/skills/universal-domain-xuanping)
- [Risk grading criteria](artifact/references/RISK_GRADING.md)
- [README and quick start](artifact/README.md)
- [Optional online experience](https://www.hu5.cn/xp/)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON]

**Output Format:** [Markdown risk report with structured JSON evidence and a separate hexagram reading]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Eight assessment dimensions; read-only evidence collection; the hexagram is entertainment only and not part of the conclusions.]

## Skill Version(s):

1.2.3 (source: frontmatter, changelog released 2026-11-24)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
