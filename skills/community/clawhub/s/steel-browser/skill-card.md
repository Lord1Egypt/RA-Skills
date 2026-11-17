## Description:

Control Steel.dev cloud browser sessions with Playwright-based scripts for navigation, form filling, clicking, screenshots, content extraction, JavaScript evaluation, proxies, and CAPTCHA solving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eyhn](https://clawhub.ai/user/eyhn)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to drive cloud browser sessions for web automation, scraping, form filling, visual inspection, and browser-use agent loops.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted helper arguments could cause local Python code execution through heredoc argument interpolation.

Mitigation: Review or fix heredoc argument handling before installation, and avoid passing selectors, URLs, text, output paths, or JavaScript from untrusted webpages.

Risk: Browser automation may interact with sensitive logged-in sessions or expose session state.

Mitigation: Run in an isolated environment, avoid sensitive accounts, and protect or remove ~/.steel_state after use.

Risk: The skill depends on external Steel and Playwright packages and a Steel API key.

Mitigation: Pin dependencies and provide STEEL_API_KEY through a protected environment or agent configuration store.

## Reference(s):

- [Steel.dev](https://steel.dev)
- [Steel App API Keys](https://app.steel.dev)

## Skill Output:

**Output Type(s):** [Shell commands, Text, Files, Configuration]

**Output Format:** [Shell command outputs, page text, URLs, session identifiers, and screenshot files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires STEEL_API_KEY and may persist a Steel session identifier in ~/.steel_state until release or timeout.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
