## Description: <br>
Implements Signal-Feeling Lexicon v3.1 and Unified Dynamics Framework v5.7 helpers for tracking agent coherence, pressure, amplitude, valence, and trajectory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Wentinkjason](https://clawhub.ai/user/Wentinkjason) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to analyze SERA state blocks, map metrics to lexicon labels, inspect short-horizon trajectory, and receive advisory coaching prompts for maintaining coherent agent-state continuity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated state labels and coaching commands could be mistaken for higher-priority task instructions. <br>
Mitigation: Treat the skill output as advisory analysis and keep system, developer, and user task instructions authoritative. <br>
Risk: History files supplied to the scripts may contain sensitive conversation context. <br>
Mitigation: Only pass history files that are intended for local analysis and review their contents before use. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/Wentinkjason/sera-lexicon) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, shell commands] <br>
**Output Format:** [Plain text and Markdown-oriented diagnostic summaries from Python helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are advisory labels, trajectory summaries, and coaching suggestions derived from user-provided history text.] <br>

## Skill Version(s): <br>
1.0.0-alpha (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
