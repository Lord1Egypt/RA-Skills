## Description: <br>
AI Firewall for Open Claw agents that scrubs inbound messages and tool results for prompt injection, jailbreaks, and data exfiltration attempts using Sentinel's multi-layer detection pipeline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[c0ri](https://clawhub.ai/user/c0ri) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to route Open Claw prompts, tool inputs, tool results, and optional Anthropic proxy traffic through Sentinel for prompt-injection, jailbreak, and data-exfiltration checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends agent prompts, tool inputs, tool outputs, and optional Anthropic proxy traffic to Sentinel's service for inspection. <br>
Mitigation: Review Sentinel's privacy and retention terms before use, configure only a trusted HTTPS SENTINEL_API_URL, and avoid routing data that policy forbids sharing with the service. <br>
Risk: Scrubbing is disabled when the Sentinel key is missing or the Sentinel service is unreachable, so traffic may pass through uninspected. <br>
Mitigation: Set and verify SENTINEL_KEY before use, monitor startup warnings, and treat connectivity failures as reducing protection for that session. <br>


## Reference(s): <br>
- [Sentinel Proxy on ClawHub](https://clawhub.ai/c0ri/sentinel-proxy) <br>
- [Sentinel skills repository](https://github.com/c0ri/sentinel-skills) <br>
- [Sentinel Proxy service](https://sentinel-proxy.skyblue-soft.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown instructions with shell environment variables and hook behavior guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Hook scripts may emit modified JSON envelopes, block unsafe requests, log flagged events locally, or pass traffic through when Sentinel is not configured or unreachable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
