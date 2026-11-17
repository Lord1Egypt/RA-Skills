## Description:

Ai Coach generates Chinese-language personalized triathlon training plans from TrainingPeaks, Garmin, weather, and race-goal data, with daily plan and review outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ciaefengye](https://clawhub.ai/user/ciaefengye)

### License/Terms of Use:

MIT-0

## Use Case:

External triathlon athletes use this skill to generate and adjust daily swim, bike, run, rest, and race-preparation plans from personal training goals and connected account data. Agents can use it to produce daily coaching guidance, training reviews, configuration steps, and command examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles health, training, and account data with under-scoped storage and sharing behavior.

Mitigation: Review before installing; use private per-user storage for tokens and caches, define deletion controls, and limit connected-account permissions before using real data.

Risk: Credential and API-key handling is security-sensitive, including Garmin password storage and IMA API keys.

Mitigation: Replace password storage with a secure credential store, remove bundled API keys, rotate any exposed credentials, and require user-provided credentials through protected configuration.

Risk: Generated training plans can influence physical training load and recovery decisions.

Mitigation: Treat outputs as coaching support, review high-intensity or recovery-changing recommendations, and avoid relying on the skill as medical or professional sports advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ciaefengye/skills/triathlon-ai-coach)
- [TrainingPeaks login](https://tpstack.trainingpeaks.com)
- [IMA note import API endpoint](https://ima.qq.com/openapi/note/v1/import_doc)
- [Weather data endpoint](https://wttr.in/Beijing?format=j1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown daily plans, console text, JSON and YAML configuration snippets, Python code examples, and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language output; may write local JSON or Markdown files and call external account, note, and weather APIs when configured.]

## Skill Version(s):

3.2.0 (source: server release evidence and target metadata; artifact/config.json reports 3.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
