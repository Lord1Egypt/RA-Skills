## Description: <br>
Generates a daily technology news report from recent AI and tech sources, with deduplication, scoring, local Markdown output, Feishu document creation, and Feishu group delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binhuatochina](https://clawhub.ai/user/binhuatochina) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and teams use this skill to collect recent technology and AI news, deduplicate and score items, and publish a daily report to local Markdown and Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically create Feishu documents and send full reports to a fixed Feishu group. <br>
Mitigation: Before each run, verify the intended chat ID and require manual confirmation before posting externally. <br>
Risk: The skill writes into a Feishu document workspace using configured folder, space, and owner settings. <br>
Mitigation: Verify folder or space tokens and owner settings before enabling document creation. <br>


## Reference(s): <br>
- [Feishu document operation reference](references/feishu-doc.md) <br>
- [ClawHub release page](https://clawhub.ai/binhuatochina/tech-news-daily-cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown report, local Markdown file, Feishu document content, and Feishu message text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes source links, relevance scores, recommendation scores, summary sections, and synchronization records.] <br>

## Skill Version(s): <br>
0.2.4 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
