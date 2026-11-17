## Description:

Search YouTube for videos matching the user's query. Use when the user asks to use YouTube for this purpose.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruchir17-cmd](https://clawhub.ai/user/ruchir17-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to open Brave and search YouTube for videos that match a user-provided query. It is limited to navigation and search verification, with explicit safeguards against credential entry or account changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: YouTube searches may run in an existing Brave session, so YouTube or Google may associate the query with the logged-in account.

Mitigation: Review queries before execution, reuse authenticated sessions only when appropriate, and stop at login or credential prompts.

Risk: Browser navigation could reach a login page or other page requiring sensitive input.

Mitigation: Do not enter passwords, authentication codes, API keys, payment details, or other credentials; stop and tell the user when authentication is required.

## Reference(s):

- [ClawHub search-youtube skill page](https://clawhub.ai/ruchir17-cmd/skills/search-youtube)
- [YouTube homepage](https://www.youtube.com/)
- [YouTube search URL prefix](https://www.youtube.com/results?search_query=)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Text guidance for browser navigation and verification]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces navigation/search instructions for an agent; it does not submit forms, modify accounts, or handle credentials.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
