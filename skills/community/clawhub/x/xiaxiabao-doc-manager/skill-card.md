## Description: <br>
XiaxiaBao Doc Manager helps an agent organize Feishu Wiki, Drive, and Bitable content through document creation, classification, archiving, backup, search, and template workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uuoov](https://clawhub.ai/user/uuoov) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Feishu workspace operators use this skill to create, classify, archive, back up, search, and tidy documents across Feishu Wiki, Drive, and Bitable. It is intended for document lifecycle management where Feishu IDs, backup sources, and cleanup actions are reviewed before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can back up sensitive local OpenClaw memory and configuration files into Feishu. <br>
Mitigation: Review and restrict backup sources before use, remove unnecessary MEMORY.md and openclaw.json sources, and confirm the Feishu destination permissions. <br>
Risk: Scheduled backups, archive moves, and retention cleanup can change or remove workspace records with limited safeguards. <br>
Mitigation: Require user confirmation before scheduled backup, archive, or cleanup actions and review retention settings such as maxCopies. <br>
Risk: Default Feishu identifiers and cross-skill configuration access may not match the user's workspace security boundaries. <br>
Mitigation: Replace all Feishu IDs with workspace-specific values and avoid reading other skills' configuration files unless explicitly authorized. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/uuoov/xiaxiabao-doc-manager) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill guide](artifact/SKILL.md) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Feishu Open Platform](https://open.feishu.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown and plain text responses with Feishu document links, archive reports, backup summaries, search results, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger Feishu document, wiki, drive, and bitable operations when configured with appropriate workspace identifiers and permissions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
