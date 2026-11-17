## Description:

Use this skill when a user wants a trust decision before installing from a skill URL, marketplace, or GitHub repo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[likw99](https://clawhub.ai/user/likw99)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and users use TrustSkills to make a quick source-provenance decision before installing a skill from a URL, marketplace, or GitHub repository. It helps distinguish vendor-owned sources, official discovery indexes, and unsupported or unverified third-party sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Trusted result is a provenance signal, not proof that a specific skill version is safe, unchanged, signed, or malware-free.

Mitigation: Review and scan the artifact itself before installing anything with meaningful access.

Risk: The skill uses a compact allowlist and may not cover every legitimate distribution channel.

Mitigation: Treat unsupported sources as not trusted under this policy until their publisher or distribution root can be verified separately.

## Reference(s):

- [TrustSkills ClawHub Skill Page](https://clawhub.ai/likw99/skills/trustskills)
- [Publisher Profile](https://clawhub.ai/user/likw99)
- [Official Distribution](https://trustskills.app/SKILL.md)

## Skill Output:

**Output Type(s):** [guidance, markdown]

**Output Format:** [Markdown decision summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a decision-oriented trust verdict with source, rationale, safest known install path, and remaining risk when useful.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
