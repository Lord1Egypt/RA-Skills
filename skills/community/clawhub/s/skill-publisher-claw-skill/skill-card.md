## Description:

Prepare Claw skills for public release by auditing security, portability, documentation, testing, git hygiene, and metadata before publication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[acastellana](https://clawhub.ai/user/acastellana)

### License/Terms of Use:

MIT

## Use Case:

Developers and skill publishers use this agent skill to prepare Claw skills for public release by running structured checks, applying common fixes, scaffolding new skill projects, and managing release documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local shell scripts can edit files, initialize git repositories, commit changes, and push to GitHub.

Mitigation: Review the target directory and git status before running publish, fix, or scaffold workflows; avoid --force and --auto unless the resulting changes are expected.

Risk: Secret scans can print matched lines to the terminal or CI logs.

Mitigation: Run scans only in trusted workspaces, redact findings before logging, and patch CI usage to avoid exposing sensitive values.

Risk: External link validation can make network requests to URLs found in skill files.

Mitigation: Skip --external for untrusted skills or run external checks in a network-isolated environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/acastellana/skills/skill-publisher-claw-skill)
- [README](artifact/README.md)
- [Versioning Guide](artifact/docs/versioning.md)
- [Deprecation Process](artifact/docs/deprecation.md)
- [README Quality Guide](artifact/docs/readme-quality.md)
- [GitHub Issues](https://github.com/acastellana/skill-publisher-claw-skill/issues)
- [Claw Docs](https://docs.clawd.bot)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with bash commands, shell scripts, templates, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or run local publishing, auditing, scaffolding, link validation, and git workflow commands when the agent is allowed to execute shell scripts.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
