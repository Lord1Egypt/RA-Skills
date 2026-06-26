## Description: <br>
Search, score, and submit AI agent tools from SkillsIndex, including MCP servers, Claude skills, GPT actions, and IDE plugins, with security, utility, maintenance, and uniqueness scoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thomasblc](https://clawhub.ai/user/thomasblc) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to discover, compare, inspect, and submit AI agent tools from the SkillsIndex directory. It helps agents retrieve tool details, top-rated listings, and security audit information while optionally submitting new tools or email subscriptions to SkillsIndex. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MCP server runs through npm via npx and makes network requests to SkillsIndex and npmjs.com. <br>
Mitigation: Review the package and be comfortable with npx execution and outbound HTTPS access before installation. <br>
Risk: submit_tool and subscribe can send a repository URL, description, or email address to SkillsIndex. <br>
Mitigation: Review any submit_tool or subscribe action before sending repository details or personal contact information. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/thomasblc/skillsindex-mcp) <br>
- [SkillsIndex Directory](https://skillsindex.dev) <br>
- [SkillsIndex MCP npm Package](https://www.npmjs.com/package/skillsindex-mcp) <br>
- [SkillsIndex Source Repository](https://github.com/thomasblc/skillsindex) <br>
- [SkillsIndex Scoring Methodology](https://skillsindex.dev/methodology/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown and text responses with optional JSON-like tool parameters and MCP configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return search results, tool metadata, security scores, audit notes, submission guidance, and subscription confirmation details from SkillsIndex.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
