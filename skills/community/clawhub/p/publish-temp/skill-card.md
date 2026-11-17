## Description:

Pokemon GO PvP cultivation query skill based on PvPokeTW ranking data and gamemaster base stats, providing rankings, recommended moves, best IVs, and user IV comparisons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pigro0314](https://clawhub.ai/user/pigro0314)

### License/Terms of Use:

MIT-0

## Use Case:

External Pokemon GO PvP players and assistant users use this skill to query league rankings, IV fit, recommended moves, team suggestions, training priority, and missing roster coverage from PvPoke-derived data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation may execute unpinned npm tooling.

Mitigation: Require a package.json and lockfile with pinned dependencies, and avoid direct unpinned npx execution before deployment.

Risk: The missing fetch script issue can prevent reliable data refresh.

Mitigation: Verify the documented fetch command exists and works before relying on ranking or gamemaster cache updates.

Risk: Evaluation may change local inventory data by filling recommended moves automatically.

Mitigation: Back up data/my_pokemon.json and require an explicit save action before allowing the skill to persist inventory changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pigro0314/skills/publish-temp)
- [PvPokeTW](https://pvpoketw.com/)
- [PvPoke GitHub Repository](https://github.com/pvpoke/pvpoke)
- [PvPoke Rankings Data](https://raw.githubusercontent.com/pvpoke/pvpoke/master/src/data/rankings/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands, Configuration]

**Output Format:** [Markdown and command-oriented text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language Pokemon GO PvP query results; may include rankings, IV comparisons, move recommendations, team suggestions, and local inventory guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata; skill text describes v1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
