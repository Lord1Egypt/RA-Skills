## Description: <br>
BotLearn Reminder delivers daily BotLearn 7-step onboarding reminders and quickstart summaries when a user starts BotLearn learning or asks about tutorial progress. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asterisk622](https://clawhub.ai/user/asterisk622) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to receive daily BotLearn onboarding reminders, fetch current BotLearn quickstart pages, summarize the relevant tutorial content, and track reminder progress locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to start recurring BotLearn web fetches and write local progress state. <br>
Mitigation: Use it only when daily BotLearn reminders are desired, and require confirmation before setup, recurring fetching, or state changes. <br>
Risk: Referenced setup files and scripts are not included in the artifact for review. <br>
Mitigation: Ask the publisher to include the setup files, scripts, and exact memory-file documentation before deployment. <br>
Risk: The trigger set includes broad learning and quickstart phrases that may activate outside a BotLearn-specific workflow. <br>
Mitigation: Narrow triggers to BotLearn-specific phrases before enabling the skill in shared or production agent environments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/asterisk622/xiaoding-botlearn-reminder) <br>
- [BotLearn 7-step overview](https://botlearn.ai/7-step) <br>
- [BotLearn localized quickstart pages](https://botlearn.ai/{lang}/quickstart/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reminder text with fetched tutorial summaries, URLs, and occasional shell command references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Daily heartbeat behavior, language-aware reminder output, and local progress state updates are described by the skill.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
