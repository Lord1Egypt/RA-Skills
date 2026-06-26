## Description: <br>
Fetch, update, and summarize Redmine issue attachments from CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinxianwei](https://clawhub.ai/user/yinxianwei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect Redmine issues, apply directed status or note updates, and summarize image attachments through a user-configured model endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Redmine API key and can read or update issue data in the configured Redmine instance. <br>
Mitigation: Use a least-privileged Redmine key and review update commands before running them. <br>
Risk: The image command sends Redmine image attachments and issue context to a user-configured OpenAI-compatible endpoint. <br>
Mitigation: Run the image command only when sharing those attachments and issue details with the configured model provider is acceptable. <br>


## Reference(s): <br>
- [ClawHub redmine-tools release page](https://clawhub.ai/yinxianwei/redmine-tools) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Redmine credentials for all commands; image summarization also requires a user-configured OpenAI-compatible endpoint.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata; artifact frontmatter reports 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
