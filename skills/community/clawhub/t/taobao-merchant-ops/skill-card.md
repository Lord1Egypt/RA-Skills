## Description:

Provides customer-facing guidance and scripts for automating Taobao merchant operations, including business report capture, shop inspection, license activation, and local report parsing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenjiahui11](https://clawhub.ai/user/chenjiahui11)

### License/Terms of Use:

MIT-0

## Use Case:

External Taobao merchants and their operators use this skill to install and run a licensed automation package that captures Taobao business reports, performs shop inspections, and parses downloaded Excel reports into structured JSON for operational review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package handles Taobao account session state and license credentials.

Mitigation: Install only if the publisher is trusted, run from a non-admin environment, keep the project folder private, and do not share generated license or storage-state JSON files.

Risk: The package depends on remote license activation and runtime dependencies.

Mitigation: Prefer an HTTPS license server and pinned dependency installation before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenjiahui11/skills/taobao-merchant-ops)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON, files]

**Output Format:** [Markdown instructions with inline shell commands; scripts produce local JSON summaries and downloaded report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.9+, Playwright Chromium, a valid card key, and an authenticated Taobao browser session.]

## Skill Version(s):

1.0.8 (source: server release metadata; artifact files list 1.0.7)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
