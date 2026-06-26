## Description: <br>
Vibe Card helps an agent generate, manage, share, receive, and synchronize social business cards and a local contact book. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sxd20010606-cmd](https://clawhub.ai/user/sxd20010606-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use this skill to create a personal Vibe Card from remembered profile information, publish selected fields, exchange cards through text messages, and maintain a synchronized contact book. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish personal card fields to the Vibe Card server. <br>
Mitigation: Review every generated or updated field before publishing, and keep sensitive background or personal notes out of public fields. <br>
Risk: The skill can import received card data into a local contact book. <br>
Mitigation: Avoid processing cards from untrusted messages and confirm ambiguous or duplicate contacts before saving or merging. <br>
Risk: The skill stores a local service credential after registration. <br>
Mitigation: Limit access to the local config file and remove the credential if the skill is no longer used. <br>
Risk: The skill can set up recurring contact synchronization. <br>
Mitigation: Create scheduled sync only with user approval and remove the cron task if background updates are not desired. <br>


## Reference(s): <br>
- [Vibe Card release page](https://clawhub.ai/sxd20010606-cmd/vibe-card) <br>
- [Vibe Card data format specification](references/data-format.md) <br>
- [Vibe Card operation manual](references/manual.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Plain text and Markdown responses with local JSON data files and optional shell commands for scheduled sync.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces contact-card text blocks, profile/contact JSON updates, server API interactions, and optional cron setup guidance.] <br>

## Skill Version(s): <br>
4.0.0 (source: server release metadata, SKILL.md metadata, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
