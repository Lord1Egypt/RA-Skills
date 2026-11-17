## Description:

Walk one platform from the visibility catalog end to end for this project - re-check the live submission page, build the artifacts it needs, run the publish step after an explicit yes, hand the account, payment, DNS and form steps to the user, then verify the listing and update the ledger.

This skill is ready for commercial/non-commercial use.

## Publisher:

[orensegal](https://clawhub.ai/user/orensegal)

### License/Terms of Use:

MIT-0

## Use Case:

Project maintainers use this skill to prepare and manage a listing on one selected platform, including building submission materials, verifying the live listing, and tracking its status. It leaves account, payment, DNS, and form-entry tasks to the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install or download steps may run code from external sources.

Mitigation: Review the exact command and source/version first, and follow the skill's explicit approval step before running it.

Risk: Publishing or uploading listing materials can make content public.

Mitigation: Review the materials and approve the exact outward-facing step before it runs.

## Reference(s):

- [Project homepage](https://github.com/OrenSegal/visibility)
- [Reviewed platform catalog revision](https://raw.githubusercontent.com/OrenSegal/visibility/1478fbd3497cdac199bdec02b8119188fdc29083/skills/plan/catalog.json)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Files, Shell commands]

**Output Format:** [Markdown guidance, command suggestions, and platform submission artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Varies by platform; may include a checklist of steps for the user.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
