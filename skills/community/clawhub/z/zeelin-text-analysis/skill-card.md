## Description:

Zeelin Text Analysis uploads local text files to the Zeelin service, submits asynchronous text analysis jobs, polls for completion, and formats extracted entities, relationship graphs, and character profiles as Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liyayong000-sketch](https://clawhub.ai/user/liyayong000-sketch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to send local novels or documents to Zeelin for text analysis, then receive structured Markdown summaries of entities, relationships, and character profiles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends uploaded documents and the Zeelin App-Key through a plaintext HTTP service endpoint.

Mitigation: Avoid entering a real App-Key until the service uses HTTPS with a verified domain, and rotate any App-Key previously used through the plaintext endpoint.

Risk: Documents are sent to the Zeelin service and OSS storage, with privacy and retention controls not established in the evidence.

Mitigation: Use only documents that are acceptable to send to the provider, and do not submit confidential material unless the provider documents acceptable security and retention terms.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liyayong000-sketch/skills/zeelin-text-analysis)
- [Zeelin platform](https://skills.zeelin.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with configuration JSON and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an md file-style analysis view after the external task succeeds; results should be based only on fields returned by the Zeelin service.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
