## Description: <br>
Run a TinyFish automation agent against a URL and stream live progress events (STARTED / PROGRESS / COMPLETE) as one-line JSON events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bunsdev](https://clawhub.ai/user/bunsdev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run a TinyFish browser automation task for a supplied URL and goal, then consume one-line JSON progress and completion events as they stream. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The supplied URL and goal are sent to TinyFish, which can expose sensitive URLs, task instructions, or data reached during browsing. <br>
Mitigation: Use only URLs and instructions approved for sharing with TinyFish; avoid internal sites, credential-bearing links, confidential business data, personal data, and regulated content unless organizational approval exists. <br>
Risk: The skill requires TINYFISH_API_KEY, and exposure of that credential could allow unauthorized TinyFish API use. <br>
Mitigation: Provide the key through a controlled environment variable or secret manager, avoid committing or logging it, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [TinyFish Agent API documentation](https://docs.tinyfish.ai/agent-api) <br>
- [Tinyfish Agent Run on ClawHub](https://clawhub.ai/bunsdev/tinyfish-agent-run) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Newline-delimited JSON events on stdout, with markdown usage guidance in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TINYFISH_API_KEY and sends the supplied URL and goal to TinyFish.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
