## Description:

Track and analyze AI session cost-to-value by logging task, value, and token use to optimize productivity and reduce wasted effort.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rushant-123](https://clawhub.ai/user/rushant-123)

### License/Terms of Use:


## Use Case:

Developers and AI agent users can use this skill to log session tasks, value categories, token usage, and estimated costs, then review patterns that help reduce low-value work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled shell script has unsafe Python fallback paths that may execute injected commands under the user's account.

Mitigation: Review or fix track.sh before installing; keep jq installed, avoid logging untrusted text, prevent untrusted code from setting SESSION_COST_FILE, and pass data and paths to Python as arguments or stdin.

Risk: Session logs can contain task, outcome, token, model, and cost details in a local JSON file.

Mitigation: Avoid recording sensitive task details and protect access to the configured session cost file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rushant-123/skills/session-cost-tracker)
- [Publisher profile](https://clawhub.ai/user/rushant-123)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell command examples and local JSON log output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes session records to a local JSON file when the shell script is used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
