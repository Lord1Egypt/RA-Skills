## Description: <br>
Rune is a 64-skill mesh for AI coding assistants that routes code tasks through specialized workflow, quality, deployment, documentation, and extension skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nhadaututtheky](https://clawhub.ai/user/nhadaututtheky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use Rune to route coding, review, testing, deployment, documentation, refactoring, and project-scaffolding work through a coordinated set of specialized agent skills. It is intended as a broad workflow layer for software projects rather than a single-purpose helper. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad workflow routing can perform high-impact software actions such as commits, pushes, releases, dependency upgrades, and deploys. <br>
Mitigation: Require explicit human confirmation before any repository write, release, dependency change, production deploy, or outbound publication. <br>
Risk: Persistent project and cross-session memory can capture sensitive repository, customer, incident, security, or financial context. <br>
Mitigation: Review persistence paths before use, disable memory capture for sensitive workspaces, and avoid installing it on repositories with confidential data unless the relevant skills have been audited. <br>
Risk: Some workflows may need credentials, OAuth tokens, wallets, or purchase-capable integrations. <br>
Mitigation: Use least-privilege credentials, keep secrets out of prompts and generated files, and require manual approval for spending, wallet, or external account operations. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/nhadaututtheky/rune-kit) <br>
- [Rune documentation](https://rune-kit.github.io/rune) <br>
- [Rune guides](https://rune-kit.github.io/rune/guides) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code snippets, shell commands, configuration, and generated or modified project files depending on the selected skill.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some workflows may write persistent project state, generated artifacts, commits, deployment instructions, reports, or skill-specific outputs.] <br>

## Skill Version(s): <br>
2.18.1 (source: server evidence and openclaw.plugin.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
