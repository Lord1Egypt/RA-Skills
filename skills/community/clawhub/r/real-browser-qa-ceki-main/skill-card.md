## Description:

QA and security testing via real Chrome browser sessions for realistic user simulation, vulnerability discovery, and cross-browser inconsistency detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iwedmak](https://clawhub.ai/user/iwedmak)

### License/Terms of Use:

MIT

## Use Case:

Developers, QA engineers, and security testers use this skill to drive real Chrome sessions against sites they own or are explicitly authorized to test. It helps surface rendering, timing, validation, accessibility, and security issues that headless browser automation can miss.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real-browser marketplace sessions can expose credentials, production data, internal systems, payments, or private content to the session host.

Mitigation: Avoid marketplace mode for sensitive workflows; prefer self mode or non-sensitive test accounts and data.

Risk: Browser automation can be misused on sites without authorization or outside allowed terms.

Mitigation: Constrain use to owned or explicitly authorized sites and review each planned session before execution.

Risk: Unpinned SDK installation and exported browser profiles can create supply-chain or sensitive-session exposure.

Mitigation: Use a pinned SDK version in a virtual environment and keep exported browser profiles private and encrypted, or avoid exporting them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/iwedmak/skills/real-browser-qa-ceki-main)
- [README](README.md)
- [Agent Skill Instructions](SKILL.md)
- [Ceki SDK on PyPI](https://pypi.org/project/ceki-sdk/)
- [Ceki Extension Install](https://browser.ceki.me/install)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Markdown]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and Python or TypeScript code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended to guide controlled real-browser QA sessions and should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
