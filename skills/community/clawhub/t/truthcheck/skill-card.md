## Description:

Truthcheck helps agents verify claims, assess URL trustworthiness, and trace claim origins with the TruthCheck CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baiyishr](https://clawhub.ai/user/baiyishr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and agents use Truthcheck to fact-check claims, evaluate source or URL trustworthiness, and trace claims to their origin. It can return human-readable analysis and optional structured output for verification workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install instructions fetch an unpinned external `truthcheck` package, so the installed package may change after this review.

Mitigation: Confirm the intended package source and version before installation, prefer a pinned version, and use an isolated environment.

Risk: Truthcheck commands may use API keys or local files for checks selected by the user.

Mitigation: Provide credentials and file paths only for checks the user explicitly intends to run.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/baiyishr/skills/truthcheck)
- [Publisher Profile](https://clawhub.ai/user/baiyishr)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands; optional JSON from TruthCheck CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can depend on the installed truthcheck package, selected search provider, selected LLM, local files supplied by the user, and configured API keys.]

## Skill Version(s):

0.4.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
