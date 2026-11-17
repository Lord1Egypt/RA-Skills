## Description:

Queries vehicle restriction information for Chinese cities, including license plate tail-number rules, restricted areas, restriction times, and penalty standards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[workxin](https://clawhub.ai/user/workxin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve city vehicle restriction rules from TianAPI by city name or city code, then present the returned restrictions in a clear response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill needs access to a TianAPI key to perform vehicle-limit lookups.

Mitigation: Store TIANAPI_VEHICLELIMIT_KEY in a protected environment or secret manager, keep scripts/.env private, and avoid passing real keys on the command line.

Risk: API key exposure or overuse could create account or billing impact.

Mitigation: Use a dedicated TianAPI key with usage limits where possible and rotate it if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/workxin/skills/tianapi-vehiclelimit)
- [TianAPI vehiclelimit API](https://www.tianapi.com/apiview/246)
- [TianAPI vehiclelimit endpoint](https://apis.tianapi.com/vehiclelimit/index)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a TianAPI key supplied through TIANAPI_VEHICLELIMIT_KEY, a private scripts/.env file, or the --key argument.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
