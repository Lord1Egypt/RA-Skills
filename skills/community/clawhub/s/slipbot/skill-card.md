## Description: <br>
Used to capture and organize notes, ideas, quotes, and journal entries with automatic tagging, linking, and knowledge graph maintenance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jrswab](https://clawhub.ai/user/jrswab) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Individuals and knowledge workers use SlipBot to capture prefixed notes, ideas, quotes, and journal entries into a local slipbox, then maintain tags, links, and a JSON graph index for later retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Messages that begin with SlipBot shorthand prefixes may be captured unintentionally into the local slipbox. <br>
Mitigation: Avoid starting sensitive or unrelated chat messages with those prefixes, and review the slipbox after pasting Markdown lists or quoted text. <br>
Risk: The skill writes and updates local note files, metadata, and graph index entries. <br>
Mitigation: Install only when local slipbox file updates are desired and review generated notes and links before relying on them. <br>


## Reference(s): <br>
- [SlipBot on ClawHub](https://clawhub.ai/jrswab/slipbot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Concise text responses plus Markdown note files with YAML frontmatter and JSON graph index updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes and updates files under a local slipbox directory when documented note prefixes are used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
