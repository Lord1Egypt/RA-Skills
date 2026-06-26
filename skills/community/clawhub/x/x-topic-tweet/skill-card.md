## Description: <br>
Researches a user-provided topic across the web and current social conversation, then drafts and publishes one X post in the user's voice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dishant0406](https://clawhub.ai/user/dishant0406) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People who manage an X account use this skill to research a topic, draft a concise post in their voice, publish it through an existing X session, and report what was posted and sourced. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish live public posts to X from the user's session without a clear final confirmation step. <br>
Mitigation: Require the agent to stop after drafting, show the exact tweet and any link, and wait for explicit user approval before publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dishant0406/x-topic-tweet) <br>
- [Research Checklist](references/research-checklist.md) <br>
- [Post Workflow](references/post-workflow.md) <br>
- [Human Voice](references/human-voice.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Concise X post text plus a Markdown completion report with topic, final post text, sources, link status, and tab-closure confirmation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Intended for one manual post per run; the skill requires web research, X context review, publication verification, and closing all x.com tabs.] <br>

## Skill Version(s): <br>
1.1.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
