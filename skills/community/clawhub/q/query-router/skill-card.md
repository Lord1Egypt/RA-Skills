## Description:

Classifies prompts by prefix, content type, and complexity to recommend or attempt a model route.

This skill is ready for commercial/non-commercial use.

## Publisher:

[walterwkchoy](https://clawhub.ai/user/walterwkchoy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to classify prompts and select a recommended model from explicit prefixes, detected content type, or estimated complexity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Model switching safeguards may be overstated for reliable routing, rollback, and locking.

Mitigation: Treat outputs as recommendations, prefer dry-run or classify-only workflows, and manually verify any model change before relying on it.

Risk: Prompt prefixes are stored in local plaintext audit logs.

Mitigation: Avoid routing secrets or private data unless audit logging is disabled or changed and local logs are access-controlled.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/walterwkchoy/skills/query-router)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text or JSON command-line output with model recommendations and routing rationale.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local plaintext audit logs that include prompt prefixes.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
