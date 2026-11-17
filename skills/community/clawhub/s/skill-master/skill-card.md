## Description:

Meta-skill for skill selection and routing that provides a decision tree, keyword triggers, and guidance on combining multiple skills for complex workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[netanel-abergel](https://clawhub.ai/user/netanel-abergel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Skill Master to choose the appropriate skill for a user request, understand the available skill library, and combine skills for multi-step workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mandatory persistent logging of request triggers and context can expose sensitive prompt or workflow information in a shared analytics file.

Mitigation: Make analytics opt-in, redact trigger and context values before storage, and avoid installing as-is where prompts may contain sensitive data or multiple users can read the analytics file.

Risk: The analytics snippet appends JSON through shell interpolation, which can mishandle untrusted request text.

Mitigation: Write analytics through a safe structured logger or JSON serializer instead of interpolating user-controlled text into an echo command.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/netanel-abergel/skills/skill-master)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with tables, decision trees, workflow examples, and inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a required analytics logging step and depends on the skill-analytics skill.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
