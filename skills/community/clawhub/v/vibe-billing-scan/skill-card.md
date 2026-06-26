## Description: <br>
Scans OpenClaw logs to identify costly runs, sessions, retry storms, and looped tool calls that may be driving API spend higher. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shinertx](https://clawhub.ai/user/shinertx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to inspect local API usage logs, find unusually expensive runs or sessions, and identify retry storms, context growth, or repeated tool calls that increase costs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to run an unpinned external npm package against sensitive local API logs. <br>
Mitigation: Review the vibe-billing npm package and its documentation before running it, treat logs and scan output as sensitive, and avoid sharing results without redaction. <br>
Risk: The optional setup command may install a persistent proxy without enough artifact detail about its traffic scope, storage, transmission, or removal process. <br>
Mitigation: Avoid npx vibe-billing setup unless you understand what the proxy observes, where data is stored or sent, and how to disable or uninstall it. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/shinertx/vibe-billing-scan) <br>
- [Vibe Billing landing page](https://api.jockeyvc.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend local npx commands for scanning existing logs, checking status, or optionally setting up ongoing monitoring.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
