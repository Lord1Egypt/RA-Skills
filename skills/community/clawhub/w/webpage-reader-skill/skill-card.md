## Description:

Downloads webpage content with a Google Chrome headless browser and returns the page HTML with a basic summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[24k-handsomer](https://clawhub.ai/user/24k-handsomer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to fetch a supplied webpage URL through headless Chrome, inspect the returned HTML, and receive a short structural summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary URLs with an unsandboxed browser during normal use.

Mitigation: Run it only in an isolated environment with no access to sensitive internal networks, metadata endpoints, or local services.

Risk: The skill may attempt privileged system package installation when Chrome is missing.

Mitigation: Preinstall Chrome through a trusted administrator process and avoid running the skill with sudo-capable privileges.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/24k-handsomer/skills/webpage-reader-skill)
- [Publisher profile](https://clawhub.ai/user/24k-handsomer)
- [Google Chrome](https://www.google.com/chrome/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Python dictionary or command-line text containing success status, message, webpage HTML content, and summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts one URL string and may return full webpage HTML; runtime behavior depends on Chrome availability and network access.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
