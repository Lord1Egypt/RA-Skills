## Description:

A random inspirational tweet from curated collections of hand-picked wisdom by tech leaders, founders, and philosophers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[acailic](https://clawhub.ai/user/acailic)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use Tweetnugget to return a concise inspirational quote selected from local curated JSON collections, optionally filtered by a requested topic tag.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A user-supplied topic may be interpolated into a Bash command for tag filtering.

Mitigation: Quote or validate topic input before execution, map requests to known tags, or call the Python script with argument arrays rather than shell-interpolated command text.

Risk: Curated quote content may be inaccurate, misattributed, or outdated.

Mitigation: Review collection entries and source URLs before relying on quote attribution or adding new collections.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/acailic/skills/tweetnugget)
- [Software Lead Weekly quote collection](references/swlw-tweets.json)
- [Twitter Wisdom quote collection](references/twitter-quotes.json)
- [Stoic Quotes collection](references/stoic-quotes.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown quote text with attribution; setup and operation guidance may include inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Quote selection is local and randomized; filtered mode performs partial tag matching and falls back to a random quote when no tag matches.]

## Skill Version(s):

1.2.0 (source: ClawHub release metadata and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
