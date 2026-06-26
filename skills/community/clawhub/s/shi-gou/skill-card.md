## Description: <br>
Monitors permission-denial events, detects prompt injection, path traversal, and dangerous commands, and generates security reports for potential threat alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lt8899789](https://clawhub.ai/user/lt8899789) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security-focused agent operators use Shi Gou to scan text or commands for common prompt-injection, path-traversal, and dangerous-command patterns, sanitize command examples, and generate simple security reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The sanitizer can return original matched secret values in its JSON metadata even when the displayed command is redacted. <br>
Mitigation: Do not log, paste, or share full sanitizer JSON output from real credentials; remove original-value metadata before retaining or transmitting results. <br>
Risk: Broad activation triggers may cause the skill to run for unrelated requests. <br>
Mitigation: Invoke scanning, reporting, or sanitization only for explicit security-review requests and review the generated findings before acting on them. <br>
Risk: Pattern-based checks can miss novel attacks or flag benign text that resembles a known pattern. <br>
Mitigation: Treat results as heuristic triage and pair them with code review, runtime safeguards, and dedicated security tooling for high-impact decisions. <br>


## Reference(s): <br>
- [Shi Gou ClawHub skill page](https://clawhub.ai/lt8899789/shi-gou) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [JSON objects and concise text summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scan results can include matched threat strings; sanitizer metadata may include original sensitive values.] <br>

## Skill Version(s): <br>
2.0.24 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
