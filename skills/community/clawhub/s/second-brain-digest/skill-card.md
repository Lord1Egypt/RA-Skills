## Description:

second-brain-digest is a Chinese-language workflow that turns fragmented articles, notes, conversations, and ideas into structured atomic knowledge cards and identifies links to an existing personal knowledge base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boboy-j](https://clawhub.ai/user/boboy-j)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese-speaking personal knowledge management users and note-taking agents use this skill to digest articles, notes, screenshots, conversations, meeting records, research data, and idea fragments into reusable atomic cards. It also suggests relationships, follow-up questions, action cues, and storage formats for second-brain workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation wording may cause the workflow to process pasted content when the user only wanted a simple summary or storage suggestion.

Mitigation: Confirm the intended note-taking outcome before converting ambiguous user input into knowledge cards.

Risk: Generated cards can misstate or over-strengthen claims from the source content.

Mitigation: Review card titles, evidence, strength labels, and source attribution against the original material before saving them to a knowledge base.

Risk: The README includes an unpinned npx install command.

Mitigation: Use a trusted or pinned installer path when installing the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/boboy-j/skills/second-brain-digest)
- [Card templates and format reference](artifact/references/card-templates.md)
- [Example article digest](artifact/examples/example-article-digest.md)
- [Test cases](artifact/tests/test-cases.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Chinese Markdown knowledge cards with optional Obsidian Markdown or Notion-ready fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include card titles, core content, source, tags, strength labels, related-knowledge links, follow-up questions, optional action cues, and storage suggestions.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
