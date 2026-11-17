## Description:

AI-powered web research assistant that leverages BrowserAct API to supplement restricted web access by searching the internet for additional information. Designed for OpenClaw and Claude Code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phheng](https://clawhub.ai/user/phheng)

### License/Terms of Use:


## Use Case:

Developers and external agent users use this skill to supplement web research when direct browsing is blocked or restricted, producing source-backed research reports from BrowserAct search results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill promotes bypassing paywalls, CAPTCHA challenges, geographic restrictions, and blocked AI access.

Mitigation: Use only for authorized web research, and avoid restricted content unless explicit rights to access it through BrowserAct are confirmed.

Risk: Queries and research topics are sent to BrowserAct.

Mitigation: Do not include sensitive business, incident, legal, credential, or personal data unless sending it to BrowserAct is acceptable.

Risk: Search snippets and generated research summaries may be incomplete or misleading.

Mitigation: Validate important claims against multiple authoritative sources before relying on the report.

## Reference(s):

- [BrowserAct Console integrations](https://www.browseract.com/reception/integrations)
- [BrowserAct MCP endpoint](https://mcp.browseract.com/)
- [ClawHub skill page](https://clawhub.ai/phheng/skills/web-research-assistant)
- [ClawHub publisher profile](https://clawhub.ai/user/phheng)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown research report or JSON search results, with CLI guidance and configuration instructions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write reports to a user-specified output file; requires BrowserAct credentials via environment variable.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
