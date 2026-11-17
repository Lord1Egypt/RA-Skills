## Description:

Security-first behavioral guidelines for cautious agent operation around external resources, installations, credentials, and other actions with external effects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[doonot](https://clawhub.ai/user/doonot)

### License/Terms of Use:


## Use Case:

Developers and agent users can use this skill to guide cautious operation before interacting with links, installing packages, handling credentials, or taking actions that may expose data or have external effects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact names a specific approver, Pat, which may not match the actual authorized user or administrator.

Mitigation: Replace the named approver with the authenticated user or configured administrator before installation.

Risk: The no-approval allowance for local file operations is broad and could cover sensitive workspace activity.

Mitigation: Limit no-approval local file activity to non-sensitive read-only workspace operations.

Risk: The artifact does not explicitly state that platform and system policies take precedence.

Mitigation: Add a clear precedence rule so platform and system policies override the skill when they conflict.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Markdown]

**Output Format:** [Markdown behavioral protocol and checklist guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces safety-oriented instructions for human review and agent behavior; no executable payload.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
