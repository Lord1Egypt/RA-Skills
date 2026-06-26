## Description: <br>
Workbuddy Smart Learning learns from task feedback and behavior signals to identify recurring work patterns, distill reusable templates, and provide adaptive alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wwenie](https://clawhub.ai/user/wwenie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to collect task feedback, analyze implicit work signals, surface high-frequency task patterns, and generate reusable process templates or caution rules for future work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persists task history, feedback, timing, tool usage, and derived templates locally, which may include sensitive work context. <br>
Mitigation: Run it only in the intended workspace, review .workbuddy/memory contents, and delete memory files that should no longer be retained. <br>
Risk: Free-form feedback notes or task summaries may capture secrets or sensitive business details. <br>
Mitigation: Avoid entering secrets or confidential details in notes, tags, and task summaries; redact sensitive data before recording feedback. <br>
Risk: Templates and avoidance rules derived from limited feedback can encode inaccurate or stale work patterns. <br>
Mitigation: Review generated recommendations, templates, and avoidance rules before relying on them for future agent behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wwenie/workbuddy-smart-learning) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown and plain text reports, JSON memory records, and YAML template or avoidance-rule files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists learned feedback, task profiles, signals, patterns, and templates under the configured workspace .workbuddy/memory directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
