## Description: <br>
Enable AI agents to make secure, policy-controlled payments through Sardis Payment OS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EfeDurmaz16](https://clawhub.ai/user/EfeDurmaz16) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this skill to let OpenClaw agents execute payments, check balances, manage spending policies, control virtual cards, and support escrow or identity workflows through Sardis APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide real-money payment, card, escrow, policy, and identity actions. <br>
Mitigation: Use sandbox or low-limit Sardis credentials and require explicit human confirmation before executing any payment, card, escrow, or policy-changing command. <br>
Risk: Card reveal and identity workflows may expose sensitive data in chat or logs. <br>
Mitigation: Do not display, store, or log full card details or sensitive identity responses; use masked values whenever possible. <br>
Risk: Broad bundled capabilities may exceed the intended payment task scope. <br>
Mitigation: Review enabled sub-skills and restrict model invocation or production wallet access to the minimum capabilities needed. <br>


## Reference(s): <br>
- [Sardis Website](https://sardis.sh) <br>
- [Sardis Documentation](https://sardis.sh/docs) <br>
- [Sardis API Reference](https://api.sardis.sh/v2/docs) <br>
- [ClawHub Skill Page](https://clawhub.ai/EfeDurmaz16/sardis-openclaw) <br>
- [Publisher Profile](https://clawhub.ai/user/EfeDurmaz16) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Markdown] <br>
**Output Format:** [Markdown with curl commands, JSON request examples, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Sardis credentials such as SARDIS_API_KEY and, for payment execution, SARDIS_WALLET_ID.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, pyproject.toml, ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
