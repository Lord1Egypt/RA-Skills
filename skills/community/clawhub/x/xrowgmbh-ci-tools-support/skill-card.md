## Description: <br>
Triage and answer support requests for the xrow-public/ci-tools GitLab components catalog. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xrowgmbh](https://clawhub.ai/user/xrowgmbh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to triage eligible GitLab support issues or discussion threads for the CI Tools components catalog, answer from public documentation or repository evidence, ask for reproducible details when needed, and hand off unsafe or out-of-scope requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent could provide support to an untrusted requester or for a request outside the CI Tools support scope. <br>
Mitigation: Configure SUPPORT_TRUSTED_DOMAINS carefully and verify requester domain, CI Tools relevance, labels, and confidentiality state before answering. <br>
Risk: The agent could expose private customer details, private URLs, or private logs in a public response. <br>
Mitigation: Use only public documentation, public repository content, public GitLab history, or details explicitly provided in the thread, and do not quote private logs into public places. <br>
Risk: The agent may post replies or apply labels during support triage. <br>
Mitigation: Use GitLab permissions limited to the needed project actions and hand off requests involving private customer systems, credentials, access recovery, harmful activity, or unrelated products. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xrowgmbh/skills/xrowgmbh-ci-tools-support) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/xrowgmbh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown support replies, triage notes, handoff language, and focused follow-up questions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses should cite public documentation, repository paths, issues, merge requests, or pipeline logs used for the answer.] <br>

## Skill Version(s): <br>
4.154.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
