## Description: <br>
Detects when a human tags their AI familiar in someone else's X/Twitter thread, fetches full conversation context, infers intent, and crafts an appropriate reply. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[m-lwatcher](https://clawhub.ai/user/m-lwatcher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to inspect X/Twitter threads where the agent was tagged, infer the human's intent, draft concise replies, and optionally post through xurl after approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes background automation that can post replies, like tweets, call Gemini, run local workflows, and restart a gateway. <br>
Mitigation: Disable or remove the background watcher and autonomous reply bot unless those actions are explicitly intended, and require human approval for every public X action and infrastructure restart. <br>
Risk: The skill depends on xurl credentials and a Gemini API key, creating risk if credentials or routed conversation data are exposed. <br>
Mitigation: Do not print credential files or verbose auth headers, keep credentials out of agent context, and document the Gemini data flow before enabling the automation. <br>
Risk: The public skill description emphasizes assisted drafting while the bundled scripts add autonomous behavior. <br>
Mitigation: Review the included scripts before installation and run any reply workflow in dry-run or manual approval mode until the operational behavior is understood. <br>


## Reference(s): <br>
- [X Tag Responder on ClawHub](https://clawhub.ai/m-lwatcher/x-tag-responder) <br>
- [m-lwatcher publisher profile](https://clawhub.ai/user/m-lwatcher) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and drafted reply text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires xurl credentials for X/Twitter actions; public posting should stay behind explicit human approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
