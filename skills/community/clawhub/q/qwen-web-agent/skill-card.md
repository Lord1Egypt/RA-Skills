## Description:

Browser automation for the Qwen web interface at qianwen.com that sends single-turn or multi-turn prompts, waits for responses, and captures replies through Playwright.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dereksongyang](https://clawhub.ai/user/dereksongyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to ask Qwen questions through its web interface and capture the model's replies for downstream workflows. It supports both one-shot prompts and multi-turn sessions that preserve browser login state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores persistent browser login state and Qwen transcript output locally, which can expose account state, prompts, and model responses.

Mitigation: Use a dedicated Qwen account or browser profile, restrict access to ~/.qwen_session/ and output Markdown files, and treat those files as sensitive.

Risk: The scripts launch Chromium with --no-sandbox.

Mitigation: Review the scripts before installation and remove --no-sandbox where the execution environment supports normal Chromium sandboxing.

Risk: The skill automatically deletes Qwen conversations from the logged-in account after use.

Mitigation: Review or modify the cleanup behavior before use if conversation retention or auditability is required.

## Reference(s):

- [Qwen Web Agent usage guide](references/使用说明.md)
- [Qwen web interface](https://www.qianwen.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown files and terminal text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-turn output is written to last_output.md; multi-turn output is appended to qwen_session_history.md.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
