## Description: <br>
Analyzes changes between PyPI package versions and produces structured changelog evidence for upgrade summaries, version diffs, release notes, dependency changes, compatibility risks, and breaking-change review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[annangela](https://clawhub.ai/user/annangela) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to compare two PyPI package releases or a version range before upgrading dependencies. It helps summarize evidence from PyPI metadata, GitHub compare data when available, source archives, and package metadata changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make outbound network requests to PyPI and GitHub while resolving package metadata, release archives, commits, reviews, and file changes. <br>
Mitigation: Run it only in environments where those outbound requests are acceptable, and review warnings when GitHub compare data is unavailable or archive fallback is used. <br>
Risk: An optional GitHub token may be used to improve API reliability and rate-limit headroom. <br>
Mitigation: Provide only a short-lived, least-privilege read-only token through GITHUB_TOKEN or a secret manager, and avoid placing real tokens in persistent configuration, chat messages, logs, or command arguments. <br>
Risk: Generated summaries may be incomplete if source evidence is truncated, rate limited, or based on archive diffs instead of Git history. <br>
Mitigation: Tell users when truncation, rate limiting, repository lookup failure, or archive fallback appears in the structured JSON result. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/AnnAngela/pypi-package-changelog-generator) <br>
- [Output schema](artifact/references/output-schema.md) <br>
- [Failure modes](artifact/references/failure-modes.md) <br>
- [OpenClaw configuration](artifact/references/openclaw-config.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON evidence from the wrapper, typically summarized by the agent as concise Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a PyPI package name plus either an explicit from/to version pair or a version range.] <br>

## Skill Version(s): <br>
0.2.1 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
