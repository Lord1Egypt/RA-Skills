## Description:

Uses Yutori Research and Browsing APIs to research topics, collect sources, navigate sites, and extract structured facts from the web when Yutori endpoints and API credentials are available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juanpin](https://clawhub.ai/user/juanpin)

### License/Terms of Use:


## Use Case:

Developers and agents with Yutori API access use this skill to delegate web research and cloud browsing tasks, then return briefs, reading lists, extracted facts, and source URLs to users.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send research prompts, browsed URLs, and the Yutori API key to the endpoint configured in YUTORI_API_BASE.

Mitigation: Set YUTORI_API_BASE only to an official HTTPS Yutori endpoint and avoid confidential or internal URLs unless approved.

Risk: The security evidence marks the release suspicious because endpoint configuration can redirect sensitive requests.

Mitigation: Review the script before installation and consider hardening it to allowlist Yutori origins before sending credentials.

## Reference(s):

- [Yutori website](https://yutori.com)
- [Yutori production API endpoint](https://api.yutori.com)
- [Yutori development API endpoint](https://api.dev.yutori.com)
- [ClawHub skill page](https://clawhub.ai/juanpin/skills/yutori-web-research)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown bullets with source URLs and optional shell or curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires YUTORI_API_KEY and may use YUTORI_API_BASE to choose the Yutori endpoint.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
