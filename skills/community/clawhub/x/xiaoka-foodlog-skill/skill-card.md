## Description: <br>
Records meal descriptions with the Xiaoka Health API, including breakfast, lunch, dinner, snacks, and today's food log, and returns calorie details and diet suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baojuqiang](https://clawhub.ai/user/baojuqiang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to bind a Xiaoka Health account, send food descriptions to the Xiaoka Health service, record meals, and review today's logged intake. The skill is intended for personal diet logging workflows that need API-backed calorie and ingredient details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meal descriptions and diet details may be sent to the Xiaoka Health remote API because the skill has broad auto-trigger behavior for food-related messages. <br>
Mitigation: Install only when intentional food logging is desired, use explicit logging phrases, and avoid casual food discussion while the skill is enabled. <br>
Risk: A local Xiaoka Health API key is stored for account binding and could continue to authorize requests after the user stops using the skill. <br>
Mitigation: Delete or revoke the stored API key when the skill is no longer needed or if account binding should be reset. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/baojuqiang/xiaoka-foodlog-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text with inline shell commands and API response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq; stores a local API key credential for Xiaoka Health account binding.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
