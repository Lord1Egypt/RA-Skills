## Description: <br>
Spotify intelligence skill with Python runners for auth, playback control, recommendations, feedback loop, governance, and explainable playlist decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Kanazumie](https://clawhub.ai/user/Kanazumie) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, agent operators, and Spotify users use this skill to authenticate with Spotify, control playback, build local listening intelligence, and generate recommendation or playlist-organization guidance with audit and governance checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores Spotify OAuth tokens and listening, profile, or context history in local files. <br>
Mitigation: Protect or periodically delete data/tokens.json and data/spotify-intelligence.sqlite, especially on shared or backed-up machines. <br>
Risk: Spotify scopes include playback control, library access, and playlist modification permissions. <br>
Mitigation: Install only after confirming those scopes are acceptable, and require user confirmation before playlist-changing workflows. <br>
Risk: Sensitive tags or life-phase flags can become part of the local personalization history. <br>
Mitigation: Avoid recording sensitive context unless intentional and review local data retention practices before regular use. <br>


## Reference(s): <br>
- [Read Layer](artifact/references/read-layer.md) <br>
- [Playback Control Layer](artifact/references/playback-control.md) <br>
- [Recommendation Layer v1](artifact/references/recommendation-layer.md) <br>
- [Feedback Loop](artifact/references/feedback-loop.md) <br>
- [Governance & Cost Guardrails](artifact/references/governance-cost.md) <br>
- [OAuth/Auth-Core Usage](artifact/references/auth.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke Spotify API actions and update local SQLite or token files when the user runs the referenced scripts.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
