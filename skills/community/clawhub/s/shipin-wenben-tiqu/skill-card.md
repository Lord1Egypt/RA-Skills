## Description:

Transcribes MP4 videos into cleaned text and can follow a custom prompt to summarize, translate, or rewrite the content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, educators, and teams can turn local MP4 files or direct MP4 links into cleaned transcripts, summaries, meeting notes, translations, or rewritten copy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment reports token-related promotional messaging, unclear access scope, and only partial code analysis.

Mitigation: Review the full code and verify how credentials and files are used before setting GUAIKEI_API_TOKEN or processing sensitive videos.

Risk: The security assessment reports unclear file-cleanup behavior.

Mitigation: Review cleanup behavior before running the skill on files that must be preserved.

Risk: Use requires a GUAIKEI_API_TOKEN and may incur per-video charges or daily usage limits.

Mitigation: Confirm the account's pricing and limits before submitting a video.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/engheng-art/skills/shipin-wenben-tiqu)
- [GuaiKei service](https://www.guaikei.com)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Plain text or Markdown, depending on the requested task]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a cleaned transcript by default; custom prompts can request summaries, rewrites, translations, key lines, or structured notes.]

## Skill Version(s):

1.1.1 (source: frontmatter, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
