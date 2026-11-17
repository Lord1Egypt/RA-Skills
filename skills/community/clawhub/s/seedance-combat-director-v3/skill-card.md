## Description:

Seedance Combat Director v3 helps agents design, diagnose, continue, and rewrite Chinese-first Seedance 2.5 combat and action video prompts using a complete brief and evidence-based video review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangminrui2022](https://clawhub.ai/user/wangminrui2022)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, prompt engineers, and video-production developers use this skill to turn complete combat briefs and provided media into structured Seedance 2.5 action-video prompts, or to revise generated footage only after inspecting the actual video evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may provide incomplete combat briefs and expect the agent to invent duration, aspect ratio, characters, scene, combat mode, or ending.

Mitigation: The skill requires hard fields before prompt generation and instructs the agent to ask one concise missing-information question set instead of producing a draft.

Risk: Generated-video revisions can become speculative if the source video is unavailable or only an old prompt is provided.

Mitigation: The skill requires actual video evidence for continuation or revision, reports visible issues by time range when available, and refuses evidence-based diagnosis when footage cannot be accessed.

Risk: Users may expose media or brief details they did not intend to have analyzed.

Mitigation: Security guidance says to provide only the videos, images, and brief details intended for analysis.

Risk: The skill is Chinese-first and may not match users who expect another language or output format.

Mitigation: Security guidance says users should ask explicitly when they want output in another language or format.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wangminrui2022/skills/seedance-combat-director-v3)
- [Seedance Combat Director README](artifact/README.md)
- [Skill Instructions](artifact/SKILL.md)
- [Intake Contract](artifact/references/intake-contract.md)
- [Combat Patterns](artifact/references/combat-patterns.md)
- [Research Notes](artifact/references/research-notes.md)
- [Combat Brief Template](artifact/templates/brief.md)
- [Brief Validator](artifact/scripts/validate_brief.py)
- [ByteDance](https://www.bytedance.com/)
- [lansenai Seedance Reference](https://x.com/lansenai/status/2097165176013255100)
- [Strength04_X Seedance Reference](https://x.com/Strength04_X/status/2096811204706795767)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, usually a single Chinese text code block for complete prompts, with concise missing-field questions or short evidence-based diagnostics when needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-first workflow; requires a complete Combat Brief before prompt generation; may use the included JSON brief validator for completeness checks.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
