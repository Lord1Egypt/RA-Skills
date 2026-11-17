## Description:

Finds student flight discounts, under-26 fares, youth travel deals, and related travel booking options through FlyAI/Fliggy searches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

Students and budget travelers use this skill to ask an agent for student-eligible, under-26, flexible-date, or budget-capped flight options. The skill guides the agent to return Markdown results with booking links and student travel notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs agents to install and run an unpinned third-party FlyAI CLI globally.

Mitigation: Prefer manual, pinned, least-privilege installation and review the CLI before allowing an agent to execute it.

Risk: Travel search details may be shared with FlyAI/Fliggy, and user-derived itinerary values may be passed into shell command templates.

Mitigation: Confirm users are comfortable sharing travel details and validate command parameters before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/skills/student-deal)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with booking links and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Travel results should be sourced from FlyAI CLI output and include booking links when results are shown.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
