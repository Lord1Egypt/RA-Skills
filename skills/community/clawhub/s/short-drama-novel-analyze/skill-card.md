## Description:

拆解小说原文，评估改编价值，并整理章节剧情、人物演进与分集候选。

This skill is ready for commercial/non-commercial use.

## Publisher:

[worldwonderer](https://clawhub.ai/user/worldwonderer)

### License/Terms of Use:

MIT

## Use Case:

For creators and story development teams, this skill evaluates a novel's adaptation potential, organizes evidence-based chapter and character analysis, and prepares episode candidates for a chosen chapter range.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment has medium confidence because part of a referenced script was not fully inspected, leaving some behavior uncertain.

Mitigation: Review the unassessed script portions and keep file access limited to source material the user is authorized to provide.

## Reference(s):

- [Adaptation triage guide](artifact/references/adaptation-triage.md)
- [Chapter extraction guide](artifact/references/chapter-extraction.md)
- [Stage contract](artifact/references/stage-contract.md)
- [Adaptation value and episode candidates](artifact/references/adaptation-value.md)
- [ClawHub release page](https://clawhub.ai/worldwonderer/skills/short-drama-novel-analyze)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, JSONL, Shell commands, Guidance]

**Output Format:** [Markdown analysis and project files, with JSON chapter indexes and JSONL episode candidates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the supplied novel and selected chapter range; source text is treated as read-only.]

## Skill Version(s):

1.0.39 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
