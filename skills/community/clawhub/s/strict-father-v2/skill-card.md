## Description:

Strict Father guides an agent through a Zi Wei Dou Shu twelve-palace self-analysis workflow that uses birth-profile inputs and chart output to surface personal blind spots in a deliberately direct style.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xcii](https://clawhub.ai/user/0xcii)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill for structured self-reflection: the agent asks for birth details, runs or interprets a Zi Wei Dou Shu chart, displays the chart, and then provides concise diagnostic guidance about behavior patterns and blind spots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer pattern can run mutable remote code from an unpinned branch.

Mitigation: Review local artifact files before installation, avoid one-line curl-to-bash installation, and pin any remote source and dependency versions used in deployment.

Risk: The workflow asks for and may reuse sensitive birth-profile details for charting and optional reminders.

Mitigation: Collect only the details needed for the requested analysis, explain any persistence or reminder behavior, and let the user decline or clear stored profile data.

Risk: The skill intentionally uses blunt personal diagnostic language that may be unsuitable for some users or contexts.

Mitigation: Frame outputs as reflective guidance rather than professional advice and keep user control over whether to continue after the chart is displayed.

## Reference(s):

- [Palace Pattern Matrix](references/palace-pattern-matrix.md)
- [ClawHub Skill Page](https://clawhub.ai/0xcii/skills/strict-father-v2)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with optional structured JSON chart output and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-provided birth date, time, gender, and optional birthplace; daily reminders are optional and should be enabled only after user consent.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
