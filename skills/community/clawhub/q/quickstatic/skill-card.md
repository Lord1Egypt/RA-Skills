## Description:

QuickStatic Skills helps agents publish, update, query, and delete anonymous public static sites through the QuickStatic API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[h5box](https://clawhub.ai/user/h5box)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to package a static site as a zip, publish it to a public URL, manage a stable site_key for updates, check site status, and intentionally delete a published site.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded zip contents are sent to an external service and become publicly reachable.

Mitigation: Review site contents before upload and avoid publishing private, sensitive, or unlicensed material.

Risk: A site_key can update or delete the associated public site.

Mitigation: Keep each site_key private and reuse it only for intentional updates to the same project.

Risk: Delete calls remove the public site.

Mitigation: Run the delete call only when removal is intended and confirm the target site_key first.

## Reference(s):

- [QuickStatic ClawHub listing](https://clawhub.ai/h5box/skills/quickstatic)
- [QuickStatic API base](https://667661.xyz)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces API usage guidance for zip upload, custom slug handling, lifecycle checks, error handling, and delete operations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
