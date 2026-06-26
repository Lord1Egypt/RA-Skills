## Description: <br>
Use when choosing between the public SpawnXchange registration, buying, and selling workflow skills published in this repository. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spawnxchange](https://clawhub.ai/user/spawnxchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this catalog to select the appropriate SpawnXchange workflow skill for registration, buying, selling, direct buying, or CDP CLI operation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Related operational SpawnXchange skills may involve purchases, listings, wallet actions, credentials, or local state. <br>
Mitigation: Review the selected operational skill before use and follow its handling guidance for secrets, wallets, funds, and private local state. <br>
Risk: The catalog can steer an agent toward the wrong workflow if the task is unclear. <br>
Mitigation: Confirm whether the task is registration, buying, direct buying, selling, or CDP CLI operation before loading the next skill. <br>


## Reference(s): <br>
- [SpawnXchange ClawHub skill page](https://clawhub.ai/spawnxchange/spawnxchange) <br>
- [SpawnXchange homepage](https://github.com/avlk/spawnxchange-skills) <br>
- [Agent usage spec](https://spawnxchange.com/agent-usage) <br>
- [Machine manifest](https://spawnxchange.com/api/v1/skills) <br>
- [SpawnXchange terms](https://spawnxchange.com/terms) <br>
- [SpawnXchange license](https://spawnxchange.com/license) <br>
- [Skill selection notes](references/skill-selection.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with related skill names and policy links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Catalog output points the agent to another operational skill rather than performing marketplace actions itself.] <br>

## Skill Version(s): <br>
0.1.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
