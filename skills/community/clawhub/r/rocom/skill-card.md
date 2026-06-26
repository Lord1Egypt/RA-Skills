## Description: <br>
Roco Kingdom World offline data tool. Local JSON queries for pets, skills, and items. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imnotriv3r](https://clawhub.ai/user/imnotriv3r) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and game-focused agents use this skill to query bundled Roco Kingdom World reference data for pets, skills, items, dungeons, regions, natures, marks, quests, and formations without network access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running bundled local Node.js code from a third-party publisher. <br>
Mitigation: Install only from a trusted publisher and review or scan before execution; the security evidence reports no network access, credential handling, persistence, elevated privileges, or destructive behavior. <br>
Risk: Responses may reflect bundled static game data or strategy notes that become stale after game updates. <br>
Mitigation: Use the skill's local queries for grounded answers and verify patch-sensitive recommendations against current game sources. <br>


## Reference(s): <br>
- [Rocom ClawHub listing](https://clawhub.ai/imnotriv3r/rocom) <br>
- [Game Knowledge](references/game-knowledge.md) <br>
- [Data Manifest](MANIFEST.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text terminal output and concise Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local-only Node.js queries over bundled static JSON; no network access, credential handling, persistence, or destructive behavior was identified in the security evidence.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
