## Description:

Creates or updates STYLE_MANIFESTO persona source code that defines a persona's identity, cognition, behavior, and linguistic style.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ar3ss12](https://clawhub.ai/user/ar3ss12)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to research and synthesize structured persona manifests for content-engine or character-style workflows. It is suited to creating STYLE_MANIFESTO.md deliverables for fictional, historical, or user-provided persona targets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persona research can produce sensitive psychological or diagnosis-like claims, especially for private or living people.

Mitigation: Use consent-aware targets, verify sources carefully, and treat psychological claims as untrusted speculation unless directly supported by reliable evidence.

Risk: The helper script uses the supplied persona name in an output path.

Mitigation: Constrain persona names to safe path characters before running the helper script.

Risk: Personal mode depends on private knowledge-base material.

Mitigation: Keep private inputs out of shared artifacts; the artifact gitignore excludes persona knowledge bases and private persona folders.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ar3ss12/skills/soul-architect-v1)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown persona manifesto with optional shell command output and status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create persona files under personas/<name>; personal mode expects a local knowledge_base.json input.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
