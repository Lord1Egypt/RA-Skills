## Description:

Generate and restore ThinkPHP UI components using this project's existing conventions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cnoder-wgh](https://clawhub.ai/user/cnoder-wgh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to create or restore ThinkPHP template UI components, matching nearby project structure, styles, mock data, and controller assignments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Template, CSS, mock data, or controller assignment edits can change rendered ThinkPHP pages in unintended ways.

Mitigation: Review generated diffs against nearby components and run the relevant page or test flow before deployment.

Risk: Missing field guards in restored templates can cause undefined index or rendering issues.

Mitigation: Use ThinkPHP default filters and conditional checks for optional fields, then verify pages with representative mock data.

## Reference(s):


## Skill Output:

**Output Type(s):** [code, configuration, shell commands, guidance]

**Output Format:** [Markdown with code snippets, file edits, and command suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ThinkPHP template changes, CSS updates, mock data, and controller or view assignment guidance.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
