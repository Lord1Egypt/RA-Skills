## Description:

Universal Release helps agents prepare releases by detecting common project version files and changelogs, choosing a semantic version bump, and drafting release changes for Node.js, Python, Rust, Claude Plugin, and generic projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoopools](https://clawhub.ai/user/zoopools)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release managers use this skill to guide agents through version detection, changelog generation, release commits, tags, and optional remote publishing across common project types.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can turn a simple push request into release edits, commits, tags, and possible remote publishing.

Mitigation: Review planned file edits, commits, tags, target branch, and push behavior before allowing the agent to proceed.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and release-plan text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or perform local release file edits, commits, tags, and remote pushes when the user approves.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
