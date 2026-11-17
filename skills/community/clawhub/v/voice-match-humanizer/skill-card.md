## Description:

Voice Match Humanizer builds local writing voice profiles from user-provided samples, scores AI-like patterns, and rewrites text to match a selected saved profile.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chris](https://clawhub.ai/user/chris)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, marketers, founders, and other ClawHub users use this skill to create and manage local voice profiles, evaluate AI-pattern risk, and rewrite drafts so they match an established personal writing style.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-supplied profile or platform names may be used for local file operations.

Mitigation: Use simple profile and platform names and confirm create, update, or delete operations target files under the local profiles/ directory.

Risk: Writing samples may contain unpublished, internal, or personal content.

Mitigation: Avoid sensitive samples unless the runtime's file-access controls are trusted, and do not quote large sample blocks in third-party-facing outputs.

Risk: The skill can be misused as detector-evasion framing.

Mitigation: Decline requests to bypass classroom AI checkers or academic-integrity systems and redirect to legitimate personal voice matching.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chris/skills/voice-match-humanizer)
- [README](README.md)
- [Changelog](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown responses and local Markdown voice profile files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, update, compare, or delete local profile files under profiles/ when the user requests profile management.]

## Skill Version(s):

1.1.1 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
