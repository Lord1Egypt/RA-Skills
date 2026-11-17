## Description:

Manages a lightweight wiki keyword index in a single JSON file with core, buffer, and new pools to keep local keyword knowledge searchable and bounded.

This skill is ready for commercial/non-commercial use.

## Publisher:

[markma84](https://clawhub.ai/user/markma84)

### License/Terms of Use:

MIT-0

## Use Case:

Agents or developers use this skill to maintain a local Chinese-language wiki keyword index, including lookup, entry creation, pool promotion and demotion, pruning, and backup routines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local wiki index can expose private definitions or referenced memory/source paths if wiki/wiki.json is shared or loaded without review.

Mitigation: Keep control of wiki/wiki.json and review referenced memory or source paths before loading private details.

Risk: Manual edits or backup restoration can corrupt or replace the active index.

Mitigation: Validate wiki/wiki.json as JSON before use and validate wiki.json.bak before restoring it.

Risk: The workflow is primarily documented in Chinese, which can reduce usability for readers who do not read Chinese.

Mitigation: Install only when a Chinese-language local wiki index workflow is appropriate for the agent or team.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/markma84/skills/wiki-manager)
- [Design note](artifact/DESIGN.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON]

**Output Format:** [Markdown with JSON examples and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local index-management procedures for a wiki/wiki.json file capped at 500 entries.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
