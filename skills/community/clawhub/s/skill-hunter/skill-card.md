## Description:

Find, evaluate, and install ClawHub skills. Semantic search across 10,000+ skills, security vetting before install, side-by-side comparison. The skill that makes skills useful.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenoodl-synthesis](https://clawhub.ai/user/kenoodl-synthesis)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use Skill Hunter to discover ClawHub skills, inspect candidate skill files, compare options, and manage user-directed installs, updates, and removals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent queries ClawHub public endpoints during search, browsing, metadata lookup, and remote file inspection.

Mitigation: Use the skill only when ClawHub public API queries are acceptable for the task, and avoid placing sensitive information in search terms.

Risk: The skill helps run install, update, and uninstall commands for ClawHub skills selected by the user.

Mitigation: Inspect candidate skill files and security profile before installation, then run only explicit ClawHub management commands for skills you intend to trust.

## Reference(s):

- [Skill Hunter on ClawHub](https://clawhub.ai/kenoodl-synthesis/skills/skill-hunter)
- [Publisher Profile](https://clawhub.ai/user/kenoodl-synthesis)
- [Skill Hunter Full Workflow](artifact/instructions.md)
- [ClawHub Public API Base](https://clawhub.ai)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Markdown]

**Output Format:** [Markdown with inline bash commands and API response inspection examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public ClawHub endpoints and produces human-readable search, vetting, comparison, and install guidance.]

## Skill Version(s):

1.0.6 (source: claw.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
