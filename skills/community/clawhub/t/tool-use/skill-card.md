## Description:

Tool Use helps agents convert natural-language intent into structured tool calls, generate OpenAI-style function schemas, dispatch explicitly registered command or Python tools, and collect results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to define tool schemas, translate user intent into JSON tool calls, register callable tools, validate arguments, and dispatch registered tools during agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registered command tools can execute shell commands.

Mitigation: Review and restrict every registry entry, run the skill in a low-privilege sandbox, and avoid passing untrusted arguments to command tools.

Risk: Python tool entries can import and execute configured functions.

Mitigation: Allow only reviewed modules and functions in the registry and keep the execution environment isolated from sensitive files or credentials.

Risk: The learning workflow can persist usage notes and preferences locally.

Mitigation: Avoid recording sensitive user data and review persisted learning files before sharing or packaging the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/tool-use)
- [Publisher profile](https://clawhub.ai/user/qq435912743)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell commands; scripts can produce JSON files and command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local persistence of learned usage notes and preferences.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
