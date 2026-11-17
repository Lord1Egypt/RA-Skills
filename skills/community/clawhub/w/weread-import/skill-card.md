## Description:

Exports WeRead highlights and notes to Markdown files for local reading workflows such as Obsidian.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gnixner](https://clawhub.ai/user/gnixner)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to import or synchronize WeRead highlights and notes into local Markdown collections. It supports single-book and bulk exports, re-rendering existing notes, custom frontmatter tags, and incremental merge behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes Markdown files into a user-selected local directory.

Mitigation: Run first against a temporary output directory and review the results before writing to a production notes folder.

Risk: The skill requires WeRead account access through a Gateway API key, browser session, or cookie.

Mitigation: Prefer the default Gateway path or an isolated browser profile, and avoid passing full cookies directly on the command line.

Risk: Legacy profile sync can duplicate broad Chrome cookies and login databases unrelated to WeRead.

Mitigation: Keep the default isolated browser profile and avoid WEREAD_PROFILE_SYNC_MODE=legacy unless the user explicitly needs and understands that behavior.

## Reference(s):

- [WeRead Import ClawHub page](https://clawhub.ai/gnixner/skills/weread-import)
- [WeRead Import workflows](references/workflows.md)
- [WeRead Import design](docs/DESIGN.md)
- [Sample Markdown output](examples/sample-output.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files with YAML frontmatter plus concise command and status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes one Markdown file per exported book and maintains incremental sync state in the selected output directory.]

## Skill Version(s):

0.4.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
