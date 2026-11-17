## Description:

Guides developers through preserving task artifacts, cleaning a completed sandbox, and confirming it is ready for reuse.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jsmartinez99](https://clawhub.ai/user/jsmartinez99)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this procedure after sandbox validation or cancellation to preserve designated artifacts, remove temporary state, and record that the sandbox is ready for another task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cleanup or Git reset may destroy uncommitted work or artifacts outside the intended sandbox.

Mitigation: Confirm the exact disposable sandbox root and artifact preserve list; require a dry-run or deletion manifest and explicit approval for the specific Git and deletion targets.

Risk: Stopping services or removing volumes may erase persistent data or disrupt other work.

Mitigation: Identify the affected services and volumes before cleanup and obtain explicit approval for any volume deletion.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/jsmartinez99/skills/sop-dev-002-cleanup-post-sandbox)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes cleanup checks and a SANDBOX_CLEANED progress record.]

## Skill Version(s):

1.0.1 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
