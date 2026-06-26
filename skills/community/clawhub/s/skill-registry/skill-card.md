## Description: <br>
Local skill registry with trigger-word routing for organizing workspace skills and matching user requests to relevant local skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Slim-Rush](https://clawhub.ai/user/Slim-Rush) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw workspace maintainers use this skill to maintain a local skill registry, answer skill-discovery queries, and route requests to matching local skills by trigger words. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trigger-word routing can influence which local skill an agent chooses for a future request. <br>
Mitigation: Keep trigger words specific and require confirmation before a matched skill performs file changes, account actions, public posting, or other high-impact work. <br>
Risk: A stale or broad registry entry can cause inaccurate skill listings or mismatched routing. <br>
Mitigation: Review registry entries regularly, remove unused skills, and keep category and trigger tables current. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Slim-Rush/skill-registry) <br>
- [Registry template](REGISTRY.template.md) <br>
- [Rules snippet](RULES.snippet.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions, registry template entries, and routing-rule snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable code; users maintain local registry and rule files.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
