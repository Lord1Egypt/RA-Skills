## Description: <br>
Fast security spot-check with 10 iterations in about 5-10 minutes, covering secrets, OWASP basics, authentication, rate limiting, and containers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dorukardahan](https://clawhub.ai/user/dorukardahan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and security reviewers use this skill to run a quick pre-deployment or daily security spot-check. It guides an agent through 10 focused checks and produces a local report for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local report may contain vulnerability details or secret-like values discovered during repository inspection. <br>
Mitigation: Review `.ralph-report.md` before committing or sharing it, and consider adding `.ralph-report*.md` to `.gitignore`. <br>
Risk: Fast spot-checks and pattern matches can produce incomplete or false-positive security findings. <br>
Mitigation: Manually review findings marked `PATTERN_MATCH` or `NEEDS_REVIEW` before treating them as confirmed issues. <br>


## Reference(s): <br>
- [Ralph Quick Security Check on ClawHub](https://clawhub.ai/dorukardahan/ralph-quick) <br>
- [Severity & Triage Reference](artifact/references/severity-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Structured text updates and a Markdown report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a final report to `.ralph-report.md`; optional focus and iteration parameters are interpreted by the agent.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
