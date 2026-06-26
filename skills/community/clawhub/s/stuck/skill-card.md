## Description: <br>
Generate a structured help-request document when stuck with AI coding by scanning selected conversation sessions, extracting errors and failed attempts, and outputting HELP_REQUEST.md. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[buzuweidao](https://clawhub.ai/user/buzuweidao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill when an AI coding session is stuck and they need a concise handoff document for another person or agent. It guides the user through selecting relevant conversations, summarizing errors and failed attempts, and creating a structured HELP_REQUEST.md. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected AI coding-session histories may contain secrets, private code, personal data, local paths, or email addresses. <br>
Mitigation: Select only sessions relevant to the stuck issue and review HELP_REQUEST.md carefully before sharing, committing, or sending it to another agent. <br>
Risk: Conversation summaries can omit context or preserve misleading failed attempts. <br>
Mitigation: Use the built-in confirmation step to correct missing errors, failed approaches, and project context before generating the final document. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/buzuweidao/stuck) <br>
- [Skill homepage](https://github.com/buzuweidao/skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown file plus conversational guidance and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces HELP_REQUEST.md after user confirmation and applies basic redaction for API-key patterns, user paths, and email addresses.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
