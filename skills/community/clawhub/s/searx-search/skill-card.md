## Description: <br>
Provides plain-text web search results by querying public SearX instances and retrying alternative instances when a request fails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FikaCode](https://clawhub.ai/user/FikaCode) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when a user requests current web search results, recent AI news, or global events. It runs a shell search helper against public SearX instances and returns the top plain-text result titles and URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to independently operated public SearX instances, which may expose sensitive terms outside the user's environment. <br>
Mitigation: Avoid searching for secrets, credentials, personal data, private URLs, internal company information, or sensitive investigations unless the skill is updated to use a trusted allowlist or a self-hosted SearX instance with explicit user confirmation. <br>
Risk: The selected public search instance can change between runs, so availability and result behavior may vary. <br>
Mitigation: Review returned titles and URLs before relying on them, and prefer a controlled SearX endpoint when consistent behavior is required. <br>


## Reference(s): <br>
- [SearX public instances](https://searx.space/) <br>
- [SearX instances JSON](https://searx.space/data/instances.json) <br>
- [ClawHub skill page](https://clawhub.ai/FikaCode/searx-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text search result titles and URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns up to five results and may emit a plain-text failure message if no queried SearX instance succeeds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
