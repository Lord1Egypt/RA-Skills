## Description: <br>
Interactive onboarding for Rotifer Protocol that helps users learn core concepts, scaffold Genes, diagnose issues, explore the ecosystem, and upgrade fidelity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoba-dev](https://clawhub.ai/user/xiaoba-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill as a Rotifer Protocol entry point for onboarding, natural-language Gene scaffolding, troubleshooting, ecosystem search, and fidelity migration guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger wording can route unrelated Rotifer or Gene prompts into this skill. <br>
Mitigation: Use explicit prompts that mention Rotifer or Genes, and confirm the user's intended sub-capability when intent is unclear. <br>
Risk: Generated scaffolds or repair guidance can introduce incorrect Gene metadata, schemas, or commands. <br>
Mitigation: Review generated scaffold plans and run Rotifer test and compile checks before publishing or submitting to Arena. <br>
Risk: The skill suggests npm-based CLI and MCP commands that resolve packages at the latest version. <br>
Mitigation: Pin npm package versions or Git tags before running install or build commands in sensitive environments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xiaoba-dev/rotifer-guide) <br>
- [Rotifer Protocol](https://rotifer.dev) <br>
- [Rotifer Documentation](https://rotifer.dev/docs) <br>
- [Rotifer Protocol Specification](https://github.com/rotifer-protocol/rotifer-spec) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands, tables, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include recommended Rotifer CLI commands, MCP configuration snippets, diagnostic tables, and scaffold plans.] <br>

## Skill Version(s): <br>
1.0.3 (source: evidence.release.version and artifact clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
