## Description:

Draft, review, and schedule distinct social posts with the TimeToPost MCP. Use when asked to plan a social calendar, draft a post or thread, check approval drafts, choose a posting time, or schedule content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[melmayssonowen](https://clawhub.ai/user/melmayssonowen)

### License/Terms of Use:

MIT-0

## Use Case:

Social media managers, creators, and teams use this skill to plan social calendars, draft distinct posts for connected accounts, review pending drafts, and schedule content through TimeToPost. It can use account history for timing suggestions and requires approval of the exact copy, account, and time before scheduling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Approving a draft schedules it for a connected social account, and the security review notes that its coverage is incomplete because a referenced path could not be resolved.

Mitigation: Confirm the intended workspace and OAuth connection, review the exact copy, account, and time, and approve only that specific draft. Treat the benign scan verdict as limited by its incomplete coverage.

## Reference(s):

- [TimeToPost](https://go.timetopost.co/mkt-clawhub)
- [TimeToPost hosted MCP endpoint](https://api.timetopost.co/mcp)
- [Setup](artifact/references/setup.md)
- [Draft and approval lifecycle](artifact/references/approval-workflow.md)
- [Platform limits and timing fallback](artifact/references/platform-limits.md)
- [Voice matching](artifact/references/voice-rules.md)
- [ClawHub skill page](https://clawhub.ai/melmayssonowen/skills/timetopost-social-scheduler)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, API Calls]

**Output Format:** [Platform-specific social post drafts, threads, and scheduling guidance in text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates distinct versions for connected accounts; scheduling requires explicit approval of the exact content, account, and time.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release record)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
