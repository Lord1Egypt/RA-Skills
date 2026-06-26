## Description: <br>
Searches Xiaohongshu / XHS / RedNote notes through SocialDataX for keyword research, content planning, competitor analysis, and trend scanning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devinchen2014](https://clawhub.ai/user/devinchen2014) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run read-only Xiaohongshu / XHS / RedNote searches for content research, market observation, competitor analysis, and trend scanning through SocialDataX. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search keywords may be sent to SocialDataX through its API and npm CLI. <br>
Mitigation: Avoid submitting confidential internal terms unless that data sharing is acceptable for the use case. <br>
Risk: The skill fetches an external npm package before running searches. <br>
Mitigation: Review and approve the external package source before installation in controlled environments. <br>
Risk: Returned result URLs may include full query parameters. <br>
Mitigation: Preserve URLs when traceability is required, and handle them as potentially sensitive output. <br>


## Reference(s): <br>
- [SocialDataX API access homepage](https://socialdatax.52choujiang.com/?from=clawhub) <br>
- [ClawHub skill page](https://clawhub.ai/devinchen2014/socialdatax-xhs-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown with CLI commands and summarized search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returned note_url values should be preserved exactly, including query parameters.] <br>

## Skill Version(s): <br>
0.1.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
