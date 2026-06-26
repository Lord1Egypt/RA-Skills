## Description: <br>
Present multiple clarifying questions as an interactive Telegram form using inline buttons, selectable options, and an Other free-text fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edonadei](https://clawhub.ai/user/edonadei) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill when they need to collect two or more clarifying answers from a Telegram user before proceeding with a task. It is suited to onboarding flows, requirement gathering, preference collection, and other structured multi-question interactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The form can collect free-text answers that may include sensitive personal, financial, or credential data. <br>
Mitigation: Ask only for information needed for the task and avoid requesting passwords, credentials, financial details, or other sensitive data unless truly necessary. <br>
Risk: A user may submit or resume a stale form after the agent has lost the original conversation state. <br>
Mitigation: Detect missing or stale form state, explain that the prior form context is unavailable, and re-send the questions before using answers. <br>


## Reference(s): <br>
- [Form Patterns Reference](references/form-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, API calls] <br>
**Output Format:** [Markdown guidance with JSON Telegram message and inline-button payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses short callback_data values and conversation-local form state for selected and free-text answers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
