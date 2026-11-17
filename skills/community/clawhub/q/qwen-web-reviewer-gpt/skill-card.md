## Description:

GPT-only reviewer workflow for Qwen Web using the authenticated ChatGPT Work/Codex Cloud Browser. Requires GPT browser-control; not an OpenClaw-native integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ciklopentan](https://clawhub.ai/user/ciklopentan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to consult Qwen Web through an authenticated Cloud Browser as an independent reviewer for questions, documents, and technical analysis while retaining primary responsibility for verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, excerpts, or uploaded files sent to Qwen Web may expose confidential, regulated, proprietary, credential, or personal data.

Mitigation: Send only selected prompts or authorized excerpts, obtain explicit user approval before sensitive transfers, and avoid passwords, OTPs, session tokens, cookies, and private browser data.

Risk: Qwen's review may be incorrect, incomplete, or overconfident.

Mitigation: Treat Qwen output as advisory evidence only, compare it with supplied material and primary sources, and keep final responsibility with the primary agent.

Risk: Browser authentication, CAPTCHA, rate limits, UI changes, or file upload state can block or alter the workflow.

Mitigation: Use secure browser-auth for login, stop at blocking states, inspect the live UI before acting, and verify attachment previews and completed responses before relying on results.

## Reference(s):

- [Qwen Web](https://chat.qwen.ai)
- [ClawHub skill page](https://clawhub.ai/ciklopentan/skills/qwen-web-reviewer-gpt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown synthesis with review findings and provenance notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include the visible Qwen model label, Thinking state, round count, accepted or rejected findings, and uncertainty labels.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
