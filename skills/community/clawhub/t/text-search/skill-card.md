## Description:

Search for a text pattern in files within a directory and show matching lines with filenames and line numbers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinwangmok](https://clawhub.ai/user/jinwangmok)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other workspace users use this skill to locate words, phrases, or patterns across files in a target directory and inspect the matching file paths, line numbers, and lines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The search reads files under the user-selected directory and can display sensitive matching lines.

Mitigation: Search only intended directories and review results before sharing them outside the workspace.

Risk: Search patterns beginning with '-' may be interpreted as grep options by the current wrapper.

Mitigation: Avoid untrusted patterns that begin with '-' unless the wrapper is updated to pass '--' before the pattern.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jinwangmok/skills/text-search)
- [Publisher profile](https://clawhub.ai/user/jinwangmok)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text search results with filename, line number, and matching line]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses grep recursively; no matches are reported as a normal outcome.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
