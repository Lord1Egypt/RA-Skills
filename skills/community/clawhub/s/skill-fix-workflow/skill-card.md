## Description:

Automatically extracts and stitches sequential skill and tool calls from a conversation into a configurable, exception-handled workflow saved as an automated Python program.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ugpoor](https://clawhub.ai/user/ugpoor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation builders use this skill to turn a successful chat-driven sequence of skill, tool, or function calls into a reusable Python workflow with extracted parameters, output handling, and exception handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation content is converted into runnable Python, so malicious or malformed text could become executable workflow code.

Mitigation: Use only trusted conversation content and inspect generated Python before running it.

Risk: Generated workflows can write to files, API destinations, or web/HTML outputs.

Mitigation: Use file, API, and web outputs only when destinations are explicit and trusted, especially for sensitive data.

Risk: Generated HTML reports may contain data from untrusted sources.

Mitigation: Do not open generated HTML reports from untrusted data in an authenticated browser context.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ugpoor/skills/skill-fix-workflow)

## Skill Output:

**Output Type(s):** [Text, Code, Files, Configuration]

**Output Format:** [JSON status objects and generated Python files, with human-facing Markdown-style status text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated workflows may write screen output, files, simulated API output, or HTML reports; generated business functions are placeholders that require review and implementation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
