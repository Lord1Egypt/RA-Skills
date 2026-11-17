## Description:

Helps manage noisy SnapVisor visual diffs by finding flaky tests, listing ignored changes, and ignoring or restoring individual changes after confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devino](https://clawhub.ai/user/devino)

### License/Terms of Use:

MIT-0

## Use Case:

Developers reviewing SnapVisor screenshot diffs can identify flaky tests, inspect ignored changes, and selectively ignore or restore a known-noisy change without affecting other diffs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting SnapVisor grants access according to approved OAuth scopes.

Mitigation: Review requested SnapVisor OAuth scopes before connecting.

Risk: Ignoring or restoring the wrong visual change can alter which diffs are flagged.

Mitigation: Confirm the intended build, test, and change before each ignore or restore action.

## Reference(s):

- [Handling Flaky Changes on ClawHub](https://clawhub.ai/devino/skills/snapvisor-handling-flaky-changes)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports returned flakiness metrics and confirms each change before ignoring or restoring it.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
