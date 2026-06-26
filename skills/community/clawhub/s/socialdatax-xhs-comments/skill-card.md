## Description: <br>
Helps agents retrieve and analyze Xiaohongshu / XHS / RedNote comment threads and replies using SocialDataX. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devinchen2014](https://clawhub.ai/user/devinchen2014) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and social media teams use this skill to fetch XHS comment and reply data, then summarize themes, sentiment, objections, FAQs, pain points, and discussion patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents to run SocialDataX CLI commands that use an API key and retrieve external social media comment data. <br>
Mitigation: Review the command, target URL or ID, pagination scope, and API key environment before execution. <br>
Risk: Large pagination options such as --all or multi-page fetching can collect more comments than intended. <br>
Mitigation: Use --max-items or a small --pages value when sampling is sufficient, and confirm broad collection requests before running them. <br>
Risk: Comment analysis may overstate sentiment or themes if based on a single page or empty result set. <br>
Mitigation: Report whether results cover one page or multiple pages and separate observed themes from inferences. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/devinchen2014/socialdatax-xhs-comments) <br>
- [SocialDataX homepage and API access](https://socialdatax.52choujiang.com/?from=clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON data summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SOCIALDATAX_API_KEY and node/npm for direct CLI use. Comment data returned by the CLI is JSON.] <br>

## Skill Version(s): <br>
0.1.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
