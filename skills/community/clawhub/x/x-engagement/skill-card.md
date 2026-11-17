## Description:

X Engagement helps an agent support X/Twitter operations through onboarding, persona learning, Browser Relay assisted browsing, memory-backed comment suggestions, manual reminders, follow recommendations, and interaction review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasoncodespace](https://clawhub.ai/user/jasoncodespace)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to plan and review X/Twitter engagement workflows, generate persona-aware comment candidates, inspect recent interactions, and prepare browser actions that require explicit user confirmation before posting, liking, or following.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated browser control can act on a user's X/Twitter account.

Mitigation: Use a dedicated browser profile and require explicit confirmation before every like, follow, comment, or send action.

Risk: Unpinned bare npx commands can execute changing third-party Browser Relay CLI code.

Mitigation: Pin and verify browser-relay-cli before use instead of running unversioned commands.

Risk: The memory system is designed to retain comment history, preferences, and personal facts, including some long-lived records.

Mitigation: Periodically inspect or delete the memory directory and run cleanup in preview mode before applying changes.

Risk: Playbook updates can change future engagement behavior.

Mitigation: Require explicit user review and confirmation before applying Playbook changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jasoncodespace/skills/x-engagement)
- [Browser Relay repository](https://github.com/jasonCodeSpace/browser-relay)
- [README](artifact/README.md)
- [Browser operations](artifact/docs/browser-operations.md)
- [Comment rules](artifact/docs/comment-rules.md)
- [Manual reminders and maintenance](artifact/docs/cron-jobs.md)
- [Memory system](artifact/docs/memory-system.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON snippets, shell command examples, and browser-operation instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces proposals and operational instructions for an agent; authenticated X/Twitter write actions are expected to remain user-confirmed.]

## Skill Version(s):

4.1.3 (source: server release evidence; artifact frontmatter reports 4.2.0-local)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
