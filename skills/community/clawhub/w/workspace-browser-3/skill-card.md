## Description:

Browse and search workspace files with syntax-highlighted code and AI-generated explanations saved persistently in SQLite.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coopeter](https://clawhub.ai/user/coopeter)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this release to browse, search, and inspect files in a workspace, view syntax-highlighted source, and create or store code explanations. It is intended for trusted local or controlled workspace review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The service can expose workspace files through an unauthenticated network interface.

Mitigation: Run only in a trusted, isolated environment, bind to localhost, and add authentication before broader access.

Risk: Wildcard CORS can allow unintended browser origins to interact with the service.

Mitigation: Remove wildcard CORS and restrict allowed origins to trusted local or organizational clients.

Risk: Code content may be sent to DeepSeek when AI explanations are generated.

Mitigation: Avoid AI explanations for sensitive files unless external processing is acceptable, and review provider configuration before use.

Risk: Rendered explanations may include unsafe or misleading content.

Mitigation: Sanitize rendered explanations and review generated guidance before relying on it.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/coopeter/skills/workspace-browser-3)
- [Artifact README](artifact/README.md)
- [Artifact skill description](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Browser UI and JSON API responses with Markdown-formatted code explanations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [SQLite persistence for saved file explanations; no special post-processing required.]

## Skill Version(s):

3.0.0 (source: server release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
