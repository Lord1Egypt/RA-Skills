## Description:

Builds search queries for network asset discovery platforms including FOFA, Quake, ZoomEye, and Shodan for asset, attack-surface, service, and CVE investigation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gandli](https://clawhub.ai/user/gandli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to draft platform-specific FOFA, Quake, ZoomEye, and Shodan queries for authorized network asset discovery, attack surface review, service search, and CVE-oriented investigations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated asset-discovery and vulnerability queries are dual-use and can be misapplied to unauthorized targets.

Mitigation: Run generated queries only for authorized research or assets the user is allowed to investigate.

Risk: Documented installation commands use mutable remote sources.

Mitigation: Verify the repository before installing and pin to a reviewed commit or released version where possible.

Risk: CVE-oriented workflows may depend on live web lookups and external source quality.

Mitigation: Allow live CVE lookups only when appropriate for the environment and prefer official platform, vendor, or vulnerability database sources.

## Reference(s):

- [Space Query Skill on ClawHub](https://clawhub.ai/gandli/skills/space-query-skill)
- [Field Reference](resources/fields.md)
- [FOFA](https://fofa.info)
- [Quake](https://quake.360.net)
- [ZoomEye](https://zoomeye.org)
- [Shodan](https://shodan.io)
- [FOFA Blog](https://en.fofa.info/blog)
- [Quake Blog](https://quake.360.net/blog)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with query code blocks, concise explanations, and suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include platform selection, field logic, additional filters, limitations, and CVE source-checking guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact metadata.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
