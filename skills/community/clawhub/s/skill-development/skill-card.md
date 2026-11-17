## Description:

Generate Skill skeleton code, SKILL.md, and reference materials following best practices

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to create or improve agent skills, including drafting SKILL.md, organizing reference materials, generating optional code skeletons, and checking quality.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated local files could overwrite existing skill work if paths are not checked.

Mitigation: Confirm output paths before writing files and avoid overwriting existing work unless the user explicitly requests it.

Risk: Generated trigger descriptions may be too broad and cause an agent to invoke the skill in unrelated contexts.

Mitigation: Review and narrow trigger wording before publishing or installing the generated skill.

Risk: When a code-hosting connector is available, generated changes may be prepared for a pull request.

Mitigation: Review generated diffs, reference files, and PR content before merging or release.

## Reference(s):

- [Skill Quality Checklist](references/skill-checklist.md)
- [SKILL.md Standard Template](references/skill-template.md)
- [ClawHub Skill Page](https://clawhub.ai/bettermen/skills/skill-development)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with optional code blocks, directory trees, generated SKILL.md content, reference-file content, and review tables.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local file paths, quality checklists, and PR-ready generated skill files when a code-hosting connector is available.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
