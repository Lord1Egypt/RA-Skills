## Description:

Tool Registry helps agents register, discover, filter, and execute tools using token-based matching, permission levels, and agent-type allowlists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xhmqq616](https://clawhub.ai/user/xhmqq616)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to route tool-related requests, search registered tools, filter tools by permission or agent type, and execute selected tools through a registry API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled execution API can read files, write files, and run shell commands.

Mitigation: Use the skill only in controlled workspaces and require explicit authorization, workspace path restrictions, confirmations, and command limits before exposing execution.

Risk: Documented permission and agent filters do not by themselves enforce all execution controls.

Mitigation: Apply enforced permission checks around registry execution and review registered tools before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xhmqq616/skills/tool-registry)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JavaScript snippets, shell command examples, and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Registry operations may return JavaScript objects containing tool metadata, match scores, execution status, stdout, stderr, and errors.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
