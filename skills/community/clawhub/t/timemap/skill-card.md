## Description:

Search historical entertainment, nightlife, and culture venues in Tel Aviv and Haifa from timemap.co.il.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexpolonsky](https://clawhub.ai/user/alexpolonsky)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and researchers use this skill to search community-curated venue history for Tel Aviv-Yafo and Haifa by name, address, year, category, city, coordinates, or venue ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation guidance includes an unpinned npx command.

Mitigation: Install from a reviewed commit or manual copy when possible, matching the server security guidance.

Risk: The skill fetches public Timemap data and writes a 24-hour cache in a shared temporary directory.

Mitigation: Use only where fetching public Timemap data is acceptable; on shared multi-user systems, move or isolate the cache before use.

Risk: Community-curated venue history may contain gaps, inaccuracies, or estimated years.

Mitigation: Treat historical results as research aids and verify important claims against cited venue references or primary sources.

## Reference(s):

- [Timemap skill on ClawHub](https://clawhub.ai/alexpolonsky/skills/timemap)
- [Timemap](https://timemap.co.il)
- [Timemap public venue API](https://timemap.co.il/api/venue)
- [Source homepage](https://github.com/alexpolonsky/agent-skill-timemap)
- [Author profile](https://github.com/alexpolonsky)
- [Agent Skills specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Terminal text or JSON from Python CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports Hebrew and English search terms; JSON mode is available with --json; results may include community-submitted venue memories, photos, coordinates, and historical year estimates.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
