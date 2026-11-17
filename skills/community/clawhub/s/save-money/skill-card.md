## Description:

Auto-detects task complexity for Claude models and routes simple requests to Haiku while escalating complex requests to Sonnet to reduce model costs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[peterokase42](https://clawhub.ai/user/peterokase42)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to reduce Claude model usage costs by answering simple tasks with a cheaper model and escalating complex work to a stronger model.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can forward full prompts, including sensitive business or personal content, to a Sonnet session without clear user confirmation.

Mitigation: Review the skill before installation and require explicit user consent or disclosure before forwarding sensitive prompts.

Risk: The skill can hide model switching unless the user asks, making it harder to understand where a request was handled.

Mitigation: Configure visible disclosure for model escalation or document the routing behavior for users before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/peterokase42/skills/save-money)
- [Publisher Profile](https://clawhub.ai/user/peterokase42)
- [Project Homepage](https://github.com/peterann/save-money)

## Skill Output:

**Output Type(s):** [Guidance, Text]

**Output Format:** [Markdown guidance and concise text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May route complex prompts to a stronger Claude model instead of answering directly.]

## Skill Version(s):

4.2.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
