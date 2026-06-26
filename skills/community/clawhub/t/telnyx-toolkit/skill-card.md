## Description: <br>
Complete Telnyx toolkit - ready-to-use tools (STT, TTS, RAG, Networking, 10DLC) plus SDK documentation for JavaScript, Python, Go, Java, and Ruby. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teamtelnyx](https://clawhub.ai/user/teamtelnyx) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to build Telnyx-powered agents and applications, run Telnyx utility workflows, and consult SDK documentation across JavaScript, Python, Go, Java, and Ruby. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill bundles broad Telnyx account, payment, backup, persistence, credential, and local privilege capabilities. <br>
Mitigation: Review the specific subtool before use and require explicit user confirmation for payment top-ups, account upgrades, backup uploads, cron jobs, public networking, and sudoers changes. <br>
Risk: Credential and identity-verification workflows can expose sensitive API keys or account identity data if run in an unsafe environment. <br>
Mitigation: Use a scoped Telnyx API key where possible, avoid sourcing untrusted .env files, and keep GitHub or LinkedIn verification flows under direct user control. <br>
Risk: Network exposure and local setup helpers may change host networking or privilege boundaries. <br>
Mitigation: Inspect shell scripts before execution and run networking or sudoers setup only in reviewed environments where those changes are intended. <br>


## Reference(s): <br>
- [Telnyx API Docs](https://developers.telnyx.com) <br>
- [Telnyx API Reference](https://developers.telnyx.com/api/v2/overview) <br>
- [Telnyx Portal](https://portal.telnyx.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/teamtelnyx/telnyx-toolkit) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Markdown with inline shell commands, code snippets, JSON examples, and API request guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TELNYX_API_KEY for Telnyx API-backed workflows.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
