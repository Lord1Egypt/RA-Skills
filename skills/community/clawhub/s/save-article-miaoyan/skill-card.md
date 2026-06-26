## Description: <br>
Saves article webpages to Miaoyan by fetching content, generating a brief summary, and writing a Markdown note to the Miaoyan/待学习 folder. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vlalamoon](https://clawhub.ai/user/vlalamoon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users who collect web or WeChat articles use this skill to turn a supplied URL into a local Miaoyan Markdown note with a source link, generated summary, and article body. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic fetching and file creation can process unintended links or create unwanted notes. <br>
Mitigation: Review messages and URLs before enabling automatic triggers, or require user confirmation before running the save workflow. <br>
Risk: URLs or article content may be sent to third-party extraction services such as Jina Reader or Tavily. <br>
Mitigation: Avoid private, authenticated, internal, or sensitive links unless the skill is changed to use a local-only fetch mode or clearly discloses external processing. <br>
Risk: The skill writes Markdown files into an iCloud-synced Miaoyan folder. <br>
Mitigation: Confirm the destination path and sync behavior before installation, and restrict execution to trusted articles and expected local accounts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vlalamoon/save-article-miaoyan) <br>
- [Tavily](https://tavily.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Markdown note files plus command-line status text or trigger JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saved notes include title, save date, source link, generated summary, and article content; long article content may be truncated.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
