## Description:

A token-efficient task routing and execution control skill for WorkBuddy, iMA Copilot, OpenClaw, QClaw, and other agent systems that classifies requests, selects Ask, Plan, Craft, or Expert mode, reduces unnecessary token usage, avoids large unconfirmed file edits, and improves task ROI through staged execution and confirmation gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afanmusic](https://clawhub.ai/user/afanmusic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this control-layer skill to classify ambiguous, file-sensitive, batch, or high-token requests before execution. It helps choose Ask, Plan, Craft, or Expert mode, set output depth, and require confirmation before broad or risky changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The control layer can add unnecessary routing or confirmation to simple, low-risk requests.

Mitigation: Enable it for ambiguous, file-touching, batch, high-token, or risky tasks; allow clear small tasks to proceed in Craft Mode.

Risk: Chinese-centric defaults and bilingual templates may not match every deployment language or channel.

Mitigation: Review and adapt prompts, confirmation choices, and default output lengths for the target agent environment before rollout.

Risk: Packaging metadata is inconsistent because server metadata reports MIT-0, README.en.md says MIT, and no LICENSE file is present in the artifact.

Mitigation: Confirm the intended license and add authoritative LICENSE and version metadata before redistribution.

## Reference(s):

- [README.en.md](README.en.md)
- [GUIDE.en.md](GUIDE.en.md)
- [CHANGELOG.md](CHANGELOG.md)
- [focus_activation_rules.md](references/focus_activation_rules.md)
- [mode_router.md](references/mode_router.md)
- [interactive_routing.md](references/interactive_routing.md)
- [file_safety_rules.md](references/file_safety_rules.md)
- [chat_confirmation_affordances.md](references/chat_confirmation_affordances.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown guidance with mode recommendations, confirmation prompts, and concise next-step instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Micro, Standard, Deep, and Artifact token budget modes; favors progressive delivery and confirmation gates for risky work.]

## Skill Version(s):

0.6.8 (source: server release metadata and CHANGELOG.md, released 2026-05-02)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
