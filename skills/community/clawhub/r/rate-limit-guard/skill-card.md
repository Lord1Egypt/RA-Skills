## Description: <br>
Prevent 429 retry loops and wasted tokens by using preflight checks, backoff, and context shrinking before expensive API calls or after rate limits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dodge1218](https://clawhub.ai/user/dodge1218) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to decide whether to proceed, enter recovery mode, or pause when a request may hit provider rate limits. It helps reduce repeated large retries, premium-provider fallback spam, and oversized calls after 429 responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can slow or pause agent work after rate-limit signals. <br>
Mitigation: Use it where reduced retry waste is more important than immediate continuation, and resume normal concurrency after the rate-limit window clears. <br>
Risk: Shrinking context or sending a minimal probe may omit information from the next request. <br>
Mitigation: Keep the probe narrowly scoped to recovery, then restore necessary context before returning to the full task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dodge1218/rate-limit-guard) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text] <br>
**Output Format:** [Text decision guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs one of proceed, recovery mode, or pause, with rate-limit handling steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
