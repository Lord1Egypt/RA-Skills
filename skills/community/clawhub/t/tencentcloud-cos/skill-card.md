## Description:

Integrates Tencent Cloud COS and CI for object storage, media processing, search, and knowledge-base workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawnminh](https://clawhub.ai/user/shawnminh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to manage COS objects and buckets and run Tencent CI processing, search, and knowledge-base workflows.

### Deployment Geography for Use:

Global; Tencent Cloud service and feature availability varies by region.

## Known Risks and Mitigations:

Risk: HTML previews may allow code injection.

Mitigation: Disable HTML previews during evaluation and prefer a version that fixes preview escaping.

Risk: Saved cloud credentials receive weaker protection than promised.

Mitigation: Use temporary credentials limited to a test bucket and avoid saving keys.

Risk: Generated links and preview files may expose private access.

Mitigation: Treat them as private access tokens; require explicit approval for ACL changes, service shutdowns, and persistent indexing scope.

## Reference(s):

- [Tencent Cloud COS skill page](https://clawhub.ai/shawnminh/skills/tencentcloud-cos)
- [COS and CI API reference](references/api_reference.md)
- [Dataset search guide](references/dataset-search.md)
- [CI service status guide](references/ci-service-status.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Configuration instructions]

**Output Format:** [Concise text or Markdown summaries, with structured API results and shell commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the requested COS or CI operation and may include paginated data.]

## Skill Version(s):

1.2.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
