## Description:

Verify the optional local Switchyard runtime path without changing Campus-owned response semantics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaojiou176](https://clawhub.ai/user/xiaojiou176)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to check whether a local Switchyard runtime is ready and, when it is, route through the Campus consumer seam while preserving Campus response fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the chat route may send prompts through whichever provider the local runtime is configured to use.

Mitigation: Confirm the local API endpoint and configured provider are controlled or trusted before sending prompts.

Risk: Bypassing Campus response semantics could expose raw upstream provider payloads or misrepresent runtime capabilities.

Mitigation: Keep outputs within the documented Campus fields and do not describe the runtime as hosted autonomy or a write-capable agent runtime.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xiaojiou176/skills/switchyard-runtime-check)
- [ClawHub Publisher Profile](https://clawhub.ai/user/xiaojiou176)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands]

**Output Format:** [Markdown with inline API routes and response field names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves Campus response semantics and avoids exposing raw upstream provider payloads.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
