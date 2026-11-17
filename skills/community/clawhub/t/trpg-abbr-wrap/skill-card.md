## Description:

Wraps English abbreviations in TRPG rulebooks, scenarios, character sheets, and related files into Chinese full-term plus abbreviation format for clearer player and GM reading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ice26985850](https://clawhub.ai/user/ice26985850)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, developers, and game editors use this skill before release to normalize TRPG terminology in Markdown, text, and Excel materials while avoiding double-wrapping existing abbreviations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect project-specific abbreviation mappings can rewrite TRPG terminology with the wrong Chinese full terms.

Mitigation: Scan the target files first, confirm the abbreviation-to-full-name mapping for the project, and review representative edits before publishing.

Risk: The skill intentionally rewrites Markdown, text, and Excel files, so broad runs can change source materials unexpectedly.

Mitigation: Limit runs to user-selected files, skip old or draft files unless requested, and review file diffs before release.

Risk: Poor replacement ordering can double-wrap already-correct abbreviations.

Mitigation: Use idempotent replacement patterns and rerun validation until repeat execution reports no further changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ice26985850/skills/trpg-abbr-wrap)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with Python code blocks and checklist items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces document-editing guidance for .md, .txt, and .xlsx files; mappings are project-specific.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
