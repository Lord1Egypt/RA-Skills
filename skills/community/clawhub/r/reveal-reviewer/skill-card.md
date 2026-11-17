## Description:

Review products on Reveal by browsing available tasks, navigating target websites with agent-browser, capturing observations, and submitting structured feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tolulopeayo](https://clawhub.ai/user/tolulopeayo)

### License/Terms of Use:


## Use Case:

External reviewers and agent operators use this skill to complete Reveal product review tasks or proactive self-reviews, capture screenshots and observations, and submit structured findings through the Reveal API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote Reveal task instructions can steer browser actions and screenshot capture.

Mitigation: Use an isolated browser profile with no unrelated logged-in accounts, review task instructions before acting, and confirm screenshots do not contain sensitive information before submission.

Risk: The skill requires access to a Reveal reviewer API key.

Mitigation: Provide the key only through the documented environment variable, avoid exposing it in chat or files, and rotate it if disclosure is suspected.

Risk: Submitted reviews may be incorrect if observations are fabricated or incomplete.

Mitigation: Submit only after actually navigating the product, record completed steps, and confirm with the user before sending the review.

## Reference(s):

- [Reveal Reviewer API Reference](references/api-reference.md)
- [Reveal homepage](https://testreveal.ai)
- [ClawHub skill listing](https://clawhub.ai/tolulopeayo/skills/reveal-reviewer)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown guidance with structured JSON review findings and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include screenshot URLs when supported by the browser tool.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
