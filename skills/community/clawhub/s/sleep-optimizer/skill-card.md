## Description:

Sleep Optimizer collects sleep timing, nap, daytime sleepiness, and life-stage inputs to generate evidence-informed sleep assessments, schedules, charts, and an eight-week improvement plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[55zhang](https://clawhub.ai/user/55zhang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to collect sleep routine details and produce a personalized sleep improvement report for common sleep-quality and schedule-adjustment questions. The skill is wellness-oriented self-help support and should not be treated as medical diagnosis or treatment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can collect and save personal sleep and health-adjacent details in local reports.

Mitigation: Use non-sensitive output locations, avoid sharing reports broadly, and avoid saving reports unless the user explicitly wants a file.

Risk: The skill can auto-activate on broad sleep-related questions and collect more personal context than a user may expect.

Mitigation: Prefer explicit invocation or confirm the user wants a structured sleep analysis before collecting detailed sleep, daytime function, or life-stage information.

Risk: The local Node.js script supports file-backed drowsiness input, which can read local files selected by path.

Mitigation: Use file inputs only when the user chose the file, verify the path before execution, and avoid using unrelated or sensitive files.

Risk: The generated recommendations may be mistaken for clinical advice.

Mitigation: Keep the artifact's medical caveat visible and direct users to appropriate care for persistent insomnia, severe daytime sleepiness, suspected apnea, restless legs symptoms, or mood concerns.

## Reference(s):

- [Sleep Optimizer Skill Definition](artifact/SKILL.md)
- [Sleep Science References](artifact/references/sleep-science-references.md)
- [Lifestyle Sleep References](artifact/references/lifestyle-sleep-references.md)
- [Sleep Diary Template](artifact/assets/sleep-diary-template.md)
- [ClawHub Skill Page](https://clawhub.ai/55zhang/skills/sleep-optimizer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with inline text charts; optional companion SVG chart file when an output path is provided]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The Node.js helper can write a local Markdown report and matching .chart.svg file.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 2.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
