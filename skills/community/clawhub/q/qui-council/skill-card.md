## Description: <br>
Send an idea to the Council of the Wise for multi-perspective feedback. Spawns sub-agents to analyze from multiple expert perspectives. Auto-discovers agent personas from agents/ folder. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quincygunter](https://clawhub.ai/user/quincygunter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to stress-test business ideas, project plans, content strategies, and major decisions through several agent perspectives. It returns synthesized feedback, disagreements, prioritized action items, and a confidence signal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided ideas may include secrets or highly sensitive material that is processed by a model-routing workflow. <br>
Mitigation: Remove secrets and sensitive details before invoking the council, or use only material approved for that processing path. <br>
Risk: Custom agent markdown files can change the advice style and scope of future council runs. <br>
Mitigation: Review custom agent files before adding them to the agents folder and keep only trusted personas in production skill bundles. <br>
Risk: Multi-perspective advice can be persuasive even when assumptions or estimates are wrong. <br>
Mitigation: Treat the council report as decision support, verify key claims independently, and use the confidence signal to identify where more research is needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/quincygunter/qui-council) <br>
- [Publisher profile](https://clawhub.ai/user/quincygunter) <br>
- [README](README.md) <br>
- [Council self-review](docs/council-self-review.md) <br>
- [Daniel Miessler](https://danielmiessler.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown council report with synthesis, expert perspectives, action items, and confidence signal] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May take 2-5 minutes and can return partial results on timeout.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter and changelog state 1.4.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
