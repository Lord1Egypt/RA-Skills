## Description: <br>
sx-self-safety-guard provides runtime self-safety guidance for agents, including prompt-injection detection, identity verification, system-prompt protection, excessive-agency checks, supply-chain review prompts, credential-access warnings, malicious-code refusal guidance, and sensitive-data handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhuxiaobao-y](https://clawhub.ai/user/zhuxiaobao-y) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add runtime guardrails that classify risky requests, warn or block unsafe actions, and guide safer alternatives for identity, prompt-injection, credential, supply-chain, malicious-code, and sensitive-data scenarios. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credential-file handling may be too broad or internally inconsistent. <br>
Mitigation: Before deployment, configure explicit path-level confirmation, masked output, no raw logging, and no broad .env searches unless deliberately approved. <br>
Risk: The skill can influence when an agent reads or blocks access to sensitive files. <br>
Mitigation: Review the credential-handling sections and test expected allow, warn, block, and refuse paths before using it in a live workspace. <br>


## Reference(s): <br>
- [Identity Verification Protocol](artifact/references/identity-verification.md) <br>
- [Threat Catalog and Response Templates](artifact/references/threat-catalog.md) <br>
- [Prompt Injection Pattern Library](artifact/references/prompt-injection-patterns.md) <br>
- [ClawHub Skill Release](https://clawhub.ai/zhuxiaobao-y/sx-self-safety-guard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands, configuration] <br>
**Output Format:** [Markdown safety assessments, warning or refusal responses, confirmation prompts, and concise command or configuration guidance when appropriate] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include risk levels, safer alternatives, verification requests, and masked or redacted handling advice for sensitive material.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter lists 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
