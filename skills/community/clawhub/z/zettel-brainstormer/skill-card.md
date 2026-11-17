## Description:

Build structured brainstorming notes from a seed zettel by retrieving linked notes, preprocessing each note with subagents for relevance extraction, drafting with cited evidence, and publishing a natural blog-style post with a final References section.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hxy9243](https://clawhub.ai/user/hxy9243)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and knowledge workers use this skill to turn local Obsidian or Zettelkasten notes into a cited brainstorming draft and publishable Markdown article.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may read Markdown outside the intended notes vault.

Mitigation: Use it only with a trusted notes vault, replace bundled config paths before running, and review candidate note paths before preprocessing.

Risk: The optional zettel-link integration can run an external skill script.

Mitigation: Verify the zettel-link source and local path before allowing the workflow to call its search script.

## Reference(s):

- [Zettel Brainstormer Skill Page](https://clawhub.ai/hxy9243/skills/zettel-brainstormer)
- [Skill Workflow](artifact/SKILL.md)
- [README](artifact/README.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline note citations, a final References section, and optional JSON intermediate packets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local note content and preserves citations to the source notes retained in the final brainstorm.]

## Skill Version(s):

1.1.2 (source: server release metadata and changelog, released 2026-03-25)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
