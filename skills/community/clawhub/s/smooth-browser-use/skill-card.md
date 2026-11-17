## Description:

Guides agents through browser workflows that need human-like navigation, reliable real-event text entry, front-end state checks, and clean recovery for stuck or stale pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuxinyang111](https://clawhub.ai/user/shuxinyang111)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to make browser automation interact through visible UI controls, real paste/input events, page state checks, and recovery refreshes when pages become stale or inconsistent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may place task text on the system clipboard, which can overwrite or expose clipboard contents.

Mitigation: Use clipboard-based entry only where clipboard use is acceptable and avoid sensitive text unless policy permits it.

Risk: Refresh-based recovery can discard unsaved page state.

Mitigation: Confirm important state is saved or reproducible before refreshing, then restart from the page's clean state after reload.

## Reference(s):

- [Smooth Browser Use on ClawHub](https://clawhub.ai/shuxinyang111/skills/smooth-browser-use)

## Skill Output:

**Output Type(s):** [guidance, text]

**Output Format:** [Markdown guidance with ordered workflows, checks, and browser recovery steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to use clipboard paste, visible controls, state inspection, and page refresh recovery.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
