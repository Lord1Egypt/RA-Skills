## Description:

Creates themed, multi-page newspapers from user stories, photos, and references, delivering page images, a print PDF, and a recoverable project.

This skill is ready for commercial/non-commercial use.

## Publisher:

[legithubhh](https://clawhub.ai/user/legithubhh)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and community organizers use the skill to turn stories, photographs, and visual references into coordinated themed newspaper issues, with page images, a print PDF, and a recoverable project archive.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Supplied photos may be sent to the selected image provider, and project archives retain source images and prompts.

Mitigation: Confirm the provider may receive the supplied photos and protect project files and archives accordingly.

Risk: Dependency versions and live image-provider behavior were not verified in the static review.

Mitigation: Use a separate environment with reviewed dependency versions and check provider behavior before use.

Risk: An approval record imported from an existing project does not represent fresh permission for a new change.

Mitigation: Keep the approval checkpoints unless the user explicitly delegates them, and do not treat imported approvals as new authorization.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/legithubhh/skills/shiguang-newspaper)
- [Editorial workflow](references/editorial-workflow.md)
- [Image treatment](references/image-treatment.md)
- [Project tools and recovery](references/project-tools.md)
- [Execution and recovery guidance](references/execution-and-recovery.md)
- [Example newspaper issue](examples/kite-town/README.md)

## Skill Output:

**Output Type(s):** [Guidance, Images, PDF files, Project files]

**Output Format:** [Newspaper page images, a print PDF, and a .newspaper.zip project archive, with planning guidance]

**Output Parameters:** [Multi-page issue; page count, paper size, and orientation are chosen for each request]

**Other Properties Related to Output:** [Requires host image reading/generation or editing and file-saving capabilities for finished artwork; page text is part of rasterized images rather than individually editable typesetting.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
