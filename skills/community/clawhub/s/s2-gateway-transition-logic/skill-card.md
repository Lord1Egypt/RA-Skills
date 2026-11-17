## Description:

Instructs the indoor SSSU agent to act as the Spatial Gatekeeper. Evaluates transit requests using the S2_BMS_VAULT_TOKENS secure environment variable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spacesq](https://clawhub.ai/user/spacesq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and building automation operators use this skill with OpenClaw agents to evaluate inbound and outbound gateway transit requests, return advisory ACS commands, and keep final physical relay execution in the isolated hardware layer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inbound access can be approved without a valid token when the caller claims to be a silicon agent.

Mitigation: Do not connect this skill to trusted BMS or access-control workflows until every permitted inbound path requires verified credentials.

Risk: The advisory output may be mistaken for an authorization decision suitable for direct physical relay control.

Mitigation: Keep physical ACS relay execution isolated and require independent review before any hardware integration trusts this advisory output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spacesq/skills/s2-gateway-transition-logic)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Text]

**Output Format:** [Markdown instructions and JSON tool-call results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires S2_BMS_VAULT_TOKENS; physical ACS relay execution remains outside the skill.]

## Skill Version(s):

1.4.2 (source: server release, SKILL.md frontmatter, package.json, openclaw.plugin.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
