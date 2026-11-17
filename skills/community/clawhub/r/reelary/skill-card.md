## Description:

Guides agents in connecting Reelary, indexing and searching local video and photo libraries, and troubleshooting related tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[reelary](https://clawhub.ai/user/reelary)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to manage a local Reelary media library, find footage by meaning, and prepare draft cuts. It also guides setup, indexing, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Footage details and preview images may be sent to the connected cloud AI provider even when media indexing is local.

Mitigation: For confidential footage, use a local model or Reelary directly; choose indexed folders carefully.

Risk: The downloaded application and npm implementation were not audited in the supplied security evidence.

Mitigation: Prefer a reviewed package version and obtain user consent before installing or running it.

## Reference(s):

- [Reelary ClawHub skill page](https://clawhub.ai/reelary/skills/reelary)
- [Installing Reelary](references/install.md)
- [Reelary MCP tools](references/tools.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands]

**Output Format:** [Markdown/text guidance, shell command examples, and Reelary search or draft-cut results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results may include local file paths and clip time ranges.]

## Skill Version(s):

0.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
