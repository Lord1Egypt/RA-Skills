## Description:

Queries Umeng mini-program acquisition sources and promotion performance through five read-only umeng-cli OpenAPI calls for channel, campaign, scene, and trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[squall0925](https://clawhub.ai/user/squall0925)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, analytics operators, and growth teams use this skill to inspect Umeng mini-program, H5, and mini-game acquisition rankings, promotion-channel results, campaign results, scene values, and time-series trends. It helps agents choose the correct read-only Umeng endpoint and construct the required umeng-cli command payloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a globally installed umeng-cli and authenticated Umeng credential storage.

Mitigation: Use a pinned, verified npm package version and confirm local credential storage policies before installation or use.

Risk: The skill text requests telemetry calls that can include the application identifier.

Mitigation: Avoid or disable trace commands unless the user explicitly consents, and treat dataSourceId/AppKey values as sensitive application metadata.

Risk: The artifact documents a curl-to-shell installer path.

Mitigation: Prefer the pinned npm installation path over curl-to-shell installation.

## Reference(s):

- [Umeng CLI homepage](https://github.com/umeng/umeng-cli)
- [Umeng web console](https://web.umeng.com)
- [Umeng scene value documentation](https://developer.umeng.com/docs/147615/detail/175369)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces read-only analytics query guidance for authenticated umeng-cli use and requires a mini-program dataSourceId/AppKey for all five business endpoints.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
