## Description: <br>
Repo Insights analyzes a GitHub repository's open issues and returns a Claude-generated summary of developer requests, pain points, and project direction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to inspect a GitHub repository's open issues and quickly understand common requests, pain points, and likely project direction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hosted mode asks users to send a raw Anthropic API key to a third-party service without enough disclosure or key-handling controls. <br>
Mitigation: Prefer self-hosting so the key remains under user control, or use a scoped, revocable, low-limit key only after verifying the operator's logging, retention, billing, and key-handling practices. <br>
Risk: Unpinned Python dependencies can change behavior or introduce supply-chain exposure during self-hosted deployment. <br>
Mitigation: Pin and review dependency versions before operating the service. <br>


## Reference(s): <br>
- [ClawHub Repo Insights Page](https://clawhub.ai/albionaiinc-del/repo-insights) <br>
- [Hosted MeshCore API Endpoint](https://meshcore.ai/gateway/call/d062a753-f46c-4a48-808c-fa27dad82de3) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, guidance] <br>
**Output Format:** [JSON response containing the repository name, top issue titles, and a natural-language summary.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses up to 10 open GitHub issues and requests a summary capped at 500 model output tokens.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
