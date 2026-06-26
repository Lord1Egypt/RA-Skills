## Description: <br>
Uses the Xiaoba AI Interview open API to create interview plans, manage candidates, start interview sessions, and retrieve interview results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[changwu](https://clawhub.ai/user/changwu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Recruiting and hiring teams use this skill to call Xiaoba interview APIs for interview planning, candidate setup, session scheduling, and result retrieval. Developers can use the included curl and jq examples to integrate those workflows into an agent run. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Candidate and interview data is sent to an external Xiaoba/ibaguo service. <br>
Mitigation: Use only with authority to process the data, confirm candidate consent and legal basis, and avoid sending unnecessary resume or contact details. <br>
Risk: The XIAOBA_API_KEY credential can expose the interview API account if logged or shared. <br>
Mitigation: Store the key in the environment, keep authorization headers out of chats and logs, and redact sensitive response details. <br>
Risk: Generated interview links may grant access to candidate interview sessions. <br>
Mitigation: Share interview URLs only with intended recipients and treat them as sensitive session links. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/changwu/xiaoba-ai-interview) <br>
- [Xiaoba / ibaguo homepage](https://www.ibaguo.com) <br>
- [Xiaoba API base URL](https://www.ibaguo.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and the XIAOBA_API_KEY environment variable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
