## Description:

Helps agents inspect Docker image manifests, initialize and destroy Docker buildx builders, and build and push multi-platform Docker images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lentiancn](https://clawhub.ai/user/lentiancn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to inspect container image tags and automate Docker buildx setup, teardown, and multi-platform image publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Build initialization can run an unpinned third-party binfmt container with privileged host access.

Mitigation: Use the skill only on a trusted, disposable, or dedicated Docker build host and pin the binfmt image by digest before use.

Risk: Build and push operations can publish images to the configured registry.

Mitigation: Review image tags, target registry, build arguments, provenance, and SBOM settings before invoking the push workflow.

Risk: Buildx cleanup can delete system-wide build cache when pruning is enabled.

Mitigation: Confirm the builder name and leave cache pruning disabled unless cache removal is intentional.

## Reference(s):

- [ClawHub Docker Skill Page](https://clawhub.ai/lentiancn/skills/skill-docker)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return Docker manifest JSON, success strings, error strings, and Docker build or registry side effects.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
