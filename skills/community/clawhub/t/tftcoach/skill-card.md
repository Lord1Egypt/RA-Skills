## Description:

tftcoach helps an agent provide Teamfight Tactics coaching from a player's screenshot or board description, including comp direction, item choices, augment picks, economy, pivots, positioning, and patch-meta advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kewang0622](https://clawhub.ai/user/kewang0622)

### License/Terms of Use:

MIT-0

## Use Case:

External users and game-focused agent operators use this skill to get concise, context-aware Teamfight Tactics decisions from a described or screenshot-based board state. It is intended for gameplay coaching on comps, items, augments, economy, pivoting, positioning, and current patch meta.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Patch-meta, item, and augment advice can become outdated as Teamfight Tactics changes.

Mitigation: Verify patch-specific recommendations against current sources before relying on them for gameplay decisions.

Risk: Screenshots or board descriptions may include visible account or gameplay information.

Mitigation: Share only the game state needed for coaching, and redact identifiers when screenshots contain information unrelated to the requested advice.

Risk: The skill directs the agent to search the web for current TFT information.

Mitigation: Review sourced recommendations and prefer current, reputable TFT references when the agent uses web search.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kewang0622/skills/tftcoach)
- [Publisher profile](https://clawhub.ai/user/kewang0622)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)
- [Repository link from artifact README](https://github.com/KeWang0622/tftcoach)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text coaching responses, optionally with simple board-layout code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May rely on current web search for patch-meta and item guidance; no executable code is produced by the skill itself.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
