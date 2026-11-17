## Description:

Summarize URLs or files with the summarize CLI (web, PDFs, images, audio, YouTube).

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to summarize web pages, local documents, images, audio files, and YouTube links through the summarize CLI. It is useful when an agent needs concise text or JSON summaries from heterogeneous input sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected URLs, local files, transcripts, images, or audio may be processed remotely through SkillBoss API Hub and downstream model or scraping services.

Mitigation: Do not submit confidential, restricted, private, or regulated content unless organizational policy permits that remote processing.

Risk: The CLI is installed from the third-party Homebrew tap steipete/tap/summarize.

Mitigation: Review and approve the tap and package source before installation in managed or production environments.

## Reference(s):

- [summarize homepage](https://summarize.sh)
- [ClawHub skill page](https://clawhub.ai/tobeyrebecca/skills/toby-summarize)
- [SkillBoss API Hub endpoint](https://api.skillbossai.com/v1/pilot)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell command examples; the CLI can also produce machine-readable JSON summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output length and token budget can be adjusted with CLI flags such as --length and --max-output-tokens.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
