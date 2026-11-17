## Description:

RetainCraft is an AI learning tutor that combines FSRS-5 spaced repetition, active recall, Feynman checks, interleaved practice, causal questioning, learning contracts, burnout detection, and progress reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaixiad](https://clawhub.ai/user/kaixiad)

### License/Terms of Use:

MIT-0

## Use Case:

External users, learners, and developers use this skill to run structured study sessions with diagnostic testing, customized learning paths, spaced repetition review, practice testing, simulations, and progress tracking. It is intended for agent-assisted tutoring workflows where local study state and reminder behavior are acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create persistent daily and weekly reminder behavior and may infer messaging targets from session metadata.

Mitigation: Review reminder setup before installation, confirm the target channel, and disable or remove reminders if persistent notifications are not acceptable.

Risk: The skill stores study progress and learning state under ~/learn.

Mitigation: Use the skill only where local storage of learning topics, progress, profiles, and review history is acceptable; review or delete that directory as needed.

Risk: The tutoring workflow uses web search for question generation and fact-checking.

Mitigation: Avoid submitting sensitive, confidential, or regulated study material to search-backed tutoring steps, or redact it before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kaixiad/skills/retaincraft)
- [Full workflow](artifact/references/full-workflow.md)
- [Scenario library](artifact/scripts/scenarios.md)
- [Academic citations and effect sizes](artifact/scripts/evidence.md)
- [Output templates](artifact/scripts/templates.md)
- [Learning templates data](artifact/learning-templates.json)
- [Donoghue and Hattie 2021 meta-analysis](https://doi.org/10.3389/feduc.2021.581216)
- [Dunlosky et al. 2013 learning techniques review](https://doi.org/10.1177/1529100612453266)
- [Kestin et al. 2025 AI tutoring RCT](https://doi.org/10.1038/s41598-025-97652-6)
- [Su et al. 2023 spaced repetition scheduling](https://doi.org/10.1109/TKDE.2023.3251721)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-like status outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces learning plans, tests, review prompts, local progress updates, reminder instructions, and study reports.]

## Skill Version(s):

1.4.5 (source: server release metadata; artifact frontmatter lists 1.4.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
