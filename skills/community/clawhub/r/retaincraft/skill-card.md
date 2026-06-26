## Description: <br>
RetainCraft helps agents run evidence-based learning sessions with FSRS-5 spaced repetition, active recall, Feynman checks, interleaved practice, causal questioning, diagnostic tests, progress tracking, burnout checks, and reminder workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaixiad](https://clawhub.ai/user/kaixiad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to structure personalized study plans, generate diagnostic tests and learning paths, run module learning loops, and maintain spaced-repetition review state across topics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent reminder and weekly report jobs may continue sending messages after installation or setup. <br>
Mitigation: Verify the exact reminder channel and recipient before enabling reminders, and remove the retaincraft-reminder and retaincraft-weekly-report cron jobs when ongoing messages are not desired. <br>
Risk: Learning history is stored locally under ~/learn and may also be summarized in platform memory or notes. <br>
Mitigation: Install only where local study records and platform memory use are acceptable, and review or delete stored progress data according to the user's retention needs. <br>
Risk: Generated learning content, tests, and factual judgments may depend on web search and agent interpretation. <br>
Mitigation: Require source links for factual learning content and have users review important study materials, test answers, and recommendations before relying on them. <br>


## Reference(s): <br>
- [RetainCraft ClawHub release page](https://clawhub.ai/kaixiad/retaincraft) <br>
- [Full workflow reference](references/full-workflow.md) <br>
- [Academic citations and effect sizes](scripts/evidence.md) <br>
- [Scenario library examples](scripts/scenarios.md) <br>
- [Donoghue & Hattie 2021 meta-analysis](https://doi.org/10.3389/feduc.2021.581216) <br>
- [Dunlosky et al. 2013 learning techniques review](https://doi.org/10.1177/1529100612453266) <br>
- [Kestin et al. 2025 AI tutoring RCT](https://doi.org/10.1038/s41598-025-97652-6) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Text] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-backed local learning state] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3; stores study progress under ~/learn and may use platform notes, web search, and scheduled reminders.] <br>

## Skill Version(s): <br>
1.4.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
