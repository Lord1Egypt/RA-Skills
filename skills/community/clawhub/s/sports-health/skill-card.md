## Description:

AI运动健康助手 helps users record workouts in natural language, estimate calorie expenditure, generate personalized exercise plans, and produce visual HTML fitness reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal wellness users use this skill to log exercise activity, estimate calories, review exercise guidance, build weekly plans, and generate daily or weekly fitness reports. The skill is intended for general fitness support and not as a substitute for medical or professional coaching advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Profile and workout history may include health-related personal data saved as plaintext files in the workspace.

Mitigation: Use the skill only in trusted workspaces, avoid entering sensitive medical details, and provide clear delete, export, and opt-out practices for local records.

Risk: Generated HTML reports can expose sensitive fitness history and may carry unsafe scripting risk if built from untrusted or edited diary data.

Mitigation: Treat generated reports as sensitive, avoid opening reports from untrusted data, escape report fields, and bundle or pin Chart.js with integrity checks.

Risk: Exercise plans and calorie estimates are general guidance and may be inappropriate for users with medical conditions or injuries.

Mitigation: Keep medical disclaimers visible, advise users with health concerns to consult a clinician or qualified coach, and tell users to stop exercising if discomfort occurs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/sports-health)
- [Project homepage](https://github.com/bettermen/sports-health)
- [Publisher profile](https://clawhub.ai/user/bettermen)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with optional JSON-backed workout records and generated HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save local profile and diary data as plaintext JSON and generate browser-viewable HTML reports.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
