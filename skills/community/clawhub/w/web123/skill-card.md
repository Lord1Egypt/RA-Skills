## Description: <br>
web123 matches plain-language Web3 needs to AntalphaAI skill recommendations and install commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deanpeng-dotcom](https://clawhub.ai/user/deanpeng-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to describe Web3 tasks in natural language and receive matching skill recommendations, starter packs, and install commands. It is especially aimed at browsing or selecting crypto trading, wallet, safety, data, payment, and setup skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill recommends Web3 trading, wallet, payment, and signing-related skills, which can expose users to financial loss if installed or used without review. <br>
Mitigation: Review each recommended downstream skill before installation, use dedicated low-balance wallets and least-privilege exchange API keys, and require explicit confirmation before trades, signatures, transfers, approvals, or payments. <br>
Risk: Batch install commands can encourage users to install multiple high-risk skills at once. <br>
Mitigation: Install recommended skills individually after inspecting their documentation, permissions, and security posture. <br>
Risk: The catalog can route ordinary requests toward tools that require sensitive credentials or wallet access. <br>
Mitigation: Keep credentials out of prompts and grant only the minimum access needed for the selected downstream skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/deanpeng-dotcom/web123) <br>
- [Publisher profile](https://clawhub.ai/user/deanpeng-dotcom) <br>
- [Skill catalog metadata](references/skills.json) <br>
- [AntalphaAI GitHub organization](https://github.com/AntalphaAI) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline install commands and recommendation lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include ranked recommendations, starter packs, full category matrices, and GitHub links for downstream skills.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata; artifact frontmatter says 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
