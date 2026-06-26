## Description: <br>
Monitor blogs and RSS feeds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to monitor blogs and RSS feeds and receive agent guidance for feed-related workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill advertises broad tool use, including shell commands and local file reads or writes. <br>
Mitigation: Use explicit feed URLs and require user confirmation before running shell commands or writing local files. <br>
Risk: The artifact notes that the skill requires integration with a Blog Watcher service or application. <br>
Mitigation: Confirm the intended Blog Watcher integration and access configuration before relying on monitoring results. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/terrycarter1985/terry-blogwatcher) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional command suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May fetch web content and propose local file operations when the host agent grants those tools.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
