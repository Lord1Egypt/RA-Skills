## Description:

Parse X (Twitter) articles with r.jina.ai, then create or reuse a NotebookLM notebook and upload the parsed article as a source.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicoxia](https://clawhub.ai/user/nicoxia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to move public X article content into NotebookLM for reading, organization, and analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted URL, notebook name, notebook ID, or environment values could cause unintended local shell command execution.

Mitigation: Review and fix command construction before use; pass only trusted, non-private values until the script safely invokes subprocesses without shell interpolation.

Risk: Fetched or uploaded article content may remain in local temporary files after a successful run.

Mitigation: Avoid sensitive content and confirm temporary files are removed after execution.

Risk: NotebookLM uploads store provided content outside the local workspace.

Mitigation: Upload only content that is appropriate to store in NotebookLM under the user's account and organization policies.

Risk: X content requiring login may not be available through r.jina.ai.

Mitigation: Use public URLs or a reviewed alternative workflow for authenticated content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nicoxia/skills/x-to-notebooklm)
- [Publisher profile](https://clawhub.ai/user/nicoxia)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Console text with identifiers, status messages, and Markdown source content uploaded through NotebookLM CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, curl, network access to r.jina.ai, and an authenticated NotebookLM CLI.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
