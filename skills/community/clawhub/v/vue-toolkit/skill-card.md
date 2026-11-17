## Description:

Helps developers identify and avoid common Vue mistakes, including reactivity traps, ref/reactive misuse, Composition API issues, and related configuration pitfalls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to review Vue projects for common reactivity, ref/reactive, Composition API, performance, and configuration mistakes. It is best treated as an automation aid whose suggested commands, file edits, and API-related steps should be reviewed before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad read, write, command, API, and integration abilities that exceed a narrow Vue troubleshooting scope.

Mitigation: Run it in a limited workspace, review proposed commands and file changes before execution, and avoid granting access outside the project being inspected.

Risk: API keys, project secrets, or sensitive code could be exposed when using broad automation or integration workflows.

Mitigation: Do not provide secrets unless necessary, keep credentials in environment variables, and remove sensitive data from prompts and logs.

Risk: Generated Vue fixes or performance recommendations may be incorrect or unsuitable for the application.

Mitigation: Review suggested code changes, run the project's Vue test and build workflows, and apply changes incrementally.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown or JSON snippets, with shell commands and configuration when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose read, write, command, API, and integration actions depending on the user task]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
