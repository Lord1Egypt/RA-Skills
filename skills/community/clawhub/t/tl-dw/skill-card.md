## Description:

Extracts YouTube captions and helps an agent summarize video transcripts into concise overviews with main points, arguments, and conclusions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vovavvk](https://clawhub.ai/user/vovavvk)

### License/Terms of Use:

AGPL-3.0

## Use Case:

Developers, researchers, analysts, and end users can use this skill to extract available YouTube captions and summarize video content without watching the full video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cookie support can expose sensitive browser session data if exported cookies are stored carelessly.

Mitigation: Use cookies only when necessary, treat them like passwords, store them outside the skill directory with restrictive permissions, prefer a dedicated account, and delete them after use.

Risk: The transcript extractor disables TLS certificate checks while using network tools.

Mitigation: Remove the TLS certificate bypass before using cookies or running the skill on untrusted networks.

Risk: Runtime package installation without pinned, hash-verified dependencies can introduce supply-chain risk.

Mitigation: Install dependencies as a non-privileged user and consider pinned, hash-verified packages.

Risk: Summaries depend on the availability and quality of YouTube captions, including auto-generated captions that may contain errors.

Mitigation: Treat summaries as aids for review and verify important claims against the source video or transcript.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vovavvk/skills/tl-dw)
- [Attribution](artifact/ATTRIBUTION.md)
- [Original TL;DW project](https://github.com/stong/tldw)
- [TL;DW website](https://tldw.tube)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown summary with optional JSON transcript metadata from the extraction script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Depends on available YouTube captions and may use a local transcript cache.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
