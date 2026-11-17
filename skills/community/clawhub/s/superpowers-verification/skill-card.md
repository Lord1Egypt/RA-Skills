## Description:

Prompts an agent to run fresh verification commands and read actual output before claiming work is complete, fixed, passing, or successful.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axelhu](https://clawhub.ai/user/axelhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to make an agent verify completion, fixes, test status, and other success claims with fresh command output before reporting them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents that cannot reliably understand the Chinese instructions may misapply or ignore the verification checklist.

Mitigation: Install this skill only where the agent can understand the Chinese instructions and can run the relevant verification commands.

Risk: The skill may make an agent more conservative about completion claims and add verification steps before reporting success.

Mitigation: Use it where extra verification before completion claims is desired, and expect reports to include command evidence and output summaries.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown instructions with verification checklists and command-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code; directs the agent to verify claims with fresh command output.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
