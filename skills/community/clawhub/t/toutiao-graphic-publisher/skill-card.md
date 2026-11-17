## Description:

Automatically publishes graphic content on Toutiao through browser automation, supporting intelligent formatting, automatic generation of popular tags, and tag activation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and content operators use this skill to format, tag, preview, and publish graphic articles to a Toutiao account through browser automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish public Toutiao articles from a logged-in account after changing formatting and tags.

Mitigation: Require the agent to stop at preview and get explicit approval of the account, title, final body text, and tags before it clicks Confirm Publish.

Risk: Automated formatting and tag generation can change how the article is presented to readers.

Mitigation: Review the previewed article formatting and tag list before approving publication.

Risk: The workflow depends on the active Toutiao login session and may act on the currently logged-in account.

Mitigation: Confirm the intended Toutiao account after QR-code login or session reuse before allowing publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/openlark/skills/toutiao-graphic-publisher)
- [OpenLark publisher profile](https://clawhub.ai/user/openlark)
- [Toutiao creator center](https://mp.toutiao.com/profile_v4/index)
- [Toutiao graphic publishing page](https://mp.toutiao.com/profile_v4/graphic/publish)

## Skill Output:

**Output Type(s):** [Text, Markdown, Browser automation actions, Guidance]

**Output Format:** [Formatted article text, generated tags, and browser interaction guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use a logged-in Toutiao browser session; the agent should stop at preview for explicit user approval before final publishing.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
