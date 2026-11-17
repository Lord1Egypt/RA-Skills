## Description:

Translates SRT subtitle files into a target language using AI, batching large files, preserving timing and format, and producing a translated SRT file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mcbaivn](https://clawhub.ai/user/mcbaivn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to translate subtitle files for films or videos into a selected target language while preserving SRT timecodes and structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing with an unpinned ClawHub installer version can change install behavior over time.

Mitigation: Use a pinned ClawHub installer version before installing the skill.

Risk: The skill reads subtitle content supplied by the user and sends text through the agent's translation workflow.

Mitigation: Run it only on subtitle files the user intends the agent to read and translate.

Risk: The workflow creates a translated SRT output file near the input path.

Mitigation: Review the requested input and output paths before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mcbaivn/skills/subtitle-translator-mcbai)
- [MCB AI](https://www.mcbai.vn)
- [OpenClaw Cheatsheet](https://openclaw.mcbai.vn)
- [OpenClaw 101](https://openclaw.mcbai.vn/openclaw101)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [SRT subtitle file and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves original SRT timecodes and writes a translated output file near the input path.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
