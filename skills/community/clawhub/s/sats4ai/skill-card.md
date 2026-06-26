## Description: <br>
Sats4AI provides an MCP server for paid-per-use AI generation and utility tools, including image, text, video, music, speech, 3D, vision analysis, file conversion, and SMS capabilities paid with Bitcoin Lightning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cnghockey](https://clawhub.ai/user/cnghockey) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to connect agents to Sats4AI's MCP or L402 services, create Lightning invoices, pay with a Lightning wallet, and call AI generation or utility tools without API keys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SMS sending can contact real recipients, expose phone numbers or message bodies to a provider, and create costs. <br>
Mitigation: Use SMS only after explicit user confirmation; confirm the provider, recipient, message content, and charges before sending. <br>
Risk: Paid tool calls can spend Lightning funds when an invoice is paid for the selected service and model. <br>
Mitigation: Confirm the tool, model, quoted cost, and invoice before payment, and keep wallet permissions scoped to the intended task. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/cnghockey/sats4ai) <br>
- [Sats4AI Website](https://sats4ai.com) <br>
- [Sats4AI OpenClaw Guide](https://sats4ai.com/openclaw) <br>
- [Sats4AI MCP Docs](https://sats4ai.com/mcp) <br>
- [Sats4AI L402 Docs](https://sats4ai.com/l402) <br>
- [Sats4AI Service Discovery](https://sats4ai.com/.well-known/l402-services) <br>
- [Alby Hub AI Wallet Setup](https://getalby.com/ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Images, Video, Audio, Files, API Calls, SMS messages] <br>
**Output Format:** [MCP tool results and L402 API responses, including text, base64 media data, transcripts, converted files, payment invoices, and delivery actions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires per-use Lightning payment; SMS use can deliver real-world messages and may incur provider charges.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
