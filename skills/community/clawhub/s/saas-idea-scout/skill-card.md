## Description: <br>
Chat-driven SaaS idea discovery and validation pipeline that generates idea seeds, coordinates discovery, critique, and evaluation agents, and produces scored, ranked PRDs with adversarial validation and founder-aware ranking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[itthomas](https://clawhub.ai/user/itthomas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, founders, and product teams use this skill to generate and stress-test SaaS opportunities before committing to deeper market research or implementation. It is suited for first-pass validation of product directions, adversarial critique of startup ideas, and contextual ranking against a founder profile. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates local run files, launches sub-agents, runs shell checks, and temporarily uses a watchdog. <br>
Mitigation: Run it only after explicit confirmation, keep outputs in a dedicated directory, and review generated files before relying on the results. <br>
Risk: Task briefs and generated idea context could influence file paths or operational scope if not bounded. <br>
Mitigation: Resolve output paths before execution and do not allow task briefs to control arbitrary filesystem destinations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/itthomas/saas-idea-scout) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/itthomas) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Discovery agent instructions](artifact/instructions/discovery.md) <br>
- [Critic agent instructions](artifact/instructions/critic.md) <br>
- [Evaluator agent instructions](artifact/instructions/evaluator.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, scored tables, ranked recommendations, shell verification commands, and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local run files under the skill's run directory, including PRDs, critiques, evaluations, dossiers, and model preference configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
