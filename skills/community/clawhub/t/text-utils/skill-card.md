## Description:

Text Utils is a local command-line text utility for counting characters, Han characters, words, and lines, changing case, reversing text, deduplicating terms, and trimming whitespace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tonyhuya](https://clawhub.ai/user/tonyhuya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and automation users use this skill to process text locally through shell commands for word counts, case conversion, text reversal, deduplication, line counting, and whitespace trimming.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may run a Chinese-language command-line utility without understanding its prompts or output.

Mitigation: Review the help text and expected command behavior before use, especially in automated workflows.

Risk: The counting command depends on python3 being available in the execution environment.

Mitigation: Install or verify python3 before using count operations.

Risk: Sensitive text could be provided to shell commands by mistake.

Mitigation: Use the tool locally as designed and review command inputs before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tonyhuya/skills/text-utils)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text and Markdown with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local command-line text processing; no network behavior indicated by security evidence.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
