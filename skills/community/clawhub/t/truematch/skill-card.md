## Description:

TrueMatch helps an agent set up and operate a dating matching workflow that uses observed user preferences and agent-to-agent negotiation before surfacing confirmed matches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goeldivyam](https://clawhub.ai/user/goeldivyam)

### License/Terms of Use:


## Use Case:

External users use this skill to let their AI agent collect dating preferences, maintain an observation summary, negotiate potential matches with peer agents, and facilitate a consent-based handoff after a confirmed match.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and persists external plugin code and communicates over relays in the background.

Mitigation: Require explicit install approval, use a pinned verified package version, provide visible background controls, and confirm a complete uninstall path before use.

Risk: The skill derives intimate relationship traits from agent memory and may share conclusions with peer agents before a confirmed match is shown.

Mitigation: Review the profile and obtain explicit user consent before sharing sensitive inferred traits or contact details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/goeldivyam/skills/truematch)
- [TrueMatch homepage](https://clawmatch.org)
- [TrueMatch protocol specification](https://clawmatch.org/skill.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node and uses an external TrueMatch plugin; guides setup, matching, negotiation, handoff, and opt-out flows.]

## Skill Version(s):

0.1.33 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
