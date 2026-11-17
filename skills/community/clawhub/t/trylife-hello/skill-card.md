## Description:

Responds to greeting-style prompts with a simple hello response, a timestamped hello-world script output, or a selected Chinese motivational quote.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trylife](https://clawhub.ai/user/trylife)

### License/Terms of Use:

MIT-0

## Use Case:

Agents can use this skill to handle simple greeting inputs for users, including returning a hello message, running a local hello-world timestamp script, or selecting a Chinese motivational quote.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chinese quote responses may include embedded promotional text for a third-party app.

Mitigation: Review and curate the quote reference before deployment if promotional content is not appropriate for the target audience.

Risk: The hello-world interaction can run a local Python script to produce timestamped output.

Mitigation: Inspect the script before enabling the skill; current evidence shows only local timestamp formatting and printing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/trylife/skills/trylife-hello)
- [Skill instructions](artifact/SKILL.md)
- [Chinese motivational quote reference](artifact/references/praise.md)

## Skill Output:

**Output Type(s):** [text, shell commands]

**Output Format:** [Plain text responses, with a Python command path for the hello-world interaction.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The hello-world script output includes the local date and time when it runs.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
