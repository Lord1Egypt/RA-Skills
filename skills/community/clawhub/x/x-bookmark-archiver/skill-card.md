## Description:

Fetches X bookmarks, categorizes them by URL, optionally generates OpenAI summaries, and saves organized markdown archives in an OpenClaw workspace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iamadig](https://clawhub.ai/user/iamadig)

### License/Terms of Use:

MIT

## Use Case:

Developers and knowledge workers use this skill to archive X bookmarks into local, categorized markdown files for later retrieval, review, and note-taking. It is useful when a user wants a repeatable CLI workflow that avoids reprocessing already archived bookmarks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes private X bookmarks through bird.

Mitigation: Install and run it only in workspaces where that bookmark access is acceptable, and review generated archive and state file permissions.

Risk: When OPENAI_API_KEY is set, bookmark URLs and tweet text may be sent to OpenAI for summarization.

Mitigation: Run without OPENAI_API_KEY when local fallback summaries are preferred, or review bookmark contents before enabling AI enrichment.

Risk: The security guidance flags the t.co expansion behavior as needing a fix before use in sensitive networks.

Mitigation: Avoid using the skill in sensitive network environments until URL expansion behavior has been reviewed and constrained.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/iamadig/skills/x-bookmark-archiver)
- [bird CLI](https://github.com/steipete/bird)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown files with YAML frontmatter plus console status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates categorized files under X-knowledge and stores pending and processed bookmark state as JSON.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
