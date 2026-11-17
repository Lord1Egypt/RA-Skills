## Description:

Shorten URLs from terminal with custom slugs, local storage, and basic analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[derick001](https://clawhub.ai/user/derick001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and command-line users use this skill to shorten, expand, search, manage, import, export, and clean up locally stored URL mappings without relying on an external shortening service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URL history is stored in plaintext under the user's home directory.

Mitigation: Avoid storing secrets in URLs and use only on systems where local plaintext URL history is acceptable.

Risk: Import, overwrite, force delete, and cleanup commands can change or remove local mappings.

Mitigation: Back up mappings before import or cleanup, prefer cleanup with --dry-run first, and review destructive flags before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/derick001/skills/url-shortener-cli)
- [Publisher profile](https://clawhub.ai/user/derick001)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration]

**Output Format:** [Terminal text and optional JSON output from CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local URL mapping data under ~/.url-shortener/mappings.json.]

## Skill Version(s):

1.0.0 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
