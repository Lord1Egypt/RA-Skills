## Description:

Use UniFuncs Deep Research API to run in-depth research and generate long-form reports (10,000 words or more).

This skill is ready for commercial/non-commercial use.

## Publisher:

[vinlic](https://clawhub.ai/user/vinlic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to send confirmed deep-research requests to UniFuncs and receive long-form reports, summaries, article drafts, or task status results. It is intended for research questions that need multiple rounds of searching and reading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research topics and prompts are sent to UniFuncs for processing.

Mitigation: Use the skill only for topics approved for UniFuncs processing; avoid confidential or regulated material unless explicitly approved.

Risk: Default report mode can continue streaming in a detached background process and leave output in temporary stream files.

Mitigation: Prefer non-streaming mode for sensitive work and manually check/delete any unifuncs-deep-research stream files after use.

Risk: The security verdict is suspicious and recommends review before installation.

Mitigation: Review the skill and its security guidance before installing or enabling it in an agent environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vinlic/skills/unifuncs-deep-research)
- [UniFuncs account and API key setup](https://unifuncs.com/account)
- [Related UniFuncs Deep Search skill](https://github.com/UniFuncs/skills/blob/main/skills/unifuncs-deep-search/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Long-form text or Markdown reports, JSON task data, task IDs, and stream-file readback commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default report output targets 10,000 words and streaming mode may return partial content before completion.]

## Skill Version(s):

0.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
