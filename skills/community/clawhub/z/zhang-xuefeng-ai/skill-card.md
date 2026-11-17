## Description:

张雪峰AI助手 provides a direct Chinese-language college admissions, major selection, university analysis, and career planning advice persona.

This skill is ready for commercial/non-commercial use.

## Publisher:

[silbosu](https://clawhub.ai/user/silbosu)

### License/Terms of Use:

MIT-0

## Use Case:

Students, families, and education counselors use this skill to draft Chinese-language guidance about Gaokao application strategy, major selection, school tiers, postgraduate exams, civil-service options, employment direction, and career planning. The advice is framed as reference guidance and should be checked against current official admissions information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The external encrypted knowledge-base activation can write extracted files under the user's home directory, and a crafted archive could write files outside the intended knowledge-base directory.

Mitigation: Install and activate only knowledge-base packages from trusted sources, review before installation, and run the skill in a constrained environment when possible.

Risk: The skill uses a forceful Chinese-language education advice persona and can trigger on broad terms such as 985, 211, 考研, or 职业规划.

Mitigation: Treat responses as reference guidance, ask for the user's specific context, and verify admissions, employment, and policy details against official current sources.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/silbosu/skills/zhang-xuefeng-ai)
- [Publisher profile](https://clawhub.ai/user/silbosu)
- [Knowledge-base download site referenced by artifact](https://vdoob.com)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain text or Markdown-style Chinese responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require a separately downloaded encrypted knowledge-base package; broad Chinese education keywords can trigger the skill.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact files report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
