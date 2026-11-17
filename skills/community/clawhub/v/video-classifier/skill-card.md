## Description:

Classifies unstructured long videos by selecting matching records in a staff video backend and applying user-provided tags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wulooongcha](https://clawhub.ai/user/wulooongcha)

### License/Terms of Use:

MIT-0

## Use Case:

Authorized staff operators or agents use this skill to classify unstructured long videos by filtering backend records and applying a requested tag to a requested number of videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bulk browser automation can apply tags to more videos than requested or to the wrong records in a logged-in staff video backend.

Mitigation: Preview affected records, enforce the requested count, log affected IDs, and require explicit confirmation before clicking the final confirm action.

Risk: The workflow can change records in the target staff video backend.

Mitigation: Run it only from an account authorized to modify that backend and verify the session before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wulooongcha/skills/video-classifier)

## Skill Output:

**Output Type(s):** [Guidance, Text, Browser actions]

**Output Format:** [Step-by-step browser automation workflow with concise status updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an authenticated, authorized session before changing video tags.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
