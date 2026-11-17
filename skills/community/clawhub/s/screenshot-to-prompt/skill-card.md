## Description:

Screenshot To Prompt helps agents analyze UI screenshots, extract page structure, states, text, and interactions, and produce implementation prompts for coding agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[z-zihan](https://clawhub.ai/user/z-zihan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn UI screenshots into structured page analysis and ready-to-send prompts for coding agents when building or recreating page layouts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Screenshots may contain private UI text, internal product details, or sensitive interface data that can be reproduced in generated prompts.

Mitigation: Review and redact screenshots and generated prompts before sending them onward.

Risk: Low-quality or ambiguous screenshots can lead to uncertain page-structure analysis or misleading implementation guidance.

Mitigation: Use clearer screenshots when possible and verify any sections the skill marks as uncertain before implementation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/z-zihan/skills/screenshot-to-prompt)
- [Project homepage](https://github.com/z-Zihan/awesome-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown response with structured screenshot analysis and a copyable coding-agent prompt]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Language follows the user's language; the skill guides prompt generation and does not produce code unless the user explicitly asks.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
