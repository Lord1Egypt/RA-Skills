## Description: <br>
Analyzes interaction and memory patterns to produce reports, candidate rules, and self-assessments for agent behavior improvement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenmeng](https://clawhub.ai/user/shenmeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to analyze learning logs and memory files, identify recurring errors or preferences, and generate candidate behavior changes or reports for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can convert prior sessions, memories, and learning logs into persistent behavior changes that may encode incorrect guidance. <br>
Mitigation: Require manual invocation, review proposed changes before any write, validate changes in isolation, and keep backups so behavior files can be restored. <br>
Risk: Memory and transcript analysis can expose sensitive data if secrets or raw conversations are included in the analyzed sources. <br>
Mitigation: Exclude secrets and raw transcripts from inputs, sanitize learning logs before analysis, and limit access to the intended workspace. <br>
Risk: Broad access to memory and behavior files can make agent conduct change unexpectedly over time. <br>
Mitigation: Use human oversight for significant changes, keep an evolution log, and apply only small reviewed updates. <br>


## Reference(s): <br>
- [Self Evolution Engine on ClawHub](https://clawhub.ai/shenmeng/self-evolution-engine) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Evolution script](artifact/scripts/evolution.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON analysis output, Markdown reports, and inline shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write report files or evolution logs when invoked with output or logging options.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
