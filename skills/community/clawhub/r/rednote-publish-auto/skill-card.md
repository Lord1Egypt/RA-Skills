## Description: <br>
RedNote Publish Auto helps an agent draft Xiaohongshu or RedNote posts, generate Markdown card content, render image cards, and publish after user confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hhua007](https://clawhub.ai/user/hhua007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content creators use this skill to turn a topic or source material into RedNote-ready copy, card images, and a confirmed publishing action. Developers can also use its scripts to render Markdown cards and run the posting workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles a reusable Xiaohongshu session cookie that can authorize account actions. <br>
Mitigation: Use a dedicated account, keep the cookie out of shared repositories and remote services, and revoke or rotate the session after use. <br>
Risk: The skill can publish public posts after confirmation. <br>
Mitigation: Review every preview carefully before approving publication and avoid API mode unless the endpoint is local and trusted. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hhua007/rednote-publish-auto) <br>
- [Xiaohongshu website](https://www.xiaohongshu.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions, generated post text, rendered PNG image files, and shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Publishing requires a Xiaohongshu session cookie and explicit user confirmation before posting.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
