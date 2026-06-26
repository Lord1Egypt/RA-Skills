## Description: <br>
WATI (WhatsApp Team Inbox) API integration with managed authentication for sending WhatsApp messages, managing contacts, and handling templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to interact with WATI through Maton-managed authentication, including reading contacts and messages, managing templates and contacts, and sending approved WhatsApp messages. Write operations require explicit user approval before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires MATON_API_KEY, a sensitive credential that can grant access to WATI data through Maton. <br>
Mitigation: Keep MATON_API_KEY private, use the least-privileged account available, and avoid exposing it in logs, prompts, or shared output. <br>
Risk: Maton proxies WATI data and manages the WATI connection for the user. <br>
Mitigation: Install and use the skill only when the user trusts Maton to process the connected WATI account data. <br>
Risk: Write operations can send WhatsApp messages or change contacts, templates, broadcasts, and related account data. <br>
Mitigation: Require explicit user approval and verify recipients, message text, templates, connection IDs, and contact changes before executing create, update, delete, or send actions. <br>


## Reference(s): <br>
- [ClawHub Wati Skill Page](https://clawhub.ai/byungkyu/wati) <br>
- [Maton Homepage](https://maton.ai) <br>
- [WATI API Documentation](https://docs.wati.io/reference/introduction) <br>
- [WATI Help Center](https://docs.wati.io/) <br>
- [Maton Community](https://discord.com/invite/dBfFAcefs2) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Code, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline HTTP, shell, Python, and JavaScript examples; API responses may be JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and MATON_API_KEY; write operations require explicit user approval.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
