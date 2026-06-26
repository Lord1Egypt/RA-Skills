## Description: <br>
SkillForge watches how users work, discovers repeated workflow patterns, and drafts reusable Skills for review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jfranklee](https://clawhub.ai/user/jfranklee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use SkillForge to identify repeated workflows in work logs or conversation history, score them for reuse, and generate skill drafts or evolution suggestions for manual approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill analyzes local logs, memory files, conversation history, and existing skills, which may expose sensitive workflow details to the agent session. <br>
Mitigation: Review the monitored paths and triggers before use, exclude sensitive logs, and disable weekly auto-scan or real-time detection unless ongoing monitoring is intended. <br>
Risk: Generated or merged skill drafts may encode incorrect, stale, or misleading workflow guidance. <br>
Mitigation: Manually review every generated draft or merge proposal before approving it, and scan drafts before deployment. <br>
Risk: Broad trigger phrases and automatic scans may produce unwanted pattern reports from private work history. <br>
Mitigation: Use narrow trigger phrases, keep pattern reports summarized, and avoid raw log quotes in generated reports. <br>


## Reference(s): <br>
- [SkillForge ClawHub release](https://clawhub.ai/jfranklee/skillforge-meta) <br>
- [jfranklee publisher profile](https://clawhub.ai/user/jfranklee) <br>
- [SkillForge - Algorithm Deep Dive](references/ALGORITHM.md) <br>
- [SkillForge - Full Configuration Reference](references/CONFIG_FULL.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown reports, SKILL.md drafts, and YAML configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Drafts are written for user review and are not installed automatically.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
