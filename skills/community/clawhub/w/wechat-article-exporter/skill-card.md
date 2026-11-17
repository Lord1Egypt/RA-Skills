## Description:

Exports WeChat public-account articles from mp.weixin.qq.com URLs as long screenshots while handling lazy-loaded images, video placeholders, and bottom toolbar obstruction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[benzking](https://clawhub.ai/user/benzking)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content operators, and external users can use this skill to preserve WeChat public-account articles as image/PDF exports from mp.weixin.qq.com links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill weakens browser protections and uses automation-evasion settings while loading remote WeChat pages.

Mitigation: Review before installing and run only in a low-privilege, disposable environment with restricted network access.

Risk: Browser automation against remote article pages can increase host exposure if secrets or existing browser profiles are mounted.

Mitigation: Run without mounted secrets or browser profiles and use only WeChat article URLs the operator intends to export.

Risk: Long-page screenshot stitching and PDF conversion can consume memory, disk, and runtime.

Mitigation: Apply memory, disk, and runtime limits to the execution environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/benzking/skills/wechat-article-exporter)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Markdown guidance with a bash command; generated PNG/PDF files and console status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates per-article output directories using the detected article title.]

## Skill Version(s):

3.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
