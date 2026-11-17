## Description:

Uno CLI lets an agent use the Uno tool gateway by searching for a specific external tool, previewing the planned invocation with a dry run, and making the real call only after explicit user approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lxyd-ai](https://clawhub.ai/user/lxyd-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when built-in skills cannot satisfy a narrow, user-requested real-time lookup or external service action. It provides a searchable gateway workflow with credential checks, dry-run previews, and explicit approval before real calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is a broad remote tool gateway with a persistent local Uno API key and possible third-party account connections.

Mitigation: Use it only after review, keep calls user-visible, require dry-run preview plus explicit approval before every real call, and avoid authorizing account or key management actions without separate confirmation.

Risk: Security-critical behavior depends on the external uno-cli package, and the release declares a version range rather than an exact pinned package.

Mitigation: Prefer a pinned, reviewed uno-cli version and re-review before upgrading the runtime dependency.

Risk: The authoritative security summary reports inconsistent consent instructions in the Chinese workflow.

Mitigation: Apply the stricter consent posture in every language workflow: search, dry-run preview, explicit user approval, then a single real call.

## Reference(s):

- [Uno homepage](https://agentools.uno)
- [Uno CLI PyPI package](https://pypi.org/project/uno-cli/)
- [ClawHub skill page](https://clawhub.ai/lxyd-ai/skills/uno-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are user-facing instructions for invoking the external Uno CLI and interpreting JSON responses.]

## Skill Version(s):

1.2.1 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
