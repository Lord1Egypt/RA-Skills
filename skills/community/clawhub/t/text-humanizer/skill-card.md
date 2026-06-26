## Description: <br>
Detects and rewrites AI-style writing patterns in user-provided text while preserving the original meaning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EvoLinkAI](https://clawhub.ai/user/EvoLinkAI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to rewrite pasted text, stdin, or selected local text files so drafts read more naturally while retaining their meaning. It is intended for editing blog posts, emails, essays, reports, and similar human-facing prose. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pasted text, stdin, or selected local files can be sent to Evolink's remote API for processing. <br>
Mitigation: Use the skill only with content approved for upload to Evolink.ai; avoid secrets, private documents, regulated data, source files, and internal drafts unless policy permits that upload. <br>
Risk: The available evidence reports no runtime confirmation step before sending user-provided content to the remote API. <br>
Mitigation: Require an explicit confirmation or opt-in workflow before submitting file, stdin, or pasted content to the API. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/EvoLinkAI/text-humanizer) <br>
- [Evolink API Reference](https://docs.evolink.ai/en/api-manual/language-series/claude/claude-messages-api?utm_source=clawhub&utm_medium=skill&utm_campaign=humanize-text) <br>
- [Evolink](https://evolink.ai?utm_source=clawhub&utm_medium=skill&utm_campaign=humanize-text) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown containing rewritten text and a brief list of changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The shell script truncates submitted content to about 50,000 characters and requests up to 4,096 output tokens from the remote API.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
