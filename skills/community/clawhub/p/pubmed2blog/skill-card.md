## Description:

Convert PubMed research papers into SEO-optimized, patient-friendly healthcare blog articles using a discover-extract-generate pipeline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[holic101](https://clawhub.ai/user/holic101)

### License/Terms of Use:


## Use Case:

External users, healthcare content teams, and agents use this skill to find relevant PubMed studies, extract paper details, and generate accessible healthcare blog articles or saved drafts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default workflow suggests recurring cron-based content generation, which can run unexpectedly or use credentials, storage, and paid provider calls without adequate review.

Mitigation: Require explicit human approval for any cron command, schedule, credential source, output location, cost expectation, and removal process before enabling recurring execution.

Risk: The installation command uses a mutable global npm install, so future installs may resolve to different code and affect the broader agent environment.

Mitigation: Prefer a pinned CLI version installed in a locally isolated workspace before use.

Risk: Generated healthcare content may be inaccurate, incomplete, or unsuitable for patient-facing publication without domain review.

Mitigation: Review source paper extraction and generated article text with qualified editorial or clinical oversight before publication.

## Reference(s):

- [ClawHub skill page: pubmed2blog](https://clawhub.ai/holic101/skills/pubmed2blog)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and CLI-oriented guidance with optional saved article files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on selected article type, language options, PubMed paper metadata, and configured AI provider.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
