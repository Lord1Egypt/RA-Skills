## Description: <br>
Summarizes a Xiaohongshu/Rednote post and representative comments into a Chinese report covering the main post content and comment sentiment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiwei26](https://clawhub.ai/user/xiwei26) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to analyze a Rednote post URL by collecting the main post text and representative comments, then producing a concise Chinese summary of the content and audience reaction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may require an authenticated browser session to access complete Rednote post and comment content. <br>
Mitigation: Use only an intended account session, avoid sharing cookies or credentials, and pause for user login when manual authentication is required. <br>
Risk: Summaries can be incomplete if comments fail to load or only a limited set of representative comments is available. <br>
Mitigation: Ask the browser agent to load more comments when needed and treat the resulting report as a synthesis of the visible content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiwei26/rednote-summarize) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report in Chinese] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes separate sections for the main post summary and comment summary.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
