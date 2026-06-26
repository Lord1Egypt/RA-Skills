## Description: <br>
A Chinese-language workflow that turns fragmented inputs such as articles, notes, screenshot text, conversation records, and ideas into standardized atomic knowledge cards with relationship discovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[boboy-j](https://clawhub.ai/user/boboy-j) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and knowledge workers use this skill to digest articles, notes, meeting records, data snippets, and personal ideas into reusable personal-knowledge-management cards. It helps structure each card with a claim, rationale, source, tags, confidence strength, related concepts, optional action cues, and storage suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private meetings, notes, conversations, or personal ideas may contain sensitive information that should not be saved without review. <br>
Mitigation: Review generated cards before storing or sharing them, especially when the input includes private or personal content. <br>
Risk: The skill uses broad trigger language and may produce knowledge-card formatting when the user only wants a plain summary. <br>
Mitigation: Ask for plain summary output when card formatting, relationship discovery, or storage suggestions are not desired. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/boboy-j/second-brain-digest) <br>
- [Publisher profile](https://clawhub.ai/user/boboy-j) <br>
- [Card templates and format reference](artifact/references/card-templates.md) <br>
- [Example article digest](artifact/examples/example-article-digest.md) <br>
- [Test cases](artifact/tests/test-cases.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or structured text knowledge cards] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce standard card format, Obsidian Markdown with frontmatter, or Notion database field guidance when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
