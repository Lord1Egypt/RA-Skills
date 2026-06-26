## Description: <br>
Pre-publish privacy scan for ClawHub skills that detects tokens, keys, credentials, .env secrets, personal info, and internal IPs before publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weidongkl](https://clawhub.ai/user/weidongkl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and publishers use this skill before publishing ClawHub skills to scan for exposed secrets, personal details, and internal network indicators, then review the full report before confirming publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Full scan reports can expose detected secrets, credentials, personal paths, emails, or internal network details in the agent conversation. <br>
Mitigation: Inspect full results locally or share a redacted summary when scanning directories that may contain real private data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/weidongkl/skill-publish-vetter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and scan report text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include sensitive findings if the scanned skill contains real secrets or private details.] <br>

## Skill Version(s): <br>
1.1.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
