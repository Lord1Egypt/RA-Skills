## Description: <br>
Maintain a large ClawHub skill portfolio with a quality-first and AI-assisted upgrade lens. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ClawHub publishers use this skill to audit public skill portfolios, prioritize maintenance, generate approval-gated cleanup or upgrade plans, and build local dashboard reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated approval boards and shell command previews can affect public skill visibility or publishing if executed without review. <br>
Mitigation: Require explicit approval for each batch, review generated boards first, and treat hide, merge, publish, and rescan operations as account-impacting actions. <br>
Risk: Partial or failed skill-detail data can lead to incorrect cleanup, maintenance, or candidate decisions. <br>
Mitigation: Move failed detail fetches to data_unavailable, exclude them from decisions for that run, and refresh collection later instead of retrying aggressively. <br>
Risk: Merge operations may be difficult to reverse. <br>
Mitigation: Review the canonical target before approving merge batches and prefer reversible hide or unhide workflows before deletion-oriented cleanup. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/skill-maintainer) <br>
- [Publisher Profile](https://clawhub.ai/user/harrylabsj) <br>
- [Repository URL from artifact metadata](https://github.com/harrylabsj/clawhub-skill-maintainer) <br>
- [Issue Tracker from artifact metadata](https://github.com/harrylabsj/clawhub-skill-maintainer/issues) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, CSV, JSON, HTML, shell command previews, and concise text guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates local reports, dashboards, approval packets, and maintainer prompts; account-impacting commands are gated by explicit approval.] <br>

## Skill Version(s): <br>
1.3.3 (source: server release evidence and package metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
