## Description:

Helps an agent call the Runware API correctly by inspecting model schemas, using valid request fields, choosing synchronous or asynchronous execution by modality, and reading returned results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runware](https://clawhub.ai/user/runware)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when preparing real Runware generation calls across image, video, audio, 3D, training, or text workflows. It helps them choose the correct model identity and task type, validate request fields against the model schema, use the right delivery mode, and account for cost before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may send files or media to Runware while following this skill.

Mitigation: Review the files, media, URLs, or base64 inputs before asking the agent to send them to Runware.

Risk: Large or repeated generation batches may create unexpected Runware API costs.

Mitigation: Use dry runs or includeCost before committing to costly batches.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Guidance, Code, Configuration]

**Output Format:** [Markdown guidance with inline API fields, headers, model identifiers, and SDK or CLI references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable files are included; the skill guides agents that may make Runware API calls.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
