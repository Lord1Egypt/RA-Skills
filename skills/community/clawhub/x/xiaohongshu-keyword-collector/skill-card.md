## Description:

Automatically accesses Xiaohongshu's Explore page via browser automation, inputs keywords into the search bar, and collects the list of related keywords from the auto-suggest dropdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content teams use this skill to collect Xiaohongshu search suggestions for keyword research, trending topic discovery, SEO planning, and competitor keyword mining.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Entered keywords are sent to Xiaohongshu through a browser session.

Mitigation: Avoid confidential product plans, client names, investigations, or other sensitive terms when collecting suggestions.

Risk: Login state, captchas, site tracking, or anti-crawling controls may affect collection.

Mitigation: Have the user handle login or captcha challenges manually and stop collection when the site restricts access.

## Reference(s):

- [Xiaohongshu Explore](https://www.xiaohongshu.com/explore)
- [ClawHub skill page](https://clawhub.ai/openlark/skills/xiaohongshu-keyword-collector)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown keyword lists grouped by input keyword]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on Xiaohongshu page behavior, login state, captchas, and suggestion availability.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
