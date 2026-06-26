## Description: <br>
Provides local heuristic checks for AI ethics safety and authenticity, including alienation-pattern detection, value-alignment review, IIQ/EQ/IQ scoring, and AI personality-matrix guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zxfei420](https://clawhub.ai/user/zxfei420) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, AI reviewers, and ethics teams use this skill to inspect AI outputs for authenticity, over-compliance, manipulation, value-alignment concerns, and personality/team-configuration patterns. It produces advisory assessments and audit-report material for human review rather than a validated enforcement layer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill presents heuristic checks as broad AI ethics monitoring and protection, which can overstate reliability. <br>
Mitigation: Treat results as advisory signals, review findings manually, and validate them with domain-specific evaluations before relying on them for governance or enforcement. <br>
Risk: Local reports or logs may contain the AI text being assessed, including confidential or sensitive content. <br>
Mitigation: Use a controlled output directory and avoid processing confidential content unless local report and log storage is acceptable. <br>


## Reference(s): <br>
- [AI 树德 theory article](https://blog.csdn.net/Figo_Cheung/article/details/159044535) <br>
- [theory.md](artifact/references/theory.md) <br>
- [equality_measurement.md](artifact/references/equality_measurement.md) <br>
- [personality_matrix.md](artifact/references/personality_matrix.md) <br>
- [ClawHub skill page](https://clawhub.ai/zxfei420/yi-shang-ai-ethics-safety) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python code examples, shell commands, JSON configuration, and local audit-report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are advisory and may write reports to a caller-controlled local output directory.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
