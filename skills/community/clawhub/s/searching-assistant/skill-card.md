## Description: <br>
Searching Assistant coordinates search work by breaking a request into independent sub-tasks and assigning them to General_Search_Agent and other suitable search agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[urrrich0](https://clawhub.ai/user/urrrich0) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Users use this skill to coordinate broad or multi-faceted search requests by decomposing them into up to eight parallel sub-tasks and routing them to suitable search agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search request details may be passed to delegated search agents. <br>
Mitigation: Avoid highly sensitive personal, confidential, or regulated information unless that routing is acceptable. <br>
Risk: Search coordination can produce incomplete or misleading task assignments if the original query is underspecified. <br>
Mitigation: Review the delegated sub-tasks and verify final search results before relying on them. <br>


## Reference(s): <br>
- [Searching Assistant on ClawHub](https://clawhub.ai/urrrich0/searching-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance] <br>
**Output Format:** [Markdown or plain text task breakdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include up to eight delegated search sub-tasks; General_Search_Agent is always included.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
