## Description: <br>
Run a conversational task list with Inbox, Today, Upcoming, recurring tasks, waiting items, projects, and review loops that stay trustworthy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Users who want conversational task management use this skill to capture work quickly, clarify next actions, maintain stable task views, track recurring and waiting work, and run daily or weekly reviews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task details and preferences may be stored locally under ~/task-list/ when continuity is enabled. <br>
Mitigation: Enable local continuity only with user consent and avoid putting secrets or unrelated private information in tasks. <br>
Risk: Automatic activation around tasks or follow-ups may be broader than some users expect. <br>
Mitigation: Choose explicit or manual activation when the user does not want the skill to appear for general task and follow-up conversations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/task-list) <br>
- [Task List Homepage](https://clawic.com/skills/task-list) <br>
- [Setup](setup.md) <br>
- [Workspace Format](workspace-format.md) <br>
- [Capture and Clarify](capture-and-clarify.md) <br>
- [Views and Sorting](views-and-sorting.md) <br>
- [Recurrence and Waiting](recurrence-and-waiting.md) <br>
- [Review Rhythm](review-rhythm.md) <br>
- [Memory Template](memory-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration, Files] <br>
**Output Format:** [Conversational text and Markdown task-list records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local Markdown files under ~/task-list/ when the user consents to continuity.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
