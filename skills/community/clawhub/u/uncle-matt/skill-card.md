## Description:

Uncle Matt is an OpenClaw security skill that lets agents use approved API actions through a hardened local Broker without seeing secrets, calling arbitrary URLs, or becoming an open proxy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uncmatteth](https://clawhub.ai/user/uncmatteth)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use Uncle Matt to route approved external API actions through a local Broker that keeps secrets out of the agent context and blocks arbitrary URL calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation depends on unpinned external installer scripts and a Docker build that were not included in the reviewed artifact.

Mitigation: Review the external repository at a pinned commit before installing, inspect installer scripts and Docker configuration, and prefer checksum or signature verification.

Risk: The skill package does not include the Broker or installer scripts required for the advertised action tool to work.

Mitigation: Do not treat the artifact alone as a complete installation; validate the full Broker setup and action configuration before enabling the skill.

Risk: Optional voice packs use a rude refusal style that may be unsuitable for some users or organizations.

Mitigation: Keep voice packs disabled unless that tone is explicitly acceptable for the deployment context.

Risk: Misconfigured actions could weaken the intended no-secrets and no-arbitrary-URL boundary.

Mitigation: Keep the Broker on loopback, avoid secrets in JSON config, restrict actions to approved host and path pairs, and validate action configuration before restart.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/uncmatteth/skills/uncle-matt)
- [Project homepage](https://bobsturtletank.fun)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline JSON and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional voice-pack lines may prefix refusal or warning responses only when enabled.]

## Skill Version(s):

5.420.70 (source: server release metadata; artifact frontmatter reports 6.420.69)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
