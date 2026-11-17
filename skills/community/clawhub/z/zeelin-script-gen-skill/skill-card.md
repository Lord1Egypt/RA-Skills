## Description:

剧本生成技能V4 converts uploaded novels or story files into structured film and storyboard scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liyayong000-sketch](https://clawhub.ai/user/liyayong000-sketch)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to upload manuscript files and request conversion into character profiles, episode outlines, and storyboard-style script content. It is intended for script-generation workflows that depend on the Zeelin service and user-provided App-Key configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Manuscripts and the Zeelin App-Key may be sent to a raw HTTP service endpoint without transport protection.

Mitigation: Use only non-sensitive manuscripts and avoid real credentials until the service uses HTTPS with an authenticated hostname.

Risk: Submitting generation tasks can consume Zeelin account quota.

Mitigation: Confirm expected cost and polling behavior before submitting tasks, especially for long manuscripts.

Risk: The artifact does not provide a clear privacy or retention policy for uploaded manuscripts.

Mitigation: Do not upload private or unpublished text unless the service's privacy and retention terms are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liyayong000-sketch/skills/zeelin-script-gen-skill)
- [Zeelin website](https://skills.zeelin.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell command examples and generated script summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce downloadable Markdown script files after polling the Zeelin task status.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
