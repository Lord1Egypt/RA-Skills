## Description: <br>
Pokemon GO PvP cultivation query skill based on PvPokeTW ranking data and gamemaster stats, providing ranking lookup, recommended moves, IV comparison, inventory review, training priority, missing-core, and team guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pigro0314](https://clawhub.ai/user/pigro0314) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Pokemon GO PvP players use this skill to query PvPokeTW rankings and moves, compare IVs, manage a local Pokemon inventory, prioritize training, identify missing roster pieces, and receive team-building guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores and updates a local Pokemon inventory file. <br>
Mitigation: Review data/my_pokemon.json after inventory or evaluation commands and remove entries or fields that should not be retained. <br>
Risk: The skill refreshes public PvPoke ranking and gamemaster data from GitHub-backed sources. <br>
Mitigation: Use it only in environments where outbound access to those public data sources and local cache updates are acceptable. <br>
Risk: Evaluation commands may fill blank move fields with recommended moves. <br>
Mitigation: Check generated move recommendations before relying on them for training or resource decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/pigro0314/publish-temp) <br>
- [Publisher profile](https://clawhub.ai/user/pigro0314) <br>
- [PvPokeTW](https://pvpoketw.com/) <br>
- [PvPoke source repository](https://github.com/pvpoke/pvpoke) <br>
- [PvPoke ranking data](https://raw.githubusercontent.com/pvpoke/pvpoke/master/src/data/rankings/) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, configuration] <br>
**Output Format:** [Plain text and Markdown-style command responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-language PvP query, inventory, prioritization, and team recommendation responses; local JSON inventory may be created or updated by inventory commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
