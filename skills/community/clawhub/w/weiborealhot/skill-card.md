## Description:

Retrieves current Weibo hot-search topics across real-time, lifestyle, entertainment, and social categories using browser automation.

This skill is for research and development only.

## Publisher:

[miaoxingjun](https://clawhub.ai/user/miaoxingjun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to retrieve Weibo hot-search entries for non-production trend monitoring, public-opinion review, and lightweight topic discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can navigate a browser to an arbitrary URL through its custom URL option.

Mitigation: Use only fixed Weibo category URLs and restrict navigation to approved Weibo hosts before deployment.

Risk: The browser configuration disables sandboxing in some environments.

Mitigation: Run the skill in an isolated environment and avoid disabling browser sandboxing during normal use.

Risk: The artifact includes anti-detection and proxy guidance that can increase misuse and compliance risk.

Mitigation: Remove anti-detection and proxy guidance, and review acceptable-use requirements before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/miaoxingjun/skills/weiborealhot)
- [Weibo hot-search page](https://s.weibo.com/top/summary)
- [Selenium documentation](https://www.selenium.dev/documentation/)

## Skill Output:

**Output Type(s):** [Text, JSON, Code, Shell commands, Guidance]

**Output Format:** [JSON data or human-readable text, with optional Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a status code, message, and a list of hot-search entries with title and heat value when successful.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
