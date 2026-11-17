## Description:

Generates a structured help-request document for stalled AI coding work by using selected conversation sessions to extract errors, failed attempts, and context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[buzuweidao](https://clawhub.ai/user/buzuweidao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when AI coding assistance is stuck and they need a concise HELP_REQUEST.md for another human or AI reviewer. It guides the user through selecting relevant chat sessions, extracting errors and failed attempts, and producing a handoff document.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can discover local AI coding chat histories across multiple tools and may expose unrelated private conversation data.

Mitigation: Review the listed sessions before selection, choose only conversations related to the current problem, and avoid sharing the generated HELP_REQUEST.md until it has been checked for sensitive content.

Risk: Generated summaries and HELP_REQUEST.md content may include paths, prompts, errors, emails, or code snippets from prior chats.

Mitigation: Use the built-in redaction behavior and manually review the final document for secrets, private identifiers, and unrelated context before handing it to another reviewer.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/buzuweidao/skills/stuck)
- [Project homepage](https://github.com/buzuweidao/skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown document with interactive prompts and command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates HELP_REQUEST.md after the user selects relevant conversation sessions; summaries may include paths, prompts, errors, and code snippets from prior chats.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
