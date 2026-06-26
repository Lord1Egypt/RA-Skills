## Description: <br>
Profile offline OpenClaw skill run samples to detect latency, CPU, and memory bottlenecks and compare sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mike007jd](https://clawhub.ai/user/mike007jd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use SkillPulse to analyze offline OpenClaw skill run samples, detect latency, CPU, and memory bottlenecks, export JSON or HTML reports, and compare before-and-after profiling sessions before regressions reach production. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted or low-quality sample files can produce misleading profiling results or unsafe HTML report content. <br>
Mitigation: Use sample files from trusted sources, validate input quality, and prefer JSON output or trusted samples when generating HTML reports. <br>
Risk: User-selected report paths can write artifacts to unintended locations. <br>
Mitigation: Choose output paths deliberately and review command arguments before running report exports. <br>


## Reference(s): <br>
- [SkillPulse on ClawHub](https://clawhub.ai/mike007jd/skillpulse) <br>
- [mike007jd publisher profile](https://clawhub.ai/user/mike007jd) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON or HTML report artifacts from the profiler] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and user-provided offline JSON sample files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
