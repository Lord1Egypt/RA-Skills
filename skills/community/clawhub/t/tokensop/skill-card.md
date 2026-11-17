## Description:

TOKEN SOP caches successful browser workflows locally and can retrieve or contribute reusable cloud workflows so agents can replay repeated tasks with lower token use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ainclaw](https://clawhub.ai/user/ainclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to intercept repeated OpenClaw browser intents, replay matching Lobster workflows from a local cache or cloud match, and compile successful sessions into reusable workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic replay of cached workflows can act in authenticated browsers, business applications, financial systems, admin consoles, or private sites.

Mitigation: Review before installation on sensitive sites, require user approval for remote workflow execution, and restrict use where replayed browser actions could cause material changes.

Risk: The skill can upload workflow context to a cloud endpoint by default when successful sessions are completed.

Mitigation: Make cloud contribution opt-in, disable auto_contribute for sensitive workflows, and confirm sanitization behavior before enabling sharing.

Risk: Local and cloud workflow matching may reuse workflows in the wrong context if trust and origin boundaries are too broad.

Mitigation: Require trusted workflow sources, bind matches to origin and page structure, and fall back to normal agent execution when validation or context checks fail.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ainclaw/skills/tokensop)
- [Publisher Profile](https://clawhub.ai/user/ainclaw)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Code]

**Output Format:** [Agent responses, Lobster workflow commands, local JSON workflow records, and cloud API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May replay cached browser workflows, save workflow JSON under the configured local store, and send workflow match or contribution payloads to the configured cloud endpoint.]

## Skill Version(s):

5.6.5 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
