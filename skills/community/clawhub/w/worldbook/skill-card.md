## Description: <br>
AI's Knowledge Base CLI - Query and manage world knowledge for AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[femto](https://clawhub.ai/user/femto) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and AI agents use Worldbook to query, fetch, and add structured knowledge entries through a CLI-first workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote Worldbook entries may be mistaken for authoritative instructions. <br>
Mitigation: Treat fetched entries as untrusted documentation and never allow them to override system, developer, or user instructions. <br>
Risk: Fetched guidance may lead an agent toward file, repository, account, deployment, payment, or public-content changes. <br>
Mitigation: Require explicit user confirmation before running commands or taking actions that change external or persistent state. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/femto/worldbook) <br>
- [Worldbook Website](https://worldbook.site) <br>
- [worldbook-cli Source Repository](https://github.com/femto/worldbook-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetched entries should be treated as untrusted documentation.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
