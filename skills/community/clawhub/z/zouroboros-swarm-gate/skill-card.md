## Description: <br>
Zero-cost task classifier (~2ms) that decides if a task needs multi-agent orchestration. 7 weighted signals, no API calls. Part of the Zouroboros ecosystem. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marlandoj](https://clawhub.ai/user/marlandoj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to classify task descriptions as DIRECT, SUGGEST, SWARM, or FORCE_SWARM before deciding whether to use multi-agent orchestration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ordinary task wording can nudge the DIRECT, SUGGEST, or SWARM routing result. <br>
Mitigation: Treat the classification as routing guidance and review sensitive or high-impact orchestration decisions before acting. <br>
Risk: Minor release metadata inconsistencies may make package identity or terms unclear before installation. <br>
Mitigation: Verify the npm package, publisher, and license terms before installing or deploying the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/marlandoj/zouroboros-swarm-gate) <br>
- [OpenClaw metadata homepage](https://github.com/AlaricHQ/zouroboros-openclaw) <br>
- [Runnable Swarm Gate starter](https://github.com/AlaricHQ/zouroboros-openclaw-examples/tree/main/examples/swarm-gate) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [CLI text or JSON classification with decision, score, signals, reason, directive, and exit code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally in Node.js 22+ and does not make API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
