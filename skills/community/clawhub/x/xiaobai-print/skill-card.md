## Description:

Xiaobai Print helps an agent print files through a local MCP bridge by checking device readiness and capabilities, uploading files, creating print jobs, and briefly confirming status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zwwz22](https://clawhub.ai/user/zwwz22)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit local or URL-based files to a configured printer through the Xiaobai MCP bridge. The workflow confirms device readiness, printer capabilities, file upload status, job creation, and short job status before ending the session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local bridge and upload path can exercise broad authority over local files, bearer tokens, and remote MCP print tools.

Mitigation: Use a dedicated low-privilege token, keep the bridge bound to 127.0.0.1, and do not expose the bridge on a network.

Risk: The upload workflow can send local files to a remote service for printing.

Mitigation: Upload only files the user explicitly intends to print, and add allowlists for upload paths and destinations before production use.

Risk: Remote tool invocation through the bridge may allow unexpected tool names or origins if deployed without containment.

Mitigation: Review the generated skill before installing and prefer allowlists for tool names, bridge origins, and permitted print operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zwwz22/skills/xiaobai-print)
- [Publisher profile](https://clawhub.ai/user/zwwz22)
- [Skill source](artifact/skills/xiaobai-print/SKILL.md)
- [Tool schema](artifact/skills/xiaobai-print/schema/tools.json)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain-text responses with inline shell commands and JSON arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node, MY_MCP_TOKEN, and a local MCP bridge; the checked-in wrapper defaults to 127.0.0.1:8787.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
