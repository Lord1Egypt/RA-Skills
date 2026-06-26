## Description: <br>
Use UniFuncs Deep Search API for fast, comprehensive information gathering when users ask for deep search, broad investigation, or in-depth topic coverage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vinlic](https://clawhub.ai/user/vinlic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to run UniFuncs Deep Search for complex or multi-part questions and return consolidated research reports, task IDs, or task status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and API credentials are sent to the UniFuncs service. <br>
Mitigation: Use the skill only when UniFuncs is trusted for the query content and API key; avoid secrets, internal documents, private URLs, customer data, and regulated information. <br>
Risk: Report runs can continue in a detached background process and streamed output may remain on disk. <br>
Mitigation: Use explicit timeouts and stream-file locations, monitor long-running report tasks, and remove stream files after completion when sensitive content may be present. <br>
Risk: The --push-to-share and --set-public options can externally share or publish results. <br>
Mitigation: Use sharing or public flags only when intentional and after confirming that the report does not contain confidential or sensitive content. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/vinlic/unifuncs-deep-search) <br>
- [UniFuncs account and API key setup](https://unifuncs.com/account) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text reports, task IDs, and optional JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May stream partial results to a local stream file and provide a follow-up command when a report is still running.] <br>

## Skill Version(s): <br>
0.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
