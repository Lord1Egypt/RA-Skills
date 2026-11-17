## Description:

YoudaoNote News analyzes recently favorited Youdao Cloud Notes to identify topics and push current related news on request or on a daily schedule.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lephix](https://clawhub.ai/user/lephix)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn recently favorited Youdao Cloud Notes into concise news briefings and to configure optional daily delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Favorite notes may contain sensitive personal, work, health, financial, or confidential topics.

Mitigation: Review the notes account and expected topics before installation, and avoid using the skill with sensitive note collections.

Risk: Derived note topics may be sent to external search services.

Mitigation: Use only approved search providers and avoid queries that reveal confidential or identifying information.

Risk: Helper scripts have local exposure risks for temporary data and the optional Perplexity API key.

Mitigation: Run the skill in a trusted local environment, protect environment variables, and clear temporary files according to local security policy.

Risk: Scheduled daily pushes may run without fresh user intent.

Mitigation: Enable scheduled delivery only intentionally and review or disable the cron job when recurring news pushes are no longer wanted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lephix/skills/youdaonote-news)
- [Perplexity API settings](https://www.perplexity.ai/settings/api)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown news briefing with a summary table and command-oriented setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Briefings are based on recent favorite notes, up to five topics, and up to five current articles per topic.]

## Skill Version(s):

1.7.8 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
