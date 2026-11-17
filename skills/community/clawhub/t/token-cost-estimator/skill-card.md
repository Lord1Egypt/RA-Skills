## Description:

Estimate API token costs from OpenClaw session transcripts. Analyzes all agent sessions to calculate what you'd pay on per-token pricing vs subscription plans. Use when asked about API costs, token usage, billing estimates, or comparing Max/Pro plans to pay-per-use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[npfaerber](https://clawhub.ai/user/npfaerber)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to estimate token usage and compare likely API costs against subscription plans from local OpenClaw session transcript data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to read historical OpenClaw session transcripts across all agents, which may include secrets or sensitive personal or business data.

Mitigation: Run it only in trusted local environments and narrow the script to a specific agent or session folder before use when transcript sensitivity is uncertain.

Risk: Cost estimates may understate real usage because transcripts can miss system prompts, tool definitions, and internal retries.

Mitigation: Treat the output as a planning estimate and compare it against provider billing data before making purchasing or usage decisions.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with an inline Python script and cost estimate output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Estimates are approximate because transcripts can omit system prompts, tool definitions, and internal retries.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
