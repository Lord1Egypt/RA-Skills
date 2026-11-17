## Description:

Convert URL to PNG suitable for mobile reading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guoqiao](https://clawhub.ai/user/guoqiao)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to capture a supplied web page as a mobile-width PNG screenshot for easier reading and sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can render arbitrary supplied URLs from the user's machine, which may expose internal-network content in generated screenshots.

Mitigation: Use it only with trusted public URLs, preferably from a sandbox or container with restricted network access.

Risk: The screenshot workflow depends on shot-scraper and Chromium components installed at runtime.

Mitigation: Pin shot-scraper and Chromium dependencies before deployment and review the installation path before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/guoqiao/skills/url2png)
- [ClawHub Homepage Metadata](https://clawhub.ai/guoqiao/url2png)
- [URL to PNG Examples](https://github.com/guoqiao/skills/tree/main/url2png/examples)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [PNG file with concise agent-facing delivery guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a mobile-width Chromium screenshot workflow and defaults to saving generated PNG files under ~/Pictures when no output path is supplied.]

## Skill Version(s):

0.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
