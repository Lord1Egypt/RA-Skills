## Description: <br>
Configure, validate, and troubleshoot a Session Messenger to n8n to OpenClaw bridge for two-way text messaging and image exchange when the hosted relay supports attachments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[droidhackzor](https://clawhub.ai/user/droidhackzor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up or repair the n8n/OpenClaw side of a Session relay, validate relay endpoints, import or patch the n8n workflow, and confirm attachment support before publication or activation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Relay URLs and API keys may expose private messaging infrastructure if copied into unsafe places. <br>
Mitigation: Use HTTPS endpoints you control, store API keys in secret management or environment variables, and avoid placing secrets in command history. <br>
Risk: The n8n workflow polls the relay and can send replies through Session once activated. <br>
Mitigation: Review the workflow, replace all placeholders, restrict allowed senders, and confirm the OpenClaw endpoint and payload shape before enabling the polling loop. <br>
Risk: Attachment support depends on the deployed relay implementation. <br>
Mitigation: Use the relay health and attachment endpoint checks to confirm capability before relying on image or file exchange. <br>


## Reference(s): <br>
- [Session OpenClaw Bridge on ClawHub](https://clawhub.ai/droidhackzor/session-openclaw-bridge) <br>
- [openclaw-session-relay-workflow.json](references/openclaw-session-relay-workflow.json) <br>
- [release.md](references/release.md) <br>
- [validate_relay.py](scripts/validate_relay.py) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline commands, JSON workflow guidance, and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include relay readiness summaries and endpoint validation guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and references/release.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
