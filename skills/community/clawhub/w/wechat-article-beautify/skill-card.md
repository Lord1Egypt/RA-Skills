## Description:

Formats a finished article as WeChat-ready HTML using one or more of seven industry templates, with an optional side-by-side preview.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weikion](https://clawhub.ai/user/weikion)

### License/Terms of Use:

MIT-0

## Use Case:

WeChat article creators and editors use this skill to apply a consistent industry template to a completed article and prepare HTML for pasting into the WeChat editor. They can generate one version or compare several template versions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may automatically install Playwright and Chromium.

Mitigation: Review the installation commands and use a trusted, isolated Python environment before installing dependencies.

Risk: Runtime file access scope is unknown, and some referenced paths were unresolved in the partial scan.

Mitigation: Review referenced files and limit runtime access to the intended input and output locations.

## Reference(s):

- [Template guide](references/template-guide.md)
- [ClawHub skill page](https://clawhub.ai/weikion/skills/wechat-article-beautify)

## Skill Output:

**Output Type(s):** [HTML, Files]

**Output Format:** [HTML with inline styles; optionally multiple template versions and a comparison preview]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reformats the supplied article while preserving its meaning.]

## Skill Version(s):

0.1.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
