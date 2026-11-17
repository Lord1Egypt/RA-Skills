## Description:

心事空间，承接私人倾诉、日记、零散想法与个人成长，支持有来源的记忆、FlowUs 同步和按需情感支持。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jichengkai](https://clawhub.ai/user/jichengkai)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals use the skill to talk through personal experiences, keep source-aware diary and reflection records, and retrieve or sync a dedicated private archive; emotional support is optional.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan flags broad private-chat capture and automatic cloud synchronization, with some inspection incomplete.

Mitigation: Do not install until the capture and sync behavior is clarified; if proceeding, bind it only to the intended private conversation and verify the destination archive's access permissions.

Risk: The security scan reports that a working-directory helper could run with access to a secret.

Mitigation: Address and review the helper-source concern before installation, and treat private conversation data and secrets as potentially exposed if you proceed.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/jichengkai/skills/xinshi-kongjian)
- [Archive and sync guide](references/archive.md)
- [Emotional support guidance](references/emotional-support.md)
- [Installation guide](references/install.md)
- [OpenClaw hooks documentation](https://docs.openclaw.ai/plugins/hooks/reference)
- [Hermes skills documentation](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills)
- [DeepSeek Harness skills documentation](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/skills.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Conversational text, Markdown records, JSON archive entries, and setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Source-aware personal records; AI-written material remains a draft pending review.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
