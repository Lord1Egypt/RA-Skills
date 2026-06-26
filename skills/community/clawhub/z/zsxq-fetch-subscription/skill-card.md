## Description: <br>
Use this skill when the user wants OpenClaw to query synced Zhishi Xingqiu content, inspect recent posts, search downloaded documents, summarize updates, or answer questions grounded in the local ZSXQ database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HashedAlex](https://clawhub.ai/user/HashedAlex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query a local ZSXQ data service, summarize subscribed-group updates, search synced documents, and answer questions from locally stored posts and document matches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can rely on a private-content API server that may be exposed on all network interfaces while background sync is active. <br>
Mitigation: Run the API on 127.0.0.1 when possible, confirm authentication before exposing it beyond localhost, and stop or restrict the server when background sync is not needed. <br>
Risk: Answers may be incomplete or stale if the local database has not synced recently. <br>
Mitigation: Check sync status for time-sensitive requests and trigger manual sync only when the user asks for latest content and the last sync is more than one hour old. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/HashedAlex/zsxq-fetch-subscription) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and cited record snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and a running local ZSXQ API server; answers should be grounded in retrieved posts or document matches.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and user changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
