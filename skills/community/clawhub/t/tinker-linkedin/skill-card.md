## Description:

Tinker LinkedIn lets an agent crawl LinkedIn profiles, search, connections, inbox, feed, and related account data through a user-shared signed-in LinkedIn browser tab.

This skill is ready for commercial/non-commercial use.

## Publisher:

[globalcaos](https://clawhub.ai/user/globalcaos)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to inspect LinkedIn account, profile, search, connection, inbox, feed, company, and post information from an explicitly shared LinkedIn tab. It can also draft or send a LinkedIn message only when the caller provides per-action consent for the exact conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill operates a signed-in LinkedIn browser tab and can read account, profile, inbox, feed, and related LinkedIn data.

Mitigation: Install only when that access is acceptable, share only the intended LinkedIn tab, and unshare the tab to stop access.

Risk: LinkedIn automation may put the user's LinkedIn account at risk even when the skill is scoped.

Mitigation: Use the built-in pacing and daily ceilings, stop on LinkedIn challenges or rate limits, and avoid unsupported bulk outreach or evasion behavior.

Risk: The optional cache can store crawled third-party profile or company data on disk.

Mitigation: Leave LINKEDIN_CACHE off unless caching is needed, rely on the short TTL when enabled, and use session logout to remove local cache and counters.

Risk: Message sending is a write action to LinkedIn.

Mitigation: Require the exact conversation URN in the per-action consent flag before sending; without that consent, treat output as a draft only.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/globalcaos/skills/tinker-linkedin)
- [Publisher profile](https://clawhub.ai/user/globalcaos)
- [TinkerClaw project homepage](https://github.com/globalcaos/tinkerclaw)
- [LinkedIn session settings](https://www.linkedin.com/psettings/sessions)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI output from LinkedIn data requests.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node and a user-shared LinkedIn browser tab through the local OpenClaw relay.]

## Skill Version(s):

1.2.2 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
