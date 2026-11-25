## Description:

World Heritage knowledge base Q&A covering heritage sites, inscription, history, values, conservation and recent updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tencent-adm](https://clawhub.ai/user/tencent-adm)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask about World Heritage sites, their locations, inscription, history, significance, conservation, and recent updates. The skill returns knowledge-base answers and provides setup or failure guidance when its query service is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release pairs its heritage-information purpose with an unverified remote CLI installer and unrelated CLI and credential operations; analysis of two scripts is incomplete.

Mitigation: Avoid installation until those operations are explained and the remote installer is independently verified; the available scan does not establish that the artifact is safe or malicious.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/tencent-adm/skills/tencent-news-world-heritage)
- [CLI environment and failure handling](artifact/references/cli-environment.md)
- [CLI integration guide](artifact/references/cli-integration.md)
- [Installation guide](artifact/references/installation-guide.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Knowledge-base answer text; structured JSON for environment failures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers are presented from the knowledge-base response; setup and failure guidance may also be provided.]

## Skill Version(s):

1.0.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
