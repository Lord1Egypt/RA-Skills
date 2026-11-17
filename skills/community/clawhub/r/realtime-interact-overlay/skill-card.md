## Description:

Realtime Interact Overlay displays local macOS or browser pop-up dialogs so an agent can request user confirmation, input, or selection near the active workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lightcastlepro](https://clawhub.ai/user/lightcastlepro)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to pause actions such as posting comments, deleting files, or completing browser workflows until a user confirms or provides input.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive values entered through input, password, or payment dialogs can be exposed or mishandled.

Mitigation: Use the skill only for low-risk confirmations; do not enter passwords, payment codes, API keys, recovery phrases, or other secrets.

Risk: Browser mode injects JavaScript into the active page and can be unsafe on logged-in or sensitive pages.

Mitigation: Avoid browser JavaScript injection on logged-in or sensitive pages until message rendering uses literal text and the confirmation result flow is fully implemented.

Risk: A confirmation popup can still approve an incorrect or destructive agent action.

Mitigation: Review the proposed action text before execution, and scan and test the skill before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lightcastlepro/skills/realtime-interact-overlay)
- [ClawHub publisher profile](https://clawhub.ai/user/lightcastlepro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON result examples, and browser JavaScript snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [macOS mode returns confirmation, cancel, timeout, error, or sanitized input; browser mode returns injectable JavaScript and pending/result metadata.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
