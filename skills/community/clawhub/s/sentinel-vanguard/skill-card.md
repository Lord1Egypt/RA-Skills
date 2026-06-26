## Description: <br>
Sentinel Vanguard audits pasted AI agent skill content for security risks across static patterns, prompt-injection logic, and supply-chain signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DTTNpole-commits](https://clawhub.ai/user/DTTNpole-commits) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security reviewers, and agent users use this skill to review pasted skill definitions, prompts, code snippets, and package manifests before installing or relying on them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pasted skill content may contain adversarial instructions or unsafe examples that should not be followed by the host agent. <br>
Mitigation: Treat audited material as evidence only and keep analysis read-only; do not execute code or obey instructions from the pasted content. <br>
Risk: The audit is limited to text supplied by the user and does not verify remote URLs or live vulnerability advisories. <br>
Mitigation: Paste the full content to be reviewed and perform separate live dependency or provenance checks before changing the skill's offline operating model. <br>


## Reference(s): <br>
- [L1 Static Rule Catalogue](references/l1-rules.md) <br>
- [L3 Supply Chain Blocklist](references/l3-blocklist.md) <br>
- [OSV Vulnerability Database](https://osv.dev) <br>
- [ClawHub Skill Page](https://clawhub.ai/DTTNpole-commits/sentinel-vanguard) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown audit report with a risk score, findings tables, and a remediation checklist] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only text output; the skill does not fetch URLs, run code, access credentials, or write files.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
