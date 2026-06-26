## Description: <br>
Monitor blogs and RSS feeds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to monitor RSS feeds and blogs, fetch web content, and receive summarized guidance or responses based on feed activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives the agent broad command and file tool authority without explaining why that authority is needed. <br>
Mitigation: Review each proposed command, file read, or file write before execution and allow it only when the agent gives a clear, task-specific reason. <br>
Risk: Broad blog or RSS monitoring tasks can fetch unexpected web content or follow ambiguous sources. <br>
Mitigation: Prefer explicit RSS or feed URLs and restrict monitoring to sources the user has identified. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/terrycarter1985/tc-blogwatcher) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with plain-text guidance and optional command proposals] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use web search, web fetch, file reads, file writes, and shell command proposals when the agent determines they are relevant.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
