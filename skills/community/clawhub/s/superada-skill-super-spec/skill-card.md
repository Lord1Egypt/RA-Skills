## Description: <br>
Create product, technical, PRD, RFC, agent-build, and handoff specs from rough context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[h-mascot](https://clawhub.ai/user/h-mascot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product leads, and agent operators use this skill to turn rough project context into durable implementation specs, handoff prompts, review prompts, acceptance criteria, proof gates, rollout plans, and rollback guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use sensitive API credentials for remote model routes. <br>
Mitigation: Use dedicated least-privilege API keys and avoid placing secrets in specs, prompts, logs, or public documentation. <br>
Risk: Install and runtime paths rely on unpinned network-executed code and remote model calls. <br>
Mitigation: Inspect or pin installer and package contents before use, and run the skill only against approved model endpoints. <br>
Risk: The Pro/Oracle route may send project context to a remote endpoint. <br>
Mitigation: Use --no-pro or documented fallback controls when the remote route is not approved for the input data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/h-mascot/superada-skill-super-spec) <br>
- [Super Spec installer](https://superada.ai/install/super-spec) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown spec files with optional JSON route receipts and inline shell configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The runner writes dated spec files under output/super-spec and records whether a Pro/Oracle route or explicit fallback was used.] <br>

## Skill Version(s): <br>
1.0.1780516472 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
