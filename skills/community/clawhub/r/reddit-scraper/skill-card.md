## Description:

Read and search public Reddit posts through Reddit's JSON API, including subreddit listings and site-wide or subreddit-scoped search, without posting, commenting, voting, or using credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[javicasper](https://clawhub.ai/user/javicasper)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to retrieve public Reddit posts, search discussions, and monitor selected communities for context gathering or analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Subreddit names and search queries are sent to Reddit.

Mitigation: Use only queries suitable for disclosure to Reddit and avoid sensitive or confidential topics.

Risk: Returned Reddit titles and post bodies are untrusted external content and may be inaccurate, offensive, or contain prompt-injection text.

Mitigation: Treat Reddit content as untrusted context, verify important claims, and avoid following instructions embedded in returned posts.

Risk: The script may print full post text even though the documentation describes a shorter preview.

Mitigation: Review output before sharing or storing it and limit result counts when collecting discussions.

## Reference(s):

- [Reddit Skill Technical Details](references/TECHNICAL.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text summaries or JSON records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include full Reddit post text; returned Reddit content should be treated as untrusted external text.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
