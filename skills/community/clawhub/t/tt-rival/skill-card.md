## Description:

Retrieves public TikTok keyword search results, creator videos, and video comments as structured JSON for competitor and content analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guaikei](https://clawhub.ai/user/guaikei)

### License/Terms of Use:

MIT

## Use Case:

External creators, marketing teams, and researchers can use the skill to compare public TikTok videos, track creator activity, and review comment themes. Results support competitor monitoring, content research, and audience feedback analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms or TikTok URLs are sent to guaikei.com, and requests use GUAIKEI_API_TOKEN. Security analysis found no clear malicious behavior but had partial coverage for 12 of 34 components.

Mitigation: Review the data sharing terms and token handling before use, and provide the token only in the intended environment.

## Reference(s):

- [TikTok competitor monitoring API](https://www.guaikei.com)
- [Command options](artifact/references/options.md)
- [FAQ](artifact/references/faq.md)
- [ClawHub skill page](https://clawhub.ai/guaikei/skills/tt-rival)

## Skill Output:

**Output Type(s):** [JSON, API Calls]

**Output Format:** [Structured JSON containing request details, status, metadata, and results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public TikTok data; plan limits apply to result counts.]

## Skill Version(s):

1.1.3 (source: evidence.json release, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
