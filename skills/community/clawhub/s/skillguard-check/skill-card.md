## Description: <br>
Audits locally installed AI Skills against skillguard.vip's public security database and reports blocked or high-risk skills with audit links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangyixxxx](https://clawhub.ai/user/yangyixxxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and security-conscious users use this skill to check locally installed AI Skills before invoking unfamiliar or newly installed skills. It helps surface blocked, high-risk, and unaudited skills so the user can decide what to review or uninstall. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installed skill names are sent to skillguard.vip or the configured replacement API during checks. <br>
Mitigation: Install only if that disclosure is acceptable, or configure an API endpoint you trust. <br>
Risk: Private, local, or unpublished skills may not appear in the public audit database. <br>
Mitigation: Review unaudited results manually and treat them as not yet assessed rather than safe. <br>
Risk: A public audit result can lag behind a republished or locally modified skill. <br>
Mitigation: Prefer pinned or marketplace-installed copies and use the linked audit page to confirm the current scan context. <br>


## Reference(s): <br>
- [Skillguard homepage](https://skillguard.vip) <br>
- [skillguard-check public audit](https://skillguard.vip/skills/clawhub/skillguard-check) <br>
- [ClawHub skill page](https://clawhub.ai/yangyixxxx/skillguard-check) <br>
- [ClawHub audit report](https://skillguard.vip/report/clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [JSON report plus Markdown-style user summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes audit URLs, risk levels, finding counts, unaudited counts, and a nonzero exit code when blocked or high-risk skills are found.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
