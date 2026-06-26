## Description: <br>
Automates Xiaohongshu note publishing from topic or news search through copywriting, cover generation, and posting through a local xiaohongshu-mcp service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaohaojie1](https://clawhub.ai/user/shaohaojie1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, marketers, and operators use this skill to draft Xiaohongshu-style posts, generate text-based cover images, and publish notes after reviewing the content and account state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish to a logged-in Xiaohongshu account through a local service without a clearly required final approval step. <br>
Mitigation: Review the generated title, content, tags, and images, and require explicit final confirmation before every publish action. <br>
Risk: The local xiaohongshu-mcp service depends on a trusted account session and cookie file. <br>
Mitigation: Install only if the service is trusted, keep it stopped except while publishing, and protect or delete the cookie/session file after use. <br>


## Reference(s): <br>
- [Xiaohongshu content template](references/content-template.md) <br>
- [xiaohongshu-mcp configuration](references/mcp-config.md) <br>
- [xiaohongshu-mcp project](https://github.com/xpzouying/xiaohongshu-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python scripts, configuration notes, and JSON publish responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local PNG cover files and submit reviewed content through the configured local Xiaohongshu service.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
