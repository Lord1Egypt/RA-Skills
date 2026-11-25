## Description:

Provides Chinese astrology and divination queries for BaZi, Zi Wei Dou Shu, Qi Men Dun Jia, Liu Yao, and Da Liu Ren, returning chart and fortune results from Xungu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cnyouker](https://clawhub.ai/user/cnyouker)

### License/Terms of Use:

MIT-0

## Use Case:

External users can request a Chinese astrology chart or reading based on birth details or a selected time, and receive results for BaZi, Zi Wei Dou Shu, Qi Men Dun Jia, Liu Yao, or Da Liu Ren.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scan notes a low-probability least-privilege concern because environment and network capabilities are present while tool scope is not declared.

Mitigation: Review the runtime permissions and restrict environment and network access to what the skill needs.

Risk: Queries send user-provided birth details or selected times to Xungu for chart generation.

Mitigation: Explain the data flow before the first query and avoid sending details the user does not want to share.

## Reference(s):

- [Xungu Agent API reference](https://www.xungufa.com/static/openapi/agent-api.json)
- [Xungu API key settings](https://www.xungufa.com/apikey/)
- [Xungu Query on ClawHub](https://clawhub.ai/cnyouker/skills/xungu-query)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [JSON responses or formatted chart text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chart and fortune details are organized by divination method; interpretations are limited to returned data.]

## Skill Version(s):

1.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
