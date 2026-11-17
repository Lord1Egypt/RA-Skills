## Description:

Automates Twitter/X posting, engagement, direct messages, follows, and profile or post lookup through the inference.sh CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[okaris](https://clawhub.ai/user/okaris)

### License/Terms of Use:


## Use Case:

Developers and social media operators use this skill to run Twitter/X workflows from an agent, including text posts, media posts, likes, retweets, direct messages, follows, deletions, and lookup actions. It is suited to automation where the user has authorized the connected X account and approves account-impacting actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install path asks users to run a remote shell installer.

Mitigation: Prefer a manual or pinned CLI install, verify checksums, and review the installer before execution.

Risk: The skill enables real account-impacting Twitter/X actions, including posting, deleting, DMs, following, liking, and retweeting.

Mitigation: Require explicit user confirmation and validate targets, content, and account identity before each account-impacting command.

Risk: Optional related-skill commands use unpinned npx package references.

Mitigation: Avoid those optional installs unless the source is trusted, pinned, and verified.

## Reference(s):

- [Twitter Automation skill page](https://clawhub.ai/okaris/skills/twitter-automation)
- [X.com Integration](https://inference.sh/docs/integrations/x)
- [X.com Integration Example](https://inference.sh/docs/examples/x-integration)
- [Apps Overview](https://inference.sh/docs/apps/overview)
- [Manual CLI checksums](https://dist.inference.sh/cli/checksums.txt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON CLI inputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may affect a connected Twitter/X account and should be gated by explicit user confirmation.]

## Skill Version(s):

0.1.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
