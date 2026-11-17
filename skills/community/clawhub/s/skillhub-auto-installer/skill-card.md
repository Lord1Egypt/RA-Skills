## Description:

Searches the Skillhub marketplace for available skills and returns results for an agent to present, while the package also includes auxiliary install and security-check scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiayao0810](https://clawhub.ai/user/jiayao0810)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to discover Skillhub skills by keyword and review candidates before deciding whether to install them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary says the skill presents itself as search-only while the package also contains scripts that can install remote skills and inspect local skill directories.

Mitigation: Treat the release as an installer and security-checking utility; review scripts before use and run only the search script when read-only behavior is required.

Risk: The server security guidance warns that installer scripts can copy third-party skills into the active agent environment using unpinned npm tooling.

Mitigation: Avoid running installer scripts unless the target skill and npx package source have been independently reviewed and trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiayao0810/skills/skillhub-auto-installer)
- [Skillhub Auto-Finder + SkillSentry integration guide](references/security-integration.md)
- [Skillhub API endpoint](https://skills.volces.com/v1)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Text and Markdown with shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search requires Node.js, npx, network access to Skillhub, and the skills npm package invoked through npx.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
