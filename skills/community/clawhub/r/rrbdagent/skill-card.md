## Description:

OpenClaw skill for RRBD Admin that uses natural-language prompts to call RRBD backend APIs and automate account, digital-human, and video-generation tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zengjwmail](https://clawhub.ai/user/zengjwmail)

### License/Terms of Use:

MIT-0

## Use Case:

External RRBD users and operators use this skill to log in, inspect digital-human assets, list videos, and create RRBD videos through guided natural-language interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill targets a real RRBD admin backend and can execute authenticated account and video operations.

Mitigation: Install only after confirming the RRBD account, tenant, and allowed task scope; narrow invocation to explicit RRBD requests.

Risk: The package stores passwords in plaintext and includes runnable scripts with hardcoded account credentials.

Mitigation: Remove password persistence, delete and rotate exposed credentials, and require runtime credential entry or a secure secret store before use.

Risk: Runtime history files and media URLs are included in the release.

Mitigation: Exclude runtime memory/history files from packaged releases and treat shipped media URLs as already disclosed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zengjwmail/skills/rrbdagent)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and console text with generated API results, setup guidance, and runnable JavaScript or Python command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call authenticated RRBD APIs and return video URLs or status information.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
