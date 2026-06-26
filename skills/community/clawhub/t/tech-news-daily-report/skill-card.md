## Description: <br>
Generates a daily technology news report by searching recent technology and AI news, deduplicating and scoring items, saving a Markdown report, creating a Feishu document, sending it to Feishu, and adding a topic relationship map. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binhuatochina](https://clawhub.ai/user/binhuatochina) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, or individual readers use this skill to assemble daily AI and technology news digests, compare international and China-focused items, and publish the result to local Markdown and Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create local files, create or write Feishu documents, and send reports to a fixed Feishu chat without clear per-run confirmation. <br>
Mitigation: Require a preview and explicit user confirmation of the exact file path, Feishu document location, and chat recipient before writing or sending. <br>
Risk: Hard-coded Feishu identifiers can direct content to an unintended workspace, folder, owner, or group. <br>
Mitigation: Replace hard-coded IDs with user-provided or environment-scoped configuration and verify the destination before each run. <br>


## Reference(s): <br>
- [Feishu document operation reference](references/feishu-doc.md) <br>
- [ClawHub skill page](https://clawhub.ai/binhuatochina/tech-news-daily-report) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, API calls, guidance] <br>
**Output Format:** [Markdown report with scored news entries, source links, topic relationship map, local file path, Feishu document link, and Feishu message content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes memory/YYYY-MM-DD-tech-news.md and a checkpoint JSON; may create or write Feishu documents and send Feishu chat messages when those tools are available.] <br>

## Skill Version(s): <br>
0.3.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
