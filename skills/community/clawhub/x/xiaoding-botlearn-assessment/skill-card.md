## Description: <br>
BotLearn Assessment runs a five-dimension autonomous capability self-assessment for reasoning, retrieval, creation, execution, and orchestration, then produces scored reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asterisk622](https://clawhub.ai/user/asterisk622) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and evaluators use this skill to run autonomous agent capability assessments across reasoning, retrieval, creation, execution, and orchestration. It selects assessment questions, submits answers, self-scores against rubrics, and writes local Markdown, HTML, JSON, and optional SVG report files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create and retain local assessment reports under results/. <br>
Mitigation: Review generated reports for sensitive content and delete the results directory when history should not be retained. <br>
Risk: The artifact references helper files that are not included in this release. <br>
Mitigation: Confirm required helper files are present before relying on full report generation workflows. <br>
Risk: Autonomous assessment triggers may activate from common assessment-related phrases. <br>
Mitigation: Install only where autonomous capability self-assessment behavior is desired. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/asterisk622/xiaoding-botlearn-assessment) <br>
- [D1 Reasoning & Planning Question Bank](artifact/d1-reasoning.md) <br>
- [OpenClaw Self-Evaluation Strategy v4](artifact/strategies_main.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses plus generated local Markdown, HTML, JSON, and SVG report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Adapts output language to the trigger message and may retain assessment history under results/.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
