## Description:

Reads WeChat Official Account article pages from provided mp.weixin.qq.com links and extracts the article title and body text for quotation, title extraction, or summarization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuyunting555](https://clawhub.ai/user/wuyunting555)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they need an agent to open a WeChat Official Account article link, extract the page title and body text, and return concise excerpts or summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can navigate a browser to arbitrary URLs if input is not constrained.

Mitigation: Run it only on trusted https://mp.weixin.qq.com article links and add URL validation plus redirect blocking for private or local network destinations before broad deployment.

Risk: The skill installs npm dependencies and Chromium at runtime.

Mitigation: Perform dependency and browser installation in an explicit reviewed setup step, then run extraction only after the installed components have been approved.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands]

**Output Format:** [JSON extraction results with concise Markdown reporting]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Extractor output includes title and bodyText, with bodyText capped at 20000 characters by the artifact script.]

## Skill Version(s):

0.1.2 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
