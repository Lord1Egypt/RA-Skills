## Description: <br>
Skill Deep Audit helps an agent audit agent-skill folders with deterministic static and read-only dry-run checks, scoring, findings, and fix guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[songhonglei](https://clawhub.ai/user/songhonglei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to check whether an agent skill is ready to ship, identify ERR and WARN findings across seven audit dimensions, and receive a scorecard with prioritized remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A normal audit may write an AUDIT-{date}.md report into the target skill folder, and fix mode can edit that target skill after explicit authorization. <br>
Mitigation: Run it only on skill directories you are comfortable having read and annotated, review proposed fixes before authorizing them, and rely on the documented backup step before any fix workflow. <br>
Risk: Static and read-only dry-run checks can miss context or produce findings that need human judgment. <br>
Mitigation: Review the generated scorecard, especially ERR and WARN items, before using its results for release or deployment decisions. <br>


## Reference(s): <br>
- [Check Rules](references/check-rules.md) <br>
- [Controlled Domains](references/controlled-domains.md) <br>
- [Audit Report Output Template](references/output-template.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/songhonglei/skill-deep-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown scorecard file plus concise text summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces an AUDIT-{date}.md scorecard with ERR/WARN findings, scoring, citations, dependency notes, and fix recommendations.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
