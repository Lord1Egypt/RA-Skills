## Description: <br>
Object storage operations for Volcengine TOS. Use when users need upload/download/sync, bucket policy checks, signed URLs, or storage troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to manage Volcengine TOS buckets and objects, including uploads, downloads, sync tasks, bucket policy checks, signed URLs, and storage troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate on Volcengine TOS buckets and objects using user-provided cloud credentials. <br>
Mitigation: Use least-privilege credentials scoped to only the required buckets and actions. <br>
Risk: Object storage operations can be destructive when they delete or overwrite bucket contents. <br>
Mitigation: Require explicit confirmation before destructive actions and review the target bucket, region, and object paths before execution. <br>


## Reference(s): <br>
- [Sources](references/sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with operation steps, result manifests, object keys, URLs, and verification notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include checksum or size verification where available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
