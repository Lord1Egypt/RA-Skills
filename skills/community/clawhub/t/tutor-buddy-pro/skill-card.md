## Description: <br>
Tutor Buddy Pro guides homework help with Socratic step-by-step explanations, study plans, adaptive quizzes, progress tracking, and learner-style adaptation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nollio](https://clawhub.ai/user/nollio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students and learners use this skill for guided homework support, quiz practice, personalized study planning, and progress summaries across core academic subjects. Parents or self-directed learners may also use its dashboard companion materials to review local learning progress. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive learner progress files may be created locally, including profile, quiz history, session log, and study plan data. <br>
Mitigation: Install only in workspaces where local learner data storage is acceptable, keep restrictive file permissions, and avoid collecting more identifying information than the skill requires. <br>
Risk: The dashboard companion materials describe a future sync path that could move learner progress off-device. <br>
Mitigation: Do not enable or implement dashboard sync unless it is explicit opt-in, uses an authenticated HTTPS endpoint, minimizes data, defines retention and deletion controls, and obtains parent or guardian consent where appropriate. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nollio/tutor-buddy-pro) <br>
- [README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Security guidance](artifact/SECURITY.md) <br>
- [Dashboard companion specification](artifact/dashboard-kit/DASHBOARD-SPEC.md) <br>
- [Tutor configuration](artifact/config/tutor-config.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown tutoring responses, JSON study and progress files, and optional shell commands for setup or progress reporting.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local learner profile, quiz history, session log, study plan, and report files when the host agent follows the skill workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
